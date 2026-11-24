# Reviewer A Report

## Summary

The manuscript presents a narrowly scoped, cautiously worded study of output-Jacobian-guided residual transmission for frozen GCN-to-SNN conversion. The matched serialized-bit accounting, consistent positive logit-MSE comparisons, explicit negative task result, and stated measurement boundaries are strengths. However, the central contribution is not isolated from the generic benefit of transmitting residual information, the rank-128 method scope is ambiguous for a hidden-width-16 model, and the practical value of logit fidelity remains weak without task superiority, energy savings, or another demonstrated downstream benefit.

## Score

4/10

## Confidence

4/5

## Strengths

1. The reported test-split result is consistently positive across three datasets and three checkpoint seeds.
2. Comparisons use an explicit serialized-bit ledger rather than only coefficient percentages.
3. The manuscript retains the failed task-superiority result and does not convert mixed task outcomes into a universal improvement claim.
4. Runtime, memory, validation exposure, lack of preregistration, absence of energy evidence, and non-temporal nature of the residual records are explicitly disclosed.

## Major Concerns

1. **Severity: Fatal — Output-Jacobian selection is not causally isolated.**  
   **Evidence:** Section 3 defines TopB squared-Jacobian selection, while Section 4.2 compares against SVD-only and vague A2Q/One-Spike adaptations. Section 4.4 reports gains over those controls but no random, residual-magnitude, uniform, or other gradient-free residual selector.  
   **Why it matters:** The experiments may show that spending available bits on residual records helps, but they do not establish that output-Jacobian scoring causes the improvement. This undermines the paper’s principal method contribution.  
   **Repair condition:** Compare against at least random selection, \(|r_i|\) or \(r_i^2\) selection, and a simple non-output-aware allocation under exactly the same ledger; show paired per-seed results and an ablation replacing or perturbing the Jacobian scores.

2. **Severity: Major — Rank-128 scope conflicts with the model definition.**  
   **Evidence:** Section 3 defines a two-layer hidden-16 GCN and \(M^{(l)}=AH^{(l-1)}\), but subsequently states “for each message matrix \(M=AX\)” and applies rank 128. For the second layer, \(AH^{(1)}\) has rank at most 16.  
   **Why it matters:** It is impossible to determine whether rank 128 applies only to the input-feature message, both graph aggregations, or another tensor. If applied to the second layer, the stated residual would be zero up to numerical error.  
   **Repair condition:** Enumerate every transported message and its shape, rank, residual budget, and cost. If only \(AX\) is compressed, revise the method and contribution scope accordingly; if both layers are compressed, use valid layer-specific ranks and report both layers separately.

3. **Severity: Major — The exact-cost comparison is not reproducible or demonstrably fair.**  
   **Evidence:** The ledger uses implementation-defined `padded_serialized_bits`, while the manuscript does not provide absolute bit counts, record formats, index widths, alignment rules, rank-basis costs, or the denominator of the “2% residual budget.” Section 3 also says payload lengths and coefficient counts may differ.  
   **Why it matters:** Arbitrary padding can equalize nominal cost without ensuring that every method uses the budget efficiently. SVD-only may merely waste slack that the proposed method consumes.  
   **Repair condition:** Publish a per-method bit decomposition, absolute total and uncompressed costs, serialization schema, and the exact definition of 2%. Demonstrate that each control uses the available budget under a common encoding policy rather than being padded into artificial equivalence.

4. **Severity: Major — The Jacobian score omits residual magnitude and interaction effects.**  
   **Evidence:** Section 3 ranks coefficients by \(\|\partial z/\partial r_i\|_2^2\), although transmitted values are \(r_i\). No first-order impact such as \(\|r_iJ_i\|^2\), curvature correction, or joint ablation is evaluated.  
   **Why it matters:** A large residual with modest sensitivity may cause more reconstruction error than a small residual with high sensitivity. Coordinatewise local gradients can also fail after jointly retaining many coefficients under nonlinearities.  
   **Repair condition:** Compare gradient-only ranking with magnitude-weighted influence, exact leave-one-out or batched ablation scores, and retained-set re-evaluation; describe the result as a heuristic unless joint effects are validated.

5. **Severity: Major — Logit fidelity has insufficient demonstrated utility.**  
   **Evidence:** Sections 4.5 and 5 state that task superiority failed, with maximum observed losses of 1.86 pp at the three-seed-mean level and 2.85 pp at seed level. No energy result exists, and runtime overhead reaches 1.124x. Logit MSE also gives weight to common-mode logit shifts that need not alter predictions.  
   **Why it matters:** Reduced teacher-logit MSE is meaningful as a compression diagnostic, but by itself does not establish a useful GNN-to-SNN compression improvement when accuracy, agreement, energy, and runtime do not improve.  
   **Repair condition:** Either demonstrate downstream utility such as better distillation, calibration, transfer, or accuracy at equal fidelity, or explicitly position the work as a limited logit-coding study. Add centered-logit or prediction-distribution metrics to separate decision-relevant error from harmless logit shifts.

