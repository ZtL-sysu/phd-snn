# Research Guidance File

## Title / Topic

- Working title: Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs
- Target field: training-free ANN-to-SNN conversion, graph neural networks, event-efficient visual inference.
- Target journal tier: top conference; do not downgrade the target tier to make a failed idea pass.
- Candidate venues: CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR. Exact venue formatting is deferred until the evidence package is frozen.
- Technique/method: signed multi-threshold differential coding with calibration that preserves dynamic neighbor selection and signed max-aggregation winners.
- Selected application scenario: a small ViG-style dynamic-kNN/max Grapher on a directly public, license-clear image benchmark, with local superpixel graph data as a diagnostic resource.

## Core Idea

Convert a trained dynamic vision graph without changing its weights by encoding each layer's continuous activations with a signed graded-pulse code, then calibrate coding parameters to minimize disagreement in the graph's discrete decisions: the k-nearest-neighbor set and the signed max-aggregation winner. The hypothesis is that activation fidelity alone is insufficient because small numeric errors cross discrete margins; preserving those decisions should recover conversion accuracy at matched event cost.

### Mechanism-Level Rationale

- Domain bottleneck: ViG-style Grapher blocks recompute kNN from features and max-aggregate signed neighbor-minus-center messages. Both operations convert small coding errors into discrete topology or winner changes.
- Why the chosen technique fits: signed multi-threshold coding supports negative values and low time steps; a structure-aware calibration loss directly targets neighbor and winner margins instead of only activation MSE.
- What must be changed or adapted: implement graph kNN and signed max outside the current DCGS CNN/Transformer code; reimplement algorithms rather than copy unlicensed upstream source; add diagnostic oracles that temporarily supply teacher neighbor indices and winners.
- Why this is more than applying method X to dataset Y: the contribution concerns discrete decision preservation in dynamic topology, with causal interventions that distinguish structure errors from generic quantization error.
- Central scientific question: can a training-free conversion preserve discrete graph structure at matched event cost and thereby recover task fidelity?
- Intended reader: researchers working on ANN-to-SNN conversion, graph neural networks, and efficient visual inference who need low-step conversion beyond fixed graphs.
- Domain/theory problem → design requirement → candidate method choice: dynamic kNN plus signed max creates margin-sensitive discrete errors → calibration must measure structure disagreement → use structure-aware signed multi-threshold coding.
- Expected contribution type: method plus mechanism diagnosis and resource-cost trade-off.

## Paper Story

- Opening problem: training-free conversion has reached low time steps on CNNs and Transformers, but visual graph models that rebuild neighbors per layer still lack a conversion method that keeps their discrete operators intact.
- Why existing work is insufficient: One-Spike/PMSM-style graph conversion uses fixed graphs or specially trained sources; point-cloud conversion replaces max pooling and retrains; DCGS has no graph operators; SpikingGCN/Spiking PointNet are direct-training routes.
- Core insight: improve the discrete decisions that define the graph, not merely the continuous activation error.
- What evidence should convince the reader: structure-disagreement measurements at T<=4, matched-event comparisons against strong conversion baselines, and teacher-neighbor/winner interventions showing that structure preservation explains accuracy recovery.
- Planned claim (not an observed finding): structure-aware calibration reduces neighbor/winner disagreement and task loss at matched event cost.
- Finding to assess after experiments: unresolved_until_evidence.
- Main claim: discrete structure preservation is the mechanism that enables low-step training-free conversion of dynamic vision graphs.
- Boundary of the claim: local dynamic Grapher on license-clear image benchmarks; no claim of general neuromorphic energy superiority or untested backbone universality.
- Skeptical-reviewer hook: DCGS may already make errors small enough that structure is naturally stable; the decisive evidence is a measured baseline failure plus oracle recovery.
- Strongest competing paper and why this is still distinct: DCGS (2025) is the strongest low-step training-free conversion family, but it is CNN/Transformer-only and has no graph-structure objective.

## Paper Outline

