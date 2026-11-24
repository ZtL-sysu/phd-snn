# P10 revision log

| Review ID | Action | Manuscript repair | Evidence used | Status |
|---|---|---|---|---|
| C1 | NARROW/REWRITE | Restrict transport to `M0=A_hat X`; give N/F shapes and valid rank-128 scope | `p10-implementation-spec.json` | done |
| C2 | REWRITE | Define 2% residual entries, 64-bit pairs, basis formula, padding and absolute totals | `p10-bit-ledger.csv` | done |
| C3 | REWRITE | Define top-absolute/random/uniform/A2Q-style/One-Spike-style controls and reference rows | `p10-control-summary.csv`, `p10-per-seed-control-comparison.csv` | done |
| C4 | REWRITE | Document rank/budget validation grid and pre-test fixation chronology | `p10-validation-grid.csv` | done |
| C5 | REWRITE | Define per-metric comparator and use maximum observed degradation | `p10-task-loss-three-seed-audit.csv`, `p10-task-loss-audit.csv` | done |
| C6 | REWRITE | Define composite score, analytic frozen-ANN Jacobian, global transductive selection | `p10-implementation-spec.json` | done |
| C7 | NARROW | Restrict contribution to input-message logit-fidelity coding | P10 packet and revision | done |
| C8 | REWRITE | Define timing scope/p95 and retain rank128/1% as secondary | `p10-timing-summary.csv` | done |
| C9 | REWRITE | Add absolute/per-seed/control evidence and SD convention | P10 evidence tables and revised Results | done |
| C10 | REWRITE | Replace bounded task language with observed maxima | revised Abstract/Results/Discussion/Conclusion | done |
| C11 | REWRITE | Correct Figure 1 notation and Figure 4 reference/condition caption | revised figures and captions | done |
| C12 | BLOCK_EVIDENCE | Do not close novelty; retain P12 36-reference audit gate | merged P9 ledger | deferred to P12 |
| C13 | REWRITE | Standardize score, ratio-of-means, task-maximum and timing terminology | revised manuscript | done |
| C14 | MOVE | Keep artifact/environment provenance outside the scientific narrative; final package will carry it | P10 implementation spec/manifests | done |
| C15 | BLOCK_EVIDENCE | Exclude independent replication, equivalence, energy, downstream utility, interaction ablation and focal 2% timing from claims | no such evidence exists | done by claim exclusion |

## Author protections preserved

- No new experimental result was added.
- No citation key was removed or invented.
- No energy, task-superiority, temporal-event, broad-GNN, equivalence or independent-replication claim was introduced.
- All main numerical results retain their unit, aggregation, comparator and measurement scope.
