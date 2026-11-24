# Research Guidance File

## Title / Topic

- Working title: Intra-Aggregation Misalignment and Bound-Derived Latency Allocation for Graph ANN-to-SNN Conversion.
- Target field: spiking neural networks, graph representation learning, ANN-to-SNN conversion theory.
- Target journal tier: CCF-A main-track conference (ICML / NeurIPS family).
- Candidate venues: ICML 2027 as the working target, NeurIPS 2027 as an alternative; neither CFP is published as of 2026-11-05, so both are assumptions rather than confirmed calls.
- Technique/method: exact per-layer conversion error identity, closed-form forward bias, order-invariant membrane readout, a neighbourhood-row-sum-weighted L-layer bound, and inversion of that bound into a per-model timestep budget.
- Selected application scenario: transductive node classification on public citation and heterophily graphs at low timestep budgets (T at most 4).

## Core Idea

A unit in a graph layer receives a sum over neighbours, and those neighbours fire at different
times; the layer therefore integrates a locally time-scrambled, per-node quantized rate. Writing
this down gives the exact identity `B_hat_l - B_l = (1-alpha) A_hat (E_{l-1} M_l)`, so the graph's
aggregation operator and its row sum `rho_n` sit **inside** the conversion error. ICML 2025
(Bojkovic, Wu, Gu, arXiv:2502.14487) instead studies random spike rearrangement across SNN layers
and repairs it with probabilistic spiking neurons. These are different physical phenomena: one is
deterministic and generated within a single aggregation, the other is stochastic and generated
between layers. The paper separates them experimentally, proves a `rho_n`-weighted L-layer bound
whose systematic term is mandatory rather than optional, and then inverts the bound's `T_L`
dependence into a per-model/per-layer minimum timestep `T*` that a practitioner can compute from
trained weights without sweeping the whole T grid. That last step is the designated new capability.

The priority claim "first conversion-based SNN framework for graphs" is deliberately **not** used
here: it belongs to an anonymous companion manuscript from the same project. This paper's claims do
not depend on that companion's results.

### Mechanism-Level Rationale

- Domain bottleneck: low-T graph conversion loses accuracy for reasons that existing image-domain bounds, which scale with a weight norm, cannot express.
- Why the chosen technique fits: the aggregation operator is linear, so its row sum and geometry enter the error recursion multiplicatively and can be bounded and inverted.
- What must be changed or adapted: the bias must be expressed per aggregation row sum rather than per layer alone; the decoder must be insensitive to spike order; the bound must carry a bias term; the T grid must be replaced by a bound-derived prediction.
- Why this is more than applying method X to dataset Y: the error identity contains the graph operator itself, and the resulting bound yields a computational rule (predict `T*`) that has no analogue in a CNN conversion paper.

## Paper Story

- Central scientific question: what physically generates graph conversion error, and can an exact bound tell a practitioner how few timesteps are enough before running a sweep?
- Intended reader and why the question matters: researchers deploying event-driven graph models under a latency budget, who currently choose T by trial and error.
- Domain/theory problem to design requirement to method choice: aggregation scrambles neighbour phases → the error must be written with `A_hat` inside it → an exact identity and a row-sum-weighted bound → inversion into a timestep budget.
- Expected contribution type: theory plus a bound-derived deployment rule, supported by controlled empirical mechanism separation.
- Opening problem: a controlled probe showing that the ICML 2025 cross-layer permutation phenomenon does not transfer to graphs, while an aggregation-internal perturbation does measurable harm.
- Why existing work is insufficient: TPP changes neuronal time randomness; FTBC zeroes an expected error in CNNs; SGNNBench contains no conversion entry; no published bound contains `rho_n`.
- Core insight: deterministic, aggregation-internal error is cancelled deterministically by a closed-form bias and is predictable from trained weights.
- What evidence should convince the reader: the 2x2 probe plus four-way neuron control, zero L at most 4 bound counterexamples, held-out `T*` savings against a matched uniform-T budget, and a never-dominated T at most 4 Pareto.
- Planned claim (not an observed finding): the bound-derived `T*` reaches a 1.5 pp target with at least 25 percent fewer timesteps on at least 3 of 3 held-out graphs.
- Finding to assess after experiments: unresolved until P5A; a negative held-out result is a legitimate finding and must be reported.
- Main claim: intra-aggregation deterministic misalignment is distinct from cross-layer stochastic misalignment, and its exact structure yields both a usable bound and a usable timestep rule.
- Boundary of the claim: two-layer transductive backbones, small and medium public graphs, spike/SynOps proxies rather than measured energy, and no claim of exceeding the source ANN.
- Skeptical-reviewer hook: "what can I compute with your bound that I could not compute before?" answered by the held-out `T*` experiment.
- Strongest competing paper and why this is still distinct: ICML 2025 TPP has a different error source, a norm-only bound and a stochastic fix; FTBC has an expectation-level CNN result; the anonymous companion has the identity but no `rho_n` bound and no timestep rule.

