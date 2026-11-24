# Research Guidance File · v2（用户指令修订版契约）

> 版本关系：v1（`guidance.md`，2026-11-10 15:24）为冻结版 ViG 场景契约，本轮由用户明确改向，**不再作为本次 `f-research-v1` 运行的契约**；v1 及其全部证据、三轮独立评审、M0 实跑与校验记录完整保留，不删除、不改写。
> v2 变更依据：用户 2026-11-10 17:19 指令 —— 「核心还是用我们 1028 现有的那套方法搞起，只是放到视觉上去」「找那种带有图的视觉数据集」「和别人的 ann 转换 snn 算法做对比」「和 ann 做对比（+比能耗）」「组合起来也是有变化的，也是我们的创新」。
> 变更记录见 `contract-change-v1-to-v2.md`。本文件为 `f-research-v1` 的权威契约。

## Title / Topic

- Working title: **Converting Graph Neural Networks for Graph-Structured Vision: Exact Error Identity, Closed-Form Bias, and Energy-Efficient Spiking Inference on Superpixel Graphs**
- Target field: 类脑计算 / ANN→SNN 转换 × 图结构视觉分类；子域为消息传递算子上的转换误差与推理能效
- Target journal tier: Q1–Q2 类脑与神经网络期刊（IEEE TNNLS / Neural Networks 档）；CVPR/ICCV 档需后续补齐更大规模证据
- Technique/method: **完整沿用 1028 成稿方法组合** —— 精确转换误差恒等式 `B̂−B = A(EW)`、闭式前向偏置 `β*=θ/(2T)`、膜电位累加解码替代计数解码、邻域时序错位的 ρ_n 加权分析、margin 恢复界；迁移到图结构视觉分类
- Selected application scenario: **SuperPixel MNIST / SuperPixel CIFAR10**（图像经 SLIC 转成超像素图，8-NN 带权邻接，10 类图级分类）—— 数据集本身即带图结构，无需人工造图、无需冻结 KNN、无需线性化非线性聚合
- Contribution framing（按用户定位）: **组合与适配创新**。单个组件各有出处（Deng&Gu ICLR'21、QCFS ICLR'22、FTBC ECCV'24、Dual-Phase TNNLS'24、TPP ICML'25），但把这一整套「精确误差恒等式 + 闭式偏置 + 膜电位解码 + 邻域错位分析」组合、适配到**自带图结构的视觉分类**这一新算子类与新任务类，并给出与全套转换方法的统一横评与 ANN/能耗对照，此前未见报道。论文据实写明继承关系，不声称发明单个组件，主张的是组合在新场景的可分析性、精度—时延—能耗三重收益。

## Core Idea

把 1028 成稿的 GNN→SNN 转换管线（`experiments/core.py` 的 `train_ann` / `convert` / `check_identity`）迁移到**图级视觉分类**：每张图像是一张超像素图，节点是超像素，边是 8-NN 带权邻接；用两层 GCN 消息传递 + 全局平均池化读出产生图级 logits。全局平均池化是固定线性算子，因此成稿的恒等式在 `R A (EW)` 形式下**精确成立**，其中 R 为池化矩阵、A 为块对角超像素邻接；这使 ρ_n 加权的系统误差、闭式偏置、膜电位解码与 margin 界都能原样迁移，且不需要对骨干做任何削弱性改造。

与 1028 的差异是**任务类与证据包**：1028 是单大图节点分类、只与直训脉冲 GNN 比较、未与其他 ANN2SNN 转换方法比较、未做能耗对照；本作是图级视觉分类、与全套转换方法在同一 teacher/同一 T/同一 split 下横评、并加入 ANN 精度上限与理论算术能耗对照。这正是用户指出的「组合起来有变化」的落点。

### Mechanism-Level Rationale

