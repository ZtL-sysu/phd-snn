# Experiment traceability

| Row | Required evidence | Result | Status |
|---|---|---|---|
| LR-A | official-test rank128/2% logit MSE vs strong controls | 26.23/33.99/25.83% reductions | done, strong-pass |
| LR-B | T2/T4 task loss bound | worst 1.86 pp | done, strong-pass |
| LR-C | exact payload/padded cost | matched rows; Jacobian Pareto gain | done, strong-pass |
| LR-D | warmed full-pipeline timing/memory | p95 1.122×; peak ≤218.23 MB | done, strong-pass |
| LR-E | A2Q/One-Spike adaptations | proposed logit-MSE gain persists | done, strong-pass |

The first validation-derived and task-superiority attempts remain in `inputs/` and `corrections/`; they are not hidden.
