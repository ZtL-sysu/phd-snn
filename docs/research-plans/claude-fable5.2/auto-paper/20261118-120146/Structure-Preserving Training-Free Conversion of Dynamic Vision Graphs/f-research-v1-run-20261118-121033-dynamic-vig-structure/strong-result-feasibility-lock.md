# Strong-result feasibility lock

| Claim | Mechanism + falsifier | Direct baselines | Baseline-calibrated threshold | Code path | Prototype | Budget | Verdict |
|---|---|---|---|---|---|---|---|
| C1 structure error is measurable | Quantization perturbs distances/signed max; teacher-feature restoration must eliminate disagreement | unsigned rate, signed uniform, DCGS-family signed multi-threshold | >=5 pp Jaccard loss or >=2 pp winner-agreement loss at T<=4 | clean PyTorch Grapher + independent coding reimplementation | 64-sample finite/shape/oracle check | 24 h, 8 GB, 3 seeds, 12 trials | pass |
| C2 structure-aware calibration helps | Optimize discrete disagreement; MSE-only matched control must not match it | MSE-only and matched-event signed coding | >=50% disagreement recovery, <=1 pp teacher gap, no event increase | calibration objective on train/calibration only | calibration loss decreases before test | included in C1 | pass |
| C3 structure explains accuracy | Teacher neighbor/winner oracles; both-oracle must explain recovery | random-neighbor, neighbor-only, winner-only, both-oracle | method recovers >=50% of both-oracle gain | diagnostic-only Grapher oracle inputs | oracle exactly matches teacher when all features are teacher features | included in C1 | pass |

## Lock decision

All three main claims pass the pre-experiment feasibility lock. The thresholds are not lowered. Any failure opens `correction-loop-state.md` and `correction-ledger.md`; paper writing remains blocked.
