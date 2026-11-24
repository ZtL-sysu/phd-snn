# S1 · Manuscript Module Map

Original (immutable): `sources/original-submitted.pdf`, `sources/main.tex`, `sources/sections/*.tex`, `sources/tables/*.tex`, `sources/references.bib`.

| Module | Location | Role |
|---|---|---|
| Title | `main.tex` | operator-class transfer + accuracy--energy frontier |
| Abstract | `main.tex` | gap, identity, redundancy finding, 20-seed energy result, honest boundary |
| 1 Introduction | `sections/1_intro.tex` | gap, combination framing, four contributions, scope |
| 2 Related Work | `sections/2_related.tex` | inheritance vs differentiation across conversion / spiking-GNN / graph-vision / energy |
| 3 Method | `sections/3_method.tex` | setup, identity, two-phase redundancy, readout/margin/width, energy, applicability |
| 4 Experiments | `sections/4_experiments.tex` | protocol, baselines, main table, baseline table, ablations, identity, frontier |
| 5 Discussion | `sections/5_discussion.tex` | mechanism, stability, trade-off, limitations |
| 6 Conclusion | `sections/6_conclusion.tex` | transferability and operator-dependent discretisation |
| Figures | `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf` | frontier, latency curve, framework |
| Tables | `tables/tab_main.tex` etc. | main, baselines, ablations, identity |
| References | `references.bib` | 42 entries, 23 in 2022--2026 |
| Declarations | none in manuscript | author-managed, routed externally |

Central question: can a conversion framework assembled for graph node classification transfer to graph-structured visual classification and yield an ANN-relative energy advantage? Core claim: linear readout preserves the exact identity, a component of the combination becomes redundant, and the adapted combination yields a stable energy advantage with a measurable fidelity cost. Supporting findings: baseline margins, fp64 identity, ablations, negative scaling result. Orphans found in S6: internal-target references and screening narration (removed in S7).
