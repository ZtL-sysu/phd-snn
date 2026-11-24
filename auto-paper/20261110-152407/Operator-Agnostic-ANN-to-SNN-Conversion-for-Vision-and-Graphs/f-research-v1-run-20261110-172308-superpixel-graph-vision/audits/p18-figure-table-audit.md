# P18 · Figure/Table Audit

| Artifact | Source | Purpose | First discussed |
|---|---|---|---|
| `figures/pareto.pdf` | `results/e10/val_sweep.json` | accuracy--energy frontier | §4.7, Fig.~\ref{fig:pareto} |
| `figures/loss_T.pdf` | `results/local_full_v2/result.json` (5 seeds) | loss vs latency with error bars | §4.7, Fig.~\ref{fig:lossT} |
| `figures/framework.pdf` | method schematic | overall framework (programmatic fallback; see note) | §3, available for Fig.~1 |
| `tex/tables/tab_main.tex` | `results/e17/confirmation.json` | main 5-seed result | §4.3, Tab.~\ref{tab:main} |
| `tex/tables/tab_baselines.tex` | `results/local_full_v2/result.json` | baseline comparison | §4.4, Tab.~\ref{tab:baselines} |
| `tex/tables/tab_ablations.tex` | `results/local_full*/result.json` | component ablations | §4.5, Tab.~\ref{tab:ablations} |
| `tex/tables/tab_identity.tex` | `results/e17,e18/confirmation.json` | float64 identity residual | §4.6, Tab.~\ref{tab:identity} |

Note: the framework figure is a programmatic schematic rather than a generative image; every label is a verified component from §3. Figures are generated from result files, captions match the evidence, and no figure hides a negative result or presents op-count energy as hardware measurement.

Figure files: framework.pdf, loss_T.pdf, pareto.pdf. Table files: tab_ablations.tex, tab_baselines.tex, tab_identity.tex, tab_main.tex.
