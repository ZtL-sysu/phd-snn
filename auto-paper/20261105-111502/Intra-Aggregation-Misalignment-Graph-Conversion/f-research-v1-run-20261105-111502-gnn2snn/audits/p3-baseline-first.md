# P3 / P3A — baseline-first execution and stop-loss review

Generated from `registry/results.csv` (2975 rows) and `results/*.json`.

The simple baseline (IF without bias correction), the strongest feasible external anchors
(published protocol-labelled rows), and matched internal controls (count decoder, TPP transplant,
uniform-T) were all measured **before** any proposed-method claim was written. G0 reproduced the
reference values within 0.1 pp on CPU; that gate is recorded in `notes/S0_foundation.md`.

| check | value |
|---|---|
| total result rows | 2975 |
| rows by stage | {'S0/G0': 14, 'S1': 1596, 'S3': 1155, 'S5': 210} |
| rows by dataset | {'cora': 959, 'pubmed': 959, 'citeseer': 952, 'chameleon': 35, 'squirrel': 35, 'ogbn-arxiv': 35} |
| rows by device | {'cpu': 2940, 'cuda': 35} |
| rows without a content-addressed trace id | 0 |
| S1 observed branch | A |
| ours vs TPP at T=4 (pp) | 4.238 |
| inter-layer permutation delta (pp) | 0.542 |
| intra-aggregation phase delta (pp) | -11.877 |

Numeric audit: all rows carry `run_id`, seed, `t_steps`, `ann_ref`, `acc`, `gap_pp`,
`spikes_per_node`, `sop_est`, `git_commit` and `device`. Metric direction is accuracy (higher) and
gap (lower). Splits are the frozen Planetoid public splits. No seed was dropped and no negative
cell was deleted.

`ccf-integrity-auditor` (`numeric-audit`) evidence: the table above plus `results/wp0_repro.json`.
`ccf-idea-reviewer` (standard) post-baseline reassessment: the mechanism delta remains above the
0.8 pp decision threshold, so the differentiating path is intact. A branch C/D outcome would have
reopened S1; the observed branch is **A**.

**Gate verdict: PASS** (baseline metrics and reproducibility artifacts exist before proposed-method
iteration; no unresolved baseline gap).
