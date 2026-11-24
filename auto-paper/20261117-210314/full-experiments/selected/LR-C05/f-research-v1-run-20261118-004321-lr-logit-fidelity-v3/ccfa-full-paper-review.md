# CCFA Full Manuscript Review

## 1. Report Metadata

Review date: 2026-11-18  
Target venue/year/track: Not specified; reviewed as a generic CCF-A computer-science conference manuscript in the GNN/SNN conversion and graph-representation-learning area.  
Paper title: `Output-Jacobian Sparse Residual Allocation for Matched-Budget GNN-to-SNN Logit Fidelity`  
Input materials reviewed: `writing/p8/paper-data-figures.md`; `writing/p9-evidence-digest.json`; `writing/arc-review-v1/reviewer-a.md`; `writing/arc-review-v1/reviewer-b.md`; `results/confirmation-summary.json`; `results/confirmation-test-v2.json`; `inputs/v2-summary.json`; `inputs/v2-timing.json`.  
Search basis: Supplied local evidence plus public-safe searches for GNN-to-SNN conversion, graph-message compression/quantization, output sensitivity, and sensitivity-guided compression. No private manuscript text was used as a public search query.  
Report file: `C:\code\phd-snn\auto-paper\20261117-210314\full-experiments\selected\LR-C05\f-research-v1-run-20261118-004321-lr-logit-fidelity-v3\ccfa-full-paper-review.md`  
Reviewer mode: `full`; independent scientific, evidence, reproducibility, writing, format, and revision-action review. No manuscript edits or experiments were run.

## 2. Desk Rejection Assessment

- Paper length: `uncertain`. The supplied frozen artifact is Markdown, so page count, appendix placement, and venue page limits cannot be checked.
- Topic compatibility: `pass` for a GNN-to-SNN / graph compression venue, but `uncertain` for a specific CCF-A venue without a named target and current venue guide.
- Minimum quality: `pass` with major revision risk. The paper has a clear question, bounded method, result tables/figures in the source plan, limitations, and negative-result disclosure.
- Policy/anonymity/compliance: `uncertain`. No submission template, author block, supplement policy, or current-year venue rules were supplied.
- Prompt injection and hidden manipulation detection: `pass` for the supplied manuscript and evidence digest. No instruction-like content was found that attempts to direct the reviewer.
- Ethics and reviewability: `pass` for obvious human-subject/privacy risks; `uncertain` for compute/environment and artifact licensing because those are not documented.

Desk rejection risk: `low-to-medium`  
Reason: The manuscript is scientifically reviewable and candidly scoped, but the central cost protocol, rank/message scope, comparator construction, and validation-selection history are not independently auditable from the frozen text.  
Can be fixed before review? `partly`; documentation and existing-result presentation can resolve several issues, while independent replication and broader utility evidence require new experiments.

## 3. Paper Summary And Contribution Map

The paper studies frozen two-layer, hidden-16 GCN checkpoints on Cora, Chameleon, and Squirrel. It transports graph messages with an operator-aligned rank-128 SVD basis and allocates a 2% sparse residual budget using squared output-Jacobian sensitivity. The claimed contribution is improved split-specific logit fidelity under an exact total padded serialized-bit ledger, while task degradation is reported as bounded rather than as universal task improvement.

Claimed problem: repeated high-dimensional `AX` messages lose output-relevant information under a serialization budget.  
Claimed gap: generic low-rank transport or output-code allocation does not identify which residual coefficients matter for downstream logits.  
Method/contribution map: rank-128 SVD transport; output-Jacobian score `||J_i||_2^2`; top-`B` exact residual pairs with explicit indices; exact padded-bit accounting; rate-coded conversion at `T=2/4`.  
Evidence package: official-test confirmation summary; 63-row confirmation table containing seven residual modes and a full-float reference; validation-grid summary at 0.5%, 1%, and 2%; 54-row timing file with three warmups and seven measured repeats; evidence digest; two ARC reviews.  
Stated limitations: validation exposure before the held-out test run; no preregistration or independent replication; sparse residual coefficients are not temporal SNN events; no energy claim; no broad GNN-generality claim; task superiority was not established.

## 4. Search And Related-Work Basis

Queries used: `GNN to SNN conversion graph neural network`; `graph message compression quantization GNN`; `output sensitivity guided compression residual allocation`; `sensitivity driven quantization graph neural network`.  
Sources searched: public web search results and official/open links when returned.  
Closest works found: `VQ-GNN: A Vector Quantized Graph Neural Network` surfaced through an official NeurIPS/OpenReview link; `Sensitivity-Driven Regularization for Quantization-Aware Training of Graph Neural Networks` surfaced as an arXiv preprint. These are positioning candidates, not a completed closest-work audit.  
Unverified related-work risks: The manuscript’s 36-reference authenticity/relevance/placement/duplicate audit is still marked as scheduled at P12 in `writing/p9-evidence-digest.json`; no claim of exhaustive related-work coverage is accepted.  
Source-quality screening status: Mixed. One NeurIPS/OpenReview source is suitable for venue positioning; the sensitivity paper is a preprint and requires author/published-version verification. Aggregator results were not treated as authoritative.

## 5. Expected Review Outcome

Expected outcome: `borderline negative / weak reject` in the current frozen state.  
Main accept signal: The reported logit-MSE improvement is positive on all nine dataset-seed comparisons at rank 128/2%, and the supplied raw table contains useful selector controls beyond those described in the manuscript.  
Main reject signal: The central matched-budget claim remains hard to audit, the rank/message scope is ambiguous, validation-driven selection is incompletely documented, and lower logit MSE has not demonstrated downstream utility, task superiority, energy benefit, or broad generality.  
Confidence: `4/5` for the evidence-backed empirical reading; `3/5` for novelty and venue-fit judgments because no venue and no completed related-work audit were supplied.

