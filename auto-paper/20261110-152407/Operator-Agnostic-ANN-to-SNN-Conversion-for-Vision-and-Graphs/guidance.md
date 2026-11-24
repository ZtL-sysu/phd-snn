# Research Guidance File

## Title / Topic

- Working title: **When Does ANN-to-SNN Conversion Fail? A Matched-Protocol Study across Grid, Frozen-Graph Vision, and Graph Message-Passing Operators**
- Target field: 类脑计算 / 脉冲神经网络 × 视觉表征与图表示学习；具体子域为 ANN→SNN 转换误差分析与转换协议
- Target journal tier: **Q2-or-better，主投 IEEE TNNLS 档（Q1–Q2 类脑与神经网络期刊）**；不主张 CVPR/ICCV 主会档（缺 ImageNet-1K，属 G2 不可得）
- Candidate venues: IEEE TNNLS、Neural Networks、Neurocomputing、IEEE TCDS；CCF-A 主会仅在补齐 ImageNet 级证据并解决 novelty 后考虑
- Technique/method: 固定、非负、线性传播算子类上的转换误差统一刻画（精确误差恒等式 + ρ_n 加权闭式偏置 + 膜电位累加解码 + 确定性两阶段第二相），与全套主流 ANN2SNN 转换方法的 matched-protocol 横评
- Selected application scenario: **S2** — 冻结 KNN 图且线性化聚合的视觉图骨干（线性化 ViG）与图消息传递层共用同一算子；标准 CNN 作 ρ≈1 对照臂；原版动态/非线性 ViG 作失效边界。详见 `scenario-decision-log.md`
- 目录名沿用 `Operator-Agnostic-...` 仅为文件系统稳定；**全文禁用 "Operator-Agnostic" 命名**（独立红队指出它掩盖"仅适用固定线性算子"的强假设）

## Core Idea

在一篇已成稿、但不改动也不投稿的图转换工作（`auto-paper/20261028-171500/Spiking-GNN-Conversion/`）之上，另起一篇以视觉数据集为主战场的新作。成稿给出精确误差恒等式 `B̂₂ − B₂ = A (E₁ W₂)`、`β* = θ/(2T)`、膜电位累加解码与 margin 恢复定理，并在图节点分类上实测 T≤8 达 ANN−1.5pp 带内。本新作**不声称发明这些数学组件**（独立新颖性核验已确认它们分别属于 Deng&Gu ICLR'21、QCFS/FTBC、Dual-Phase TNNLS'24、PASCAL TMLR'25、TPP ICML'25 / SpikeConverter AAAI'22 / One-Spike SNN）。新作的核心是把问题反过来问：**当传播算子固定、非负、线性但行和 ρ_n ≠ 1 时，为 ρ=1 的行随机算子导出的校准律是否仍然最优？** 用同一个算子在视觉骨干与图消息传递层上，与全套 SOTA 转换方法做统一协议横评，并给出可证伪的失效边界。

### Mechanism-Level Rationale

- Domain bottleneck: 视觉侧转换方法（QCFS、FTBC、TPP、并行转换、DCGS、AdaFire）几乎都在 ρ≈1 的卷积/线性算子上推导与校准；视觉图骨干（ViG 的 KNN 图聚合）与 GNN 消息传递的行和可以远离 1（成稿实测 GCN 对称归一化 Cora 上 ρ_n 最高 5.75，sum 聚合可达 169）。缺少统一协议下的检验，也缺少"何时失效"的判据
- Why the chosen technique fits: 成稿已证误差**精确**等于 `A (E₁ W₂)`；对一般 A，`E[E₁] = β − 1/(2T)` 传播过 A 后 margin 平移为 `ρ_n/(2T)·Σ_h DW_c[h]`（按行和加权），而相对误差由 `‖a_n‖₂ ‖DW‖₂ / (T Δ_n)` 控制（ρ-不变）。M0 本机实跑已验证：25 格恒等式最大残差 `9.880984919163893e-15`、Hoeffding 型上界 0 违反、同一 problem 只缩放 A 时相对误差 ρ=0.5→10 为 `0.3056→0.3111` 且 argmax 一致率全 1.0
- What must be changed or adapted: 视觉侧把 ViG 的 KNN 图在前处理**冻结**并把 max-relative 聚合**线性化**，使其落入固定线性算子类；该替换相对原版 ViG 的 ANN teacher 精度代价必须量化，不得隐瞒。原版动态 KNN + max 非线性保留为失效边界诊断（M0 实测动态 A_t 残差 `0.7058297672203355`、max 非线性 gap `1.1668779395601996`，显著非零）
- Why this is more than applying method X to dataset Y: 贡献是「一个可先验计算、可证伪的算子类判据」加「首个含全部最近邻基线的 matched-protocol 横评」加「实测失效边界」，不是把某方法换个数据集跑一遍。判据 `κ_n = ρ_n / ‖a_n‖₂` 预测为 ρ=1 推导的校准律在 κ_n 大且 T≤4 时系统性欠校准，差距随 ρ_n/T 单调增大；ρ≈1 的 CNN 臂上则预测非劣效。**该预测尚未在真实训练网络上验证，属预注册主张**

