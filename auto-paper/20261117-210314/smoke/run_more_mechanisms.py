"""Run CERT/EDGEPRUNE/POS/DLY candidate screens."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from smoke.mechanism_prototypes import causal_residual_frames
from smoke.more_mechanisms import (
    affine_error_envelope,
    hop_position_messages,
    prune_lowest_edges,
    quantize_uniform,
)


WORKSPACE = Path(__file__).resolve().parents[3]
CORE_ROOT = WORKSPACE / "auto-paper" / "20261028-171500" / "Spiking-GNN-Conversion" / "f-research-v1-run-20261028-174053-gnn-snn-conv"
MODEL_ROOT = WORKSPACE / "auto-paper" / "20261105-111502" / "Intra-Aggregation-Misalignment-Graph-Conversion" / "f-research-v1-run-20261105-111502-gnn2snn/results/models"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


def load_model(path: Path, data: dict) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        model = {"Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()], "bs_layers": [archive["bs0"].copy()], "b_out": archive["b_out"].copy()}
    model["Hs"] = [np.maximum(np.asarray(data["adj"] @ data["X"]) @ model["Ms"][0] + model["bs_layers"][0], 0.0)]
    return model


def cert_screen() -> dict:
    rows = []
    for dataset in ("chameleon", "squirrel"):
        data = core.load(dataset, str(CORE_ROOT / "results/.data"))
        model = load_model(MODEL_ROOT / f"{dataset}__H1_mean__s0.npz", data)
        messages = np.asarray(data["X"] @ model["Ms"][0] + model["bs_layers"][0], dtype=np.float64)
        quantized, step = quantize_uniform(messages, levels=8)
        delta = float(np.max(np.abs(messages - quantized)))
        target = messages @ model["Ms"][1] + model["b_out"]
        converted = quantized @ model["Ms"][1] + model["b_out"]
        bound = affine_error_envelope(np.eye(data["N"]), model["Ms"][1], delta)
        actual = np.abs(target - converted)
        rms = float(np.sqrt(np.mean(actual**2))) or 1.0
        rows.append({"dataset": dataset, "coverage": float(np.mean(actual <= bound + 1e-12)), "certificate_width_over_rms": float(np.median(bound) / rms), "quantization_step": step})
    return {"rows": rows, "gate_pass": all(row["coverage"] == 1.0 and row["certificate_width_over_rms"] <= 10.0 for row in rows)}


def edge_prune_screen() -> dict:
    rows = []
    for dataset in ("chameleon", "squirrel"):
        data = core.load(dataset, str(CORE_ROOT / "results/.data"))
        adjacency = data["adj"].toarray()
        pruned, removed = prune_lowest_edges(adjacency, keep_fraction=0.60)
        original = adjacency @ data["X"]
        reduced = pruned @ data["X"]
        relative_error = float(np.linalg.norm(original - reduced) / max(np.linalg.norm(original), 1.0))
        kept = float(np.count_nonzero(pruned) / max(np.count_nonzero(adjacency), 1))
        rows.append({"dataset": dataset, "kept_fraction": kept, "removed_edges": removed, "message_relative_error": relative_error})
    return {"rows": rows, "gate_pass": all(row["kept_fraction"] <= 0.60 + 1e-12 and row["message_relative_error"] <= 0.15 for row in rows)}


def position_screen() -> dict:
    data = core.load("chameleon", str(CORE_ROOT / "results/.data"))
    adjacency = data["adj"].toarray()[:512, :512]
    row_sums = adjacency.sum(axis=1, keepdims=True)
    adjacency = adjacency / np.maximum(row_sums, 1.0)
    features = np.asarray(data["X"][:512], dtype=np.float64)
    messages = hop_position_messages(adjacency, features, hops=3)
    quantized, step = quantize_uniform(messages, levels=8)
    error = float(np.linalg.norm(messages - quantized) / max(np.linalg.norm(messages), 1.0))
    rng = np.random.default_rng(20261117)
    permutation = rng.permutation(512)
    permuted = hop_position_messages(adjacency[np.ix_(permutation, permutation)], features[permutation], hops=3)
    permutation_error = float(np.max(np.abs(permuted - messages[permutation])))
    return {"nodes": 512, "relative_error": error, "permutation_error": permutation_error, "storage_reduction_factor": 32 / 6, "quantization_step": step, "gate_pass": error <= 0.20 and permutation_error <= 1e-10}


def delay_screen() -> dict:
    archive = np.load(WORKSPACE / "legacy/novix/platform-runs/_nv18156/project/data/processed/davis2017_motion_clips.npz", allow_pickle=False)
    frames = np.swapaxes(archive["frames"].astype(np.float64), 0, 1)
    residuals = causal_residual_frames(frames)
    reconstruction_error = float(np.max(np.abs(np.cumsum(residuals, axis=0) - (frames[1:] - frames[:1]))))
    changed = frames.copy()
    changed[-1] += 1000.0
    changed_residuals = causal_residual_frames(changed)
    prefix_error = float(np.max(np.abs(changed_residuals[:-1] - residuals[:-1])))
    reduction = float(1.0 - np.count_nonzero(residuals) / max(np.count_nonzero(frames[1:]), 1))
    return {"clips": int(frames.shape[1]), "reconstruction_error": reconstruction_error, "future_prefix_error": prefix_error, "event_reduction": reduction, "gate_pass": reconstruction_error <= 1e-12 and prefix_error <= 1e-12 and reduction >= 0.10}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = {"CERT-C11-v1": cert_screen(), "EDGEPRUNE-C12-v1": edge_prune_screen(), "POS-C13-v1": position_screen(), "DLY-C14-v1": delay_screen()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