## 6. Strengths And Weaknesses

### Strengths

- The manuscript states the measurement boundaries unusually clearly: held-out confirmation after validation exposure, no preregistration, no temporal-event claim, no energy claim, and no broad-GNN claim (`paper-data-figures.md:L5`, `L55`, `L112`).
- The main fidelity direction is consistent. The digest reports 26.23%, 33.99%, and 25.83% reductions versus the strongest evaluated matched-budget control, with all nine dataset-seed comparisons positive (`p9-evidence-digest.json:L6-L25`).
- The raw confirmation file contains 63 rows: `downstream_jacobian`, `top_abs`, `random`, `uniform`, `a2q_node_budget`, `one_spike`, and a full-float `none` reference across nine dataset-seed pairs. This is stronger evidence than the frozen manuscript’s four-row method table alone.
- For the matched SVD rows, the raw file gives equal total padded bits within each dataset: Cora 21,932,736 bits; Chameleon 25,630,208 bits; Squirrel 43,771,008 bits. The full-float `none` rows are larger and should not be treated as matched controls.
- The manuscript retains the failed task-superiority result and explicitly refuses to turn mixed task deltas into universal improvement (`paper-data-figures.md:L98-L100`).
- The timing claim is numerically recoverable from `inputs/v2-timing.json`: ratios of `downstream_jacobian` p95 to `svd_only` p95 span 1.020393–1.123798 across nine dataset-seed pairs, with maximum peak allocation 218.23 MB.

### Major weaknesses

#### W1. Rank-128 message scope is not well-defined

Evidence basis: Section 3 defines a hidden-width-16 model and then writes `M = AX` with rank 128 (`paper-data-figures.md:L25-L35`). The second-layer message `AH^(1)` has width/rank constraints that make a blanket rank-128 statement ambiguous.  
Reviewer deduction: A reader cannot tell whether only `AX` is transported, both graph aggregations are transported, or rank 128 is a nominal setting applied to another tensor. If the second layer is included, the stated residual can be zero or numerically degenerate.  
Required fix: Enumerate every transported tensor, shape, layer, rank, residual budget, and serialized cost. If only `AX` is compressed, narrow the method and contribution scope to input-message transport; if both layers are compressed, use valid layer-specific ranks and report them separately.  
Repair class: Existing implementation/configuration evidence can likely repair the description; new experiments are required only if the current runs actually compressed both layers under an invalid rank.

#### W2. Exact-cost matching is not independently reproducible

Evidence basis: The method defines `C(S) = sum padded_serialized_bits(q)` but not the record schema, numeric formats, index widths, headers, alignment, padding rule, basis cost, or denominator of “2%” (`paper-data-figures.md:L39-L45`). The raw rows show equal totals per dataset but do not explain how equality was produced.  
Reviewer deduction: Equal nominal totals can conceal inefficient padding or unequal treatment of basis, indices, metadata, and coefficient counts. The frozen text also switches between matching “within each dataset, seed, rank, and budget condition” and “within each dataset.”  
Required fix: Publish the complete serialization schema and a per-method/per-condition bit decomposition. Define whether 2% means residual entries, total message entries, or serialized bits; state rounding; and make all matching-scope wording identical.  
Repair class: Existing raw fields and code/config can repair the accounting if they are complete. If the ledger cannot be recovered, re-encoding or re-running the comparisons is a new-result requirement.

#### W3. Selector isolation is partly present in raw data but absent from the manuscript

Evidence basis: `results/confirmation-test-v2.json` contains `top_abs`, `random`, and `uniform` rows in addition to the proposed selector, while Section 4.2 only lists SVD-only, the proposed selector, and two adapted controls (`paper-data-figures.md:L63-L74`). The proposed method beats `top_abs` on all nine paired logit-MSE comparisons, but the meanings of `top_abs`, `random`, and `uniform` are not defined in the frozen text.  
Reviewer deduction: The raw evidence weakens the ARC claim that no magnitude/random/non-output-aware selector exists, but it does not establish what those controls actually do. Without definitions, the reader cannot tell whether Jacobian scoring is isolated from residual magnitude, random allocation, or a different budget policy.  
Required fix: Define every raw control and show a compact comparison table. If `top_abs` is magnitude selection and `uniform` is a non-output-aware allocation, say so explicitly and report all nine paired values. Add a Jacobian-versus-magnitude/leave-one-out interaction ablation if the mechanism claim remains causal.  
Repair class: Existing raw results can repair the baseline disclosure. New experiments are needed for interaction, curvature, or leave-one-out ablations not present in the supplied files.

#### W4. Validation selection and comparator choice are underdocumented

Evidence basis: The manuscript says validation was used for setting selection and that the focal setting and reframing were fixed after validation exposure (`paper-data-figures.md:L55`, `L78`, `L112`). The raw summary names `top_abs` as `best_control`, but does not state whether control selection used test outcomes, three-seed means, or a pre-fixed rule.  
Reviewer deduction: “Held-out confirmation” is appropriately qualified, but selection multiplicity and comparator adaptivity cannot be assessed. The strongest fidelity control may not be the same denominator used for task loss.  
Required fix: Enumerate all validation-exposed candidates and outcomes, define the rule that selected rank 128 and 2%, identify the comparator for every dataset/metric/seed, and state whether the test split was accessed only after freezing the rule.  
Repair class: Existing run logs/configs can repair disclosure if they exist. Independent replication or a preregistered confirmatory run is a new experiment; retrospective wording alone cannot create independence.