- Domain bottleneck: 视觉数据集一旦以图表示，聚合算子 A 的行和 ρ_n 远离 1（8-NN 带权邻接 + 对称归一化），为 ρ≈1 的卷积算子推导的转换校准律不再自动成立；同时边缘视觉部署要求精度、时延、能耗三者同时可查
- Why the chosen technique fits: 恒等式把误差压缩为 `R A (E W)`，闭式 `β*=θ/(2T)` 消去系统项，膜电位解码去掉 1/T 网格与单位截断天花板，邻域时序错位分析给出 `‖a_n‖₂‖DW‖₂/(TΔ_n)` 型恢复界；这些机制对任意固定非负线性 A 成立，超像素 kNN 图正是该类成员
- What must be changed or adapted: 输出层加线性池化 R；把单图 N×N 邻接换成批内块对角稀疏邻接；训练目标从节点分类交叉熵改为图级交叉熵；`convert` 的 `inst1` 与 `acc_out` 相应改为按图归约
- Why this is more than applying method X to dataset Y: 新算子类（非行随机视觉 kNN 图）+ 新任务类（图级视觉分类）+ 新证据包（全套转换方法横评 + ANN 上限 + 理论能耗）+ 组合在新类上的恒等式重新推导与数值验证；不是把同一套代码换个数据集重跑

## Paper Story

- Central scientific question: 一整套为图节点分类组合起来的 ANN→SNN 转换方法，在**自带图结构的视觉分类**上能否同时保持 ANN 精度、低时延与算术能耗优势，并优于单点的视觉转换方法
- Intended reader and why the question matters: 类脑视觉与图学习交叉方向的研究者；图结构视觉表示正在普及，而转换理论与能效证据仍集中在 CNN 网格上
- Domain/theory problem → design requirement → candidate method choice: 非行随机聚合 + 图级读出 → 需要算子级精确误差刻画与线性读出 → 1028 组合（恒等式 + β* + 膜电位解码 + 邻域错位）+ 统一协议横评
- Expected contribution type: 方法组合在新算子类/任务类上的适配与理论分析 + 系统实证比较 + 精度/时延/能耗三重证据
- Opening problem: 低时延 ANN→SNN 转换在规则网格视觉上已成熟，但图结构视觉表示与能效对照缺少统一分析
- Why existing work is insufficient: 视觉转换方法各自为 CNN 校准；One-Spike SNN 跨过 CNN+GCN 但无算子级误差刻画；1028 有精确误差理论但只在引文图节点分类验证且未与转换方法横评、未比能耗
- Core insight: 只要读出是线性算子，池化不破坏恒等式；因此整套组合可迁移到图级视觉，且非行随机 ρ_n 使闭式偏置与膜电位解码的收益比在 CNN 上更可观测
- What evidence should convince the reader: ① 恒等式在新管线上的浮点残差；② 与 ANN teacher 的精度差 ≤1.5pp（T≤8）；③ 与 QCFS/FTBC/TPP/并行转换适配基线的同协议横评；④ 消融隔离 β*、膜电位解码、确定性两阶段、邻域错位校准；⑤ 与 ANN 的 MAC 对照和 SNN 的 AC/SynOps 理论能耗估算；⑥ 5 seeds 配对 CI 与 BH
- Planned claim (not an observed finding): 在 SuperPixel MNIST / CIFAR10 上，1028 组合方法在 T≤8 达到 ANN−1.5pp 带内，优于各单点转换基线，且理论算术能耗显著低于同架构 ANN
- Finding to assess after experiments (leave unresolved until evidence exists): 上述精度、横评优势与能耗比**全部待 P3/P4 实测裁定**；本 guidance 阶段不产生任何结果数值
- Main claim: 组合式图转换框架可迁移到图结构视觉分类，并在精度—时延—算术能耗三方面给出可复算证据
- Boundary of the claim: 覆盖固定、非负、线性的超像素邻接与线性全局池化；不覆盖动态图、注意力重加权、非线性池化；能耗为基于操作计数的理论估算，不是神经形态硬件实测焦耳数
- Skeptical-reviewer hook: 「只是把 1028 换个数据集，组件都是别人的」—— 论文用组合在新算子类上的恒等式重推、全套转换方法横评、ANN/能耗对照与逐组件消融正面回答
- Strongest competing paper and why this is still distinct: One-Spike SNN（跨 CNN+GCN 转换，IEEE TETC 2024/25）与 Dual-Phase（精确等式 + 膜电位解码，TNNLS 2024）；二者均未覆盖超像素图视觉分类的图级读出、全套转换方法统一横评与理论能耗对照

## Paper Outline

