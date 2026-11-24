import json, sys, time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from structure_conversion import load_images

run = Path(__file__).resolve().parent
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class SmallViGTeacher(nn.Module):
    def __init__(self, patch=4, hidden=64, k=9, classes=10):
        super().__init__()
        self.patch = patch
        self.k = k
        self.grid = 28 // patch
        self.embed = nn.Linear(patch * patch, hidden)
        self.graph_norm = nn.LayerNorm(hidden)
        self.message = nn.Linear(hidden, hidden)
        self.update = nn.Sequential(nn.Linear(hidden * 2, hidden), nn.LayerNorm(hidden), nn.ReLU())
        self.head = nn.Sequential(nn.Linear(hidden, 64), nn.ReLU(), nn.Linear(64, classes))

    def forward(self, images):
        batch = images.size(0)
        nodes = images.unfold(1, self.patch, self.patch).unfold(2, self.patch, self.patch)
        nodes = nodes.contiguous().view(batch, self.grid * self.grid, self.patch * self.patch)
        features = F.normalize(F.relu(self.embed(nodes)), dim=-1)
        similarities = torch.bmm(features, features.transpose(1, 2))
        mask = torch.eye(features.size(1), device=features.device).unsqueeze(0)
        similarities = similarities - 1e4 * mask
        indices = similarities.topk(self.k, dim=-1).indices
        row = torch.arange(batch, device=features.device).view(batch, 1, 1).expand(batch, features.size(1), self.k)
        neighbors = features[row, indices]
        messages = F.relu(self.message(neighbors - features.unsqueeze(2)))
        pooled = messages.max(dim=2).values
        updated = self.update(torch.cat([features, pooled], dim=-1))
        features = self.graph_norm(features + updated)
        return self.head(features.mean(dim=1)), features


def seed_all(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def batches(images, labels, size, shuffle, seed=0):
    generator = torch.Generator().manual_seed(seed)
    order = torch.randperm(len(images), generator=generator).tolist() if shuffle else list(range(len(images)))
    for start in range(0, len(order), size):
        idx = torch.tensor(order[start:start + size])
        yield images[idx].to(device), labels[idx].to(device)


def train_one(seed, train_images, train_labels, val_images, val_labels, epochs=8, batch_size=128):
    seed_all(seed)
    model = SmallViGTeacher().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    best = -1.0
    best_state = None
    history = []
    for epoch in range(epochs):
        model.train()
        total = 0.0
        for images, labels in batches(train_images, train_labels, batch_size, True, seed + epoch):
            logits, _ = model(images)
            loss = F.cross_entropy(logits, labels)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            total += float(loss.item()) * images.size(0)
        scheduler.step()
        model.eval()
        correct = 0
        with torch.no_grad():
            for images, labels in batches(val_images, val_labels, 256, False):
                logits, _ = model(images)
                correct += int((logits.argmax(1) == labels).sum())
        acc = correct / len(val_images)
        history.append({"epoch": epoch + 1, "loss": total / len(train_images), "val_acc": acc})
        if acc > best:
            best = acc
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
    model.load_state_dict(best_state)
    return model, best, history


def main():
    started = time.time()
    train_images, train_labels = load_images(run / "data/fashion_mnist_train.parquet")
    val_start, val_end = 55000, 60000
    val_images, val_labels = train_images[val_start:val_end], train_labels[val_start:val_end]
    fit_images, fit_labels = train_images[:val_start], train_labels[:val_start]
    results = []
    for seed in (41, 42, 43):
        model, best_acc, history = train_one(seed, fit_images, fit_labels, val_images, val_labels)
        path = run / f"teacher_seed{seed}.pt"
        torch.save({"state_dict": model.state_dict(), "seed": seed, "best_val_acc": best_acc}, path)
        results.append({"seed": seed, "best_val_acc": best_acc, "checkpoint": path.name, "history": history})
        print(f"seed {seed}: best_val_acc={best_acc:.4f}")
    report = {"device": str(device), "wall_seconds": time.time() - started, "results": results}
    (run / "teacher-training-results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
