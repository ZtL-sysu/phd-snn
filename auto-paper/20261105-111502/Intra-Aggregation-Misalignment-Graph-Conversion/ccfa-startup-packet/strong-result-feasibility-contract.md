# Strong-result feasibility contract

Binding pre-experiment contract. Every `expected_strong` below is calibrated against measured or
primary-source evidence, never chosen for presentation value. Constants are frozen and committed
**before** measurement at P4. This document is the substantive evidence that
`feasibility-contract.json` indexes.

Shared protocol: Planetoid public splits; seeds 0–6 (never extended); T grid {2,4,8,16,32};
paired bootstrap 95% CI; noise floor 0.4 pp at T≥8; any claimed improvement must exceed 2× the
noise floor (0.8 pp), otherwise it is reported as a tie. Device is a frozen field decided by the G0
reproduction. All rows carry `run_id`, seed, git commit, config hash and device.

---

## Claim C1 — mechanism separation

- **Claim:** conversion error on graphs arises inside a single neighbourhood aggregation as a
  deterministic, `ρ_n`-amplified phase error; the ICML'25 cross-layer stochastic rearrangement is a
  different phenomenon and does not remove it.
- **Mechanism:** `B̂_l − B_l = (1−α)Â(E_{l−1}M_l)`. The aggregation operator is inside the error;
  randomising the neuron's firing time changes `E` but not `Â`'s systematic bias term.
- **Assumptions:** rate-coded IF/TPP neurons, static graph, fixed normalized `Â`, shared weights,
  no test-time adaptation, same backbone and seeds across arms.
- **Falsifying ablation:** 2×2 crossed design — inter-layer permutation on/off × intra-aggregation
  phase randomisation on/off — plus the four-way neuron control
  (IF / IF+`β*` / TPP / TPP+`β*`). Branch C (TPP ≥ ours) or D (phase randomisation helps) falsifies.
- **Dataset / split:** https://github.com/kimiyoung/planetoid/raw/master/data ; Cora 140/500/1000,
  CiteSeer 120/500/1000, PubMed 60/500/1000.
- **Primary metric / direction:** node-classification accuracy, higher is better; reported as pp
  differences against the matched control.
- **Simple baseline:** IF conversion with no bias correction.
- **Strongest feasible domain baseline:** TPP neuron re-implemented from ICML'25 equations (8)–(13),
  under identical aggregation, backbone, seeds and hyperparameters.
- **Matched internal control:** IF+`β*` vs TPP+`β*` at the same T; the difference isolates the neuron.
- **Calibration evidence:** task book §2 T=8 ablation gives our method 0.8021/0.6880/0.7684 vs TPP
  0.7756/0.6457/0.7427, i.e. 2.65/4.23/2.57 pp margins — already above the 0.8 pp decision rule.
  ICML'25 Figure 1 primary-source numbers are in `notes/G0_literature_map.md` §2.
- **Minimum:** S1 lands in branch A or B; TPP transplant ≥ 1.5 pp behind IF+`β*` at T=4 on ≥2/3
  graphs; the 2×2 directions differ by more than 2× noise floor.
- **Expected strong:** branch B (cross-layer permutation effect < noise floor while TPP still
  trails), with the intra-aggregation randomisation arm significantly worse, on all three graphs and
  7 seeds; TPP+`β*` ≥ TPP (orthogonality), so the correction is not neuron-specific.
- **Failure:** branch C or D; or a direction reversal across seeds; or the TPP unit test missing
  the frozen T=8 values by > 0.5 pp.
- **Implementation path:** adapt the companion L-layer `experiments/core.py` (record source commit
  `d125112` and sha256), add `probes.py` with the two permutations and a `tpp_neuron.py` from
  equations (8)–(13); store the diff in `runs/`.
- **Prototype check:** single-cell T=8 Cora TPP re-implementation must reproduce 0.7756 ± 0.5 pp
  before the full probe grid starts.
