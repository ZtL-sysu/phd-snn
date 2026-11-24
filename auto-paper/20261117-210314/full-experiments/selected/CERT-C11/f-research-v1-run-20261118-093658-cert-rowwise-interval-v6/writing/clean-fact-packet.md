# Clean fact packet

- Scope: frozen two-layer GCN final-logit chain on Cora, Chameleon and Squirrel; seeds 0/1/2; levels 4/8; global/rowwise uniform quantizers.
- Formula: `B_abs=|A||A|Delta|W1|`.
- Minkowski comparator: `( |A||A| rownorm(Delta,2) ) ||W1[:,k]||_2`.
- Matched global-radius ablation: `rowsum(|A||A|) max(Delta) ||W1[:,k]||_1`.
- Main result: 36/36 deterministic containment and 36/36 analytic comparator ordering.
- Structural control: 18/18 global-uniform equality cells.
- Empirical utility: 18/18 rowwise cells, tightening 74.26%–82.12%, standard median 79.65%.
- Descriptive width/RMS: standard median 30.68, maximum 36.91; no absolute-width claim.
- Diagnostics: zero clipping, zero non-finite rows, zero omissions, radius hashes preserved.
- Safe interpretation: deterministic final-logit certificate plus matched global-radius ablation.
- Forbidden interpretation: statistical coverage, SOTA compression superiority, robustness, temporal SNN, energy, hardware, learned-quantizer or multilayer generality.
