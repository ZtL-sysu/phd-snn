# P8 table plan

| Planned table | Scientific purpose | Evidence | Decision |
|---|---|---|---|
| Main fidelity and task trade-off | Report three-seed mean logit-MSE reductions and both task-loss maxima at the focal rank128/2% setting | `results/confirmation-summary.json` | include in TeX |
| Matched-budget adapted controls | Compare Output-Jacobian against our matched-budget A2Q-style and One-Spike-style adaptations | `results/confirmation-test-v2.json` | include in TeX |
| Exact cost and warmed cost | Record padded-bit equality, coefficient accounting, p95 ratio range, and peak memory | `results/confirmation-test-v2.json`, `inputs/v2-timing.json` | include in TeX |

These are compact evidence tables rather than decorative additions. Detailed raw rows remain outside the manuscript.
