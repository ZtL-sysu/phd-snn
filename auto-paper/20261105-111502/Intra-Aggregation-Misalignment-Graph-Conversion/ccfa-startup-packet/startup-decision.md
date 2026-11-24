# Startup decision

**Decision: `proceed`.**

Rationale in the exact order the gates ran. `CCFA-startup` completed first (all seven packet
artifacts present, red-team conditions F1/F2 written into the execution contract), so G0 may be
recorded against this packet.

**CCFA-startup.** The orchestrator named the owner of every stage and recorded the six risks; the
idea optimizer produced a single coherent card after rejecting four contradictory concretizations;
the literature searcher produced a closest-work table with a public-source policy; the independent
red-team review returned `revise → accept-to-develop` with two fatal-if-unaddressed concerns; the
experiment designer produced a claim–evidence matrix and the binding feasibility contract. Both
fatal concerns are now closed *at the design stage*: F1 is the binding `expected_strong` capability
(C3), and F2 is the author's 2026-11-05 decision (independent third paper, anonymous companions, no
reused priority claim). Neither is closed by a result — they are closed by a pre-registered test and
an author decision, which is the correct closure at this stage.

**G0 — recent literature and baseline map: PASS.** 12 arXiv full-search queries plus PMLR, ICML,
ECVA, ACM, NeurIPS, OpenReview, GitHub, OGB, PyG and SNAP primary pages. Current strong baselines
identified with official URLs, code/checkpoint status, datasets, metrics and local-rerun role.
Direct baselines (`must-rerun`, `adaptation-attempt`) are separated from literature-context rows.
Source conflicts with the task book are recorded, not smoothed over.

**G1 — public dataset access: PASS.** Planetoid (raw GitHub files), ogbn-arxiv (OGB loader,
ODC-BY), chameleon/squirrel (SNAP zip) are directly downloadable with no approval, payment, NDA or
account vetting. Licences and the heterophily duplicate-node caveat are recorded.

**G2 — task and evaluation validity: PASS.** Node classification with fixed public splits, accuracy
as the primary metric, 7 seeds, paired bootstrap CI, a frozen T grid, a measured noise floor and a
2× noise-floor decision rule. The evaluation protocol is written before any result exists.

**G3 — theoretical fit: PASS, mechanism-level.** The error identity places the aggregation operator
`Â` and its row sum `ρ_n` inside the recursion. This is a concrete algebraic reason the graph case
differs from the image case, not "apply method X to dataset Y". The theoretical audit names the
assumptions, the supporting literature and the falsifying ablation. The proof itself is P4 work; G3
requires the mechanism and falsifier, not a finished theorem.

**G4 — novelty and non-duplication: PASS with a declared boundary.** No published work matches the
method family, task, dataset class and central claim at once (`prior-art-opportunity-map.md`).
The genuine overlap is **within the same project**: companions A/B own the identity, `β*`, the
membrane decoder and the Pareto. The author chose the independent-third-paper route; the new paper
claims only the mechanism separation, the `ρ_n`-weighted L-layer bound and the bound-derived
latency allocation. Confidence is medium-high and bounded by the search coverage; a final
pre-submission sweep is recorded as an open item.

**G5 — hardware and runtime: PASS.** RTX 3060 12 GB with CUDA on four Windows Conda envs and WSL2
pass-through, 12 cores, 513 GB free. The four contracts total ~108 h wall clock, ≤12 GB memory,
7 seeds and 470 search trials. The C3 design explicitly reuses one ANN per (graph, seed) instead of
re-training per threshold, which removes the budget overrun that made a companion cell infeasible.
Scale repair is defined (drop the largest graphs first, keep all seeds and the full T grid).

**G6 — strong baselines and ablations: PASS with one labelled limitation.** Four baseline classes
are present, including ≥3 recent authoritative SGNNBench implementations planned as direct reruns,
plus ≥7 mechanism-isolating ablations and negative controls. The one partial gate, inherited from
the domain, is that **no published spiking-GNN method ships checkpoints** and TPP's full codebase is
unreleased. The decision is to re-implement TPP from the paper's equations with a recorded unit
test, and to label any literature-only row with its protocol difference. Proceeding with the
limitation stated is honest; claiming the gate is fully met would not be.

**G7 — strong-result plausibility: PASS.** Every binding claim has a mechanism, a falsifying
ablation, calibrated `minimum`/`expected_strong`/`failure` conditions traced to measured evidence,
an implementation route, a prototype milestone, a finite compute/seed/search budget, and a
stop–return condition. The C3 target (≥25% timestep saving at matched accuracy on ≥3/3 held-out
graphs) is calibrated from the frozen task-book numbers showing graph-dependent minimum T, not from
a desired headline. No arbitrary accuracy gain is promised.

**G8 — story strength: PASS.** A skeptical reviewer's decisive question ("what can I compute with
your bound that I could not before?") has a named experiment. The strongest incrementality threat
(the companion's own 8-score manuscript) is answered by a new capability, not by reframing. If C3
fails, the honest fallback is a bound-derived model-selection rule plus an exact negative result —
a weaker but still publishable diagnostic paper, which the contract states explicitly.

**Blocking issues found:** none that cannot be handled by labelling. Two scientific risks remain
open by design and must not be quietly upgraded later: (1) whether the bound holds at L=4, and
(2) whether `T*` transfers to held-out graphs. Both are pre-registered with failure conditions.
Two administrative facts remain author-owned: the unpublished 2027 venue rules and the eventual
code-release route. Neither is inferred.

This `proceed` authorizes G0 only as the next recorded stage, then G1–G8 in canonical order,
`validation`, and `handoff` to `f-research-v1`. It does **not** authorize submission, upload,
publication or any external action.