- **Budget:** 24 h wall clock, 8 GB, 7 seeds, 120 search trials; 12 CPU cores and RTX 3060 12 GB.
- **Reviewer questions answered:** main experiment — "is this TPP on graphs?"; ablation — "is the
  bias orthogonal to the neuron?"; robustness — "does the direction hold across T and seeds?";
  efficiency — recorded as spike counts, not an energy claim.
- **Test isolation:** held-out graphs are untouched; probe seeds are fixed and separate from any
  model-selection decision.
- **Stop–return condition:** if the prototype fails or branch C/D is observed, stop the campaign,
  write `notes/`, report to the author per GP, and return to mechanism design. Do not rescale the
  target or continue to S3.

---

## Claim C2 — `ρ_n`-weighted L-layer bound

- **Claim:** `‖E_L‖ ≤ f(ρ_n, ‖D_W‖, θ, T, ‖E_l‖)` with a mandatory `β*` system term; the L-layer
  closed form gives an explicit `T_L` dependence. Unlike `‖W‖∞·θ/T`, the multiplier involves
  neighbourhood geometry.
- **Mechanism:** recursion of `E_l` through `Â`; the row-sum `ρ_n` enters multiplicatively per hop,
  and the un-corrected system term accumulates linearly in `ρ_n`.
- **Assumptions:** bounded activations, fixed `Â`, ReLU homogeneity, known spectral norms, no
  train-time renormalisation of the threshold scale.
- **Falsifying ablation:** L∈{2,3,4} counterexample search over the 30-cell-style grid used in the
  companion project; spectral-norm-constrained training and adaptive-threshold controls as escape
  routes to close.
- **Dataset / split:** the same three Planetoid graphs; L∈{2,3,4} GCN backbones.
- **Primary metric / direction:** number of bound violations, lower is better (target 0); secondary
  bound/measured conservatism ratio.
- **Simple baseline:** the image-domain form `‖W‖∞·θ/T` applied naively to the graph weights.
- **Strongest feasible domain baseline:** the companion's empirical `G^0.95` law (r = 0.990 over
  9 cells), reaccepted as external calibration evidence with hashes/commits, not as this run's result.
- **Matched internal control:** same networks with `β*` removed, so the system term's contribution
  is measured directly.
- **Calibration evidence:** the companion measured `‖E_L‖/‖E_1‖ ∝ G^0.948`, r = 0.990, and a
  four-layer loss of 21 pp at T=8; the exact per-layer identity has a numerical residual ≤ 2e-6.
  These make a `ρ_n`/`G`-indexed bound plausible rather than aspirational.
- **Minimum:** L=2 and L=3 have zero counterexamples and the conservatism ratio is reported for
  every cell; if L=4 fails, an explicit failure-depth condition is derived.
