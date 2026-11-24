# Literature baseline matrix

Built before `guidance.md`, as required by `f-guidance-builder-v1`. All entries verified 2026-11-05
against arXiv, PMLR, ECVA/ECCV, ICLR/ICML/IJCAI pages, OpenReview or the official repository.
Role vocabulary: `must-rerun`, `adaptation-attempt`, `internal-matched`, `oracle/upper-bound`,
`literature-context`.

| # | method | year / venue / official URL | task, dataset, metric | code | checkpoints | direct-rerun on this machine | role | why strong / why rejected |
|---|---|---|---|---|---|---|---|---|
| 1 | TPP (ICML 2025) | 2025, PMLR 267:4791–4822, https://proceedings.mlr.press/v267/bojkovic25a.html , arXiv:2502.14487 | image conversion, CIFAR/ImageNet, accuracy | https://github.com/shizukanaskytree/TPP-SNN (full code "coming soon") | none | partial — equations (8)–(13) re-implemented locally | `adaptation-attempt` | the anchor paper; its neuron is the direct mechanism control, not a graph baseline |
| 2 | FTBC (ECCV 2024) | 2024, ECCV LNCS 155–173, https://arxiv.org/abs/2403.18388 | image conversion, CIFAR/ImageNet, accuracy | https://github.com/shizukanaskytree/FTBC | none | not needed (mechanism ancestor) | `literature-context` | must-cite inheritance; CNN and expectation-level, so not a graph comparator |
| 3 | QCFS (ICLR 2022) | 2022, https://arxiv.org/abs/2303.04347 | image conversion, accuracy vs T | referenced by FTBC/TPP repos | none | not needed | `literature-context` | standard conversion host; defines the low-latency framing |
| 4 | SpikingGCN (IJCAI 2022) | 2022, https://arxiv.org/abs/2205.02767 ; https://github.com/ZulunZhu/SpikingGCN | Cora/CiteSeer/PubMed, accuracy | official | none found | yes, via pinned `spikinggcn36` (py3.6 + graphgallery 0.7.2) or WSL `spikg` | `must-rerun` | most-cited spiking-GNN number; its Split I / Split II ambiguity is documented |
| 5 | SpikeGCL (ICLR 2024) | 2024, https://arxiv.org/abs/2305.19306 ; https://github.com/EdisonLeeeee/SpikeGCL | Planetoid + ogbn-arxiv, accuracy | official, per-dataset commands in README | none found | yes, WSL `spikg` (torch 2.1 + PyG/dgl) | `must-rerun` | strong recent self-supervised spiking encoder; codebase anchor |
| 6 | SpikeGraphormer | 2024, https://arxiv.org/abs/2403.15480 ; https://github.com/PHD-lanyu/SpikeGraphormer | large-graph node tasks, accuracy | official | none found | yes, WSL `spikg` + dgl 1.1.3 | `adaptation-attempt` | its split flag changes Cora by ~10.7 pp; a controlled external anchor |
| 7 | DRSGNN (AAAI 2024) | 2024, 38:16970–16978 (SGNNBench README) | static / link prediction, accuracy | SGNNBench `drsgnn.py` | none | likely; random-walk PE may be costly | `adaptation-attempt` | recent authoritative SGNN; protocol must be labelled |
| 8 | SiGNN | 2025, Pattern Recognition 158:111026 | dynamic inductive link prediction | SGNNBench `signn.py` | none | likely with neighbourhood sampling | `adaptation-attempt` | recent SGNN, different protocol; labelled row only for the main Pareto |
| 9 | MSG (NeurIPS 2024) | 2024, https://arxiv.org/abs/2410.17941 | graph benchmarks, accuracy | SGNNBench `msg.py` | none | likely | `literature-context` | recent authoritative method; reserve if an arm fails |
| 10 | GC-SNN / GA-SNN (IJCAI 2021) | 2021, https://arxiv.org/abs/2107.06865 | Cora/CiteSeer/PubMed, accuracy | **no official code**; SGNNBench reimplementation | none | only as a reimplementation | `literature-context` | foundational but cannot be a codebase-level external baseline |
| 11 | SGNNBench | 2025, https://arxiv.org/abs/2509.21342 ; https://github.com/Zhhuizhe/SGNNBench | 9 methods × 18 datasets, 5 seeds, 2×RTX 3090Ti | official | **explicitly none** | small graphs yes; ogbn-proteins/Tmall/Patent no | `must-rerun` (implementation source) | the only unified protocol; it has **no conversion entry**, which is the gap |
| 12 | SpikeNet (AAAI 2023) | 2023, https://arxiv.org/abs/2208.10364 ; https://github.com/EdisonLeeeee/SpikeNet | dynamic graphs, Macro/Micro-F1 | official | none found | DBLP plausible; Tmall/Patent out of envelope | `literature-context` | different task/protocol, cannot carry a node-classification Pareto claim |
| 13 | Internal IF no-bias | this run | three fitted graphs, accuracy | this run | n/a | yes | `internal-matched` | simple floor |
| 14 | Internal TPP, TPP+`β*`, count decoder, uniform-T | this run | three fitted graphs, accuracy | this run | n/a | yes | `internal-matched` | isolates the neuron, the bias, the decoder and the allocation |
| 15 | Full T-grid oracle / source ANN | this run | three fitted + held-out graphs | this run | n/a | yes | `oracle/upper-bound` | ceiling column (not ranked) and the cost the method avoids |

## Strong-baseline rationale

For a CCF-A target, a matched ANN control alone is insufficient. At least three recent authoritative
spiking-GNN methods (rows 4, 5, 6, with 7/8 as adapters) are planned as **direct reruns or
adaptations** under the frozen protocol before any proposed-method iteration, satisfying G6.
Literature-only rows (2, 3, 9, 10, 12) are explicitly separated and cannot carry the main
comparison. No published method in this table ships checkpoints, and TPP's full codebase is
unreleased; this is the single labelled G6 limitation recorded in `startup-decision.md`.

## Name-verification notes

`SSEL` and `DRSGCN` appear in the task book but could not be verified against arXiv or the web;
the actual SGNNBench method is `DRSGNN`. Neither unverified name enters any table or manuscript
sentence. `SpikeGraphormer` is recorded as `SpikeGT` inside SGNNBench; both names refer to
arXiv:2403.15480.

## Source access

All URLs above accessed 2026-11-05. Full search queries and the 52-entry verified reference
candidate list are in `notes/G0_literature_map.md`.