1. Introduction: 图结构视觉表示与低时延转换的缺口；明确 1028 组合的继承关系与本作的新算子类、新证据包；列出精度/时延/能耗三问
2. Related Work: 转换误差理论（Deng&Gu、QCFS、FTBC、Dual-Phase、PASCAL）、低时延转换（TPP、并行转换、DCGS、AdaFire）、跨骨干与图转换（One-Spike SNN、SpikingGCN）、超像素图视觉（SLIC、Benchmarking GNNs、ViG）、能耗模型（Horowitz 45nm 表）；逐条写明继承与差异
3. Method: 超像素图与块对角邻接、图级线性读出 R、恒等式 `B̂−B=R A(EW)` 的推导、ρ_n 加权系统项、闭式偏置、膜电位解码、确定性两阶段、邻域时序错位与 margin 界、MAC/AC 理论能耗模型、适用条件与失效边界
4. Experiments and Results: 统一协议（同一 teacher/T/θ/split/seed）；主表 accuracy 与 conversion loss–T 曲线；全套转换基线横评；ANN 上限与理论能耗对照；逐组件消融；恒等式数值验证；统计检验
5. Discussion: 组合创新的边界（哪些是继承、哪些是新适配）、理论能耗估算与硬件实测的差别、超像素图相对 CNN 网格的差异、G2 排除大规模数据集对外部效度的影响、威胁到效度
6. Conclusion: 组合式图转换框架在图结构视觉上的可迁移性与三重收益，给出可复算协议与后续硬件实测方向

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| SuperPixel MNIST | `https://data.dgl.ai/dataset/benchmarking-gnns/MNIST.pkl` | 官方 benchmark 发布，无审批 | 主数据集一 | 1.39 GB，70,000 图，40–75 节点/图 | 10 类手写数字 | 官方 55,000 train / 5,000 val / 10,000 test | direct-public |
| SuperPixel CIFAR10 | `https://data.dgl.ai/dataset/benchmarking-gnns/CIFAR10.pkl` | 官方 benchmark 发布，无审批 | 主数据集二 | 2.51 GB，60,000 图，85–150 节点/图 | 10 类自然图像 | 官方 45,000 train / 5,000 val / 10,000 test | direct-public |
| 备选自构 patch 图 | `https://www.cs.toronto.edu/~kriz/cifar.html` | license NOT VERIFIED，仅引用要求 | 官方 pkl 不可得时的可复现替代 | 170,498,071 B | 10 类 | 固定 seed 从官方 train 切 45k/5k，test 10k 仅最终一次 | direct-public |
| Cora / CiteSeer / PubMed | `https://github.com/kimiyoung/planetoid` | NOT VERIFIED，引用要求 | 复现 1028 基线的回归锚点 | 逐文件公开直链 | 7 / 6 / 3 类 | PyG `split='public'`，不重切 | direct-public |

图构造口径（官方 pkl 已是图）：SLIC 超像素为节点，节点特征为超像素强度与坐标，8-NN 带权邻接 `W_ij = exp(−‖x_i−x_j‖²/σ_x²)`；批内以块对角稀疏矩阵拼接，全局平均池化 R 为固定线性算子。备选自构图仅在官方 pkl 下载或解析失败时启用，且须在结果中标注为不同数据源、不得与官方结果混列。

### Baselines

- Simple baseline: 朴素 rate 转换（无偏置、无校准、计数解码），作为一切改进的零点
- Matched internal baseline: 同一 teacher、同一骨干、同一 T 下逐一关闭组件的消融臂（去 β*、改计数解码、去两阶段、去 ρ 加权校准）
- Domain-standard baseline to rerun/adapt: ANN teacher（两层 GCN + 线性全局池化，图级 top-1 为精度上限与 conversion loss 基准）
- Strong recent baseline to rerun/adapt: QCFS（clip-floor-shift 激活 + 量化步长 L=T）、FTBC（前向时序偏置，含网格搜索与闭式两版）、TPP（两阶段概率神经元）、Parallel Conversion（并行脉冲简化适配）逐一适配到超像素图消息传递层
- Strong recent baseline for literature context only: DCGS（ICML'25）、AdaFire（AAAI'25）、PASCAL（TMLR'25）、CS-QCFS（Neural Networks'25）、One-Spike SNN（IEEE TETC'25）；无官方码或需重训的适配结果如实标注
- Technique-family baseline: 直接训练的脉冲 GCN（替代梯度，同架构同 T 重训），作为训练路线的对照
- Upper-bound or oracle-style comparison, if applicable: 冻结 ANN teacher top-1（conversion loss 的分母基准，不是可超越目标）
- Strongest expected comparison: FTBC/QCFS/TPP 在**同一超像素图骨干、同 T/θ/calibration** 下与 1028 组合方法的 conversion loss 差值
- 统一协议细则见 `matched-protocol.md` v1，v2 增补「图级池化与批内块对角邻接」条款

