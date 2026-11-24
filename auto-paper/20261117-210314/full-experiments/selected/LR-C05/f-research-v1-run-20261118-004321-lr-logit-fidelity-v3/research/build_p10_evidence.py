from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


RUN_ROOT = Path(__file__).resolve().parents[1]
RESULTS = RUN_ROOT / "results"
SHAPES = {
    "cora": {"N": 2708, "F": 1433, "train": 140, "val": 500, "test": 1000},
    "chameleon": {"N": 2277, "F": 2325, "train": 1092, "val": 729, "test": 456},
    "squirrel": {"N": 5201, "F": 2089, "train": 2496, "val": 1664, "test": 1041},
}
MODES = [
    "downstream_jacobian",
    "top_abs",
    "random",
    "uniform",
    "a2q_node_budget",
    "one_spike",
    "none",
]
MATCHED_MODES = [mode for mode in MODES if mode != "none"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def metric(row: dict, path: tuple[str, ...]) -> float:
    value: object = row
    for key in path:
        value = value[key]
    return float(value)


def main() -> int:
    confirmation = json.loads((RUN_ROOT / "results" / "confirmation-test-v2.json").read_text(encoding="utf-8"))
    budget_summary = json.loads((RUN_ROOT / "inputs" / "v2-summary.json").read_text(encoding="utf-8"))
    timing = json.loads((RUN_ROOT / "inputs" / "v2-timing.json").read_text(encoding="utf-8"))
    rows = confirmation["rows"]

    control_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        for mode in MODES:
            group = [row for row in rows if row["dataset"] == dataset and row["residual_mode"] == mode]
            logit = np.array([row["logit_mse"] for row in group], dtype=float)
            hidden = np.array([row["hidden_mse"] for row in group], dtype=float)
            control_rows.append(
                {
                    "dataset": dataset,
                    "residual_mode": mode,
                    "n_seeds": len(group),
                    "mean_logit_mse": float(logit.mean()),
                    "sample_sd_logit_mse": float(logit.std(ddof=1)),
                    "mean_hidden_mse": float(hidden.mean()),
                    "sample_sd_hidden_mse": float(hidden.std(ddof=1)),
                    "mean_T2_accuracy": float(np.mean([row["T2"]["accuracy"] for row in group])),
                    "mean_T2_teacher_agreement": float(np.mean([row["T2"]["teacher_agreement"] for row in group])),
                    "mean_T4_accuracy": float(np.mean([row["T4"]["accuracy"] for row in group])),
                    "mean_T4_teacher_agreement": float(np.mean([row["T4"]["teacher_agreement"] for row in group])),
                    "basis_bits": group[0]["basis_bits"],
                    "residual_target_bits": group[0]["residual_target_bits"],
                    "residual_payload_bits": group[0]["residual_payload_bits"],
                    "residual_padded_bits": group[0]["residual_padded_bits"],
                    "total_padded_bits": group[0]["total_padded_bits"],
                    "coefficient_count": group[0]["coefficient_count"],
                }
            )
    write_csv(RESULTS / "p10-control-summary.csv", control_rows)

    per_seed_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        for seed in (0, 1, 2):
            selected = {
                row["residual_mode"]: row
                for row in rows
                if row["dataset"] == dataset and row["seed"] == seed
            }
            proposed = selected["downstream_jacobian"]
            for mode in MATCHED_MODES:
                control = selected[mode]
                per_seed_rows.append(
                    {
                        "dataset": dataset,
                        "seed": seed,
                        "proposed_logit_mse": proposed["logit_mse"],
                        "control_mode": mode,
                        "control_logit_mse": control["logit_mse"],
                        "proposed_reduction_percent": 100 * (1 - proposed["logit_mse"] / control["logit_mse"]),
                        "paired_difference_control_minus_proposed": control["logit_mse"] - proposed["logit_mse"],
                    }
                )
    write_csv(RESULTS / "p10-per-seed-control-comparison.csv", per_seed_rows)

    bit_rows: list[dict[str, object]] = []
    for dataset, shape in SHAPES.items():
        proposed = next(row for row in rows if row["dataset"] == dataset and row["residual_mode"] == "downstream_jacobian")
        residual_entries = shape["N"] * shape["F"]
        selected_count = max(1, int(round(0.02 * residual_entries)))
        basis_formula = (shape["N"] * 128 + 128 + 128 * shape["F"]) * 32
        bit_rows.append(
            {
                "dataset": dataset,
                "N": shape["N"],
                "F": shape["F"],
                "transported_tensor": "M0=A_hat X",
                "tensor_shape": f'{shape["N"]}x{shape["F"]}',
                "rank": 128,
                "residual_entries": residual_entries,
                "budget_fraction": 0.02,
                "rounding_rule": "round-half-even via Python round",
                "selected_coefficients": selected_count,
                "bits_per_selected_pair": 64,
                "basis_bits_formula": "(N*rank + rank + rank*F)*32",
                "basis_bits": proposed["basis_bits"],
                "basis_formula_check": basis_formula,
                "residual_target_bits": proposed["residual_target_bits"],
                "total_padded_bits": proposed["total_padded_bits"],
                "full_float_bits": residual_entries * 32,
            }
        )
    write_csv(RESULTS / "p10-bit-ledger.csv", bit_rows)

    metric_paths = {
        "T2_accuracy": ("T2", "accuracy"),
        "T2_teacher_agreement": ("T2", "teacher_agreement"),
        "T4_accuracy": ("T4", "accuracy"),
        "T4_teacher_agreement": ("T4", "teacher_agreement"),
    }
    task_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        for seed in (0, 1, 2):
            selected = {
                row["residual_mode"]: row
                for row in rows
                if row["dataset"] == dataset and row["seed"] == seed
            }
            proposed_row = selected["downstream_jacobian"]
            for metric_name, path in metric_paths.items():
                proposed_value = metric(proposed_row, path)
                candidates = [(mode, metric(selected[mode], path)) for mode in MATCHED_MODES if mode != "downstream_jacobian"]
                best_mode, best_value = max(candidates, key=lambda item: item[1])
                task_rows.append(
                    {
                        "dataset": dataset,
                        "seed": seed,
                        "metric": metric_name,
                        "proposed": proposed_value,
                        "best_control_mode": best_mode,
                        "best_control": best_value,
                        "observed_degradation_pp": max(0.0, best_value - proposed_value) * 100,
                        "aggregation_rule": "best matched-budget non-proposed control per dataset/seed/metric",
                    }
                )
    write_csv(RESULTS / "p10-task-loss-audit.csv", task_rows)

    task_aggregate_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        for metric_name, path in metric_paths.items():
            proposed_values = [
                metric(row, path)
                for row in rows
                if row["dataset"] == dataset and row["residual_mode"] == "downstream_jacobian"
            ]
            proposed_mean = float(np.mean(proposed_values))
            control_means = []
            for mode in MATCHED_MODES:
                if mode == "downstream_jacobian":
                    continue
                values = [
                    metric(row, path)
                    for row in rows
                    if row["dataset"] == dataset and row["residual_mode"] == mode
                ]
                control_means.append((mode, float(np.mean(values))))
            best_mode, best_mean = max(control_means, key=lambda item: item[1])
            task_aggregate_rows.append(
                {
                    "dataset": dataset,
                    "metric": metric_name,
                    "proposed_three_seed_mean": proposed_mean,
                    "best_control_mode": best_mode,
                    "best_control_three_seed_mean": best_mean,
                    "three_seed_mean_observed_degradation_pp": max(0.0, best_mean - proposed_mean) * 100,
                    "aggregation_rule": "three-seed means, then best matched-budget non-proposed control per dataset/metric",
                }
            )
    write_csv(RESULTS / "p10-task-loss-three-seed-audit.csv", task_aggregate_rows)

    f8_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        proposed = next(row for row in control_rows if row["dataset"] == dataset and row["residual_mode"] == "downstream_jacobian")
        for mode in ("a2q_node_budget", "one_spike"):
            control = next(row for row in control_rows if row["dataset"] == dataset and row["residual_mode"] == mode)
            f8_rows.append(
                {
                    "dataset": dataset,
                    "control_mode": mode,
                    "proposed_three_seed_mean_logit_mse": proposed["mean_logit_mse"],
                    "control_three_seed_mean_logit_mse": control["mean_logit_mse"],
                    "reduction_percent": 100 * (1 - proposed["mean_logit_mse"] / control["mean_logit_mse"]),
                    "derivation": "1 - mean(proposed across three seeds) / mean(control across three seeds)",
                    "source": "results/confirmation-test-v2.json via results/p10-control-summary.csv",
                }
            )
    write_csv(RESULTS / "p10-f8-derivation.csv", f8_rows)

    validation_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        for budget in (0.005, 0.01, 0.02):
            record = budget_summary["datasets"][dataset][str(budget)]
            validation_rows.append(
                {
                    "dataset": dataset,
                    "rank_grid": "16,32,64,128",
                    "budget": budget,
                    "logit_reduction_percent": 100 * record["logit_mse"]["relative_reduction"],
                    "hidden_reduction_percent": 100 * record["hidden_mse"]["relative_reduction"],
                    "T2_gain_pp": record["T2"]["gain_pp"],
                    "T4_gain_pp": record["T4"]["gain_pp"],
                    "evidence_scope": "validation-exposed grid before focal test confirmation",
                }
            )
    write_csv(RESULTS / "p10-validation-grid.csv", validation_rows)

    timing_rows: list[dict[str, object]] = []
    for dataset in SHAPES:
        for seed in (0, 1, 2):
            method = next(row for row in timing["rows"] if row["dataset"] == dataset and row["seed"] == seed and row["method"] == "downstream_jacobian")
            baseline = next(row for row in timing["rows"] if row["dataset"] == dataset and row["seed"] == seed and row["method"] == "svd_only")
            timing_rows.append(
                {
                    "dataset": dataset,
                    "seed": seed,
                    "method_p95_sec": method["p95_elapsed_sec"],
                    "svd_only_p95_sec": baseline["p95_elapsed_sec"],
                    "ratio_of_method_p95_to_svd_only_p95": method["p95_elapsed_sec"] / baseline["p95_elapsed_sec"],
                    "method_peak_memory_mb": method["peak_memory_mb"],
                    "rank": 128,
                    "budget": 0.01,
                    "warmups": 3,
                    "measured_repeats": 7,
                    "timed_scope": "basis construction, residual construction/selection, reconstruction, rate conversion, evaluation; precomputed frozen model and adjacency/features",
                }
            )
    write_csv(RESULTS / "p10-timing-summary.csv", timing_rows)

    task_max_by_dataset = {
        dataset: max(
            float(row["three_seed_mean_observed_degradation_pp"])
            for row in task_aggregate_rows
            if row["dataset"] == dataset
        )
        for dataset in SHAPES
    }
    spec = {
        "schema_version": 1,
        "transport_scope": {
            "tensor": "M0 = A_hat X",
            "shape": "N x F for each dataset",
            "rank": 128,
            "not_compressed": "A_hat H1 and the output layer",
            "rank_validity": "F>128 for all three datasets; rank 128 applies only to M0",
        },
        "selection": {
            "score": "s_i = r_i^2 * ||J_i||_2^2",
            "jacobian": "analytic derivative of frozen ANN logits with respect to a transported message entry using the ReLU hidden mask and normalized adjacency column norm",
            "granularity": "one global coefficient set per dataset and checkpoint seed over the full transductive graph message",
            "access": "uses full graph adjacency/features and frozen model outputs/hidden mask, not labels; test features are part of the transductive graph",
            "tie_rule": "implementation uses numpy argpartition with no additional semantic tie-break",
        },
        "budget_and_cost": {
            "budget_definition": "fraction of residual message entries selected",
            "rounding": "max(1, round(budget * N * F))",
            "selected_pair_cost_bits": 64,
            "basis_cost_bits": "(N*rank + rank + rank*F)*32",
            "total_cost_bits": "basis_bits + residual_padded_bits",
            "matching_scope": "identical total_padded_bits within each dataset/seed/rank/budget among matched residual controls; full-float and SVD-only are references outside this matched residual budget",
        },
        "rate_conversion": {
            "operation": "clip hidden at zero, per-hidden-dimension maximum theta, round count=rint(hidden/theta*T), decode count*theta/T",
            "horizons": [2, 4],
            "jacobian_model": "frozen ANN logits, not the rate-coded converted model",
        },
        "splits": SHAPES,
        "comparators": {
            "fidelity_headline": "post-hoc strongest evaluated matched-budget non-proposed residual control by three-seed mean logit MSE per dataset; top_abs is best on all three reported datasets",
            "task_observation": "best matched-budget non-proposed residual control per dataset/seed/metric; report maximum observed degradation, not a bound",
        },
        "validation_test_chronology": {
            "validation_grid": "ranks 16/32/64/128 and residual budgets 0.5/1/2% were evaluated on validation",
            "focal_fix": "guidance-v3 fixed rank128 and 2% after validation exposure and before the confirmation test run",
            "test_status": "held-out confirmation after validation exposure; not preregistered or independent replication",
        },
        "timing": {
            "condition": "rank128/1%, not the focal 2% fidelity setting",
            "p95_convention": "for each method/dataset/seed, numpy quantile 0.95 over seven measured elapsed times after three warmups; headline ratio is method p95 divided by SVD-only p95",
            "cuda": "synchronize before and after each timed call; reset peak allocation before each call",
            "scope": "basis construction, residual construction/selection, reconstruction, rate conversion, and evaluation with frozen model/adjacency/features precomputed",
        },
        "task_observed_degradation": {
            "max_three_seed_mean_by_dataset_pp": task_max_by_dataset,
            "max_three_seed_mean_pp": max(task_max_by_dataset.values()),
            "max_seed_level_pp": max(float(row["observed_degradation_pp"]) for row in task_rows),
            "metric_set": ["T2_accuracy", "T2_teacher_agreement", "T4_accuracy", "T4_teacher_agreement"],
        },
    }
    (RESULTS / "p10-implementation-spec.json").write_text(
        json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    manifest_paths = [
        RESULTS / "p10-control-summary.csv",
        RESULTS / "p10-per-seed-control-comparison.csv",
        RESULTS / "p10-bit-ledger.csv",
        RESULTS / "p10-task-loss-audit.csv",
        RESULTS / "p10-task-loss-three-seed-audit.csv",
        RESULTS / "p10-f8-derivation.csv",
        RESULTS / "p10-validation-grid.csv",
        RESULTS / "p10-timing-summary.csv",
        RESULTS / "p10-implementation-spec.json",
    ]
    manifest = {
        "schema_version": 1,
        "artifacts": [
            {"path": str(path.relative_to(RUN_ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in manifest_paths
        ],
    }
    (RESULTS / "p10-evidence-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "passed", "task_max_by_dataset": task_max_by_dataset, "artifacts": len(manifest_paths)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
