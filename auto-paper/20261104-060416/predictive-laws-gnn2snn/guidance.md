# Guidance — When Does Graph-to-Spiking Conversion Work?

Run folder `auto-paper/20261104-060416/predictive-laws-gnn2snn/`. This file is the contract for
`f-research-v1`. Every binding number below is traceable to `ccfa-startup-packet/` and, where it is
already measured, to `registry/results.csv` in the predecessor run.

## Title / Topic

**Working title.** *When Does Graph-to-Spiking Conversion Work? Predictive Laws for Latency, Depth
and Energy.*

**Target field.** Neuromorphic / spiking computation for graph-structured data (cs.LG, cs.NE).

**Target venue.** ICML 2027 (primary), ICLR 2028 / NeurIPS 2027 (fallback). Tier: CCF-A.

**Contribution type.** Predictive theory with method consequences, anchored by an external
benchmark. Not a new architecture, not an accuracy SOTA.

## Core Idea

A conversion's fidelity is not a property that must be discovered by simulation. It is a closed-form
function of three quantities read off the trained ANN.

The conversion error obeys, exactly, for any depth,
`B̂_l − B_l = (1−α)·Â·(E_{l−1}·M_l)` with `E_0 = 0` and `E_l = count_l/T − relu(B_l)`.
Taking norms, and using `‖Â‖₂ ≤ 1`, gives

`‖E_L‖ ≲ ‖E_1‖ · ∏_l (1−α)‖M_l‖₂  =:  ‖E_1‖ · G`.

Layer 1's error is a sum of independent per-unit quantisation errors, each of size at most
`1/(2T)`, so `‖E_1‖ ≈ c·√H_active/(2T)`. A prediction survives when the resulting logit
perturbation is smaller than the margin `Δ_n`. Therefore

`P(flip at node n) ≈ Φ(−Δ_n / (σ_n))`, with `σ_n` fixed by `c·√H·G/T` and the row of `M_L`,

and the whole accuracy–latency curve follows from `(G, H, Δ, T)` — three of which are read from the
weights in milliseconds. The paper's claim is that this predicts *held-out* configurations to within
the measurement noise, and that the two design consequences (depth is unusable, width is the lever)
fall out of it rather than being tuned.

Secondary, and independently falsifiable: with a sum readout the accumulator contains no `t`, so the
membrane decoder is *exactly* invariant to the order of upstream spikes while the count decoder is
not. This is what separates our error object from the cross-layer shuffle of the 2025 conversion
literature, and it is settled by a 2×2 measurement, not by a definition.

## Paper Story

**Problem.** Practitioners convert a trained GNN to a spiking network to get event-driven, low-
latency inference without retraining per latency budget. Every such project discovers the achievable
fidelity by running the conversion, and every design decision — depth, width, timestep budget,
whether to sparsify — is therefore made blind, because the ANN's own accuracy is the only signal
available and it is the wrong signal.

**Gap.** The conversion literature for feed-forward networks gives error *bounds*. No work gives a
*prediction* of the accuracy a conversion will reach, for graphs or otherwise; no work states what
happens at more than two layers; and the field's vocabulary conflates two different temporal
phenomena. The largest unified spiking-GNN benchmark contains no conversion entry at all.

**Insight.** On a graph the error is not a bound but an identity: the layer that follows integrates a
neighbour-averaged, per-node-quantised rate, and the resulting error is exactly `Â(E_{l−1}M_l)`. Once
written that way, the only unknowns are spectral gains and quantisation variance, both of which are
measurable before conversion.

**Evidence chain the reader should follow.** (1) The identity, verified to `2×10⁻⁶`. (2) The two
laws — amplification exponent 0.948 at `r = 0.990`, and `‖E_1‖ ∝ √H` stable to 6 % — measured, then
(3) used *out of sample* to predict held-out cells. (4) The consequences: depth fails and `G` says by
how much; width works and `√H` says why; sparsity buys synaptic operations but not spikes. (5) An
external Pareto under one protocol, including the row where a published architecture beats us.
(6) The order-invariance 2×2 that makes the decoder a mechanism rather than a preference.

## Paper Outline

1. Introduction: the practitioner's blind choice; the four claims; what the paper deliberately does
   not claim.
2. Related Work: trained spiking GNNs; conversion theory for feed-forward nets and what we inherit
   from the bias-correction and cross-layer-misalignment lines; why ordering and quantisation are
   different objects.
3. Method: the L-layer recursion and its proof; the layer-1 quantisation law; the margin criterion
   and the resulting predictor; the membrane readout and its order invariance; the depth and width
   corollaries; the design rule (compute `G`, choose width, do not stack depth).
