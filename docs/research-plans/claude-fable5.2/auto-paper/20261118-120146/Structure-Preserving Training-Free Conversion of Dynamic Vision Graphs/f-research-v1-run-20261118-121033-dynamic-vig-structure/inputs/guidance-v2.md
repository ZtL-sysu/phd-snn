# Research Guidance File

## Title / Topic

- Working title: Message-Exact Low-Step Conversion for Dynamic Vision Graphs
- Target field: training-free ANN-to-SNN conversion, graph neural networks, efficient visual inference.
- Target journal tier: top conference; no downgrade after failure.
- Candidate venues: CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR.
- Technique/method: signed residual-rate coding whose objective is exact preservation of Grapher messages at matched low-step cost.
- Selected application scenario: the same license-clear Fashion-MNIST/MNIST dynamic Grapher benchmark; local exposed data remain diagnostic only.

## Core Idea

Version 1 showed that preserving neighbor indices and max-winner indices is insufficient: calibrated conversion still trailed the teacher by 33.37 pp, while replacing encoded features with teacher features recovered all but 0.62 pp. Version 2 therefore changes the mechanism rather than the target: allocate signed multilevel pulses so that the aggregated message tensor, not merely discrete decisions, is reconstructed with minimal error at the same event budget.

### Mechanism-Level Rationale

- Domain bottleneck: the Grapher output depends on the signed messages `ReLU(m_ij - m_i)`, so index agreement can coexist with large magnitude error.
- Why the chosen technique fits: a message-aware calibration directly minimizes the tensor that feeds the remaining layers.
- What must be changed or adapted: replace scale-only calibration with a per-layer/per-channel offset-and-step search using training data, and report exact message error.
- Why this is more than applying method X to dataset Y: the target quantity is the graph message tensor under a fixed dynamic topology, with causal controls that separate index, winner, and magnitude errors.
- Central scientific question: can message-exact low-step coding close most of the teacher gap at matched events?
- Intended reader: conversion and graph-learning researchers seeking low-latency event-efficient Grapher inference.
- Domain/theory problem → design requirement → candidate method choice: magnitude error dominates after v1 → calibrate the full message tensor → signed residual-rate coding with message loss.
- Expected contribution type: method plus failure analysis distinguishing structure and magnitude errors.

## Paper Story

- Opening problem: low-step graph conversion can look structurally correct yet fail badly at task level.
- Why existing work is insufficient: prior conversion metrics emphasize activation MSE or accuracy; v1 evidence shows discrete structure metrics alone are misleading.
- Core insight: convert the quantity that propagates through the graph—the signed aggregated message—not just activations or topology.
- What evidence should convince the reader: message error, accuracy gap, matched events, and ablations separating scale, offset, neighbor, and winner factors.
- Planned claim (not an observed finding): message-aware calibration reduces teacher gap by at least 50% compared with activation/scale calibration at matched events.
- Finding to assess after experiments: unresolved_until_evidence.
- Main claim: message-level fidelity is the operative bottleneck in low-step dynamic graph conversion.
- Boundary of the claim: small patch-grid dynamic Graphers on Fashion-MNIST/MNIST; no neuromorphic-energy claim.
- Skeptical-reviewer hook: v1 already showed teacher-feature oracle succeeds; v2 must show a deployable coding method approaches that oracle without teacher features.
- Strongest competing paper and why this is still distinct: DCGS remains the strongest training-free conversion family but has no graph-message objective.

## Paper Outline

