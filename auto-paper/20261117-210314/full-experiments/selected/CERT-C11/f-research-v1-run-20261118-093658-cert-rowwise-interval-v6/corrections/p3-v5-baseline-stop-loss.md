# P3 v5 baseline stop-loss

The v5 seed-0 baseline-first run had 12/12 deterministic containment and valid Minkowski comparisons, but global-uniform width/RMS reached 28.3 and rowwise/per-channel tightening was not yet the accepted method. The absolute width thresholds were not evidence-grounded for the corrected two-aggregation chain.

Guidance-v6 changes the scientific claim rather than weakening it silently:

- Replace per-channel radii with rowwise radii, giving `Delta∈R^(N×H)` and the matrix bound `|A||A|Delta|W1|`.
- Keep deterministic containment and the valid Minkowski comparison as hard gates.
- Keep global-uniform equality as a structural control.
- Require ≥25% tightening in every rowwise cell; diagnostic seed-0 evidence is 78.4–81.4%.
- Report absolute width/RMS descriptively and explicitly reject any absolute-width claim.

The v5 baseline result remains preserved as negative evidence for the old target.
