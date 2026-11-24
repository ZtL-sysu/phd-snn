"""CONF-C09-v1 smoke driver."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from smoke.adaptive_prefix import make_internal_partitions
from smoke.conformal_selective import fit_risk_threshold, selective_result, uncertainty_scores


ROOT = Path(__file__).resolve().parent
AUTO_PAPER = ROOT.parents[1]
ARCHIVE_ROOT = AUTO_PAPER / "20261110-152407" / "Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs" / "f-research-v1-run-20261110-172308-superpixel-graph-vision/takeover_20261112"
ARCHIVES = {"MNIST": ARCHIVE_ROOT / "dc_mn_val1.npz", "CIFAR10": ARCHIVE_ROOT / "dc_cf_val1.npz"}


def run_dataset(name: str, path: Path) -> dict:
    with np.load(path, allow_pickle=False) as archive:
        arrays = {key: archive[key].copy() for key in ("indices", "labels", "teacher_logits", "T1_logits", "T2_logits", "T4_logits")}
    partitions = make_internal_partitions(arrays["indices"], seed=20261117, dev=512, tune=512, validation=512)
    index_by_id = {int(value): position for position, value in enumerate(arrays["indices"])}
    positions = {key: np.array([index_by_id[int(value)] for value in values], dtype=np.int64) for key, values in partitions.items()}
    scores = uncertainty_scores(arrays["T1_logits"], arrays["T2_logits"])
    tune = positions["tune"]
    validation = positions["validation"]
    correct_tune = np.argmax(arrays["T2_logits"][tune], axis=1) == arrays["labels"][tune]
    fit = fit_risk_threshold(scores[tune], correct_tune, target_risk=0.05)
    result = selective_result(arrays["T2_logits"][validation], arrays["labels"][validation], scores[validation], fit["threshold"])
    accepted = result["accepted"]
    random_errors = []
    rng = np.random.default_rng(20261117)
    for _ in range(2000):
        choice = rng.random(len(validation)) < result["coverage"]
        random_errors.append(float(np.mean(np.argmax(arrays["T2_logits"][validation][choice], axis=1) != arrays["labels"][validation][choice])) if choice.any() else 1.0)
    random_win = float(np.mean(np.asarray(random_errors) >= result["selective_error"]))
    return {
        "dataset": name,
        "fit": fit,
        "validation": {"coverage": result["coverage"], "selective_error": result["selective_error"], "accepted": int(accepted.sum())},
        "random_error_percentiles": {"p5": float(np.quantile(random_errors, 0.05)), "p50": float(np.quantile(random_errors, 0.5)), "p95": float(np.quantile(random_errors, 0.95))},
        "random_win_fraction": random_win,
        "gate": {
            "coverage_pass": result["coverage"] >= 0.30,
            "risk_pass": result["selective_error"] <= 0.05,
            "random_win_pass": random_win >= 0.95,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = [run_dataset(name, path) for name, path in ARCHIVES.items()]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
