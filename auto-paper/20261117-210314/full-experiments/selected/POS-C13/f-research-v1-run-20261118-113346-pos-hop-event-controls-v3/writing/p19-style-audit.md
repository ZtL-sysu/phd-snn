# P19 Selective Academic Style Audit

review_execution: independent-agent

## Verdict

**REVISE**

The manuscript is technically restrained and does not need broad humanization. Two wording edits and one TeX readability fix are justified. Formulas, numerical claims, terminology, leakage evidence and scope boundaries should remain unchanged.

## Findings

| # | Exact location | Defect | Recommended action | Recommendation |
|---:|---|---|---|---|
| 1 | `writing/p10-revised-manuscript.md:5`; `writing/p13-final-v1/stage-22/paper.tex:21` | “Across five split/probe seeds, hybrid reconstruction error is 3.952% and 4.879%” factually drifts from the evidence: representation error is a two-graph representation audit, while the five seeds apply to task/probe evaluation. | Change to “In the representation audit, hybrid reconstruction error is…” and keep the five-seed clause attached to task results. | **edit** |
| 2 | `writing/p10-revised-manuscript.md:149`; `writing/p13-final-v1/stage-22/paper.tex:205` | “show clear ordered-versus-shuffled gaps” is mildly promotional; the measured gaps are already explicit. | Prefer “show ordered-minus-shuffled gaps” or state the two numeric gaps directly. | **edit** |
| 3 | `writing/p13-final-v1/stage-22/paper.tex:66` | Inline tensor dimensions are placed inside `\texttt` with escaped math symbols (`X$\in$R\textasciicircum{}...`), which is difficult to read in the export. | Use normal inline math for `X`, `A`, dimensions and set notation. | **edit** |

## Content To Retain

- **Captions:** Figure 1–3 and Table 1–2 are complete and not duplicated in the final TeX; retain their substantive descriptions.
- **Discussion structure:** the First/Second/Third statements at source line 139 / TeX line 194 separate fidelity, permutation and order-mismatch evidence; this is not rule-of-three padding.
- **Negative evidence:** retain source line 135 / TeX line 189, including the leaky probe description and its exclusion.
- **Scope language:** retain source lines 37, 141–145 / TeX lines 58, 196–200, especially the non-causal fixed-probe statement and exclusions for temporal spikes, energy, hardware and broad conversion.
- **Terminology:** keep “hybrid Lloyd/escape encoding,” “codec-consistent,” “ordered-codebook mismatch,” “fixed raw probe,” and “sample SD.”
- **Numerical presentation:** retain the paired means, SDs, min/max values and bit ledger unchanged.

## Final Recommendation

Apply only the three targeted edits above. Do not rewrite the formulas, negative leakage paragraph, scope limitations or substantive evidence taxonomy.