- **Expected strong:** zero counterexamples for all L≤4, mean conservatism between 3× and 8× (the
  companion's latency bound was 3.2–6.7×), and a closed-form `T_L` whose exponent matches the
  measured depth scaling within the pre-registered tolerance.
- **Failure:** any bound violation that cannot be attributed to a stated assumption, or conservatism
  > 20× (a technically true but unusable bound).
- **Implementation path:** `bound.py` implementing the recursion, closed form and violation scan;
  proof in the appendix with a symbol table.
- **Prototype check:** numerical residual of the identity ≤ 1e-5 on a 30-cell grid before any
  theorem claim is written.
- **Budget:** 18 h, 8 GB, 7 seeds, 60 search trials.
- **Reviewer questions answered:** main — "is the bound true?"; ablation — "does the bias term
  matter?"; robustness — "at what depth does it break?"; efficiency — `T_L` is the resource link.
- **Test isolation:** the counterexample grid is fixed before fitting any bound constant.
- **Stop–return condition:** a violation with no stated failure condition returns to theory design;
  writing an empirical characterisation instead requires a versioned contract correction.

---

## Claim C3 — bound-derived latency allocation (BINDING `expected_strong`)

- **Claim:** inverting the C2 closed form predicts each model's minimum `T*` for a target error
  ε = 1.5 pp, and a per-layer allocation reaches that target with fewer total timesteps than a
  matched uniform-T budget, **on graphs not used to fit any constant**.
- **Mechanism:** `T_L` is an explicit function of `ρ_n`, `G`, θ and the margin distribution;
  inversion gives a per-model/per-layer step budget. This is a capability: a practitioner can
  choose T from trained weights without running the full T grid.
- **Assumptions:** the bound's assumptions hold; the margin proxy is computable from the trained
  ANN alone; the target ε is fixed before measurement; constants are frozen in a committed
  pre-registration.
- **Falsifying ablation:** (i) uniform-T matched-budget control, (ii) shuffled-`ρ_n` control
  (bound constant present, geometric signal destroyed), (iii) grid-search oracle as an upper bound
  on achievable savings, (iv) an L=3 per-layer schedule negative control.
- **Dataset / split:** constants fitted on the three fitted Planetoid graphs only; **held-out**
  evaluation on ogbn-arxiv and chameleon (version declared), with squirrel reserved as a stress
  cell and excluded from any claim if the runtime budget is exceeded — its partial rows are retained.
- **Primary metric / direction:** total timesteps to reach ε, lower is better; secondary prediction
  hit rate (predicted `T*` within one T-grid step of the grid-searched minimum) and achieved gap.
- **Simple baseline:** uniform T = the largest `T` required across the panel (task-book §2 shows
  T=4 already reaches 1.17/1.02/0.18 pp, so a single uniform T wastes steps on the easy graphs).
- **Strongest feasible domain baseline:** full T-grid search per model (oracle), which costs 5
  conversions per model and is exactly what the method is meant to avoid.
- **Matched internal control:** uniform-T allocation with the **same total timestep budget** as the
  predicted allocation, so savings cannot come from simply spending less compute.
- **Calibration evidence:** task-book §2 shows graph-dependent minimum T (Cora T=4 gap 1.17 pp,
  PubMed T=4 gap 0.18 pp, CiteSeer T=4 gap 1.02 pp), i.e. a uniform budget is provably wasteful
  in the frozen data; the companion's `G^0.95` law (r = 0.990) supports predictability of the
  error scale from weights. A 25% saving over a 5-step grid is one grid step on average, a
  conservative target rather than a headline number.
- **Minimum:** on ≥2/3 held-out graphs, the predicted `T*` actually reaches ε (no under-provision),
  the shuffled-`ρ_n` control is worse, and L≤4 has zero bound counterexamples.
- **Expected strong:** on ≥3/3 held-out graphs the predicted `T*` is within one T-grid step of the
  grid-searched minimum and reaches ε; total timesteps fall by **≥ 25%** relative to the uniform-T
  baseline at matched accuracy; the matched-budget uniform control does **not** reach ε on ≥2/3
  graphs, so the gain is attributable to allocation rather than to spending more compute.
- **Failure:** any held-out graph under-provisioned by more than 2× noise floor (gap > ε + 0.8 pp),
  hit rate < 2/3, savings < 0%, or the shuffled-`ρ_n` control matching the real allocation.
- **Implementation path:** `latency_alloc.py` uses the C2 closed form and a margin proxy computed
  from the trained ANN; constants and the held-out graph list are committed at pre-registration
  before any held-out measurement.
- **Prototype check:** on the three fitted graphs only, closed-form prediction must land within one
  T-grid step for ≥6/9 (graph × L) cells before held-out evaluation is unlocked.
- **Budget:** 30 h, 10 GB, 7 seeds, 90 search trials. Re-training per cell is avoided by reusing
  one ANN per (graph, seed) as in the companion's corrected WP15 design (7 trainings per graph,
  not 49), which removes the exact budget overrun that previously made squirrel infeasible.
- **Reviewer questions answered:** main — "what can I compute with the bound?"; ablation — "is the
  saving from the geometry term or from a smaller budget?"; robustness — "does it transfer to an
  unseen graph?"; efficiency — timesteps and retrain count are reported directly.
- **Test isolation:** held-out graph identities, ε, the T grid and the fitting constants are frozen
  in a committed pre-registration; no held-out result may be used to re-fit a constant.
