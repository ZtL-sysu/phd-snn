# Idea Cards — GNN × SNN × 果蝇连接组 × 视觉（CVPR 2027 选题筛选轮）

生成时间 2026-11-05。全部 idea 共享的**证据底座**见 `literature-baseline-matrix.md`、
`dataset-access-log.md`、`prior-art-dedup-log.md`、`hardware-profile.md`。
时间硬约束：CVPR 2027 全文截止 2026-11-16 AOE（还有 11 天），注册 11-10。

## 共享底座（评审时视为已验证事实）

- 图 A：FlyWire v783（139,255 神经元 / 5,450 万突触），`train-your-fly` 1.3 GB 图包直下，含复眼 Voronoi 坐标与 4 种随机图。
- 图 B：MaleCNS v1.0（166,691 神经元 / 1.25 亿突触），1.05 GB feather 全图直下，另有 13 MB 标注 / 42 MB 递质预测。
- 刺激：`cogstim`（MIT，pip）生成 8 类 512×512 PNG，按 class 分 train/test，`--seed` 可复现。
- 基线：`train-your-fly` / arXiv:2610.10023（无状态 GNN + 等布线预算随机图对照）为 must-rerun；
  内部对照含随机图、规则网格、ANN、spikingjelly LIF。
- 环境：`dyg-cold`，torch 2.11+cu128 / PyG 2.8.0.post1 / spikingjelly / RTX 3060 12 GB / 31.9 GB RAM。
- 红线：arXiv:2610.10023（无状态 GNN 视觉）、arXiv:2609.01330（连接组+SNN 朝向图仿真）、
  Nature 2024 flyvis、BrainTrace / BioReservoir / MaleCNS X-ray 博客已占据大部分朴素叙事。

---

## I1 — FlySpike-T：连接组拓扑 × 脉冲动力学的交互增益

**标题**：*Wiring × Dynamics: Connectome-Constrained Spiking Graph Networks for Temporal Vision*

- **瓶颈**：现有连接组视觉模型把连接组当**静态结构先验**——`train-your-fly` 明写"neurons keep no state between steps"，
  3 步无状态消息传递 + tanh 就读出；而果蝇视觉最有代表性的计算（ON/OFF 分离、方向选择性、looming、适应）
  本质上是**时间**计算。反过来，连接组 + 脉冲神经元的工作（NeurIPS 2025 朝向图、BrainTrace）只做神经科学仿真，
  没有可训练 CV 任务，也没有把"结构"和"动力学"拆开归因。
- **机制**：固定生物图为稀疏有向循环骨架，边权 = `syn_count` × 递质符号(±) × 可学习增益；
  把节点从无状态 tanh 换成 LIF/ALIF（膜电位、泄漏、阈值、可选适应）；
  视觉输入按 T 个时间步送入（静态图重复采样 / 时序变化 / 事件流），读出 Kenyon 群体脉冲计数。
  假设生物图的 ON/OFF 分叉、前馈-反馈 motif 与膜时间常数 τ 之间存在**匹配**，
  使信息在有限 T 内既能传播到读出层又不会饱和；随机图丢失这种匹配。
- **关键假设**：结构（拓扑）与动力学（脉冲状态）在时序任务上存在**超可加交互**；在静态任务上则退化为可加。
- **可证伪消融**：2×2 受控设计 —— {生物图, 4 种随机图} × {无状态 GNN, LIF, ALIF}，
  再加 (a) 去掉泄漏（τ→∞）、(b) 打乱递质符号、(c) 固定增益不训练、(d) 打乱输入时间顺序。
  若时序任务上"生物图优势"在无状态条件下一样大（即无交互项，双因素 ANOVA 交互不显著），机制被证伪。
- **贡献类型**：新架构 + 一个可归因的机制结论（结构×动力学），而非又一个 backbone。
- **任务/指标**：cogstim `lines` 时序化、运动方向/looming 合成序列、可选 CIFAR10-DVS；
  主指标 = 固定 synaptic-op 预算下的 test accuracy；次指标 = spike rate、首次正确判别时刻、
  accuracy-vs-T 曲线、参数量/突触操作数。
- **强基线**：`train-your-fly`（must-rerun）、4 种随机图 ensemble、spikingjelly LIF 基线、
  同参数量 ANN、CVPR 2026 SpikeTrack 思路对照（文献）。
