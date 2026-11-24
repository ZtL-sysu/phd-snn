# P7 reverse outline

## Part 1

Edit rationale: P7 is limited to the title, abstract, introduction, and related work. The central question is stated verbatim from the manuscript brief, all numerical results retain their reported units, aggregation, and scope, and the required qualifications are kept explicit. No References section is included; only supplied citation keys are used.

Reverse outline:
- Abstract paragraph 1: identifies the frozen GNN-to-SNN transport problem, states the bounded question, reports the main matched-budget logit-MSE result (F1), bounded task loss (F2), exact serialized-cost condition (F3), warmed runtime and memory scope (F4), and the validation/measurement limitations (F5).
- Introduction paragraph 1: defines the output-sensitive information-loss problem and states the unresolved question.
- Introduction paragraph 2: describes the bounded contribution: rank-128 SVD transport, a 2% output-Jacobian-selected sparse residual budget, the exact padded-bit ledger (F3), and the distinction between residual coefficients and temporal spikes.
- Introduction paragraph 3: previews diagnostic hidden-state and budget-grid evidence (F6, F7), prior-art adapted comparisons (F8), and the retained negative task-superiority finding (F9).
- Related Work paragraph 1: groups graph-conversion approaches by source model and temporal/compute assumptions, citing only supplied keys.
- Related Work paragraph 2: groups graph-message compression approaches by quantization, communication, and low-rank trade-offs, and identifies our matched-budget adaptations as ledger-bound comparisons.
- Related Work paragraph 3: groups output-sensitive coding by what is selected for downstream outputs, distinguishes exact residual coefficients from temporal SNN events, and ends with the exact gap question.

Fact coverage: F1-F9 are represented without upgrading observed results to causal, novelty, state-of-the-art, energy, temporal-event-equivalence, task-superiority, or broad-GNN-generality claims. F5 is placed in the abstract and constrained interpretation; F9 is retained explicitly as negative evidence.

## Part 2

Reverse outline:
- Method paragraph 1: defines the frozen two-layer hidden-16 GCN, graph-message computation, hidden width, and seeds.
- Method paragraph 2: defines rank-128 SVD transport and the message residual.
- Method paragraph 3: defines output-Jacobian squared sensitivity, sparse coefficient encoding, and the exact padded serialized-bit ledger, including F3.
- Method paragraph 4: defines rate-coded conversion and preserves the temporal-event, energy, and generality boundaries from F5.
- Experimental Scope paragraph 1: specifies datasets, reported splits, seeds, and the validation-exposed/held-out status from F5.
- Experimental Scope paragraph 2: defines logit MSE, hidden-state MSE, \(T=2/4\) accuracy, teacher agreement, and descriptive uncertainty handling.
- Compared Methods paragraph 1: introduces the compact compared-method table and the strongest evaluated matched-budget control.
- Compared Methods paragraph 2: reports the focal rank-128/2% logit-MSE reductions from F1 and the matched-budget adaptation comparisons from F8.
- Compared Methods paragraph 3: reports hidden-state sensitivity from F6 and the 0.5%-2% budget-grid result from F7.
- Compared Methods paragraph 4: reports bounded task degradation from F2, retains the negative task-superiority finding from F9, and reports the warmed runtime and memory scope from F4.

Rationale: The requested headings are used exactly. Equations define the frozen GCN, SVD residual, sensitivity score, sparse encoding, cost ledger, and rate-coded decoding. The table is limited to comparison roles and exact-cost assumptions. No claim of novelty, state of the art, energy efficiency, temporal-event equivalence, task superiority, or broad GNN generality is made. Exact split-file identifiers were not supplied, so the manuscript retains the reported split protocol rather than inventing indices.

## Part 3

Reverse outline:
- 4.3 paragraph 1: reports the principal rank-128/2% logit-MSE comparison, positive dataset-seed direction, exact serialized-cost condition from F3, uncertainty boundary, and held-out status from F1 and F5.
- 4.4 paragraph 1: reports hidden-state MSE reductions from F6 and identifies their validation-grid sensitivity scope.
- 4.4 paragraph 2: reports the nine-cell residual-budget result from F7 and distinguishes validation-grid sensitivity from later held-out confirmation.
- 4.4 paragraph 3: reports the matched-budget comparisons with our matched-budget adaptations of A2Q and One-Spike from F8, retaining descriptive uncertainty.
- 4.5 paragraph 1: reports the bounded task degradation from F2 and states that it is not an equivalence proof.
- 4.5 paragraph 2: preserves the mixed task deltas, failed task-superiority target, and bounded-claim interpretation from F9.
- 4.5 paragraph 3: reports the warmed runtime and peak-memory measurements from F4 with their wall-clock, non-energy boundary.
- Discussion paragraph 1: separates the observed fidelity-resource pattern from the untested output-Jacobian mechanism hypothesis.
- Discussion paragraph 2: states the static-GCN, validation-exposure, temporal-event, energy, and generality limits from F5.
- Conclusion paragraph 1: answers the Introduction with the three-graph logit-MSE result and bounded task loss from F1 and F2, without adding a new promise.

Rationale: The requested continuation headings are used exactly, and no additional top-level Results, Experiments, Limitations, or Future Work sections are created. F1-F9 are retained with their reported values, aggregation, uncertainty, and measurement scope. Negative task-superiority evidence is preserved. The discussion labels the proposed explanation as a hypothesis rather than a demonstrated mechanism. No novelty, state-of-the-art, energy, temporal-event-equivalence, task-superiority, or broad-GNN-generality claim is made.
