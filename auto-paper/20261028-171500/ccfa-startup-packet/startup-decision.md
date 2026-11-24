# Startup Decision（CCFA startup）

决策时间：2026-10-28

## 决策：**proceed（D1 作为首篇 B 会）**
- D1（Spiking-GNN Conversion）通过 CCFA-startup 与 G0–G5 硬门：基线清晰、数据公开、理论机制（邻域时序错位）明确、新颖性（GNN 转换为空白）成立、本地 RTX 3060 可跑。
- 附带 **proceed D3**（跨被试 EEG 低延迟概率 SNN）：复用 xhf 既有 SpikeMLDA，叠加吴的概率/低延迟方法，B 会稳妥。
- D4 标记为 **revise/pivot-with-rescue-route**：作为旗舰，待 D1/D3 实证后抽象为统一框架，避免空泛。
- D2 标记为 **needs-evidence**：博士主线，需先筛选可本地跑的动态图子集。

## 给吴老师讨论的建议议程
1. 先认 D1：最稳的 B 会，且直接复用 xhf 的 P-SGCN 图 SNN 资产，吴只需提供转换法指导。
2. 再认 D3：xhf 已有 EEG 工作，吴的概率神经元是"增量 novelty"，风险低。
3. 把 D4 作为"跟着吴老师出 A 会"的旗舰，框架由前两篇自然生长。
4. 明确分工：吴 = 转换/低延迟方法指导 + 通讯；xhf = 图/EEG 应用、实验、写作。

## 风险与 stop 条件
- 若 D1 校准后低 T 精度落后 ANN-GNN >5% 且消融无救 → 退回"直训脉冲 GNN + 转换对比"重定位，不硬上转换。
- 若 D3 的 EEG 数据获取受阻（注册/伦理）→ 切到 xhf 已持有的数据集，或换 SEED 公开集。
- 所有远程/集群计算需 xhf 显式授权，默认本地 RTX 3060。
