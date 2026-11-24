# Idea Red-Team Review（独立红队）

## 评审对象
D1 Spiking-GNN Conversion（预训练 GNN → SNN，邻域时序校准）

## Readiness Score
- 当前就绪度：**6/10**。机制清晰、数据公开、本地可跑，但图转换无现成代码、TPP/时序错位 venue 待核实、强基线（直训脉冲 GNN 近年工作）需精确检索。

## Development Potential
- **高**。图 + SNN 交叉热度高；"转换"在图上明确空白；可自然生长为 D4 统一 non-vision 基准（A 会潜力）。

## Confidence
- **中高**。FTBC/TPP 在视觉已证机制；推广到图的"邻域错位"是合理推断，但需在 Cora 小图上先做管线 sanity check 确证。

## Fatal Risks
1. 图转换只是"视觉转换套到图"而无新机制 → G4 新颖性不足。
2. 邻域错位机制弱（消融 F1 无增益）→ 机制证伪。
3. 大图（PubMed）算力超 RTX3060 预算 → 需缩放到子集或授权集群。

## Score-change Conditions
- 若 Cora 小图 sanity check 显示校准带来 >2% 低 T 精度提升 → 就绪度升到 8/10，可 proceed 实验。
- 若 TPP/时序错位 venue 核实为顶会且代码可得 → 方法基座可信度升。
- 若精确检索发现已有"GNN 转换"高相似工作 → 降级为 pivot-with-rescue-route（换 D3/D2）。