1. Introduction: motivate low-step training-free conversion for dynamic visual graphs; state the discrete-decision bottleneck and the structure-preservation hypothesis.
2. Related Work: separate ANN-to-SNN conversion, graph conversion, visual graph backbones, incremental/event-driven inference, and energy accounting; position against DCGS, One-Spike, PMSM, point-cloud conversion, and direct-trained spiking graph models.
3. Method: define the dynamic Grapher, signed multi-threshold encoder, structure-disagreement calibration objective, event ledger, and diagnostic oracle variants.
4. Experiments and Results: describe datasets, frozen splits, baselines, ablations, seeds, and report structure, accuracy, event-count, and latency evidence around research questions rather than an inventory of table cells.
5. Discussion: interpret mechanism support, scope conditions, local-resource boundaries, negative results, and threats to validity without turning into a workflow log.
6. Conclusion: summarize the supported claim and the next scientific question; do not add appendices or research content after the conclusion.

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| Fashion-MNIST | `https://huggingface.co/datasets/zalando-datasets/fashion_mnist/tree/main/fashion_mnist` | MIT dataset card | Binding final-test route | Train parquet 30,931,277 bytes; test parquet 5,175,617 bytes | 10 apparel classes, 60,000 train and 10,000 test | Official train/test; fixed 5,000 calibration subset from train; validation subset from remaining train | direct-public |
| MNIST | `https://huggingface.co/datasets/ylecun/mnist/tree/main/mnist` | MIT dataset card | License-clear fallback and robustness route | Train parquet 15,561,616 bytes; test parquet 2,595,890 bytes | 10 digit classes, 60,000 train and 10,000 test | Same isolation policy as Fashion-MNIST | direct-public |
| Local SuperPixel MNIST/CIFAR10 graphs | `C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\data\pyg_bench` | Local MIT benchmark source/license record | Prototype and historically-exposed diagnostic only | 12 files, 4,380,659,876 bytes; MNIST 55k/5k/10k and CIFAR10 45k/5k/10k graph splits | 10 classes | Existing official splits, but test explicitly historically exposed | local-diagnostic |
| CIFAR-10 mirror | `https://huggingface.co/datasets/uoft-cs/cifar10/tree/main/plain_text` | `license: unknown`; no explicit research-use license found | Rejected for binding claims | 119,705,255 train and 23,940,850 test bytes | 10 classes | Not used | rejected |

### Baselines

- Simple baseline: unsigned rate or uniform coding at matched nominal levels.
- Matched internal baseline: signed uniform quantization with the same levels and event budget.
- Domain-standard baseline to rerun/adapt: locally trained small ViG-style dynamic-kNN/max Grapher teacher on a license-clear benchmark.
- Strong recent baseline to rerun/adapt: independently reimplemented signed multi-threshold differential coding from the published DCGS algorithm; upstream repository has no detected license and is not copied.
- Strong recent baseline for literature context only: training-free Transformer conversion and point-cloud conversion results that cannot be directly rerun in this local envelope.
- Technique-family baseline: multi-threshold signed coding without structure-aware calibration.
- Upper-bound or oracle-style comparison: teacher-neighbor-only, teacher-winner-only, and both-oracle diagnostic interventions; not deployable methods.
- Strongest expected comparison: proposed structure-aware signed coding versus DCGS-family coding at matched events and T<=4.

### Proposed Method Variants

- Main method: signed multi-threshold coding with joint neighbor-Jaccard and winner-agreement calibration.
- Variant A: activation-MSE calibration only, controlling parameter count.
- Variant B: neighbor-only structure calibration, isolating the topology term.
- Variant C: winner-only structure calibration, isolating the signed max term.
- Implementation notes: use the Conda environment `C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`; implement Grapher and coding operators independently; preserve all configs, seeds, hashes, and failed runs in the f-research-v1 run root.

### Metrics

- Primary metric: layerwise neighbor-set Jaccard and channelwise signed-max winner agreement versus teacher.
- Secondary metrics: top-1 accuracy, teacher-student logit agreement, accuracy recovery under oracle interventions.
- Efficiency metrics: graded events per scalar, exact quantized-level counts, warmed CPU/GPU latency, and peak memory.
- Statistical test / confidence reporting: report all seeds, means, sample SD, paired example/seed differences, and descriptive bootstrap intervals; do not claim unadjusted significance.

### Required Ablations