#### W5. Task-loss aggregation is internally ambiguous

Evidence basis: The manuscript reports a maximum three-seed-mean loss of 1.86 pp and seed-level loss of 2.85 pp across T=2/4 accuracy and teacher agreement (`paper-data-figures.md:L96-L100`). In `confirmation-summary.json:L17`, the global numbers match the raw data when task loss is computed against the best task control per metric. However, the per-dataset `worst_task_loss_pp` values match teacher-agreement-only degradation: Cora 0.4667 pp, Chameleon 1.1696 pp, Squirrel 1.8572 pp. Recomputing against `top_abs`, which the summary labels `best_control`, gives different values, including a 2.2 pp seed-level accuracy loss on Cora.  
Reviewer deduction: The headline task-loss statistic cannot be reproduced until the comparator and metric aggregation are stated. “Bounded” reads like a guarantee although it is only a maximum observed degradation.  
Required fix: Define the task-loss formula, comparator identity, metric set, aggregation order, and rounding. Replace “bounded task loss” with “maximum observed degradation” unless a non-inferiority/equivalence design is supplied.  
Repair class: Existing rows can repair the table and wording. A formal bound, equivalence claim, or population guarantee requires new statistical evidence.

#### W6. Practical significance is limited to logit fidelity

Evidence basis: Task superiority failed, deltas are mixed (`paper-data-figures.md:L100`; `p9-evidence-digest.json:L185-L203`), runtime overhead is nonzero, and no energy or downstream benefit is reported.  
Reviewer deduction: Lower teacher-logit MSE is a useful compression diagnostic, but it is not yet a demonstrated GNN-to-SNN capability improvement. The paper must either establish downstream utility or position itself explicitly as a narrow logit-coding study.  
Required fix: Either add distillation/calibration/transfer/accuracy-at-equal-fidelity or energy/resource evidence, or narrow the title, abstract, and contribution claim to logit-fidelity coding.  
Repair class: Narrowing and limitation wording can be repaired with existing evidence; utility, energy, equivalence, and broader generality require new experiments.

#### W7. Novelty positioning is not closed

Evidence basis: The related-work section lists conversion and quantization families but does not establish the exact difference from sensitivity-guided compression/pruning or graph vector quantization. The evidence digest marks the 36-reference audit as pending. Public search surfaced VQ-GNN and sensitivity-driven quantization as candidates.  
Reviewer deduction: The novelty delta may be real—output-Jacobian allocation for frozen GNN-to-SNN logit fidelity—but the current manuscript does not demonstrate that delta against the closest sensitivity-allocation literature.  
Required fix: Complete the reference audit and add a precise technical comparison to sensitivity-guided compression, graph quantization, and output-aware coding. Do not claim “first” or broad novelty without verification.  
Repair class: Existing bibliography/source materials can repair positioning. New baselines are required only if the closest method cannot be compared fairly with the current protocol.

## 7. Potentially Missing Related Work

Work: `VQ-GNN: A Vector Quantized Graph Neural Network`  
Status: `unverified` for final bibliography; public-safe search candidate.  
Why relevant: It addresses graph-representation compression/quantization and could clarify whether the contribution is a new allocation principle or a graph-specific application of vector quantization.  
Overlap: Compressed graph representations and communication efficiency; not identical to frozen GNN-to-SNN logit fidelity.  
Needed comparison: Exact-cost graph-message protocol, fidelity metric, and whether output sensitivity changes coefficient allocation.

Work: `Sensitivity-Driven Regularization for Quantization-Aware Training of Graph Neural Networks`  
Status: `unverified` preprint; requires bibliographic verification.  
Why relevant: It is close to sensitivity-guided graph quantization and could challenge the novelty framing of Jacobian-ranked residual allocation.  
Overlap: Sensitivity-aware quantization/allocation; differs if the present work is frozen conversion rather than quantization-aware training.  
Needed comparison: Frozen checkpoint versus trained quantizer; residual records versus learned quantization; output-logit objective versus task-training objective.

No other missing citation is asserted. The scheduled 36-reference authenticity/relevance/placement/duplicate audit remains a hard reviewability gate.

## 8. Claim-Evidence Audit

