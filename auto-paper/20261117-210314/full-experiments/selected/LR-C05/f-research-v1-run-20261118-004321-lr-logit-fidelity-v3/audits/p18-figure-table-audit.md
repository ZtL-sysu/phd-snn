# P18 figure and table audit

## Scope

Audited manuscript: `writing/p17/paper-guidance-complete.md`.

## Artifact ledger

| Artifact | Source | Placement | Caption | Numeric/visual QA | Status |
|---|---|---|---|---|---|
| Figure 1 | `figures/specs/figure1-architecture-spec.json`, `figures/figure1-architecture.png` | Method, before experimental scope | Explains M0 input-message transport, magnitude-weighted Jacobian score, exact ledger and rate coding | SVG/PDF/PNG generated; visual inspection passed; score notation uses `r_i` and `dz/dr_i` | inserted |
| Figure 2 | `figures/source-data/figure2-main-logit-mse.csv` | Section 4.3, after main result | Three-seed mean±sample SD, lower is better, matched residual controls | PNG/SVG/PDF/TIFF inspected; error bars and labels legible | inserted |
| Figure 3 | `figures/source-data/figure3-budget-sensitivity.csv` | Section 4.4, after validation-grid result | 0.5/1/2% validation-grid sensitivity and confirmation caveat | Lines, labels and zero reference inspected | inserted |
| Figure 4 | `figures/source-data/figure4-tradeoff-and-runtime.csv` | Section 4.5, after task/runtime evidence | Fidelity/task maxima and rank128/1% paired p95 ratios; explains 3 pp reference | Two-panel layout inspected; corrected Cora task point is 0.53 pp | inserted |
| Table 1 | `results/p10-control-summary.csv`, `results/p10-task-loss-three-seed-audit.csv`, `results/confirmation-test-v2.json` | Section 4.3, before Figure 2 | Logit means±SD, message/hidden reductions versus top-absolute, task maxima, coefficient counts | Values recomputed from frozen rows; message-MSE trade-off is explicit | inserted |
| Table 2 | `results/p10-control-summary.csv` | Section 4.4, after adapted-control comparison | Proposed versus A2Q-style and One-Spike-style means±SD and reductions | Values match P10 derivation; adaptations are not called direct reproductions | inserted |
| Table 3 | `results/p10-bit-ledger.csv` | Section 4.5, before Figure 4 | Basis, residual, total, coefficient and full-float bit ledger | Formula and absolute totals match implementation | inserted |

## Coverage

| Results subsection | Covered by |
|---|---|
| 4.3 Main Logit-Fidelity Result | Figure 2, Table 1, main prose |
| 4.4 Sensitivity and Matched-Budget Controls | Figure 3, Table 2, control prose |
| 4.5 Task and Runtime Trade-offs | Figure 4, Table 3, timing/task prose |

## Judgment

- Every included figure and table has a scientific purpose, source evidence, caption, and nearby discussion.
- No artifact is decorative or included only to satisfy a count.
- The message-MSE negative trade-off is visible and not hidden by the logit-MSE headline.
- The 3 pp dashed line is explicitly a reference threshold, not an observed equivalence claim.
- Figure 1 is a user-authorized deterministic self-drawn fallback after GPT generation failure; the fallback is disclosed in the figure contract and gate report.

Decision: **PASS**.
