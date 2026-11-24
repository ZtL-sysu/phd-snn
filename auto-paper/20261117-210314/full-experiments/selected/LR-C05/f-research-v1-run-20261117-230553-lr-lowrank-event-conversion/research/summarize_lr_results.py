"""Aggregate LR-C05 results and evaluate frozen strong gates."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def paired_bootstrap(values: np.ndarray, seed: int = 20261117, draws: int = 10000) -> dict:
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    samples = values[rng.integers(0, len(values), size=(draws, len(values)))].mean(axis=1)
    return {
        "mean": float(values.mean()),
        "lower_95": float(np.quantile(samples, 0.025)),
        "upper_95": float(np.quantile(samples, 0.975)),
    }


def main() -> None:
    baseline = json.loads((ROOT / "results/baseline.json").read_text(encoding="utf-8"))["rows"]
    method = json.loads((ROOT / "results/method.json").read_text(encoding="utf-8"))["rows"]
    summary: dict = {"datasets": {}}
    for dataset in ("cora", "chameleon", "squirrel"):
        proposed = [r for r in method if r.get("dataset") == dataset and r.get("rank") == 128 and r.get("residual_fraction") == 0.01 and r.get("method") == "downstream_residual"]
        controls = [r for r in baseline if r.get("dataset") == dataset and r.get("rank") == 128 and r.get("residual_fraction") == 0.01 and r.get("method") in ("random_residual", "uniform_residual")]
        by_control = {name: sorted([r for r in controls if r["method"] == name], key=lambda r: r["seed"]) for name in ("random_residual", "uniform_residual")}
        proposed.sort(key=lambda r: r["seed"])
        result: dict = {"seeds": [r["seed"] for r in proposed], "rank": 128, "residual_fraction": 0.01}
        for step in ("T2", "T4"):
            proposed_values = np.array([r[step]["teacher_agreement"] for r in proposed])
            control_means = {name: float(np.mean([r[step]["teacher_agreement"] for r in rows])) for name, rows in by_control.items()}
            strongest_name = max(control_means, key=control_means.get)
            strongest = np.array([r[step]["teacher_agreement"] for r in by_control[strongest_name]])
            result[step] = {
                "proposed_teacher_agreement": float(proposed_values.mean()),
                "strongest_control": strongest_name,
                "strongest_control_teacher_agreement": float(strongest.mean()),
                "gain": paired_bootstrap((proposed_values - strongest) * 100),
            }
        best_error_name = min(("random_residual", "uniform_residual"), key=lambda name: np.mean([r["message_relative_error"] for r in by_control[name]]))
        best_error = np.array([r["message_relative_error"] for r in by_control[best_error_name]])
        proposed_error = np.array([r["message_relative_error"] for r in proposed])
        reference = next(r for r in method if r.get("dataset") == dataset and r.get("rank") == 128 and "message_relative_error" in r and "teacher" in r)
        n, f = reference["shape"]
        dimension_compression = n * f / (128 * (n + f))
        result["message_error"] = {
            "proposed": float(proposed_error.mean()),
            "strongest_control": best_error_name,
            "strongest_control_error": float(best_error.mean()),
            "relative_reduction": float(1 - proposed_error.mean() / best_error.mean()),
            "dimension_compression": float(dimension_compression),
        }
        summary["datasets"][dataset] = result
    runtime_ratios = []
    for dataset in ("cora", "chameleon", "squirrel"):
        for seed in (0, 1, 2):
            for rank in (16, 32, 64, 128):
                for fraction in (0.005, 0.01, 0.02):
                    base = next(r for r in baseline if r.get("dataset") == dataset and r.get("seed") == seed and r.get("rank") == rank and r.get("residual_fraction") == fraction and r.get("method") == "svd_only")
                    prop = next(r for r in method if r.get("dataset") == dataset and r.get("seed") == seed and r.get("rank") == rank and r.get("residual_fraction") == fraction and r.get("method") == "downstream_residual")
                    runtime_ratios.append(prop["elapsed_sec"] / max(base["elapsed_sec"], 1e-9))
    summary["runtime"] = {
        "mean_ratio": float(np.mean(runtime_ratios)),
        "median_ratio": float(np.median(runtime_ratios)),
        "p95_ratio": float(np.quantile(runtime_ratios, 0.95)),
        "max_ratio": float(np.max(runtime_ratios)),
        "fraction_over_1_2": float(np.mean(np.asarray(runtime_ratios) > 1.2)),
    }
    summary["strong_gates"] = {
        "LR_A": sum(
            result["message_error"]["dimension_compression"] >= 8 and result["message_error"]["relative_reduction"] >= 0.20
            for result in summary["datasets"].values()
        ) >= 2,
        "LR_B": sum(
            max(result["T2"]["gain"]["mean"], result["T4"]["gain"]["mean"]) >= 1.0
            for result in summary["datasets"].values()
        ) >= 2,
        "LR_C": sum(
            max(result["T2"]["gain"]["mean"], result["T4"]["gain"]["mean"]) >= 1.0
            for result in summary["datasets"].values()
        ) >= 2,
        "LR_D": summary["runtime"]["p95_ratio"] <= 1.2 or summary["runtime"]["fraction_over_1_2"] <= 0.05,
    }
    (ROOT / "results/summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
