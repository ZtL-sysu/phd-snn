# Literature and baseline matrix

Verified 2026-11-17. `must-adapt` means a direct frozen-conversion baseline must be rerun/adapted before publication; `context` means the work constrains novelty/terminology but is not necessarily a direct rerun.

| Work | Year / venue | Verified URL | Paradigm | Role |
|---|---|---|---|---|
| One-Spike SNN | 2024/2025 IEEE TETC | https://arxiv.org/abs/2403.08786 ; https://doi.org/10.1109/TETC.2024.3386893 | CNN+GCN conversion | must-adapt; graph conversion and output-code anchor |
| ASGCN | AAAI 2025 | https://ojs.aaai.org/index.php/AAAI/article/view/32154 ; https://doi.org/10.1609/aaai.v39i2.32154 | ANN graph → asynchronous event graph conversion | must-adapt for event/temporal graph claims |
| SpikingGCN | IJCAI 2022 | https://www.ijcai.org/proceedings/2022/338 | direct spiking GCN | context/heterophily baseline |
| SpikeNet | AAAI 2023 | https://ojs.aaai.org/index.php/AAAI/article/view/26034 | direct dynamic spiking GNN | context for DYN/DLY |
| Dy-SIGN | AAAI 2024 | https://doi.org/10.1609/aaai.v38i15.29587 | direct dynamic spiking GNN | context for DYN/DLY |
| Delay-DSGN | ICML 2025 | https://proceedings.mlr.press/v267/wang25dm.html | direct delayed dynamic spiking GNN | context for DLY |
| SiGNN | Pattern Recognition 2025 | https://doi.org/10.1016/j.patcog.2024.111026 | direct temporal spiking GNN | context for DYN/DLY |
| MSG | NeurIPS 2024 | https://proceedings.neurips.cc/paper_files/paper/2024/hash/3ba7560b4c3e66d760fbdd472cf4a5a9-Abstract-Conference.html | spiking geometric model | context for EQ |
| GC-LIF | 2026 preprint | https://arxiv.org/abs/2610.39601 | direct/hybrid equivariant spiking GNN | context for EQ |
| SGSPose | IEEE Access 2026 | https://doi.org/10.1109/ACCESS.2026.3651795 | spiking pose model | context for EQ |
| Negative-spike conversion | IJCAI 2025 | https://www.ijcai.org/proceedings/2025/719 | generic signed ANN→SNN conversion | must-adapt for SIGN |
| A²Q | 2023 | https://arxiv.org/html/2302.00193 | graph-aware learned quantization | must-adapt for LR/EDGE |
| AdaQP | MLSys 2023 | https://proceedings.mlsys.org/paper_files/paper/2023/hash/420bcf98bb3615a21468f1efb426e96d-Abstract-mlsys2023.html | graph message quantization/communication | context for LR/EDGE |
| Fast-SNN | 2023 | https://arxiv.org/abs/2305.19868 | converted SNN acceleration | context for EDGE/CERT |
| SEENN | NeurIPS 2023 | https://papers.neurips.cc/paper_files/paper/2023/hash/c801e68207da477bbc44182b9fac1129-Abstract-Conference.html | conversion-compatible early exit | must-adapt for CERT/selection claims |
| SpikeGraphormer | 2024 | https://arxiv.org/abs/2403.15480 | direct spiking graph transformer | context/must-adapt for POS |
| SpikeZIP-TF | ICML 2024 | https://proceedings.mlr.press/v235/you24b.html | transformer conversion | must-adapt for POS |
| ECMT | 2025 | https://arxiv.org/abs/2502.21193 | transformer conversion | must-adapt for POS |
| TTFSFormer | ICML 2025 | https://proceedings.mlr.press/v267/zhao25n.html | direct TTFS transformer | context for POS |
| SGNNBench | 2025 | https://arxiv.org/abs/2509.21342 | direct spiking-GNN benchmark | protocol context; no conversion arm |
| SIGHT | WWW 2026 | https://doi.org/10.1145/3774904.3793044 | spiking graph uncertainty | context for confidence claims |

## Required publication baselines

- Frozen-conversion: One-Spike adaptation and ASGCN-style event conversion where applicable.
- Domain: GCN/GatedGCN or graph-transformer ANN teacher, direct spiking GCN/SpikeGraphormer context, A²Q/AdaQP for message compression.
- Internal matched controls: universal rate/count conversion, signed/unsigned, permutation-shuffled, uniform/low-rank, full/pair readout, delayed/non-delayed schedules.
- Every efficiency claim reports graph traversal, indexing, pooling, readout and memory separately; event counts alone are not energy.