## Paper Story

- Central scientific question: 为行随机传播算子导出的 ANN→SNN 转换校准律，在非行随机（ρ_n≠1）的固定线性算子上何时、为何失效
- Intended reader and why the question matters: 做低时延 SNN 转换与视觉图骨干/图学习的研究者。视觉骨干正从规则网格走向图与动态聚合，但转换误差理论仍隐含 ρ=1；若不界定适用类，低 T 下的精度损失无法归因
- Domain/theory problem → design requirement → candidate method choice: ρ_n≠1 → 误差必须按算子而非层类型刻画 → 固定线性算子类 + 统一协议（所有方法同一骨干/同一 teacher/同一 θ/同一 calibration 数据/同一 T 网格）→ ρ 加权闭式偏置与膜电位解码作为受控臂，PASCAL/TPP 作为最近邻对照
- Expected contribution type: 理论判据 + 评估/实证发现 + 失效边界诊断（empirical/diagnostic），接受 Q1–Q2 期刊的增量但充分验证定位
- Opening problem: 低时延 ANN→SNN 转换的精度—时延曲线在标准 CNN 上已很成熟，但同一套方法换到非网格聚合骨干时，误差从哪来、能否预测，没有统一答案
- Why existing work is insufficient: 各方法各自校准自己的算子；One-Spike SNN 已跨 CNN+GCN 但没有算子级误差刻画，Dual-Phase 已有精确等式但针对 ρ=1，PASCAL 已有确定性计数但未在 ρ≠1 上检验。最近邻工作密集（2024–2025 八篇），"再发明一个组件"不再可行
- Core insight: 误差恒等式把层类型差异压缩进一个矩阵 A；A 的行和 ρ_n 只改变**系统项**的权重，不改变**相对误差**的尺度，因此"何时失效"可由 ρ_n、margin 与 T 先验算出，而不必靠试 T
- What evidence should convince the reader: ① M0 级恒等式浮点残差与 ρ 加权/ρ-不变数值验证；② 含第 0 批 PASCAL/TPP 的统一协议 conversion loss–T 曲线；③ ρ_n/T 单调性的趋势检验；④ A1–A7 消融隔离每个组件；⑤ 原版 ViG 失效边界的定量报告；⑥ 5 seeds 配对 CI 与 BH
- Planned claim (not an observed finding): 在 ρ_n≠1 的固定线性算子上，按 ρ 加权闭式偏置校准的臂在 T≤4 的 conversion loss 优于按 ρ=1 校准的强基线，且差距随 ρ_n/T 增长；在 ρ≈1 的 CNN 臂上两者非劣效
- Finding to assess after experiments (leave unresolved until evidence exists): 上述单调性与增益**全部待 P4 实测裁定**；本次 guidance 阶段视觉侧 0 正式实验，任何结果数值都不得写入
- Main claim: 转换误差的适用边界由传播算子类决定；给出一个可先验计算的判据与可复算的统一比较协议
- Boundary of the claim: 只覆盖固定、非负、线性传播算子；动态 KNN 图、softmax 动态 attention、max-relative 非线性聚合**不在**适用类；不覆盖深度>2 的理论推导；不声称精度 SOTA、能耗实测或生物保真
- Skeptical-reviewer hook: 「`A(E₁W₂)` 只是已知逐层递归的矩阵重述，`s[t]` 只是 PASCAL+TPP 的组合」—— 这正是三轮独立红队的一致质疑，论文必须正面回答，不能绕开
- Strongest competing paper and why this is still distinct: One-Spike SNN（已跨 CNN+GCN）+ Dual-Phase（已有精确等式）+ PASCAL（已确定性计数）三者合起来几乎覆盖组件层；区别只能落在「ρ≠1 算子类上的可证伪判据 + 含全部最近邻的统一协议横评 + 实测失效边界」，且必须承认这是窄的增量贡献

## Paper Outline