- **G4 定位**：相对 P1 增加**时间维度与脉冲状态**并把比较轴从 wiring cost 换成 spike/energy；
  相对 P2 增加**可训练 CV 任务 + 受控 2×2 归因**。不是"再跑一次仿真"。
- **最小冒烟实验**：下载真实图 → 抽取视叶子图（<=20k 节点）→ 构建 PyG 稀疏边 →
  LIF 前向 T=8、batch=4 → 记录显存/耗时/spike 率 → 生物图 vs 1 种随机图跑 30 步训练，
  看 loss 是否下降、两者是否出现可分辨差距。
- **风险**：166k 节点 BPTT 显存爆炸（必须子图化）；τ、阈值、surrogate gradient 超参敏感；
  11 天内做不出完整多种子论文；与 arXiv:2610.10023 只差"加了时间维"可能被判 incremental。
- **11 天可投性**：低（机制漂亮但实验量大）。

---

## I2 — Wiring-as-Regularizer：连接组结构先验带来的鲁棒视觉

**标题**：*Biological Wiring as a Free Regularizer for Spiking Vision under Corruption*

- **瓶颈**：SNN 视觉的抗腐蚀/对抗鲁棒性通常靠额外训练技巧或集成；连接组的稀疏、重尾度分布、
  反馈环、ON/OFF 双通路是**免费**的结构冗余，但没有人把它与 LIF 的时间去噪联合量化。
- **机制**：生物图的稀疏连通限制扰动传播路径，反馈环提供复现/纠错，ON/OFF 分离提供差分冗余；
  LIF 阈值 + 泄漏对输入噪声做时间低通。二者叠加应降低对高斯噪声、亮度漂移、遮挡、FGSM/PGD 的敏感度。
- **可证伪消融**：等 spike 率 / 等参数量下比较 {生物图, 随机图} × {无状态, LIF}；
  若生物图的鲁棒性优势落在 95% CI 内，或只在合成腐蚀上出现、在真实腐蚀/对抗上消失，机制被证伪。
  另需排除"只是稀疏所以鲁棒"：加入度分布匹配但 motif 打乱的随机图。
- **贡献类型**：实证型机制发现 + 鲁棒性benchmark 结论。
- **任务/指标**：cogstim `shapes/colours/ans` + 腐蚀集；主指标 = 干净/腐蚀准确率落差（relative drop、
  mCE 风格）；次指标 = 对抗鲁棒精度、spike rate 变化。
- **强基线**：`train-your-fly`、随机图 ensemble、ResNet-18 / 小 ViT（ANN 上界）、
  SNN + 对抗训练（若时间允许）。
- **G4 定位**：P1/P2 都没做扰动鲁棒性；但 ESA/BioReservoir 已提出"连接组拓扑比随机 reservoir 更抗过拟合"
  ——那是**过拟合/泛化**，不是**输入腐蚀鲁棒性**，且没有 CVPR 级视觉基准。需明确写清这一区别。
- **最小冒烟实验**：生物图 vs 随机图，在 `shapes` 上加 3 档高斯噪声，各跑 30 步训练，
  比较干净/噪声准确率差与 spike 率。
- **风险**：容易被质疑"生物结构 ≈ 任意稀疏图"，需要度分布匹配的对照才有说服力；
  CVPR 对鲁棒性数字要求强基线与多种子；11 天内工作量大。
- **11 天可投性**：低-中。

---

## I3 — Fly-Eye Front-end：连接组导出的可插拔脉冲视觉前端

**标题**：*Connectome-Measured Photoreceptor Geometry as a Plug-in Neuromorphic Vision Front-end*

- **瓶颈**：SNN / 事件视觉模型把输入当**规则网格 patch**，忽略了传感器几何；
  而事件相机的异步脉冲与果蝇复眼 R1-R6 / R7 / R8 的采样、光谱、ON/OFF 分离高度同构。
  `train-your-fly` 有复眼模型，但它与全脑 GNN 死绑在一起，从未被当作**通用、可插拔、与连接组图解耦**的
  视觉前端在标准 CV 基准上验证。
- **机制**：从 FlyWire 光感受器 3D 终扣位置投影 → 以 R7 为种子的 Voronoi 小眼划分（非均匀、中心密集）
  → 每个小眼按光谱通道（R1-6 亮度 / R7 蓝 / R8p 绿 / R8y 红）+ ON/OFF 双路做脉冲编码；
  非均匀采样天然实现"中央凹式"空间资源分配与亮度自适应（R7/R8 互抑制）。
  等价于用**真实生物测量**替代手工设计的事件编码 / patch embedding，参数量近乎为零。