### Proposed Method Variants

- Main method: 1028 组合全量 —— 精确误差恒等式导出的 `β*=θ/(2T)`、膜电位累加解码、邻域错位 ρ_n 加权分析、确定性两阶段第二相 `s[t]=round(tn/T)−round((t−1)n/T)`、图级线性池化
- Variant A: 仅 β*（其余用朴素 rate 与计数解码），隔离闭式偏置贡献
- Variant B: β* + 膜电位解码（保留确定性/随机第二相对照），隔离解码贡献
- Implementation notes: 复用 `auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv/experiments/core.py` 的 `train_ann` / `convert` / `check_identity` / `gauge_normalize`，仅新增 `vision_core.py` 处理块对角邻接与图级池化；环境 `dyg-cold`（torch 2.11.0+cu128 / numpy 2.4.4 / scipy 1.18.0 / PyG 2.8.0 / CUDA 12.8 / RTX 3060 12GB）

### Metrics

- Primary metric: 图级 top-1 accuracy（%）；与之配对报告 `conversion loss = ANN teacher top-1 − SNN top-1`（pp，越低越好）
- Secondary metrics: 达到 ANN−1.5pp 带内所需最小 T、恒等式浮点残差、`argmax` 一致率、Σs[t]=n 命中率与第二相条件方差、逐图 spike 密度分布
- Efficiency metrics: ANN 的 32-bit MAC 计数、SNN 的 AC/SynOps 计数、按 45 nm CMOS 表（MAC 4.6 pJ、AC 0.9 pJ）估算的理论算术能耗与能耗比、峰值显存与 wall-clock；**理论估算与硬件实测严格区分**
- Statistical test / confidence reporting: 5 个冻结 seed（0–4）；seed 级配对 bootstrap R=5000 给 95% CI；sign-flip 置换 1000 次；多比较 BH 校正 q<0.05；主表报均值±std 与配对差值 CI，不报单 seed 最好值

### Required Ablations

- Ablation 1: 去 β*（β=0）—— 系统项是否按 ρ_n 加权、闭式偏置是否必要
- Ablation 2: 计数解码 vs 膜电位累加解码 —— 量化 1/T 网格与单位截断的代价
- Ablation 3: 确定性第二相 vs TPP 随机第二相 —— 零条件方差是否带来可测系统收益
- Robustness or subgroup analysis: 按图节点数/平均度/ρ_n 分桶；替换超像素邻接为对称归一化/mean/sum 三种算子；替换全局平均池化为全局求和池化；阈值 θ ∈ {0.5, 1.0, 2.0} 敏感性
- Error analysis: 逐图层 `B̂−B` 与 `R A(EW)` 残差分解、系统项 vs 波动项、margin 界覆盖率、失效案例的图结构统计

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / 548 GB 空闲；`C:\Users\xhf\miniconda3\envs\dyg-cold`
- Optional remote fallback, only if authorized: 用户已授权大规模实验上 `novix-platform` / `exp-4090`；本轮 guidance 与 P0–P5 以本机为主，全量扩展时按 `--provider novixlet --resource-pool exp-4090 --gpu --gpu-count 1` 提交，不写端点或凭据
- GPU/CPU: 本机 1×3060 + 12 核；远端 GPU 未在本轮探测
- RAM: 技能探针未返回，NOT VERIFIED
- Disk: 548,335,472,640 B 空闲；两个官方 pkl 合计约 3.9 GB
- Max runtime per run: 本机单臂 ≤30 min（含 5 seeds）；全量扩展转远端 ≤6 h/臂
- Max total runs: 2 数据集 × 5 seeds × 5 T × (1 ANN + 5 转换基线 + 3 变体 + 7 消融)，按 `experiment-traceability.md` 分批
- Frozen train/validation/test identifiers and validation-only selection policy: 使用官方 pkl 自带 55k/5k/10k 与 45k/5k/10k 划分，冻结图索引与 SHA-256；只在 val 上选择超参；test 只在最终评测用一次
- Full search/trial ledger and held-out test isolation: 每次运行落 `config.json`、teacher 权重/图文件 SHA-256、seed 列表、环境快照；超参搜索预算每方法 ≤12 组，全部记入 trial ledger
- CCFA packet path and feasibility-contract.json: 复用 v1 的 `ccfa-startup-packet/`，并在 P1A 生成 v2 对应的 `claim-evidence-matrix-v2.md` 与 `strong-result-feasibility-lock.md`
- Resource budget exhaustion and next-candidate decision rule: 单臂超时或显存溢出时先降子集规模与 batch，仍失败则记录 `infeasible-with-evidence` 并进入授权修正回路
- Scaling fallback: 先用每数据集固定子集（train 5,000 / val 1,000 / test 2,000）跑通全管线与全部基线，再在 3060 上扩到可用规模，CIFAR10 全量训练转远端 4090
- Stopping criteria: 恒等式残差超浮点容差、官方数据解析失败且备选自构图不可用、最强基线复现失败、或能耗估算口径不自洽时停止并回退到 P2/P3

