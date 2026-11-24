import json, sys, time
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from structure_conversion import load_images
from train_teacher import SmallViGTeacher, seed_all, batches

run = Path(__file__).resolve().parent
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_mnist(seed, epochs=8):
    seed_all(seed)
    train_images, train_labels = load_images(run / "data/mnist_train.parquet")
    val_images, val_labels = train_images[55000:], train_labels[55000:]
    fit_images, fit_labels = train_images[:55000], train_labels[:55000]
    model = SmallViGTeacher().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    best = -1.0
    best_state = None
    history = []
    for epoch in range(epochs):
        model.train()
        for images, labels in batches(fit_images, fit_labels, 128, True, seed + epoch):
            logits, _ = model(images)
            loss = F.cross_entropy(logits, labels)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
        scheduler.step()
        model.eval()
        correct = 0
        with torch.no_grad():
            for images, labels in batches(val_images, val_labels, 256, False):
                logits, _ = model(images)
                correct += int((logits.argmax(1) == labels).sum())
        acc = correct / len(val_images)
        history.append({"epoch": epoch + 1, "val_acc": acc})
        if acc > best:
            best = acc
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
    model.load_state_dict(best_state)
    torch.save({"state_dict": model.state_dict(), "seed": seed, "best_val_acc": best}, run / f"mnist_teacher_seed{seed}.pt")
    return {"seed": seed, "best_val_acc": best, "history": history}


def main():
    started = time.time()
    rows = [train_mnist(seed) for seed in (41, 42, 43)]
    out = {"dataset": "MNIST", "device": str(device), "wall_seconds": time.time() - started, "results": rows}
    (run / "mnist-teacher-training-results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps({"seed": row["seed"], "best_val_acc": row["best_val_acc"]}))


if __name__ == "__main__":
    main()
