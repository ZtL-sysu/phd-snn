# CCFA baseline evidence review

- The baseline landscape supports the claimed bottleneck: discrete neighbor and winner decisions degrade sharply under naive coding.
- Novelty delta remains plausible because the degradation is structural, not just activation MSE.
- The binding expected_strong result remains evidence-grounded at the structure level.
- Fatal risk: the current baseline rows do not include task accuracy on a trained classifier. P4 must add an end-to-end teacher and frozen test evaluation before any paper claim.
- Second risk: signed multilevel coding underperforms signed uniform, so the method variant must improve it through calibration or the method family must be revised under the correction policy.
- Decision: continue to P4 baseline-first full experiments; do not write the paper.
