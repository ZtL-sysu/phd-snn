# P8 gate report

## Decision

**PASS under explicit user-authorized Figure 1 fallback.**

## Completed checks

| Check | Result |
|---|---|
| Data Figures 2-4 generated from frozen JSON | pass |
| Source CSVs and hash manifest | pass |
| SVG/PDF/PNG/TIFF data exports | pass |
| Figure 1 deterministic SVG/PDF/PNG source and export | pass |
| Figure 1 structural validation | pass |
| Figure 1 visual QA | pass |
| Figure captions and evidence alignment | pass |
| Figures 2-4 inserted near explanatory text | pass |
| Figure 1 inserted in Method | pass |
| Three evidence tables selected for TeX | pass |
| Figure/table insertion audit finalized | pass |

## Fallback disclosure

The built-in GPT image generator failed three times with `502/ECONNRESET`. The user explicitly authorized self-drawing as the temporary Figure 1 route while keeping other standards unchanged. The replacement is a deterministic, editable SVG generated from `figures/specs/figure1-architecture-spec.json`; it is not an AI-generated illustration and no Nature plotting tool was used for the architecture figure.

The figure shows only verified scientific components: frozen graph/GCN input, rank-128 SVD transport, residual construction, output-Jacobian sensitivity, top-B exact residual selection, exact padded serialized-bit accounting, rate-coded T=2/4 conversion, and the reported evaluation metrics. The dashed scope box records validation-grid sensitivity and held-out confirmation after validation exposure.
