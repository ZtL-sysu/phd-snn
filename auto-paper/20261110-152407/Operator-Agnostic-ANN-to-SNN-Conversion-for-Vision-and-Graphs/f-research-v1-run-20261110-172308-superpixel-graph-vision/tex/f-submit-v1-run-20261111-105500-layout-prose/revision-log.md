# S7 · Revision Log

| Concern | Action | Passage / file | Facts changed | Post-edit check |
|---|---|---|---|---|
| Blue ruler numbers overlap text | `\AtBeginDocument{\nolinenumbers}`, keep review header | `main.tex` | none | visual round 1, all 7 pages |
| `pagebackref` digits in references | remove option | `main.tex` | none | visual round 1, pages 6--7 |
| Eq. (5) exceeds column | rewrap as two aligned rows | `3_method.tex` | none | visual round 1, page 3 |
| Subsection headings wrap | shorten two headings | `3_method.tex` | none | visual round 1, page 3 |
| Tables overflow / truncated exponents | resizebox wrapper, rebuild identity table from result JSON, remove wide multicolumn note | `tables/*.tex`, `4_experiments.tex` caption | none (values retained from generated source) | visual round 1, page 4 |
| Two figures in one column | second figure `[b]` | `main.tex` | none | visual round 1, page 5 |
| Abrupt supplementary paragraph | rewrite as natural closing sentence | `2_related.tex` | none | visual round 1, page 2 |
| Internal-target / defensive wording | narrow or remove | intro, experiments, discussion, conclusion | none | prose lint after S7 |
| Screening-workflow narration | remove | `5_discussion.tex` | none | prose lint after S7 |

Protected-scope check: no numeric macro altered; no citation key removed; no negative result deleted; no declaration inserted; 45 nm theoretical label retained. Profile/adapter status: `writing_adapter.py` used to record the manuscript-facing brief; the returned text is verified independently by `manuscript_lint.py` and visual inspection.


## Second prose pass (scientific-paper-writing)

| Concern | Action | File | Facts changed |
|---|---|---|---|
| Contribution bullets restated the results table | replace with contribution-led statements; numbers deferred to §4 | `sections/1_intro.tex` | none |
| Repeated defensive disclaimers ("no accuracy-SOTA claim", "not an accuracy claim") | replace with one neutral evaluation-scope statement | intro, discussion | none |
| Related Work repeated the no-novelty claim | replace with a neutral substrate sentence | `sections/2_related.tex` | none |
| Discussion repeated §4.7 numbers | replace with mechanism interpretation of the frontier | `sections/5_discussion.tex` | none |
| Conclusion spread over two paragraphs with repeated numbers | compact single-paragraph synthesis with future work derived from the operator boundary | `sections/6_conclusion.tex` | none |
| Bold run-in headings lost their period and ran into body text (layout regression) | restore periods with formal noun-phrase headings | `sections/5_discussion.tex` | none |

Post-edit verification: `latexmk` rc=0, 7 pages, full 7-page visual inspection, citation gate re-bound, `--complete` rc=0. Every numeric macro, citation, equation, figure/table reference, negative result and evidence boundary preserved.