## Paper Outline

1. Introduction: opens with the controlled misalignment probes, states the two distinct phenomena, lists three contributions (mechanism separation, `rho_n`-weighted L-layer bound, bound-derived latency allocation), and declares the boundary of the claims.
2. Related Work: four clusters of conversion literature, the mandatory three-row bound contrast table, explicit FTBC inheritance, and the anonymous companion division-of-evidence statement.
3. Method: notation, the aggregation-internal error source, the exact identity, Theorem G1 (a)-(d) with its `rho_n` and mandatory bias term, the closed-form bias `beta*=theta/(2T)`, the order-invariant membrane decoder, the bound inversion into `T*`, the three aggregation hosts, and hardware implementability (no randomness, single hyperparameter, no extra storage).
4. Experiments and Results: frozen protocol, Table 1 method-by-T grid, the 2x2 probe and four-way neuron control, Table 2 Pareto against reproduced direct-training arms, Table 3 bound/measured conservatism and counterexample search, the held-out `T*` allocation result, plug-in hosts, and larger/heterophily graphs.
5. Discussion: positive evidence boundaries on efficiency and depth, protocol differences in external baselines, the failure-depth condition if one exists, threats to validity, and the relation to probabilistic neurons.
6. Conclusion: restates the mechanism separation and the bound-derived rule, with the limits attached to each.

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| Cora | https://github.com/kimiyoung/planetoid/raw/master/data | PyG states no explicit licence | fitted graph and G0 reproduction | 2708 nodes, 1433 features | 7 classes, accuracy | public 140/500/1000 | direct-public |
| CiteSeer | https://github.com/kimiyoung/planetoid/raw/master/data | PyG states no explicit licence | fitted graph | 3327 nodes, 3703 features | 6 classes, accuracy | public 120/500/1000 | direct-public |
| PubMed | https://github.com/kimiyoung/planetoid/raw/master/data | PyG states no explicit licence | fitted graph and G0 reproduction | 19717 nodes, 500 features | 3 classes, accuracy | public 60/500/1000 | direct-public |
| ogbn-arxiv | https://ogb.stanford.edu/docs/nodeprop/ | ODC-BY | held-out graph for `T*` | 169343 nodes, 128 features | 40 classes, accuracy | official temporal split | direct-public |
| chameleon | https://snap.stanford.edu/data/wikipedia.zip | SNAP gives no explicit licence; Geom-GCN version GPL-3.0 | held-out heterophily graph | 2277 nodes, 31421 edges | 5 classes, accuracy | declared version with duplicate-node treatment | direct-public |
| squirrel | https://snap.stanford.edu/data/wikipedia.zip | SNAP gives no explicit licence | stress cell only, excluded from claims if budget exceeded | 5201 nodes, 198493 edges | 5 classes, accuracy | declared version with duplicate-node treatment | direct-public |

Heterophily versions must name their source and duplicate-node handling, following Platonov et al.
(arXiv:2302.11640). All datasets are public HTTP with no approval, payment or account vetting.

### Baselines

