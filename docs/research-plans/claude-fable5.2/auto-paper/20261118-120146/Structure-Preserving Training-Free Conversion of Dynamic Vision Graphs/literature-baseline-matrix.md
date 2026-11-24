# Literature baseline matrix

| Paper/method | Year/venue | Task/dataset/metric | Code/checkpoint | Local rerun role | Why included/rejected |
|---|---|---|---|---|---|
| DCGS | 2025, arXiv/ICML context | CNN/ViT ImageNet accuracy and energy proxy | Public code, no detected license | must-rerun via independent reimplementation | Strongest recent training-free low-step conversion family |
| ViG | 2022 NeurIPS | Image recognition/detection | Public code, no detected license; local small reimplementation | internal-matched teacher | Defines dynamic kNN and Grapher |
| SpikeZIP-TF | 2024 ICML context | Transformer conversion | Public status to verify | literature-context | Strong conversion family outside graphs |
| One-Spike SNN | 2024/2025 | Text GCN conversion | Public link in secondary sources | literature-context | Fixed graph and linear aggregation |
| PMSM | 2025 | Tactile/image GCN conversion | Version-sensitive | literature-context | Requires specially trained source |
| Lan et al. | ICCV 2023 | Point-cloud conversion | Public status to verify | literature-context | Replaces max pooling and retrains |
| SpikingGCN | IJCAI 2022 | Node classification, MNIST image graphs | Public code | literature-context | Direct-trained, not conversion |
| Spiking PointNet | NeurIPS 2023 | Point-cloud recognition | Public code | literature-context | Direct-trained |
| DeltaCNN | CVPR 2022 | Video CNN inference, speedup | Repository URL requires verification | rescue-baseline context | Strong delta-inference baseline for scenario B |
| TopGQ | 2026 context | Quantized GNN | Public status to verify | literature-context for rescue D | Strong low-bit GNN comparator |
