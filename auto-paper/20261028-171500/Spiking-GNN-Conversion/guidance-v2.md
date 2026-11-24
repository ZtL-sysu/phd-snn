# Guidance v2 — 由图上的 ANN→SNN 转换分析驱动的论文（按实际卖点重写）

> **来源与关系。** 本文件是 v1（`guidance.md`）的**事后重写版**：v1 写于实验之前，把"邻域到达分布
> 校准 + TPP 补偿"当作核心方法；实验做完后，其中两条假设被数据否掉（TPP 在 T≥2 反而更差；到达
> 分布不需要估计，因为相对误差 ρ-不变），另有一条卖点方向相反（脉冲数不降反升）。v2 不修改历史，
> 只把**已经被证据支持的东西**重新组织成一份可执行的 guidance。v1 保留在 `guidance.md` 作为记录，
> 差异台账见 `audits/p16-p17-length-and-guidance-audit.md`。

## Title / Topic

- 工作标题：*Converting Graph Neural Networks to Spiking Networks: Neighbourhood Temporal
  Misalignment, a Closed-Form Bias, and a Membrane Readout*
- 领域：图表示学习 × 类脑计算（图上的转换，而非直训）
- 目标层级：**先 B 会稳收（IJCNN / ICONIP / CIKM），A 会（NeurIPS/ICLR/KDD）作为升级路径**，
  升级所需的两项工作见文末"升级 backlog"
- 定位一句话：**不是"又一个脉冲 GNN"，而是"图上的 ANN→SNN 转换第一次被写成可分析的对象"**

## Core Idea

把训练好的两层 GCN 忠实地转成脉冲网络时，障碍不是量化精度，而是**邻域内没有共同时钟**：第二层
积的是邻居在各自相位上发出的脉冲，所以部分和 `inst_t` 不是 `B2` 的任何有意义的偏序和。把它写成
精确恒等式后，误差自然分成"邻域会平均掉的部分"和"平均不掉的部分"，由此得到三件事：

1. 系统项是一个**闭式偏置** `β* = θ/(2T)`（机制继承 FTBC，取值与 ρ-加权是本文的）；
2. **相对误差与行和 ρ 无关**（推翻"sum 聚合必崩"的初始预测），真正控制量是 `‖a_n‖₂‖DW‖₂/(TΔ_n)`；
3. 用**膜电位**而非脉冲计数解码，恒等式下免费去掉输出量化与截断天花板。

卖点排序（写作时按此顺序，不要倒过来）：
**部署灵活性（训练一次、任意 T 部署）> 低时延 > 无标定的闭式解 > 理论可核查性**。
**能耗不在卖点里**（见 Non-goals）。

## Paper Story

- **Problem**：图模型要上边缘/神经形态硬件，直训脉冲 GNN 的代价是"每个 T 都要重训一次反向"，
  且精度对 T 敏感；现场无法改 T。
- **Gap**：视觉/序列的转换已经能低时延逼近 ANN，并且有理论；图上的转换**没有被分析过**——
  不是没人做脉冲 GNN，而是没人回答"把一个训好的 GNN 拆成脉冲网络会坏在哪里"。
- **Insight**：坏在邻域时序错位。给出精确恒等式，把"图"从背景变成误差的来源。
- **Evidence**：恒等式 → 闭式偏置 → 膜解码 → margin 定理；6 个图、7 seeds、两族直训基线、
  两档等精度带；定理 30/30 不被反例推翻，并量化其保守程度。

## Paper Outline（与实际定稿一致）

1. Introduction：转换在图上没有对应物 → 错位现象 → 恒等式 → 五条贡献（**含"我们不主张什么"**）
2. Related Work：转换线（Diehl→Rueckauer→QCFS→FTBC→TPP）、直训线、图算子；**单列"继承 vs 未继承"段**
3. Method：3.1 设定 → 3.2 错位与恒等式 → 3.3 IF 即精确 floor 量化器 → 3.4 闭式偏置 → 3.5 膜解码
   → 3.6 margin 定理 → 3.7 复杂度与部署
4. Experiments：4.1 协议 → 4.2 保真度 → 4.3 直训基线对比 → 4.4 消融 → 4.5 等精度时延（含**脉冲反向**）
   → 4.6 算子/异质泛化 → 4.7 定理检验与紧致度 → 4.8 规模=保真度而非榜单
