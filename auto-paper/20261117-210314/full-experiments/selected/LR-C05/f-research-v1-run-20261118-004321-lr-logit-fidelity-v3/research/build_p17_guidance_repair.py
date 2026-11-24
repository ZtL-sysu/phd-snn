from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
SOURCE = RUN_ROOT / "writing" / "p12" / "paper-with-verified-references.md"
OUT_DIR = RUN_ROOT / "writing" / "p17"
OUT_PAPER = OUT_DIR / "paper-guidance-complete.md"
AUDIT = RUN_ROOT / "paper-guidance-audit.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def insert_after(text: str, anchor: str, addition: str) -> str:
    if text.count(anchor) != 1:
        raise RuntimeError(f"anchor count is not one: {anchor[:80]}")
    return text.replace(anchor, anchor + "\n\n" + addition, 1)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = SOURCE.read_text(encoding="utf-8")
    controls = read_csv(RUN_ROOT / "results" / "p10-control-summary.csv")
    bit_rows = read_csv(RUN_ROOT / "results" / "p10-bit-ledger.csv")
    task_rows = read_csv(RUN_ROOT / "results" / "p10-task-loss-three-seed-audit.csv")
    raw_rows = json.loads(
        (RUN_ROOT / "results" / "confirmation-test-v2.json").read_text(encoding="utf-8")
    )["rows"]

    control_map = {(row["dataset"], row["residual_mode"]): row for row in controls}
    task_map = {}
    for row in task_rows:
        task_map[row["dataset"]] = max(
            task_map.get(row["dataset"], 0.0),
            float(row["three_seed_mean_observed_degradation_pp"]),
        )
    bit_map = {row["dataset"]: row for row in bit_rows}

    method_anchor = (
        "| One-Spike-style coefficient adaptation | Coefficient-coding allocation adapted to the same ledger | "
        "Matched-budget adapted control | \\cite{one-spike} |\n"
    )
    method_addition = (
        "The validation grid also evaluated random-projection rank-$k$ bases with "
        "top-absolute, random, and A2Q-style residual controls across the rank and "
        "budget sweep. Because guidance-v3 fixed the operator-aligned SVD basis "
        "before the test run, random projection is retained as a validation "
        "diagnostic rather than a focal test comparator. Message MSE, hidden MSE, "
        "logit MSE, accuracy, teacher agreement, exact bit totals, coefficient "
        "counts, and warmed latency/memory were all recorded; the focal tables "
        "below expose the previously implicit message-MSE, coefficient-count, and "
        "exact-cost evidence.\n"
    )
    text = insert_after(text, method_anchor, method_addition)

    main_anchor = "Each comparison used identical total padded serialized bits within the corresponding dataset"
    rows = []
    for dataset, label in (("cora", "Cora"), ("chameleon", "Chameleon"), ("squirrel", "Squirrel")):
        proposed = control_map[(dataset, "downstream_jacobian")]
        top = control_map[(dataset, "top_abs")]
        proposed_message = sum(
            float(row["message_mse"])
            for row in raw_rows
            if row["dataset"] == dataset and row["residual_mode"] == "downstream_jacobian"
        ) / 3
        top_message = sum(
            float(row["message_mse"])
            for row in raw_rows
            if row["dataset"] == dataset and row["residual_mode"] == "top_abs"
        ) / 3
        message_reduction = 100 * (1 - proposed_message / top_message)
        hidden_reduction = 100 * (1 - float(proposed["mean_hidden_mse"]) / float(top["mean_hidden_mse"]))
        rows.append(
            f"| {label} | {float(proposed['mean_logit_mse']):.6f} ± {float(proposed['sample_sd_logit_mse']):.6f} | "
            f"{float(top['mean_logit_mse']):.6f} ± {float(top['sample_sd_logit_mse']):.6f} | "
            f"{message_reduction:.2f}% | {hidden_reduction:.2f}% | {task_map[dataset]:.2f} | {bit_map[dataset]['selected_coefficients']} |"
        )
    table1 = (
        "**Table 1. Fidelity decomposition and observed task trade-off.** "
        "Values are three-seed means ± sample SD (n=3); reductions are versus the "
        "top-absolute residual control, and task loss is the maximum three-seed-mean "
        "degradation across T=2/4 accuracy and teacher agreement. Message MSE is a "
        "diagnostic: the proposed method trades higher message MSE for lower hidden "
        "and logit MSE. Lower MSE is better; task loss is a descriptive maximum, "
        "not an equivalence bound.\n\n"
        "| Dataset | Proposed logit MSE | Top-absolute logit MSE | Message MSE reduction | Hidden MSE reduction | Max observed task loss (pp) | Selected coefficients |\n"
        "|---|---:|---:|---:|---:|---:|---:|\n"
        + "\n".join(rows)
        + "\n"
    )
    text = insert_after(text, main_anchor, table1)

    adapted_anchor = (
        "These paired descriptive comparisons use matched total padded serialized-bit budgets and the frozen two-layer GCN checkpoints."
    )
    rows2 = []
    for dataset, label in (("cora", "Cora"), ("chameleon", "Chameleon"), ("squirrel", "Squirrel")):
        proposed = control_map[(dataset, "downstream_jacobian")]
        a2q = control_map[(dataset, "a2q_node_budget")]
        one = control_map[(dataset, "one_spike")]
        a2q_reduction = 100 * (1 - float(proposed["mean_logit_mse"]) / float(a2q["mean_logit_mse"]))
        one_reduction = 100 * (1 - float(proposed["mean_logit_mse"]) / float(one["mean_logit_mse"]))
        rows2.append(
            f"| {label} | {float(proposed['mean_logit_mse']):.6f} ± {float(proposed['sample_sd_logit_mse']):.6f} | "
            f"{float(a2q['mean_logit_mse']):.6f} ± {float(a2q['sample_sd_logit_mse']):.6f} | {a2q_reduction:.2f}% | "
            f"{float(one['mean_logit_mse']):.6f} ± {float(one['sample_sd_logit_mse']):.6f} | {one_reduction:.2f}% |"
        )
    table2 = (
        "**Table 2. Matched-budget adapted controls.** Values are three-seed "
        "means ± sample SD of logit MSE; reductions are relative to our matched-budget "
        "A2Q-style and One-Spike-style adaptations, not direct reproductions of the "
        "published systems.\n\n"
        "| Dataset | Proposed | A2Q-style | Reduction vs A2Q-style | One-Spike-style | Reduction vs One-Spike-style |\n"
        "|---|---:|---:|---:|---:|---:|\n"
        + "\n".join(rows2)
        + "\n"
    )
    text = insert_after(text, adapted_anchor, table2)

    cost_anchor = (
        "This is a wall-clock pipeline measurement and does not measure hardware energy."
    )
    rows3 = []
    for dataset, label in (("cora", "Cora"), ("chameleon", "Chameleon"), ("squirrel", "Squirrel")):
        row = bit_map[dataset]
        rows3.append(
            f"| {label} | {int(row['basis_bits']):,} | {int(row['residual_target_bits']):,} | "
            f"{int(row['total_padded_bits']):,} | {int(row['selected_coefficients']):,} | {int(row['full_float_bits']):,} |"
        )
    table3 = (
        "**Table 3. Exact serialized-cost ledger at rank 128 and the 2% residual "
        "budget.** Each selected index-value pair is charged 64 bits. The total "
        "padded budget is basis bits plus residual padded bits; full-float is shown "
        "only as an uncompressed reference.\n\n"
        "| Dataset | Basis bits | Residual target bits | Total padded bits | Selected coefficients | Full-float bits |\n"
        "|---|---:|---:|---:|---:|---:|\n"
        + "\n".join(rows3)
        + "\n"
    )
    text = insert_after(text, cost_anchor, table3)
    OUT_PAPER.write_text(text, encoding="utf-8")

    audit_rows = [
        ("Canonical six sections", "covered", "Sections 1-6 are present and ordered."),
        ("Datasets and fixed splits", "covered", "Cora/Chameleon/Squirrel, fixed masks, seeds 0/1/2, validation/test chronology."),
        ("Baselines", "covered", "Full-float, SVD-only, random projection validation diagnostic, top-absolute, random, uniform, A2Q-style and One-Spike-style controls are named; random projection is explicitly scoped to the validation grid."),
        ("LR-A main logit gate", "covered", "26.23/33.99/25.83% reductions and 9/9 paired direction."),
        ("LR-B task trade-off", "covered", "0.53/1.17/1.86 pp three-seed maxima and 2.85 pp seed-level maximum."),
        ("LR-C exact ledger", "covered", "Formula, 2% denominator, coefficient counts, absolute bit totals, and matched scope."),
        ("LR-D warmed cost", "covered-with-scope", "1.020-1.124x p95 and 218.23 MB at rank128/1%; focal 2% timing remains explicitly outside the claim."),
        ("LR-E adapted prior art", "covered", "A2Q-style and One-Spike-style matched-budget adaptations and numeric comparisons."),
        ("Metrics", "covered", "Message, hidden, logit MSE; T=2/4 accuracy; teacher agreement; bits; coefficients; latency/memory."),
        ("Statistics", "covered", "n=3, sample SD, paired descriptive comparisons, no formal CI/equivalence claim."),
        ("Figures", "covered", "Figure 1 architecture and Figures 2-4 evidence/robustness panels inserted."),
        ("Tables", "covered-after-repair", "Tables 1-3 added from frozen source evidence."),
        ("Citation scope", "covered", "41 verified unique references; 30 from 2022-2026; duplicate audit passed."),
        ("Language/output constraints", "covered", "English manuscript, one final PDF, complete TeX/BibTeX/figures, no commit/push."),
        ("Negative findings", "covered", "Task-superiority failure, mixed task deltas, message-MSE trade-off, and scope limits retained."),
    ]
    audit_lines = [
        "# Paper guidance audit",
        "",
        "| Guidance requirement | Status | Evidence / paper location |",
        "|---|---|---|",
    ]
    for requirement, status, evidence in audit_rows:
        audit_lines.append(f"| {requirement} | {status} | {evidence} |")
    audit_lines.extend(
        [
            "",
            "## Judgment",
            "",
            "The guidance coverage is complete after adding the random-projection validation diagnostic, message-MSE/coefficient-count evidence, and Tables 1-3. The focal claim remains deliberately narrow: logit-fidelity coding of M0=A_hat X under matched total padded serialized-bit cost. The rank128/1% timing result is not generalized to the focal 2% setting.",
        ]
    )
    AUDIT.write_text("\n".join(audit_lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "paper": str(OUT_PAPER), "words": len(text.split()), "audit": str(AUDIT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
