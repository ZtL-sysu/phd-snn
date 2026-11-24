# Figure 1 GPT image-generation prompt

Use case: scientific-educational.

Asset type: Figure 1 overall framework/architecture diagram for a machine-learning research paper.

Create a clean publication-ready left-to-right framework diagram for a method that improves logit fidelity in frozen GNN-to-SNN compression using output-Jacobian-selected sparse residual coefficients at an exact serialized-bit budget.

Style: editable-looking modern ML paper architecture diagram, wide landscape approximately 16:9, white background, thin black outlines, rounded rectangles, straight black arrows, restrained pastel fills, small technical icons, and crisp sans-serif labels. Do not use poster, infographic, photorealistic, marketing, 3D, shadow, or gradient styles.

Five columns:

1. `INPUT + FROZEN GCN`: graph `G=(V,E)`, node features `X`, normalized graph message `M=A_hat X`, frozen two-layer hidden-16 GCN.
2. `LOW-RANK TRANSPORT`: SVD rank-128 transport, `M approximately M_128`, residual `R=M-M_128`.
3. `OUTPUT-SENSITIVE RESIDUALS`: output-Jacobian sensitivity `s_i=||dz/dm_i||_2^2`; select top-B residual coefficients with explicit indices and values.
4. `EXACT-COST CONVERSION`: exact padded serialized-bit ledger, matched total padded serialized-bit budget, serialized basis and selected residual coefficients, rate-coded frozen conversion at `T=2` and `T=4`.
5. `EVALUATION`: converted logits `z_s`, split-specific logit MSE, hidden-state MSE, `T=2/4` accuracy, teacher agreement.

Show branch and merge flow from residual `R` into the rank-128 path and selected sparse residual path, then merge before serialization. Use pale gray inputs, pale blue SVD, pale purple Jacobian selection, pale orange serialization, pale teal conversion, and stronger orange outputs. Add one dashed red diagnostic box: `validation-grid sensitivity` and `held-out confirmation after validation exposure`. Add a bottom legend explaining the color families.

Visible-text constraints: use only the verified labels and symbols above. Do not include skill names, prompt titles, production instructions, stage labels, audit/pass labels, file paths, unsupported equations, energy claims, temporal-event claims, novelty claims, or state-of-the-art claims.

Generation status: three built-in GPT image-generation attempts returned `502 Bad Gateway` with `ECONNRESET`; no AI-generated image was created. The user explicitly authorized a self-drawn replacement while keeping the other standards unchanged. The accepted replacement is the deterministic `figure1-architecture.svg` generated from `specs/figure1-architecture-spec.json`.