## Expected Results

- Minimum acceptable result: 两个超像素图数据集上，主方法 T≤8 的 conversion loss ≤3.0pp；至少在一个数据集上 T≤4 优于全部单点转换基线；恒等式残差在浮点容差内；理论算术能耗比 ANN 更低
- Strong result: 两数据集均在 T≤8 达到 ANN−1.5pp 带内（以 1028 成稿在三个引文图 7 seeds 的实测水平为 baseline-calibrated 依据）；T≤4 时相对最强单点转换基线 conversion loss 低 ≥1.0pp（配对 bootstrap CI 下界 >0、BH q<0.05）；理论算术能耗比 ANN 低 ≥5×；逐组件消融方向一致
- Failure signal: 恒等式残差超容差；T≤8 conversion loss 持续 >5pp；任一数据集上理论算术能耗比 ANN 无优势（≤1×）或低于 2× 而 spike 密度未显著低于 ANN 激活密度；消融方向与机制预测相反
- What to do if minimum is not reached: 保留全部负结果，检查数据对齐、阈值尺度、池化算子与基线适配；加强基线、调参、补消融后重跑；不得下调阈值、不得挑 seed、不得删负结果
- Claim adjustment rule if expectations fail: 若能耗优势只在理论操作计数成立而无法在可实现稀疏度下兑现，收窄为「稀疏活动与 SynOps 代理指标」的表述；`observed_finding` 由 P5A 依证据填写，不由 planned_claim 推定
- 能耗假设（用户预判「一定有优势」，此处按可证伪方式预注册）: 在 ANN−1.5pp 带内，转换后 SNN 的 AC 操作数与 0.9 pJ/AC 之积低于 ANN 的 MAC 数与 4.6 pJ/MAC 之积至少 5×；这是**理论算术能耗估算，不是硬件实测**，须与 spike 密度、SynOps、wall-clock 一并报告

## Figure/Table Decision Rules

Do not lock final figure/table contents before experiments are completed; define evidence-driven decision rules instead.

- Required first figure type: 方法定稿后直接生成一张框架/架构图，展示超像素图 → 两层消息传递 → 线性全局池化 → 脉冲转换与 ANN/能耗对照；只画经证据确认的组件与标签
- Required experiment visualizations if supported by data: 每数据集一张 accuracy–T / conversion loss–T 曲线（含全部基线与 95% CI 带）；ρ_n 分桶的误差分解图；能耗比与 spike 密度的联合图（若能耗假设成立）
- Required result tables if supported by data: 主表（方法 × T × 数据集的 top-1 与 conversion loss、配对差值 CI、BH q）、消融表、理论—仿真一致性表（恒等式残差、Σs=n 命中率）、ANN vs SNN 的 MAC/AC/SynOps/理论能耗对照表
- Author or venue figure/table requirements, with source (if any): 具体 venue 官方当年页限与图表规则尚未核验，确认前只按 venue-family 通用期望设计
- Evidence that may benefit from a visual: 非行随机 ρ_n 的系统误差加权、膜电位解码去掉 1/T 网格的收益、确定性第二相的零方差、ANN 与 SNN 的操作计数差距
- Rules for excluding weak or misleading plots: 任何只显示单 seed 最好值、隐去 CI、隐去负结果、或把理论估算画成硬件实测能耗的图一律不进正文
- Scientific claims for which a figure/table would aid inspection (optional): 「精度—时延—能耗三重收益」由 loss–T 曲线与能耗对照表共同支撑，二者缺一不可
- Final count and placement are chosen after evidence stabilizes; no per-subsection quota applies.