- Simple baseline: IF conversion with no bias correction.
- Matched internal baseline: count decoding, no-bias, theta=2, TPP, TPP+`beta*`, and a uniform-T matched-budget allocation.
- Domain-standard baseline to rerun/adapt: SpikingGCN (IJCAI 2022) and SpikeGCL (ICLR 2024) under the frozen protocol.
- Strong recent baseline to rerun/adapt: SGNNBench (arXiv:2509.21342) implementations of SpikeGraphormer, DRSGNN and SiGNN, with a protocol-compatibility column.
- Strong recent baseline for literature context only: SGNNBench published numbers with explicit protocol labels; these rows cannot carry the main comparison.
- Technique-family baseline: QCFS / FTBC-style bias calibration and the three aggregation hosts H1 mean, H2 sum, H3 symmetric normalization.
- Upper-bound or oracle-style comparison, if applicable: the source ANN as an accuracy ceiling column (not ranked) and a full T-grid search as the timestep oracle.
- Strongest expected comparison: the TPP transplant under identical seeds, aggregation and backbone, plus the matched uniform-T allocation for the capability claim.

### Proposed Method Variants

- Main method: exact identity, closed-form per-row bias, order-invariant membrane decoder, and the G1(d)-derived per-layer `T*` allocation.
- Variant A: bias correction disabled, to isolate the systematic term.
- Variant B: count decoder instead of membrane decoder, to isolate the order-invariance property.
- Implementation notes: adapt the companion's L-layer core with its source commit and sha256 recorded; add `probes.py`, `tpp_neuron.py`, `bound.py`, `latency_alloc.py`, `hosts.py`, `pareto.py` and `tables.py`; TPP is re-implemented from ICML 2025 equations (8)-(13) because its full official code is unreleased; every run writes `config.yaml`, `log.txt`, `metrics.json` and one `results.csv` row with a git commit.

### Metrics

- Primary metric: node-classification accuracy and the accuracy gap to the source ANN in percentage points.
- Secondary metrics: paired bootstrap 95 percent intervals, mean and standard deviation over 7 seeds, the number of bound violations, the bound/measured conservatism ratio, `T*` prediction hit rate within one T-grid step, and the achieved gap at predicted `T*`.
- Efficiency metrics: spikes per node, SynOps proxy (`T` times edges times hidden width), training wall-clock seconds, and retrain count needed to cover the T grid; all declared as proxies, never measured neuromorphic energy.
- Statistical test / confidence reporting: paired bootstrap 95 percent intervals, noise floor 0.4 pp at T at least 8, and the 2x noise-floor rule (0.8 pp) below which any difference is reported as a tie.

### Required Ablations

- Ablation 1: 2x2 crossed probe (inter-layer permutation on/off times intra-aggregation phase randomisation on/off) with K=5 permutations.
- Ablation 2: four-way neuron control (IF, IF+`beta*`, TPP, TPP+`beta*`) at T in {2,4,8,16}.
- Ablation 3: shuffled-`rho_n` control and a matched uniform-T budget control for the bound-derived allocation.
- Robustness or subgroup analysis: L in {2,3,4} counterexample search, three aggregation hosts, larger ogbn-arxiv, heterophily chameleon/squirrel, and a 512-wide published architecture with its unfavourable row retained.
- Error analysis: bound/measured conservatism, failure-depth condition, spectral-normalisation and adaptive-threshold negative controls, and every partial or over-budget cell retained with its reason.

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Windows `C:/Users/xhf/miniconda3` env `base` (Python 3.13.13, torch 2.11.0+cu128) plus WSL2 Ubuntu 22.04 env `spikg` for third-party code without Windows wheels; legacy `spikinggcn36` for SpikingGCN.
- Optional remote fallback, only if authorized: none; remote compute is not authorized.
- GPU/CPU: RTX 3060 12 GB with CUDA on four Windows envs and WSL2 GPU pass-through; the device is a frozen protocol field because CUDA sparse-reduction order changed an earlier ANN by 0.69 pp; CPU fallback is explicit and logged.
- RAM: 12 GB GPU VRAM is the binding memory limit; host RAM not separately measured.
- Disk: 953 GB total, 513 GB free.
- Max runtime per run: no single experiment above 24 GPU-hours without a prior report; the four feasibility contracts total about 108 wall-clock hours.
- Max total runs: 7 seeds times the T grid times 8 Table-1 rows times 3 graphs, plus probes, hosts, counterexample search, held-out allocation and at least 3 direct-training arms; every row is logged even when it fails.
- Frozen train/validation/test identifiers and validation-only selection policy: Planetoid public splits, seeds 0-6 never extended, early stopping on validation only, and held-out graph identities frozen before any constant is fitted.
- Full search/trial ledger and held-out test isolation: 470 search trials across the four claims, committed pre-registration of constants, `epsilon=1.5 pp`, the T grid and the held-out graph list before measurement.
- CCFA packet path and feasibility-contract.json: `ccfa-startup-packet/` and `ccfa-startup-packet/feasibility-contract.json` in this run root.
- Resource budget exhaustion and next-candidate decision rule: cut S6 extras first, then the squirrel stress cell, then the largest graphs; never cut seeds, the T grid, Table 1 rows or the TPP transplant row.
- Scaling fallback: reuse one ANN per (graph, seed) instead of retraining per threshold, freeze the probe grid, and report any `infeasible-with-evidence` cell rather than inventing a value.
- Stopping criteria: G0 reproduction within 0.1 pp; S1 branch decision before any other campaign; the task book's 5-working-day stop-loss for a baseline that cannot run; any Gate failure enters the correction loop and writes to `notes/`.

