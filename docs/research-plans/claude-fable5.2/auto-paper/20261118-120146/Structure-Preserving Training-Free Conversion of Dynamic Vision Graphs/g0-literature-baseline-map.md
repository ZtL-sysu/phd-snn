# G0 — Recent literature and baseline map

Access date: 2026-11-18.

## Direct verification performed

- arXiv API record `2503.00301`: *Differential Coding for Training-Free ANN-to-SNN Conversion*, published 2025-03-01, updated 2025-07-08. Abstract states differential coding, threshold iteration, CNN/Transformer evaluation, state-of-the-art performance, and code at `https://github.com/h-z-h-cell/ANN-to-SNN-DCGS`. This is the current strong training-free conversion baseline family.
- arXiv API record `2206.00272`: *Vision GNN: An Image is Worth Graph of Nodes*, published 2022-06-01, NeurIPS 2022 comment. Abstract confirms patch nodes, nearest-neighbor graph construction, Grapher/FFN modules, and official PyTorch code at `https://github.com/huawei-noah/Efficient-AI-Backbones`.
- arXiv API record `2203.03996`: *DeltaCNN*, published 2022-03-08, CVPR 2022 comment. Abstract confirms training-free sparse frame differences, per-layer sparse updates, and up to 7x practical speedup over cuDNN.
- arXiv API records `2205.02767`, `2310.06232`, `2410.17941`, `2406.03470` confirm the closest graph/Transformer clusters are direct-training or non-graph conversion routes, not the proposed dynamic-kNN/signed-max training-free conversion.
- Targeted arXiv query `all:"Vision Graph" AND all:"spiking"` returned no records. Query `all:"graph" AND all:"training-free" AND all:"conversion"` returned unrelated retrieval/RAG records, not a competing graph-conversion paper. These are search observations, not a proof of absolute novelty.
- GitHub API: `h-z-h-cell/ANN-to-SNN-DCGS` exists, pushed 2025-05-29, 17 stars, no detected license. Direct `LICENSE` request returned 404.
- GitHub API: `huawei-noah/Efficient-AI-Backbones` exists, 4,430 stars, no detected license. Direct `LICENSE` and `LICENSE.txt` requests returned 404.
- Raw remote `Casey-sketch-cyber/gnn2gsnn/literature/questions.md` was retrieved successfully; it is an imported secondary source and is not used as a primary scientific claim without its linked paper evidence.

## Baseline classification

| Paper/method | Year/venue | Task/dataset/metric in source | Code/checkpoint | Local rerun role | Reason |
|---|---|---|---|---|---|
| DCGS | 2025 arXiv/ICML-context | CNN/ViT ImageNet accuracy, energy proxy | Code public, no detected license | `adaptation-attempt` via independent reimplementation | Strongest recent training-free low-step conversion family; must not be copied unlicensed |
| ViG | 2022 NeurIPS | Image classification/detection, top-1 | Official PyTorch code public, no detected license; ImageNet weights not verified for direct CIFAR path | `internal-matched` via paper-faithful small Grapher reproduction | Defines dynamic kNN and signed max; teacher for mechanism test |
| SpikingGCN | 2022 arXiv/IJCAI-context | Graph/node and image-graph classification | Public implementations exist | `literature-context` | Direct-trained spiking GCN, not conversion |
| Spiking PointNet | 2023 arXiv/NeurIPS-context | Point-cloud recognition | Public code to verify | `literature-context` | Direct-trained visual graph SNN, not training-free conversion |
| MSG | 2024 arXiv/NeurIPS-context | Graph learning | Public status to verify | `literature-context` | Early spiking graph work; does not match visual dynamic topology conversion |
| SpikeZIP-TF | 2024 ICML-context | Transformer conversion | Code to verify | `technique-family` context | Strong conversion method for attention/normalization, not graphs |
| DeltaCNN | 2022 CVPR | Video CNN inference, accuracy/speedup | Repository link requires verification | `adaptation-attempt` only if direction B is selected | Strong sparse-delta baseline for streaming variant |
| One-Spike SNN / PMSM / point-cloud conversion | 2025 context | Fixed-text GCN, tactile GCN, point cloud | Secondary-source links | `literature-context` | Closest graph-conversion attempts; each has fixed graph, source retraining, or max-pooling replacement limitations in the imported audit |

## Gate verdict

`pass` for G0 with a caveat. A current authoritative baseline family (DCGS) and the defining teacher architecture (ViG) are identified with direct primary records and code links. The local route must independently reimplement graph operators and conversion because detected licenses are absent. Official CIFAR-10 ViG checkpoints are not verified; a locally trained teacher is therefore an internal evidence route, and this limitation must remain explicit through G6.