4. Experiments and Results: protocol and floors; prediction on held-out cells; external Pareto in
   accuracy–timesteps and accuracy–SOPs; depth; width; order invariance; sparsity exchange rate;
   theorem soundness and tightness; generality across operators, homophily and 169k nodes.
5. Discussion: what the laws do and do not license; why the amplification cannot be
   reparametrised away (the threshold is an absolute scale); honest limits on external comparison;
   deployment implications.
6. Conclusion: the four laws, the negative results, and the one-sentence rule.

## Experiment Plan

**Datasets** (all directly public, no approval flow). Planetoid Cora / CiteSeer / PubMed via
`https://github.com/kimiyoung/planetoid` (raw `ind.*` files, public split 20-per-class / 500 / 1000);
ogbn-arxiv via `https://ogb.stanford.edu/docs/nodeprop/` (official time split 90941/29799/48603);
chameleon and squirrel via PyG `WikipediaNetwork` (Geom-GCN split 0). Source/access recorded in
`dataset-access-log.md`.

**Baselines.** Four arms, all run under the frozen protocol at 7 seeds.
(a) *Conversion* (ours): FTBC bias, membrane readout, one training per dataset.
(b) *Direct*: surrogate-gradient BPTT spiking GCN with per-step dropout, retrained per `T`.
(c) *Rate-coded / Poisson*: the SpikingGCN formulation of input coding.
(d) *Published architecture*: SGC-2 propagation plus a 512-wide spiking layer, the SpikingGCN
architecture — this arm **beats us on Cora and CiteSeer** and stays in the table.
Literature context only, never in the main comparison: SGNNBench's unified numbers.

**Method variants** for the ablation ladder — bias none / scalar / per-channel; readout membrane /
count; neuron IF / TPP; `θ ∈ {0.5,1,2}`; width `{16,32,64,128}`; depth `{2,3,4}`; sparsity
`{0,25,50,75} %`; ensemble `V ∈ {1,3,9}` with a random-seed ensemble control.

**Ablations that can falsify the mechanism** — shuffle per-unit quantisation errors before
propagation (kills the `√H` claim if prediction is unaffected); gauge-normalise each layer (kills the
amplification claim if conversion accuracy survives); replace the sum readout with a leaky membrane
(kills the order claim if order still does not matter).

**Metrics.** Primary metric — mean absolute error (pp) of the predicted conversion gap on held-out
cells; secondary metrics — accuracy, gap to ANN, synaptic operations per inference
`SOPs = T × edges × H_active`, spikes per node, retrain count to cover the `T` grid, wall-clock
training time, and the fraction of cells where predicted required-`T` matches observed.
Statistical checks — 7 seeds, paired percentile bootstrap (10 000 draws) over per-seed differences,
and the measured run-to-run floor (0.36 / 3.40 / 0.40 pp by latency class) applied as a 2× rule; no
claim below 2× the floor.

**Runtime / Hardware Budget.** Local AMD 12-core, 32 GB RAM, RTX 3060 12 GB. Training on CPU
(deterministic; CUDA moves the PubMed ANN by 0.69 pp through sparse-reduction order). Estimated
40 h total: 20 h prediction grid, 6 h external Pareto, 3 h ensemble, 11 h writing and analysis.
No cloud.

**Stopping criteria.** Stop and re-scope rather than tune toward the target if (i) prediction MAE
exceeds 2 pp after the full grid, (ii) any external arm dominates at `T ≤ 4` on two or more graphs,
or (iii) the grid cannot complete in 24 h wall clock — in that case cut widths to `{16,64}` and keep
7 seeds, never cut seeds.

## Expected Results

**Minimum acceptable.** The two laws describe the data (`r ≥ 0.9`) and predict held-out cells with
Spearman `ρ ≥ 0.7`; the conversion is not dominated at `T ≤ 4` on more than one graph; membrane order
spread `≤ 0.1 pp`. At this level the paper is a solid B-venue analysis.

**Strong result (binding `expected_strong`).** Prediction MAE `≤ 1.0 pp` on held-out cells with
required-`T` exact on `≥ 70 %` of cells; conversion reaches ANN−1.5 pp with fewer SOPs than every
external arm on `≥ 2/3` graphs; membrane spread `≤ 0.01 pp` with count spread `≥ 0.3 pp` in the same
cells. At this level the paper has the two properties the red team named as score-change conditions
and is an A-venue candidate.