- Ablation 1: replace quantized features with teacher features; structure disagreement must vanish.
- Ablation 2: activation-MSE calibration versus structure calibration at equal parameters/events.
- Ablation 3: teacher-neighbor only, teacher-winner only, both, and random-neighbor control.
- Robustness or subgroup analysis: T in {2,4,8}, multiple seeds, and layers grouped by k/k+1 distance margin.
- Error analysis: report cases where accuracy changes without neighbor/winner disagreement and cases where structure flips without task loss.

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Windows 11; `C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`; Python 3.13.13; PyTorch 2.11.0+cu128.
- Optional remote fallback, only if authorized: none.
- GPU/CPU: NVIDIA GeForce RTX 3060 12 GB; 12 logical CPUs.
- RAM: OS value not exposed by the privacy-safe probe; local runtime must be logged from actual process observations.
- Disk: about 481 GiB free at probe time.
- Max runtime per run: 4 hours.
- Max total runs: 24 hours and 12 search trials for the first contract.
- Frozen train/validation/test identifiers and validation-only selection policy: official benchmark splits; calibration and validation drawn only from train; test frozen before final selection; index SHA-256 recorded.
- Full search/trial ledger and held-out test isolation: every trial logged; any test used for design is marked exposed and requires a fresh holdout or versioned replacement contract.
- CCFA packet path and feasibility-contract.json: `ccfa-startup-packet/` beside this guidance file.
- Resource budget exhaustion and next-candidate decision rule: preserve evidence, classify the blocker, and activate the authorized streaming-graph rescue route only through a versioned replacement contract.
- Scaling fallback: smaller Grapher, fewer layers, fixed 64-sample smoke prototype, then full seed campaign only if the prototype passes.
- Stopping criteria: stop a campaign on invalid oracle equivalence, non-finite values, unresolved strong-baseline gap, exposed-test redesign, or budget exhaustion without new evidence.

## Expected Results

- Minimum acceptable result: measurable neighbor/winner disagreement under the strong conversion baseline and a valid oracle intervention with finite, reproducible metrics.
- Strong result: at T<=4, the conversion baseline loses at least 5 pp neighbor Jaccard or 2 pp winner agreement; structure-aware calibration recovers at least 50% of that disagreement loss at matched events with at most 1 pp teacher accuracy gap; the method recovers at least half of both-oracle accuracy recovery.
- Failure signal: less than 1% structure disagreement and less than 1 pp accuracy gap at T=4, no oracle effect, method gains when structure is unchanged, or recovery only with a deployable teacher oracle.
- What to do if minimum is not reached: open the correction loop, repair implementation/baseline/data issues, and rerun the earliest affected stage; do not write the paper.
- Claim adjustment rule if expectations fail: only a versioned replacement contract with a genuinely different mechanism or scenario may replace the failed target; do not lower the same target to pass.

## Figure/Table Decision Rules
Do not lock final figure/table contents before experiments are completed.

- Required first figure type: GPT-generated framework/architecture figure after the method is finalized.
- Required experiment visualizations if supported by data: structure disagreement versus T/events; margin-stratified neighbor/winner flips; oracle recovery bars with seed dispersion.
- Required result tables if supported by data: matched-event baseline comparison, full seed table, and ablation/intervention matrix.
- Author or venue figure/table requirements, with source: none supplied by the user; venue-specific requirements must be checked at P20.
- Evidence that may benefit from a visual: the causal chain from coding error to discrete flip to accuracy recovery.
- Rules for excluding weak or misleading plots: omit plots whose seed intervals overlap decisively, whose metric is not defined in the contract, or that imply hardware energy not measured.
- Scientific claims for which a figure/table would aid inspection: discrete structure preservation, matched-event trade-off, and oracle attribution.
- Final count and placement are chosen after evidence stabilizes; no per-subsection quota applies.

## Traceability Checklist

| Requirement | Dataset | Baseline/method/ablation | Metric | Expected result | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|---|
| Public license-clear data | Fashion-MNIST, MNIST | Data loading and splits | Counts, labels, split hashes | Direct access and MIT terms verified | Table 1 setup | yes |
| Dynamic teacher reproduction | Fashion-MNIST or MNIST patches | ViG-style kNN/max Grapher | Teacher accuracy and finite activations | Reproducible teacher within budget | Figure 1 framework | yes |
| Strong conversion baseline | Fashion-MNIST or MNIST | DCGS-family signed multi-threshold reimplementation | Neighbor Jaccard, winner agreement, accuracy, events | Baseline disagreement threshold | Table 2 baseline comparison | yes |
| Matched control | Same split | Signed uniform quantization at same levels | Same metrics | No higher event budget | Table 2 | yes |
| Structure calibration | Same split | MSE-only vs neighbor/winner calibration | Disagreement recovery, accuracy, events | At least 50% recovery | Figure 2 disagreement vs T/events | yes |
| Causal interventions | Same split | Teacher features, neighbor oracle, winner oracle, both, random control | Accuracy recovery and structure agreement | Method recovers at least half of oracle gain | Figure 3 oracle recovery | yes |
| Robustness | Same split | T={2,4,8}, 3 seeds, margin strata | All primary/secondary metrics | Full distribution reported | Table 3 seed/ablation matrix | yes |
| Historical local diagnostic | Local superpixel graphs | Existing fixed-graph GatedGCN metadata | Diagnostic accuracy only | Clearly labeled historically exposed | Optional diagnostic table | no |

