# Strong-result feasibility lock

The binding expected-strong result is frozen before corrected operator-aware experiments:

1. All 36 graph/seed/level/quantizer cells contain every measured post-ReLU logit error within the deterministic output-column bound.
2. Median proposed width/RMS is at most 10 and no individual cell exceeds 15.
3. Minimum tightening relative to the global scalar bound is at least 25%, with median and full range reported.
4. The proposed interval bound is no looser than the Euclidean comparator beyond numerical tolerance.
5. Coverage is reported only as theorem/implementation containment, not independent statistical coverage.

Failure of any condition prevents the strong claim. The run must preserve the failed matrix and return to correction or narrow the claim rather than lowering the threshold.
