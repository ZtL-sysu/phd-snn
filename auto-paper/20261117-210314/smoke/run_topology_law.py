"""LAW-C07-v1: descriptive topology/gap screen on local frozen graph checkpoints."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import scipy.sparse.linalg as spla

from smoke.operator_calibration import teacher_logits


WORKSPACE = Path(__file__).resolve().parents[3]
CORE_ROOT = WORKSPACE / "auto-paper" / "20261028-171500" / "Spiking-GNN-Conversion" / "f-research-v1-run-20261028-174053-gnn-snn-conv"
MODEL_ROOT = WORKSPACE / "auto-paper" / "20261105-111502" / "Intra-Aggregation-Misalignment-Graph-Conversion" / "f-research-v1-run-20261105-111502-gnn2snn/results/models"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402
import graph_data  # noqa: E402


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


def topology_statistics(data: dict) -> dict:
    adjacency = data["adj"].tocsr()
    labels = data["y"]
    degrees = np.diff(adjacency.indptr)
    entropy_terms = []
    for node in range(adjacency.shape[0]):
        row = adjacency.indices[adjacency.indptr[node] : adjacency.indptr[node + 1]]
        if len(row) <= 1:
            entropy_terms.append(0.0)
            continue
        neighbor_labels = labels[row]
        neighbor_labels = neighbor_labels[neighbor_labels >= 0]
        if neighbor_labels.size == 0:
            entropy_terms.append(0.0)
            continue
        counts = np.bincount(neighbor_labels, minlength=int(labels.max()) + 1).astype(float)
        probabilities = counts[counts > 0] / counts.sum()
        denominator = np.log(len(probabilities)) if len(probabilities) > 1 else 1.0
        entropy_terms.append(float(-(probabilities * np.log(probabilities)).sum() / denominator))
    try:
        spectral = float(spla.eigsh(adjacency, k=1, which="LM", return_eigenvectors=False)[0])
    except Exception:
        spectral = float(np.linalg.norm(adjacency.toarray(), ord=2))
    return {
        "edge_homophily": float(graph_data.edge_homophily(adjacency, labels)),
        "degree_entropy": float(np.mean(entropy_terms)),
        "normalized_spectral_radius": spectral,
        "mean_degree": float(np.mean(degrees)),
    }


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    def ranks(values):
        order = np.argsort(values)
        result = np.empty(len(values), dtype=float)
        result[order] = np.arange(len(values), dtype=float)
        return result
    return float(np.corrcoef(ranks(x), ranks(y))[0, 1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    rows = []
    for dataset in ("cora", "citeseer", "pubmed", "chameleon", "squirrel", "ogbn-arxiv"):
        data = core.load(dataset, str(CORE_ROOT / "results/.data"))
        host = "H3_sym" if dataset == "ogbn-arxiv" else "H1_mean"
        path = MODEL_ROOT / f"{dataset}__{host}__s0.npz"
        model = load_model(path, data)
        target = teacher_logits(data, model)
        val = data["val"]
        teacher_acc = float(np.mean(np.argmax(target[val], axis=1) == data["y"][val]))
        conversions = {}
        for t_steps in (2, 4):
            result = core.convert(data, model, T=t_steps, return_logits=True)
            logits = result["logits"][val]
            conversions[str(t_steps)] = {
                "accuracy": float(np.mean(np.argmax(logits, axis=1) == data["y"][val])),
                "teacher_agreement": float(np.mean(np.argmax(logits, axis=1) == np.argmax(target[val], axis=1))),
                "gap_pp": float(100 * (teacher_acc - np.mean(np.argmax(logits, axis=1) == data["y"][val]))),
                "spikes_per_node": float(result["spikes_per_node"]),
            }
        rows.append({"dataset": dataset, "teacher_accuracy": teacher_acc, "topology": topology_statistics(data), "conversion": conversions})
        print(json.dumps(rows[-1]), flush=True)
    stats = ("edge_homophily", "degree_entropy", "normalized_spectral_radius")
    correlations = {}
    for stat in stats:
        values = np.array([row["topology"][stat] for row in rows])
        correlations[stat] = {
            "T2": spearman(values, np.array([row["conversion"]["2"]["gap_pp"] for row in rows])),
            "T4": spearman(values, np.array([row["conversion"]["4"]["gap_pp"] for row in rows])),
        }
    passing = []
    for stat, values in correlations.items():
        if abs(values["T2"]) >= 0.60 and abs(values["T4"]) >= 0.60 and np.sign(values["T2"]) == np.sign(values["T4"]):
            passing.append(stat)
    output = {"rows": rows, "correlations": correlations, "passing_statistics": passing, "gate_pass": len(passing) >= 2 and len(rows) >= 5}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"correlations": correlations, "passing_statistics": passing, "gate_pass": output["gate_pass"]}, indent=2))


if __name__ == "__main__":
    main()
