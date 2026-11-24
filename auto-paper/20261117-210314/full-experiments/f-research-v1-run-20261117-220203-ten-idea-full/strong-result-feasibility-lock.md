# P1A strong-result feasibility lock

Mode: `ccf-experiment-designer` design. Every row is a planned target calibrated to prior smoke or a matched control, not a desired arbitrary gain.

| ID | Prerequisites | Baseline path | Minimum / expected-strong / failure | Budget | Verdict |
|---|---|---|---|---|---|
| DYN-C01 | 728 labeled clips; deterministic split | raw absolute vs residual | exact prefix; ≥10%/≥15% reduction and ≤1 pp accuracy loss; leakage or <10% | 5 seeds CPU/GPU | pass |
| EQ-C02 | typed coordinates; rotations | raw vs component-uniform | ≤1e-8; ≤2 pp loss + ≥1 pp control gain + ≤10% error; otherwise unsupported | 5 seeds | pass with scope: coordinate encoder only |
| PERM-C03 | real sparse graphs | naive row order | exact; naive counterexample required | CPU | pass |
| SIGN-C04 | signed preactivations; labels | abs/positive-only | exact; ≥2 pp mean on both heterophilic sets; miss → no benefit claim | 3 seeds | pass |
| LR-C05 | message matrices; deterministic ranks | random projection | finite; ≥8× and ≥20% MSE reduction; miss → compression-only | CPU | pass |
| EDGE-C06 | finite FlyWire weights | uniform/float | <50%; ≥4×, ≤20%, ≥10% better than uniform; miss → no nonuniform claim | CPU | pass |
| CERT-C11 | quantization errors and weights | global bound | 100%; width≤10×RMS and ≥25% tighter; uncovered error invalidates | CPU | pass |
| POS-C13 | normalized hop features | raw/uniform | exact permutation; ≤5%, ≤2 pp, ≥4×; miss → certificate-only | CPU | pass |
| DLY-C14 | DAVIS labels/clips | delay0/absolute | causal; ≤1 pp and ≥10% reduction on ≥4/5; leak/<10% fail | 5 seeds | pass with scope: application bridge |
| READ-C18 | converted logits, C≥2 | full/top1 | top2 exact; ≥50% slots; any change or reduction miss | graph seeds | pass |

All main claims have a runnable local path, falsifier, matched controls and finite budget. No binding target assumes hardware energy. Strong wording remains blocked until P5 actual evidence.
