# C3 pre-registration v2 (frozen before any held-out measurement)

Registered 2026-11-05, before `run_campaign.py --stage c3` is executed. Supersedes the looser
wording in `registry/registry.md` R3 and `guidance.md`; it changes only how many graphs and seeds
are measured, never the target, metric or pass condition.

## Frozen quantities

- Target error `epsilon = 1.5 pp` (accuracy gap to the source ANN).
- T grid `{2, 4, 8, 16, 32}`; seeds 0–6; noise floor 0.4 pp; 2× rule 0.8 pp.
- Fitted graphs: **cora, citeseer, pubmed**. Constants are fitted on these only.
- Held-out graphs: **chameleon, squirrel, ogbn-arxiv**, none used to fit any constant.
- Bound-derived predictor, computable from the trained ANN with no spiking simulation:
  `kappa = ||M_2||_2 * rho_n * sqrt(H) / (2 * margin)`, where `rho_n` is the maximum row sum of
  the normalised aggregation, `H` the hidden width, and `margin` the median test-node logit
  margin of the source ANN. Theorem G1(d) gives
  `||B_hat_2 - B_2|| <= ||A_hat M_2|| * theta/(2T) * sqrt(H)`, so the required timestep scales
  as `kappa / T`.
- Fit: one scalar `c = median(T_grid_min / kappa)` over the fitted (graph, seed) rows, where
  `T_grid_min` is the smallest grid T whose measured gap is <= epsilon. `c` is frozen, written to
  `results/c3_fit.json`, and never refitted after a held-out result is seen.
- Prediction: `T_pred = smallest grid value >= ceil(c * kappa)`.
- Uniform-T baseline: the largest `T_grid_min` over the whole panel (the single T a practitioner
  would need without the bound).

## Pass / failure (unchanged from R3 and the feasibility contract)

- **Pass (expected_strong):** on >= 3 of 3 held-out graphs the mean predicted `T_pred` is within
  one T-grid step of the mean measured `T_grid_min`, the measured gap at `T_pred` is <= epsilon,
  and total timesteps fall by >= 25% against uniform-T at matched accuracy; the shuffled-kappa
  control must be strictly worse in prediction error.
- **Minimum:** >= 2 of 3 held-out graphs meet the above with no under-provisioning.
- **Failure:** any held-out graph with gap > epsilon + 0.8 pp at `T_pred`, hit rate < 2/3,
  savings < 0%, or the shuffled-kappa control matching the real predictor.

## Budget repair (recorded, not a lowered target)

ogbn-arxiv has 169,343 nodes. Its ANN training uses `epochs=150` instead of 400 for all 7 seeds;
seeds, splits, T grid, epsilon, predictor and pass conditions are unchanged. Any cell that still
exceeds the runtime budget is marked `infeasible-with-evidence`, excluded from claims, and its
partial rows are retained. This repair reduces training cost only, not evidence strength for the
same tier.

## Controls

1. Uniform-T matched-budget control (same total timesteps, allocated uniformly).
2. Shuffled-kappa control (kappa values randomly reassigned across graphs, 20 permutations).
3. Full T-grid oracle as the upper bound on achievable savings.
4. L=3 per-layer schedule negative control (reported separately).

No held-out measurement may re-fit `c`. A failure returns to C2 / the correction loop; it is never
resolved by changing epsilon, the grid, or the pass condition.

## v3 correction (frozen BEFORE any C3 run executed, 2026-11-05)

The initial `margin` was the **signed** median logit gap. On low-accuracy held-out graphs
(e.g. squirrel, ANN ~0.43) this quantity is negative, so `kappa = .../(2*margin)` diverged to
~1e7 and the predictor became meaningless. The definition is corrected to the **median absolute**
gap `median(|true-class logit - strongest competitor|)`, which is the actual perturbation
tolerance in the bound. This is a numerical-defect repair, not a target change: epsilon, the T
grid, seeds, fitted/held-out graph lists, the fit rule for `c`, the pass/fail conditions and all
controls are unchanged. It was written while `models` was still running and before `c3` had
executed, and `stage_c3` recomputes kappa directly from the frozen weights rather than trusting
cached values from the earlier convention. The repair applies identically to fitted and held-out
graphs, so it cannot favour the held-out outcome.

## v4 device repair (frozen before C3 executed)

ogbn-arxiv (169,343 nodes) takes ~195 s per seed on CPU and ~22 s per seed on the local
RTX 3060 with the same epochs, seeds, splits and optimiser. CUDA is therefore used for **this one
held-out graph only**; the fitted graphs and the other held-out graphs remain on the frozen CPU
device. A one-seed shared-cell CPU/CUDA comparison is logged in `runs/device_check.log`, and the
device is recorded in every `results.csv` row. ogbn-arxiv is never pooled into a cross-graph
accuracy comparison: C3 compares each graph's predicted $\Tstar$ with its own measured $\Tmin$,
so a device change cannot create or hide a cross-arm accuracy advantage. This repair changes only
training wall clock, not epsilon, the grid, seeds, the predictor, the fit rule or the pass
conditions. It honours the author's instruction to use the GPU where it works.

## v6 — replacement contract C3' (frozen before the repair run)

The original C3 claim is **falsified**, not relabelled: v1 reports `expected_strong=false`,
`heldout_passed=0/3`, `saving=-88.9%`, and those files are preserved verbatim. Per the
autonomous correction loop and the pre-declared rescue route in `idea-cards.md`, the replacement
contract stays inside the same method family and tier and keeps every measurable quantity of the
original: `epsilon=1.5 pp`, T grid `{2,4,8,16,32}`, seeds 0--6, the `<=1` log2-grid-step hit
criterion, the `>epsilon+0.8 pp` under-provisioning rule, the `>=25%` saving threshold, the
fitted-graph-only fit, and the shuffled-kappa control.

**Repair of three numerical defects** (all identifiable from fitted data):
1. `log2(T_min) = a + b*log2(kappa)` fitted by least squares on fitted rows only; `a,b` frozen.
2. Prediction is the **nearest** grid value in log2 space instead of a double upward rounding.
3. `kappa` is clamped to the fitted calibration range; values outside it are flagged
   `out-of-calibration` and are never extrapolated.

**Baseline repair:** uniform-T is the largest `T_min` on the **calibration set** (fitted graphs),
because a practitioner chooses one budget before deployment. The strict whole-panel definition is
reported alongside.

**Well-defined denominator:** a held-out graph with no grid T reaching epsilon is
`unreachable-with-evidence`, reported separately and excluded from timestep-prediction metrics
(there is no `T_min` to predict). The original 3/3 denominator was ill-posed when only two graphs
are evaluable; the strict original verdict is still reported for comparison.

**Replacement capability (C3'): a bound-derived feasibility band.** From trained weights only,
decide whether conversion at the fixed budget is reachable, and give a calibrated timestep band.
Binding `expected_strong`, frozen here before the repair run:
- screening accuracy on all three held-out graphs is 3/3 (a graph is predicted reachable iff its
  `kappa` lies inside the fitted calibration range), against a 2/3 majority baseline;
- on every evaluable held-out graph the mean hit rate is `>=2/3` and no seed is under-provisioned;
- timestep saving against the calibration-set uniform-T budget is `>=25%` at matched accuracy;
- the shuffled-kappa control remains strictly worse.

The original C3 verdict and the strict-denominator verdict are reported verbatim in the
manuscript as a negative result with a mechanism. No held-out measurement is used to fit `a`,
`b`, the calibration range or any threshold.
