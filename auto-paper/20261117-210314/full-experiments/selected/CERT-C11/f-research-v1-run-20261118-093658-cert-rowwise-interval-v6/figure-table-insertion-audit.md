# Figure and table insertion audit

| Artifact | Source | Placement | QA | Status |
|---|---|---|---|---|
| Figure 1 | `research/make_figures.py`; deterministic local drawing | Method after bound derivation | Formula chain legible; radius-before-error disclosure visible | inserted |
| Figure 2 | `results/cert-methods.json` | Results after main containment/tightening text | 36 points visible; log width and 25% gate labeled | inserted |
| Figure 3 | `figures/source-data/figure3-rowwise-tightening.csv` | Results after Figure 2 | Equality gap and rowwise distribution traceable | inserted |
| Table 1 | `contract-extraction.yaml` | Method before experiments | Bound roles distinguish analytic ordering from empirical effect | inserted |
| Table 2 | `results/cert-methods.json`; `writing/table2-36-cells.md` | Results after failure audit | all 36 rows included; no omitted failures | inserted |

All captions state the condition and avoid statistical-coverage or absolute-width claims.