**Failure signal.** Prediction MAE `> 2 pp`, or an external arm dominating at `T ≤ 4` on two or more
graphs, or membrane spread `> 0.1 pp`. Any of these removes the corresponding claim from the title
and the abstract, and the paper is repositioned as a diagnostic framework — which is a decision made
from the numbers, not negotiated afterwards.

## Figure and Table Plan

Selection is deferred until results stabilise; what follows are decision rules, not a quota.

- The identity and the recursion want a *schematic plus a residual plot*: a figure is justified only
  if the residual is at float level, because that is the point being made.
- The predictor wants *predicted-vs-observed scatter with the identity line* — one panel per
  held-out regime — because a scatter shows calibration in a way a table of MAEs cannot.
- The external comparison wants *two Pareto panels* (accuracy vs timesteps, accuracy vs SOPs) rather
  than a wide table, since dominance is a geometric property.
- Depth and width want *one table each* with the spectral gain as a column, so the reader can check
  the law rather than take it.
- Order invariance wants a *small 2×2 table*, not a figure; four numbers per dataset carry it.
- Anything that would need more than one page of table is split or moved to the appendix.

## Traceability Checklist

| Guidance requirement | Required artifact | Success check | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|
| L-layer identity holds | `experiments/core.py::check_identity`, residual log | max residual ≤ 1e−5 at L∈{2,3,4} | none (inline) | yes |
| Prediction on held-out cells | `results/wp7_predict.json` | MAE ≤ 1.0 pp, required-T ≥ 70 % | Fig. predicted-vs-observed | yes |
| External Pareto, 4 arms | `results/wp2_pareto.json` | no domination at T ≤ 4 on ≥2 graphs | Fig. Pareto (2 panels) | yes |
| Depth law | `results/wp3_depth.json` | exponent ∈ [0.5,1.5], r ≥ 0.9 | Tab. depth | yes |
| Width law | `results/wp3_depth.json:_P2` | `‖E_1‖/√H` spread < 10 % | Tab. width | yes |
| Order invariance | `results/wp6a_misalignment.json` | membrane ≤ 0.1 pp, count ≥ 0.3 pp | Tab. order | yes |
| Sparsity exchange rate | `results/wp4_sparsity.json` | SOPs ∝ kept fraction; accuracy cost stated | Tab. sparsity | yes |
| Ensemble (stretch) | `results/wp5_ensemble.json` | gain vs random-ensemble control | Tab. ensemble | conditional |
| Theorem soundness | `results/theory_s7.json` | 0 counterexamples | Tab. theory | yes |
| Closed-form bias beats grid | `results/beta_star_s7.json` | ≥ 7 of 9 cells | Tab. ablation | yes |
| Generality: operators, homophily, scale | `results/arch_s7.json`, `hetero_s7.json`, `arxiv_s7.json` | gap ≤ 1.5 pp at T=8 | Tab. extended | yes |
| Falsifier: quantisation shuffle | `results/wp7_predict.json:_shuffle` | shuffled predictor worse by ≥ 0.5 pp MAE | inline | yes |

## Citation Scope

**Clusters.** (1) Trained spiking GNNs — SpikingGCN (IJCAI'22), SiGNN, DGSNN, SpikeGraphormer,
continuous spiking GNN, geometry-aware, Riemannian, Loihi deployment, heterogeneous spiking GAT;
(2) conversion theory — FTBC (ECCV'24), temporal misalignment and TPP (ICML'25), threshold/potential
initialisation (ICML'21, IJCAI'21), rate-coding normalisation; (3) GNN depth and propagation —
GCN, SGC, APPNP/DAGNN, GCNII, oversmoothing; (4) benchmarks and infrastructure — Planetoid, OGB,
PyG, SGNNBench.

**Must cite.** FTBC and the 2025 temporal-misalignment paper (mechanism ancestors, and the boundary
must be explicit), SpikingGCN (the formulation we re-implement), SGNNBench (the only unified protocol
we could align to), GCNII/DAGNN (the depth backbones we test and reject).

**Recency.** At least 36 distinct verified works with a strict majority from 2022–2026; every entry
checked against its arXiv or publisher record before it enters `refs.bib`. Venue mix: ICML, ICLR,
NeurIPS, IJCAI, AAAI, ECCV, KDD, plus arXiv preprints where no venue version exists.

## Handoff note on claims

`planned_claim` above is what the guidance asks for. `observed_finding` stays
`unresolved_until_evidence` until P5A/P6 read the registered results. No predicted number in this
file may be copied into the manuscript as a result; the manuscript's numbers come from
`registry/results.csv` only.