1. Introduction: 低时延转换在 ρ≈1 视觉算子上的成熟、非网格聚合骨干的兴起、以及"误差何时失效"这一未被回答的问题；明确列出不声称的组件与适用类
2. Related Work: 转换误差理论（Deng&Gu、QCFS、FTBC、Dual-Phase）、低时延方法（TPP、并行转换、DCGS、AdaFire、PASCAL、CS-QCFS、ECL）、跨骨干转换（One-Spike SNN）、视觉图骨干（ViG）；逐条写明本文继承什么、不主张什么
3. Method: 固定线性传播算子类定义、精确误差恒等式、ρ_n 加权系统项与 ρ-不变相对误差、κ_n 判据、闭式偏置与膜电位解码（均注明出处）、确定性第二相、冻结/线性化的构造与其代价、适用条件 A1–A5 与失效边界
4. Experiments and Results: 统一 protocol（骨干 B1–B5、teacher/θ/calibration/T 网格、split 预注册）；主表 conversion loss–T；第 0 批 PASCAL/TPP；ρ_n/T 单调性趋势检验；A1–A7 消融；B4 失效边界；效率 proxy 与统计检验
5. Discussion: 三轮独立红队提出的 F1/F2/F3 如何被证据处理、T1 非平凡性的诚实评估、冻结/线性化代价、κ_n–T2 张力、G2 排除 ImageNet 对外部效度的影响、威胁到效度
6. Conclusion: 算子类决定转换误差适用边界；给出可复算的协议与判据；明确若判据被推翻则应收敛为纯 benchmark 故事

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| CIFAR-10 | `https://www.cs.toronto.edu/~kriz/cifar.html` | license NOT VERIFIED，仅引用要求 | B1/B2 主战场 | 170,498,071 B | 10 类，60k 图 | 50k train 切 45k/5k，10k test 仅最终一次 | direct-public |
| CIFAR-100 | 同上 `cifar-100-python.tar.gz` | license NOT VERIFIED | B1/B2 主战场 | 169,001,437 B | 100 细类 | 同 CIFAR-10 | direct-public |
| Tiny-ImageNet | `https://cs231n.stanford.edu/tiny-imagenet-200.zip` | 非商业研究条款 | B2 规模扩展 | 248,100,043 B | 200 类 | 100k train / 10k val 最终评测，test 无标签不用 | direct-public |
| CIFAR10-DVS | `https://figshare.com/articles/dataset/CIFAR10_DVS_New/4724671` | CC BY 4.0 | B5 稳健性（可选，不进主 claim） | 8,384,752,624 B | 10 类，10k 事件流 | 预注册社区 9000/1000，降采样 48×48 | direct-public |
| Cora / CiteSeer / PubMed | `https://github.com/kimiyoung/planetoid` | NOT VERIFIED，引用要求 | B3 同一算子的图侧通用性 | 逐文件，Cora `ind.cora.x` 22,119 B | 7 / 6 / 3 类 | PyG `split='public'`，不重切 | direct-public |
| ViG 代码与 8 个权重 | `https://github.com/huawei-noah/Efficient-AI-Backbones` | Apache-2.0 | 构造 B2/B4 骨干 | 29,090,248–382,087,395 B | 模型仓库 | 不做全量训练，权重用于推理评估 | direct-public |

被排除的 G2 数据（不得使用）：ImageNet-1K / ILSVRC（需账号+机构邮箱+人工审批）、ImageNet-100（无统一直链/split）、DVS128 Gesture（需登录手动下载）、N-MNIST（许可冲突且登录要求未核验）。详见 `dataset-access-log.md`。

### Baselines

- Simple baseline: 朴素 rate 转换（无偏置、无校准、计数解码），作为一切改进的零点
- Matched internal baseline: 同一 teacher、同一骨干、同一 T 下逐一关闭组件的 A1–A7 消融臂
- Domain-standard baseline to rerun/adapt: QCFS（锚点，先做 91.18%@T=2 / 93.96%@T=4 回归测试）与 FTBC
- Strong recent baseline to rerun/adapt: **第 0 批 PASCAL（无官方码，自行复现）与 TPP（官方码）**；第 1 批 Parallel Conversion / DCGS（CNN 子集）/ AdaFire（分类子集）
- Strong recent baseline for literature context only: Adaptive Fission NeurIPS'25、2026 的 RMP-Alignment / GTDL / Neurocomputing BPTT 微调类（无代码无可靠数值，只进 related work）
- Technique-family baseline: CS-QCFS、ECL（自行复现，复现失败须如实登记，不得用文献数值顶替主表）
- Upper-bound or oracle-style comparison, if applicable: 冻结 ANN teacher top-1（转换损失的分母基准，不是可超越目标）
- Strongest expected comparison: PASCAL（确定性精确计数）与 TPP（两阶段）在同一冻结/线性化骨干、同 T/θ/calibration 下的差异；若与之等价，按 S4 回退为纯 benchmark 故事
- 详见 `literature-baseline-matrix.md` 与 `matched-protocol.md` §6

