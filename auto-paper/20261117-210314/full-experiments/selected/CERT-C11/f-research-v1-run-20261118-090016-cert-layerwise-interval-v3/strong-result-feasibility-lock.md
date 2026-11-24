# Strong-result feasibility lock

Before corrected experiments, the binding expected-strong gate is:

1. 36/36 deterministic theorem/implementation containment.
2. Median proposed width/RMS ≤10 and every cell ≤15.
3. Per-cell tightening versus the global scalar reference ≥25%.
4. Proposed interval bound is no looser than the rowwise Euclidean bound under `atol=1e-10`, `rtol=1e-12`.
5. No clipping outside declared ranges, error-derived radius, NaN, Inf, or silent zero-denominator substitution.

Any failure blocks the strong claim and preserves the failed matrix; thresholds cannot be weakened.