## Expected Results

- Minimum acceptable result: S1 lands in branch A or B with TPP at least 1.5 pp behind at T=4 on at least 2 of 3 graphs; zero L at most 3 bound counterexamples with an explicit L=4 failure condition if needed; on at least 2 of 3 held-out graphs the predicted `T*` reaches a 1.5 pp gap without under-provisioning; at least 2 direct-training arms reproduce with no dominated T at most 4 conversion point.
- Strong result: branch B on all three graphs over 7 seeds with TPP+`beta*` at least TPP; zero counterexamples for all L at most 4 with mean conservatism between 3x and 8x; on at least 3 of 3 held-out graphs the predicted `T*` is within one T-grid step of the grid-searched minimum and reaches the target while total timesteps fall by at least 25 percent against a matched uniform-T budget; at least 3 direct-training arms reproduce and conversion is never dominated at T at most 4.
- Failure signal: branch C or D, any bound violation without a stated failure condition, a held-out gap above 2.3 pp at predicted `T*`, a `T*` hit rate below 2 of 3, negative timestep savings, a shuffled-`rho_n` control matching the real allocation, or fewer than 2 reproducible direct-training arms with no honest labelled substitute.
- What to do if minimum is not reached: preserve every run and negative result, enter the autonomous correction loop from the earliest affected stage, repair the evidence or narrow the claim under a versioned contract, and report to the author only when a material scope change is needed.
- Claim adjustment rule if expectations fail: never lower a binding target silently; the fallback is a bound-derived model-selection rule plus an exact negative result, recorded as a weaker but honest contribution.

## Figure/Table Decision Rules

Evidence-driven selection; no figure or table is locked before the results exist. Figure 1 is the
overall framework/architecture figure generated directly with image generation after the method is
finalized, showing only verified components. Data visualizations are scripted from `results.csv`.

- Required first figure type: GPT-generated framework/architecture figure after the method is finalized.
- Required experiment visualizations if supported by data: the S1 accuracy-versus-T phenomenon plot with baseline, permuted and corrected curves; a predicted-`T*` versus measured-minimum-T plot; and accuracy-versus-T plus accuracy-versus-cost Pareto curves.
- Required result tables if supported by data: Table 1 method-by-T grid, Table 2 Pareto and cost, Table 3 bound/measured/conservatism, and a three-row bound-contrast table in Related Work.
- Author or venue figure/table requirements, with source (if any): three-line tables with `booktabs`, 300 dpi figures, grey-scale-distinguishable colours, 8-page main text as an ICML-2026-derived working assumption; every in-text number carries a `% run:` comment and every table is generated by script.
- Evidence that may benefit from a visual: probe direction reversals, bound tightness across depth, timestep savings per graph, and cost-accuracy dominance.
- Rules for excluding weak or misleading plots: drop a plot if it hides a negative result, mixes devices or protocols, or implies an energy claim from a proxy; retain the underlying rows in `results.csv` regardless.
- Scientific claims for which a figure/table would aid inspection: mechanism separation, bound validity, held-out `T*` transfer, and low-latency non-dominance.
- Final count and placement are chosen after evidence stabilizes; no per-subsection quota applies.

## Traceability Checklist

