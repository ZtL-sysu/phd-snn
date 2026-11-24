# Experiment traceability

| Batch | Matrix | Planned rows | Status | Raw output |
|---|---|---:|---|---|
| P3 baseline | 3 graphs × seed 0 × 2 levels × 2 quantizers | 12 | done | `results/cert-baseline.json`, `results/cert-baseline.csv` |
| P4 methods | 3 graphs × seeds 0/1/2 × 2 levels × 2 quantizers | 36 | done | `results/cert-methods.json`, `results/cert-methods.csv`, `results/cert-summary.json` |

The P4 batch was fixed before execution and did not use actual errors to alter radii or bounds. All 36 rows retain dataset, seed, level, quantizer, radius hash, containment, comparator, width, tightening and failure diagnostics.

## Provenance

- `provenance-manifest.json` hashes 9 frozen model snapshots, 10 dataset snapshot files, run code and raw outputs.
- `figures/source-data/figure3-rowwise-tightening.csv` is a direct 36-row export used for the planned tightening/width distribution figure.
- The standard rowwise width/RMS median is 30.679169413662216; the pre-repair upper-middle statistic is preserved as negative bookkeeping evidence.
