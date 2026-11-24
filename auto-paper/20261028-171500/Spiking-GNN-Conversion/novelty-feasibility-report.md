# Novelty & Feasibility Report — D1 Spiking-GNN Conversion

## Novelty Statement
首个针对**图神经网络**的 ANN→SNN 转换框架，并提出"邻域时序错位"机制与图感知时序校准（推广 FTBC/TPP）。区别于现有（a）直训脉冲 GNN（替代梯度）与（b）视觉/序列转换（FTBC/并行）。核心差异化：转换对象从规则网格/序列变为不规则图，且错位源于聚合的异步脉冲传播。

## Feasibility
- **数据**：Cora/CiteSeer/PubMed 公开直接下载；自有洪涝图（P-SGCN）私有可用。✅
- **代码**：基于 SpikingJelly 自建转换管线；FTBC/TPP 在 PyTorch 上可复现。✅
- **硬件**：RTX 3060 12GB 单卡可跑小图分钟级、PubMed 小时级。✅
- **人力**：xhf 已有脉冲 GNN 经验（P-SGCN）+ 吴的转换法指导。✅

## Risks & Mitigations
- R1 图转换无现成代码 → 基于 SpikingJelly 自建，先小图验证管线。
- R2 邻域错位机制弱 → 用 F1/F2 消融 + 与朴素转换对比证伪/证实。
- R3 大图算力 → 先用小图出 B 会，大图作为强结果扩展。

## Gate Verdict（方向级）
G0✅ G1✅ G2✅ G3✅ G4✅ G5✅ G6(repairable, 待补齐强基线重跑) G7(repairable, 契约细化) G8(final, 待证据)。**整体 proceed**。