| Requirement | Dataset | Baseline/method/ablation | Metric | Expected result | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|---|
| G0 reproduction within 0.1 pp | Cora, PubMed | frozen conversion kernel | accuracy gap | reproduce frozen T=8 values | protocol appendix row | yes |
| S1 mechanism separation | Cora, CiteSeer, PubMed | 2x2 probe and four-way TPP control | accuracy difference in pp | branch A or B, TPP behind by at least 1.5 pp at T=4 | phenomenon figure and Table 1 | yes |
| Table 1 full T grid | three fitted graphs | 8 method rows, three hosts | accuracy mean and std | zero blanks including T=2 | Table 1 | yes |
| G1(d) bound validity | three fitted graphs | L in {2,3,4} counterexample grid | violation count, conservatism | zero violations or stated failure depth | Table 3 | yes |
| Bound-derived `T*` capability | ogbn-arxiv, chameleon, squirrel stress | matched uniform-T and shuffled-`rho_n` controls | timesteps to 1.5 pp, hit rate | at least 25 percent savings on at least 3 of 3 held-out graphs | prediction plot and Table 3 | yes |
| Low-latency Pareto | three fitted graphs | at least 3 SGNNBench direct-training arms | accuracy, spikes, SynOps, retrain count | never dominated at T at most 4 | Table 2 and Pareto curves | yes |
| Plug-in hosts | three fitted graphs | H1 mean, H2 sum, H3 symmetric norm | accuracy difference | less than 1 pp at T=8 | Table 1 host rows | yes |
| Negative controls | fitted and held-out graphs | spectral norm, adaptive threshold, L=3 schedule, shuffled rho | accuracy difference | all fail as pre-registered | appendix table | yes |

## Citation Scope

- Must-cite foundational papers: Kipf and Welling (arXiv:1609.02907), Planetoid (arXiv:1603.08861), QCFS (arXiv:2303.04347), Hoeffding-type concentration used in the bound, and SpikingJelly (Science Advances 2023).
- Must-cite recent papers: TPP / ICML 2025 (arXiv:2502.14487), FTBC / ECCV 2024 (arXiv:2403.18388), SGNNBench (arXiv:2509.21342), SpikeGCL (arXiv:2305.19306), SpikeGraphormer (arXiv:2403.15480), MSG (arXiv:2410.17941), Platonov et al. (arXiv:2302.11640), and the 2024-2026 conversion-error preprints listed in `notes/G0_literature_map.md`.
- Dataset papers: Planetoid, OGB (arXiv:2005.00687), MUSAE (arXiv:1909.13021), plus the heterophily duplicate-node critique.
- Baseline papers: SpikingGCN (arXiv:2205.02767), SpikeNet (arXiv:2208.10364), GC-SNN (arXiv:2107.06865), DRSGNN (AAAI 2024), SiGNN (Pattern Recognition 2025), and SGNNBench.
- Search keywords: graph ANN-to-SNN conversion, spiking GNN conversion, temporal misalignment spiking, intra-aggregation phase error, probabilistic spiking neuron, forward temporal bias correction, low-latency spiking GNN, spike count energy proxy, reproducibility audit.
- Target recency: at least 36 distinct verified actually-cited works, with a strict majority in the frozen inclusive window 2023-2026; foundational works are retained with their real years.
- Excluded areas: neuromorphic hardware measurements, image-only SOTA tables used as direct comparators, and any method name that could not be verified (SSEL, DRSGCN).
- Reference scope/coverage appropriate to the question and venue: conversion theory, spiking GNN, graph benchmarks, probabilistic spiking neurons, audit and reproducibility, and efficiency proxies.
- Recency expectation and its source: f-research-v1 `references/citation-requirements.md`, with a four-year window justified because the spiking-GNN and low-latency conversion literature becomes substantive from 2023.
- Duplicate-paper risks: preprint versus PMLR versions of TPP and FTBC, arXiv versus ICLR versions of SpikeGCL and QCFS, and arXiv versus IJCAI versions of SpikingGCN; all resolved by DOI/arXiv/title scan at P12 and P14.

## Novelty And Feasibility Summary

