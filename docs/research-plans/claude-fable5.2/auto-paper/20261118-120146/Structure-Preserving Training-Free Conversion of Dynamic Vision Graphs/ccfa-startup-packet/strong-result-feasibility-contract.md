# Strong-result feasibility contract

## Scope

This contract is binding for the first candidate: training-free conversion of dynamic-vision-graph operators. It deliberately does not claim a final top-conference result before evidence. It authorizes only the pre-registration and pilot needed to decide whether the direction can support the target tier. If the falsifiers trigger, the authorized next step is a versioned replacement from the material set, not a weaker claim.

## Main claim C1

- Claim: structured discretization error produces measurable neighbor/winner disagreement in a dynamic vision graph.
- Mechanism: signed multi-threshold coding perturbs features; kNN and signed max are non-Lipschitz discrete decisions, so small perturbations can change discrete outputs.
- Prerequisite assumptions: teacher uses per-layer kNN and signed max; a public or locally reproducible teacher exists; calibration data are available.
- Falsifying ablation: replace quantized features with teacher features at the same layer and verify that disagreement vanishes.
- Dataset: CIFAR-10 direct public parquet route, pending dataset-card license check: `https://huggingface.co/datasets/uoft-cs/cifar10/tree/main/plain_text`.
- Split protocol: official train/test; fixed 5,000-example calibration subset from train; three training splits; test frozen before tuning.
- Primary metric: layerwise neighbor Jaccard plus max-winner agreement; direction higher is better; accuracy is secondary.
- Simple baseline: unsigned rate coding.
- Strong feasible domain baseline: signed multi-threshold coding adapted from the published DCGS algorithm, independently reimplemented because the repository has no detected license.
- Matched internal control: signed uniform quantization at the same nominal levels and event budget.
- Minimum: measurable disagreement and a valid oracle intervention.
- Expected strong: baseline conversion loses at least 5 pp neighbor Jaccard or 2 pp winner agreement at T<=4 relative to teacher, and restoring teacher structure recovers at least half the accuracy loss.
- Failure: less than 1% structure disagreement and less than 1 pp accuracy gap at T=4, or an unresolved baseline/licensing/data blocker.
- Implementation path: reproduce the small ViG-style Grapher operator in PyTorch from the paper; implement signed multi-threshold coding separately from the upstream repository.
- Prototype sanity check: 64 random samples through one Grapher block with exact teacher and quantized features, all-shape and finite-value assertions.
- Calibration evidence: imported audit, arXiv records for DCGS/ViG, and GitHub API repository checks recorded in `prior-art-opportunity-map.md`.
- Test isolation: official CIFAR-10 test used once after configuration freeze; calibration subset drawn from train.
- Stop-and-return: any failed license/data/baseline/prototype/budget condition returns to scenario design before a full campaign.
- Resource budget: 24 runtime hours, 8 GB GPU memory, 3 seeds, 12 search trials, estimates pending hardware profiling.

## Main claim C2

- Claim: structure-aware calibration improves discrete agreement at a matched event budget.
- Mechanism: choose thresholds/offsets by directly minimizing topology and winner disagreement, not only activation MSE.
- Prerequisite assumptions: C1 is observed; calibration signal correlates with held-out disagreement.
- Falsifying ablation: activation-MSE calibration with the same parameter count and event budget matches or beats structure-aware calibration.
- Dataset/split/metric/baselines/controls: same as C1.
- Minimum: no significant degradation versus matched baseline.
- Expected strong: at least 50% recovery of baseline disagreement loss with <=1 pp teacher accuracy gap and no higher event count than the matched baseline.
- Failure: no recovery over activation-MSE control, or recovery only with a test-time teacher-structure oracle.
- Implementation path: add calibration objective over training-subset Grapher outputs; freeze parameters before test.
- Prototype sanity check: calibration loss decreases on train and calibration subset without using test labels.
- Calibration evidence: strong baseline gap must be measured in R2 before tuning target thresholds.
- Test isolation: same frozen test as C1.
- Stop-and-return: if C1 fails, C2 is void and the run returns to scenario selection.
- Resource budget: included in C1 envelope.

## Main claim C3

- Claim: discrete structure preservation causally explains accuracy recovery.
- Mechanism: teacher-neighbor and teacher-winner oracles isolate the contribution of each discrete decision.
- Prerequisite assumptions: oracle interventions are scientifically valid diagnostics, not deployable method components.
- Falsifying ablation: both-oracle intervention does not improve accuracy while method does.
- Dataset/split/metric/baselines/controls: same as C1, with random-neighbor control.
- Minimum: all intervention rows complete.
- Expected strong: method recovers at least half of both-oracle accuracy recovery.
- Failure: oracle interventions do not change accuracy or method gains are orthogonal to structure agreement.
- Implementation path: modify Grapher to accept teacher indices/winners during diagnostic only.
- Prototype sanity check: oracle exactly matches teacher layer outputs when all quantized activations are also replaced.
- Test isolation: interventions run on frozen test after design freeze.
- Stop-and-return: any test-driven redesign marks the test exposed and opens a replacement contract.
- Resource budget: included in C1 envelope.
