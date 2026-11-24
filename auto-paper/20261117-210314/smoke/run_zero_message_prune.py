"""ZERO-C10-v1 smoke driver."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from smoke.zero_message_prune import prune_zero_rows, zero_message_mask


WORKSPACE = Path(__file__).resolve().parents[3]
CORE_ROOT = WORKSPACE / "auto-paper" / "20261028-171500" / "Spiking-GNN-Conversion" / "f-research-v1-run-20261028-174053-gnn-snn-conv"
MODEL_ROOT = WORKSPACE / "auto-paper" / "20261105-111502" / "Intra-Aggregation-Misalignment-Graph-Conversion" / "f-research-v1-run-20261105-111502-gnn2snn/results/models"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


def load_model(path: Path, data: dict) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        model = {
            "Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()],
            "bs_layers": [archive["bs0"].copy()],
            "b_out": archive["b_out"].copy(),
            "n_layers": 2,
            "alpha": float(archive["alpha"]),
            "beta_idm": 0.0,
        }
    model["Hs"] = [np.maximum(np.asarray(data["adj"] @ data["X"]) @ model["Ms"][0] + model["bs_layers"][0], 0.0)]
    return model


def run_dataset(dataset: str) -> dict:
    data = core.load(dataset, str(CORE_ROOT / "results/.data"))
    model = load_model(MODEL_ROOT / f"{dataset}__H1_mean__s0.npz", data)
    counts, _, _, _ = core.simulate_counts(data, model, T=2, theta=1.0)
    mask = zero_message_mask(counts[0])
    hidden_rate = counts[0] / 2.0
    original_message = np.asarray(data["adj"] @ (hidden_rate @ model["Ms"][1])) + model["b_out"]
    pruned_hidden = prune_zero_rows(hidden_rate, mask)
    pruned_message = np.asarray(data["adj"] @ (pruned_hidden @ model["Ms"][1])) + model["b_out"]
    error = float(np.max(np.abs(original_message - pruned_message)))
    zero_fraction = float(mask.mean())
    return {
        "dataset": dataset,
        "nodes": int(data["N"]),
        "T": 2,
        "zero_node_fraction": zero_fraction,
        "message_slot_reduction": zero_fraction,
        "pruned_vs_original_logit_max_error": error,
        "gate": {"zero_fraction_pass": zero_fraction >= 0.10, "exact_pass": error <= 1e-10},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [run_dataset(dataset) for dataset in ("chameleon", "squirrel")]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