## Traceability Checklist

| Requirement | Dataset | Baseline/method/ablation | Metric | Expected result | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|---|
| 恒等式在图级管线上精确成立 | SuperPixel MNIST/CIFAR10 | 固定线性 A + 池化 R vs 动态/非线性变体 | 恒等式浮点残差 | 类内 <1e-12，类外显著非零 | 理论—仿真一致性表 | yes |
| ANN 精度上限 | 两数据集 + Planetoid 回归锚点 | ANN teacher | 图级 top-1 | 作为 conversion loss 分母 | 主表 | yes |
| 全套转换方法横评 | 两数据集 | QCFS/FTBC/TPP/Parallel 适配 + 朴素 rate + 直训 SNN | conversion loss | T≤4 相对最强基线低 ≥1.0pp（预注册） | 主表 + loss–T 曲线 | yes |
| 1028 组合主臂 | 两数据集 | 主方法 + Variant A/B | top-1 / conversion loss | T≤8 达 ANN−1.5pp 带内（预注册） | 主表 | yes |
| 闭式偏置贡献 | 两数据集 | 消融 1 去 β* | conversion loss、margin 平移 | 去偏置后随 ρ_n 放大 | 消融表 + ρ_n 分桶图 | yes |
| 膜电位解码贡献 | 两数据集 | 消融 2 计数解码 | conversion loss | 去掉 1/T 网格后改善 | 消融表 | yes |
| 确定性第二相 | 两数据集 | 消融 3 TPP 随机相 | Σs=n 命中率、条件方差、conversion loss | 零方差成立、系统收益待裁定 | 消融表 | yes |
| ANN vs SNN 能耗对照 | 两数据集 | ANN teacher vs 主方法 | MAC/AC/SynOps、理论算术能耗比 | 能耗比 ≥5×（预注册假设） | 能耗对照表 | yes |
| 统计稳健性 | 两数据集 | 全部方法 | 配对差值 95% CI、BH q | CI 与 q 完整报告 | 主表附注 | yes |
| 算子与阈值鲁棒性 | 两数据集 | 三种归一化、两种池化、θ∈{0.5,1,2} | conversion loss | 方向一致 | 稳健性表 | yes |
| 复现 1028 回归锚点 | Cora/CiteSeer/PubMed | 1028 原管线 | 节点分类 top-1 | 与成稿 shipped numbers 一致到 0.003pp | 回归锚点表 | yes |

## Citation Scope

绑定政策沿用 `f-guidance-builder-v1/references/citation-requirements.md`：`min_unique=36`、`as_of=2026`、`recent_window_years=5`（2022–2026 含端点，rationale 为 QCFS ICLR 2022 建立 clip-floor-shift 范式）、严格近期多数；最终真实性、命题级支撑、去重与数量/年份算术由 `f-research-v1` P12/P14 复核。

