# P3 baseline-first gate

## Decision

**PASS.** The simple global-radius outputwise comparator and strongest feasible Minkowski/norm comparator were frozen and evaluated before the full three-seed campaign.

## Baseline matrix

- 12 rows: 3 graphs × 2 levels × 2 quantizers at checkpoint seed 0.
- Raw artifacts: `results/cert-baseline.json` and `results/cert-baseline.csv`.
- Deterministic containment: 12/12.
- Minkowski comparator validity: 12/12.
- Global-uniform equality: 6/6; median tightening is zero as expected.
- Rowwise tightening: 78.38%–81.36%, median 80.97%.
- No clipping, non-finite values or zero-denominator substitutions.
- Descriptive proposed width/RMS: 9.99–28.30 for global-uniform and 15.84–36.91 for rowwise; this negative absolute-width evidence is preserved and is not used as a strong claim.

The baseline landscape supports the rowwise relative-tightening mechanism while explicitly rejecting an absolute-width claim.
