# Strong-Result Feasibility Contract（D1，叙事版；机器可读见 feasibility-contract.json）

## 主声明 C（聚合）
**Claim**：在公开图节点分类基准上，图感知时序校准使 ANN→SNN 转换在 T≤8 逼近全精度 GNN（≥ −1.5%），且理论 spike 计数低于直训脉冲 GNN。
**Mechanism**：图聚合的异步脉冲传播 = 邻域时序错位；推广 FTBC 通道偏置为邻域到达分布校准；TPP 概率神经元补超低 T 信息密度。
**Assumptions**：A1 邻居激活分布可轻量估计；A2 错位主因是到达时延分散；A3 低 T 下概率神经元保信息密度（视觉已证）。
**Falsifying ablation**：去掉邻域校准（F1）或换确定性 IF（F2）后低 T 精度不显著下降 → 机制弱。
**Dataset/Split**：Cora/CiteSeer/PubMed 标准公开分割；自有洪涝图按 P-SGCN 原分割。
**Primary metric**：节点分类准确率，方向 higher。
**Secondary**：时间步 T、理论 spike 数（能效）。
**Simple baseline**：全精度 ANN-GNN（上限）、朴素转换（无校准）。
**Strong baseline**：直训脉冲 GNN（近年权威）、FTBC/并行转换适配版（直接重跑/适配）。
**Matched control**：有/无校准、有/无概率神经元。
**Implementation path**：SpikingJelly（ANN2SNN/替代梯度/量化）+ 自建图转换管线；FTBC/TPP 在 PyTorch 复现。
**Prototype check**：先在 Cora 小图跑通"预训练 GCN→SNN + 校准" sanity check（≤2h，RTX3060）。
**Calibration evidence**：FTBC(ECCV24) 证明时序偏置校准误差可趋于 0；TPP 证明概率神经元超低 T 保精度。
**Test isolation**：种子≥5 固定；Cora sanity 用独立种子，不与主结果种子重叠。
**Stop-return condition**：低 T（≤8）精度落后 ANN-GNN >5% 且 F1/F2 无救 → 退回"直训脉冲 GNN + 转换对比"重定位，不在 P2 后训练至虚高目标。
**Budget**：runtime_hours ≤ 24，memory_gb ≤ 12，seeds ≥ 5，search_trials 轻量网格（T 与校准系数）。
