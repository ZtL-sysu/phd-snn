# Scenario decision log (round 001)

Independent `ccf-idea-reviewer standard` results, `review_execution: independent-agent`,
reports in `fly-connectome-cvpr2027/ideas/round-001/reviews/`. Scores rank only; there is no
hard threshold in this round.

| Rank | Idea | Overall | Verdict | Decision |
|---|---|---:|---|---|
| 1 | C1 real optical flow external validity | 6.1 | GO | **PRIMARY**: highest score, zero hard fatal gates, cleanest decisive controls, executable now |
| 2 | C3 connectome-derived homeostasis scale | 6.0 | REVISE | backup 1; Venue<=2 gate hit and success criterion only ties the manual constant |
| 3 | C4 structure-derived heterogeneous tau | 5.8 | REVISE | backup 2 |
| 4 | C2 readout follows spike front | 5.6 | REVISE | backup 3; PCA-confound risk |
| 5 | C5 cell-type layered routing readout | 5.6 | REVISE | backup 4; adjacent to the vetoed module-merging shape |

C1's three recorded fatal_risks are all fixable and were converted into go-conditions in the
guidance: undefined real-flow interface, remote clean-environment dependency risk (from task 17682),
and the guardrail-4 framing boundary. The independent Panel Synthesis recorded zero hard fatal gates
and explicitly recommended C1 as primary, with C3 as first backup. Failed and backup ideas are
retained in `candidate_pool`, not discarded.

Rejected earlier scenarios (S1 biological-wiring advantage, S2 robustness/lesion, S3 pure simulation,
S4 higher-order null as headline) remain rejected with their evidence in `mining/MINING-LOG.md`.