- Literature/baseline map verdict: PASS; 12 arXiv queries and primary pages, no duplicate public work at the intersection.
- Dataset access verdict: PASS; all six graphs directly public with no approval flow.
- Task/evaluation verdict: PASS; node classification, fixed public splits, accuracy, 7 seeds, bootstrap CI, frozen T grid.
- Theoretical fit verdict: PASS; the aggregation operator is inside the error identity, with a named falsifier.
- Novelty verdict: PASS with a declared same-group boundary; the priority claim is not reused.
- Hardware feasibility verdict: PASS; RTX 3060 12 GB, 12 cores, 513 GB free, about 108 wall-clock hours.
- Baseline/ablation verdict: PASS with one labelled limitation; no released checkpoints and no full TPP codebase.
- Effectiveness plausibility verdict: PASS; graph-dependent minimum T and a r=0.990 error-scale law calibrate the target.
- Q2+ story verdict: PASS; the decisive reviewer question has a named held-out experiment.

## Theoretical Feasibility Audit

- Mechanism expected to help: the aggregation operator's row sum and geometry enter the error recursion, so error scale is predictable from trained weights and the timestep budget can be inverted from a bound rather than searched.
- Required assumptions: bounded activations, fixed normalized aggregation, ReLU homogeneity, rate-coded neurons, shared weights, and a margin proxy computable from the ANN alone.
- Supporting literature: the exact identity's numerical verification in the companion project (residual at most 2e-6), ICML 2025 Theorem 1 (a)-(d), FTBC's expectation-level bias calibration, and the companion's measured `G^0.95` depth law at r=0.990.
- Falsifying ablation: the shuffled-`rho_n` control and the matched uniform-T budget control, plus the L in {2,3,4} counterexample grid.
- Critical failure mode: a bound that is true but too loose to invert, or a `T*` that under-provisions an unseen graph; both have explicit failure conditions in the feasibility contract.

## Story Strength Audit

- Why a top-journal reviewer should care: it separates two mechanisms that the literature conflates and turns an exact error structure into a deployment rule, rather than adding another accuracy row.
- Strongest incrementality threat: the same project's anonymous companion manuscript, which already owns the identity and the bias but scored 8 for lacking a new capability.
- Decisive distinguishing experiment: the pre-registered held-out `T*` allocation with a matched uniform-T budget and a shuffled-`rho_n` control.
- Strong-paper result threshold: at least 25 percent timestep savings at matched accuracy on at least 3 of 3 held-out graphs, zero L at most 4 counterexamples, and a `ccf-paper-reviewer` full-mode stance of at least 9.
- Honest fallback story if only partially successful: an exact bound with a stated failure depth, a mechanism-separation result, and a bound-derived model-selection rule, published with the failed allocation recorded as a negative result.

## Constraints and Preferences

- Writing preference/source: English, formal academic register, contribution-led evidence-supported argument; f-research-v1 `references/scientific-writing-contract.md`.
- Protected sections or edit scope/source: every sentence carrying a `% run:` comment, every scripted table, Theorem G1 (a)-(d), the FTBC attribution, and the legal/illegal phrasing list in task book section 10; source `contracts/execution-contract-v1.md`.
- Journal page/word/figure requirements and source: 8-page main text plus unlimited references and appendix, derived from ICML 2026 official rules because the 2027 CFPs are unpublished; recorded as a working assumption, not a verified constraint.
- Things the workflow must do: baseline-first execution, pre-register before every experiment, script all tables from `results.csv`, keep negative results, freeze constants before held-out measurement, use `ccf-paper-reviewer` for every score, and report `workflow_complete` separately from `submission_ready`.
- Things the workflow must avoid: hand-typed table numbers, seed shopping, silent device mixing, deleting unfavourable rows, claiming SOTA or energy savings, claiming to beat ICML 2025, inventing author or venue facts, and any submission or upload action.
- Preferred writing language: English.
- Preferred LaTeX/template/venue style: ICML-style official double-blind LaTeX, `booktabs` three-line tables, 300 dpi figures, grey-scale-safe colours; the official style file is acquired and verified at P20 when a venue is confirmed.

## Citation policy and pending facts

The binding f-series default applies: `min_unique=36`, `as_of=2026`, `recent_window_years=4` giving
the inclusive 2023-2026 window, and `require_recent_majority=true`, verified by a separate
quantity/recency arithmetic at P12 and P14. Author names and affiliations, target-venue
confirmation, code/data release route, funding and competing-interest declarations, generative-AI
disclosure and submission approval are a pending checklist owned by the author; they do not block
scientific stages but keep `submission_ready=false` until resolved. No such fact is inferred.
