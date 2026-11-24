from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import sys
from pathlib import Path

import numpy as np

from pos_core import hop_features, shuffle_hop_blocks
from pos_runner import encode_methods, load_graph


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("PHD_SNN_WORKSPACE", Path(__file__).resolve().parents[7]))
PRIOR_FULL_ROOT = WORKSPACE / "auto-paper/20261117-210314/full-experiments/f-research-v1-run-20261117-220203-ten-idea-full"


def _campaign():
    if str(PRIOR_FULL_ROOT) not in sys.path:
        sys.path.insert(0, str(PRIOR_FULL_ROOT))
    return importlib.import_module("research.campaign")


def fit_probe(features: np.ndarray, labels: np.ndarray, validation: tuple[np.ndarray, np.ndarray], seed: int):
    campaign = _campaign()
    probe = campaign.TorchLinearProbe(seed=seed, epochs=120, device=str(campaign.DEVICE))
    fit = probe.fit(features, labels, validation)
    return probe, fit


def probe_metrics(probe, features: np.ndarray, labels: np.ndarray, splits: dict) -> dict:
    campaign = _campaign()
    prediction = probe.predict(features)
    metrics = campaign.classification_metrics(labels[splits["test"]], prediction[splits["test"]])
    return {
        "accuracy": float(metrics["accuracy"]),
        "balanced_accuracy": float(metrics["balanced_accuracy"]),
    }


def evaluate_dataset(dataset: str) -> tuple[list[dict], dict]:
    campaign = _campaign()
    adjacency, features, labels = load_graph(dataset)
    representations = hop_features(adjacency, features, hops=3)
    valid = labels >= 0
    task_representations = representations[valid]
    task_labels = labels[valid]
    splits_by_seed = {seed: campaign.stratified_splits(task_labels, seed) for seed in range(600, 605)}
    rows = []
    fixed_rows = []
    for split_seed, splits in splits_by_seed.items():
        train_mask = np.zeros(task_labels.shape[0], dtype=bool)
        train_mask[splits["train"]] = True
        methods = encode_methods(task_representations, escape_fraction=0.005, fit_mask=train_mask)
        raw_probe, raw_fit = fit_probe(
            methods["raw"]["reconstructed"][splits["train"]],
            task_labels[splits["train"]],
            (methods["raw"]["reconstructed"][splits["validation"]], task_labels[splits["validation"]]),
            split_seed,
        )
        for method_name in ("raw", "uniform", "lloyd", "hybrid"):
            item = methods[method_name]
            probe, fit = fit_probe(
                item["reconstructed"][splits["train"]],
                task_labels[splits["train"]],
                (item["reconstructed"][splits["validation"]], task_labels[splits["validation"]]),
                split_seed,
            )
            metrics = probe_metrics(probe, item["reconstructed"], task_labels, splits)
            rows.append({
                "dataset": dataset,
                "split_seed": split_seed,
                "method": method_name,
                "relative_error": item["error"],
                "average_bits_per_value": item["ledger"]["average_bits_per_value"],
                "storage_reduction": item["ledger"]["storage_reduction"],
                "escape_fraction": item.get("escape_fraction", 0.0),
                "escape_threshold": item.get("escape_threshold", 0.0),
                "retrained_accuracy": metrics["accuracy"],
                "retrained_balanced_accuracy": metrics["balanced_accuracy"],
                "best_validation_accuracy": float(fit["best_validation_accuracy"]),
            })
            fixed_metrics = probe_metrics(raw_probe, item["reconstructed"], task_labels, splits)
            fixed_rows.append({
                "dataset": dataset,
                "split_seed": split_seed,
                "method": method_name,
                "fixed_accuracy": fixed_metrics["accuracy"],
                "fixed_balanced_accuracy": fixed_metrics["balanced_accuracy"],
            })

        hybrid = methods["hybrid"]["reconstructed"]
        for shuffle_seed in range(2200, 2205):
            permutation = np.random.default_rng(shuffle_seed).permutation(4)
            if np.array_equal(permutation, np.arange(4)):
                permutation = np.roll(permutation, 1)
            shuffled, _ = shuffle_hop_blocks(hybrid, feature_dim=features.shape[1], seed=shuffle_seed)
            metrics = probe_metrics(raw_probe, shuffled, task_labels, splits)
            fixed_rows.append({
                "dataset": dataset,
                "split_seed": split_seed,
                "method": "hybrid_shuffled",
                "shuffle_seed": shuffle_seed,
                "shuffle_permutation": permutation.tolist(),
                "fixed_accuracy": metrics["accuracy"],
                "fixed_balanced_accuracy": metrics["balanced_accuracy"],
            })
        del methods
    return rows, {"fixed_rows": fixed_rows}


def summarize(rows: list[dict], controls: dict) -> dict:
    summary = {"schema_version": 1, "datasets": {}}
    for dataset in ("chameleon", "squirrel"):
        dataset_rows = [row for row in rows if row["dataset"] == dataset]
        raw = [row for row in dataset_rows if row["method"] == "raw"]
        hybrid = [row for row in dataset_rows if row["method"] == "hybrid"]
        fixed_hybrid = [row for row in controls["fixed_rows"] if row["dataset"] == dataset and row["method"] == "hybrid"]
        fixed_shuffled = [row for row in controls["fixed_rows"] if row["dataset"] == dataset and row["method"] == "hybrid_shuffled"]
        raw_ba = np.array([row["retrained_balanced_accuracy"] for row in raw])
        hybrid_ba = np.array([row["retrained_balanced_accuracy"] for row in hybrid])
        ordered_fixed = np.array([row["fixed_balanced_accuracy"] for row in fixed_hybrid])
        shuffled_fixed = np.array([row["fixed_balanced_accuracy"] for row in fixed_shuffled])
        summary["datasets"][dataset] = {
            "retrained_raw_balanced_accuracy_mean": float(raw_ba.mean()),
            "retrained_hybrid_balanced_accuracy_mean": float(hybrid_ba.mean()),
            "retrained_hybrid_loss_pp": float((raw_ba.mean() - hybrid_ba.mean()) * 100),
            "fixed_ordered_balanced_accuracy_mean": float(ordered_fixed.mean()),
            "fixed_shuffled_balanced_accuracy_mean": float(shuffled_fixed.mean()),
            "fixed_ordered_minus_shuffled_pp": float((ordered_fixed.mean() - shuffled_fixed.mean()) * 100),
            "hybrid_error_max": float(max(row["relative_error"] for row in hybrid)),
            "hybrid_storage_min": float(min(row["storage_reduction"] for row in hybrid)),
        }
    summary["strong_gate_pass"] = all(
        item["hybrid_error_max"] <= 0.05
        and item["hybrid_storage_min"] >= 4
        and item["retrained_hybrid_loss_pp"] <= 2.0
        for item in summary["datasets"].values()
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    controls = {"fixed_rows": []}
    for dataset in ("chameleon", "squirrel"):
        dataset_rows, dataset_controls = evaluate_dataset(dataset)
        rows.extend(dataset_rows)
        controls["fixed_rows"].extend(dataset_controls["fixed_rows"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "pos-task-rows.json").write_text(json.dumps({"rows": rows, "controls": controls}, indent=2) + "\n", encoding="utf-8")
    with (args.output_dir / "pos-task-rows.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = summarize(rows, controls)
    (args.output_dir / "pos-task-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"task_rows": len(rows), "fixed_rows": len(controls["fixed_rows"]), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
