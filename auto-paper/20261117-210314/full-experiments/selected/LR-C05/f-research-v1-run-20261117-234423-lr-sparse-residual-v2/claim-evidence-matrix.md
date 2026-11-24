# Claim–evidence matrix

| ID | Claim | Falsifier | Strong controls | Required evidence |
|---|---|---|---|---|
| LR-A | sensitivity residual lowers hidden/logit MSE at exact cost | no ≥20% gain on 2/3 | top-abs, random, A2Q-style, uniform | 3×3×4×3 matrix |
| LR-B | task agreement improves at T2/4 | no ≥1 pp on 2/3 | full float and all equal-cost baselines | accuracy/agreement |
| LR-C | exact serialized cost explains gain | bit mismatch or no Pareto gain | exact factors/scales/index/value accounting | cost JSON |
| LR-D | full pipeline practical | p95 >1.2× or memory failure | warmed SVD-only/strong baseline | 3 warm + 7 timed repeats |
| LR-E | advantage survives prior-art adaptations | A2Q/One-Spike match or beat | explicit adapted baselines | same task/cost metrics |