### Proposed Method Variants

- Main method: OAC-rev2 主臂 = ρ 加权闭式偏置 `β*=θ/(2T)` + 膜电位累加解码 + 确定性两阶段第二相；全部组件明确归功前人
- Variant A: 仅 β*（无膜电位解码、无确定性第二相），用于隔离 ρ 加权校正
- Variant B: β* + 膜电位解码（保留随机/Bernoulli 第二相），用于隔离确定性化的边际贡献
- Implementation notes: 基于 `dyg-cold`（torch 2.11.0+cu128 / CUDA 12.8 / RTX 3060 12GB）；`torchvision` 缺失为 G6 blocker；6 个官方仓库的 torch 2.11 兼容性须先由 QCFS 回归测试锁定；ViG KNN 图在预处理冻结并落图文件 SHA-256；所有表由脚本从结果文件生成，禁止手抄

### Metrics

- Primary metric: `conversion loss = ANN teacher top-1(%) − SNN top-1(%)`，单位 pp，越低越好
- Secondary metrics: 达 ANN−1.5pp 带内所需最小 T、`argmax` 一致率、恒等式浮点残差、Σs[t]=n 命中率与第二相条件方差、ρ_n/T 趋势检验的斜率与 CI
- Efficiency metrics: SynOps、spike count、峰值显存、wall-clock —— **全部标注为 proxy**，不写成能耗实测
- Statistical test / confidence reporting: 5 个冻结 seed（0–4）；seed 级配对 bootstrap R=5000 给 95% CI；sign-flip 置换 1000 次；多比较 BH 校正 q<0.05；主表报均值±std 与配对差值 CI，不报单 seed 最好值

### Required Ablations

- Ablation 1: A1 去 β*（β=0）—— 验证系统项是否真按 ρ_n 加权
- Ablation 2: A2 计数解码 vs 膜电位累加解码 —— 判定两解码是否冗余，冗余则删组件
- Ablation 3: A3 Bernoulli 第二相 vs 确定性 s[t] —— 判定确定性化是否只有"零方差"这一同义反复
- Robustness or subgroup analysis: A4 去累积相、A5 固定图 vs 动态图、A6 线性聚合 vs 原版 max-relative（并量化冻结/线性化代价）、A7 ρ≈1 的 CNN 臂 vs ρ≠1 的 B2/B3 臂；按 ρ_n 分桶做子群分析
- Error analysis: 逐节点/逐样本的 margin 误差分解（系统项 vs 波动项）、Hoeffding 上界覆盖率、失效边界 B4 的残差分布

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / 548 GB 空闲；`C:\Users\xhf\miniconda3\envs\dyg-cold`
- Optional remote fallback, only if authorized: 用户本轮已授权「大规模实验上 novix-platform」；资源池 `exp-4090`；guidance 阶段不提交；不写任何端点或凭据
- GPU/CPU: 本机 1×3060 + 12 核；远端 GPU 未在本轮探测，NOT VERIFIED
- RAM: 本机技能探针未返回，NOT VERIFIED
- Disk: 548,335,472,640 B 空闲
- Max runtime per run: 本机 smoke ≤10 min（M0 实跑 <5 s）；远端单臂 ≤6 h
- Max total runs: 按 `matched-protocol.md` §6 分批，先第 0 批 PASCAL/TPP；5 seeds × 5 T × (8 基线 + 7 消融 + 1 主臂) × 4 数据集分组
- Frozen train/validation/test identifiers and validation-only selection policy: CIFAR 无官方 val → 固定 seed 从 train 切 45k/5k；test 只在最终评测用一次；用于选择的切分之后不得称 unseen
- Full search/trial ledger and held-out test isolation: 全部 trial 记 `config.json` + teacher/图文件 SHA-256 + seed 列表 + 环境快照；超参搜索预算 ≤ 每方法 12 组，且只在验证集上选择
- CCFA packet path and feasibility-contract.json: `ccfa-startup-packet/` 与 `ccfa-startup-packet/feasibility-contract.json`（哈希绑定 7 工件）
- Resource budget exhaustion and next-candidate decision rule: 命中 S1/S2/S5 → 回退 `needs-evidence` 或 `revise`；命中 S3/S4/H9 → 回退 `pivot-with-rescue-route`
- Scaling fallback: 本机只跑 smoke + 基线回归 + CIFAR 单 seed；全量 5 seeds + Tiny-ImageNet + 事件视觉转远端 4090；ViG 用公开权重做推理评估
- Stopping criteria: S1–S7 见 `matched-protocol.md` §8；`expected_strong` 在 G7 pilot 复现基线后锁定，锁前不得填绝对 headline gain

