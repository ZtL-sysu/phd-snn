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
levels = 16


def load_teacher(seed):
    state = torch.load(run / f"teacher_seed{seed}.pt", map_location=device, weights_only=False)
    model = SmallViGTeacher().to(device)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model


def teacher_state(model, images):
    batch = images.size(0)
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(batch, model.grid * model.grid, model.patch * model.patch)
    features = F.normalize(F.relu(model.embed(nodes)), dim=-1).detach()
    return features


def graph_message(model, features):
    indices = matrix_knn_indices(features, model.k)
    row = torch.arange(features.size(0), device=features.device).view(features.size(0), 1, 1).expand(features.size(0), features.size(1), model.k)
    neighbors = features[row, indices]
    raw = F.relu(model.message(neighbors - features.unsqueeze(2)))
    return raw.max(dim=2).values


def forward_with_codes(model, images, codes):
    row = torch.arange(codes.size(0), device=codes.device).view(codes.size(0), 1, 1).expand(codes.size(0), codes.size(1), model.k)
    indices = matrix_knn_indices(codes, model.k)
    neighbors = codes[row, indices]
    messages = F.relu(model.message(neighbors - codes.unsqueeze(2))).max(dim=2).values
    updated = model.update(torch.cat([codes, messages], dim=-1))
    features = model.graph_norm(codes + updated)
    return model.head(features.mean(dim=1)), messages


def encode(values, scale, offset):
    centered = (values + offset).clamp(-1, 1)
    quantized = torch.round(((centered + 1) / 2) * scale) / scale
    return 2 * quantized - 1 - offset


def message_mse(teacher_features, codes, model, batch_size=256):
    total = 0.0
    count = 0
    for start in range(0, len(teacher_features), batch_size):
        target = graph_message(model, teacher_features[start:start + batch_size])
        pred = graph_message(model, codes[start:start + batch_size])
        total += float(((target - pred) ** 2).sum())
        count += target.numel()
    return total / count


def calibrate(model, cal_features, train_loss):
    best = None
    for scale in (5.0, 7.0, 9.0, 11.0, 15.0):
        for offset in (0.0, 0.05, 0.10):
            codes = encode(cal_features, scale, offset)
            loss = message_mse(cal_features, codes, model)
            candidate = {"scale": scale, "offset": offset, "message_mse": loss}
            if best is None or loss < best["message_mse"]:
                best = candidate
    return best


def evaluate_seed(seed, train_images, train_labels, test_images, test_labels):
    model = load_teacher(seed)
    cal_images = train_images[:5000].to(device)
    cal_features = teacher_state(model, cal_images)
    calib = calibrate(model, cal_features, None)

    images = test_images[:2000].to(device)
    targets = test_labels[:2000].to(device)
    teacher_features = teacher_state(model, images)
    teacher_logits, _ = forward_with_codes(model, images, teacher_features)
    teacher_acc = float((teacher_logits.argmax(1) == targets).float().mean())

    v1_codes = encode(teacher_features, 9.0, 0.0)
    v2_codes = encode(teacher_features, calib["scale"], calib["offset"])
    v1_logits, _ = forward_with_codes(model, images, v1_codes)
    v2_logits, _ = forward_with_codes(model, images, v2_codes)
    return {
        "seed": seed,
        "teacher_accuracy": teacher_acc,
        "v1_accuracy": float((v1_logits.argmax(1) == targets).float().mean()),
        "v2_accuracy": float((v2_logits.argmax(1) == targets).float().mean()),
        "v1_message_mse": message_mse(teacher_features, v1_codes, model),
        "v2_message_mse": message_mse(teacher_features, v2_codes, model),
        "calibration": calib,
        "v1_events": int((v1_codes != 0).sum()),
        "v2_events": int((v2_codes != 0).sum()),
    }


def main():
    started = time.time()
    train_images, train_labels = load_images(run / "data/fashion_mnist_train.parquet")
    test_images, test_labels = load_images(run / "data/fashion_mnist_test.parquet")
    rows = [evaluate_seed(seed, train_images, train_labels, test_images, test_labels) for seed in (41, 42, 43)]
    out = {"contract": "v2-message-exact", "wall_seconds": time.time() - started, "rows": rows}
    (run / "v2-message-calibration-results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row))


if __name__ == "__main__":
    main()
