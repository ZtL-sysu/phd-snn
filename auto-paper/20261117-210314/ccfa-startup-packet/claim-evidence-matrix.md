# Claim–evidence design matrix

| Claim family | Required direct comparison | Primary smoke evidence | Falsifying control | Full-paper evidence if admitted |
|---|---|---|---|---|
| Signed/heterophily conversion | Best nonnegative frozen-teacher conversion; sign-shuffled control | Paired teacher agreement and accuracy gap at T≤4, events/work | Sign information removed at same event count | ≥3 seeds, homophilous/heterophilous external validation |
| Graph-conditioned calibration | Source-only calibration; shuffled neighborhood | Internal-validation gain with fixed train-only fit | Neighborhood randomization; equal parameter count | Cross-dataset/graph-size shift and ablation |
| Adaptive computation | Uniform T and random stopping at equal work | Agreement–work Pareto, causal prefix, no future labels | Random or activation-only selection | Runtime/memory plus seeds and hard-example analysis |
| Residual/message compression | Equal-budget channel pruning/uniform quantization | Reconstruction + downstream fidelity at equal events | Same-rank random projector | Strong conversion baselines, actual event/work accounting |
| Robust conversion | Clean-calibrated equal-fidelity conversion | Robust agreement under frozen perturbations | Clean-MSE matched calibration | Multiple perturbation strengths/types, certified coverage |
| Uncertainty/adaptation | Confidence-only selection/source-frozen model | Paired target-shift validation improvement | Shuffled uncertainty/target-statistic control | Multiple shift families, target-only unlabeled protocol |

## Common reporting requirements

Record all tried configurations and IDs, teacher/reference logits, converted logits, events and executed graph operations, runtimes, environment/source hashes, and failure states. Primary outcomes are paired per-example fidelity/accuracy, not coordinate MSE alone. Smoke must improve on the strongest feasible control under the predeclared joint criterion; two datasets are required for broad visual/cross-graph claims.

No hardware-energy claim from spike counts. No direct-SNN result labeled as conversion. No official test read during discovery. Every accepted candidate receives its own numeric gate before execution.
