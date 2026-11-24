# Matched external/control baselines

## Protocol

All methods use the same `teacher_seed41/42/43.pt` checkpoints, Fashion-MNIST official train calibration split (first 5,000 examples per seed), first 2,000 official test examples per seed, 16 levels, and the same unchanged teacher forward path with converted codes driving kNN, winners, messages, update, and readout. Search grids are in `strong-baseline-results.json`; no test example was used for parameter selection.

## Main results

| Method | Label | Accuracy mean ± SD | Message MSE mean | Events mean |
|---|---|---:|---:|---:|
| v1 scale-uniform control | internal control | 50.23 ± 4.32% | 0.007922 | 6,272,000 |
| v2 message-MSE uniform reference | internal control | 78.83 ± 0.79% | 0.001411 | 6,272,000 |
| Activation/feature-MSE uniform | faithful adaptation | 78.83 ± 0.79% | 0.001411 | 6,272,000 |
| Logit-MSE uniform | proxy | 78.83 ± 0.79% | 0.001411 | 6,272,000 |
| DCGS-style signed multilevel, default threshold | faithful adaptation | 18.53 ± 6.65% | 0.008290 | 2,799,201 |
| DCGS-style signed multilevel, message-selected threshold | proxy | 18.27 ± 5.31% | 0.008259 | 2,799,197 |
| DCGS-style signed multilevel, budget-match threshold | proxy | 19.13 ± 5.68% | 0.008272 | 2,799,194 |
| DCGS-style signed multilevel + feature/logit/message gamma | faithful/proxy | 18.53 ± 6.65% | 0.008290 | 2,799,201 |

Per-seed accuracy, message MSE, events, levels, and selected parameters are in `strong-baseline-results.json`.

## Interpretation

- Activation/feature MSE and logit MSE both select the same `(scale=15, offset=0.05)` as message MSE on this benchmark and therefore tie v2. This is an important negative result for novelty: on this code family, a standard activation-MSE calibration would reproduce the v2 number. The manuscript's claim that only message-level calibration works is not supported by this matched experiment.
- The DCGS-style signed multilevel implementation is a **faithful adaptation** only in the sense that the multilevel signed threshold encoder from the local helper was transferred to the Grapher. It is not the published DCGS implementation, and is labelled a proxy where a local search replaces missing external details. It fails badly under this Grapher forward path (18–19% mean accuracy), using fewer events but higher message MSE.
- The gamma search collapsed to 1.0 for all objectives; the logged runs are retained to show this was tested rather than omitted.
- The budget-match threshold scan selected the closest tested setting per seed (for seed 41, threshold 1.4) and still used only 45.8% of the uniform-code event rate in that seed. A fully faithful DCGS reproduction would require the original code and its event/level accounting; this run cannot claim that comparison.

## Failed attempts preserved

- First baseline version did not include gamma-calibrated DCGS controls; superseded by the current JSON.
- First gamma version showed all DCGS gamma objectives selecting 1.0; a threshold-expansion run was added rather than deleting the failed result.
- The first audit runs failed on loader unpacking and index-shape handling; errors are summarized in `structure-number-reconciliation.md`.