5. Discussion：错位是方差现象而非偏置现象 → 界为何松、松在哪 → 边界（深度/算子/规模/能耗）→ 展望
6. Conclusion

## Experiment Plan

### Datasets（6 个，全部公开）
- 引文图：Cora / CiteSeer / PubMed（Planetoid 标准划分）
- 异质图：chameleon / squirrel（Geom-GCN 60/20/20）
- 规模图：ogbn-arxiv（169,343 节点，官方时间划分）
- **不使用**私有洪涝图（v1 计划项，本次不可得；替代理由：arxiv 测规模、chameleon/squirrel 测异质）

### Baselines（三条臂，全部同划分/同种子/同宽度）
- `conv`：本文转换（训练 ANN 一次，任意 T 复用）
- `direct`：常数电流直训脉冲 GCN，**两种 dropout 协议**（逐时间步 mask = 主基线；跨时间步共享 mask
  = 协议敏感性对照），每个 T 重训
- `poisson`：SpikingGCN 式速率编码直训（**formulation 级复现，不是 codebase 复现**）
- 上限：`oracle` 速率理想极限（不可部署，同时充当正确性检查）

### Variants / Ablations（T=8，7 seeds）
读取方式（膜电位 vs 计数）、有/无偏置、标量 vs 逐通道 β、IF vs TPP 神经元、θ∈{0.5,1,2}。
**每个变体必须配一个"严格更差"的对照**；退化为打平的（逐通道 β）要报告为"预测未失败"，不能删。

### Metrics
- 主：节点分类准确率（7 seeds 均值，配对 Wilcoxon；**注明 n=7 时 p 下限 0.0156**）
- 次：达到 ANN−1pp / −1.5pp 的最小 T（四臂 × 两档）
- 次：脉冲总数（**只作为代价指标报告，不作为卖点**）
- 不做：焦耳、硬件实测能耗

### Statistics
7 seeds + 配对 Wilcoxon（v1 写的 5 seeds/配对 t 已废止）。凡效应量小于复现噪声（≈0.7pp）的格，
一律报"打平"并同时给两档阈值。

### Hardware / Runtime
单卡 RTX 3060 12GB + 12 核 CPU。**直训基线必须在 GPU 上跑**：CPU 1343 ms/epoch vs GPU 33.5 ms/epoch
（40×），7-seed 全量从 6 小时降到 7 分钟。转换/理论臂是 NumPy，与设备无关，结果逐位不受影响。

### Stopping criteria
- 若 T≤8 落后 ANN >5% 且消融无救 → 机制证伪，退回"直训 + 转换对比"定位（与 v1 同）
- 若等精度下转换不是"从不更晚" → 放弃时延主张，只保留理论 + 保真度

## Expected Results（**已实测值，作为 v3 复现的验收线**）

- **minimum**：T≤16 时 ≥ ANN−3%，且优于无偏置 ≥2%
  → 实测：T=8 差距 0.34 / 1.24 / 0.17 pp；无偏置落后 2.96 / 6.45 / 1.53 pp ✔
- **strong**：T≤8 时 ≥ ANN−1.5%
  → 实测更强：**T=4 就进带**（三个引文图）✔
- **strong（时延）**：等精度下"从不更晚"，且在至少一个图上 ≤ 一半
  → 实测：Cora 8 vs 16（−1pp 带）、4 vs 8（−1.5pp 带）；CiteSeer 唯一达标；PubMed 打平 ✔
- **外部基线**：对 rate-coded（SpikingGCN 范式）在 13/15 格显著领先 ✔
- **理论**：30/30 格不被反例推翻；保守 3.2–6.7×，73–99% 松弛来自 Hoeffding 项 ✔
- **falsifier 全部成立**：计数解码 −3.68/−6.24/−0.01 pp；去偏置 −2.57/−4.94/−0.80 pp；
  θ=2 时 −32.45 pp ✔

## Non-goals（本次**不允许**出现的主张）

1. **不做能耗主张。** 实测：等 T 下转换脉冲约为直训的 2×；等精度下仍多 17%（Cora 83,392 vs 70,998）
   到 83%（PubMed）。任何"更省能"的表述都必须在下一轮被实测推翻前禁止。
