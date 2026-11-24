# Generated Research Directions Index

> 由 f-guidance-builder-v1 维护；每条完成的 guidance 追加一行。

| 时间戳 | 方向标题 | 技术 | 选定应用场景 | 闸门结论 | guidance 路径 | 备注 |
|--------|----------|------|--------------|----------|---------------|------|
| 20261028-171500 | Spiking-GNN Conversion | ANN→SNN 转换 + 邻域时序校准 | 图节点分类（Cora/PubMed + 洪涝图） | proceed（B→A 会） | auto-paper/20261028-171500/Spiking-GNN-Conversion/guidance.md | 首选首篇；复用 P-SGCN 资产；RTX3060 本地可跑 |
| 20261028-171500 | Cross-subject EEG Low-latency Probabilistic SNN | TPP/概率神经元 + 时序校准 | 跨被试 EEG 解码（SEED 系列） | proceed（B→A 会） | auto-paper/20261028-171500/Cross-Subject-EEG-Probabilistic-SNN/guidance.md | 复用 SpikeMLDA；呼应吴 FDCT 可穿戴方向 |
| 20261105-111502 | Intra-Aggregation Misalignment and Bound-Derived Latency Allocation for Graph ANN-to-SNN Conversion | 精确误差恒等式 + ρ_n 加权 L 层界 + 由界反演逐层时延 T* | 图节点分类（Planetoid / ogbn-arxiv / 异配图），低时延 T≤4 | proceed（CCF-A 主会，目标技能终评 ≥9） | auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/guidance.md | 独立第三篇；A/B 为匿名 companion；G1(d) 时延分配为绑定 expected_strong；guidance 已通过 `--strict --packet` 校验 |
| 20261110-152407 | When Does ANN-to-SNN Conversion Fail? A Matched-Protocol Study across Grid, Frozen-Graph Vision, and Graph Message-Passing Operators | ρ_n 加权系统误差 + ρ-不变相对误差 + 确定性两阶段；同一算子跨骨干与全套转换基线统一协议横评 | 视觉：CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS（可选）；图：Cora/CiteSeer/PubMed | proceed (conditional)，CCFA-startup 三轮独立红队 2.5→3.2→3.4、0 未解 fatal；G0–G8 全过；`--strict --packet` 与 `--complete` 均 PASS | auto-paper/20261110-152407/Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs/guidance.md | 基于已成稿 GNN2SNN 另起视觉新篇，**成稿不动**；G4 `pass-with-narrowing`（数学组件全被占，降档 IEEE TNNLS/Q1–Q2）；资料库报告 v3 包本地不存在、仅作参考；M0 本机 3060 实跑（恒等式残差 9.88e-15、失效边界 0.7058/1.1669）；视觉侧 0 正式实验；novix 未提交；`submission_ready=false` |

## 关联决策
- 顶层：auto-paper/20261028-171500/scenario-decision-log.md（4 方向 + 推荐组合）
- CCFA 包：auto-paper/20261028-171500/ccfa-startup-packet/
- 硬件：auto-paper/20261028-171500/hardware-profile.md
- 待启动（needs-evidence）：D2 事件驱动时空动态图 SNN（博士主线）；D4 统一 non-vision 转换基准（旗舰，建在 D1/D3 之后）

## 扩展文档
- D1 研究方案详述（可读版，含创新/新颖性/可行性证据）：auto-paper/20261028-171500/Spiking-GNN-Conversion/D1-研究方案详述.md
- D1 契约式 guidance（已通过 --strict 校验）：auto-paper/20261028-171500/Spiking-GNN-Conversion/guidance.md