## Expected Results

- Minimum acceptable result: 在 ρ_n≠1 的 B2/B3 臂上，主臂相对最强 must-rerun 基线的 conversion loss 改善 ≥0.3pp 且方向在 ≥2/3 数据集一致；ρ≈1 的 B1 臂非劣效成立（±0.5pp）；PASCAL/TPP 第 0 批已复现；B4 失效边界按预测分裂。**全部为预注册目标，非实测**
- Strong result: 在 T≤4 且 ρ_n≠1 的臂上，主臂 conversion loss 比最强 must-rerun 基线低 ≥1.0pp（配对 bootstrap CI 下界 >0，BH q<0.05），且 ρ_n/T 趋势检验斜率显著为正、B1 非劣效、B3 图侧复现 ≤1.5pp、B4 残差显著非零。**该阈值须在 G7 pilot 复现基线后依据基线方差重新锁定，现在不是承诺数字**
- Failure signal: 恒等式残差超浮点容差；conversion loss 差距与 ρ_n/T 无单调关系；ρ≈1 的 CNN 臂上主臂反而"显著更好"（说明判据不具算子特异性）；与原版动态/非线性 ViG 上恒等式仍成立；与 PASCAL/TPP 在统一协议下等价
- What to do if minimum is not reached: 按 S4 停止方法迭代，保留全部负结果，把贡献收敛为「首个统一协议横评 + 实测失效边界」的 Q2 诊断型故事；不下调阈值、不挑 seed、不删负结果、不改写负结果
- Claim adjustment rule if expectations fail: 一旦单调性连续落 failure 或 G3 证明 T1 可一行照搬，立即删除「可归因于算子级统一的增益」这类因果措辞，只保留描述性结论；`observed_finding` 由 P5A/P6 依证据填写，不由 planned_claim 推定

## Figure/Table Decision Rules

Do not lock final figure/table contents before experiments are completed; define evidence-driven decision rules instead.

- Required first figure type: 方法定稿后生成一张框架/架构图（GPT 生成或程序绘制），展示固定线性算子类、被排除的动态/非线性算子、以及五条骨干臂的关系
- Required experiment visualizations if supported by data: 每数据集一张 conversion loss–T 曲线（含全部基线 + 主臂，带 95% CI 带）；ρ_n/T 趋势图（若趋势检验成立）；B4 失效边界的残差分布对比图；ρ_n 分桶子群图（若子群效应显著）
- Required result tables if supported by data: 主表（各方法 × T × 数据集的 conversion loss，含配对差值 CI 与 BH q）、消融表 A1–A7、理论—仿真一致性表（恒等式残差、上界覆盖率、Σs=n 命中率）、效率 proxy 表、数据集与 split 登记表
- Author or venue figure/table requirements, with source (if any): 具体 venue 官方当年页限/图表规则尚未核验（第三轮红队明确记录），确认前只按 venue-family 通用期望设计，不套用未核验规则
- Evidence that may benefit from a visual: ρ_n 系统项加权、ρ-不变相对误差、冻结/线性化的精度代价、动态 vs 固定算子的残差分裂
- Rules for excluding weak or misleading plots: 任何只显示单 seed 最好值、隐去 CI、隐去负结果、或把 proxy 画成能耗的图一律不进正文；若某曲线各方法重叠不可分辨，改为表格报告配对差值
- Scientific claims for which a figure/table would aid inspection (optional): 「适用类由算子类决定」这一主张由 B4 残差图与主表共同支撑，二者缺一不可
- Final count and placement are chosen after evidence stabilizes; no per-subsection quota applies.

## Traceability Checklist

