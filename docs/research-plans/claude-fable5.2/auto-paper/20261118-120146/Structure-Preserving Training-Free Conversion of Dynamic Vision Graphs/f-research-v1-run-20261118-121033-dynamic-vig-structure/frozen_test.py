import json, sys, time
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from structure_conversion import (
    load_images,
    matrix_knn_indices,
    matrix_winners,
    signed_multilevel_encode,
)
from train_teacher import SmallViGTeacher

run = Path(__file__).resolve().parent
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_teacher(seed):
    state = torch.load(run / f"teacher_seed{seed}.pt", map_location=device, weights_only=False)
    model = SmallViGTeacher().to(device)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model


def teacher_components(model, images):
    batch = images.size(0)
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(batch, model.grid * model.grid, model.patch * model.patch)
    features = F.normalize(F.relu(model.embed(nodes)), dim=-1)
    similarities = torch.bmm(features, features.transpose(1, 2))
    mask = torch.eye(features.size(1), device=features.device).unsqueeze(0)
    similarities = similarities - 1e4 * mask
    indices = similarities.topk(model.k, dim=-1).indices
    row = torch.arange(batch, device=features.device).view(batch, 1, 1).expand(batch, features.size(1), model.k)
    neighbors = features[row, indices]
    winners = (neighbors - features.unsqueeze(2)).argmax(dim=2)
    return features, indices, winners


def uniform_encode(values, levels):
    scale = float(levels - 1)
    quantized = torch.round(((values.clamp(-1, 1) + 1) / 2) * scale) / scale
    return 2 * quantized - 1


def evaluate(seed, images, labels, levels=16, limit=2000):
    model = load_teacher(seed)
    encoded_images = images[:limit].to(device)
    targets = labels[:limit].to(device)
    with torch.no_grad():
        teacher_logits, teacher_features = model(encoded_images)
        _, teacher_indices, teacher_winners = teacher_components(model, encoded_images)
        teacher_acc = float((teacher_logits.argmax(1) == targets).float().mean())

        signed_uniform = uniform_encode(teacher_features.detach(), levels)
        signed_events = int((signed_uniform != 0).sum())
        ml_codes, ml_events, _ = signed_multilevel_encode(teacher_features.detach(), levels=levels)

        rows = []
        for name, codes, events in [
            ("signed_uniform", signed_uniform, signed_events),
            ("signed_multilevel", ml_codes, ml_events),
        ]:
            enc_indices = matrix_knn_indices(codes, model.k)
            enc_winners = matrix_winners(codes, enc_indices)
            jac = []
            agreement = []
            for t_idx, e_idx, t_win, e_win in zip(teacher_indices, enc_indices, teacher_winners, enc_winners):
                a = {tuple(x) for x in t_idx.cpu().tolist()}
                b = {tuple(x) for x in e_idx.cpu().tolist()}
                jac.append(len(a & b) / len(a | b))
                agreement.append(float((t_win == e_win).float().mean()))
            rows.append({
                "seed": seed,
                "method": name,
                "teacher_accuracy": teacher_acc,
                "neighbor_jaccard": sum(jac) / len(jac),
                "winner_agreement": sum(agreement) / len(agreement),
                "events": events,
                "samples": limit,
            })
        return rows


def main():
    images, labels = load_images(run / "data/fashion_mnist_test.parquet")
    rows = []
    for seed in (41, 42, 43):
        rows.extend(evaluate(seed, images, labels, limit=2000))
    report = {
        "stage": "P4",
        "split": "Fashion-MNIST official test, first final evaluation after teacher selection",
        "seed_policy": "teacher seeds selected on validation only",
        "rows": rows,
    }
    (run / "frozen-test-results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row))


if __name__ == "__main__":
    main()
