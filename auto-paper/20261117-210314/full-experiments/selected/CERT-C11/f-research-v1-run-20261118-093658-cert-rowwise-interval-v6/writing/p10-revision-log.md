# P10 revision log

| Concern | Action | Evidence |
|---|---|---|
| C1 missing bibliography | Added a 50-entry BibTeX file and References section; all 34 cited keys resolve | `writing/references.bib`, `writing/p10-revised-manuscript.md` |
| C2 rate-coded SNN overclaim | Removed rate-coded implementation wording; scope now says frozen finite-precision conversion/final logits | abstract and introduction |
| C3 novelty ambiguity | Explicitly state interval propagation is standard and the delta is rowwise radii through two graph operators plus matched ablation | Related Work |
| C4 Table 1 shorthand | Replaced with exact summation/norm formulas | Table 1 |
| C5 Table 2 auditability | Added containment, `B_abs<=B_mink`, and global-equality columns | `writing/table2-36-cells.md` |
| C6 signed zero | Global tightening is formatted as `0.00` within tolerance | Table 2 |
| C7 hidden-16 provenance | Added `results/model-shapes.json`; all 9 snapshots have H=16 | Method and architecture provenance |

No experiment rows, radii, bounds or strong results changed.
