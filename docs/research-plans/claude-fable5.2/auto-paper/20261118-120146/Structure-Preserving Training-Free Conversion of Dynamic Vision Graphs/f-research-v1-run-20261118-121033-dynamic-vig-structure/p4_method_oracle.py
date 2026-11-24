import json, sys, time
from pathlib import Path

import torch
import torch.nn.functional as F

run = Path(__file__).resolve().parent
sys.path.insert(0, str(run / "src"))
sys.path.insert(0, str(run))
from structure_conversion import load_images, matrix_knn_indices, matrix_winners, signed_multilevel_encode
from train_teacher import SmallViGTeacher

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_teacher(seed):
    state = torch.load(run / f"teacher_seed{seed}.pt", map_location=device, weights_only=False)
    model = SmallViGTeacher().to(device)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model


def teacher_logits(model, images, features, indices, winners):
    batch = images.size(0)
    row = torch.arange(batch, device=device).view(batch, 1, 1).expand(batch, features.size(1), indices.size(-1))
    neighbors = features[row, indices]
    messages = F.relu(model.message(neighbors - features.unsqueeze(2)))
    pooled = messages.max(dim=2).values
    updated = model.update(torch.cat([features, pooled], dim=-1))
    updated_features = model.graph_norm(features + updated)
    return model.head(updated_features.mean(dim=1))


def teacher_state(model, images):
    batch = images.size(0)
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(batch, model.grid * model.grid, model.patch * model.patch)
    features = F.normalize(F.relu(model.embed(nodes)), dim=-1).detach()
    indices = matrix_knn_indices(features, model.k)
    winners = matrix_winners(features, indices)
    return features, indices, winners


def uniform_encode(values, levels, scale):
    normalized = ((values.clamp(-1, 1) + 1) / 2) * scale
    quantized = torch.round(normalized) / scale
    return 2 * quantized - 1


def calibrate_scale(teacher_features, images, targets, teacher_logits_ref):
    best = None
    for scale in (3.0, 5.0, 7.0, 9.0, 11.0, 15.0):
        codes = uniform_encode(teacher_features, 16, scale)
        indices = matrix_knn_indices(codes, 9)
        winners = matrix_winners(codes, indices)
        logits = teacher_logits(model_holder[0], images, codes, indices, winners)
        accuracy = float((logits.argmax(1) == targets).float().mean())
        agreement = float((teacher_winners_holder[0] == winners).float().mean())
        candidate = {"scale": scale, "accuracy": accuracy, "winner_agreement": agreement}
        if best is None or (agreement, accuracy) > (best["winner_agreement"], best["accuracy"]):
            best = candidate
    return best


model_holder = [None]
teacher_winners_holder = [None]


def evaluate_seed(seed, train_images, train_labels, test_images, test_labels, calibration_count=5000, test_limit=2000):
    global model_holder, teacher_winners_holder
    model = load_teacher(seed)
    model_holder = [model]
    cal_images = train_images[:calibration_count].to(device)
    cal_targets = train_labels[:calibration_count].to(device)
    cal_features, _, cal_winners = teacher_state(model, cal_images)
    teacher_winners_holder = [cal_winners]
    calibration = calibrate_scale(cal_features, cal_images, cal_targets, None)

    images = test_images[:test_limit].to(device)
    targets = test_labels[:test_limit].to(device)
    with torch.no_grad():
        teacher_features, teacher_indices, teacher_winners = teacher_state(model, images)
        teacher_acc = float((model(images)[0].argmax(1) == targets).float().mean())

        rows = []
        codes = uniform_encode(teacher_features, 16, calibration["scale"])
        indices = matrix_knn_indices(codes, model.k)
        winners = matrix_winners(codes, indices)
        converted_logits = teacher_logits(model, images, codes, indices, winners)
        converted_acc = float((converted_logits.argmax(1) == targets).float().mean())
        jac = sum(
            len({tuple(x) for x in a.tolist()} & {tuple(x) for x in b.tolist()}) / 9
            for a, b in zip(teacher_indices, indices)
        ) / len(indices)
        win_agree = float((teacher_winners == winners).float().mean())

        oracle_logits_teacher_features = teacher_logits(model, images, teacher_features, indices, winners)
        neighbor_oracle_logits = teacher_logits(model, images, teacher_features, teacher_indices, winners)
        both_oracle_logits = teacher_logits(model, images, teacher_features, teacher_indices, teacher_winners)

        rows.append({
            "seed": seed,
            "teacher_accuracy": teacher_acc,
            "converted_accuracy": converted_acc,
            "neighbor_jaccard": jac,
            "winner_agreement": win_agree,
            "calibration": calibration,
            "oracle_accuracy_with_winners": float((oracle_logits_teacher_features.argmax(1) == targets).float().mean()),
            "neighbor_oracle_accuracy": float((neighbor_oracle_logits.argmax(1) == targets).float().mean()),
            "both_oracle_accuracy": float((both_oracle_logits.argmax(1) == targets).float().mean()),
        })
        return rows


def main():
    started = time.time()
    train_images, train_labels = load_images(run / "data/fashion_mnist_train.parquet")
    test_images, test_labels = load_images(run / "data/fashion_mnist_test.parquet")
    rows = []
    for seed in (41, 42, 43):
        rows.extend(evaluate_seed(seed, train_images, train_labels, test_images, test_labels))
    out = {"stage": "P4", "wall_seconds": time.time() - started, "rows": rows}
    (run / "p4-method-oracle-results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row))


if __name__ == "__main__":
    main()

