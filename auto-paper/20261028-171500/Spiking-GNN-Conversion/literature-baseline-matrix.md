# Literature & Baseline Matrix — D1 Spiking-GNN Conversion

| 论文/方法 | 年/场 | URL | 任务/数据 | 代码 | 本地重跑 | 角色 | 纳入理由 |
|----------|-------|-----|-----------|------|----------|------|----------|
| FTBC (Wu et al.) | ECCV 2024 | arXiv:2403.18388 | ANN-SNN 转换, CIFAR/ImageNet | 开源 | 适配图 | adaptation-attempt | 校准基线，D1 方法基座 |
| Temporal Misalignment + TPP (Wu) | (待核实 venue) | 见 prior-art 集群1 | 概率脉冲神经元, ImageNet | 待核 | 适配图 | adaptation-attempt | 超低 T 信息密度机制来源 |
| Parallel Conversion (ICML 2025) | ICML 2025 | icml.cc/2025/poster/44986 | 并行脉冲+转换 | github hzc1208/Parallel_Conversion | 适配图 | adaptation-attempt | 并行校准基线 |
| Kugele et al. | Front Neurosci 2020 | doi:10.3389/fnins.2020.00439 | 序列转换 delay-matching | 待核 | literature-context | 证明 non-vision 转换失效 |
| GCN (Kipf & Welling) | ICLR 2017 | arXiv:1609.02907 | 节点分类 | 内置 | must-rerun | 全精度上限基线 |
| GAT / GraphSAGE | 2018 | — | 节点分类 | 内置 | must-rerun | 全精度上限基线 |
| 直训脉冲 GNN（替代梯度） | 近年 | 待 G4 精确检索 | 节点分类 | 复现 | adaptation-attempt | 直接竞品（非转换） |
| SpikingJelly | Science Advances 2023 | 开源框架 | SNN 工具链 | github | must-rerun(作为底座) | 实现基座 | 提供 ANN2SNN/训练/量化 |

## 基线策略（G6）
- **simple baseline**：朴素转换（无校准）、全精度 ANN-GNN。
- **matched internal**：有/无校准对照、有/无概率神经元。
- **strong domain baseline**：直训脉冲 GNN（近期权威）、FTBC/并行转换适配版（直接重跑/适配尝试）。
- **oracle/upper-bound**：全精度 ANN-GNN 精度上限。

## 待办（锁定时）
- 精确核实 TPP/时序错位 venue 与代码；精确检索"直训脉冲 GNN"近 3–5 年工作以完成 G4 不重复核查。
- 扩到 ≥36 条文献且近 3–5 年占多数（citation-requirements）。