2. **不做规模 SOTA 主张。** ogbn-arxiv 只证明"转换机制在 16.9 万节点上原样可跑且保真"。
3. **不做深度主张。** 只有两层；三层需要逐层 `‖a_n‖^ℓ` 追踪，未测。
4. **不碰学习型注意力。** GAT 的 per-edge 权重会破坏恒等式所依赖的固定算子；GAT 用 mean(SAGE)/
   sum(GIN) 两个算子替代，只主张算子族泛化。
5. **不宣称复现任何 codebase。** 基线是 formulation 级；SGNNBench 是"我们没进的榜"，要写出来。
6. **不宣称"首个图 SNN"。** 只宣称"首个针对 message passing 的转换误差分析（formulation-level）"。

## Figure/Table Decision Rules

- 图 1：方法框架 + 邻域错位 inset（矢量感；避免"手绘示意图"观感）
- 图 2：精度–时延曲线（三图并列，含 ANN 与 −1.5pp 带）
- 图 3：脉冲数–时延（**用于说明"省的是时间步不是脉冲"，不是能耗卖点**）
- 图 4：消融矩阵（灰=默认，彩=移除）
- 图 5：定理两 panel（certified vs preserved；界的三项分解）
- 表 1 主保真度；表 2 直训/速率编码对比（含配对 p）；表 3 消融；表 4 等精度双档；
  表 5 算子；表 6 规模/异质；表 7 定理检验
- 所有表由脚本从 `results/*.json` 生成，禁止手抄

## Citation Scope

- 关键词：ANN-SNN conversion、low-latency SNN、spiking GNN、neuromorphic、graph node classification
- 必引：FTBC (ECCV'24)、TPP/temporal misalignment (ICML'25)、QCFS (ICLR'22)、Deng & Gu (ICLR'21)、
  Kugele (Front. Neurosci.'20)、SpikingJelly、GCN/GAT/GraphSAGE/GIN、近年脉冲 GNN 直训工作
- 门禁：≥36 条且近 5 年严格过半（本版实测 45 条 / 24 条近五年 = 53%）
- **注意**：arXiv 预印本占比偏高，A 会版本应把其中若干替换为已正式发表的版本

## Traceability Checklist

| 要求 | 产物 | 验收 | 状态 |
|---|---|---|---|
| 转换框架 + 闭式校准 | §3.1–3.4 | T≤8 ≥ ANN−1.5% | ✔ 实测 T=4 进带 |
| 邻域错位机制 | §3.2 + 恒等式 | 消融：去偏置严格变差 | ✔ −2.57/−4.94/−0.80 pp |
| 膜电位解码 | §3.5 | 对计数解码严格更优 | ✔ −3.68/−6.24/−0.01 pp |
| 全精度上限 | 每表 ANN 列 + oracle | oracle 与 ANN 逐位相同 | ✔ gap 0 |
| 直训/转换基线 | 表 2 / 表 4 | 等精度不更晚 | ✔ Cora 2×、CiteSeer 唯一 |
| 定理可核查 | 表 7 + 图 5 | 30/30 不被推翻 | ✔ 违约率 ≤0.6% |
| 算子泛化 | 表 5 | ρ 跨两个数量级仍保真 | ✔ 0.13–0.59 pp |
| 能效证据 | —— | v1 要求"脉冲数低于直训" | ✘ **反向证据**，已转为 Non-goal |
| 真实应用域（洪涝图） | —— | v1 要求 | ✘ 数据不可得，用 arxiv+异质图替代 |

## 升级 backlog（把 4/10 推到 6–7 所需的最小改动，按性价比排序）

1. **配对 bootstrap 置信区间 + 每格"效应量/噪声"比**（把 Cora 的主张钉死或降级为打平）。
2. **一个已发表脉冲 GNN 的同划分复现**（哪怕只有 Cora），换掉"无外部锚点"这条致命伤。
3. **成本代理表**：脉冲数 × 突触事件数 + 膜更新数，找出转换真正更便宜的那个区间；
   若找不到，就把"仅时延"写成明确的设计选择而不是缺陷。
4. **三层实验**（一张表即可），把"仅两层"从边界变成结论。
5. **摘要加限定**："two-layer, transductive node classification"，消除"graph neural networks"的过度概括。
6. 表 3 把四行默认配置合并为一行 + 脚注。
