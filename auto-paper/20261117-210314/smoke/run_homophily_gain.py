"""HOM-C17-v1 held-out-seed grouped confirmation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

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
    high = ("cora", "citeseer", "pubmed")
    low = ("chameleon", "squirrel")
    rows = []
    for seed in (4, 5, 6):
        deltas = {}
        for dataset in high + low:
            data = core.load(dataset, str(CORE_ROOT / "results/.data"))
            model = load_model(MODEL_ROOT / f"{dataset}__H1_mean__s{seed}.npz", data)
            values = {}
            for t_steps in (2, 4):
                logits = core.convert(data, model, T=t_steps, return_logits=True)["logits"][data["val"]]
                values[t_steps] = float(np.mean(np.argmax(logits, axis=1) == data["y"][data["val"]]))
            deltas[dataset] = 100 * (values[4] - values[2])
        high_mean = float(np.mean([deltas[name] for name in high]))
        low_mean = float(np.mean([deltas[name] for name in low]))
        difference = high_mean - low_mean
        rows.append({"seed": seed, "deltas_pp": deltas, "high_mean_pp": high_mean, "low_mean_pp": low_mean, "difference_pp": difference, "seed_pass": difference >= 5.0})
        print(json.dumps(rows[-1]), flush=True)
    passing = sum(row["seed_pass"] for row in rows)
    result = {"rows": rows, "passing_seeds": passing, "gate_pass": passing >= 2}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passing_seeds": passing, "gate_pass": result["gate_pass"]}, indent=2))


if __name__ == "__main__":
    main()