| Requirement | Dataset | Baseline/method/ablation | Metric | Expected result | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|---|
| 恒等式与算子类刻画 | 合成算子 + CIFAR-10 激活 | 固定线性 A vs 动态 A_t vs max 聚合 | 恒等式浮点残差 | 固定类内 ~1e-15，类外显著非零 | 理论—仿真一致性表 + B4 残差图 | yes |
| ρ_n 加权系统项 | B2/B3 | A1（β=0）vs 主臂 | margin 平移 / conversion loss | 去 β* 后随 ρ 放大 | 消融表 + ρ_n 分桶图 | yes |
| ρ-不变相对误差 | B1/B2/B3 | A7 跨臂对照 | mean_relative_error / argmax 一致率 | 相对误差随 ρ 稳定 | 趋势图（若成立） | yes |
| 强基线横评 | CIFAR-10/100、Tiny-ImageNet | QCFS/FTBC/TPP/PASCAL/Parallel/DCGS/AdaFire | conversion loss | 预注册 minimum / strong，待 P4 裁定 | 主表 + loss–T 曲线 | yes |
| 第 0 批最近邻 | CIFAR-10/100 + Planetoid | PASCAL（自行复现）/ TPP（官方码） | conversion loss + 第二相条件方差 | 二者任一未复现即 S2 回退 | 主表 + 消融表 | yes |
| 确定性第二相 | 全部臂 | A3 Bernoulli vs 确定性 s[t] | Σs=n 命中率、条件方差、conversion loss | 零方差成立；精度增益待裁定 | 消融表 | yes |
| 解码冗余 | 全部臂 | A2 计数 vs 膜电位累加 | conversion loss | 若冗余则删组件 | 消融表 | yes |
| 失效边界 | B4 原版 ViG | A5/A6 动态图与 max 非线性 | 恒等式残差 / rate–ANN gap | 显著非零（M0 已给合成证据） | 残差分布图 | yes |
| 图侧通用性 | Cora/CiteSeer/PubMed | 同一算子 + 最强图转换基线 | conversion loss | 预注册 ≤1.5pp，待 P4 裁定 | 主表 | yes |
| 效率 proxy | 全部臂 | 全部方法 | SynOps / spike count / 峰值显存 | 只报 proxy，不声称能耗 | 效率表 | yes |
| 统计稳健性 | 全部数据集 | 5 seeds + bootstrap + BH | 配对差值 95% CI / q 值 | CI 与 q 完整报告 | 主表附注 | yes |
| 冻结/线性化代价 | B2 vs B4 | ANN teacher 精度对照 | top-1 差值 | 必须量化，不得隐瞒 | 主表附注 | yes |

## Citation Scope

**绑定政策**（`references/citation-requirements.md`）：`min_unique = 36`，`as_of = 2026`，`recent_window_years = 5`（**2022–2026 含端点**），`require_recent_majority = true`。取 5 年窗口的 field/topic rationale：QCFS（ICLR 2022）建立 clip-floor-shift 范式，此后全部低时延转换方法都在其之上，3 年窗口会把该分水岭与基础校准律排除。多数判定 `recent_count × 2 > total_distinct_count`。最终真实性、命题级支撑、去重与数量/年份算术由 `f-research-v1` 在 P12/P14 用 `citation_requirements.py` 复核；本节是 citation scope，不是已核验 bibliography。

