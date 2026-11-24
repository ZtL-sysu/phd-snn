import json
import statistics
import sys
from pathlib import Path

import numpy as np
import torch

run = Path(__file__).resolve().parent
sys.path.insert(0, str(run / "src"))
from structure_conversion import load_images

seeds = (41, 42, 43)
n_boot = 20000
rng = np.random.default_rng(20261118)
_, test_labels = load_images(run / "data/fashion_mnist_test.parquet")
labels_np = test_labels[:2000].numpy().astype(np.int64)


def load(path):
    value = torch.load(path, map_location="cpu", weights_only=False)
    return value.numpy().astype(np.int64)


per_seed = {}
for seed in seeds:
    v1 = load(run / f"fm_v1_predictions_seed{seed}.pt")
    v2 = load(run / f"fm_v2_predictions_seed{seed}.pt")
    labels = labels_np
    diff = (v2 == labels).astype(np.float64) - (v1 == labels).astype(np.float64)
    per_seed[seed] = {
        "n": int(len(diff)),
        "mean": float(diff.mean()),
        "v1_accuracy": float((v1 == labels).mean()),
        "v2_accuracy": float((v2 == labels).mean()),
        "diff": diff,
    }

all_diffs = np.concatenate([per_seed[seed]["diff"] for seed in seeds])
flat_boot = np.empty(n_boot, dtype=np.float64)
for index in range(n_boot):
    sample = rng.choice(all_diffs, size=len(all_diffs), replace=True)
    flat_boot[index] = sample.mean()

hierarchical_boot = np.empty(n_boot, dtype=np.float64)
seed_means = np.array([per_seed[seed]["mean"] for seed in seeds], dtype=np.float64)
for index in range(n_boot):
    drawn_seeds = rng.integers(0, len(seeds), size=len(seeds))
    hierarchical_boot[index] = seed_means[drawn_seeds].mean()

report = {
    "purpose": "Seed-aware difference analysis for v2 minus v1 on Fashion-MNIST",
    "source": "fm_v1_predictions_seed*.pt, fm_v2_predictions_seed*.pt, data/fashion_mnist_test.parquet labels",
    "label_source_correction": "fm_predictions_seed*.pt stores teacher predictions, not ground-truth labels; the first run was invalid and is superseded.",
    "difference": "per-example correctness(v2) - correctness(v1)",
    "seeds": list(seeds),
    "per_seed": {str(seed): {key: value for key, value in per_seed[seed].items() if key != "diff"}
                 for seed in seeds},
    "pooled_example_bootstrap": {
        "n": int(len(all_diffs)),
        "mean": float(all_diffs.mean()),
        "se": float(all_diffs.std(ddof=1) / np.sqrt(len(all_diffs))),
        "ci95": [float(np.quantile(flat_boot, 0.025)), float(np.quantile(flat_boot, 0.975))],
        "warning": "Treats seeds as exchangeable examples and ignores seed clustering.",
    },
    "hierarchical_seed_bootstrap": {
        "n_seeds": len(seeds),
        "mean": float(seed_means.mean()),
        "sd": float(seed_means.std(ddof=1)),
        "se": float(seed_means.std(ddof=1) / np.sqrt(len(seeds))),
        "ci95": [float(np.quantile(hierarchical_boot, 0.025)), float(np.quantile(hierarchical_boot, 0.975))],
        "warning": "Only three seed units; interval is coarse and should not be presented as a precise frequentist confidence interval.",
    },
    "bootstrap_replicates": n_boot,
    "random_seed": 20261118,
}
path = run / "hierarchical-bootstrap-results.json"
path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
