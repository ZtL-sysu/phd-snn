"""Run diversified conversion-mechanism screens on local real assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from smoke.mechanism_prototypes import (
    causal_residual_frames,
    low_rank_message,
    permutation_equivariant_mean,
    radial_event_encode,
    signed_split,
)


WORKSPACE = Path(__file__).resolve().parents[3]
CORE_ROOT = WORKSPACE / "auto-paper" / "20261028-171500" / "Spiking-GNN-Conversion" / "f-research-v1-run-20261028-174053-gnn-snn-conv"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


def davis_causal_screen() -> dict:
    archive = np.load(WORKSPACE / "legacy/novix/platform-runs/_nv18156/project/data/processed/davis2017_motion_clips.npz", allow_pickle=False)
    frames = archive["frames"].astype(np.float64)
    time_major = np.swapaxes(frames, 0, 1)
    residuals = causal_residual_frames(time_major)
    reconstructed = np.cumsum(residuals, axis=0)
    target = np.swapaxes(frames[:, 1:] - frames[:, :1], 0, 1)
    changed = frames.copy()
    changed[:, -1] += 1000.0
    changed_residuals = causal_residual_frames(np.swapaxes(changed, 0, 1))
    prefix_error = float(np.max(np.abs(changed_residuals[:-1] - residuals[:-1])))
    raw_nonzero = int(np.count_nonzero(frames[:, 1:]))
    residual_nonzero = int(np.count_nonzero(residuals))
    return {
        "asset": "DAVIS-2017 processed motion clips",
        "clips": int(frames.shape[0]),
        "frames_per_clip": int(frames.shape[1]),
        "prefix_reconstruction_max_error": float(np.max(np.abs(reconstructed - target))),
        "future_change_prefix_error": prefix_error,
        "nonzero_residual_fraction": residual_nonzero / max(raw_nonzero, 1),
        "reduction_vs_raw_nonzero": 1.0 - residual_nonzero / max(raw_nonzero, 1),
    }


def flywire_equivariance_screen() -> dict:
    frame = pd.read_feather(WORKSPACE / "fly-connectome-cvpr2027/data/malecns_annotations.feather")
    coords = []
    for value in frame["somaLocation"].head(4096):
        if isinstance(value, (list, tuple, np.ndarray)) and len(value) == 3:
            coords.append(np.asarray(value, dtype=np.float64))
    points = np.asarray(coords)
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]], dtype=np.float64)
    direct = radial_event_encode(points, levels=8)
    rotated = radial_event_encode(points @ rotation.T, levels=8)
    error = float(np.max(np.abs(rotated["reconstructed"] - direct["reconstructed"] @ rotation.T)))
    raw = points
    quant_error = float(np.linalg.norm(raw - direct["reconstructed"]) / max(np.linalg.norm(raw), 1.0))
    return {
        "asset": "MaleCNS soma coordinates",
        "coordinates": int(points.shape[0]),
        "dimension": int(points.shape[1]),
        "equivariance_max_abs_error": error,
        "quantization_relative_error": quant_error,
        "event_levels": direct["event_levels"],
    }


def graph_permutation_screen() -> dict:
    data = core.load("chameleon", str(CORE_ROOT / "results/.data"))
    rng = np.random.default_rng(20261117)
    permutation = rng.permutation(data["N"])
    direct = permutation_equivariant_mean(data["X"], data["adj"].toarray())
    permuted = permutation_equivariant_mean(data["X"][permutation], data["adj"].toarray()[np.ix_(permutation, permutation)])
    error = float(np.max(np.abs(permuted - direct[permutation])))
    return {
        "asset": "Chameleon graph",
        "nodes": int(data["N"]),
        "edges_nnz": int(data["adj"].nnz),
        "permutation_equivariance_max_abs_error": error,
    }


def signed_message_screen() -> dict:
    data = core.load("squirrel", str(CORE_ROOT / "results/.data"))
    checkpoint = np.load(
        WORKSPACE / "auto-paper" / "20261105-111502" / "Intra-Aggregation-Misalignment-Graph-Conversion" / "f-research-v1-run-20261105-111502-gnn2snn" / "results" / "models" / "squirrel__H1_mean__s0.npz"
    )
    messages = np.asarray(data["X"] @ checkpoint["Ms0"] + checkpoint["bs0"], dtype=np.float64)
    positive, negative = signed_split(messages)
    error = float(np.max(np.abs((positive - negative) - messages)))
    return {
        "asset": "Squirrel graph messages",
        "message_shape": list(messages.shape),
        "positive_events": int(np.count_nonzero(positive)),
        "negative_events": int(np.count_nonzero(negative)),
        "reconstruction_max_abs_error": error,
        "negative_message_fraction": float(np.mean(messages < 0)),
    }


def low_rank_screen() -> dict:
    data = core.load("chameleon", str(CORE_ROOT / "results/.data"))
    messages = np.asarray(data["adj"] @ data["X"], dtype=np.float64)
    result = low_rank_message(messages, rank=128)
    return {
        "asset": "Chameleon graph messages",
        "input_shape": list(messages.shape),
        "rank": result["rank"],
        "compressed_dimension": result["compressed_dimension"],
        "input_dimension": int(messages.shape[0] * messages.shape[1]),
        "relative_error": result["relative_error"],
    }


def edge_weight_screen() -> dict:
    edges = pd.read_csv(WORKSPACE / "fly-connectome-cvpr2027/data/flywire_edges_real.csv")
    weights = edges["syn_count"].to_numpy(dtype=np.float64)
    weights = weights[np.isfinite(weights)]
    levels = 64
    maximum = float(weights.max())
    quantized = np.round(weights / maximum * levels) / levels * maximum
    relative_error = float(np.linalg.norm(weights - quantized) / max(np.linalg.norm(weights), 1.0))
    return {
        "asset": "FlyWire biological edge-weight messages",
        "edges": int(len(weights)),
        "quantization_levels": levels,
        "bits_per_weight": 6,
        "float32_bits_per_weight": 32,
        "storage_reduction_factor": 32 / 6,
        "quantization_relative_error": relative_error,
        "weighted_synapse_mass": float(weights.sum()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = {
        "DYN-C01": davis_causal_screen(),
        "EQ-C02": flywire_equivariance_screen(),
        "PERM-C03": graph_permutation_screen(),
        "SIGN-C04": signed_message_screen(),
        "LR-C05": low_rank_screen(),
        "EDGE-C06": edge_weight_screen(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