| Claim | Where stated | Evidence provided | Strength | Reviewer deduction | Required fix |
|---|---|---|---|---|---|
| Rank-128/2% Jacobian selection reduces logit MSE by 26.23%, 33.99%, 25.83% versus the strongest matched-budget control | Abstract; Section 4.3; Conclusion (`paper-data-figures.md:L5`, `L78`, `L116`) | `confirmation-summary.json:L6-L9`; 63-row `confirmation-test-v2.json`; digest F1 | Strong within the reported scope | The direction and rounded values are supported; per-seed values are not visible in the manuscript | Add absolute means, sample SD, and all nine paired values from raw JSON |
| All nine dataset-seed comparisons improve | Section 4.3 (`L78`) | Raw confirmation rows; digest F1 | Strong | Supports consistency, not statistical generalization | Keep descriptive language; do not imply population certainty |
| All compared rank-128/2% methods use identical total padded bits | Abstract; Section 4.2 (`L5`, `L74`) | Raw `total_padded_bits` equality within each dataset; digest F3 | Adequate | The equality is visible, but the ledger construction is not | Publish schema, absolute bit decomposition, and one matching scope |
| Output-Jacobian scoring itself causes the gain | Section 3 and Discussion (`L35-L45`, `L110`) | Raw `top_abs`, `random`, `uniform` controls; proposed beats `top_abs` in all nine comparisons | Adequate but not complete | Raw controls improve the case, but their definitions and interaction effects are missing | Define controls; add Jacobian-versus-magnitude/leave-one-out ablation if causal language is retained |
| Task loss is bounded at 1.86 pp mean and 2.85 pp seed-level | Abstract; Section 4.5 (`L5`, `L98`) | `confirmation-summary.json:L17`; raw rows | Weak-to-adequate | The global numbers are reproducible only under a particular comparator/metric interpretation; `best_control: top_abs` does not explain the per-dataset values | State formula and comparator; replace “bounded” with “maximum observed” absent equivalence testing |
| Task superiority is not established | Section 4.5 (`L100`) | `inputs/v2-summary.json:L254-L257`; digest F9 | Strong | Negative result is retained honestly | Keep this limitation prominent in abstract and conclusion |
| Runtime is 1.020–1.124x with 218.23 MB peak allocation | Abstract; Section 4.5 (`L5`, `L102`) | `inputs/v2-timing.json`; digest F4 | Adequate | Recomputes as p95 method ratio across nine pairs; timing boundary and p95 convention remain unclear | Define stages, synchronization, pairing, p95, and memory reset; report raw repeats |
| The test run is held-out confirmation, not preregistered replication | Abstract; Sections 4.1 and 5 (`L5`, `L55`, `L112`) | `confirmation-summary.json:L19`; digest F5 | Strong disclosure | Honest, but selection history is incomplete | Add validation candidate ledger and access chronology |
| Broad GNN-to-SNN or energy claims are unsupported | Abstract; Discussion (`L5`, `L112`) | Stated boundary; no energy experiment | Strong as a limitation | Scope discipline is a strength | Keep claims narrow unless new evidence is added |

## 9. Experiment / Benchmark / Reproducibility Audit

- Baselines: The raw confirmation file includes `top_abs`, `random`, `uniform`, `a2q_node_budget`, `one_spike`, `downstream_jacobian`, and a full-float `none` reference. The manuscript exposes only four method labels and does not define the selector controls. The full-float `none` rows have larger `total_padded_bits` and must be labeled as reference, not matched controls.
- Ablations: Budget sensitivity is available at 0.5%, 1%, and 2% in `inputs/v2-summary.json`; hidden-state MSE and logit MSE are reported. No supplied ablation isolates Jacobian interaction, curvature, leave-one-out effects, or ANN versus rate-coded Jacobians.
- Datasets/benchmarks: Cora, Chameleon, and Squirrel; frozen two-layer hidden-16 GCN checkpoints; seeds 0/1/2. The split source, exact indices, preprocessing, and whether splits vary by seed are not specified.
- Metrics: Split-specific logit MSE, hidden-state MSE, T=2/4 accuracy, and teacher agreement. Hidden MSE is called “analogously”; the denominator and sample-SD convention are absent.
- Statistical rigor: Three seeds and descriptive comparisons; no formal confidence intervals are claimed. The manuscript should expose per-seed values and avoid treating maxima as bounds.
- Robustness/failure cases: Budget direction is consistent across nine validation-grid cells, but task deltas are mixed. No broad model/dataset robustness or failure analysis is supplied.
- Implementation details: Missing exact adjacency construction, tensor shapes, activation/rate scaling, negative-value handling, Jacobian differentiated model, precision, tie-breaking, index granularity, and adaptation hyperparameters.
- Artifacts and reproducibility: Raw JSON files are unusually useful and their SHA256 values match the evidence digest for the four cited result inputs. However, the frozen manuscript does not map raw fields to the method definitions or provide executable configuration details.
- Limitations: The paper is candid about validation exposure, non-temporal residuals, no energy claim, and no broad-GNN claim. Practical utility and statistical equivalence remain unresolved.

Raw-result audit notes:

1. `confirmation-test-v2.json` contains 63 rows: seven residual modes times nine dataset-seed pairs. `downstream_jacobian`, `top_abs`, `random`, `uniform`, `a2q_node_budget`, and `one_spike` are SVD/matched-cost rows; `none` is a larger full-float reference.
2. The strongest fidelity control is `top_abs` for Cora, Chameleon, and Squirrel in `confirmation-summary.json`. The proposed selector beats it on all nine paired logit-MSE comparisons.
3. The raw task fields show why the task-loss statement needs a formula. The summary’s per-dataset values align with teacher-agreement-only degradation against the best task control per metric, while the manuscript says the statistic covers accuracy and teacher agreement. The report should not silently choose one interpretation.
4. `inputs/v2-timing.json` contains 54 rows, six methods times nine dataset-seed pairs, with three warmups and seven measured repeats. The reported rounded ratio range and memory maximum are recoverable as a ratio of method-level p95 values, but the exact timed boundary is not.

## 10. Multi-Reviewer Panel

Reviewer: Best-Justified Reviewer  
Expertise: GNN-to-SNN conversion and compression  
Likely score: 6/10  
Confidence: 4/5  
Main positive signal: The focal logit-MSE improvement is consistent and the raw table contains selector controls beyond the manuscript’s visible baseline list.  
Main negative signal: The practical value is limited to logit fidelity and the cost protocol is not yet independently auditable.  
Evidence basis: `confirmation-test-v2.json`, `confirmation-summary.json`, Sections 4.3–4.5.  
Score-change condition: +1 if the raw selector definitions, bit ledger, and per-seed tables make the comparison reproducible and the paper narrows its claim to logit coding.

