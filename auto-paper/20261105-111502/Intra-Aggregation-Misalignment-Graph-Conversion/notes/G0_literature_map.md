# G0 — literature, baseline and novelty map

Collected 2026-11-05 by an independent literature-research agent. Method: 12 arXiv
`searchtype=all` queries plus primary-source pages (PMLR, ICML, ECCV, ACM DL, NeurIPS,
OpenReview, GitHub raw README, OGB, PyG docs, SNAP). All access dates 2026-11-05.
**This file is material for G0; G0 is not recorded passed until CCFA-startup passes.**

Coverage limit: "not found" means not found within arXiv + the official pages above. Chinese
databases, non-arXiv full-text proceedings, unpublished submissions and anything after 2026-11-05
are outside this sweep. The project's own unpublished companion manuscripts are handled separately
in `notes/overlap-risk-AB.md`.

## 1. G4 novelty verdict (for the public literature)

**Core contribution not duplicated (confidence: medium-high, not absolute).**

- `spiking GNN ANN conversion` on arXiv full search: **0 hits**.
- `graph neural network ANN to SNN conversion`: 1 hit, arXiv:2403.08786 (One-Spike SNN, CNN phase
  coding), not a graph method and has no exact identity.
- Latest 50 `spiking graph neural network` hits (2025-04 → 2026-10): all direct-training /
  architecture / benchmark work (SGNNBench, GT-SNT, Geometry-Aware Spiking GNN, ChronoSpike,
  Spiking Heterogeneous GAT, Photonic Spiking GNN, MorphSNN, MSGAT...), **no conversion + error
  identity**.
- Latest 50 `ANN-SNN conversion` hits (2024-07 → 2026-10): all CNN/Transformer/LLM/control/detection
  (QCFS, FTBC, PASCAL, One-Timestep, Differential Coding, Error Amplification, Residual Membrane
  Potential Alignment...), **none on graph-structured data**.
- `"intra-aggregation" misalignment spiking`: hits belong to federated learning, point clouds and
  multimodal work, unrelated to within-neighbourhood-aggregation phase skew.
- `temporal misalignment spiking`: the only ANN–SNN conversion hit is the ICML'25 original;
  no graph transfer of the TPP neuron.

Nearest neighbours that must be positioned explicitly (not duplicates, but incremental-risk):
FTBC (ECCV 2024) — expected error zeroed per timestep via a forward-only bias, CNN, not a graph and
not an exact identity; arXiv:2608.13952 (Residual Membrane Potential Alignment, 2026) and
arXiv:2601.21778 (Error Amplification, 2026) — conversion error analyses, non-graph.

Terminology caution: the ICML'25 paper uses *temporal misalignment* and describes random spike
rearrangement **across layers**; the exact phrase "inter-layer misalignment" was **not found** in
the primary text. The manuscript must quote the actual phrasing rather than invent a label.

## 2. Primary-source verification of the two anchor papers

**ICML'25 / TPP** — Bojković, Wu, Gu, *Temporal Misalignment in ANN-SNN Conversion and Its
Mitigation via Probabilistic Spiking Neurons*, ICML 2025, PMLR 267:4791–4822,
arXiv:2502.14487 (v1 2025-02-20), OpenReview `Kip4avTjth`.
Official code: https://github.com/shizukanaskytree/TPP-SNN — README says the full codebase is
"coming soon"; only a QCFS core link is exposed, no checkpoints.
Theorem 1 (a)–(d), verified against arXiv HTML:
(a) `((T−t+1)θ/T)·E[Σ_{i≤t}s[i]] = ReLU_θ(X)`;
(b) residual-voltage form of the same expectation;
(c) exactness when the activation is an integer multiple of `θ/T`, otherwise one adjacent grid point;
(d) `‖X^(l+1) − X̃^(l+1)‖∞ ≤ ‖W^(l+1)‖∞·θ^(l)/T`.
Sources: https://arxiv.org/abs/2502.14487v2 , https://arxiv.org/html/2502.14487v2 ,
https://proceedings.mlr.press/v267/bojkovic25a.html , https://icml.cc/virtual/2025/poster/45627 .

**FTBC** — Wu, Bojkovic, Gu, Suo, Zou, *FTBC: Forward Temporal Bias Correction for Optimizing
ANN-SNN Conversion*, ECCV 2024, LNCS pp.155–173, DOI 10.1007/978-3-031-72890-7_10,
arXiv:2403.18388. Code https://github.com/shizukanaskytree/FTBC (no releases/checkpoints).
Sources: https://arxiv.org/abs/2403.18388 , https://eccv2024.ecva.net//virtual/2024/poster/437 .

## 3. Strong baselines (SGNNBench is the authoritative skeleton)

SGNNBench — Zhang, Li, Zhu, Chen, Kuang, arXiv:2509.21342 (2025-09-16), 9 methods × 18 datasets,
5 seeds, hardware 2×RTX 3090Ti; code https://github.com/Zhhuizhe/SGNNBench ; explicitly no
pretrained checkpoints. Source: https://arxiv.org/html/2509.21342v1 .

