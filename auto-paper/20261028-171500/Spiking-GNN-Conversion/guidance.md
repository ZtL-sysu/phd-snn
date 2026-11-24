# Guidance — Spiking-GNN Conversion: ANN→SNN 转换用于图神经网络（邻域时序校准）

## Title / Topic
- Working title: Spiking-GNN Conversion: ANN-to-SNN Conversion for Graph Neural Networks with Neighborhood Temporal Calibration
- Target field: 图表示学习 × 类脑计算（Spiking GNN）
- Target venue tier: 先 B 会（IJCNN / ICONIP / ICASSP / CIKM），强结果冲 A 会（NeurIPS / ICLR / KDD）
- 合作：吴晓锋（澳门城大，转换/低延迟 SNN 方法指导，通讯）；xhf（图 SNN 应用、实验、写作）

## Core Idea
提出首个面向**图神经网络**的 ANN→SNN 转换框架。核心假设：图的消息传递使脉冲在邻域间异步传播，产生"邻域时序错位"，导致直接套用视觉转换法在图上失效。把 FTBC 的通道级时序偏置推广为"邻域到达分布校准"，并以概率脉冲神经元（TPP）补偿超低时间步的信息密度，从而在 T≤8 逼近全精度 ANN-GNN 并保持 SNN 的节能/事件驱动优势。

## Paper Story
- **Problem**：GNN 算力/能耗高、难边缘部署；SNN 事件驱动节能，但图上的 SNN 多为直训（替代梯度），训练难、延迟高。
- **Gap**：视觉/序列的 ANN→SNN 转换已成熟（FTBC/并行转换），GNN 转换无人系统研究；现有脉冲 GNN 不是"转换"而来。
- **Insight**：图聚合的异步脉冲传播 = 邻域时序错位；图感知时序校准可在低 T 保持聚合一致性。
- **Evidence**：理论（错位上界）→ 校准方法 → 在 Cora/CiteSeer/PubMed + 自有洪涝图（P-SGCN 数据）上对比全精度 GNN、直训脉冲 GNN、FTBC/并行转换适配版；指标精度/时间步/能效（理论 spike 计数）。

## Paper Outline
1. Introduction: 图 SNN 现状；转换为空白；邻域时序错位洞见；本文贡献（首个 GNN 转换 + 校准）。
2. Related Work: ANN→SNN 转换（FTBC/TPP/并行转换）；脉冲 GNN 直训；图学习（GCN/GAT/SAGE）。
3. Method: 3.1 GNN→SNN 转换管线；3.2 邻域时序错位建模；3.3 图感知时序校准（推广 FTBC）；3.4 概率脉冲聚合（超低 T）。
4. Experiments and Results: 数据集/基线/变体/消融/指标/统计/能效；主结果表 + 低 T 精度-能耗权衡图。
5. Discussion: 邻域错位的普遍意义；与动态图（博士主线 D2）和神经形态部署的衔接；局限。
6. Conclusion: 总结；与吴老师旗舰方向（D4 统一 non-vision 转换基准）的衔接。

## Experiment Plan
### Datasets（直接公开访问）
- Cora：https://pytorch-geometric.readthedocs.io/en/latest/modules/datasets.html#torch_geometric.datasets.Planetoid （PyG 内置，source/access: 程序化直接下载）
- CiteSeer：同上（Planetoid）
- PubMed：同上（Planetoid）
- 自有洪涝图（P-SGCN 数据）：xhf 私有可用，作为真实应用域增强故事。
### Baselines
- 全精度 ANN-GNN（GCN/GAT/SAGE）—— 上限（must-rerun）
- 直训脉冲 GNN（替代梯度）—— 直接竞品（adaptation-attempt）
- FTBC 适配图 / 并行转换适配图 —— 转换基线（adaptation-attempt）
- 朴素转换（无校准）—— 内部对照（internal-matched）
### Method variants
有/无邻域校准；有/无概率脉冲聚合；时间步 T∈{1,2,4,8,16}。
### Ablations
校准项（F1）；概率神经元（F2）；邻域到达分布估计 vs 均匀假设（F3）。
### Metrics
- Primary metric：节点分类准确率（Node Classification Accuracy）
- Secondary metrics：时间步 T、理论能耗（spike 数 × 权重）、推理延迟（若 neurolorphic 模拟）
### Expected outcomes / statistical
T≤8 时转换 GNN 精度 ≥ ANN-GNN −1.5%；5 随机种子均值±std，配对 t 检验 vs 基线。
### Hardware Budget / Runtime
RTX 3060 12GB 单卡；小图（Cora/CiteSeer）分钟级，PubMed 小时级；runtime_hours 估计 ≤ 24；memory_gb ≤ 12。
### Stopping criteria / Failure signal
低 T（≤8）精度落后 ANN-GNN >5% 且消融无救 → 退回"直训脉冲 GNN + 转换对比"定位（stop_return_condition）。

## Expected Results
- minimum（可接受）：T≤16 时转换 GNN 精度 ≥ ANN-GNN −3%，优于朴素转换 ≥2%。
- strong（强）：T≤8 时精度 ≥ ANN-GNN −1.5%，spike 数显著低于直训脉冲 GNN。
- failure signal：T≤8 精度落后 >5% 且校准消融无增益 → 机制证伪，重定位。

## Figure/Table Decision Rules
- 图1：方法框架（GNN→SNN + 邻域校准）。
- 图2：低 T 下精度-能耗（spike 数）权衡曲线（核心卖点）。
- 表1：各数据集 × 各基线 × T 的精度表（主结果）。
- 图/表选择在证据稳定后由 f-research-v1 决定，不在此固定数量。

## Citation Scope
- 关键词：Spiking Neural Network, ANN-to-SNN Conversion, Graph Neural Network, Low-latency SNN, Neuromorphic。
- 必引：FTBC(ECCV24, arXiv:2403.18388)、TPP/时序错位(Wu)、并行转换(ICML25)、Kugele20(Front Neurosci)、SpikingJelly(Science Advances 2023)、GCN/GAT/SAGE、脉冲 GNN 直训近年工作。
- 边界：聚焦图 + 转换；近 3–5 年文献占多数；锁定时扩到 ≥36 条独立相关文献（citation-requirements）。

## Traceability Checklist
| Guidance requirement | Required artifact | Success check | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|
| 转换框架 + 邻域校准 | Method §3 | 低 T 精度 ≥ ANN-GNN −1.5% | 图1/表1 | Yes |
| 邻域错位机制 | §3.2 + 理论 | 校准消融 F1 显著提升 | 表1 | Yes |
| 概率脉冲聚合 | §3.4 | F2 超低 T 不掉点 | 图2 | Yes |
| 全精度上限基线 | §4 | ANN-GNN 复现 | 表1 | Yes |
| 直训/转换基线对比 | §4 | 优于朴素转换 ≥2% | 表1/图2 | Yes |
| 能效证据 | §4 | spike 数低于直训 | 图2 | Yes |
| 真实应用域 | §4 | 洪涝图结果一致 | 表1 | Yes |
