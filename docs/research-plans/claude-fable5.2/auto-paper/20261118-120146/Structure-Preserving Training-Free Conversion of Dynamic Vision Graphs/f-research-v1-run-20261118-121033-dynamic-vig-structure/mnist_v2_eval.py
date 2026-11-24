import json, sys, time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from structure_conversion import load_images
from v2_message_calibration import graph_message, forward_with_codes
from train_teacher import SmallViGTeacher

run = Path(__file__).resolve().parent
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_teacher(seed):
    state = torch.load(run / f"mnist_teacher_seed{seed}.pt", map_location=device, weights_only=False)
    model = SmallViGTeacher().to(device)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model


def teacher_features(model, images):
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(images.size(0), model.grid * model.grid, model.patch * model.patch)
    return torch.nn.functional.normalize(torch.relu(model.embed(nodes)), dim=-1).detach()


def encode(values, scale, offset):
    centered = (values + offset).clamp(-1, 1)
    quantized = torch.round(((centered + 1) / 2) * scale) / scale
    return 2 * quantized - 1 - offset


def mse(features, codes, model):
    return float(((graph_message(model, features) - graph_message(model, codes)) ** 2).mean())


def evaluate_seed(seed, train_images, test_images, test_labels):
    model = load_teacher(seed)
    cal_features = teacher_features(model, train_images[:5000].to(device))
    best = None
    for scale in (5.0, 7.0, 9.0, 11.0, 15.0):
        for offset in (0.0, 0.05, 0.10):
            loss = mse(cal_features, encode(cal_features, scale, offset), model)
            if best is None or loss < best["message_mse"]:
                best = {"scale": scale, "offset": offset, "message_mse": loss}
    images = test_images[:2000].to(device)
    targets = test_labels[:2000].to(device)
    features = teacher_features(model, images)
    teacher_logits, _ = forward_with_codes(model, images, features)
    v1_logits, _ = forward_with_codes(model, images, encode(features, 9.0, 0.0))
    v2_logits, _ = forward_with_codes(model, images, encode(features, best["scale"], best["offset"]))
    return {
        "seed": seed,
        "teacher_accuracy": float((teacher_logits.argmax(1) == targets).float().mean()),
        "v1_accuracy": float((v1_logits.argmax(1) == targets).float().mean()),
        "v2_accuracy": float((v2_logits.argmax(1) == targets).float().mean()),
        "v1_message_mse": mse(features, encode(features, 9.0, 0.0), model),
        "v2_message_mse": mse(features, encode(features, best["scale"], best["offset"]), model),
        "calibration": best,
        "events_equal": int((encode(features, 9.0, 0.0) != 0).sum()) == int((encode(features, best["scale"], best["offset"]) != 0).sum()),
    }


def main():
    started = time.time()
    train_images, _ = load_images(run / "data/mnist_train.parquet")
    test_images, test_labels = load_images(run / "data/mnist_test.parquet")
    rows = [evaluate_seed(seed, train_images, test_images, test_labels) for seed in (41, 42, 43)]
    out = {"dataset": "MNIST", "wall_seconds": time.time() - started, "rows": rows}
    (run / "mnist-v2-results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row))


if __name__ == "__main__":
    main()