- Must-cite foundational papers: Maass 1997（Neural Networks，脉冲神经元第三代）；Diehl et al. IJCNN 2015（weight/threshold balancing）；Rueckauer et al. Front Neurosci 2017（转换理论、soft reset 前身）；Sengupta et al. Front Neurosci 2019（SpikeNorm）；Han et al. CVPR 2020（RMP-SNN）；Deng & Gu ICLR 2021（`β*=θ/(2T)` 与逐层误差递归）；Kipf & Welling ICLR 2017（GCN）；Veličković et al. ICLR 2018（GAT）；Hamilton et al. NeurIPS 2017（GraphSAGE）；Yang et al. ICML 2016（Planetoid）；Krizhevsky 2009（CIFAR tech report）；Orchard et al. Front Neurosci 2015（N-MNIST）；Kugele et al. Front Neurosci 2020（非图像模态时序错位）；Neftci et al. IEEE SPM 2019（surrogate gradient）
- Must-cite recent papers: Bu et al. ICLR 2022（QCFS）；Liu et al. AAAI 2022（SpikeConverter）；Han et al. NeurIPS 2022（Vision GNN, arXiv:2206.00272）；Fang et al. Science Advances 2023（SpikingJelly）；Eshraghian et al. Proc IEEE 2023（SNN 训练综述）；Wu et al. ECCV 2024（FTBC, arXiv:2403.18388）；Bojković et al. PMLR v238 2024（转换的最优传输视角）；Dual-Phase, IEEE TNNLS 2024（膜电位解码 + 精确误差等式，卷期待 P12 核）；Hwang & Kung, IEEE TETC 2025 / arXiv:2403.08786（One-Spike SNN，跨 CNN+GCN）；Bojković, Wu, Gu, ICML 2025（TPP, arXiv:2502.14487）；Hao et al. ICML 2025（Parallel Conversion, arXiv:2412.13610）；Huang et al. ICML 2025（DCGS, arXiv:2503.00301）；Wang et al. AAAI 2025（AdaFire, arXiv:2311.14265）；Ramesh & Srinivasan, TMLR 2025（PASCAL, arXiv:2505.01730）；Yang et al. Neural Networks 2025（CS-QCFS, DOI 10.1016/j.neunet.2024.107076）；Liu et al. arXiv:2506.01968, 2025（ECL，venue 待核）；Jiang et al. NeurIPS 2025（Adaptive Fission）；SGNNBench, arXiv:2509.21342, 2025（同期大规模评测）；Li et al. Front Neurosci 2017（CIFAR10-DVS, DOI 10.3389/fnins.2017.00309）；Zhou, Chen, Datta, IEEE ICEdge 2025（低时延神经形态视觉）；熊志民等《控制理论与应用》2025（RMPE 微调）；Chen et al. arXiv:2608.13952, 2026（RMP-Alignment）；Ji et al. IEEE DLCV 2026（GTDL）；Xia et al. Neurocomputing 670:132604, 2026（负阈值 + BPTT 微调）
- Dataset papers: 上述 CIFAR tech report、Planetoid、Vision GNN、CIFAR10-DVS、N-MNIST、Tiny-ImageNet（CS231N 课程项目，无独立 dataset paper）；ViG 官方实现 `huawei-noah/Efficient-AI-Backbones`（Apache-2.0）
- Baseline papers: 见 `literature-baseline-matrix.md` 全表（6 个 must-rerun、3 个 adaptation-attempt、其余 literature-context）
- Search keywords: `ANN-to-SNN conversion error identity`；`row-stochastic operator calibration`；`low-latency spiking conversion`；`spiking vision GNN`；`frozen KNN graph message passing`；`deterministic two-phase spiking neuron`；`membrane potential readout`；`conversion loss benchmark`
- Target recency: 2022–2026 严格多数；保留必要奠基工作真实年份；不把访问年份当发表年份；预印本与其正式版不重复计数
- Excluded areas: 纯直训脉冲 GNN 的精度竞赛、神经形态硬件能耗实测、生物保真度建模、ImageNet-1K 全量 SOTA（G2 不可得）
- Reference scope/coverage appropriate to the question and venue: 覆盖转换误差理论、低时延转换方法、跨骨干转换、视觉图骨干、图学习基础、脉冲框架与数据集；目标期刊以理论严谨与可复算协议为主，不靠 leaderboard 规模取巧
- Recency expectation and its source; retain relevant foundational work: 来源为 `f-guidance-builder-v1/references/citation-requirements.md` 的绑定默认；奠基工作（2015–2021）保留但不得冒充近年工作
- 待 P12 核验项（**不得当成已确认条目**）: Deng & Gu ICLR 2021 的正式 DOI；Dual-Phase TNNLS 2024 的卷期页；Fang et al. Science Advances 2023 的 DOI；ECL 的正式 venue；Vision GNN 的 NeurIPS 2022 卷页；Li et al. CIFAR10-DVS 的作者列表；SGNNBench 的正式发表状态

## Novelty And Feasibility Summary

- Literature/baseline map verdict: **G0 pass** — 6 个官方码 must-rerun、3 个自行复现、2026 预印本仅关注；纠正 FTBC 全称与 QCFS venue/预印本年份两处题面错误
- Dataset access verdict: **G1 pass** — 5 组直链实测；ImageNet-1K / ImageNet-100 / DVS128 判 G2 并排除；CIFAR 与 Planetoid 许可状态标注 NOT VERIFIED
- Task/evaluation verdict: **G2 pass** — 主指标、次指标、proxy、5 seeds + bootstrap + BH、split 预注册成文
- Theoretical fit verdict: **G3 pass（带 H2 硬前置）** — 机制级 ρ 加权/ρ-不变；M0 实跑证据；κ_n 单调性、T1 非平凡性、‖A‖ 严格界、推论层检索须在 P4 前关闭
- Novelty verdict: **G4 pass-with-narrowing** — 数学组件全被占；剩余三处真空白；降档 IEEE TNNLS / Q1–Q2；三轮独立红队 2.5→3.2→3.4（1–5 尺度），第三轮 0 未解 fatal 并建议 `proceed`
- Hardware feasibility verdict: **G5 pass（带 G6 blocker）** — 3060 smoke 已实跑，全量转用户授权的 4090；`torchvision` 待补装
- Baseline/ablation verdict: **G6 pass（带执行前条件）** — 第 0 批 PASCAL/TPP 必跑 + S2 硬回退；A1–A7 七项消融
- Effectiveness plausibility verdict: **G7 pass（预注册，非实测）** — 三档目标全部标「预注册 / 非实测」，G7 pilot 后锁阈值；S1–S7 stop-and-return
- Q2+ story verdict: **G8 pass（收窄后）** — 中心问题、最强增量威胁、决定性实验、诚实风险与回退故事齐备

