#!/usr/bin/env python3
"""Independent structural and numerical validator for P4 C1 outputs."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
EXPECTED_CONDITIONS = [
    "stateless", "lif_homeostasis", "lif_combo", "degree_null_lif", "A0",
    "lif_combo_no_adaptive", "lif_combo_no_refractory", "lif_combo_no_ei",
]
EXPECTED_SEEDS = [1, 2, 3, 4, 5]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def exact_p(deltas: np.ndarray) -> float:
    signs = np.asarray(list(itertools.product([-1.0, 1.0], repeat=len(deltas))))
    obs = abs(float(np.mean(deltas)))
    null = np.abs(np.mean(signs * deltas, axis=1))
    return float(np.mean(null >= obs - 1e-15))


class Validator:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def check(self, name: str, condition: bool, detail: Any = None) -> None:
        self.checks.append({"name": name, "passed": bool(condition), "detail": detail})

    @property
    def passed(self) -> bool:
        return all(item["passed"] for item in self.checks)


def _payload(project_dir: Path, result_path: Path, v: Validator) -> dict[str, Any]:
    digest = sha256(result_path) if result_path.exists() else None
    return {
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "validator": str(Path(__file__).resolve()),
        "project_dir": str(project_dir.resolve()),
        "result_json_bytes": result_path.stat().st_size if result_path.exists() else 0,
        "result_json_sha256": digest,
        "result_json_sha256_prefix16": digest[:16] if digest else None,
        "passed": v.passed,
        "checks": v.checks,
        "summary": {
            "total": len(v.checks),
            "passed": sum(item["passed"] for item in v.checks),
            "failed": sum(not item["passed"] for item in v.checks),
        },
    }


def _validate_design_invalid(project_dir: Path, result_path: Path, result: dict[str, Any],
                             config: dict[str, Any], v: Validator) -> dict[str, Any]:
    """Validate a scientifically legitimate fail-fast terminal state.

    This branch checks that the triggering measurement is present and that no
    downstream method rows were invented.  It does *not* reinterpret an invalid
    design as a successful method result.
    """
    v.check("status_design_invalid", result.get("status") == "design_invalid", result.get("status"))
    v.check("design_valid_false", result.get("design_valid") is False, result.get("design_valid"))
    reason = result.get("design_invalid_reason", "")
    v.check("design_invalid_reason_present", isinstance(reason, str) and bool(reason.strip()), reason)
    v.check("fail_fast_final_phase", result.get("phase") == "design_invalid_final", result.get("phase"))
    v.check("result_path_exact", Path(result.get("result_path", "")).resolve() == result_path.resolve(),
            result.get("result_path"))

    invariants = result.get("invariant_checks", {})
    invariant_names = ("kc_reachable_count", "kc_feature_std", "synthetic_ceiling", "real_domain_ceiling")
    failed = [name for name in invariant_names if invariants.get(name, {}).get("passed") is False]
    v.check("at_least_one_invariant_failed", len(failed) >= 1, failed)
    reason_prefix = reason.split(":", 1)[0] if ":" in reason else ""
    v.check("reason_names_failed_invariant", reason_prefix in failed, {"prefix": reason_prefix, "failed": failed})
    failed_stage = reason_prefix

    edge = {item.get("key"): item for item in result.get("data_files_used", [])}.get("connectome_edges", {})
    if edge:
        v.check("edge_full_not_prefix", edge.get("bytes") == 178_853_187 and edge.get("prefix") is False, edge)
    reach = invariants.get("kc_reachable_count", {})
    if reach.get("passed") is True:
        hops = reach.get("exact_length_kc_counts_hop_1_to_8", {})
        v.check("all_hops_1_to_8_reported", set(hops) == set(map(str, range(1, 9))), hops)
        actual_k = reach.get("actual_k")
        v.check("actual_k_at_least_5", isinstance(actual_k, int) and 5 <= actual_k <= 8, actual_k)
        v.check("config_actual_k_matches_result", config.get("graph_protocol", {}).get("actual_k") == actual_k,
                {"config": config.get("graph_protocol", {}).get("actual_k"), "result": actual_k})

    for key, ceiling in result.get("ceilings", {}).items():
        values = ceiling.get("accuracies", [])
        v.check(f"ceiling_five_seeds:{key}", len(values) == 5, values)
        if len(values) == 5:
            v.check(f"ceiling_mean_recomputes:{key}",
                    math.isclose(float(np.mean(values)), float(ceiling.get("mean_accuracy", math.nan)),
                                 rel_tol=0, abs_tol=1e-12),
                    {"values": values, "mean": ceiling.get("mean_accuracy")})
        for seed_record in ceiling.get("per_seed", []):
            raw_path = Path(seed_record.get("raw_npz", ""))
            exists = raw_path.exists() and raw_path.stat().st_size > 0
            v.check(f"ceiling_raw_exists:{key}:seed{seed_record.get('seed')}", exists, str(raw_path))
            if exists:
                with np.load(raw_path, allow_pickle=False) as raw:
                    raw_accuracy = float(raw["accuracy"])
                v.check(f"ceiling_raw_accuracy_match:{key}:seed{seed_record.get('seed')}",
                        math.isclose(raw_accuracy, float(seed_record["accuracy"]), rel_tol=0, abs_tol=1e-12),
                        {"raw": raw_accuracy, "json": seed_record["accuracy"]})

    if failed_stage == "kc_feature_std":
        dataset_checks = invariants.get("kc_feature_std", {}).get("datasets", {})
        synthetic_checks = dataset_checks.get("SYNTHETIC_direction", {}).get("conditions", {})
        v.check("all_eight_conditions_feature_checked", set(synthetic_checks) == set(EXPECTED_CONDITIONS),
                list(synthetic_checks))
        feature_dir = project_dir / "evidence" / "features"
        for condition in EXPECTED_CONDITIONS:
            feature_path = feature_dir / f"SYNTHETIC_direction__{condition}.npz"
            exists = feature_path.exists() and feature_path.stat().st_size > 0
            v.check(f"feature_cache_exists:{condition}", exists, str(feature_path))
            if not exists:
                continue
            with np.load(feature_path, allow_pickle=False) as cached:
                features = cached["features"].astype(np.float64)
                diagnostics = json.loads(str(cached["diagnostics_json"].item()))
            recomputed_std = float(np.std(features, axis=0, ddof=0).mean())
            json_std = float(synthetic_checks.get(condition, {}).get("feature_std", math.nan))
            v.check(f"feature_std_cache_matches_result:{condition}",
                    math.isclose(recomputed_std, json_std, rel_tol=0, abs_tol=1e-15) and
                    math.isclose(float(diagnostics["feature_std"]), json_std, rel_tol=0, abs_tol=1e-15),
                    {"recomputed": recomputed_std, "cache_diagnostics": diagnostics.get("feature_std"),
                     "result": json_std})
        raw_paths = list((project_dir / "evidence" / "raw").glob("*.npz"))
        v.check("no_method_readout_raw_after_feature_failure",
                all("flattened_8frame_ceiling" in path.name for path in raw_paths),
                [path.name for path in raw_paths])
        v.check("degree_null_constraints_verified_before_feature_check",
                result.get("degree_null_graph", {}).get("verification", {}).get("all_passed") is True,
                result.get("degree_null_graph", {}).get("verification"))

    experiments = result.get("experiments", {})
    if failed_stage in {"kc_reachable_count", "synthetic_ceiling", "real_domain_ceiling"}:
        v.check("no_method_results_after_pretraining_failure", len(experiments) == 0, list(experiments))
    else:
        v.check("no_unregistered_experiment_groups",
                set(experiments).issubset({"SYNTHETIC_direction", "SYNTHETIC_flash", "REAL_DAVIS_2017", "REAL_SINTEL"}),
                list(experiments))

    main_meta = result.get("main_table", {})
    main_path = project_dir / "evidence" / "main_table.csv"
    v.check("partial_main_table_recorded", main_meta.get("scope") in {
        "partial_ceiling_evidence", "partial_method_results"
    }, main_meta)
    if main_path.exists():
        table = pd.read_csv(main_path)
        if not experiments:
            v.check("partial_table_has_only_ceiling_rows",
                    len(table) == len(result.get("ceilings", {})) and
                    (table["record_type"].eq("ceiling").all() if "record_type" in table else False),
                    {"rows": len(table), "columns": table.columns.tolist()})
    v.check("no_fabricated_unrun_rows", main_meta.get("fabricated_unrun_method_rows") is False, main_meta)
    v.check("traceability_recorded", bool(result.get("traceability", {}).get("sha256")), result.get("traceability"))
    fail_fast = result.get("fail_fast_action", {})
    v.check("downstream_training_stopped", fail_fast.get("downstream_readout_training_stopped") is True and
            fail_fast.get("experiment_groups_completed_before_stop") == [], fail_fast)
    history = result.get("development_preflight_history", {})
    v.check("posthoc_real_protocol_revision_disclosed",
            history.get("post_hoc_revision") is True and history.get("davis_full_frame_v1_ceiling_mean") == 0.685,
            history)
    v.check("five_seed_power_limit_disclosed", "0.0625" in result.get("statistical_power_note", ""),
            result.get("statistical_power_note"))
    v.check("invalid_not_claimed_as_verdict_accept", result.get("verdict", {}).get("decision") != "ACCEPT",
            result.get("verdict"))
    return _payload(project_dir, result_path, v)


def validate(project_dir: Path) -> dict[str, Any]:
    v = Validator()
    result_path = project_dir / "result.json"
    config_path = project_dir / "config.json"
    required = [
        project_dir / "experiment.py", project_dir / "entrypoint.sh", config_path,
        project_dir / "validate_results.py", project_dir / "test_pipeline.py",
        result_path, project_dir / "evidence" / "main_table.csv",
        project_dir / "experiment-traceability.csv", project_dir / "command_history.log",
    ]
    for path in required:
        v.check(f"required_file:{path.name}", path.exists() and path.stat().st_size > 0,
                {"path": str(path), "bytes": path.stat().st_size if path.exists() else 0})
    if not result_path.exists() or not config_path.exists():
        return {
            "validated_at_utc": datetime.now(timezone.utc).isoformat(),
            "passed": False,
            "checks": v.checks,
            "summary": {"passed": sum(c["passed"] for c in v.checks), "failed": sum(not c["passed"] for c in v.checks)},
        }
    result = json.loads(result_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if result.get("status") == "design_invalid":
        return _validate_design_invalid(project_dir, result_path, result, config, v)
    v.check("status_completed", result.get("status") == "completed", result.get("status"))
    v.check("design_valid_true", result.get("design_valid") is True, result.get("design_valid"))
    v.check("result_path_exact", Path(result.get("result_path", "")).resolve() == result_path.resolve(), result.get("result_path"))
    v.check("grind_block_four_elements", set(result.get("grind_block", {})) == {
        "previous_failure_points", "current_hypothesis", "concrete_changes", "expected_signal_and_failure_next_step"
    }, list(result.get("grind_block", {})))
    v.check("config_diff_nonempty", len(result.get("config_diff_vs_18156", [])) >= 5,
            result.get("config_diff_vs_18156"))

    hardware = result.get("hardware", {}).get("torch", {})
    v.check("cuda_available_recorded", hardware.get("cuda_available") is True, hardware)
    v.check("gpu_model_recorded", bool(hardware.get("devices", [{}])[0].get("name") if hardware.get("devices") else False),
            hardware.get("devices"))

    data_files = {item["key"]: item for item in result.get("data_files_used", [])}
    edge = data_files.get("connectome_edges", {})
    v.check("edge_full_not_prefix", edge.get("bytes") == 178_853_187 and edge.get("prefix") is False, edge)
    for key in ("connectome_edges", "neuron_annotations", "eye_positions", "davis_2017"):
        item = data_files.get(key, {})
        v.check(f"data_file_record:{key}", bool(item.get("bytes", 0) > 0 and re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", ""))), item)

    graph = result.get("graph", {})
    base = graph.get("base_graph", {})
    v.check("graph_matrix_protocol", base.get("matrix_definition") == "A[post_index, pre_index] = sum(log1p(syn_count))", base.get("matrix_definition"))
    v.check("no_row_normalization", base.get("row_normalization") is False, base.get("row_normalization"))
    v.check("power_iterations_ge_40", base.get("power_iterations", 0) >= 40, base.get("power_iterations"))
    scaled_rho = base.get("spectral_radius_estimate_before_scaling", 0) * base.get("spectral_scale", 0)
    v.check("spectral_target_0_95", abs(scaled_rho - 0.95) < 1e-5, scaled_rho)
    mapping = graph.get("voronoi_mapping", {})
    v.check("uses_x_axis_y_axis", mapping.get("coordinate_columns") == ["x_axis", "y_axis"] and mapping.get("forbidden_3d_columns_used") is False, mapping)

    invariants = result.get("invariant_checks", {})
    for name in ("kc_reachable_count", "kc_feature_std", "synthetic_ceiling", "real_domain_ceiling"):
        v.check(f"invariant_passed:{name}", invariants.get(name, {}).get("passed") is True, invariants.get(name))
    hop_counts = invariants.get("kc_reachable_count", {}).get("exact_length_kc_counts_hop_1_to_8", {})
    v.check("all_hops_1_to_8_reported", set(hop_counts) == set(map(str, range(1, 9))), hop_counts)
    actual_k = invariants.get("kc_reachable_count", {}).get("actual_k")
    selected_count = invariants.get("kc_reachable_count", {}).get("selected_k_kc_reachable_count")
    v.check("actual_k_at_least_5", isinstance(actual_k, int) and 5 <= actual_k <= 8, actual_k)
    v.check("selected_k_nonzero_or_fallback", selected_count > 0 or invariants.get("kc_reachable_count", {}).get("readout_fallback"), selected_count)
    v.check("config_actual_k_matches_result", config.get("graph_protocol", {}).get("actual_k") == actual_k,
            {"config": config.get("graph_protocol", {}).get("actual_k"), "result": actual_k})

    ceilings = result.get("ceilings", {})
    synthetic_ceiling = ceilings.get("synthetic", {})
    v.check("synthetic_ceiling_five_seeds", len(synthetic_ceiling.get("accuracies", [])) == 5, synthetic_ceiling.get("accuracies"))
    v.check("synthetic_ceiling_ge_0_90", synthetic_ceiling.get("mean_accuracy", 0) >= 0.90, synthetic_ceiling.get("mean_accuracy"))
    real_key = invariants.get("real_domain_ceiling", {}).get("available_real_domain")
    real_ceiling_key = "davis_2017" if real_key == "REAL_DAVIS_2017" else "sintel"
    real_ceiling = ceilings.get(real_ceiling_key, {})
    v.check("real_ceiling_five_seeds", len(real_ceiling.get("accuracies", [])) == 5, real_ceiling.get("accuracies"))
    v.check("real_ceiling_ge_0_70", real_ceiling.get("mean_accuracy", 0) >= 0.70, real_ceiling.get("mean_accuracy"))

    experiments = result.get("experiments", {})
    v.check("three_experiment_groups", len(experiments) == 3, list(experiments))
    numerical_mismatches: list[dict[str, Any]] = []
    expected_raw = 0
    for group, conditions in experiments.items():
        v.check(f"conditions_complete:{group}", list(conditions) == EXPECTED_CONDITIONS,
                {"actual": list(conditions), "expected": EXPECTED_CONDITIONS})
        baseline = np.asarray(conditions.get("stateless", {}).get("accuracies", []), dtype=float)
        for condition in EXPECTED_CONDITIONS:
            item = conditions.get(condition, {})
            accuracies = np.asarray(item.get("accuracies", []), dtype=float)
            v.check(f"five_seeds:{group}:{condition}", item.get("seeds") == EXPECTED_SEEDS and len(accuracies) == 5,
                    {"seeds": item.get("seeds"), "accuracies": accuracies.tolist()})
            if len(accuracies) == 5:
                if not math.isclose(float(accuracies.mean()), float(item.get("mean_accuracy", math.nan)), rel_tol=0, abs_tol=1e-12):
                    numerical_mismatches.append({"group": group, "condition": condition, "field": "mean_accuracy"})
                if len(baseline) == 5:
                    deltas = accuracies - baseline
                    if not math.isclose(float(deltas.mean()), float(item.get("delta_vs_stateless_mean", math.nan)), rel_tol=0, abs_tol=1e-12):
                        numerical_mismatches.append({"group": group, "condition": condition, "field": "delta"})
                    if condition != "stateless":
                        recomputed_p = exact_p(deltas)
                        if not math.isclose(recomputed_p, float(item.get("exact_p_two_sided", math.nan)), rel_tol=0, abs_tol=1e-12):
                            numerical_mismatches.append({"group": group, "condition": condition, "field": "exact_p", "expected": recomputed_p, "actual": item.get("exact_p_two_sided")})
                diagnostics = item.get("encoder_diagnostics", {})
                v.check(f"feature_std_positive:{group}:{condition}", diagnostics.get("feature_std", 0) > 0,
                        diagnostics.get("feature_std"))
                v.check(f"timing_recorded:{group}:{condition}", diagnostics.get("elapsed_s", -1) >= 0,
                        diagnostics.get("elapsed_s"))
                v.check(f"gpu_peak_recorded:{group}:{condition}", diagnostics.get("peak_gpu_mib") is not None,
                        diagnostics.get("peak_gpu_mib"))
                if condition.startswith("lif") or condition == "degree_null_lif":
                    v.check(f"spike_rates_recorded:{group}:{condition}",
                            diagnostics.get("spike_rate") is not None and diagnostics.get("kc_readout_spike_rate") is not None,
                            {"spike_rate": diagnostics.get("spike_rate"), "kc": diagnostics.get("kc_readout_spike_rate")})
                for seed_record in item.get("per_seed", []):
                    expected_raw += 1
                    raw_path = Path(seed_record.get("raw_npz", ""))
                    v.check(f"raw_exists:{group}:{condition}:seed{seed_record.get('seed')}", raw_path.exists() and raw_path.stat().st_size > 0,
                            str(raw_path))
                    if raw_path.exists():
                        with np.load(raw_path, allow_pickle=False) as raw:
                            raw_acc = float(raw["accuracy"])
                            v.check(f"raw_accuracy_match:{group}:{condition}:seed{seed_record.get('seed')}",
                                    math.isclose(raw_acc, float(seed_record["accuracy"]), abs_tol=1e-12),
                                    {"raw": raw_acc, "json": seed_record["accuracy"]})
            ci = item.get("bootstrap_95ci_delta_vs_stateless")
            v.check(f"bootstrap_ci_present:{group}:{condition}", isinstance(ci, list) and len(ci) == 2, ci)
            q_value = item.get("bh_q_value")
            v.check(f"bh_q_in_range:{group}:{condition}", q_value is not None and 0 <= q_value <= 1, q_value)
    v.check("numerical_recomputation", not numerical_mismatches, numerical_mismatches)
    raw_count = len(list((project_dir / "evidence" / "raw").glob("*.npz")))
    # Method raw count plus 5 synthetic ceiling + 5 real ceiling; possibly 5 rejected DAVIS + 5 Sintel.
    v.check("raw_npz_at_least_method_seed_count", raw_count >= expected_raw + 10,
            {"actual": raw_count, "method_expected": expected_raw, "ceiling_min": 10})

    main_path = project_dir / "evidence" / "main_table.csv"
    if main_path.exists():
        table = pd.read_csv(main_path)
        v.check("main_table_row_count", len(table) == len(experiments) * len(EXPECTED_CONDITIONS), len(table))
        v.check("main_table_has_raw_values", table["accuracies"].notna().all(), table.columns.tolist())
    null_verify = result.get("degree_null_graph", {}).get("verification", {})
    v.check("degree_null_all_constraints", null_verify.get("all_passed") is True, null_verify)
    v.check("five_seed_power_limit_disclosed", "0.0625" in result.get("statistical_power_note", ""), result.get("statistical_power_note"))
    v.check("verdict_distinct_from_completion", result.get("verdict", {}).get("decision") in {"ACCEPT", "REJECT_FAILURE"} and bool(result.get("completion_distinction")), result.get("verdict"))

    return _payload(project_dir, result_path, v)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=PROJECT_DIR)
    args = parser.parse_args()
    validation = validate(args.project_dir.resolve())
    output = args.project_dir.resolve() / "validation.json"
    output.write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": validation["passed"],
        "summary": validation["summary"],
        "validation_path": str(output),
        "result_json_bytes": validation.get("result_json_bytes"),
        "result_json_sha256_prefix16": validation.get("result_json_sha256_prefix16"),
    }, indent=2, ensure_ascii=False))
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