| method | year / venue | official code | checkpoint | protocol note |
|---|---|---|---|---|
| SpikingGCN | IJCAI 2022, arXiv:2205.02767 | https://github.com/ZulunZhu/SpikingGCN | not found | its own Split I / Split II; legacy py3.6 stack |
| SpikeGCL | ICLR 2024, arXiv:2305.19306 | https://github.com/EdisonLeeeee/SpikeGCL | not found | self-supervised + linear probe; README gives per-dataset commands |
| SpikeGraphormer (SGNNBench: SpikeGT) | 2024, arXiv:2403.15480 | https://github.com/PHD-lanyu/SpikeGraphormer | not found | rand_split_class by default; `--protocol semi` for public split |
| SpikeNet | AAAI 2023, arXiv:2208.10364 | https://github.com/EdisonLeeeee/SpikeNet | not found | dynamic graphs, Macro/Micro-F1, link prediction |
| SiGNN | Pattern Recognition 158 (2025) 111026 | SGNNBench `signn.py` | not found | dynamic inductive link prediction |
| DRSGNN | AAAI 2024, 38:16970–16978 | SGNNBench `drsgnn.py` | not found | static / link prediction, random-walk PE |
| MSG | NeurIPS 2024, arXiv:2410.17941 | SGNNBench `msg.py` | not found | Riemannian spiking GNN |
| GC-SNN / GA-SNN | IJCAI 2021, arXiv:2107.06865 | **no official code** | not found | SGNNBench provides a reimplementation |

No paper states "reproducible on a single RTX 3060 12 GB"; the VRAM column must be measured in
this run and reported, not inferred. Name corrections: **SSEL not found anywhere**;
**DRSGCN not found** (the actual method is DRSGNN). See `notes/G0_source_conflicts.md`.

## 4. Public dataset access (G1 material)

| dataset | direct URL | terms | friction |
|---|---|---|---|
| Planetoid Cora/CiteSeer/PubMed | https://github.com/kimiyoung/planetoid/raw/master/data (`ind.*` files, PyG `Planetoid.download()`) | PyG docs state no explicit licence | none; public HTTP |
| ogbn-arxiv | https://ogb.stanford.edu/docs/nodeprop/ (OGB loader); titleabs at https://snap.stanford.edu/ogb/data/misc/ogbn_arxiv/titleabs.tsv.gz | ODC-BY | none |
| chameleon / squirrel | https://snap.stanford.edu/data/wikipedia.zip ; https://snap.stanford.edu/data/wikipedia-article-networks.html | SNAP page gives no explicit licence; Geom-GCN version GPL-3.0 | none |

Heterophily caveat, verified: Platonov et al., arXiv:2302.11640, show heavy duplicate nodes in
chameleon/squirrel; the manuscript must state the exact version and any de-duplication.
Source: https://arxiv.org/abs/2302.11640 , https://huggingface.co/datasets/anomalypoint/NEExT/blob/main/wikipedia-articles/card.md .

## 5. Venue rules (G8 / P20 material)

- **NeurIPS 2026**: 9 content pages, references/appendix/checklist excluded, double blind mandatory,
  official LaTeX style, abstract deadline 2026-05-04 AOE — **window closed**. Source:
  https://neurips.cc/Conferences/2026/CallForPapers , .../MainTrackHandbook .
- **ICML 2026**: 8 pages main paper, unlimited references/impact statement/appendices, single file,
  double blind, OpenReview; abstract 2026-01-23 AOE — **window closed**. Source:
  https://icml.cc/Conferences/2026/CallForPapers .
- **ICML 2027**: CFP page exists but says "will be posted here soon" — **not published**.
  https://icml.cc/Conferences/2027/CallForPapers .
- **NeurIPS 2027**: CFP returns 404 — **not published**.
  https://neurips.cc/Conferences/2027/CallForPapers .

Therefore the 8-page main-text target is a **working assumption** modelled on ICML 2026, to be
re-verified when a CFP exists. It is not a reported fact about ICML 2027.

## 6. Verified reference candidates (52; 44 from 2023–2026 = 84.6%)

All identifiers below came from the actual searches, not from memory. arXiv IDs:

**ANN–SNN conversion (17)**: 2502.14487, 2403.18388, 2303.04347, 2302.02091, 2412.16219,
2412.13610, 2409.03368, 2407.01645, 2411.17431, 2403.08786, 2503.00301, 2502.21193,
2506.01968, 2505.01730, 2505.09659, 2508.07710, 2601.21778.

**Spiking GNN / graph benchmarks (14)**: 2107.06865, 2205.02767, 2208.10364, 2305.19306,
2403.15480, 2410.17941, DRSGNN (AAAI 2024, 38:16970–16978), SiGNN (Pattern Recognition 158
(2025) 111026), 2509.21342, 2508.06793, 2508.02069, 2504.11840, 2601.02401, 2602.01124.

**GNN foundations / benchmarks / audit (7)**: 1609.02907, 1603.08861, 2005.00687, 1909.13021,
2106.05234, 2302.11640, 2404.03139.

**Probabilistic / stochastic spiking neurons (8)**: 1910.01059, 2305.16044, 2305.12148,
2305.13982, 2406.02923, 2404.17719, 2506.21324, 2511.11320.

**Low latency / energy proxies / reproducibility / survey (6)**: SpikingJelly
(Science Advances 2023, DOI 10.1126/sciadv.adi1480), 2308.08649, 2401.08001, 2409.02111,
2510.08591, 2610.15146.

Search-result provenance (all accessed 2026-11-05):
https://arxiv.org/search/?query=graph+neural+network+ANN+to+SNN+conversion&searchtype=all ,
...query=spiking+GNN+ANN+conversion , ...query=spiking+graph+neural+network+conversion ,
...query=spiking+graph+neural+network , ...query=ANN-SNN+conversion ,
...query=temporal+misalignment+spiking , ...query=aggregation+misalignment+spiking ,
...query=probabilistic+spiking+neuron , ...query=SSEL+spiking+graph ,
...query=spiking+neural+network+energy+efficiency+FLOPs .

Every entry must be re-verified against its primary page and checked for duplicate
preprint/published versions at P12/P14 before it enters `refs.bib`.