Reviewer: Critical Reviewer  
Expertise: Empirical ML and reviewer-risk analysis  
Likely score: 4/10  
Confidence: 4/5  
Main positive signal: Negative task evidence and validation exposure are disclosed rather than hidden.  
Main negative signal: Rank/message ambiguity, comparator ambiguity, and lack of downstream utility can independently justify rejection.  
Evidence basis: Sections 3, 4.1, 4.2, 4.5; raw task recomputation.  
Score-change condition: No score increase until the central protocol is reconstructable; new utility evidence or explicit narrow positioning is required.

Reviewer: Method / Soundness Reviewer  
Expertise: Graph algorithms and conversion methodology  
Likely score: 4/10  
Confidence: 4/5  
Main positive signal: The proposed score is defined and the exact-cost idea is concrete.  
Main negative signal: It is unclear which graph message is compressed, which model is differentiated, and how joint residual effects are handled.  
Evidence basis: Section 3 and raw row fields.  
Score-change condition: +1 to +2 if the paper resolves the layer/rank and Jacobian definitions and adds a selector/mechanism ablation.

Reviewer: Evidence / Experiment Reviewer  
Expertise: Experimental design and statistical audit  
Likely score: 5/10  
Confidence: 4/5  
Main positive signal: Positive paired logit comparisons are consistent and raw repeats/timing rows are available.  
Main negative signal: Three seeds, descriptive statistics, missing per-seed display, and an ambiguous task-loss denominator limit inference.  
Evidence basis: `confirmation-test-v2.json`, `inputs/v2-summary.json`, `inputs/v2-timing.json`.  
Score-change condition: Existing data can raise presentation/reproducibility scores; stronger generalization or equivalence claims require new runs.

Reviewer: Novelty / Positioning Reviewer  
Expertise: Graph representation compression and sensitivity methods  
Likely score: 4/10  
Confidence: 3/5  
Main positive signal: The specific combination of frozen GNN-to-SNN conversion, output-Jacobian residual allocation, and exact serialization accounting appears nontrivial.  
Main negative signal: The novelty delta is not established against sensitivity-guided quantization/pruning or graph vector quantization; the citation audit is pending.  
Evidence basis: Related-work section; public-safe search candidates; digest `known_late_gate`.  
Score-change condition: +1 if the citation audit establishes a clear technical delta and the paper avoids broad first-ever language.

Reviewer: Writing / Clarity Reviewer  
Expertise: Scientific writing and reviewer readability  
Likely score: 5/10  
Confidence: 4/5  
Main positive signal: Scope and negative results are unusually clear.  
Main negative signal: The central definitions and result denominators are hidden in implementation shorthand, and Figures 2–4 need tighter condition labels.  
Evidence basis: `paper-data-figures.md:L25-L45`, `L63-L106`; ARC reviews.  
Score-change condition: Existing prose/table/figure edits can move this to 6/10 without changing experiments.

Reviewer: Ethics / Reproducibility Reviewer  
Expertise: Responsible research and artifact audit  
Likely score: 5/10  
Confidence: 4/5  
Main positive signal: No obvious human-subject or privacy issue; limitations are candid.  
Main negative signal: Artifact provenance, licensing, environment, and implementation details are incomplete.  
Evidence basis: Supplied evidence digest and raw result summaries.  
Score-change condition: Add artifact/configuration provenance and limitation detail; new experiments are not required for this score unless reproducibility cannot be recovered.

Reviewer: Domain Application Reviewer  
Expertise: Practical GNN/SNN deployment  
Likely score: 4/10  
Confidence: 3/5  
Main positive signal: Serialization budget and runtime are at least measured.  
Main negative signal: No energy, latency-at-fidelity, deployment, or downstream-task benefit is established; the residual records are not temporal events.  
Evidence basis: Sections 4.5 and 5; timing and limitation statements.  
Score-change condition: Either narrow to a transport-fidelity study or add deployment-relevant evidence in a new experiment.

Reviewer: Evidence / Ablation Reviewer  
Expertise: Mechanism ablation  
Likely score: 4/10  
Confidence: 3/5  
Main positive signal: `top_abs`, `random`, and `uniform` rows exist in the raw confirmation data.  
Main negative signal: Their definitions and interaction effects are absent; no gradient-only versus magnitude-weighted or leave-one-out study is supplied.  
Evidence basis: `confirmation-test-v2.json` residual modes; Section 3.  
Score-change condition: Existing data can support a selector comparison; mechanistic attribution needs a new ablation.

Reviewer: Reproducibility Reviewer  
Expertise: Artifact and protocol reconstruction  
Likely score: 3/10  
Confidence: 4/5  
Main positive signal: Raw row fields expose bit counts, metrics, seeds, repeats, and memory.  
Main negative signal: The fields are not connected to a complete schema, split rule, model implementation, or comparator protocol.  
Evidence basis: Raw JSON schemas and manuscript method/experiment sections.  
Score-change condition: Existing code/config can likely raise this to 4/10; if those artifacts do not exist, re-running is necessary.

Reviewer: Novice Advocate Reviewer  
Expertise: First-pass reader accessibility  
Likely score: 5/10  
Confidence: 4/5  
Main positive signal: The paper explains the question and limitations in plain scientific prose.  
Main negative signal: A new reader cannot reconstruct what “2%”, “strongest control”, or “rank 128” means without external implementation knowledge.  
Evidence basis: Abstract, Sections 3–4, Figures 2–4 captions.  
Score-change condition: Existing terminology and table edits can remove this confusion.

Panel synthesis:

