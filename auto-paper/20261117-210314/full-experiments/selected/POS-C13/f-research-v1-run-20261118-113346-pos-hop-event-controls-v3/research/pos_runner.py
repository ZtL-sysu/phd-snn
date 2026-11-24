from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import sys
from pathlib import Path

import numpy as np

from pos_core import (
    hop_features,
    hybrid_lloyd_escape_encode,
    ordered_codebook_shuffle_error,
    relative_frobenius_error,
    serialized_bit_ledger,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("PHD_SNN_WORKSPACE", Path(__file__).resolve().parents[7]))
PRIOR_FULL_ROOT = WORKSPACE / "auto-paper/20261117-210314/full-experiments/f-research-v1-run-20261117-220203-ten-idea-full"


def load_graph(dataset: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if str(PRIOR_FULL_ROOT) not in sys.path:
        sys.path.insert(0, str(PRIOR_FULL_ROOT))
    campaign = importlib.import_module("research.campaign")
    data = campaign.core.load(dataset, str(campaign.CORE_ROOT / "results/.data"))
    adjacency = np.asarray(data["adj"].toarray(), dtype=np.float64)
    features = np.asarray(data["X"], dtype=np.float64)
    labels = np.asarray(data["y"], dtype=np.int64)
    return adjacency, features, labels


def uniform_encode(values: np.ndarray, levels: int, fit_mask: np.ndarray | None = None) -> tuple[np.ndarray, dict]:
    matrix = np.asarray(values, dtype=np.float64)
    selected = np.ones(matrix.shape[0], dtype=bool) if fit_mask is None else np.asarray(fit_mask, dtype=bool)
    minimum = matrix[selected].min(axis=0)
    maximum = matrix[selected].max(axis=0)
    step = (maximum - minimum) / (levels - 1)
    safe = np.where(step > 0, step, 1.0)
    indices = np.floor((matrix - minimum) / safe + 0.5)
    indices = np.clip(indices, 0, levels - 1)
    reconstructed = np.where(step > 0, minimum + indices * step, matrix)
    return reconstructed, {"step": step, "minimum": minimum, "maximum": maximum}


def hybrid_escape_mask(
    values: np.ndarray,
    base_reconstructed: np.ndarray,
    escape_fraction: float,
    fit_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, float]:
    matrix = np.asarray(values, dtype=np.float64)
    errors = np.abs(matrix - base_reconstructed)
    selected = np.ones(matrix.shape[0], dtype=bool) if fit_mask is None else np.asarray(fit_mask, dtype=bool)
    if fit_mask is None:
        mask = np.zeros(matrix.shape, dtype=bool)
        count = int(round(escape_fraction * matrix.size))
        if count:
            threshold = float(np.partition(errors.ravel(), -count)[-count])
            mask = errors >= threshold
        return mask, threshold if count else 0.0
    train_errors = errors[selected]
    count = max(1, int(round(escape_fraction * train_errors.size)))
    threshold = float(np.partition(train_errors.ravel(), -count)[-count])
    return errors >= threshold, threshold


def encode_methods(values: np.ndarray, escape_fraction: float = 0.005, fit_mask: np.ndarray | None = None) -> dict:
    matrix = np.asarray(values, dtype=np.float64)
    raw = matrix.copy()
    uniform, uniform_meta = uniform_encode(matrix, 8, fit_mask)
    base = hybrid_lloyd_escape_encode(matrix, 8, 0.0, fit_mask=fit_mask)
    lloyd = base
    escape_mask, escape_threshold = hybrid_escape_mask(matrix, base.reconstructed, escape_fraction, fit_mask)
    hybrid = np.where(escape_mask, matrix, base.reconstructed)
    nodes, channels = matrix.shape
    return {
        "raw": {"reconstructed": raw, "error": 0.0, "ledger": serialized_bit_ledger(nodes, channels, 0.0) | {"format": "float32", "average_bits_per_value": 32.0, "storage_reduction": 1.0}},
        "uniform": {"reconstructed": uniform, "error": relative_frobenius_error(matrix, uniform), "ledger": {"format": "8-level uniform", "average_bits_per_value": 3.0 + 64.0 / nodes, "storage_reduction": 32.0 / (3.0 + 64.0 / nodes)}, "metadata": uniform_meta},
        "lloyd": {"reconstructed": lloyd.reconstructed, "error": relative_frobenius_error(matrix, lloyd.reconstructed), "ledger": {"format": "8-centroid Lloyd", "average_bits_per_value": 3.0 + 256.0 / nodes, "storage_reduction": 32.0 / (3.0 + 256.0 / nodes)}},
        "hybrid": {"reconstructed": hybrid, "error": relative_frobenius_error(matrix, hybrid), "ledger": {"format": "8-centroid Lloyd + escape", "average_bits_per_value": 4.0 + 32.0 * escape_mask.mean() + 256.0 / nodes, "storage_reduction": 32.0 / (4.0 + 32.0 * escape_mask.mean() + 256.0 / nodes)}, "escape_fraction": float(escape_mask.mean()), "escape_threshold": escape_threshold, "escape_mask": escape_mask, "representatives": base.representatives},
    }


def representation_rows(dataset: str) -> tuple[list[dict], dict]:
    adjacency, features, _ = load_graph(dataset)
    original = hop_features(adjacency, features, hops=3)
    methods = encode_methods(original)
    rows = []
    for name in ("raw", "uniform", "lloyd", "hybrid"):
        item = methods[name]
        rows.append({
            "dataset": dataset,
            "method": name,
            "relative_error": item["error"],
            "average_bits_per_value": item["ledger"]["average_bits_per_value"],
            "storage_reduction": item["ledger"]["storage_reduction"],
            "escape_fraction": item.get("escape_fraction", 0.0),
            "escape_threshold": item.get("escape_threshold", 0.0),
        })

    permutation_rows = []
    for seed in range(5):
        permutation = np.random.default_rng(1200 + seed).permutation(original.shape[0])
        permuted = hop_features(adjacency[np.ix_(permutation, permutation)], features[permutation], hops=3)
        permuted_base = hybrid_lloyd_escape_encode(permuted, 8, 0.0)
        permuted_escape, _ = hybrid_escape_mask(permuted, permuted_base.reconstructed, 0.005)
        permuted_hybrid = np.where(permuted_escape, permuted, permuted_base.reconstructed)
        restored = np.empty_like(permuted_hybrid)
        restored[permutation] = permuted_hybrid
        raw_restored = np.empty_like(permuted)
        raw_restored[permutation] = permuted
        permutation_rows.append({
            "dataset": dataset,
            "permutation_seed": 1200 + seed,
            "raw_max_error": float(np.max(np.abs(raw_restored - original))),
            "hybrid_max_error": float(np.max(np.abs(restored - methods["hybrid"]["reconstructed"]))),
        })

    shuffle_rows = []
    for seed in range(5):
        shuffle_permutation = np.random.default_rng(2200 + seed).permutation(4)
        if np.array_equal(shuffle_permutation, np.arange(4)):
            shuffle_permutation = np.roll(shuffle_permutation, 1)
        result = ordered_codebook_shuffle_error(original, _encoded_from_methods(methods["hybrid"]), feature_dim=features.shape[1], seed=2200 + seed, permutation=shuffle_permutation)
        result["permutation"] = shuffle_permutation.tolist()
        result["identity_permutation"] = False
        shuffle_rows.append({"dataset": dataset, "shuffle_seed": 2200 + seed, **result})
    controls = {"permutation": permutation_rows, "shuffle": shuffle_rows}
    return rows, controls


def _encoded_from_methods(item: dict):
    from pos_core import EncodedValues

    return EncodedValues(
        reconstructed=item["reconstructed"],
        representatives=item["representatives"],
        assignments=np.zeros(item["reconstructed"].shape, dtype=np.int16),
        escape_mask=item["escape_mask"],
        alphabet_size=9,
        escape_fraction=item["escape_fraction"],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("representation",), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    all_rows = []
    all_controls = {"permutation": [], "shuffle": []}
    for dataset in ("chameleon", "squirrel"):
        rows, controls = representation_rows(dataset)
        all_rows.extend(rows)
        all_controls["permutation"].extend(controls["permutation"])
        all_controls["shuffle"].extend(controls["shuffle"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "pos-representation.json").write_text(json.dumps({"rows": all_rows, "controls": all_controls}, indent=2) + "\n", encoding="utf-8")
    with (args.output_dir / "pos-representation.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)
    print(json.dumps({"rows": len(all_rows), "permutation_rows": len(all_controls["permutation"]), "shuffle_rows": len(all_controls["shuffle"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