1. Introduction: motivate message fidelity after showing structure-only preservation fails.
2. Related Work: conversion, graph SNN, dynamic vision graphs, message/structure preservation, event-cost accounting.
3. Method: define signed residual-rate coding, message-aware calibration, matched event ledger, and diagnostic ablations.
4. Experiments and Results: report baseline, v1 scale calibration, v2 message calibration, oracles, seeds, and message/accuracy/event metrics.
5. Discussion: interpret why structure metrics were insufficient, scope boundaries, negative results, and threats.
6. Conclusion: summarize only evidence-supported conclusions.

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| Fashion-MNIST | `https://huggingface.co/datasets/zalando-datasets/fashion_mnist/tree/main/fashion_mnist` | MIT | Binding final-test route | 60,000 train and 10,000 test | 10 classes | Official split; 5,000 train calibration; validation subset separate | direct-public |
| MNIST | `https://huggingface.co/datasets/ylecun/mnist/tree/main/mnist` | MIT | Robustness route | 60,000 train and 10,000 test | 10 classes | Same isolation policy | direct-public |
| Local superpixel graphs | `C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\data\pyg_bench` | Local MIT benchmark record | Historical diagnostic only | 4.38 GB | 10 classes | Official but historically exposed | local-diagnostic |

### Baselines

- Simple baseline: unsigned uniform coding.
- Matched internal baseline: v1 signed scale calibration with 16 levels.
- Strong conversion baseline: independently reimplemented DCGS-family signed multilevel coding.
- Domain baseline: locally trained dynamic Grapher teacher.
- Method: v2 message-aware offset/step calibration at matched levels.
- Oracle: teacher features with converted indices/winners, teacher indices only, teacher winners only, and both.
- Upper reference: unconstrained real-valued teacher features.

### Proposed Method Variants

- Main method: per-layer scale and offset calibration minimizing message MSE on train/calibration data.
- Variant A: scale-only calibration (v1 control).
- Variant B: message MSE calibration without offset.
- Variant C: message MSE plus structure disagreement regularization.
- Implementation notes: all coding parameters are fit on train/calibration only; final test remains frozen; all trials logged.

### Metrics

- Primary metric: teacher-student top-1 accuracy gap at matched events.
- Secondary metrics: message MSE, neighbor Jaccard, winner agreement, logit MSE, seed SD.
- Efficiency metrics: graded events per tensor and wall-clock latency.
- Statistical test / confidence reporting: all seeds, means, SD, paired differences, descriptive bootstrap intervals.

### Required Ablations

- Scale-only versus message-aware calibration.
- Offset disabled versus enabled.
- Structure regularization disabled versus enabled.
- Teacher neighbor/winner/both oracle controls.
- Robustness across T/level budgets and three seeds.

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Windows 11; `C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`; PyTorch 2.11.0+cu128.
- Optional remote fallback: none.
- GPU/CPU: RTX 3060 12 GB; 12 logical CPUs.
- RAM: record actual process observations; no value exposed by privacy-safe probe.
- Disk: about 481 GiB free at builder probe.
- Max runtime per run: 4 hours.
- Max total runs: 24 hours and 12 new search trials after v1 failure.
- Frozen train/validation/test identifiers: official splits; test frozen before v2 calibration.
- Full search/trial ledger: preserve v1 and all v2 trials.
- CCFA packet path and feasibility-contract.json: `ccfa-startup-packet/`.
- Resource exhaustion and next-candidate decision: if message-aware calibration fails, create v3 for streaming-graph delta inference; do not lower target.
- Scaling fallback: smaller level set and fewer calibration blocks.
- Stopping criteria: non-finite values, target failure with exhausted budget, or test exposure.

## Expected Results

- Minimum acceptable result: message MSE decreases on calibration data and all seeds complete.
- Strong result: reduce the v1 mean teacher gap from 33.37 pp to below 16.69 pp (at least 50% closure) at event count no higher than v1, with message MSE lower than scale-only calibration and no seed worse by more than 3 pp.
- Failure signal: gap closure below 25%, event count increases, or message MSE not lower than scale-only control.
- What to do if minimum is not reached: repair implementation and rerun earliest affected stage; no drafting.
- Claim adjustment rule: only a versioned replacement contract with a genuinely different mechanism may replace the target.

## Figure/Table Decision Rules
Do not lock final visuals before evidence stabilizes.

