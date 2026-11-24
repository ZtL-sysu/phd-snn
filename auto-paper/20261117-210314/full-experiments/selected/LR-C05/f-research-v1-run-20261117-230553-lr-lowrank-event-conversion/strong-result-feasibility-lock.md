# P1A strong-result feasibility lock

Mode: `ccf-experiment-designer` design. Prior LR screen is baseline-calibration evidence only.

| ID | Prerequisites | Baseline path | Minimum / expected-strong / failure | Budget | Verdict |
|---|---|---|---|---|---|
| LR-A | local graphs/checkpoints; CUDA SVD | float/SVD/random/uniform | complete curves / ≥8× on 2/3 and ≥20% error reduction / no equal-budget gain | 3 seeds | pass |
| LR-B | reconstructed hidden messages; conversion code | SVD-only/random/uniform residual | sane task / ≥1 pp agreement on 2/3 at T2 or T4 / only MSE gain | 3 seeds | pass |
| LR-C | exact bit/event counters | equal-bit residual controls | finite / ≥2× fewer bits or ≥1 pp at matched bits / budget contradiction | same runs | pass |
| LR-D | timing and allocator counters | SVD-only | finite / no >20% regression or documented trade-off / unbounded cost | same runs | pass |

Every row has a runnable path, falsifier, strong baseline and bounded resources. No target assumes energy or universal GNN scope.
