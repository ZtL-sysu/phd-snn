"""C10-v1 frozen smoke: train-only operator-factor selection on local graph checkpoints."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from smoke.operator_calibration import evaluate_factor, fit_operator_factor, teacher_logits


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]
CORE_ROOT = (
    WORKSPACE
    / "auto-paper"
    / "20261028-171500"
    / "Spiking-GNN-Conversion"
    / "f-research-v1-run-20261028-174053-gnn-snn-conv"
)
MODEL_ROOT = (
    WORKSPACE
    / "auto-paper"
    / "20261105-111502"
    / "Intra-Aggregation-Misalignment-Graph-Conversion"
    / "f-research-v1-run-20261105-111502-gnn2snn"
    / "results"
    / "models"
)
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


HOSTS_BY_DATASET = {
    "chameleon": ("H1_mean", "H2_sum", "H3_sym"),
    "squirrel": ("H1_mean", "H3_sym"),
}
SEEDS = (0, 1, 2, 3)
FACTORS = (0.5, 0.65, 0.8, 1.0, 1.25, 1.5, 2.0)


def load_checkpoint(path: Path, data: dict) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        model = {
            "Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()],
            "bs_layers": [archive["bs0"].copy()],
            "b_out": archive["b_out"].copy(),
            "n_layers": int(archive["n_layers"]),
            "alpha": float(archive["alpha"]),
            "beta_idm": 0.0,
            "seed": int(archive["seed"]),
        }
    first = np.maximum(np.asarray(data["adj"] @ data["X"], dtype=np.float32) @ model["Ms"][0] + model["bs_layers"][0], 0.0)
    model["Hs"] = [first]
    return model


def bootstrap_accuracy(a_logits: np.ndarray, b_logits: np.ndarray, labels: np.ndarray, draws: int = 2000, seed: int = 20261117) -> dict:
    rng = np.random.default_rng(seed)
    n = len(labels)
    deltas = np.empty(draws)
    for index in range(draws):
        take = rng.integers(0, n, size=n)
        deltas[index] = 100 * (
            np.mean(np.argmax(a_logits[take], axis=1) == labels[take])
            - np.mean(np.argmax(b_logits[take], axis=1) == labels[take])
        )
    return {"mean_pp": float(np.mean(deltas)), "lower_95_pp": float(np.quantile(deltas, 0.025)), "upper_95_pp": float(np.quantile(deltas, 0.975))}


def evaluate_model(data: dict, path: Path, host: str, seed: int) -> dict:
    model = load_checkpoint(path, data)
    target = teacher_logits(data, model)
    fit = fit_operator_factor(
        data=data, model=model, target_logits=target, train_mask=data["train"],
        factors=FACTORS, t_steps=2, convert=core.convert,
    )
    baseline = evaluate_factor(data=data, model=model, target_logits=target, mask=data["val"], factor=1.0, t_steps=2, convert=core.convert)
    proposed = evaluate_factor(data=data, model=model, target_logits=target, mask=data["val"], factor=fit["factor"], t_steps=2, convert=core.convert)
    random_factor = FACTORS[int(np.random.default_rng(20261117 + seed).integers(len(FACTORS)))]
    random = evaluate_factor(data=data, model=model, target_logits=target, mask=data["val"], factor=random_factor, t_steps=2, convert=core.convert)
    labels = np.asarray(data["y"])[data["val"]]
    return {
        "host": host, "seed": seed, "checkpoint": str(path),
        "fit": fit,
        "baseline": {k: v for k, v in baseline.items() if k != "logits"},
        "proposed": {k: v for k, v in proposed.items() if k != "logits"},
        "random_factor": random_factor,
        "random": {k: v for k, v in random.items() if k != "logits"},
        "paired_bootstrap": bootstrap_accuracy(proposed["logits"], baseline["logits"], labels),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    rows = []
    for dataset in ("chameleon", "squirrel"):
        data = core.load(dataset, str(CORE_ROOT / "results" / ".data"))
        for host in HOSTS_BY_DATASET[dataset]:
            for seed in SEEDS:
                path = MODEL_ROOT / f"{dataset}__{host}__s{seed}.npz"
                if not path.is_file():
                    raise FileNotFoundError(path)
                row = evaluate_model(data, path, host, seed)
                row["dataset"] = dataset
                rows.append(row)
                print(json.dumps({k: row[k] for k in ("dataset", "host", "seed", "baseline", "proposed", "random", "paired_bootstrap")}, default=float), flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
