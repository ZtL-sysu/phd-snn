# Figure and table insertion audit

| Artifact | Source experiment/generation step | Manuscript label | First citation location | Caption quality | Discussed near citation? | Results subsection covered | Status |
|---|---|---|---|---|---|---|---|
| Framework diagram | Deterministic local FigureSpec-style SVG under explicit user fallback authorization | Figure 1 | Method mechanism overview | Complete | Yes in P8 draft | Method | inserted-in-p8-draft |
| Main logit-MSE bars | `confirmation-test-v2.json` | Figure 2 | Section 4.3 main result | Complete | Yes in P8 draft | Main fidelity | inserted-in-p8-draft |
| Budget sensitivity lines | `v2-summary.json` | Figure 3 | Section 4.4 sensitivity | Complete | Yes in P8 draft | Sensitivity | inserted-in-p8-draft |
| Task/runtime panels | `confirmation-summary.json`, `v2-timing.json` | Figure 4 | Section 4.5 trade-offs | Complete | Yes in P8 draft | Task and runtime | inserted-in-p8-draft |
| Main fidelity/task table | Official-test summary | Table 1 | Section 4.3 | Planned | Planned | Main fidelity | planned-for-tex |
| Adapted-control table | Official-test rows | Table 2 | Section 4.4 | Planned | Planned | Matched-budget controls | planned-for-tex |
| Cost/runtime table | Exact ledger and timing rows | Table 3 | Sections 4.2 and 4.5 | Planned | Planned | Exact and warmed cost | planned-for-tex |

## Results subsection coverage

| Experiments and Results subsection | Scientific purpose | Required artifact | Artifact label | Nearby citation? | Status |
|---|---|---|---|---|---|
| 4.3 Main Logit-Fidelity Result | Principal exact-cost comparison | Main result bars and table | Figure 2; Table 1 | Yes | covered |
| 4.4 Sensitivity and Matched-Budget Controls | Budget sensitivity and adapted controls | Budget lines and adapted-control table | Figure 3; Table 2 | Yes | covered |
| 4.5 Task and Runtime Trade-offs | Bounded task loss and warmed cost | Two-panel trade-off and cost table | Figure 4; Table 3 | Yes | covered |

## Image QA

- Figures 2-4 were rendered by Python/matplotlib from clean source-data CSV files.
- SVG, PDF, PNG, and TIFF outputs exist for every data figure.
- Figures 2-4 passed visual inspection after two layout repairs; labels do not overlap and the plots are legible.
- Figure 1 passed structural and visual QA after the user explicitly authorized self-drawing. Three prior GPT attempts failed with transient 502 errors; the deterministic SVG/PDF/PNG replacement preserves the verified method labels and scope boundaries.