Agreement: All lenses agree that the logit-fidelity direction is promising and the negative task result is honestly reported.  
Agreement: Most lenses agree that the current manuscript is not independently reproducible from the text alone.  
Disagreement: Reviewer A treats missing selector isolation as fatal; the raw table partly answers that concern because `top_abs`, `random`, and `uniform` rows exist. Reviewer B is more positive because the numbers and scope disclosures are consistent.  
Decisive positive axis: Consistent paired logit-MSE gains under equal raw `total_padded_bits`, with candid post-selection and no-task-gain language.  
Decisive negative axis: The protocol and comparator semantics are not reconstructable, and the practical benefit is limited to logit fidelity.  
Unresolved evidence: Which tensor is compressed; what the 2% denominator is; which control is used for task loss; how validation candidates were selected; what the selector controls implement; and whether timing includes all relevant stages.  
AC stance: `Weak reject / borderline negative` for the current frozen manuscript. This is not a rejection of the empirical direction; it is a rejection of presenting it as a fully auditable, broadly useful GNN-to-SNN contribution before the listed repairs are closed.

## 11. Concerns Table

| ID | Severity | Concern | Evidence basis | Affected criterion | Fix class | Required action | Owner skill | Score-change condition |
|---|---|---|---|---|---|---|---|---|
| C1 | major | Rank-128 transport scope is ambiguous for hidden-16 messages | Section 3, `paper-data-figures.md:L25-L35` | Soundness | method/soundness | Enumerate tensors/layers/shapes/ranks and revise scope or rerun if the protocol is invalid | `ccf-paper-writer`; `experiment-plan` | +0.5 to +1 overall if resolved without changing results; no increase if rank validity is unresolved |
| C2 | major | Exact padded-bit ledger cannot be reconstructed | Section 3; raw bit fields | Reproducibility | reproducibility | Publish schema, bit decomposition, 2% denominator, rounding, and one matching scope | `ccf-paper-writer`; `experiment-plan` | +0.5 to +1 if auditable; re-run if raw encoding cannot be recovered |
| C3 | major | Raw selector controls are omitted and undefined | `confirmation-test-v2.json`; Section 4.2 | Evidence | experiment | Define `top_abs`, `random`, `uniform`, `a2q_node_budget`, `one_spike`; report all paired values | `ccf-paper-writer`; `ccf-paper-reviewer` | Existing data can +0.5; new ablation for causal mechanism |
| C4 | major | Validation selection history is incomplete | Section 4.1; `confirmation-summary.json:L19` | Reproducibility | reproducibility | List every validation-exposed candidate, selection rule, and test-access chronology | `ccf-paper-writer`; `experiment-plan` | Existing logs can repair; independent replication needs new experiment |
| C5 | major | Strongest-control and task-loss denominator are ambiguous | `confirmation-summary.json:L6-L17`; raw rows | Evidence | method/soundness | State comparator per dataset/metric/seed and recompute task loss from explicit formula | `ccf-paper-writer`; `ccf-paper-reviewer` | Existing rows can repair; formal bound needs new statistics |
| C6 | major | Conversion/Jacobian implementation is underspecified | Section 3; Section 4.1 | Soundness | reproducibility | Define adjacency, tensors, activation/rate coding, precision, tie-breaking, differentiated output, and selection granularity | `ccf-paper-writer` | Existing code/config can +0.5; missing implementation may require rerun |
| C7 | major | Fidelity gain lacks downstream utility or resource benefit | Sections 4.5–5 | Significance | experiment | Narrow to logit coding or add task/utility/energy evidence | `ccf-paper-writer`; `experiment-plan` | Wording can repair scope; utility requires new result |
| C8 | major | Timing boundary and p95 convention are unclear; focal 2% timing is absent | Section 4.5; `inputs/v2-timing.json` | Reproducibility | reproducibility | Define stages, synchronization, pairing, p95, memory reset; report focal-setting repeats if claimed | `experiment-plan`; `ccf-paper-writer` | Existing repeats can repair secondary claim; focal timing needs new benchmark |
| C9 | moderate | Per-seed values, absolute MSEs, and uncertainty displays are missing | Figures 2–4; raw JSON | Evidence | writing | Add per-seed tables/points, absolute means, SD convention, and paired differences | `ccf-paper-writer` | Existing results can +0.5 to evidence/clarity |
| C10 | moderate | “Bounded task loss” overstates a maximum observation | Abstract; Section 4.5 | Clarity | writing | Replace with “maximum observed degradation”; retain no-equivalence disclaimer | `ccf-paper-writer` | Existing wording fix; no experiment needed |
| C11 | moderate | Figure 3 chronology and Figure 4 condition key are easy to misread | Figure captions; `p9-evidence-digest.json:L213-L217` | Clarity | writing | Mark validation versus confirmation, split, budget, comparator, sample count, and memory panel explicitly | `ccf-paper-writer` | Existing figure source can fix |
| C12 | moderate | Novelty/related-work positioning is not closed | Section 2; digest `known_late_gate` | Originality | related-work | Complete 36-reference audit; compare sensitivity-guided compression and graph quantization precisely | `ccf-paper-reviewer`; `ccf-paper-writer` | Existing sources may repair; new baselines only if comparison is materially missing |
| C13 | minor | Terminology and statistical notation are inconsistent | Sections 3–4; Figure 2 caption | Clarity | writing | Standardize rank/budget labels, “ratio of three-seed means”, hidden-MSE denominator, and SD formula | `ccf-paper-writer` | Existing prose fix |
| C14 | minor | Artifact/environment/licensing provenance is not stated | Evidence digest and raw files | Ethics / limitations | reproducibility | Add code/config/data availability, hardware/software versions, and licensing boundary | `ccf-paper-writer` | Existing documentation can fix |