## Citation Scope

- Must-cite foundational papers: Cao/Diehl early conversion, Rueckauer SNN toolbox, QCFS, SNN calibration, ViG, DGCNN, SpikingGCN.
- Must-cite recent papers: DCGS 2025, One-Spike SNN, PMSM, point-cloud conversion, SpikeZIP-TF, STA, AEGNN, DeltaCNN, InkStream/RIPPLE family, and recent SNN-vs-quantized energy analyses.
- Dataset papers: Fashion-MNIST, MNIST, Krizhevsky CIFAR-10 report when discussing rejected local data, and the benchmarking-gnns source for local diagnostic data.
- Baseline papers: DCGS, ViG, One-Spike, PMSM, Lan et al. point-cloud conversion, GatedGCN benchmarking source.
- Search keywords: training-free ANN-to-SNN conversion, dynamic graph conversion, signed max aggregation, kNN flip, visual graph SNN, delta graph inference, quantized GNN energy.
- Target recency: prioritize the last 3-5 years while retaining foundational conversion and graph papers.
- Excluded areas: finance/bio databases unrelated to the project, private-data studies, and hardware-only claims without measured prototypes.
- Reference scope/coverage appropriate to the question and venue: cover the three relevant clusters without padding to a fixed count.
- Recency expectation and its source: top-conference review expectations plus the explicit f-guidance-builder requirement for recent authoritative baselines.

## Novelty And Feasibility Summary

- Literature/baseline map verdict: pass; DCGS and ViG are primary verified anchors, graph conversion attempts are separated.
- Dataset access verdict: pass for Fashion-MNIST/MNIST; CIFAR-10 rejected for unknown license; local superpixel data diagnostic only.
- Task/evaluation verdict: pass with frozen splits, primary/secondary metrics, and exposure rules.
- Theoretical fit verdict: pass with margin-based discrete-decision mechanism and three falsifiers.
- Novelty verdict: pass in bounded searches; final paper-stage novelty recheck mandatory.
- Hardware feasibility verdict: pass on local RTX 3060 with scaled small Grapher.
- Baseline/ablation verdict: pass; simple, strong, domain, matched, and oracle controls are planned.
- Effectiveness plausibility verdict: pass as pre-registration; no result is claimed before experiments.
- Q2+ story verdict: pass conditional on observed strong evidence before drafting.

## Theoretical Feasibility Audit

- Mechanism expected to help: structure-aware calibration preserves kNN and signed max decisions under coding error.
- Required assumptions: a dynamic Grapher teacher exists; margin-sensitive flips are measurable; calibration transfers from train to held-out data.
- Supporting literature: ViG primary record, DCGS primary record, separately audited imported graph-conversion evidence, and elementary distance/max margin bounds.
- Falsifying ablation: teacher-feature restoration must remove disagreement; MSE calibration must not match structure calibration; both-oracle must explain accuracy recovery.
- Critical failure mode: near-perfect baseline agreement at T<=4 removes the method story; the run must then pivot under a versioned replacement contract.

## Story Strength Audit

- Why a top-conference reviewer should care: training-free graph conversion fails at discrete operators that prior conversion metrics ignore.
- Strongest incrementality threat: DCGS already solves low-step conversion and makes graph decisions naturally stable.
- Decisive distinguishing experiment: matched-event structure disagreement plus teacher-neighbor/winner causal interventions.
- Strong-paper result threshold: >=50% structure-disagreement recovery and at least half of oracle accuracy recovery with <=1 pp teacher gap at matched events.
- Honest fallback story if only partially successful: report the negative diagnostic and activate the streaming-graph or fair-energy replacement; do not downgrade the claim.

## Constraints and Preferences

- Writing preference/source: formal top-conference scientific prose; strict six-section body; user requires no downgrade after failed ideas.
- Protected sections or edit scope/source: six required top-level sections; no workflow logs in the manuscript; protected scope from `f-research-v1` and user goal.
- Journal page/word/figure requirements and source: none supplied; check at P20 before final compilation.
- Things the workflow must do: baseline-first execution, preserve failures, verify all claims, lock strong result before drafting, verify citations and duplicates, compile PDF and source package.
- Things the workflow must avoid: unlicensed code copying, inaccessible data, invented results, test-set tuning, remote execution without authorization, commits/pushes/submission.
- Preferred writing language: English manuscript; Chinese progress communication.
- Preferred LaTeX/template/venue style: deferred until the exact venue is selected.

