from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import sys
from pathlib import Path

import numpy as np

from cert_core import (
    certificate_bounds_matrix,
    rowwise_quantize,
    uniform_quantize,
)


WORKSPACE = Path(os.environ.get("PHD_SNN_WORKSPACE", Path(__file__).resolve().parents[7]))
PRIOR_FULL_ROOT = (
    WORKSPACE
    / "auto-paper/20261117-210314/full-experiments/f-research-v1-run-20261117-220203-ten-idea-full"
)


def evaluate_snapshot(
    adjacency: np.ndarray,
    features: np.ndarray,
    weight0: np.ndarray,
    bias0: np.ndarray,
    weight1: np.ndarray,
    bias1: np.ndarray,
    levels: int,
    quantizer: str,
    dataset: str,
    seed: int,
) -> dict:
    adjacency64 = np.asarray(adjacency, dtype=np.float64)
    features64 = np.asarray(features, dtype=np.float64)
    weight0_64 = np.asarray(weight0, dtype=np.float64)
    bias0_64 = np.asarray(bias0, dtype=np.float64)
    weight1_64 = np.asarray(weight1, dtype=np.float64)
    bias1_64 = np.asarray(bias1, dtype=np.float64)
    if quantizer not in {"global", "per_channel", "rowwise"}:
        raise ValueError("quantizer must be global, per_channel or rowwise")

    message = features64 @ weight0_64
    if quantizer == "rowwise":
        quantized, step, radius_matrix, clipping_count = rowwise_quantize(message, levels=levels)
    else:
        quantized, step, radius_vector, clipping_count = uniform_quantize(
            message,
            levels=levels,
            per_channel=quantizer == "per_channel",
        )
        radius_matrix = np.repeat(np.asarray(radius_vector)[None, :], message.shape[0], axis=0)
    hidden = np.maximum(adjacency64 @ message + bias0_64, 0.0)
    hidden_quantized = np.maximum(adjacency64 @ quantized + bias0_64, 0.0)
    logits = adjacency64 @ hidden @ weight1_64 + bias1_64
    logits_quantized = adjacency64 @ hidden_quantized @ weight1_64 + bias1_64
    actual = np.abs(logits - logits_quantized)
    proposed, minkowski, global_column, scalar = certificate_bounds_matrix(
        adjacency64,
        weight1_64,
        radius_matrix,
    )
    tolerance = 1e-10 + 1e-12 * np.abs(proposed)
    actual_rms = float(np.sqrt(np.mean(actual**2)))
    proposed_median = float(np.median(proposed))
    global_median = float(np.median(global_column))
    minkowski_median = float(np.median(minkowski))
    scalar_median = float(np.median(scalar))

    def width_ratio(median: float) -> float:
        if actual_rms == 0:
            return 0.0 if median == 0 else float("inf")
        return median / actual_rms

    proposed_ratio = width_ratio(proposed_median)
    global_ratio = width_ratio(global_median)
    if global_ratio == 0:
        tightening = 0.0 if proposed_ratio == 0 else float("-inf")
    else:
        tightening = 1.0 - proposed_ratio / global_ratio
    row = {
        "dataset": dataset,
        "seed": int(seed),
        "levels": int(levels),
        "quantizer": quantizer,
        "containment": bool(np.all(actual <= proposed + tolerance)),
        "minkowski_valid": bool(np.all(proposed <= minkowski + tolerance)),
        "global_equality": bool(np.allclose(proposed, global_column, rtol=1e-12, atol=1e-10)),
        "actual_rms": actual_rms,
        "proposed_width_over_rms": proposed_ratio,
        "minkowski_width_over_rms": width_ratio(minkowski_median),
        "global_width_over_rms": global_ratio,
        "scalar_width_over_rms": width_ratio(scalar_median),
        "tightening": tightening,
        "max_abs_error": float(np.max(actual)),
        "max_bound_excess": float(np.max(actual - proposed)),
        "clipping_count": int(clipping_count),
        "zero_step_channels": int(np.count_nonzero(np.asarray(step) == 0)),
        "radius_sha256": __import__("hashlib").sha256(np.ascontiguousarray(radius_matrix).tobytes()).hexdigest(),
        "nonfinite": bool(
            not np.isfinite(actual).all()
            or not np.isfinite(proposed).all()
            or not np.isfinite(minkowski).all()
        ),
    }
    return row


def load_snapshot(dataset: str, seed: int):
    if str(PRIOR_FULL_ROOT) not in sys.path:
        sys.path.insert(0, str(PRIOR_FULL_ROOT))
    campaign = importlib.import_module("research.campaign")
    data, model = campaign.load_model(dataset, seed)
    return (
        np.asarray(data["adj"].toarray(), dtype=np.float64),
        np.asarray(data["X"], dtype=np.float64),
        np.asarray(model["Ms"][0], dtype=np.float64),
        np.asarray(model["bs_layers"][0], dtype=np.float64),
        np.asarray(model["Ms"][1], dtype=np.float64),
        np.asarray(model["b_out"], dtype=np.float64),
    )


def run_matrix(phase: str, output_dir: Path) -> list[dict]:
    datasets = ("cora", "chameleon", "squirrel")
    seeds = (0,) if phase == "baseline" else (0, 1, 2)
    rows = []
    for dataset in datasets:
        for seed in seeds:
            snapshot = load_snapshot(dataset, seed)
            for levels in (4, 8):
                for quantizer in ("global", "rowwise"):
                    row = evaluate_snapshot(*snapshot, levels, quantizer, dataset, seed)
                    row["phase"] = phase
                    rows.append(row)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"cert-{phase}.json"
    csv_path = output_dir / f"cert-{phase}.csv"
    json_path.write_text(json.dumps({"phase": phase, "rows": rows}, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("baseline", "methods"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = run_matrix(args.phase, args.output_dir)
    print(json.dumps({"phase": args.phase, "rows": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