### Existing-evidence repairs

- Use `confirmation-test-v2.json` to publish the seven-mode comparison, all nine paired values, and the full-float reference distinction.
- Use raw `basis_bits`, `residual_target_bits`, `residual_payload_bits`, `residual_padded_bits`, `total_padded_bits`, and `coefficient_count` to make the bit ledger visible.
- Use `inputs/v2-summary.json` to show the budget grid, hidden-MSE sensitivity, and failed task-superiority gate.
- Use `inputs/v2-timing.json` to show all seven repeats, the exact nine p95 ratios, and peak-memory attribution.
- Use existing run/config artifacts, if present, to resolve layer/message scope, seed semantics, selector definitions, comparator rule, and validation history.

### Repairs requiring new experiments or new statistical evidence

- Independent replication or preregistered confirmation after validation exposure.
- Formal equivalence/non-inferiority evidence for task loss; more seeds or confidence intervals if a population claim is desired.
- Focal rank-128/2% runtime measurement if the headline resource claim is meant to apply to the headline setting.
- Downstream utility, calibration/distillation/transfer benefit, energy, or deployment evidence if the paper retains a broad GNN-to-SNN value claim.
- Jacobian interaction, curvature, leave-one-out, or ANN-versus-converted-output ablations if causal mechanism language remains.

## 12. AC / Meta-Review

Reviewer consensus: The empirical fidelity signal is credible within the tested static-graph scope, and the manuscript is appropriately cautious about negative task results and validation exposure.  
Reviewer disagreement: The main disagreement is whether the raw selector rows resolve the causal-isolation concern and how much to penalize the missing protocol metadata. The raw data supports a narrower selector comparison than the ARC reports acknowledge, but it does not make the method fully reproducible.  
Decisive acceptance axis: A fully specified, re-computable matched-budget protocol plus a sharply scoped contribution centered on logit fidelity could move the paper into borderline-positive territory.  
Decisive rejection axis: If the rank/message ambiguity, comparator definition, and validation-selection history remain unresolved, a skeptical reviewer can reject the central claim as unauditable. Broad practical claims would also be rejected because task superiority and energy evidence are absent.  
AC stance: `Weak reject / borderline negative`, with `major revision` required before resubmission.  
Discussion risks: Reviewers may conflate the raw `top_abs` control with a formally defined magnitude baseline; may interpret maximum observed task degradation as a bound; may treat the full-float `none` row as a matched baseline; and may question whether rank 128 is meaningful for hidden width 16.

## 13. Quantitative Scores

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|---|---:|---:|---|---|
| Novelty | 3 | 3 | Method section; related-work section; public candidates | Incremental positioning risk and pending citation audit. +1 only if closest sensitivity/quantization work is differentiated precisely; do not award broad novelty from current text. |
| Soundness | 3 | 4 | Sections 3–4; raw rows | Rank/message ambiguity, Jacobian definition, comparator semantics, and interaction assumptions. +1 if those are resolved from existing artifacts; lower if rank validity is contradicted. |
| Evidence | 3 | 4 | Confirmation, validation-grid, timing JSON; Figures 2–4 | Strong focal logit direction but missing per-seed display, task denominator, and utility. +0.5–1 from existing-data presentation; stronger evidence needs new runs. |
| Significance | 2 | 4 | Sections 4.5–5 | Narrow logit-fidelity value, mixed task outcomes, no energy or downstream benefit. Repair by narrowing claims or adding new utility evidence. |
| Clarity | 3 | 4 | Frozen manuscript and ARC reviews | Scope language is good, but central definitions and result aggregation are hidden. Existing writing/table edits can raise this. |
| Reproducibility | 2 | 4 | Raw JSON schemas; method/experiment text | Raw fields are useful but not connected to complete implementation and ledger definitions. Existing code/config can repair; otherwise re-run is required. |
| Ethics / Limitations | 4 | 4 | Abstract, Discussion, evidence digest | Honest limitations and no apparent human-data risk. Add artifact/licensing/environment provenance. |

Quality: 3/5  
Clarity: 3/5  
Significance: 2/5  
Originality: 3/5  
Soundness: 3/5  
Evidence: 3/5  
Reproducibility: 2/5  
Ethics / Limitations: 4/5  
Overall: 5/10  
Confidence: 4/5  
Score-change conditions: `+1` overall is plausible after the protocol, comparator, and validation-history repairs plus per-seed/raw-data presentation; `+2` would require either independently replicated evidence or a clearly demonstrated downstream/resource benefit. A score below 4 would be triggered by evidence that the rank/message protocol is invalid, that the test split influenced selection, or that the matched-cost controls were not implemented comparably.

## 14. Questions For Authors

1. Which exact tensor is transported and compressed: `AX`, `AH^(1)`, both layers, or another message? What are the tensor shapes and valid ranks?
2. What exactly does the 2% residual budget count: residual entries, total message entries, or serialized bits? What rounding rule is used?
3. What are the record schema, index widths, numeric formats, padding/alignment rules, and included basis/metadata costs?
4. Are `top_abs`, `random`, and `uniform` in `confirmation-test-v2.json` residual-magnitude, random, and non-output-aware selectors? How are ties and coefficient indices defined?
5. Is `top_abs` the comparator used for every task-loss number? If not, what is the exact task-loss formula and comparator-per-metric rule?
6. Are 0/1/2 checkpoint seeds only, or do they also change splits, initialization, or rate-code randomness?
7. Which model is differentiated for `J_i`: the frozen ANN, the rate-coded converted model at T=2/4, or another output?
8. Was the test split accessed exactly once after the focal setting and reframing were frozen? Where is the complete validation candidate ledger?
9. What stages are included in full-pipeline timing, how are CUDA synchronization and host-device transfers handled, and what does p95 mean with seven repeats?
10. What downstream use makes lower logit MSE valuable enough to accept mixed task outcomes and nonzero runtime overhead?