6. **Severity: Major — Baseline and novelty boundaries are inadequate.**  
   **Evidence:** Section 4.2 gives only one-sentence descriptions of “our matched-budget adaptations” of A2Q and One-Spike. Section 2 does not establish novelty against broader sensitivity-guided residual coding or saliency-based allocation. The evidence digest reports that the 36-reference audit remains pending.  
   **Why it matters:** Unspecified adaptations may be weak or unfaithful controls, and output-gradient saliency may be a direct application of established sensitivity-based allocation rather than a distinct method.  
   **Repair condition:** Fully specify adaptation algorithms, tuning, and fidelity to the cited methods; add appropriate nonlearned controls; complete the citation audit and explicitly distinguish the contribution from sensitivity-guided compression and pruning.

## Minor Concerns

1. **Severity: Minor — Absolute effect sizes are missing.**  
   **Evidence:** Sections 4.3-4.4 report percentage reductions but no numerical absolute MSE values in the text or evidence digest.  
   **Why it matters:** A 26-34% relative reduction may correspond to a practically negligible error difference.  
   **Repair condition:** Add absolute three-seed means, sample SDs, and per-seed values for every principal comparison.

2. **Severity: Minor — “Strongest control” is ambiguously selected.**  
   **Evidence:** Section 4.2 defines it as the lowest-logit-MSE non-proposed method “under the corresponding exact-cost condition,” without stating whether identity is fixed per dataset, seed, metric, or budget.  
   **Why it matters:** The comparison target and aggregation cannot be reconstructed exactly.  
   **Repair condition:** Name the selected control for every dataset and condition and state the selection rule before computing reductions.

3. **Severity: Minor — “Bounded task loss” overstates the evidence.**  
   **Evidence:** Section 4.5 reports 1.86 pp and 2.85 pp as bounds but acknowledges they are observations rather than an equivalence proof.  
   **Why it matters:** “Bound” can imply a statistical or worst-case guarantee beyond the tested samples.  
   **Repair condition:** Replace it with “maximum observed degradation” and retain the no-equivalence disclaimer.

4. **Severity: Minor — ANN-to-SNN objective alignment is unclear.**  
   **Evidence:** Section 3 defines Jacobians of the frozen output, while evaluation concerns rate-coded conversion at \(T=2,4\). The manuscript does not state whether gradients pass through conversion.  
   **Why it matters:** ANN-logit sensitivity may not rank coefficients optimally for low-horizon converted outputs.  
   **Repair condition:** Identify the differentiated model explicitly and report whether Jacobian ranking transfers consistently to converted logits at \(T=2\) and \(T=4\).

5. **Severity: Minor — Selection granularity and transductive access are underspecified.**  
   **Evidence:** Section 3 defines residual coefficients over a message matrix but does not state whether \(S\) is global per graph, per layer, per node, or selected using outputs from validation/test nodes.  
   **Why it matters:** The transport cost, permitted input access, and relation to split-specific logit MSE cannot be reconstructed.  
   **Repair condition:** Define the coefficient index, selection unit, nodes used to form \(J_i\), and whether all test-node features and teacher outputs are available during selection.

6. **Severity: Minor — Runtime statistics are detached from the focal setting.**  
   **Evidence:** Section 4.5 reports rank128/1% timing, whereas the main result uses rank128/2%; p95 is estimated from only seven repeats.  
   **Why it matters:** Resource overhead at the headline setting remains unknown, and p95 from seven samples is unstable.  
   **Repair condition:** Report focal 2% timing with median, spread, and raw repetitions, while retaining the 1% timing only as secondary evidence.

## Required Revisions

- Resolve the layer/message and rank-128 specification, especially the rank of \(AH^{(1)}\) under hidden width 16.
- Add selection-specific baselines and ablations that isolate Jacobian scoring from generic residual transmission.
- Specify the full serialized-cost ledger, absolute bit budgets, record format, and exact meaning of 2%.
- Report absolute MSE values, per-seed outcomes, named control identities, and complete task metrics at the focal setting.
- Establish practical relevance through a downstream benefit or an equal-quality resource comparison, or narrow the contribution explicitly to logit-coding fidelity.
- Complete the pending citation audit and strengthen the novelty comparison to sensitivity-guided compression methods.

## Questions

1. Which graph messages are actually transported and compressed: only \(AX\), both graph aggregations, or another tensor?
2. What exactly is the denominator of the 2% residual budget?
3. How does SVD-only consume the same serialized-bit budget without being artificially padded?
4. Are the A2Q and One-Spike adaptations faithful to their cited methods, and how were their parameters tuned?
5. Are Jacobians computed through the ANN checkpoint or through the rate-coded converted model?
6. What downstream use makes lower logit MSE valuable enough to accept mixed task outcomes and nonzero runtime overhead?
