"""Predeclared C09-v1 smoke driver; reads validation archives only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from smoke.adaptive_prefix import (
    choose_thresholds,
    make_internal_partitions,
    selective_prefix,
    uncertainty_scores,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARCHIVES = {
    "MNIST": ROOT.parent
    / "20261110-152407"
    / "Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs"
    / "f-research-v1-run-20261110-172308-superpixel-graph-vision"
    / "takeover_20261112"
    / "dc_mn_val1.npz",
    "CIFAR10": ROOT.parent
    / "20261110-152407"
    / "Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs"
    / "f-research-v1-run-20261110-172308-superpixel-graph-vision"
    / "takeover_20261112"
    / "dc_cf_val1.npz",
}


def metrics(logits: np.ndarray, labels: np.ndarray, teacher_logits: np.ndarray) -> dict:
    pred = np.argmax(logits, axis=1)
    return {
        "accuracy": float(np.mean(pred == labels)),
        "accuracy_percent": float(100 * np.mean(pred == labels)),
        "teacher_agreement": float(np.mean(pred == np.argmax(teacher_logits, axis=1))),
        "teacher_agreement_percent": float(
            100 * np.mean(pred == np.argmax(teacher_logits, axis=1))
        ),
    }


def interval(a: np.ndarray, b: np.ndarray, labels: np.ndarray, draws: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    n = len(labels)
    values = np.empty(draws, dtype=np.float64)
    for index in range(draws):
        sampled = rng.integers(0, n, size=n)
        values[index] = 100 * (
            np.mean(np.argmax(a[sampled], axis=1) == labels[sampled])
            - np.mean(np.argmax(b[sampled], axis=1) == labels[sampled])
        )
    return {
        "mean_pp": float(np.mean(values)),
        "lower_95_pp": float(np.quantile(values, 0.025)),
        "upper_95_pp": float(np.quantile(values, 0.975)),
        "nonnegative_fraction": float(np.mean(values >= 0)),
    }


def load_case(path: Path, seed: int) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        arrays = {key: archive[key].copy() for key in ("indices", "labels", "teacher_logits", "T1_logits", "T2_logits", "T4_logits")}
    partitions = make_internal_partitions(
        arrays["indices"], seed=seed, dev=512, tune=512, validation=512
    )
    index_by_id = {int(value): position for position, value in enumerate(arrays["indices"])}
    positions = {name: np.array([index_by_id[int(value)] for value in ids], dtype=np.int64)
                 for name, ids in partitions.items()}
    return {"arrays": arrays, "partitions": partitions, "positions": positions}


def evaluate_dataset(name: str, path: Path, seed: int) -> dict:
    case = load_case(path, seed)
    arrays = case["arrays"]
    tune = case["positions"]["tune"]
    validation = case["positions"]["validation"]
    selected = choose_thresholds(
        arrays["T1_logits"][tune],
        arrays["T2_logits"][tune],
        arrays["T4_logits"][tune],
        arrays["teacher_logits"][tune],
        fractions=(0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0),
    )
    score_validation = uncertainty_scores(arrays["T1_logits"][validation], arrays["T2_logits"][validation])
    method_logits, upgraded = selective_prefix(
        arrays["T2_logits"][validation],
        arrays["T4_logits"][validation],
        score_validation,
        uncertainty_threshold=float(selected["threshold"]),
    )
    labels = arrays["labels"][validation]
    teacher = arrays["teacher_logits"][validation]
    fraction = float(selected["fraction"])
    random_scores = []
    rng = np.random.default_rng(20261117)
    for _ in range(2000):
        choice = rng.random(len(validation)) < fraction
        random_logits = np.array(arrays["T2_logits"][validation], copy=True)
        random_logits[choice] = arrays["T4_logits"][validation][choice]
        random_scores.append(metrics(random_logits, labels, teacher))
    margin = 1.0 / (1.0 + np.maximum(
        np.partition(-arrays["T2_logits"][validation], kth=1, axis=1)[:, 0]
        - np.partition(-arrays["T2_logits"][validation], kth=1, axis=1)[:, 1],
        0.0,
    ))
    margin_threshold = -np.inf if fraction == 1 else float(np.quantile(margin, 1 - fraction))
    margin_logits, margin_upgraded = selective_prefix(
        arrays["T2_logits"][validation],
        arrays["T4_logits"][validation],
        margin,
        uncertainty_threshold=margin_threshold,
    )
    output = {
        "dataset": name,
        "archive": str(path),
        "partitions": {key: value.tolist() for key, value in case["partitions"].items()},
        "tune_selection": selected,
        "validation_fraction": fraction,
        "validation_mean_T": 2 + 2 * fraction,
        "methods": {
            "T2": metrics(arrays["T2_logits"][validation], labels, teacher),
            "T4": metrics(arrays["T4_logits"][validation], labels, teacher),
            "C09": metrics(method_logits, labels, teacher),
            "margin_only": metrics(margin_logits, labels, teacher),
        },
        "upgraded_C09": int(upgraded.sum()),
        "upgraded_margin": int(margin_upgraded.sum()),
        "random": {
            "accuracy_percentiles": {
                "p5": float(100 * np.quantile([x["accuracy"] for x in random_scores], 0.05)),
                "p50": float(100 * np.quantile([x["accuracy"] for x in random_scores], 0.5)),
                "p95": float(100 * np.quantile([x["accuracy"] for x in random_scores], 0.95)),
            },
            "agreement_percentiles": {
                "p5": float(100 * np.quantile([x["teacher_agreement"] for x in random_scores], 0.05)),
                "p50": float(100 * np.quantile([x["teacher_agreement"] for x in random_scores], 0.5)),
                "p95": float(100 * np.quantile([x["teacher_agreement"] for x in random_scores], 0.95)),
            },
        },
        "paired_C09_minus_T2_accuracy": interval(
            method_logits, arrays["T2_logits"][validation], labels, 5000, seed + 17
        ),
    }
    methods = output["methods"]
    output["gate"] = {
        "minimum_accuracy_gain_pp": 100 * (methods["C09"]["accuracy"] - methods["T2"]["accuracy"]),
        "minimum_accuracy_gain_pass": methods["C09"]["accuracy"] - methods["T2"]["accuracy"] >= 0.002,
        "random_95_accuracy_pass": methods["C09"]["accuracy"] >= output["random"]["accuracy_percentiles"]["p95"] / 100,
        "strong_beat_random": methods["C09"]["accuracy"] >= output["random"]["accuracy_percentiles"]["p95"] / 100,
        "strong_beat_margin": methods["C09"]["accuracy"] > methods["margin_only"]["accuracy"],
        "strong_T4_agreement_gap_pp": 100 * (methods["T4"]["teacher_agreement"] - methods["C09"]["teacher_agreement"]),
        "strong_mean_T_pass": output["validation_mean_T"] <= 3.0,
        "strong_bootstrap_pass": output["paired_C09_minus_T2_accuracy"]["lower_95_pp"] >= -0.5,
    }
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = [evaluate_dataset(name, path, 20261117) for name, path in ARCHIVES.items()]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
