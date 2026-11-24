# Prior-art opportunity map (`ccf-literature-searcher`, standard mode)

**Search purpose:** novelty check (G4), closest-work clustering, baseline/code discovery, and
reviewer-risk diagnosis for a graph ANN→SNN conversion paper positioned against ICML'25.

**Queries used** (arXiv `searchtype=all`, plus primary pages; all accessed 2026-11-05):
`graph neural network ANN to SNN conversion`; `spiking GNN ANN conversion`;
`spiking graph neural network conversion`; `spiking graph neural network` (latest 50);
`ANN-SNN conversion` (latest 50); `temporal misalignment spiking`;
`aggregation misalignment spiking`; `probabilistic spiking neuron`;
`SSEL spiking graph`; `spiking neural network energy efficiency FLOPs`.
Primary sources: PMLR v267, ICML 2025 virtual, ECVA ECCV 2024, ACM DL, NeurIPS 2026/2027 CFP,
OpenReview, arXiv abs/html/pdf, GitHub READMEs, OGB, PyG docs, SNAP.

**Source policy:** primary or high-confidence venues only (PMLR, arXiv, OpenReview, CVF/ECVA, ACM,
official project pages and repositories). Low-quality/predatory/inaccessible sources excluded.
Broad web search was used only to locate primary links; a Chinese-language-heavy general search
returned popular-science pages that were **discarded**, not used as evidence. Every included paper
has a stable URL, year/venue, paper type and relevance rationale. Candidate deduplication by title
and arXiv ID was applied; preprint/published pairs (e.g. ICML'25 / arXiv:2502.14487) are one work.

**Folder written:** this packet plus `notes/G0_literature_map.md` (full URL ledger and the 52-entry
verified reference candidate list) and `literature-baseline-matrix.md` (baseline roles).

## Top paper table

| # | work | year / venue | type | insight | completeness | numeric evidence | relevance |
|---|---|---|---|---|---|---|---|
| 1 | TPP, arXiv:2502.14487, ICML'25 | 2025 / PMLR 267 | method + theory | 5 | 4 | 5 | **the anchor**: cross-layer random rearrangement, Theorem 1 (a)–(d), `‖W‖∞·θ/T` |
| 2 | FTBC, arXiv:2403.18388, ECCV'24 | 2024 / ECCV | method + theory | 4 | 4 | 4 | mechanism ancestor of `β*`; expected-error zeroing, CNN only |
| 3 | SGNNBench, arXiv:2509.21342 | 2025 / preprint | pure benchmark | 3 | 5 | N/A benchmark | unified protocol, 9 methods × 18 datasets, no conversion entry |
| 4 | SpikingGCN, arXiv:2205.02767, IJCAI'22 | 2022 / IJCAI | pure method | 4 | 3 | 3 | most-cited spiking GNN number; Split I/II ambiguity |
| 5 | SpikeGCL, arXiv:2305.19306, ICLR'24 | 2024 / ICLR | pure method | 4 | 4 | 4 | strong self-supervised spiking encoder, releases code |
| 6 | SpikeGraphormer, arXiv:2403.15480 | 2024 / preprint | pure method | 4 | 4 | 4 | split flag changes Cora by ~10.7 pp; codebase anchor |
| 7 | QCFS, arXiv:2303.04347, ICLR'22 | 2022 / ICLR | method + theory | 4 | 4 | 4 | standard conversion host used by both TPP and FTBC |
| 8 | MSG, arXiv:2410.17941, NeurIPS'24 | 2024 / NeurIPS | pure method | 4 | 3 | 3 | recent authoritative spiking GNN, SGNNBench implementation |
| 9 | Residual Membrane Potential Alignment, arXiv:2608.13952 | 2026 / preprint | theory/proof | 3 | 3 | 3 | nearest conversion-error analysis, non-graph |
| 10 | Error Amplification in Continuous Control, arXiv:2601.21778 | 2026 / preprint | theory/proof | 3 | 3 | 3 | depth-like error amplification, non-graph |
| 11 | Platonov et al., arXiv:2302.11640 | 2023 / preprint | empirical finding | 5 | 4 | 4 | heterophily benchmark duplicate-node caveat |
| 12 | GC-SNN, arXiv:2107.06865, IJCAI'21 | 2021 / IJCAI | pure method | 3 | 2 | 3 | earliest spiking GNN; no official code |

Scores are 1–5 on insight / completeness / numeric evidence, as required by the skill's search
policy; a pure benchmark paper receives `N/A benchmark` instead of a numeric-evidence score.

**Near-miss / negative-signal cluster:** One-Spike SNN (arXiv:2403.08786) is the only hit for
"graph + ANN→SNN conversion", yet it is a CNN phase-coding method with no graph operator and no
exact identity. This near miss is the clearest evidence that the intersection is empty.

## Closest-work clusters

| cluster | already covered | under-tested | differentiation route |
|---|---|---|---|
| Image ANN→SNN conversion error (TPP, FTBC, QCFS, 2024–2026 preprints) | expectation identities, `‖W‖∞·θ/T` bounds, bias calibration, low-latency CNN/Transformer | graph aggregation operator, `ρ_n`, neighbourhood geometry, deterministic intra-aggregation error | put `Â` and `ρ_n` **inside** the identity and bound; show the bias term is mandatory |
| Spiking GNN direct training (SpikingGCN, SpikeGCL, SpikeGraphormer, MSG, DRSGNN, SiGNN, SGNNBench) | accuracy, energy proxies, unified protocols, large graphs | conversion methods entirely — SGNNBench has **no conversion entry** | first conversion-side comparison under a unified protocol, with codebase anchors |
| Probabilistic / stochastic spiking neurons | stochastic firing theory, RNG hardware cost | whether stochasticity helps a **deterministic** aggregation bias | four-way TPP transplant control, pre-registered expectation |
| Reproducibility / audit | split-mixing findings, protocol variance (companion A) | converting audit findings into a conversion-method comparison | cite as anonymous companion; keep this paper's claims independent |

## Opportunity map

1. **Mechanism gap.** ICML'25's fix changes the neuron's time randomness; graph error enters through
   the aggregation operator's row sum. A 2×2 probe can separate them physically — no published
   work does this.
2. **Theory gap.** No existing bound contains `ρ_n`, neighbourhood geometry, or a mandatory
   systematic-bias term. G1(d) fills it and, unlike a looser empirical law, is invertible.
3. **Capability gap.** No conversion work predicts a per-model/per-layer minimum `T*` before
   running the T grid. This is the practitioner-usable result the companion B review asked for.
4. **Evaluation gap.** SGNNBench has no conversion entry; a conversion arm under a stated protocol
   with codebase anchors is a genuine addition rather than another leaderboard row.

## Benchmark / dataset candidates

Planetoid (Cora/CiteSeer/PubMed, public 140/500/1000 etc.), ogbn-arxiv (ODC-BY, temporal split),
chameleon/squirrel (SNAP; version and de-duplication must be declared per arXiv:2302.11640).
All directly public, no approval flow. Full URLs in `notes/G0_literature_map.md` §4 and
`dataset-access-log.md`.

## Novelty and positioning risks

- Public-literature duplication: **not found** (medium-high confidence, bounded coverage).
- Same-group overlap: **real and author-managed** — see `notes/overlap-risk-AB.md`.
- Incremental-risk: FTBC's expected-error zeroing can be mistaken for our `β*`; the identity vs
  expectation, graph vs CNN, and `ρ_n`-weighted vs norm-weighted distinctions must be explicit.
- Terminology risk: ICML'25 never uses the exact phrase "inter-layer misalignment"; quote its own
  wording.
- Baseline risk: TPP code is unreleased, no checkpoints exist, and several SGNN baselines are
  link-prediction methods; protocol columns are mandatory.

**Quality-score rationale:** scores above reflect what the linked primary source actually reports;
no score was inferred from a snippet or a secondary summary.

**Recommended next module:** `ccf-idea-reviewer` (standard, strict) using this closest-work table,
then `ccf-experiment-designer` (design mode).

**Checklist status:** 11/11 mandatory items completed. Reusable report written locally. The
handoff to `ccf-idea-reviewer` is part of the authorized integrated CCFA startup.
