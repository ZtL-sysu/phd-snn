# Remaining fatal-report issues

## Fixed or corrected in this run

-_FALSE per-seed claim: corrected in `seed-fact-correction.md`; true v2 values are 78.40 / 78.35 / 79.75.
-Seed-aware uncertainty: added `hierarchical-bootstrap-results.json`; seed-level interval [23.50, 33.45] pp versus pooled-example [27.17, 30.03] pp.
-Missing matched baselines: added `strong-baseline-results.json` and `strong-baseline-explanation.md`.
-Structure-number provenance: added `structure-number-audit.json` and `structure-number-reconciliation.md`.

## Still fatal or manuscript-blocking

1. **Message calibration may not be novel on this benchmark.** Matched feature-MSE and logit-MSE uniform baselines tie v2 exactly at 78.83% mean accuracy, 0.001411 message MSE, and 6,272,000 events. The claim that message-aware calibration uniquely explains the gain is not supported.

2. **The frozen structure numbers are irreproducible and partly misquoted.** A strict re-execution of `frozen_test.py` with saved checkpoints gives 0.805 / 0.660 for signed-uniform, not the stored means 0.065 / 0.482 or the manuscript's 0.065 / 0.488. The manuscript must remove or relabel those numbers; see `structure-number-reconciliation.md`.

3. **The P4 metric is mislabeled.** P4's 0.758 is overlap@k, not Jaccard. The manuscript currently treats the two metric families as commensurable.

4. **No faithful external DCGS reproduction exists in this run.** The signed-multilevel baseline is a local adaptation/proxy, uses fewer events, and fails at 18–19% accuracy; it cannot support a strong claim against published DCGS.

5. **Uncertainty reporting was too strong.** The paper's [27.2, 30.1] pp interval treats 6,000 example-seed predictions as independent. The seed-aware interval is [23.50, 33.45] pp with only three seeds; it is descriptive, not a precise confidence interval.

## Recommended action before resubmission

Remove the uniqueness claim for message MSE, either replace or explicitly qualify the frozen structure numbers, rename P4's metric to overlap@k, obtain a faithful published-DCGS implementation for a real external baseline, and report both pooled and seed-aware intervals. No manuscript files were modified in this run.