- Must-cite foundational papers: Maass 1997; Diehl et al. IJCNN 2015; Rueckauer et al. Front Neurosci 2017; Sengupta et al. Front Neurosci 2019; Han et al. CVPR 2020 (RMP-SNN); Deng & Gu ICLR 2021; Kipf & Welling ICLR 2017; Veličković et al. ICLR 2018; Hamilton et al. NeurIPS 2017; Yang et al. ICML 2016; Krizhevsky 2009; LeCun et al. 1998 (MNIST); Achanta et al. IEEE TPAMI 2012 (SLIC); Knyazev et al. NeurIPS-W 2019 (graph attention pooling); Kugele et al. Front Neurosci 2020; Horowitz, IEEE ISSCC 2014 (45 nm MAC/AC energy table); Orchard et al. Front Neurosci 2015; Li et al. Front Neurosci 2017 (CIFAR10-DVS); Neftci et al. IEEE SPM 2019
- Must-cite recent papers: Dwivedi, Joshi, Laurent, Bengio, Bresson, JMLR 2023 / arXiv:2003.00982 (Benchmarking GNNs, SuperPixel MNIST/CIFAR10); Han et al. NeurIPS 2022 (Vision GNN, arXiv:2206.00272); Bu et al. ICLR 2022 (QCFS, arXiv:2303.04347); Liu et al. AAAI 2022 (SpikeConverter); Fang et al. Science Advances 2023 (SpikingJelly); Eshraghian et al. Proc IEEE 2023; Wu et al. ECCV 2024 (FTBC, arXiv:2403.18388); Bojković et al. PMLR v238 2024; Dual-Phase, IEEE TNNLS 2024; Hwang & Kung, IEEE TETC 2025 / arXiv:2403.08786 (One-Spike SNN); Bojković, Wu, Gu, ICML 2025 (TPP, arXiv:2502.14487); Hao et al. ICML 2025 (Parallel Conversion, arXiv:2412.13610); Huang et al. ICML 2025 (DCGS, arXiv:2503.00301); Wang et al. AAAI 2025 (AdaFire, arXiv:2311.14265); Ramesh & Srinivasan, TMLR 2025 (PASCAL, arXiv:2505.01730); Yang et al. Neural Networks 2025 (CS-QCFS); Liu et al. arXiv:2506.01968, 2025 (ECL); Jiang et al. NeurIPS 2025 (Adaptive Fission); SGNNBench, arXiv:2509.21342, 2025; Zhou, Chen, Datta, IEEE ICEdge 2025; Chen et al. arXiv:2608.13952, 2026; Ji et al. IEEE DLCV 2026; Xia et al. Neurocomputing 670:132604, 2026
- Dataset papers: Benchmarking GNNs (SuperPixel MNIST/CIFAR10 官方 pkl 与 split)、SLIC、CIFAR tech report、MNIST、Planetoid、Vision GNN
- Baseline papers: 见 `literature-baseline-matrix.md` 全表
- Search keywords: `ANN-to-SNN conversion error identity`；`superpixel graph classification`；`graph message passing spiking conversion`；`non-row-stochastic aggregation calibration`；`membrane potential readout`；`SynOps energy estimation spiking neural network`；`45nm MAC AC energy`
- Target recency: 2022–2026 严格多数；保留必要奠基工作真实年份；不把访问年份当发表年份；预印本与正式版不重复计数
- Excluded areas: 神经形态芯片实测焦耳数、生物保真建模、ImageNet-1K 全量 SOTA、纯直训脉冲 GNN 精度竞赛
- Recency expectation and its source; retain relevant foundational work: 来源为 f 系列绑定默认；Horowitz 2014、SLIC 2012、Maass 1997 等奠基工作保留但不冒充近年工作
- 待 P12 核验项（不得当成已确认条目）: Dual-Phase TNNLS 2024 卷期页、Fang et al. Science Advances 2023 DOI、ECL 正式 venue、Deng & Gu ICLR 2021 正式 DOI、Horowitz 2014 表中 0.9pJ/4.6pJ 的原文页码

## Novelty And Feasibility Summary

- Literature/baseline map verdict: G0 pass —— 1028 组合的组件出处清楚，超像素图视觉分类与全套转换方法横评的组合未见报道；基线矩阵见 `literature-baseline-matrix.md`
- Dataset access verdict: G1 pass —— 官方 `data.dgl.ai` 两个 pkl 直链实测 HTTP 200，无需审批，官方 split 齐备；备选自构图路径已登记
- Task/evaluation verdict: G2 pass —— 图级 10 类分类，官方 train/val/test，主指标与统计协议明确
- Theoretical fit verdict: G3 pass —— 线性全局池化不破坏恒等式；M0 已实跑验证固定线性算子类上的恒等式与上界（`evidence-snapshots/m0-results.json`）
- Novelty verdict: G4 pass（组合与适配定位）—— 不声称发明单个组件，主张组合在新算子类/任务类的可分析性与三重收益
- Hardware feasibility verdict: G5 pass —— 3060 12GB + 548 GB 空闲，分批/子集策略与远端 4090 回退明确
- Baseline/ablation feasibility verdict: G6 pass —— ANN 上限、朴素 rate、四个转换方法适配、直训 SNN、七项消融齐备
- Effectiveness plausibility verdict: G7 pass（预注册，非实测）—— 以 1028 成稿 7 seeds 的 ANN−1.5pp 带内水平作 baseline-calibrated 锚点；能耗优势按理论操作计数预注册为可证伪假设
- Q2+ story verdict: G8 pass —— 组合创新定位、精度/时延/能耗三重证据、诚实边界与回退故事齐备

