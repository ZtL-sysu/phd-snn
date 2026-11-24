#!/usr/bin/env python3
"""Independent artifact and raw-numeric validator for the P4 batch."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path("/home/novix/workspace/project")
RESULT = PROJECT / "result.json"
EVIDENCE = PROJECT / "evidence"
REQUIRED_EVIDENCE = [
    "main_table.csv",
    "ablation.json",
    "null.json",
    "diagnostics.json",
    "real_ceiling.json",
    "synthetic_ceiling.json",
    "stats.json",
    "robustness.json",
    "efficiency.json",
    "run_manifest.json",
    "experiment-traceability.csv",
]


def validate_metric(metric: dict[str, Any], errors: list[str], checked: list[str]) -> None:
    artifact = metric.get("artifact", {}).get("path")
    if not artifact:
        errors.append(f"metric lacks artifact: {metric.get('domain')}/{metric.get('task')}/{metric.get('condition')}/{metric.get('seed')}")
        return
    path = Path(artifact)
    if not path.exists():
        errors.append(f"missing raw metric artifact: {path}")
        return
    with np.load(path, allow_pickle=False) as archive:
        truth, pred = archive["y_true"], archive["y_pred"]
    recomputed = float(np.mean(truth == pred))
    if abs(recomputed - float(metric["accuracy"])) > 1e-12:
        errors.append(f"accuracy mismatch {path}: {metric['accuracy']} vs {recomputed}")
    checked.append(str(path))


def validate_stage_runs(stage: dict[str, Any], stage_name: str, errors: list[str], checked: list[str]) -> None:
    for task, conditions in (stage.get("runs") or {}).items():
        for condition, records in conditions.items():
            successful = [records.get(str(seed)) for seed in [1, 2, 3, 4, 5]]
            if any(not isinstance(metric, dict) or "accuracy" not in metric for metric in successful):
                errors.append(f"{stage_name}/{task}/{condition} does not contain five successful seeds")
                continue
            for metric in successful:
                validate_metric(metric, errors, checked)


def main() -> int:
    errors: list[str] = []
    checked: list[str] = []
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    if result.get("seeds") != [1, 2, 3, 4, 5]:
        errors.append("top-level seeds are not exactly [1,2,3,4,5]")
    if result.get("status") not in {"completed", "partial"}:
        errors.append(f"invalid final status: {result.get('status')}")
    stage_a = result.get("stage_A") or {}
    if stage_a.get("status") != "completed":
        errors.append("Stage A is not completed")
    else:
        validate_stage_runs(stage_a, "stage_A", errors, checked)
        graph = stage_a.get("graph", {})
        if graph.get("row_normalized") is not False:
            errors.append("graph was row-normalized")
        if abs(float(graph.get("normalized_spectral_radius_40_iter", 0.0)) - 0.95) > 1e-4:
            errors.append("graph spectral radius is not 0.95 within tolerance")
    stage_b = result.get("stage_B") or {}
    if stage_b.get("status") == "completed":
        validate_stage_runs(stage_b, "stage_B", errors, checked)
    elif stage_b.get("status") != "unavailable":
        errors.append(f"Stage B is neither completed nor explicitly unavailable: {stage_b.get('status')}")
    stage_c = result.get("stage_C") or {}
    if stage_c.get("status") not in {"completed", "partial"}:
        errors.append(f"Stage C is incomplete: {stage_c.get('status')}")

    for name in REQUIRED_EVIDENCE:
        path = EVIDENCE / name
        if not path.exists() or path.stat().st_size == 0:
            if name == "real_ceiling.json" and stage_b.get("status") == "unavailable":
                continue
            errors.append(f"required evidence missing/empty: {path}")
        else:
            checked.append(str(path))
    trace = EVIDENCE / "experiment-traceability.csv"
    if trace.exists():
        with trace.open("r", encoding="utf-8", newline="") as handle:
            for row_index, row in enumerate(csv.DictReader(handle), start=2):
                artifact = row.get("artifact_path")
                if not artifact:
                    errors.append(f"traceability row {row_index} has no artifact_path")
                elif not Path(artifact).exists():
                    errors.append(f"traceability row {row_index} points to missing artifact: {artifact}")

    for seed in [1, 2, 3, 4, 5]:
        meta_path = PROJECT / f"data/null_graphs/degree_null_seed{seed}.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            for key in ["in_degree_exact", "out_degree_exact", "nnz_exact", "original_reciprocal_edges_unchanged", "weights_exact_and_same_order"]:
                if meta.get(key) is not True:
                    errors.append(f"null seed {seed} failed invariant {key}")

    report = {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "raw_and_evidence_artifacts_checked": len(set(checked)),
        "stage_B_status": stage_b.get("status"),
        "final_status": result.get("status"),
    }
    (EVIDENCE / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