- **可证伪消融**：(a) Voronoi 换成规则网格，(b) 随机 Voronoi 种子，(c) 去掉 ON/OFF 双路，
  (d) 去掉光谱分离，(e) 打乱小眼与通道对应关系。若 (a)(b) 无差异，则"几何有用"被证伪。
- **贡献类型**：新的输入编码层 / 计算成像视角，可直接接到任意 SNN 或轻量 CNN。
- **任务/指标**：CIFAR-10 / CIFAR10-DVS / cogstim `shapes`，可选高速低光；
  主指标 = 等输入脉冲数下的 accuracy；次指标 = 脉冲数、参数量、时延、低输入率下的精度保持。
- **强基线**：规则网格 rate coding、TTFS / Poisson 编码、标准 patch embedding、`train-your-fly` 的 eye 模块原样接入。
- **G4 定位**：P1 的 eye model 是**整篇论文的组成部分**，这里我们把它抽象成**与脑图解耦的、
  在标准 CV 基准上可比较的前端**，并给出脉冲预算-精度曲线；这是不同的贡献单元。
  风险是仍被看成"拆了别人一个模块"。
- **最小冒烟实验**：用 `train-your-fly` 图包里的 `right_visual_positions_all_neurons.csv`
  重建 Voronoi 采样器，对 cogstim 图像生成脉冲张量，接一个 2 层 LIF + 线性头跑 50 步，
  对比规则网格编码的 loss 曲线与脉冲数。
- **风险**：eye 数据依赖官方图包；"通用前端"需要至少 2 个下游 backbone + 2 个数据集才算站住；
  单独发 CVPR 主会偏轻，容易被判 component-level。
- **11 天可投性**：**中-高**（实现最快、数据现成、无需训练大图 SNN）——但故事偏小。

---

## I4 — Cross-Connectome Motif Prior：从两个完整连接组蒸馏可迁移视觉拓扑

**标题**：*Evolutionarily Conserved Visual Motifs as Transferable Sparse Priors for Vision Backbones*

- **瓶颈**：一个连接组只是"一个个体的接线"。雄（MaleCNS 166k）与雌（FlyWire 139k）两个独立完整
  连接组 + `ol_annotations` 跨数据集视叶 cell-type 匹配，第一次让"哪些视觉 motif 是保守的"可被测量。
  但现有工作都在单图上做建模，没人把**跨图共识 motif** 提取成可注入 CV backbone 的稀疏先验。
- **机制**：用 GNN 在两图上做对齐/共聚类，提取跨个体稳定出现的前馈链、反馈环、ON/OFF 分叉 motif；
  把 motif 分布作为稀疏 MLP / 稀疏注意力的拓扑生成器，替代随机稀疏或手工局部性。
  假设保守 motif 携带对视觉统计有用的归纳偏置，在参数受限时优于同稀疏度的随机图。
- **可证伪消融**：保守 motif vs 单图 motif vs 度匹配随机稀疏 vs 稠密；
  若只在极小模型上有差异、或跨数据集排序不稳定，机制被证伪。
- **贡献类型**：结构先验发现 + 架构迁移。
- **任务/指标**：CIFAR-10/100、ImageNet-100 子集，参数量-精度权衡；辅助任务 = 细胞类型/递质预测。
- **强基线**：随机稀疏 / ER / 小世界图、ViT 稀疏注意力、`train-your-fly` 的随机图 ensemble。
- **G4 定位**：避开 P1-P4 的任务与主张；但 CVPR fit 明显更弱（更像 graph representation learning /
  计算神经科学），且 `cocoa`、`coconatfly` 等比较连接组工具已存在。
- **最小冒烟实验**：加载 MaleCNS 与 FlyWire 两张图的度/motif 统计，验证两图视叶子图的
  motif 分布相关性是否显著高于随机对照。
- **风险**：链条长（对齐→motif→注入→验证）；生物学结论与 CV 收益之间因果链薄弱；
  11 天完全不可行；容易被 desk reject 为"不是 CV"。
- **11 天可投性**：极低。

---

## I5 — Structure-Aware Spike Distillation：基础模型蒸馏到连接组脉冲图

**标题**：*Distilling Vision Foundation Models into Connectome-Constrained Spiking Graphs*

