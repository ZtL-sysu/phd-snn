# Initial mechanism cards — screening pool, not accepted ideas

The following cards come from the observed gap between graph conversion fidelity and structure-dependent decision confidence. All novelty fields remain `needs-search` until their individual primary-source screen.

## C01 — Signed two-sided conversion for heterophily

- Bottleneck: nonnegative rate neurons erase low-pass/heterophilic negative evidence and inhibitory message contributions.
- Mechanism: split a linear signed preactivation into nonnegative excitatory/inhibitory components with exact fixed-point reconstruction, then propagate signed residual corrections across normalized adjacency.
- Assumption: trained signed heterophilic filters contain information unavailable to nonnegative ReLU encoders.
- Falsifier: matched signed conversion does not improve validation fidelity over the best magnitude/threshold baseline at T≤4 on two graph families.
- Contribution: conversion mechanism plus graph-frequency error analysis. Risk: signed-spike and bipolar encoding prior art.

## C02 — Aggregation-aware per-neuron time budgets

- Bottleneck: a global T ignores degree/neighborhood entropy and error amplification through graph aggregation.
- Mechanism: allocate local residual precision from training-only degree/neighborhood statistics while preserving a synchronous decodable prefix.
- Assumption: graph statistics predict per-node conversion residual beyond activation magnitude.
- Falsifier: no better fidelity/event Pareto than equal-work activation-only or random allocation on two datasets.
- Contribution: topology-conditioned conversion precision. Risk: A²Q, mixed timesteps, and prior local budget failures.

## C03 — Neighborhood-contrast calibration

- Bottleneck: conversion errors can be systematic between a node and its neighborhood, rather than zero-mean per-coordinate rounding.
- Mechanism: estimate signed residual moments conditional on train-only neighborhood feature/label-free disagreement and correct the first residual term without labels at inference.
- Assumption: neighborhood contrast contains out-of-sample residual information after controlling for source activation.
- Falsifier: fails against source-only and shuffled-neighborhood calibrators at equal parameters on two datasets.
- Contribution: graph-specific bias correction. Risk: FTBC/local calibration and previous graph-objective failures.

## C04 — Reception-field stopping for graph readout

- Bottleneck: classification may stabilize before every layer/site has consumed all T frames; fixed T charges unnecessary message propagation.
- Mechanism: a causal margin/ensemble-stability rule prunes later graph layers or sites, with an exact fallback to full conversion when uncertain.
- Assumption: confidence stabilization predicts final teacher agreement early enough to save work.
- Falsifier: cannot beat uniform reduced-T and random-site stopping at matched validation teacher agreement and actual event/work cost.
- Contribution: conversion-time graph computation reduction, not a generic SNN early-exit rename. Risk: dynamic inference and early-exit SNN prior art.

## C05 — Topology-shift recalibration without labels

- Bottleneck: frozen conversion thresholds can fail under degree/feature-shifted graph distributions.
- Mechanism: update only bounded residual/threshold statistics from unlabeled target graphs, retaining a source-statistics anchor and exact no-shift fallback.
- Assumption: activation/threshold mismatch is measurable without labels and correctable across graph shift.
- Falsifier: no consistent improvement over source-frozen and target-percentile baselines across two held-out shift families.
- Contribution: test-time graph conversion adaptation. Risk: SNN test-time adaptation and generic normalization.

## C06 — Decision-margin directed residual allocation

- Bottleneck: coordinate MSE is not the decision loss; near-tied graph predictions have different tolerance to conversion error.
- Mechanism: use train-only teacher top-class sensitivity to bound and correct only residual directions capable of changing the pooled logit margin.
- Assumption: sensitivity-weighted residual correction buys fidelity with fewer extra events than uniform residual refinement.
- Falsifier: no improvement over matched random/same-cost residual directions at equal event budget on two datasets.
- Contribution: graph-readout decision-aware conversion bound and mechanism. Risk: margin-based SNN conversion and previously closed hard-event objective family.

## C07 — Sign-preserving low-rank message events

- Bottleneck: dense analog node features generate costly graph messages even when the graph operator needs only a low-dimensional subspace.
- Mechanism: train-only projector derived from downstream weight spectra, transmit quantized low-rank signed residuals, reconstruct at receivers; exact residual fallback handles omitted components.
- Assumption: useful message variability is lower rank than node activation variability.
- Falsifier: cannot dominate PCA-free channel pruning and uniform quantization at equal transmitted events and teacher agreement on two datasets.
- Contribution: operator-conditioned message compression during conversion. Risk: graph quantization/low-rank compression is established; novelty must be conversion-specific.

## C08 — Perturbation-robust threshold certificates

- Bottleneck: near-threshold conversion instability under input/edge perturbations can change graph predictions even when clean fidelity is high.
- Mechanism: calibrate neuron dead zones and residual guards from training perturbations to bound flipped spike events; abstain/fallback on unbounded cases.
- Assumption: spike-event stability bounds translate into better robust teacher agreement than clean-MSE calibration.
- Falsifier: no robust gain over equal-clean-accuracy percentile/FTBC control on at least two perturbation types/datasets.
- Contribution: certified graph conversion under perturbation. Risk: robust SNN training and randomized smoothing are adjacent.

## C09 — Teacher-consistent selective residual ensemble

- Bottleneck: deterministic conversion can be biased on difficult graphs; more T uniformly is costly.
- Mechanism: use two cheap complementary deterministic residual orderings, detect disagreement, and refine only the uncertain graph subset.
- Assumption: cheap-converter disagreement identifies examples whose accuracy improves from extra T.
- Falsifier: no better agreement/work tradeoff than confidence-only selection and uniform T on two datasets.
- Contribution: deterministic conversion uncertainty and adaptive computation. Risk: SNN ensembles/early exit and temporal coding.

## C10 — Homophily-conditioned conversion routing

- Bottleneck: high- and low-homophily graphs/regions require different signed residual and aggregation precision.
- Mechanism: route between signed two-sided and ordinary residual conversion using only label-free train-calibrated neighborhood statistics; preserve an exact unified decoder.
- Assumption: homophily predicts the best converter beyond activation statistics.
- Falsifier: routing does not beat both component converters and a shuffled-router control at matched work on homophilous and heterophilous data.
- Contribution: graph-regime-conditioned conversion. Risk: conditional/dynamic GNN and mixture-of-experts routing.

These are hypotheses. C02/C03/C06 have close relationships to previously failed local loss/event allocation families and must use a clearly different mechanism and matched control before execution; they cannot be accepted from a renamed retry.
