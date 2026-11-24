# Claim–Evidence Matrix（筛选轮，占位符均为计划而非结果）

只覆盖 CCF 评审后保留的 3 个 idea。所有"结果"字段为 `pending`，
冒烟实验只用于 Go/No-Go，不写入任何已观测结论。

| # | Claim（planned_claim） | 机制 | 必需证据 | 实验 | 证伪消融 |  reviewer 会问的问题 | Stop-and-return 条件 |
|---|---|---|---|---|---|---|---|
| C1 (I1) | 果蝇连接组拓扑与脉冲神经元时间动力学在时序视觉任务上存在超可加交互增益 | ON/OFF 分叉、前馈-反馈 motif 与膜时间常数匹配，使有限 T 内信息可传播而不饱和 | 2×2 受控实验（生物图/打乱图 × 无状态/LIF）在等 synaptic-op 预算下的交互项 + 多种子 95% CI | cogstim `lines` 时序化 / looming 合成序列；固定图权重或训练增益；Kenyon 读出 | (a) LIF→无状态，(b) 生物图→4 随机图，(c) τ→∞，(d) 打乱递质符号，(e) 打乱时间顺序 | "相对 arXiv:2610.10023，除了加时间维还有什么？" | 冒烟 OOM / >600s / 交互项 <=0 或 \|Δ\|<0.02 / 官方基线无法复跑 → 回到场景设计，不继续训练 |
| C2 (I3) | 连接组实测光感受器几何作为解耦脉冲前端，在等输入脉冲预算下优于规则网格 | 非均匀 Voronoi 小眼实现中央凹式空间分配 + 光谱/ON-OFF 分离 | 同一下游 backbone 下 Voronoi vs 规则网格 vs 随机种子的脉冲预算-精度曲线；至少 2 个下游 + 2 个数据集 | cogstim `shapes` + CIFAR-10 / CIFAR10-DVS；T=8 速率编码 | (a) 规则网格，(b) 随机 Voronoi 种子，(c) 去 ON/OFF，(d) 去光谱分离，(e) 打乱通道对应 | "这不就是拆了 2610.10023 的 eye 模块？" | 等脉冲数下 Voronoi 与 grid 无可分辨差异 / 单个下游不复现 → 淘汰 I3 |
| C3 (I6) | 结构×动力学×预算的受控网格能给出稳定排名与交互效应（负结果同样可发表） | 统一数据/split/seed/读出后，先前论文的结论不可比问题可被消除 | 缩范围网格的多种子排名稳定性 + 单格成本外推 | mini-benchmark（先 2×2×1 四格） | 去掉交互检验、改变预算轴、改变读出群体 | "60 格多种子在 12GB 单卡怎么做完？" | 外推显示缩范围网格仍超预算 → 降级为 I1 附表或放弃独立投稿 |

## 共同的非协商项

- **不得把 `planned_claim` 写成 `observed_finding`**；所有数值阈值必须在
  `train-your-fly` 官方基线本机复跑完成后冻结，禁止先写想要的提升幅度。
- 主指标方向：`higher`（等预算 accuracy）；能效指标方向：`lower`（synaptic ops / spike rate）。
- 简单基线：线性分类器 / 规则网格 rate coding。
- 强基线：`train-your-fly`（must-rerun，含 4 种随机图 ensemble）。
- 匹配内部控制：同参数量无状态 GNN、度分布匹配的打乱图、ANN 小模型。
- 测试隔离：cogstim `--seed` 固定生成；test split 在方法选择期间不得用于调参。
