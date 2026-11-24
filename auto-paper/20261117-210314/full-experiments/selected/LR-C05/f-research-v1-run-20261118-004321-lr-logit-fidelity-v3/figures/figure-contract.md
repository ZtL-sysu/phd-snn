# P8 figure contract

## Data figures

- Core conclusion: output-Jacobian-selected sparse residual coefficients reduce logit MSE at matched serialized cost across three graphs, with bounded observed task loss and modest measured runtime overhead.
- Figure archetype: quantitative grid.
- Target/output: Q2+ journal-style vector figures with editable SVG text.
- Backend: Python/matplotlib.
- Final size: 183 mm wide double-column data figures.
- Panel map:
  - Figure 2: three-seed mean logit MSE for the proposed selector and matched-budget controls.
  - Figure 3: logit-MSE reduction over the evaluated 0.5%-2% residual-budget grid.
  - Figure 4a: fidelity gain versus worst three-seed-mean task loss.
  - Figure 4b: paired p95 runtime ratios for nine dataset-seed pairs.
- Evidence hierarchy: official-test main comparison is primary; validation-grid sensitivity is supporting; A2Q-style/One-Spike-style adaptations and runtime are controls/robustness.
- Statistics: `n=3` checkpoint seeds; bars show mean and sample SD; no formal confidence interval or significance test is claimed.
- Source data: clean CSV files derived from the frozen JSON evidence.
- Image-integrity notes: no image adjustment or crop applies to quantitative plots.
- Reviewer risk: task loss is a maximum descriptive trade-off, not equivalence; runtime is measured at rank128/1%, not the focal 2% setting.

## Figure 1 architecture

- Core conclusion: a rank-128 SVD path plus output-Jacobian-selected sparse residual coefficients is serialized under an exact padded-bit ledger before rate-coded frozen conversion.
- Figure archetype: schematic-led framework diagram.
- Backend: deterministic local FigureSpec-style SVG drawing under the user's explicit fallback authorization after direct GPT image generation became unavailable; not Nature plotting tools.
- Final size: wide landscape approximately 16:9.
- Visible modules: frozen graph/GCN input, SVD rank-128 transport, output-Jacobian sensitivity, sparse exact residual selection, exact padded serialized-bit ledger, rate-coded T=2/4 conversion, and evaluation outputs.
- Image-integrity notes: generated diagram only; no source photograph or quantitative pixel claim.
- Status: three built-in GPT generation attempts returned transient `502/ECONNRESET`; the user then explicitly authorized self-drawing as the temporary replacement. A reproducible structured SVG was generated and visually checked.