## 15. Score Revision Criteria

Raising the score would require:

- A complete, re-computable serialized-bit ledger and one consistent matching scope.
- Explicit tensor/layer/rank definitions and a clear statement of what is compressed.
- Definitions and paired results for all raw selector controls, including what `top_abs`, `random`, and `uniform` implement.
- A complete validation-selection and test-access chronology.
- A precise task-loss formula with comparator identity, metric set, and aggregation order.
- Per-seed values, absolute MSEs, sample-SD convention, and raw timing repeats in the manuscript or an auditable supplement.
- Either a sharply narrowed logit-fidelity claim or new downstream/resource evidence.
- A completed related-work/citation audit with exact novelty positioning.

Lowering the score would be triggered by:

- Evidence that rank 128 is invalid for the actually compressed message.
- Evidence that the test split or test outcomes selected the comparator or focal setting.
- Evidence that matched controls use materially different serialization rules or budget denominators.
- Evidence that reported task loss excludes metrics claimed in the abstract.
- Evidence that the raw controls are not the stated selectors or that implementation details cannot be recovered.

Concerns unlikely to change before submission:

- No independent replication exists.
- No formal task-equivalence claim exists.
- No energy or broad GNN-generality evidence exists.
- The scope remains limited to frozen two-layer hidden-16 GCN checkpoints on three static graphs unless new experiments are added.

## 16. Action Plan And CCFA Handoffs

Priority: P0  
Action: Resolve tensor/layer/rank and serialization schema from existing implementation/configuration; revise the method text without changing results.  
Owner skill: `ccf-paper-writer`  
Input needed: code/config, tensor shapes, serialization implementation  
Expected output: exact transport scope, 2% denominator, and per-method bit ledger  
Handoff required: yes

Priority: P0  
Action: Rebuild the comparator and task-loss table from raw JSON using one explicit formula; label `top_abs`, `random`, `uniform`, adapted controls, and the full-float reference.  
Owner skill: `ccf-paper-writer`  
Input needed: `confirmation-test-v2.json`, `confirmation-summary.json`  
Expected output: per-seed/per-metric table and corrected “maximum observed degradation” wording  
Handoff required: yes

Priority: P0  
Action: Document validation candidate exposure, selection rule, and test-access chronology.  
Owner skill: `ccf-paper-writer`  
Input needed: run logs/configuration and validation outputs  
Expected output: auditable post-selection confirmation statement  
Handoff required: yes

Priority: P1  
Action: Add selector definitions and all paired raw-control results; add interaction or leave-one-out ablation only if the authors retain causal mechanism language.  
Owner skill: `ccf-paper-writer`; `experiment-plan`  
Input needed: selector implementation; optional new ablation run  
Expected output: mechanism claim scoped to what the evidence shows  
Handoff required: partly

Priority: P1  
Action: Tighten Figures 2–4, terminology, hidden-MSE formula, SD convention, and timing boundary.  
Owner skill: `ccf-paper-writer`  
Input needed: figure source CSV/plots and timing JSON  
Expected output: reviewer-readable captions and reproducible statistics  
Handoff required: yes

Priority: P1  
Action: Complete the 36-reference authenticity/relevance/placement/duplicate audit and position the work against sensitivity-guided compression and graph quantization.  
Owner skill: `ccf-paper-reviewer`; `ccf-paper-writer`  
Input needed: bibliography/source files and verified public sources  
Expected output: exact novelty delta without invented citations  
Handoff required: yes

Priority: P2  
Action: Decide whether to narrow the paper to logit-fidelity coding or run new downstream, energy, focal-runtime, broader-model, or independent-replication experiments.  
Owner skill: `experiment-plan`; `ccf-paper-writer`  
Input needed: author decision and compute budget  
Expected output: either a narrow, defensible contribution or a stronger evidence package  
Handoff required: yes

Checks run:

- Read the frozen manuscript, evidence digest, both ARC reviews, confirmation summary, confirmation rows, validation summary, and timing rows.
- Verified the SHA256 values of the four raw evidence inputs cited in the digest.
- Recomputed matched-bit totals, selector-control coverage, nine paired fidelity directions, task-loss alternatives, and timing p95 ratios from the supplied JSON.
- Ran a public-safe related-work search for positioning candidates; treated non-official results as unverified.
- Did not edit the manuscript, run experiments, or invent citations/results.

Checks skipped:

- PDF/page/template/anonymity check because no compiled PDF or venue guide was supplied.
- Code-level execution and independent result reproduction, per the request not to run experiments.
- Full bibliography authenticity audit, which remains the scheduled P12 gate.

Unresolved risks:

- The actual compressed tensor and rank validity.
- The 2% denominator and complete serialized-cost schema.
- The exact task-loss comparator and metric aggregation.
- Validation selection multiplicity and test-access chronology.
- Selector-control definitions and mechanism attribution.
- Timing stage boundaries and focal 2% runtime.
- Novelty positioning and downstream utility.

Recommended next CCFA owner: `ccf-paper-writer` for P0 documentation/claim repairs, followed by `experiment-plan` only for evidence that cannot be recovered from existing artifacts.