- **瓶颈**：大规模 SNN 难训练（梯度消失、脉冲稀疏）；连接组提供的是**有语义的稀疏骨架**而非随机稀疏。
  若把 teacher 的 patch 关系对齐到生物图邻接，就能给 SNN 一个结构监督信号。
- **机制**：用 DINOv2/CLIP 的 patch 相似度矩阵作为 teacher，对生物图上的消息传递做关系蒸馏；
  学生为连接组约束 LIF-GNN。teacher 提供语义，生物图提供稀疏结构，二者共同缓解脉冲训练不稳定。
- **可证伪消融**：随机图 + 同蒸馏 / 生物图 + 无蒸馏 / teacher 换成随机矩阵；
  若随机图同样好，则生物结构无贡献；若无蒸馏同样好，则蒸馏无贡献。
- **贡献类型**：训练方法 + 结构蒸馏。
- **任务/指标**：CIFAR-10/100、cogstim 三任务；accuracy、收敛步数、spike rate。
- **强基线**：`train-your-fly`、无蒸馏 SNN、随机图蒸馏、ANN teacher 本身（上界）。
- **G4 定位**：P1 无蒸馏、P2 无可训练 CV 任务；但 JEPA-on-connectome（2026 工作论文）
  已探索"连接组脉冲 + 自监督表征"，P4 ทำให้本 idea 的新颖性变薄。
- **最小冒烟实验**：小图上做一次 teacher-student 关系损失前向 + 反传，确认显存与收敛。
- **风险**：强烈"A+B 拼盘"感；引入 teacher 后"结构是否有用"更难干净归因；
  需要额外大模型推理成本；11 天不可行。
- **11 天可投性**：极低。

---

## I6 — ConnectomeBench：结构 × 动力学 × 能效的首个受控基准

**标题**：*ConnectomeBench: A Controlled Benchmark of Topology, Neural Dynamics and Efficiency in Connectome-Constrained Vision*

- **瓶颈**：MaleCNS（2026-09）与 FlyWire 刚齐备，社区却缺少统一对照：
  不同论文用不同图、不同动力学、不同任务、不同指标，导致"生物接线到底值多少"无法比较。
  `train-your-fly` 只覆盖了 {生物图, 4 随机图} × 无状态 GNN × wiring cost 这一格。
- **机制**（基准不是方法）：定义 5 种图 × 3 种动力学（无状态 / LIF / ALIF）× 2 类任务
  （静态 / 时序）× 2 个预算轴（wiring cost / synaptic ops）的可复现网格，
  统一数据、split、seed、读出与统计检验，输出交互效应与排名稳定性；负结果同样有效。
- **可证伪**：若所有组合排序稳定、结构×动力学无交互，则"生物接线有特权"这一说法被削弱——
  这本身是可发表结论。
- **贡献类型**：dataset/benchmark + 系统性归因（对应 CVPR 2027 "Datasets and Benchmarks"、
  "Efficient and scalable vision"、"AI for Science" 主题）。
- **任务/指标**：cogstim 8 类任务 + 时序扩展；主指标 = 等预算 accuracy、交互效应量、排名稳定性、
  复现方差；次指标 = spike rate、显存、吞吐。
- **强基线**：`train-your-fly` 原配置作为基准的一个单元格；4 种随机图；ANN / LIF 基线。
- **G4 定位**：不与 P1-P4 抢"方法新颖性"，而是提供它们都缺的**受控比较框架**；
  但必须证明网格规模与多种子统计在本地 12 GB GPU 上可完成，否则是空头支票。
- **最小冒烟实验**：跑通网格中 2×2×1 的 4 个单元格各 30 步，估计单格耗时与显存，
  外推全网格成本，判断 11 天内是否可完成。
- **风险**：benchmark 论文需要大量算力与多种子；11 天内全网格几乎不可能；
  但可以作为 I1 的副产品先交付一个"mini-benchmark"。
- **11 天可投性**：低（全量）；中（作为 I1 附表）。

---

## 漏斗提示（给评审用）

- 最可能"有搞头"：I1（机制最硬）、I3（最快出结果）、I6（I1 的副产品）。
- 最可能被 CCF 判致命：I4（CVPR fit）、I5（拼盘 + 撞车）、I2（与 P4 泛化结论边界模糊）。
- 所有 idea 都必须在评审中回答同一个问题：**相对 arXiv:2610.10023，增量是否足以撑起 CVPR 主会？**