- Required first figure type: GPT-generated framework figure after v2 method is frozen.
- Required experiment visualizations if supported by data: accuracy gap versus events, message MSE versus teacher gap, and oracle decomposition.
- Required result tables if supported by data: v1 versus v2 matched-event table and full seed/ablation table.
- Author or venue figure/table requirements: none supplied.
- Evidence that may benefit from a visual: failure transition from structure-only to message-aware mechanism.
- Rules for excluding weak or misleading plots: omit plots with unlogged trials, undefined metrics, or implied hardware energy not measured.
- Scientific claims aided by visuals: message-fidelity mechanism and matched-event trade-off.
- Final count and placement are chosen after evidence stabilizes; no per-subsection quota applies.

## Traceability Checklist

| Requirement | Dataset | Baseline/method/ablation | Metric | Expected result | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|---|
| Message-aware method | Fashion-MNIST/MNIST | v2 calibration | Teacher gap, message MSE | >=50% gap closure | Figure 1 and Table 1 | yes |
| v1 control | Same split | Scale-only calibration | Same metrics | v2 strictly better at matched events | Table 1 | yes |
| Strong coding baseline | Same split | DCGS-family multilevel | Same metrics | v2 not worse at equal events | Table 1 | yes |
| Oracle attribution | Same split | Teacher neighbor/winner/both | Accuracy | Decompose residual | Figure 2 | yes |
| Seeds and robustness | Same split | Three seeds and level budgets | All metrics | Full distribution | Table 2 | yes |

## Citation Scope

- Must-cite foundational papers: early conversion, QCFS, calibration, ViG, DGCNN, SpikingGCN.
- Must-cite recent papers: DCGS, One-Spike, PMSM, point-cloud conversion, SpikeZIP-TF, STA, DeltaCNN, AEGNN, InkStream/RIPPLE, and SNN-vs-quantized analyses.
- Dataset papers: Fashion-MNIST, MNIST, benchmarking-gnns for historical diagnostics.
- Search keywords: message-preserving SNN conversion, graph signal reconstruction, dynamic vision graph conversion, training-free SNN, event budget.
- Target recency: last 3-5 years plus foundational works.
- Excluded areas: unrelated databases, private data, unmeasured energy claims.
- Reference scope/coverage: relevant conversion/graph/cluster only.
- Recency expectation/source: top-conference review and builder contract.

## Novelty And Feasibility Summary

- Literature/baseline map verdict: pass.
- Dataset access verdict: pass.
- Task/evaluation verdict: pass.
- Theoretical fit verdict: pass after v1 failure localized magnitude error.
- Novelty verdict: pass in bounded search; final recheck required.
- Hardware feasibility verdict: pass.
- Baseline/ablation verdict: pass.
- Effectiveness plausibility verdict: pass as pre-registration; no result claimed.
- Q2+ story verdict: pass conditional on strong evidence.

## Theoretical Feasibility Audit

- Mechanism expected to help: message tensor is the propagated quantity; reducing its error should reduce downstream task loss.
- Required assumptions: message MSE correlates with accuracy and calibration transfers.
- Supporting literature: conversion error calibration and v1 oracle evidence.
- Falsifying ablation: scale-only control matches v2 or message MSE decreases without accuracy recovery.
- Critical failure mode: integer coding resolution leaves irreducible magnitude error.

## Story Strength Audit

- Why a reviewer should care: v1 provides a concrete failure mode where structure looks preserved but accuracy collapses.
- Strongest incrementality threat: message MSE is a standard objective; distinctness requires graph-message formulation and causal decomposition.
- Decisive distinguishing experiment: matched-event v1 versus v2 and oracle decomposition.
- Strong-paper threshold: at least 50% teacher-gap closure at no higher event cost.
- Honest fallback: create v3 for streaming-graph delta inference; do not downgrade.

## Constraints and Preferences

- Writing preference/source: formal top-conference English; no workflow narration in manuscript.
- Protected sections: six canonical sections.
- Journal page/word/figure requirements: none supplied; verify at P20.
- Things to do: preserve v1 failure, baseline-first for v2, strong-result lock before writing.
- Things to avoid: lowering failed targets, unlicensed code, exposed-test tuning, commits/push/submission.
- Preferred writing language: English manuscript; Chinese progress communication.
- Preferred LaTeX/template: deferred.