## Theoretical Feasibility Audit

- Mechanism expected to help: 误差经 `A(E₁W₂)` 线性传播；ρ_n 只加权系统项，相对误差由 `‖a_n‖₂‖DW‖₂/(TΔ_n)` 控制 → 可由算子类先验预测何时校准律失效
- Required assumptions: A 固定、非负、线性；亚阈值残差近似均匀独立；激活主要在 `[0,θ]`；所有方法同 teacher/θ/calibration/T
- Supporting literature: 成稿（`p7-draft.md`，**用户提供的未公开先验，不充当公开证据**）；Deng & Gu ICLR'21、QCFS/FTBC、Dual-Phase TNNLS'24、PASCAL TMLR'25、TPP ICML'25；M0 本机实跑 `evidence-snapshots/m0-results.json`
- Falsifying ablation: A1（去 β*）应使系统项随 ρ 放大；A5/A6 应使恒等式在动态/非线性算子上显著失效；A7 应显示 CNN 臂无非劣效以外的差异
- Critical failure mode: κ_n 单调性在真实训练网络上不成立，或 G3 证明 T1 可由 `A·1=ρ_n·1` + QCFS 零期望偏置一行照搬 → 理论贡献坍缩，按 H9 回退纯 benchmark 故事

## Story Strength Audit

- Why a top-journal reviewer should care: 视觉骨干从网格走向图/动态聚合，而转换误差理论仍隐含 ρ=1；给出可先验计算的适用边界与可复算协议，对社区有复用价值
- Strongest incrementality threat: One-Spike SNN（已跨 CNN+GCN）+ Dual-Phase（已有精确等式）+ PASCAL（已确定性计数）的组合；三轮独立红队一致指出组件层已被占满
- Decisive distinguishing experiment: 第 0 批 PASCAL/TPP 在同一冻结/线性化骨干、同 T/θ/calibration 下的横评 + ρ_n/T 单调趋势检验 + B4 失效边界残差；三者共同决定是"新判据"还是"已知结论的重述"
- Strong-paper result threshold: H7 约束下的预注册 strong（G7 pilot 后锁定），且必须同时满足 B1 非劣效、B3 图侧 ≤1.5pp、B4 边界分裂；缺一不可
- Honest fallback story if only partially successful: 收敛为「首个含全部最近邻基线的统一协议横评 + 实测失效边界」的 Q2 诊断型论文，保留全部负结果，不硬撑方法增益

## Constraints and Preferences

- Writing preference/source: 用户本轮指定 —— 实验设置与故事讲法用 `f-guidance-builder-v1`；做实验写文章用 `f-research-v1`；大规模实验用 `novix-platform`；小规模本机 3060 smoke
- Protected sections or edit scope/source: 已成稿的 GNN2SNN 论文（`auto-paper/20261028-171500/Spiking-GNN-Conversion/`）**本轮完全不动、不投稿、不改写**；资料库报告 `DNmhLQWbiipm5eE1efL8oW` 只读不修改
- Journal page/word/figure requirements and source: 具体 venue 官方当年规则**未核验**（第三轮红队记录）；确认前不套用任何页限/匿名/artifact 规则
- Things the workflow must do: 保留三轮独立红队原文与分数；遵守 H1–H9；`expected_strong` 全部标预注册；test 隔离；所有数值由脚本从结果文件生成；不删除负结果
- Things the workflow must avoid: 声称发明已被占的数学组件；声称精度 SOTA / 能耗实测 / 生物保真；把未发表内部先验当公开证据；把 G2 数据写成公开；把 proxy 写成能耗；挑 seed 或调参到显著
- Preferred writing language: 论文正文英文；内部研究与审计文档中文
- Preferred LaTeX/template/venue style: 待具体 venue 确认后由 `f-research-v1` P6 决定，当前不预设

## Citation policy and pending facts

按 `references/citation-requirements.md` 执行绑定默认 `min_unique=36`、严格近期多数、2022–2026 冻结窗口与独立数量/年份审计；按 `references/deferred-completion.md` 维护 `delivery-readiness.json` 与待办清单。当前 `workflow_complete` 与 `submission_ready` 分开记录：`submission_ready = false`（作者信息、投稿确认、代码发布安排、目标 venue 官方规则等均属作者管理的待决事实）。这些行政待决项不阻塞本地科学阶段；但任何科学证据、数据使用权、引用真实性与产物一致性仍是硬门。
