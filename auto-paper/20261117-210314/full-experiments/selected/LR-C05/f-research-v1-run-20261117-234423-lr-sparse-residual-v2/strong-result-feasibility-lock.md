# P1A strong-result feasibility lock

| ID | Mechanism | Minimum / expected-strong / failure | Budget | Verdict |
|---|---|---|---|---|
| LR-A | sensitivity rank vs strong equal-cost allocation | finite / ≥8× on 2/3 and ≥20% hidden-logit MSE reduction / no gain | 3 seeds | pass |
| LR-B | residual allocation improves rate conversion | sane / ≥1 pp on 2/3 / no task gain | T2/T4 | pass |
| LR-C | exact serialization | matched bits / Pareto gain / mismatch | fixed grid | pass |
| LR-D | full warmed cost | finite / p95 ≤1.2× / tail dominates | 3+7 repeats | pass |
| LR-E | prior-art adaptation | runnable / beat on 2/3 or narrow novelty / lose | fixed grid | pass |

All rows have code paths, falsifiers, strong controls and bounded resources.
