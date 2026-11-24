# P17 · Guidance Coverage Audit (v3)

| guidance-v3 requirement | Covered in manuscript |
|---|---|
| 1 Introduction — gap, combination framing, four contributions, boundaries | `tex/sections/1_intro.tex` |
| 2 Related Work — inheritance vs differentiation | `tex/sections/2_related.tex` |
| 3 Method — exact identity, redundant beta*, membrane readout, margin regularisation, two energy conventions, applicability | `tex/sections/3_method.tex` |
| 4 Experiments — datasets, baselines, four disjoint holdouts, table, ablations, identity, Pareto frontier, statistics | `tex/sections/4_experiments.tex` + `tex/tables/*.tex` + `figures/*.pdf` |
| 5 Discussion — mechanism, trade-off, negative result, threats | `tex/sections/5_discussion.tex` |
| 6 Conclusion | `tex/sections/6_conclusion.tex` |
| Measured conversion loss + explicit Pareto frontier (user-authorized statement) | Intro bullet 4, §4.7, §5, §6 |
| Horizontal comparison, 5x energy, identity targets unchanged | §4.3--§4.6 |
| No 1.5pp attainment claim, E18 negative result reported | §4.3, §4.7, §5 |
| 45 nm estimate, not hardware measurement | Abstract, §3.5, §5 |

All numeric values are LaTeX macros defined in `tex/numbers.tex` by `protocols/gen_paper_artifacts.py` from `results/*.json`. No number is hand-copied into prose or tables.
