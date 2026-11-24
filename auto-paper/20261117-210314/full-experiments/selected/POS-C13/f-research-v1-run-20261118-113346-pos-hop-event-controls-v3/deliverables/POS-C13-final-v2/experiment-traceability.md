# Experiment traceability

| Batch | Matrix | Rows | Status | Outputs |
|---|---|---:|---|---|
| P3 representation | 2 graphs × 4 methods plus 5 permutations and 5 shuffles | 8 + 10 + 10 | done | `results/pos-representation.json`, CSV, summary |
| P4 task/probe | 2 graphs × 5 split seeds × 4 retrained methods | 40 | done | `results/pos-task-rows.json`, CSV |
| P4 fixed probe | 2 graphs × 5 split seeds × 4 ordered + 5 shuffled | 90 | done | `results/pos-task-rows.json` controls |

All task codebooks use training-only fitting and escape thresholds. Fixed raw probes reuse identical weights, splits and evaluation nodes. Raw rows retain escape fractions, bit ledgers and failure fields. The first task run used full-data probe fitting and is preserved in `corrections/pos-task-leaky-probe-v1.json` as negative evidence; corrected rows train only on split train indices.
