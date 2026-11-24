# P9 merged concern-to-action ledger

Sources: AutoResearchClaw Reviewer A, Reviewer B, independent CCFA full manuscript review, and independent CCFA full integrity audit.

| ID | Severity | Consolidated concern | Evidence status | P10 action | Owner/location | Gate |
|---|---|---|---|---|---|---|
| C1 | major | Rank-128 scope is ambiguous for hidden width 16 | Existing code proves only `M0=A_hat X` is transported; `A_hat H1` is not compressed | REWRITE Method/title/scope to input-message transport and give tensor shapes | Method, Abstract, Figure 1 | existing-evidence repair |
| C2 | major | Exact-cost ledger and 2% denominator are underdefined | Existing code gives formulas and absolute totals | REWRITE cost model: 2% residual entries, 64 bits/selected pair, basis formula, padding and absolute totals | Method, Table 3 | existing-evidence repair |
| C3 | major | Selector controls are omitted/undefined | Raw data contains `top_abs`, `random`, `uniform`, A2Q-style, One-Spike-style | REWRITE controls and add complete control/per-seed tables | Method, Section 4.2/4.4 | existing-evidence repair |
| C4 | major | Validation selection history is incomplete | Grid is recoverable: ranks 16/32/64/128 and budgets 0.5/1/2%; focal rank128/2% was fixed before test after validation exposure | REWRITE chronology and label all grid results validation-exposed; avoid independence language | Section 4.1/4.4, Discussion | existing-evidence repair with disclosure |
| C5 | major | Strongest-control and task-loss denominator are ambiguous | Raw rows permit recomputation; current summary mixes labels | NARROW to “maximum observed degradation”; define comparator/metric/aggregation in table | Section 4.5 | existing-evidence repair |
| C6 | major | Jacobian/conversion implementation is underspecified | Code gives analytic frozen-ANN path, ReLU mask, rate scaling, and global full-graph selection | REWRITE implementation details and state transductive feature access | Method | existing-evidence repair |
| C7 | major | Practical significance is limited to logit fidelity | No task superiority or energy evidence | NARROW title/contribution to logit-fidelity coding; retain negative task result | Whole paper | claim narrowing |
| C8 | major | Timing boundary/p95 convention is unclear; focal 2% timing absent | Seven repeats and full `make_variant` timing exist only at 1% | Define timing boundary and p95 convention; keep 1% as secondary, do not generalize to 2% | Section 4.5 | existing-evidence repair; focal 2% timing remains outside current claim |
| C9 | moderate | Absolute MSE/per-seed displays are missing | Raw JSON/CSV support them | MOVE to compact tables/source data; report mean±sample SD and paired per-seed deltas | Section 4.3/4.4 | existing-evidence repair |
| C10 | moderate | “Bounded task loss” overstates maximum observations | Supported only descriptively | REWRITE as “maximum observed degradation” | Abstract, Results, Discussion, Conclusion | wording repair |
| C11 | moderate | Figure chronology/condition labels are ambiguous | Figure source data supports precise captions | REWRITE captions and Figure 1 notation; explain 3 pp reference line | Figures 1/3/4 | existing-evidence repair |
| C12 | major | Novelty/citation positioning is incomplete | Scheduled P12 gate remains open | BLOCK broad novelty; complete 36-reference audit at P12 | Related Work | late gate |
| C13 | minor | Terminology/statistical notation is inconsistent | Code/CSV give definitions | REWRITE terminology, hidden-MSE formula, `ddof=1`, and `Top-|m|` mapping | Method/Results | wording repair |
| C14 | minor | Artifact/environment provenance is incomplete | Local code, environment and data loaders exist | MOVE to external reproducibility artifact; add concise scientific implementation boundary | Method/limitations | external artifact |
| C15 | blocker outside claim | Independent replication, formal equivalence, energy/downstream benefit, interaction/leave-one-out ablation, focal 2% timing | Not in supplied evidence | BLOCK_EVIDENCE and exclude from current claims; list as future work/limitations only | Discussion | no fabrication |

## Reviewer score positions

- Reviewer A: 4/10, confidence 4/5; fatal concern is selector isolation, partly repaired by existing raw controls.
- Reviewer B: 6/10, confidence 4/5; no fatal numeric contradiction, but major reproducibility revision required.
- Independent CCFA full review: 5/10, confidence 4/5; weak reject / borderline negative in frozen state.
- Independent integrity audit: F1-F7/F9 supported, F8 provenance partially supported; no unsupported numerical claim.

## P10 acceptance condition

P10 may pass only after C1-C11 and C13-C14 are repaired from existing evidence, C12 remains explicitly deferred to P12, and C15 is excluded from the accepted contribution rather than silently promised.
