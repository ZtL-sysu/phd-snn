"""READ-C18-v1 smoke driver."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from smoke.readout_pair import top2_pair_readout


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
    rows = []
    for dataset in ("cora", "citeseer", "pubmed", "chameleon", "squirrel", "ogbn-arxiv"):
        data = core.load(dataset, str(CORE_ROOT / "results/.data"))
        host = "H3_sym" if dataset == "ogbn-arxiv" else "H1_mean"
        model = load_model(MODEL_ROOT / f"{dataset}__{host}__s0.npz", data)
        logits = core.convert(data, model, T=2, return_logits=True)["logits"][data["val"]]
        pair = top2_pair_readout(logits)
        original = np.argmax(logits, axis=1)
        preserved = float(np.mean(pair["predictions"] == original))
        reduction = 1.0 - pair["output_slots_per_graph"] / pair["full_slots_per_graph"]
        rows.append({"dataset": dataset, "classes": int(logits.shape[1]), "graphs": int(len(logits)), "prediction_preservation": preserved, "output_slot_reduction": reduction, "median_margin": float(np.median(pair["margin"]))})
        print(json.dumps(rows[-1]), flush=True)
    median_reduction = float(np.median([row["output_slot_reduction"] for row in rows]))
    result = {"rows": rows, "median_output_slot_reduction": median_reduction, "gate_pass": all(row["prediction_preservation"] == 1.0 for row in rows) and median_reduction >= 0.50}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"median_output_slot_reduction": median_reduction, "gate_pass": result["gate_pass"]}, indent=2))


if __name__ == "__main__":
    main()
