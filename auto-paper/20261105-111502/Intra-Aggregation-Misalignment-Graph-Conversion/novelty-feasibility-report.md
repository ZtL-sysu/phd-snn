# Novelty and feasibility report

## Verdict

`proceed` — with a declared same-group overlap boundary and one labelled baseline limitation.
Date: 2026-11-05. Public-literature novelty confidence: medium-high, bounded by the search coverage.

## Novelty delta after subtracting the nearest prior work

| closest work | what it already owns | what remains for this paper |
|---|---|---|
| ICML 2025 TPP (arXiv:2502.14487) | cross-layer stochastic misalignment, probabilistic neuron, expectation identities, `‖W‖∞·θ/T` bound | a different error source inside `Â`, a `ρ_n`-weighted bound with a mandatory bias term, and a bound-derived timestep rule |
| FTBC (ECCV 2024, arXiv:2403.18388) | forward-only temporal bias for CNN conversion, expected error zeroed per timestep | an **exact** (not expectation-level) graph identity with `ρ_n`, plus explicit attribution of the bias mechanism |
| SGNNBench (arXiv:2509.21342) | unified spiking-GNN protocol, 9 methods, 18 datasets | a conversion entry and a codebase-level anchor; the benchmark has no conversion arm |
| 2026 conversion-error preprints (2608.13952, 2601.21778) | error amplification and residual-potential alignment, non-graph | graph aggregation geometry inside the bound |
| Anonymous companion (same project, unpublished) | the exact identity, `β*`, membrane decoder, Pareto, threshold law, empirical `G^0.95` law | **only** the controlled mechanism separation, the `ρ_n`-weighted L-layer bound, and the bound-derived `T*` capability |

After subtraction, no "first conversion framework" claim remains available. The author's decision
(`contracts/execution-contract-v1-addendum-C8.md`) makes this an independent third paper with an
anonymous companion citation and an explicit division-of-evidence statement.

## Search record

12 arXiv `searchtype=all` queries plus PMLR, ICML, ECVA/ECCV, ACM DL, NeurIPS, OpenReview, GitHub
READMEs, OGB, PyG docs and SNAP, accessed 2026-11-05. Zero hits for `spiking GNN ANN conversion`;
the latest 50 spiking-GNN and 50 ANN-SNN-conversion papers have an empty intersection. Full URLs
and the 52-entry verified reference candidate list are in `notes/G0_literature_map.md`.

Coverage limits: Chinese databases, non-arXiv proceedings full text, unpublished external
submissions, and anything after 2026-11-05 were not searched. A final pre-submission sweep of
Semantic Scholar and OpenReview is recorded as an open item in `startup-decision.md`.

## Feasibility summary

| gate | verdict | decisive evidence |
|---|---|---|
| G0 literature/baselines | pass | primary-source baseline matrix with code/checkpoint status |
| G1 public data | pass | six direct-public graphs, no approval flow |
| G2 task/evaluation | pass | fixed splits, accuracy, 7 seeds, bootstrap CI, noise floor |
| G3 theory | pass | `Â` inside the identity, named falsifier |
| G4 novelty | pass with boundary | no public duplicate; same-group overlap author-managed |
| G5 hardware | pass | RTX 3060 12 GB, WSL GPU pass-through, ~108 h, ≤12 GB |
| G6 baselines/ablations | pass with limitation | ≥3 direct reruns, ≥7 ablations, no released checkpoints |
| G7 strong result | pass | four calibrated contracts with prototype and stop-return conditions |
| G8 story | pass | held-out `T*` answers the decisive reviewer question |

## Honest risks carried forward

1. The binding capability (C3) has not been tested; a failure is a legitimate negative result but
   removes the intended +1 route to a score of 9.
2. Whether the bound holds at L=4 is open by design.
3. TPP's full official code is unreleased, so the transplant is a re-implementation with a recorded
   unit test, not a reproduction of their repository.
4. ICML 2027 and NeurIPS 2027 CFPs are unpublished; page and template rules are working assumptions.
5. Three same-topic manuscripts from one group require an airtight division-of-evidence statement.

No dataset, citation, benchmark result or access status in this report was invented.