- **Stop–return condition:** if the prototype misses 6/9, or a held-out failure occurs, return to
  C2 (the bound) before C3; do not tune on held-out graphs. A persistent failure triggers the
  autonomous correction loop and, if needed, the within-family pivot to a bound-derived
  model-selection rule recorded in `idea-cards.md`.

---

## Claim C4 — low-latency Pareto and plug-in hosts

- **Claim:** at T≤4 the conversion is not dominated by reproduced direct-training SNNs on
  (accuracy, spike/SynOps proxy, retrain count), and the correction plugs into mean, sum and
  symmetric-normalized aggregation without code changes to the neuron.
- **Mechanism:** conversion needs one ANN training for the whole T grid, whereas direct training
  retrains per T; the bias correction is an affine offset independent of the aggregation kernel.
- **Assumptions:** identical hyperparameter search budget for conversion and direct-training arms;
  the efficiency proxy is stated as a proxy; protocol differences for external arms are labelled.
- **Falsifying ablation:** remove `β*`, swap to count decoding, and rerun with a 512-wide published
  architecture (the unfavourable row must be retained).
- **Dataset / split:** three Planetoid graphs, public splits, 7 seeds, full T grid.
- **Primary metric / direction:** accuracy (higher), spikes/node and SynOps proxy (lower),
  retrain count (lower); dominance is judged on the pair (accuracy, cost).
- **Simple baseline:** IF no-bias conversion.
- **Strongest feasible domain baseline:** ≥3 SGNNBench direct-training implementations; the task
  book's 5-day stop-loss applies with labelled public numbers as a fallback.
- **Matched internal control:** same-width, same-propagation-order conversion vs direct training.
- **Calibration evidence:** the companion's four-arm Pareto found conversion never dominated at
  T≤4 with 2–23× fewer SOPs, and its 512-wide published architecture was more accurate on two
  graphs — both facts are retained, including the unfavourable one. Task-book §2 gives T=4 gaps
  1.17/1.02/0.18 pp.
- **Minimum:** ≥2 direct-training arms reproduce under the frozen protocol and no T≤4 conversion
  point is dominated; H1/H2/H3 rows complete with no blank cell.
- **Expected strong:** ≥3 arms reproduce; conversion is never dominated on the (accuracy, cost)
  pair at T≤4; H1–H3 differ by < 1 pp at T=8; Table 1 has zero blanks including T=2.
- **Failure:** a direct-training arm dominates a T≤4 conversion point on both accuracy and cost,
  or fewer than 2 arms reproduce with no honest labelled substitute.
- **Implementation path:** `hosts.py` for the three normalizations, `pareto.py` for the dominance
  scan, `tables.py` generating Tables 1–3 from `results.csv`.
- **Prototype check:** H3 sym-norm runs end-to-end on Cora for one seed before the full grid.
- **Budget:** 36 h, 12 GB, 7 seeds, 200 search trials.
- **Reviewer questions answered:** main — "is the low-latency claim real?"; ablation — "which
  component earns it?"; robustness — "does it survive another aggregation?"; efficiency — the
  proxy definition and its limits are stated explicitly.
- **Test isolation:** the dominance rule and T grid are frozen before any arm is measured.
- **Stop–return condition:** if an arm cannot run within 5 working days, apply the task book's
  labelled stop-loss; if a reproduced arm dominates, record it and narrow the claim through a
  versioned correction rather than deleting the row.

---

## Cross-claim rules

- The four claims are independent enough that a C4 failure does not erase a C3 capability, but
  **P5 cannot pass unless C3 reaches its `expected_strong`**, because C3 is the designated
  Significance repair for the ≥9 target.
- No result may be promoted from `planned` to `observed` before P5A.
- Every experiment writes `config.yaml`, `log.txt`, `metrics.json` under `runs/<run_id>/` and a row
  in `registry/results.csv`; a run without a git commit is void.
- Gate failure enters the autonomous correction loop (contract C2). Lowering a binding target,
  inventing numbers, dropping negative results or silently changing the frozen constants is
  prohibited.
