# Claim–evidence matrix (`ccf-experiment-designer`, design mode)

**Venue and assumptions:** CCF-A main ML track (ICML/NeurIPS family), double blind, 8-page main
text as a working assumption. No results exist yet; every cell below is a **planned** evidence
requirement. No numeric outcome is asserted.

## Claim–evidence matrix

| id | main claim | reviewer question | required evidence | baseline / comparator | primary metric | falsifier | priority |
|---|---|---|---|---|---|---|---|
| C1 | Graph conversion error is generated inside one neighbourhood aggregation and is deterministic; ICML'25's cross-layer stochastic misalignment is a different phenomenon | "isn't this just TPP on graphs?" | S1-a inter-layer permutation probe, S1-b intra-aggregation phase randomisation, S1-c TPP transplant four-way control, 2×2 crossed design | IF no-bias / IF+`β*` / TPP / TPP+`β*` under identical seeds, aggregation and backbone | accuracy difference in pp at T∈{2,4,8,16} | branch C (TPP ≥ ours) or D (intra-aggregation randomisation helps) | P0 (must precede everything) |
| C2 | An exact per-layer identity yields a `ρ_n`-weighted L-layer error bound with a mandatory systematic-bias term | "is the bound true, and is it tight enough to use?" | Theorem G1 (a)–(d), appendix proof, symbol table, L∈{2,3,4} counterexample search, bound/measured conservatism table (Table 3) | `‖W‖∞·θ/T` image-domain form; companion empirical `G^0.95` law as calibration only | bound violation count; bound/measured ratio | any L≤4 counterexample without a stated failure-depth condition | P1 |
| C3 | **The bound can be inverted into a per-model/per-layer minimum timestep `T*` that reaches a target error with fewer steps than a uniform-T budget, on held-out graphs** | "what can I compute now that I could not before?" | bound inversion with constants frozen **before** measurement; predicted `T*` vs grid-searched true minimum; matched uniform-T control; held-out graphs never used for constant fitting | uniform-T (largest required T across the panel) and grid-search oracle | prediction hit within one T-grid step; total timesteps saved at matched accuracy | under-provisioned `T*` on any held-out graph by > 2× noise floor | P0 (binding `expected_strong`) |
| C4 | At T≤4 the conversion is not dominated by reproduced direct-training SNNs, and the correction plugs into three aggregation hosts | "is the low-latency claim real under a unified protocol?" | Table 1 full T grid × 8 rows × 3 graphs × 7 seeds; Table 2 Pareto; H1 mean / H2 sum / H3 sym-norm plug-in rows | ≥3 verifiable SGNNBench direct-training arms + internal four-arm Pareto | accuracy, spikes/node, SynOps proxy, retrain count | a direct-training point dominating our T≤4 cell on both accuracy and cost | P1 |

## Dataset / benchmark needs

Cora, CiteSeer, PubMed (Planetoid public splits 140/500/1000, 120/500/1000, 60/500/1000),
ogbn-arxiv (OGB temporal split), chameleon/squirrel (SNAP; exact version and duplicate-node
treatment declared per arXiv:2302.11640). All directly public. Held-out graphs for C3 are frozen
before any constant is fitted and may not be used for method selection.

## Baseline matrix

| class | baseline | role |
|---|---|---|
| simple | IF conversion, no bias correction | floor |
| matched internal | count decoding, no-bias, `θ=2`, TPP, TPP+`β*`, uniform-T | isolates each mechanism |
| technique-family | QCFS/FTBC-style bias calibration; three aggregation hosts | orthogonality and plug-in |
| strong recent, direct rerun | ≥3 SGNNBench implementations (SpikingGCN, SpikeGCL or SpikeGraphormer, DRSGNN/SiGNN) | external Pareto anchors |
| literature context | SGNNBench published numbers, labelled with protocol differences | not allowed to carry the main comparison |
| upper bound | source ANN accuracy (ceiling column, not ranked) | reference |

## Main experiments

1. G0 reproduction: Cora/PubMed T=8 within 0.1 pp of the frozen values, device frozen.
2. S1 three probes and the 2×2 crossed design; branch decision before any other campaign.
3. Table 1: 8 rows × T∈{2,4,8,16,32} × 3 graphs × 7 seeds, T=2 bad values retained.
4. Three aggregation hosts on the full T grid.
5. Theorem G1 verification and L∈{2,3,4} counterexample search with conservatism quantification.
6. C3 latency allocation: fit constants on the three fitted graphs only, freeze them in a committed
   pre-registration, then predict and measure on held-out graphs.
7. ≥3 direct-training arms under the frozen protocol, with the 5-day stop-loss from the task book.

## Ablations

- Bias removal (`β*`), decoder swap (membrane vs count), threshold scaling, spectral normalisation,
  L=3 per-layer schedule (negative control), adaptive `q999` threshold (negative control),
  uniform-T budget control, and a shuffled-`ρ_n` control for the bound's causal term.
- Every ablation has a pre-registered expected direction and a failure condition.

## Robustness / failure / efficiency

7 seeds (0–6) fixed, paired bootstrap 95% CI, noise floor 0.4 pp at T≥8, 2× noise-floor rule for
any claimed improvement, mean±std, device/log/commit recorded per run. Efficiency is reported only
as spike counts, SynOps proxies and wall-clock training time — never measured neuromorphic energy.
Negative results, partial cells and budget overruns are retained in `notes/` and in `results.csv`.

## Result tables or figure specs

Tables 1 (method × T), 2 (Pareto/cost), 3 (bound/measured/conservatism), and a Table 0 three-row
contrast of the ICML'25 bound vs ours. Figure 1 is the framework/architecture figure generated
directly with image generation; the S1 phenomenon plot, the `T*` prediction-vs-measured plot and
the Pareto curves are scripted from `results.csv`. Final count and placement are decided after
evidence stabilizes. No per-subsection quota.

## Missing values

All result cells are missing at design time. Unknowns: the true S1 branch, whether G1(d) holds at
L=4, whether `T*` generalizes, which SGNNBench arms run under the frozen protocol, and the 2027
venue rules. These are recorded as open assumptions, never filled with plausible numbers.

## Execution priority

S0/G0 reproduction → S1 branch decision (hard stop) → Table 1 + three hosts → G1(d) proof and
counterexample search → **C3 held-out `T*`** → direct-training Pareto → optional S6 extras
(sparsity, multi-view) only if the binding claims pass. S6 is the first thing cut under budget
pressure, per the task book's cut order.

## No-fabrication status

No experiment has been run for this manuscript. All numbers in the task book §2 are calibration
targets and G0 reproduction targets, not results of this run. Companion A/B numbers are external
immutable evidence, reaccepted only with hashes and commits, never rewritten as this run's rows.

## Next CCFA owner

`ccf-idea-reviewer` for the pre-experiment adversarial review at P1B; `ccf-integrity-auditor` in
`claim-audit` mode over these **planned** claims. Later: `ccf-visual-composer` for figure layout and
`ccf-paper-reviewer` for the full manuscript review.