## Theoretical Feasibility Audit

- Mechanism expected to help: 误差经 `R A (E W)` 线性传播，ρ_n 只加权系统项，闭式偏置与膜电位解码分别消去系统项与输出量化
- Required assumptions: A 固定非负线性、池化 R 线性、亚阈值残差近似均匀独立、激活主要在 `[0,θ]`、所有方法同 teacher/θ/calibration/T
- Supporting literature: 1028 成稿（未发表内部成果，仅作方法出处）、Deng&Gu ICLR'21、QCFS/FTBC、Dual-Phase TNNLS'24、TPP ICML'25、SLIC 与 Benchmarking GNNs、Horowitz 2014
- Falsifying ablation: 去 β*、改计数解码、随机第二相、非线性池化与动态邻接变体
- Critical failure mode: 图级池化引入的归约使 margin 结构改变，导致闭式偏置不再最优；或 spike 密度不稀疏使理论能耗优势消失

## Story Strength Audit

- Why a top-journal reviewer should care: 图结构视觉表示正在普及，而转换理论与能效证据仍集中在 CNN 网格；一套可分析、可复算、含 ANN/能耗对照的组合框架有直接复用价值
- Strongest incrementality threat: One-Spike SNN 与 Dual-Phase 的组合，以及「只是把 1028 换数据集」的质疑
- Decisive distinguishing experiment: 同一超像素图骨干上全套转换方法横评 + 逐组件消融 + ANN vs SNN 理论能耗对照 + 图级恒等式浮点残差
- Strong-paper result threshold: 两数据集 T≤8 进 ANN−1.5pp 带、T≤4 优于最强单点基线 ≥1.0pp、理论能耗比 ≥5×，且消融方向一致
- Honest fallback story if only partially successful: 收敛为「首个图结构视觉分类上的转换方法统一横评与理论能耗分析」，保留全部负结果，不硬撑方法增益

## Constraints and Preferences

- Writing preference/source: 用户指定 `f-guidance-builder-v1` 定实验设置与故事、`f-research-v1` 做实验写文章、大规模上 `novix-platform`、小规模本机 3060 smoke
- Protected sections or edit scope/source: 1028 成稿目录只读、不改写、不投稿；资料库报告只读；v1 guidance 与其全部证据只读
- Journal page/word/figure requirements and source: 具体 venue 官方当年规则未核验，确认前不套用页限或 artifact 规则
- Things the workflow must do: 保留三轮独立红队原文与分数；`expected_strong` 全部标预注册；test 隔离；所有数值由脚本从结果文件生成；不删除负结果；能耗明确标注为理论估算
- Things the workflow must avoid: 声称发明已被占的单个组件；把理论算术能耗写成硬件实测；把未发表 1028 结果当公开证据；挑 seed 或调参到显著
- Preferred writing language: 论文正文英文；内部研究与审计文档中文
- Preferred LaTeX/template/venue style: 待具体 venue 确认后由 P13/P15 决定

## Citation policy and pending facts

按 f 系列绑定默认执行 `min_unique=36`、严格近期多数、2022–2026 冻结窗口与独立数量/年份审计；按 `deferred-completion.md` 维护 `delivery-readiness.json` 与待办清单。`workflow_complete` 与 `submission_ready` 分开记录，当前 `submission_ready=false`（作者信息、投稿确认、代码发布安排、目标 venue 官方规则等待决）。行政待决项不阻塞本地科学阶段；科学证据、数据使用权、引用真实性、产物一致性仍是硬门。
