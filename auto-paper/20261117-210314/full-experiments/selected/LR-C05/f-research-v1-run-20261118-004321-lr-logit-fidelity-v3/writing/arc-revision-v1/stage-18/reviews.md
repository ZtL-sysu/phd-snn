# AutoResearchClaw Stage 18 Peer Review

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

# Reviewer B Report

## Summary
The manuscript is unusually candid about validation exposure, negative task results, temporal-event limitations, and the absence of energy claims. The reported values agree with the evidence digest. However, the exact-cost ledger, split/seed protocol, comparator construction, timing boundary, and per-seed data are insufficiently specified for independent reproduction. No fatal inconsistency was found, but major revision is required before the central matched-budget claim is auditable.

## Score
6/10

## Confidence
4/5

## Strengths
- The abstract, Sections 4.3–4.5, and conclusion consistently distinguish held-out confirmation from preregistration or independent replication.
- Section 4.5 retains the mixed task results and failed task-superiority gate instead of presenting universal task improvement.
- The manuscript clearly states that sparse residual coefficients are not temporal SNN events and excludes energy and broad-GNN claims.
- Reported values and qualifiers in Sections 4.3–4.5 agree with facts F1–F9 in the evidence digest.
- Figure captions generally distinguish validation-grid results from later held-out results and separate the rank-128/2% fidelity condition from the rank-128/1% runtime condition.

## Major Concerns
1. **Major — Exact-cost matching is not reproducible.**  
   **Evidence:** Section 3 defines only \(C(S)=\sum \operatorname{padded\_serialized\_bits}(q)\), while “Method” says matching occurs “within each dataset, seed, rank, and budget condition”; F3 says only “within each dataset.” “Comparisons therefore use a matched total padded serialized-bit budget” does not specify whether the rank-128 basis, indices, metadata, headers, padding, and conversion parameters are included.  
   **Why it matters:** The central claim depends on exact bit equality, but the ledger cannot be reconstructed or checked, and the stated matching scope is internally inconsistent.  
   **Repair condition:** Define the complete record schema, numeric formats, index widths, alignment/padding rule, included basis and metadata costs, and the denominator defining “2%.” Report proposed/control bit totals for every dataset, seed, rank, and budget row, and make all descriptions use one consistent matching scope.

2. **Major — Split and seed semantics are incomplete.**  
   **Evidence:** Section 4.1 uses “the reported split protocol” without identifying split indices, proportions, preprocessing, or whether all methods share identical nodes. Section 3 calls 0/1/2 “checkpoint seeds,” whereas results are aggregated as “three-seed means.”  
   **Why it matters:** Readers cannot reproduce the evaluated population or determine whether variation comes from checkpoints, splits, initialization, or rate-code randomness.  
   **Repair condition:** Specify the split source and exact indices or deterministic generation rule, state whether splits are fixed across methods and seeds, define every stochastic seed, and provide a per-seed/per-split results table.

3. **Major — Validation-driven selection is not fully accounted for.**  
   **Evidence:** Section 4.1 states that “Validation was used for setting selection” and that the focal setting and framing were fixed after validation exposure. Section 4.4 reports the 0.5%, 1%, and 2% grid, but the complete candidate set, selection criterion, and number of examined variants are not stated.  
   **Why it matters:** “Held-out confirmation” remains appropriately qualified, but the degree of adaptive validation exposure and selection multiplicity cannot be assessed.  
   **Repair condition:** Enumerate all validation-exposed settings and outcomes, define the rule that selected rank 128 and 2%, confirm that the reported test split was evaluated only after fixing the rule, and retain “post-selection held-out confirmation” in the abstract and conclusion.

4. **Major — Comparator and “strongest control” selection are underdefined.**  
   **Evidence:** Section 4.2 gives only one-line descriptions of “our matched-budget adaptations of A2Q” and “One-Spike.” It defines the strongest control as the non-proposed method with the lowest logit MSE but does not say whether selection uses test results, three-seed means, or a fixed comparator per dataset/seed. Section 4.5 also refers to degradation “relative to the strongest control” without clarifying whether the fidelity-best control is reused for task metrics.  
   **Why it matters:** The adaptation algorithms and conservative-but-post-hoc baseline choice cannot be reproduced, and task and fidelity comparisons may use different denominators.  
   **Repair condition:** Fully specify both adaptations and their hyperparameters, state when and on which data the strongest control is selected, identify it for every dataset and metric, and ensure the same comparator definition is used consistently or explicitly justify different comparators.

5. **Major — Conversion and model implementation details are insufficient.**  
   **Evidence:** Section 3 alternates between \(A\) and \(\widetilde D^{-1/2}\widetilde A\widetilde D^{-1/2}\), defines “analogously” hidden-state MSE, and says rate coding represents “each nonnegative post-activation value,” without defining normalization, clipping, negative-value handling, decoding ties, or sensitivity precision. The precise output used for \(J_i\), tie-breaking in `TopB`, and treatment of matrix-shaped residual entries are also absent.  
   **Why it matters:** These choices can materially change sensitivities, reconstruction error, accuracy, and teacher agreement.  
   **Repair condition:** Give the exact adjacency construction, activations, tensor shapes, rate scaling and decoding rule, deterministic tie-breaking, Jacobian output and norm definition, precision, and complete evaluation implementation or executable configuration.

