# Final figure and table insertion audit

| Artifact | Final source | Placement | Final QA | Status |
|---|---|---|---|---|
| Figure 1 | `figures/data/figure1-certificate-chain.png` | Method after derivation | chain, formulas and radius policy legible | inserted |
| Figure 2 | `figures/data/figure2-width-tightening.png` | Results after tightening text | 36 cells, log width, 25% line and legend legible | inserted |
| Figure 3 | `figures/data/figure3-equality-tightening.png` | Results after Figure 2 | equality gap and rowwise tightening distribution legible | inserted |
| Table 1 | exact bound formulas | Method/comparator section | formulas and roles unambiguous | inserted |
| Table 2 | 36-row result summary | Results/failure audit | all rows and comparator statuses present | inserted |

The final TeX references all three PNG files at the packaged paths. Captions avoid statistical coverage, absolute-width and SOTA claims. Figure 3 uses `figures/source-data/figure3-rowwise-tightening.csv`; Table 2 is generated from `results/cert-methods.json`.
