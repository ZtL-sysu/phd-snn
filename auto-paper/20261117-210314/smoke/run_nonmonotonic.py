"""NM-C16-v1 held-out-seed confirmation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from smoke.operator_calibration import teacher_logits


WORKSPACE = Path(__file__).resolve().parents[3]
CORE_ROOT = WORKSPACE / "auto-paper" / "20261028-171500" / "Spiking-GNN-Conversion" / "f-research-v1-run-20261028-174053-gnn-snn-conv"
MODEL_ROOT = WORKSPACE / "auto-paper" / "20261105-111502" / "Intra-Aggregation-Misalignment-Graph-Conversion" / "f-research-v1-run-20261105-111502-gnn2snn/results/models"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


def load_model(path: Path, data: dict) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        model = {"Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()], "bs_layers": [archive["bs0"].copy()], "b_out": archive["b_out"].copy(), "n_layers": 2, "alpha": float(archive["alpha"]), "beta_idm": 0.0}
    model["Hs"] = [np.maximum(np.asarray(data["adj"] @ data["X"]) @ model["Ms"][0] + model["bs_layers"][0], 0.0)]
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    seed_rows = []
    for seed in (1, 2, 3):
        rows = []
        for dataset in ("cora", "citeseer", "pubmed", "chameleon", "squirrel", "ogbn-arxiv"):
            data = core.load(dataset, str(CORE_ROOT / "results/.data"))
            host = "H3_sym" if dataset == "ogbn-arxiv" else "H1_mean"
            path = MODEL_ROOT / f"{dataset}__{host}__s{seed}.npz"
            if not path.is_file():
                raise FileNotFoundError(path)
            model = load_model(path, data)
            val = data["val"]
            accuracies = {}
            for t_steps in (2, 4):
                logits = core.convert(data, model, T=t_steps, return_logits=True)["logits"][val]
                accuracies[str(t_steps)] = float(np.mean(np.argmax(logits, axis=1) == data["y"][val]))
            delta = 100 * (accuracies["4"] - accuracies["2"])
            rows.append({"dataset": dataset, "T2": accuracies["2"], "T4": accuracies["4"], "delta_pp": delta})
        positives = sum(row["delta_pp"] >= 1.0 for row in rows)
        negatives = sum(row["delta_pp"] <= -0.5 for row in rows)
        seed_rows.append({"seed": seed, "rows": rows, "positive_datasets": positives, "negative_datasets": negatives, "seed_pass": positives >= 3 and negatives >= 1})
        print(json.dumps(seed_rows[-1]), flush=True)
    passing = sum(row["seed_pass"] for row in seed_rows)
    result = {"seed_rows": seed_rows, "passing_seeds": passing, "gate_pass": passing >= 2}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passing_seeds": passing, "gate_pass": result["gate_pass"]}, indent=2))


if __name__ == "__main__":
    main()