6. **Major — Runtime statistics and boundary are ambiguous.**  
   **Evidence:** Section 4.5 reports paired p95 ratios from seven measured repeats but does not define whether each ratio is \(p95_{\text{proposed}}/p95_{\text{SVD}}\) or the p95 of paired repeat ratios. It does not state CUDA synchronization, data-transfer inclusion, preprocessing/SVD-basis construction, selection-cost inclusion details, peak-memory reset, or whether 218.23 MB is proposed-method maximum memory.  
   **Why it matters:** A p95 estimated from seven observations is highly unstable, and pipeline boundaries can change the reported 1.020–1.124x range substantially.  
   **Repair condition:** Define every timed stage and exclusion, synchronization and device-transfer policy, pairing and p95 formula, allocation/reset method, method and horizon associated with memory, and provide all repeat-level timings with the exact nine pair ratios.

7. **Major — Numerical transparency and uncertainty reporting are inadequate.**  
   **Evidence:** Figure 2 shows means and “sample SD,” but the caption does not state \(n=3\), the SD convention, or individual points. F1 and F8 report ratios of three-seed means and all-nine positive comparisons, but per-seed values are absent. Section 4.5 reports the maximum observed degradation across multiple metrics, datasets, horizons, and seeds without exposing the full distribution.  
   **Why it matters:** The aggregation cannot be recomputed, and an observed maximum is not a statistical upper bound. The manuscript appropriately avoids formal inference, but readers still need the underlying paired observations.  
   **Repair condition:** Add per-seed values and sample SDs for every principal comparison, define `ddof`, show all nine paired differences, retain “maximum observed degradation,” and avoid interpreting 1.86/2.85 pp as population bounds.

## Minor Concerns
1. **Minor — Figure 3 chronology could be visually overstated.**  
   **Evidence:** Section 4.4 and Figure 3 mix the validation-grid 2% result with the later held-out confirmation statement.  
   **Why it matters:** Viewers may interpret all plotted 2% values as independent test confirmation.  
   **Repair condition:** Label validation and confirmation points separately in the plot itself, not only in the prose and caption.

2. **Minor — Figure 4 combines incomparable conditions without a complete visual key.**  
   **Evidence:** Its caption separates fidelity at rank128/2% from runtime at rank128/1%, but “official-test” and “warmed” are informal, and the reported peak memory is not assigned to a panel or method.  
   **Why it matters:** The composite figure may imply a common experimental condition.  
   **Repair condition:** Label each panel with split, residual budget, horizon, comparator, uncertainty convention, and sample count; state where or whether peak memory is displayed.

3. **Minor — Terminology and formatting are inconsistent.**  
   **Evidence:** The manuscript uses “rank128/1%,” “rank 128 and 2%,” “three-seed mean split-specific logit MSE,” and “ratio of three-seed mean.”  
   **Why it matters:** Inconsistent terminology obscures whether values are ratios of means, mean paired ratios, or reductions in per-seed ratios.  
   **Repair condition:** Use one term such as “ratio of three-seed means” and normalize all condition labels.

4. **Minor — Statistical notation is incomplete.**  
   **Evidence:** Section 4.1 defines logit MSE with class dimension \(C\), while hidden MSE is merely “analogously”; Figure 2 says “sample SD” without defining its denominator.  
   **Why it matters:** These omissions prevent exact metric recomputation.  
   **Repair condition:** Write the hidden-MSE denominator explicitly and define the sample-SD formula.

## Required Revisions
- Provide an auditable per-condition serialized-bit ledger and resolve the mismatched matching scopes.
- Specify the exact split, checkpoint, rate-code, Jacobian, and evaluation procedures.
- Fully describe the adapted controls and the data-dependent “strongest control” rule.
- Document the complete validation-selection path and consistently call the test result post-selection held-out confirmation.
- Release or tabulate per-seed results, sample SDs, all nine paired comparisons, and repeat-level timing observations.
- Tighten Figures 2–4 captions and panel labels so validation/test status and experimental conditions are unambiguous.
- Complete the scheduled 36-reference authenticity/relevance/placement/duplicate audit; related-work claims cannot be accepted while that gate remains open.

## Questions
- Does “2%” refer to residual coefficients, residual entries, total transport entries, or a serialized-bit fraction?
- Are seeds 0/1/2 checkpoint seeds only, or do they also change data splits or rate-code randomness?
- Is the strongest control chosen from test outcomes, and is it the same control for fidelity and task-loss comparisons?
- Does full-pipeline timing include adjacency construction, SVD-basis construction, host-device transfers, and CUDA synchronization?
- Was the reported test split accessed exactly once after all selection and reframing decisions were frozen?