**Canonical six-section outline and claim/evidence map**

## 1 Introduction
- Open from output-sensitive information loss in compressed graph messages under a fixed serialized budget.
- State the bounded question: can output-Jacobian-selected sparse residual coefficients improve logit fidelity at a **matched total padded serialized-bit budget** while bounding task degradation in frozen GNN-to-SNN compression?
- State the contribution with the reported test-split result: rank-128 SVD transport with a 2% output-Jacobian-selected sparse residual budget reduced the ratio of three-seed mean split-specific logit MSE versus the strongest evaluated matched-budget control on Cora, Chameleon, and Squirrel (F1).
- Include the bounded-degradation result as the secondary claim (F2).
- Do not claim task superiority, energy savings, temporal SNN-event equivalence, or broad GNN generality (F5).
- **Fact IDs:** F1, F2, F3, F5.

## 2 Related Work
- Organize methodologically, not paper-by-paper: low-rank or quantized graph-message transport; output-sensitive coefficient or residual selection; logit-preserving GNN-to-SNN conversion; matched-budget fidelity evaluation.
- Compare assumptions, cost models, and evaluation settings rather than incompatible published scores as direct experiments.
- Claim that prior work cannot solve the focal problem only where supported by verified citations.
- If prior-art adaptations are compared in the experiments, introduce those adaptation choices here at a high level.
- **Fact IDs:** none primary; methodological framing supports the comparison behind F1.

## 3 Method
- Define the frozen two-layer hidden-16 GCN checkpoints seeds 0/1/2, SVD rank-128 transport, and the 2% sparse residual coefficient budget.
- Define output-Jacobian squared sensitivity as the selector for sparse residual coefficients after SVD transport (F1 condition).
- Define sparse residual coefficients as selected exact message residual values with explicit indices, not temporal spikes (F5).
- Define the exact serialized-cost ledger: within each dataset, all compared rank-128/2% methods used identical total padded serialized bits, while payload lengths and coefficient counts could differ; this is the **matched total padded serialized-bit budget** (F3).
- Define rate-coded conversion and the evaluation scope: reported test split, held-out confirmation after validation-exposed reframing, not preregistered independent replication (F5).
- Place F5 at home here; repeat locally when any statement of generality, novelty, energy, or event semantics would otherwise become misleading.
- **Fact IDs:** F1 model/condition, F3, F5.

## 4 Experiments and Results
- **Main comparison:** On the reported test split, rank-128 SVD transport with a 2% output-Jacobian-selected sparse residual budget reduced the ratio of three-seed mean split-specific logit MSE versus the strongest evaluated matched-budget control by 26.23% on Cora, 33.99% on Chameleon, and 25.83% on Squirrel; all nine dataset-seed comparisons improved (F1).
- **Task trade-off:** Maximum three-seed-mean degradation across T=2/4 accuracy and teacher agreement was 1.86 percentage points; largest seed-level degradation was 2.85 percentage points (F2). Present as a bounded observation, not an equivalence proof.
- **Cost:** Across nine dataset-seed pairs, paired p95 full-pipeline runtime ratios versus SVD-only ranged from 1.020 to 1.124; peak CUDA allocation was 218.23 MB on the warmed RTX 3060 benchmark with three warmups and seven measured repeats, using rank-128/1% full encode/selection/decode/conversion timing (F4). Scope is wall-clock pipeline cost, not hardware energy.
- **Exact cost match:** Reiterate that comparisons used the **matched total padded serialized-bit budget** (F3).
- **Supporting and diagnostic:** prior-art adaptations, hidden MSE, rank/budget sensitivity, and negative task-superiority evidence as needed.
- Organize around questions and observed patterns, not run IDs or table cells; cite figures near their evidence.

## 5 Discussion
- Interpret the fidelity gain at matched serialized cost as an observed predictive benefit, not as task superiority.
- Distinguish observed patterns from mechanism hypotheses; incomplete mechanism identification does not erase the observed predictive benefit.
- State the material limits (F5): the test run is held-out confirmation, not preregistered independent replication; sparse residual coefficients are not temporal SNN events; no energy or broad GNN-generality claim is supported.
- Avoid repeating the Results inventory and avoid commands for future experiments; optional future work must be targeted.

## 6 Conclusion
- Answer the Introduction’s question with the supported three-graph result: on the reported test split, rank-128 SVD transport with a 2% output-Jacobian-selected sparse residual budget reduced the ratio of three-seed mean split-specific logit MSE by 26.23% on Cora, 33.99% on Chameleon, and 25.83% on Squirrel versus the strongest evaluated **matched total padded serialized-bit budget** control; all nine dataset-seed comparisons improved (F1).
- Bound the task trade-off: maximum three-seed-mean degradation was 1.86 percentage points and maximum seed-level degradation was 2.85 percentage points (F2).
- Close within the tested frozen-GCN scope; add no new result, mechanism, or application promise.
- **Fact IDs:** F1, F2, with F5 constraining scope.