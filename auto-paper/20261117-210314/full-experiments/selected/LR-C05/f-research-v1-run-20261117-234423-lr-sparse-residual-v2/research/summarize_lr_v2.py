"""Summarize v2/v3 exact-cost results without changing raw evidence."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CONTROL_MODES = ("top_abs", "a2q_node_budget", "one_spike", "uniform", "random")


def aggregate(rows: list[dict], controls_rows: list[dict], dataset: str, budget: float) -> dict:
    proposed = [r for r in rows if r.get("dataset") == dataset and r.get("rank") == 128 and r.get("budget") == budget and r.get("basis") == "svd"]
    output = {"proposed_rows": len(proposed)}
    for metric in ("hidden_mse", "logit_mse"):
        proposed_value = float(np.mean([r[metric] for r in proposed]))
        controls = {
            mode: float(np.mean([r[metric] for r in controls_rows if r.get("dataset") == dataset and r.get("rank") == 128 and r.get("budget") == budget and r.get("basis") == "svd" and r.get("residual_mode") == mode]))
            for mode in CONTROL_MODES
        }
        best_mode = min(controls, key=controls.get)
        output[metric] = {
            "proposed": proposed_value,
            "best_control": best_mode,
            "best_control_value": controls[best_mode],
            "relative_reduction": float(1 - proposed_value / controls[best_mode]),
        }
    for step in ("T2", "T4"):
        proposed_value = float(np.mean([r[step]["teacher_agreement"] for r in proposed]))
        controls = {
            mode: float(np.mean([r[step]["teacher_agreement"] for r in controls_rows if r.get("dataset") == dataset and r.get("rank") == 128 and r.get("budget") == budget and r.get("basis") == "svd" and r.get("residual_mode") == mode]))
            for mode in CONTROL_MODES
        }
        best_mode = max(controls, key=controls.get)
        output[step] = {
            "proposed": proposed_value,
            "best_control": best_mode,
            "best_control_value": controls[best_mode],
            "gain_pp": float(100 * (proposed_value - controls[best_mode])),
        }
    return output


def main() -> None:
    baseline = json.loads((ROOT / "results/baseline.json").read_text(encoding="utf-8"))["rows"]
    method = json.loads((ROOT / "results/method-v3-jacobian-exact.json").read_text(encoding="utf-8"))["rows"]
    summary = {"datasets": {}, "budgets": {}}
    for dataset in ("cora", "chameleon", "squirrel"):
        summary["datasets"][dataset] = {}
        for budget in (0.005, 0.01, 0.02):
            summary["datasets"][dataset][str(budget)] = aggregate(method, baseline, dataset, budget)
    summary["strong_gates_at_2pct"] = {
        "LR_A_logit_mse": all(
            summary["datasets"][dataset]["0.02"]["logit_mse"]["relative_reduction"] >= 0.20
            for dataset in ("cora", "chameleon", "squirrel")
        ),
        "LR_B_task_gain": sum(
            max(summary["datasets"][dataset]["0.02"]["T2"]["gain_pp"], summary["datasets"][dataset]["0.02"]["T4"]["gain_pp"]) >= 1.0
            for dataset in ("cora", "chameleon", "squirrel")
        ) >= 2,
    }
    (ROOT / "results/summary-v2.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
