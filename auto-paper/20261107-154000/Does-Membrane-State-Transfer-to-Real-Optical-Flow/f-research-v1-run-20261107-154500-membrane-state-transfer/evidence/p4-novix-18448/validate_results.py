#!/usr/bin/env python3
"""Strict structural/semantic validator for attempt #5 result artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

PROJECT = Path("/home/novix/workspace/project")
EXPECTED_VARIANTS = {
    "current",
    "temporal_w2",
    "temporal_w4",
    "temporal_w8",
    "multiscale",
    "oracle_gt",
    "difficulty_stratified",
}
ALLOWED_STATES = {"LABEL_NOT_DECODABLE", "INPUT_BOTTLENECK", "DOMAIN_USABLE"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_objects(result: dict[str, Any], config: dict[str, Any], project: Path = PROJECT) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, predicate: bool, detail: Any = None) -> None:
        checks.append({"name": name, "passed": bool(predicate), "detail": detail})

    check("result_schema", result.get("schema_version") == "f-research-v1.p4.c1.attempt5.result.v1")
    check("config_schema", config.get("schema_version") == "f-research-v1.p4.c1.attempt5.preregistered.v1")
    thresholds = config.get("thresholds", {})
    check("real_threshold_frozen", thresholds.get("real_domain_ceiling") == 0.70)
    check("minimum_delta_frozen", thresholds.get("c1_minimum_real_delta") == 0.15)
    check("strong_delta_frozen", thresholds.get("c1_expected_strong_real_delta") == 0.25)
    check("thresholds_not_lowered", thresholds.get("thresholds_lowered") is False)
    check("primary_seeds", config.get("randomness", {}).get("primary_seeds") == [1, 2, 3, 4, 5])
    check("extended_seeds", config.get("randomness", {}).get("extended_seeds") == list(range(1, 12)))
    check("bootstrap_2000", config.get("statistics", {}).get("bootstrap_resamples") == 2000)
    check("test_families_frozen", config.get("statistics", {}).get("test_families") == ["exact_sign_flip", "paired_bootstrap_percentile", "paired_permutation"])
    check("n5_min_p", config.get("statistics", {}).get("minimum_attainable_two_sided_p", {}).get("n5") == 0.0625)
    check("n11_min_p", config.get("statistics", {}).get("minimum_attainable_two_sided_p", {}).get("n11") == 0.0009765625)

    grind = result.get("grind_block", {})
    for key in ("上一轮失败点", "本轮假设", "具体改动", "预期信号_若失败下一步"):
        check(f"grind_block_{key}", isinstance(grind.get(key), str) and len(grind[key]) > 100)
    check("grind_hypothesis_marked_not_conclusion", "假设不是结论" in grind.get("本轮假设", ""))
    check("grind_forbids_collapse_repair", "禁止继续沿「修复零方差塌缩」" in grind.get("上一轮失败点", ""))

    integrity = result.get("data_integrity", {})
    files = integrity.get("files", [])
    expected_file_ids = {x["id"] for x in config.get("downloads", {}).get("files", [])}
    check("all_data_ids_reported", {x.get("id") for x in files} == expected_file_ids)
    check("all_data_sizes_reported", all(isinstance(x.get("bytes"), int) for x in files))
    check("all_data_hashes_reported", all(x.get("sha256") or not x.get("available") for x in files))

    ladder = result.get("real_domain_ceiling_ladder", {})
    check("real_domains_exact", set(ladder) == {"DAVIS", "SINTEL"})
    for domain in ("DAVIS", "SINTEL"):
        block = ladder.get(domain, {})
        check(f"{domain}_all_ladder_variants", set(block) == EXPECTED_VARIANTS, sorted(block))
        for variant in EXPECTED_VARIANTS:
            row = block.get(variant, {})
            check(f"{domain}_{variant}_five_seeds", len(row.get("seed_results", [])) == 5)
            check(f"{domain}_{variant}_sample_count", int(row.get("sample_count", 0)) >= 4)
            check(f"{domain}_{variant}_ci", len(row.get("five_seed_ceiling", {}).get("bootstrap_95pct_ci", [])) == 2)
            check(f"{domain}_{variant}_mi", row.get("mi_bin_count") == 8 and bool(row.get("mi_estimator")))
            check(f"{domain}_{variant}_all_reported", row.get("all_registered_condition_reported") is True)
        state = result.get("decidability_states", {}).get(domain, {})
        check(f"{domain}_valid_state", state.get("decidability_state") in ALLOWED_STATES)
        check(f"{domain}_state_has_basis", bool(state.get("basis")))
        check(f"{domain}_state_has_gap_ci", len(state.get("oracle_minus_current_bootstrap_95pct_ci", [])) == 2)
        check(f"{domain}_no_ci_thresholding", state.get("ci_upper_bound_used_for_state") is False)
        deltas = result.get("real_domain_contrasts", {}).get(domain)
        if state.get("decidability_state") == "DOMAIN_USABLE":
            check(f"{domain}_delta_present_when_usable", isinstance(deltas, dict))
        else:
            check(f"{domain}_delta_absent_when_unusable", deltas is None)

    both_unusable = all(
        result.get("decidability_states", {}).get(d, {}).get("decidability_state") != "DOMAIN_USABLE"
        for d in ("DAVIS", "SINTEL")
    )
    if both_unusable:
        check(
            "both_unusable_migration_verdict",
            result.get("migration_verdict") == "NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE",
        )
        check("both_unusable_no_transfer_claim", result.get("transfer_claim_made") is False)

    c1_minimum_met = result.get("c1_guidance", {}).get("minimum_met") is True
    check(
        "positive_transfer_claim_requires_c1_minimum",
        result.get("transfer_claim_made") is bool(c1_minimum_met),
    )
    if not c1_minimum_met:
        check(
            "failed_c1_has_no_positive_transfer_claim",
            result.get("transfer_claim_made") is False
            and result.get("transfer_outcome_verdict")
            in {
                "NO_POSITIVE_TRANSFER_C1_MINIMUM_NOT_MET",
                "NO_TRANSFER_CLAIM_REAL_DOMAINS_UNAVAILABLE",
            },
        )

    graph = result.get("connectome", {})
    check("hop_1_to_8", len(graph.get("eye_to_kc_exact_hop_counts", [])) == 8)
    check("selected_kc_count_positive", int(graph.get("selected_kc_count", 0)) > 0)
    check("full_edge_rows", int(graph.get("graph_statistics", {}).get("raw_rows", 0)) > 1_000_000)
    null_checks = graph.get("degree_null", {}).get("checks", {})
    for key in ("per_node_in_degree_exact", "per_node_out_degree_exact", "weight_multiset_exact", "nnz_exact", "reciprocal_pairs_exact", "self_loops_exact"):
        check(f"degree_null_{key}", null_checks.get(key) is True)

    audit = result.get("cross_implementation_audit", {})
    check("seven_single_factors", len(audit.get("single_factor_variants", [])) == 7)
    check("two_audit_endpoints", len(audit.get("endpoints", [])) == 2)
    check("prior_discrepancies_preserved", "504.30" in json.dumps(audit.get("prior_report_references", {}), ensure_ascii=False))
    for row in audit.get("single_factor_variants", []) + audit.get("endpoints", []):
        check(f"audit_{row.get('variant_id')}_five_tensor_stages", all(k in row.get("tensor_fingerprints", {}) for k in ("drive", "syn", "v", "soft", "hard")))

    synthetic = result.get("synthetic", {})
    check("synthetic_explicit_label", synthetic.get("domain_label") == "SYNTHETIC")
    check("synthetic_ceiling_five", len(synthetic.get("ceiling", {}).get("values", [])) == 5)
    conditions = synthetic.get("conditions", {})
    expected_conditions = set(config.get("synthetic", {}).get("historical_anchor_conditions", [])) | set(config.get("synthetic", {}).get("one_factor_ablations", [])) | set(config.get("synthetic", {}).get("negative_controls", []))
    # zero_effect is named in controls; degree_null appears in both, so subset is intentional.
    check("all_registered_synthetic_conditions_present", expected_conditions.issubset(set(conditions)), sorted(set(conditions)))
    check("all_synthetic_conditions_11_seeds", all(len(x.get("seed_results", [])) == 11 for x in conditions.values()))
    check("A0_guardrail", "not evidence" in config.get("synthetic", {}).get("A0_definition", ""))

    power_rows = result.get("statistical_power_matrix", [])
    check("power_matrix_28_rows", len(power_rows) == 2 * len(config.get("statistics", {}).get("primary_contrasts", [])))
    check("power_matrix_cohorts", {x.get("n_pairs") for x in power_rows} == {5, 11})
    check("power_matrix_all_tests", all(set(x.get("tests", {})) == set(config.get("statistics", {}).get("test_families", [])) for x in power_rows))
    check("power_matrix_all_bh", all(all("bh_q" in y for y in x.get("tests", {}).values()) for x in power_rows))
    neg = result.get("statistical_power", {}).get("negative_control_calibration", {})
    check("label_permutation_calibration", "label_permutation_minus_lif_combo" in neg)
    check("zero_effect_calibration", neg.get("zero_effect_injection", {}).get("calibrated_nonsignificant") is True)

    invariants = result.get("invariant_checks", {})
    check("four_invariant_checks", set(invariants) == {"kc_reachable_count", "synthetic_ceiling", "real_domain_ceiling", "data_integrity"})
    check("no_zero_information_termination", result.get("zero_information_termination") is False)
    check("configuration_diff_present", len(result.get("configuration_diff_from_18390", [])) >= 10)
    check("unavailable_conditions_list", isinstance(result.get("unavailable_conditions"), list))
    check("gpu_report", bool(result.get("hardware", {}).get("gpu", {}).get("name")))
    check("runtime_report", float(result.get("runtime", {}).get("wall_seconds", 0)) > 0)

    raw_dir = project / "evidence" / "raw"
    raw_files = list(raw_dir.glob("*.npz")) if raw_dir.exists() else []
    check("raw_npz_present", len(raw_files) > 0, len(raw_files))
    check("raw_npz_count_matches", len(raw_files) == int(result.get("artifact_counts", {}).get("raw_npz", -1)), len(raw_files))

    failed = [x for x in checks if not x["passed"]]
    return {
        "schema_version": "attempt5-validation.v1",
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "design_valid": len(failed) == 0,
        "checks": checks,
        "failed_checks": failed,
    }


def validate_manifest(project: Path = PROJECT) -> dict[str, Any]:
    """Read-only verification of every MANIFEST entry, including self-size."""
    manifest = project / "MANIFEST.txt"
    failures: list[dict[str, Any]] = []
    if not manifest.exists():
        return {"valid": False, "entries": 0, "failures": [{"path": "MANIFEST.txt", "reason": "missing"}]}
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[1] != "# path\texists\tbytes\tsha256":
        return {"valid": False, "entries": 0, "failures": [{"path": "MANIFEST.txt", "reason": "bad_header"}]}
    entries = 0
    root = project.resolve()
    for line in lines[2:]:
        parts = line.split("\t")
        if len(parts) != 4:
            failures.append({"path": "MANIFEST.txt", "reason": "malformed_entry", "line": line})
            continue
        rel, expected_exists, expected_size_text, expected_sha = parts
        entries += 1
        try:
            expected_size = int(expected_size_text)
            path = (project / rel).resolve()
            if path != root and root not in path.parents:
                raise ValueError("path escapes project")
        except Exception as exc:
            failures.append({"path": rel, "reason": f"invalid_path_or_size:{exc!r}"})
            continue
        actual_exists = path.exists() and path.is_file()
        if (expected_exists == "true") != actual_exists:
            failures.append({"path": rel, "reason": "existence_mismatch"})
            continue
        if not actual_exists:
            continue
        actual_size = path.stat().st_size
        if actual_size != expected_size:
            failures.append(
                {"path": rel, "reason": "size_mismatch", "expected": expected_size, "actual": actual_size}
            )
            continue
        if rel == "MANIFEST.txt":
            if expected_sha != "SELF_SHA256_NOT_RECURSIVELY_DEFINED":
                failures.append({"path": rel, "reason": "bad_self_hash_sentinel"})
        else:
            actual_sha = sha256(path)
            if actual_sha != expected_sha:
                failures.append(
                    {"path": rel, "reason": "sha256_mismatch", "expected": expected_sha, "actual": actual_sha}
                )
    return {"valid": not failures, "entries": entries, "failures": failures}


def validate_files(project: Path = PROJECT) -> dict[str, Any]:
    result_path = project / "result.json"
    config_path = project / "config.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    report = validate_objects(result, config, project)
    snapshot_result = project / "evidence" / "result_snapshot.json"
    snapshot_config = project / "evidence" / "config_snapshot.json"
    report["final_file_checks"] = {
        "result_snapshot_byte_identical": snapshot_result.exists() and result_path.read_bytes() == snapshot_result.read_bytes(),
        "config_snapshot_byte_identical": snapshot_config.exists() and config_path.read_bytes() == snapshot_config.read_bytes(),
        "result_sha256": sha256(result_path),
        "config_sha256": sha256(config_path),
    }
    if not all(v for k, v in report["final_file_checks"].items() if k.endswith("byte_identical")):
        report["design_valid"] = False
    report["manifest_checks"] = validate_manifest(project)
    if not report["manifest_checks"]["valid"]:
        report["design_valid"] = False
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT)
    parser.add_argument("--write", action="store_true", help="write evidence/validation_posthoc.json")
    parser.add_argument("--summary", action="store_true", help="print only the read-only validation summary")
    args = parser.parse_args()
    report = validate_files(args.project)
    if args.summary:
        print(
            json.dumps(
                {
                    "design_valid": report["design_valid"],
                    "semantic_checks_total": report["total"],
                    "semantic_checks_failed": report["failed"],
                    "snapshots_byte_identical": all(
                        value
                        for key, value in report["final_file_checks"].items()
                        if key.endswith("byte_identical")
                    ),
                    "manifest_valid": report["manifest_checks"]["valid"],
                    "manifest_entries": report["manifest_checks"]["entries"],
                    "manifest_failures": report["manifest_checks"]["failures"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.write:
        path = args.project / "evidence" / "validation_posthoc.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["design_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
