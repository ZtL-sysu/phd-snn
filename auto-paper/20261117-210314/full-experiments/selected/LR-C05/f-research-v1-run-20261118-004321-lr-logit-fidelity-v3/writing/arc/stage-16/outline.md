# Paper Outline: SPAR for Frozen GNN-to-SNN Conversion

## Proposed Method Name
**SPAR** — Sparse Projected Aligned Residuals  
- 4 characters, pronounced “spar”
- Evokes sparsity and residual alignment
- Directly tied to the paper’s core mechanism: operator-aligned low-rank sparse residual coefficient selection

---

## Candidate Titles

All titles follow the `MethodName: Subtitle` format and are ≤ 14 words.

| # | Title | Word Count | Memorability (1–5) | Specificity (1–5) | Novelty Signal (1–5) |
|---|---|---|---|---|---|
| 1 | **SPAR: Sparse Projected Operator-Aligned Low-Rank Residual Coefficients for Frozen GNN-to-SNN Conversion** | 11 | 4 | 5 | 4 |
| 2 | **SPAR: Sparse Low-Rank Residual Coefficients for Frozen GNN-to-SNN Conversion** | 9 | 4 | 3 | 3 |
| 3 | **SPAR: Operator-Aligned Sparse Low-Rank Residual Coefficients for Frozen GNN-to-SNN Conversion** | 10 | 3 | 5 | 4 |

**Preferred title:** Title 1 — it names all three components (sparse, operator-aligned, low-rank) while keeping the method name short and the subtitle under 14 words.

---

## Global Evidence Anchors

The outline below links each section to the accepted result analysis and decision.

- **[Evidence: Result Analysis]**
  - Rank = 128
  - Sparse residual coefficient budget = 2%
  - Output-Jacobian-selected coefficients
  - Three-seed mean split-specific logit MSE ratio reductions:
    - Cora: **26.23%**
    - Chameleon: **33.99%**
    - Squirrel: **25.83%**
  - Maximum three-seed-mean task degradation: **1.86 percentage points**
  - Maximum seed-level task degradation: **2.85 percentage points**
  - Paired p95 runtime ratios: **1.020–1.124×**
  - Peak allocation: **218.23 MB**
  - Focal setting was fixed after validation exposure; test run is