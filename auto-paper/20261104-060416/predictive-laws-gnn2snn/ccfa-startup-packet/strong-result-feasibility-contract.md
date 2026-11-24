# Strong-result feasibility contract

Target: CCF-A (ICML 2027 primary; ICLR 2028 / NeurIPS 2027 fallback). Binding `expected_strong` is
stated per claim and is calibrated against numbers we have already measured, never against a desired
headline. The machine-checkable index is `feasibility-contract.json`; this file is the reasoning.

## Why this is not a wish

We are not forecasting; two of the three laws are already measured on this machine, at seven seeds,
with the code in `experiments/`. What is *not* yet shown is that they **predict held-out
configurations**, which is the difference between a curve fit and a law. That is the risk this
contract prices.

Existing calibration points (all from `registry/results.csv`, measured 2026-11-03):

| quantity | measured value | source |
|---|---|---|
| amplification exponent vs `G` | 0.948, r = 0.990, n = 9 | `results/wp3_depth.json:_P1` |
| `‖E_1‖/√H` stability | 1.724 → 1.614 over H = 16…128 (6.4 % spread) | `results/wp3_depth.json:_P2` |
| membrane order spread | 0.000 pp over 4 perturbations, 2 neurons, 2 graphs | `results/wp6a_misalignment.json` |
| count order spread | 0.386–1.614 pp | same |
| run-to-run floor | 0.36 / 3.40 / 0.40 pp by latency class | `results/stats_ci.json` |
| sparsity exchange rate | 50 % units → −23…−36 % spikes at ≤ 0.5 pp | `results/wp4_sparsity.json` |

## Claim P (the title claim) — prediction

**Mechanism.** `‖E_L‖ ≈ c·√H·G/T`, where `G` and `H` are read from the weights and `c` is a single
constant fit on training cells. The decision flips when the perturbation exceeds the margin, so
predicted accuracy is `E[𝟙(Δ_n > |ε_n|)]` under a per-node error model with a fixed shape.

**What "strong" means numerically.** Two thresholds, both pre-registered:

- **minimum:** Spearman ρ between predicted and observed gap ≥ 0.7 across held-out cells.
- **expected_strong:** MAE ≤ 1.0 pp *absolute* on held-out cells, and the predicted required-T
  (smallest T reaching ANN − 1.5 pp) equals the observed T on ≥ 70 % of cells, with no error larger
  than one grid step.
- **failure:** MAE > 2.0 pp or required-T exact on < 50 % of cells. Then the paper drops the
  predictive claim from the title and reports the laws as descriptive.

**Why ≤ 1 pp is credible and not optimistic.** Our measured gaps at T ≥ 8 are 0.03–1.24 pp; the run-
to-run floor at T ≥ 8 is 0.40 pp. A predictor that is wrong by less than 1 pp is therefore wrong by
less than the noise on the quantity being predicted — which is the correct standard for a prediction
of an aggregate accuracy, and it is stricter than it looks because the floor is 0.4 pp.

**Where it could break.** (a) `c` might be dataset-dependent. Mitigation: report `c` per dataset and
also a single pooled `c`; if per-dataset `c` varies more than 20 %, the claim becomes "predicts up to
one calibrated constant", which is still a prediction but must be stated. (b) The margin distribution
of a graph with 3 classes (PubMed) is very different from 7 (Cora); a single error-shape model may
need a per-dataset scale. That is the same mitigation.

**Test isolation.** All fitting uses only cells whose (dataset, L, H, T) is in the fit set; no cell
contributes to both fit and evaluation. `T` is never in the fit set of its own evaluation.

## Claim E (the anchor) — external Pareto

**Mechanism.** If conversion is a different discretisation of the same computation rather than a
different model family, then at small `T` it should reach a given accuracy in fewer synaptic
operations than a *trained* spiking network, because the latter pays a training cost per `T` and
learns sparser but weaker features. If that is false, the low-latency positioning is false.

**Thresholds.**
- **minimum:** no external arm dominates the conversion at `T ≤ 4` (higher accuracy *and* lower
  SOPs). Equivalently: at least one external arm is beaten on both axes, and none beats us on both.
- **expected_strong:** conversion reaches ANN − 1.5 pp with strictly fewer SOPs than every external
  arm on ≥ 2 of 3 citation graphs.
- **failure:** any external arm has both higher accuracy and lower SOPs at `T ≤ 4` on ≥ 2 graphs.
  Then §4.2 is rewritten as "conversion trades accuracy for training cost" and the low-latency claim
  is withdrawn.

**Honesty constraint that is part of the contract.** The table must label each arm
`codebase-reproduction` or `formulation-reimplementation`. We have zero codebase reproductions, and
the caption must say so. The SpikingGCN-style architecture arm already measured **beats us on Cora
and CiteSeer**; that row stays in the table even though it weakens the claim, because removing a
measured unfavourable row is the one thing that would make the whole paper untrustworthy.

## Claim O (the mechanism separation) — order invariance

**Mechanism.** `Σ_t inst_t = Â(count₁M₂) + Tb₂` contains no `t`, so any permutation or phase shift of
layer-1 spikes is invisible to the membrane decoder and visible to the count decoder.

**Thresholds.**
- **minimum:** membrane accuracy spread ≤ 0.1 pp over the four perturbations.
- **expected_strong:** ≤ 0.01 pp, i.e. float-level, on both datasets and both neuron models, with the
  count spread ≥ 0.3 pp in the same cells.
- **failure:** membrane spread > 0.1 pp, which would mean the accumulator is not what we claim.

Already measured: 0.000 pp in all four cells. The remaining work is to make the *count* side move
enough to be convincing, which it does (up to 1.6 pp).

## Budget

| item | estimate | basis |
|---|---|---|
| prediction grid (3 datasets × 3 depths × 4 widths × 6 latencies, 7 seeds) | 20 h CPU | measured: ~25 min per (dataset × 3 depths) block on 12 cores |
| external Pareto (3 arms × 3 datasets × 6 latencies × 7 seeds) | 6 h | measured: full 7-seed baseline suite ≈ 7 min per arm on GPU; CPU-only ~2 h |
| ensemble (3 graphs × V∈{1,3,9} × 7 seeds) | 3 h | 9 forward simulations per cell |
| writing/analysis | 10 h | — |
| **total** | **≈ 40 h** | single 3060 + 12 cores, no cloud |

Stop-and-return conditions: if the prediction grid cannot be completed within 24 h of wall clock,
cut widths to {16,64} rather than cutting seeds (seeds protect the floor, widths do not); if that
still overruns, return to the guidance and re-scope the claim rather than reporting a weak test.
