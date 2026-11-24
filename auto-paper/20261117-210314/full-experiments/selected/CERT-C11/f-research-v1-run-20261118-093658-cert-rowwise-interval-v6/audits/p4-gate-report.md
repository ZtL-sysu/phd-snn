# P4 experiment gate

## Decision

**PASS.** The complete corrected matrix is frozen and meets every binding v6 gate.

## Results

- 36/36 deterministic containment.
- 36/36 `B_abs <= B_mink + tol`.
- 18/18 global-uniform cells satisfy the expected equality control.
- 18/18 rowwise cells tighten by 74.26%–82.12% versus `B_global_col`, median 79.65%.
- Zero clipping events, non-finite rows or omitted failures.
- Proposed width/RMS is descriptive: standard median 30.68 and maximum 36.91 for rowwise; no absolute-width claim is made.

Raw outputs are `results/cert-methods.json`, `results/cert-methods.csv` and `results/cert-summary.json`.
