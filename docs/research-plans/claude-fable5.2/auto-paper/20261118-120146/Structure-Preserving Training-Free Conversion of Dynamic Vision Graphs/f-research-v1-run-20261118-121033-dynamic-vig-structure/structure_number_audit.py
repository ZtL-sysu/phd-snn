import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

run = Path(__file__).resolve().parent
sys.path.insert(0, str(run / "src"))
sys.path.insert(0, str(run))
from structure_conversion import load_images, matrix_knn_indices, matrix_winners, signed_multilevel_encode
from train_teacher import SmallViGTeacher

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
seeds = (41, 42, 43)
limit = 2000


def load_model(seed):
    state = torch.load(run / f"teacher_seed{seed}.pt", map_location=device, weights_only=False)
    model = SmallViGTeacher().to(device)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model


def learned_features(model, images):
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(images.size(0), model.grid * model.grid, model.patch * model.patch)
    return F.normalize(F.relu(model.embed(nodes)), dim=-1).detach()


def learned_features_pre_norm(model, images):
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(images.size(0), model.grid * model.grid, model.patch * model.patch)
    return F.relu(model.embed(nodes)).detach()


def raw_patch_features(model, images):
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    return nodes.contiguous().view(images.size(0), model.grid * model.grid, model.patch * model.patch)


def encode(values, scale):
    quantized = torch.round(((values.clamp(-1, 1) + 1) / 2) * scale) / scale
    return 2 * quantized - 1


def jaccard(left, right):
    values = []
    for left_row, right_row in zip(left.reshape(-1, left.size(-1)), right.reshape(-1, right.size(-1))):
        left_set = {int(value) for value in left_row.tolist()}
        right_set = {int(value) for value in right_row.tolist()}
        values.append(len(left_set & right_set) / len(left_set | right_set))
    return sum(values) / len(values)


def overlap_at_k(left, right):
    values = []
    for left_row, right_row in zip(left.reshape(-1, left.size(-1)), right.reshape(-1, right.size(-1))):
        left_set = {int(value) for value in left_row.tolist()}
        right_set = {int(value) for value in right_row.tolist()}
        values.append(len(left_set & right_set) / len(left_set))
    return sum(values) / len(values)


def winner_agreement(left_features, left_indices, right_features, right_indices):
    row = torch.arange(left_features.size(0), device=device).view(-1, 1, 1).expand(-1, left_features.size(1), left_indices.size(-1))
    left_neighbors = left_features[row, left_indices]
    right_neighbors = right_features[row, right_indices]
    left_winners = (left_neighbors - left_features.unsqueeze(2)).argmax(dim=2)
    right_winners = (right_neighbors - right_features.unsqueeze(2)).argmax(dim=2)
    return float((left_winners == right_winners).float().mean())


def audit_one(seed, features, scale, images, targets):
    if features.shape[-1] == model_hidden:
        teacher_indices = matrix_knn_indices(F.normalize(features, dim=-1), 9)
        codes = encode(features, scale)
        encoded_indices = matrix_knn_indices(codes, 9)
    else:
        teacher_indices = matrix_knn_indices(features, 9)
        codes = encode(features, scale)
        encoded_indices = matrix_knn_indices(codes, 9)
    return {
        "seed": seed,
        "scale": scale,
        "jaccard": jaccard(teacher_indices, encoded_indices),
        "overlap_at_k": overlap_at_k(teacher_indices, encoded_indices),
        "winner_agreement": winner_agreement(features, teacher_indices, codes, encoded_indices),
        "teacher_neighbors_nonzero_fraction": float((features.abs() > 0).float().mean()),
        "encoded_zero_fraction": float((codes == 0).float().mean()),
    }


def strict_frozen_reproduction(seed, images):
    model = load_model(seed)
    teacher_logits, _ = model(images)
    del teacher_logits
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(images.size(0), model.grid * model.grid, model.patch * model.patch)
    features = F.normalize(F.relu(model.embed(nodes)), dim=-1)
    similarities = torch.bmm(features, features.transpose(1, 2))
    mask = torch.eye(features.size(1), device=device).unsqueeze(0)
    similarities = similarities - 1e4 * mask
    indices = similarities.topk(model.k, dim=-1).indices
    row = torch.arange(images.size(0), device=device).view(-1, 1, 1).expand(-1, features.size(1), model.k)
    neighbors = features[row, indices]
    winners = (neighbors - features.unsqueeze(2)).argmax(dim=2)
    del neighbors, row, similarities, mask, nodes

    signed_uniform = encode(features.detach(), 16.0)
    ml_codes, ml_events, _ = signed_multilevel_encode(features.detach(), levels=16)
    output = []
    for name, codes, events in (("signed_uniform", signed_uniform, int((signed_uniform != 0).sum())),
                                ("signed_multilevel", ml_codes, ml_events)):
        encoded_indices = matrix_knn_indices(codes, model.k)
        encoded_winners = matrix_winners(codes, encoded_indices)
        output.append({
            "seed": seed,
            "method": name,
            "jaccard": jaccard(indices.squeeze(-1), encoded_indices),
            "overlap_at_k": overlap_at_k(indices.squeeze(-1), encoded_indices),
            "winner_agreement": float((winners == encoded_winners).float().mean()),
            "events": events,
        })
    return output


def main():
    started = time.time()
    global model_hidden
    test_images, test_labels = load_images(run / "data/fashion_mnist_test.parquet")
    images = test_images[:limit].to(device)
    targets = test_labels[:limit].to(device)
    rows = []
    strict_rows = []
    for seed in seeds:
        strict_rows.extend(strict_frozen_reproduction(seed, images))
        model = load_model(seed)
        model_hidden = model.embed.out_features
        learned = learned_features(model, images)
        raw = raw_patch_features(model, images)
        for source, features, scale in (("learned_embedding_scale9", learned, 9.0),
                                        ("learned_pre_norm_scale9", learned_features_pre_norm(model, images), 9.0),
                                        ("raw_patch_scale15", raw, 15.0)):
            rows.append({"source": source, **audit_one(seed, features, scale, images, targets)})
    report = {
        "purpose": "Reconcile frozen-test structure metrics with P4 oracle metrics.",
        "split": "Fashion-MNIST official test, first 2000 examples; read-only re-analysis",
        "features": "teacher learned embeddings and raw 4x4 patches",
        "jaccard_definition": "mean |N_t ∩ N_e| / |N_t ∪ N_e| per node",
        "overlap_at_k_definition": "mean |N_t ∩ N_e| / k per node; this is the P4 oracle script's value labeled neighbor_jaccard",
        "strict_frozen_reproduction": strict_rows,
        "rows": rows,
        "wall_seconds": time.time() - started,
    }
    path = run / "structure-number-audit.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
