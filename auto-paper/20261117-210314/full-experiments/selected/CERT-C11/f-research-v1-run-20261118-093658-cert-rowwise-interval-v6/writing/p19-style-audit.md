# P19 Selective Academic Style Audit

review_execution: independent-agent

## Verdict

**REVISE**

The manuscript source is generally restrained, precise, and scientifically scoped. It does not need broad humanization. The final export requires a small presentation correction for duplicated/generic captions; two defensive prose phrases in the source and export also justify direct edits.

## Files Reviewed

- `writing/p12-citation-updated-manuscript.md`
- `writing/p13-final-v4/stage-22/paper.tex`

No source or export file was edited.

## Findings

| # | Location | Defect | Recommended action | Recommendation |
|---:|---|---|---|---|
| 1 | Export `paper.tex:140-146`, `185-199`, `156-171`, `211-260` | Figures and tables have short automatic captions followed by separate bold paragraphs repeating the same artifact title/description. This creates redundant prose and split caption semantics. | Use one complete caption inside each figure/table environment and remove the duplicated manual paragraph. | **edit** |
| 2 | Export `paper.tex:215` | Table 2 caption `Comparison of Graph across Seed, Levels, Quantizer, Contained` is generic, auto-generated, and omits the certificate result, comparator ordering, equality control, and tightening content. | Replace with the existing meaningful description from source line 159, integrated into the table caption. | **edit** |
| 3 | Export `paper.tex:143`, `188`, `196` | Figure captions are shortened to generic artifact titles; the substantive description sits outside the float. Figure 2’s caution about descriptive width should not be separated from its caption. | Merge the source captions into the float captions, retaining the no-absolute-width and traceability qualifications. | **edit** |
| 4 | Source line 139; export `paper.tex:181` | `This result is important because...` is promotional meta-commentary; the useful content is the equality-control logic. | Edit to a direct statement such as: “This equality confirms that the rowwise gain does not arise from comparing different formulas under constant radius.” | **edit** |
| 5 | Source line 206; export `paper.tex:269` | `The high absolute width/RMS is not hidden.` is defensive meta-commentary. | Edit to: “The high absolute width/RMS is retained as negative evidence.” Preserve the explanatory mechanism and large-width numbers. | **edit** |

## Content To Retain

- **Abstract and conclusion scope wording** — source lines 5 and 212-214; export lines 21 and 276-278. The deterministic-final-logit and matched-global-radius boundaries are precise, not promotional padding.
- **First/Second/Third distinction** — source line 202; export line 265. This is not decorative rule-of-three writing: it separates deterministic containment, analytic ordering, and empirical tightening.
- **Negative width evidence** — source lines 151-157 and 206-208; export lines 201-209 and 269-271. Keep the standard median 30.68, maximum 36.91, high-width limitation, and zero-failure diagnostics.
- **Terminology** — retain “rowwise uniform quantizer,” “independent-coordinate interval,” “Minkowski upper comparator,” “global-radius ablation,” “deterministic theorem/implementation containment,” and “standard median.”
- **Section roadmap** — source line 25; export line 45. It is conventional but concise and maps to the actual six sections.
- **Em-dash usage** — no overuse was found. No edit is needed.
- **Synonym cycling** — the terms `matched global-radius ablation` and `matched radius-granularity ablation` are close variants, but their repetition preserves claim consistency. No stylistic substitution is recommended.

## Final Recommendation

Apply only the five targeted edits above. Do not rewrite the abstract, discussion taxonomy, mathematical definitions, scope exclusions, or negative-result paragraphs for stylistic variety. The source prose can then proceed; the export must be regenerated without duplicate captions.
