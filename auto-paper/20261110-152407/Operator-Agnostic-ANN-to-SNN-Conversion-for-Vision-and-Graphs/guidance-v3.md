# Research Guidance File · v3（用户授权验收口径修订版）

> 权威契约 v3，生成 2026-11-10。v1（`guidance.md`）与 v2（`guidance-v2.md`）及其全部证据、审计、负结果完整保留，不删除、不改写。
> 变更依据：用户 2026-11-10 明确授权「按证据定稿」—— 故事五条定位不变，把精度主张从「1.5pp 带」改为「双口径 ≥5× 能效约束下实测 conversion loss + 显式精度—能耗 Pareto 前沿」。
> 变更文件：`execution-contract-v2.md`、`contracts/precision-claim-authorization.md`、`audits/e17-final-confirmation.md`、`audits/e18-results-and-decision-point.md`。

## Title / Topic

- Working title: **Converting Graph Neural Networks for Graph-Structured Vision: Exact Error Identity, Membrane Readout, and an Accuracy–Energy Frontier on Superpixel Graphs**
- Target field: 类脑计算 / ANN→SNN 转换 × 图结构视觉分类
- Target venue: CVPR 主会档（官方 LaTeX author kit，双盲 `review` 模式，正文 ≤8 页，仅参考文献页不计入）
- Technique/method: 1028 成稿组合（精确误差恒等式、闭式偏置、膜电位解码、邻域错位/ρ_n 分析）+ 本轮修正（确定性两阶段下去除冗余 β*、margin 正则、窄网络训练、低 T 工作点、统一 fp64 前向）
- Selected scenario: 官方 SuperPixel MNIST / CIFAR10（PyG `GNNBenchmarkDataset`，SLIC 超像素为节点、8-NN 带权邻接，10 类图分类）
- Contribution framing: **组合与适配创新**。组件继承逐条写明，不声称发明单个组件；主张这套组合在自带图视觉数据集上的可分析性、相对全套转换方法的优势与能效边界。

## Core Idea

把 1028 为图节点分类建立的转换组合迁移到图级视觉分类：多张超像素图拼成块对角稀疏邻接 A 与线性全局池化 R，恒等式 `B̂−B = R A(E₁W₂)` 在 R 线性时精确成立。本轮发现确定性两阶段已精确实现发放率，再叠加 `β*=θ/(2T)` 构成双重校正，故主臂去掉该冗余项；并用 margin 正则与窄网络低 T 工作点把 45 nm 理论算术能耗比推过 5×，同时用统一 fp64 前向把恒等式残差验证到 1e-14。所有主张由本机 3060 实跑证据支撑。

### Mechanism-Level Rationale

- Domain bottleneck: 视觉转换方法与误差分析集中在 ρ≈1 的规则网格；图结构视觉表示的聚合算子及其能效缺少统一分析
- Why the chosen technique fits: R 为线性算子，误差恒等式可原样迁移；45 nm 口径下 MAC/AC 单操作比 5.11×，需把 spike 数压到 ANN MAC 量级以下才能取得能效优势
- What must be changed or adapted: 图级线性读出、块对角邻接、去冗余 β*、margin 正则、窄网络、低 T、fp64 校验
- Why this is more than applying method X to dataset Y: 新算子类 + 新任务类 + 组合内部机制重认定 + 全套转换方法统一横评 + ANN/能耗对照

## Paper Story

- Central scientific question: 一整套为图节点分类组合起来的 ANN→SNN 转换方法，能否迁移到自带图的视觉分类，并在保持转换保真的同时取得相对 ANN 的算术能效优势
- Intended reader and why the question matters: 类脑视觉与图学习交叉方向；图结构视觉骨干普及而转换理论仍隐含网格假设
- Domain/theory problem → design requirement → candidate method choice: 线性读出保恒等式 → 需算子级误差刻画 → 1028 组合 + 去冗余 + margin 正则 + 低 T 窄网络
- Expected contribution type: 方法组合在新算子类上的适配与理论分析 + 系统实证比较 + 精度—能耗 Pareto 前沿
- Opening problem: 低时延转换在规则网格上成熟，但图结构视觉表示与 ANN 能效对照缺少统一证据
- Why existing work is insufficient: 视觉转换方法各自为 CNN 校准；跨骨干工作缺算子级误差刻画；1028 只在引文图节点分类验证且未与转换方法横评、未比能耗
- Core insight: 只要读出线性，误差恒等式即精确成立；能效优势来自把脉冲总数压到 ANN MAC 量级以下，代价是 teacher 容量与转换保真，构成可量化的 Pareto 前沿
- What evidence should convince the reader: 20 个互不相交独立 seed 的能耗结果、横评领先、float64 恒等式残差、去 β* 与膜电位解码消融、显式精度—能耗权衡
- Planned claim (not an observed finding): 组合方法在图结构视觉上可同时给出精确误差分析与稳定能效优势
- Finding to assess after experiments (leave unresolved until evidence exists): 实测 conversion loss 与能效前沿由 E1–E18 证据固定，见 `results/e17/confirmation.json` 与 `results/e18/confirmation.json`
- Main claim: 在图结构视觉分类上，1028 转换组合经去冗余与低 T 适配后，可在双口径 ≥5× 理论算术能效比下保持可量化的转换保真，并优于全套单点转换方法
- Boundary of the claim: 覆盖固定非负线性超像素邻接与线性全局池化；能耗为 45 nm 理论操作计数估算而非硬件实测；teacher 绝对精度不是 SOTA；不含 ImageNet 级规模
- Skeptical-reviewer hook: 「只是把已知组件换个数据集」—— 用恒等式重新推导、组件冗余的实证发现、全套方法横评与 Pareto 前沿正面回答
- Strongest competing paper and why this is still distinct: One-Spike SNN（跨 CNN+GCN）与 Dual-Phase（精确等式 + 膜电位解码）；二者均未覆盖超像素图视觉分类的图级读出、全套转换方法统一横评与 ANN 能效对照

## Paper Outline

1. Introduction: 图结构视觉表示与低时延转换缺口；组合创新的继承边界；精度—时延—能耗三问
2. Related Work: 转换误差理论、低时延转换、跨骨干转换、超像素图视觉、能耗模型；逐条写明继承与差异
3. Method: 超像素图与块对角邻接、线性池化、精确误差恒等式、去冗余 β* 的机制分析、膜电位解码、确定性两阶段、margin 正则、45 nm 双口径能耗模型、适用条件
4. Experiments and Results: 数据与统一协议、全套转换方法横评、主结果（四组独立 holdout）、精度—能耗 Pareto 前沿、消融、恒等式数值验证、统计检验
5. Discussion: 组合内部重认定、精度—能耗权衡、理论能耗估算的边界、teacher 绝对精度、威胁到效度
6. Conclusion: 组合式图转换框架在图结构视觉上的可迁移性与能效前沿，给出可复算协议与后续硬件实测方向

## Experiment Plan

### Datasets

| Dataset | Direct access URL | License/terms | Task role | Size | Labels/targets | Split strategy | Access decision |
|---|---|---|---|---|---|---|---|
| SuperPixel MNIST | `https://data.pyg.org/datasets/benchmarking-gnns/MNIST_v2.zip` | 官方 benchmark 发布，无审批 | 主数据集一 | 192,378,381 B，55,000/5,000/10,000 图 | 10 类 | 官方 split，seeds 0–19 冻结抽样 | direct-public |
| SuperPixel CIFAR10 | `https://data.pyg.org/datasets/benchmarking-gnns/CIFAR10_v2.zip` | 官方 benchmark 发布，无审批 | 主数据集二 | 316,368,127 B，45,000/5,000/10,000 图 | 10 类 | 官方 split，seeds 0–19 冻结抽样 | direct-public |

### Baselines

- Simple baseline: 朴素 rate 转换（无偏置、无校准、计数解码）
- Matched internal baseline: 同一 teacher 下逐一关闭组件的消融臂
- Domain-standard baseline to rerun/adapt: ANN teacher（两层 GCN + 线性全局池化）
- Strong recent baseline to rerun/adapt: QCFS、FTBC、TPP、Parallel Conversion 逐一适配到超像素图消息传递层
- Strong recent baseline for literature context only: DCGS、AdaFire、PASCAL、CS-QCFS、One-Spike SNN
- Technique-family baseline: 直接训练的脉冲 GCN（替代梯度）
- Upper-bound or oracle-style comparison, if applicable: 冻结 ANN teacher top-1
- Strongest expected comparison: 全套单点转换方法在同一骨干、同 T/θ/split 下的 conversion loss

### Proposed Method Variants

- Main method: 去冗余 β* 的确定性两阶段 + 膜电位解码 + margin 正则 + 窄网络低 T 工作点 + fp64 校验
- Variant A: 带 β* 的原 1028 组合（用于量化双重校正的代价）
- Variant B: 计数解码替代膜电位解码（用于量化 1/T 网格与截断代价）
- Implementation notes: `vision_pipeline.py`、`run_e1.py` 至 `run_e18.py`；环境 `dyg-cold`，CUDA 12.8，torch 2.11.0

### Metrics

- Primary metric: 图级 top-1 与 conversion loss（pp，越低越好）
- Secondary metrics: 45 nm 理论算术能耗比（primary 事件驱动 AC 与 conservative A 传播 MAC 两套口径）、峰值显存、spike 数、恒等式残差
- Efficiency metrics: 全部标注为理论操作计数估算，非硬件实测焦耳数
- Statistical test / confidence reporting: 5 冻结 seeds 均值±std 与 95% CI；四组互不相交 holdout（seeds 0–4、5–9、10–14、15–19）；配对差值与 BH 在汇总脚本中计算

### Required Ablations

- Ablation 1: 去 β* 与带 β* 的配对比较
- Ablation 2: 计数解码与膜电位解码的配对比较
- Robustness or subgroup analysis: gauge 尺度、θ、T、keep 比例网格；窄网络与全宽网络对照
- Error analysis: float64 恒等式残差；fp32 累加误差来源定位；零脉冲与退化 teacher 的排除规则

### Runtime / Hardware Budget

- Local experiment machine and Conda environment: Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / `dyg-cold`
- Optional remote fallback, only if authorized: novix `exp-4090` 已授权但任务 `20049` 长时间 `queued / NO_ALLOCATION`，按用户 22:25 指令不再等待
- GPU/CPU: 本机单卡 3060；远端未分配
- RAM: 技能探针未返回，NOT VERIFIED
- Disk: 548,335,472,640 B 空闲
- Max runtime per run: 本机单 seed 全套约 165–530 s（视数据集）
- Max total runs: E1–E18 已完成，全部结果文件在 `results/`
- Frozen train/validation/test identifiers and validation-only selection policy: 工作点只在 val 多 seed 上筛选；四组 test holdout 互不相交，每组只用一次
- Full search/trial ledger and held-out test isolation: 全部 trial 记于 `results/*` 与 `experiment-traceability.md`
- CCFA packet path and feasibility-contract.json: `../ccfa-startup-packet/`、`contracts/strong-result-feasibility-lock.md`
- Resource budget exhaustion and next-candidate decision rule: 见 `audits/e18-results-and-decision-point.md`
- Scaling fallback: 增大训练规模（E18）已证伪并保留负结果
- Stopping criteria: 见 `contracts/strong-result-no-retreat.md`

## Expected Results

- Minimum acceptable result: 两组独立 holdout 上两套能耗口径 ≥5×、teacher 超过 2× chance、恒等式残差 <1e-10、横评领先 ≥1.0pp
- Strong result: 四组独立 holdout（20 个独立 seed）全部满足上述四项，且精度—能耗 Pareto 前沿可量化报告
- Failure signal: 零脉冲网络、teacher 退化到 chance、任一能耗口径低于 5×、恒等式残差超 1e-10
- What to do if minimum is not reached: 保留负结果并按修正回路改进；不挑 seed、不下调目标、不改已报告数值
- Claim adjustment rule if expectations fail: v3 由用户 2026-11-10 明确授权把精度主张改为「双 5× 能效约束下实测 conversion loss + 显式 Pareto 前沿」；该授权仅改变精度带的验收表述，不改故事五条定位、不改横评/能耗/恒等式三项已闭合目标
- 实测精度结果（用户授权口径）：CIFAR10 **1.57±0.67pp**（95% CI 下界 0.983pp，与 1.5pp 无显著差异）、MNIST **3.79±2.26pp**，来自 E17 全新 holdout；E18 增大规模结果 2.27/7.29pp 作为负结果与权衡证据一并报告。不得把 1.57 四舍五入表述为「达到 1.5pp 带」。

## Figure/Table Decision Rules

Do not lock final figure/table contents before experiments are completed; define evidence-driven decision rules instead.

- Required first figure type: 方法定稿后生成整体框架图，展示超像素图 → 块对角邻接 → 两层消息传递 → 线性池化 → 脉冲转换与 ANN/能耗对照
- Required experiment visualizations if supported by data: conversion loss–T 曲线（含 95% CI）、精度—能耗 Pareto 前沿散点、恒等式残差随 T 的变化
- Required result tables if supported by data: 主表（四组 holdout 的 top-1、conversion loss、两套能耗比、teacher）、横评表、消融表、恒等式与数值精度表
- Author or venue figure/table requirements, with source (if any): CVPR 2026/2027 官方模板双栏、图题小字号、正文 ≤8 页；官方指南见 `contracts/submission-constraints.md`
- Evidence that may benefit from a visual: 去 β* 的配对改善、膜电位解码贡献、能耗随 T 的单调关系、精度—能耗权衡
- Rules for excluding weak or misleading plots: 隐去 CI、只画单 seed 最好值、把理论估算画成硬件实测、或省略负结果的图一律不进正文
- Scientific claims for which a figure/table would aid inspection (optional): 「精度—能耗权衡」由 Pareto 图与主表共同支撑
- Final count and placement are chosen after evidence stabilizes; no per-subsection quota applies.

## Traceability Checklist

| Requirement | Dataset | Baseline/method/ablation | Metric | Expected result | Planned figure/table | Must appear in paper? |
|---|---|---|---|---|---|---|
| 恒等式精确成立 | MNIST/CIFAR10 | 固定线性 A+R vs 动态/非线性 | float64 残差 | <1e-10 | 理论—仿真一致性表 | yes |
| 全套转换方法横评 | 两数据集 | naive/QCFS/FTBC/TPP/Parallel/ours | conversion loss | 领先 ≥1.0pp | 横评表 | yes |
| 双口径能耗 ≥5× | 两数据集 × 四组 holdout | ANN teacher vs 主方法 | primary + conservative | 全部 seed ≥5× | 主表 + Pareto 图 | yes |
| 精度—能耗前沿 | 两数据集 | 工作点网格 | conversion loss 与能耗比 | 显式报告权衡 | Pareto 图 | yes |
| 去 β* 消融 | 两数据集 | 带 β* vs 去 β* | 配对差值 | 方向一致 | 消融表 | yes |
| 膜电位解码消融 | 两数据集 | 计数 vs 膜电位 | conversion loss | 膜电位显著更优 | 消融表 | yes |
| 统计稳健性 | 四组 holdout | 全部方法 | 5-seed 均值±std 与 CI | 完整报告 | 主表附注 | yes |

## Citation Scope

绑定政策沿用 `f-guidance-builder-v1/references/citation-requirements.md`：`min_unique=36`、`as_of=2026`、窗口 2022–2026 严格多数；最终真实性与数量/年份算术由 P12/P14 复核。

- Must-cite foundational papers: Maass 1997; Diehl et al. IJCNN 2015; Rueckauer et al. Front Neurosci 2017; Sengupta et al. Front Neurosci 2019; Han et al. CVPR 2020; Deng & Gu ICLR 2021; Kipf & Welling ICLR 2017; Achanta et al. IEEE TPAMI 2012; Knyazev et al. NeurIPS-W 2019; Horowitz IEEE ISSCC 2014
- Must-cite recent papers: Dwivedi et al. JMLR 2023 (Benchmarking GNNs); Bu et al. ICLR 2022 (QCFS); Han et al. NeurIPS 2022 (ViG); Fang et al. Science Advances 2023 (SpikingJelly); Wu et al. ECCV 2024 (FTBC); Bojković et al. ICML 2025 (TPP); Hao et al. ICML 2025 (Parallel Conversion); Huang et al. ICML 2025 (DCGS); Wang et al. AAAI 2025 (AdaFire); Ramesh & Srinivasan TMLR 2025 (PASCAL); Yang et al. Neural Networks 2025 (CS-QCFS); Jiang et al. NeurIPS 2025 (Adaptive Fission); SGNNBench arXiv 2025; Chen et al. arXiv 2026; Ji et al. IEEE DLCV 2026; Xia et al. Neurocomputing 2026
- Dataset papers: Benchmarking GNNs、SLIC、CIFAR tech report、MNIST、Planetoid
- Baseline papers: 见 `literature-baseline-matrix.md`
- Search keywords: `ANN-to-SNN conversion error identity`；`superpixel graph classification`；`spiking message passing`；`SynOps energy estimation`；`45nm MAC AC energy`
- Target recency: 2022–2026 严格多数；奠基工作保留真实年份；预印本与正式版不重复计数
- Excluded areas: 神经形态芯片实测焦耳数、生物保真建模、ImageNet-1K 全量 SOTA
- Recency expectation and its source; retain relevant foundational work: f 系列绑定默认；Horowitz 2014 等奠基工作保留但不冒充近年工作
- 待 P12 核验项: 部分卷期页与 DOI，以官方出版商页为准

## Novelty And Feasibility Summary

- Literature/baseline map verdict: pass —— 组件出处清楚，组合在图结构视觉分类与全套转换方法横评的组合未见报道
- Dataset access verdict: pass —— `data.pyg.org` 两个官方 zip 直链实测并完整落盘
- Task/evaluation verdict: pass —— 10 类图级分类，官方 split，四组互不相交 holdout
- Theoretical fit verdict: pass —— R 线性保证恒等式；45 nm 双口径能耗模型
- Novelty verdict: pass（组合与适配定位，不声称发明单个组件）
- Hardware feasibility verdict: pass —— 本机 3060 完成 E1–E18 全部实验
- Baseline/ablation feasibility verdict: pass —— 六方法横评 + 消融齐备
- Effectiveness plausibility verdict: pass —— 三项冻结目标在 20 个独立 seed 上闭合；精度带按用户授权改为实测 conversion loss + Pareto 前沿
- Q2+ story verdict: pass —— CVPR 主会档，组合创新 + 三重证据 + 显式权衡

## Theoretical Feasibility Audit

- Mechanism expected to help: 误差经 `R A(E₁W₂)` 线性传播；脉冲总数决定 45 nm 算术能耗比
- Required assumptions: A 固定非负线性、R 线性、亚阈值残差近似均匀独立、所有方法同 teacher/θ/split
- Supporting literature: 1028 成稿（未发表，仅方法出处）、Deng&Gu、QCFS/FTBC、Dual-Phase、TPP、Benchmarking GNNs、Horowitz 2014
- Falsifying ablation: 去 β*、计数解码、确定性第二相、非线性/动态算子
- Critical failure mode: teacher 退化到 chance 或零脉冲造成假达标（两者已由严格四条判定排除）

## Story Strength Audit

- Why a top-journal reviewer should care: 图结构视觉表示普及而转换理论仍隐含网格；组合方法给出可分析性与能效边界
- Strongest incrementality threat: One-Spike SNN 与 Dual-Phase 的组合
- Decisive distinguishing experiment: 全套转换方法统一横评 + 20 个独立 seed 的双口径能效 + float64 恒等式
- Strong-paper result threshold: 三项冻结目标闭合 + 精度—能耗前沿可量化报告
- Honest fallback story if only partially successful: 不适用；v3 由用户授权按证据定稿，不降级故事

## Constraints and Preferences

- Writing preference/source: 用户指定 `f-guidance-builder-v1` 定实验设置与故事、`f-research-v1` 做实验写文章、CVPR 官方模板、正文 ≤8 页、双栏英文、双盲
- Protected sections or edit scope/source: 1028 成稿目录只读；资料库报告只读；v1/v2 guidance 与全部证据只读
- Journal page/word/figure requirements and source: `contracts/submission-constraints.md`，CVPR 2026 Author Guidelines 与官方 author-kit 模板
- Things the workflow must do: 保留三轮独立红队原文、全部负结果与实现缺陷；所有数值由脚本从结果文件生成；不删除负结果
- Things the workflow must avoid: 声称发明单个组件；把理论能耗写成硬件实测；把 1.57pp 写成达到 1.5pp 带；挑 seed；把 val 结果冒充 test
- Preferred writing language: 论文正文英文；内部研究文档中文
- Preferred LaTeX/template/venue style: CVPR 官方 author-kit，`\usepackage[review]{cvpr}`，六节主结构

## Citation policy and pending facts

按 `deferred-completion.md` 维护 `delivery-readiness.json` 与作者管理待决清单；`workflow_complete` 与 `submission_ready` 分开记录，当前 `submission_ready=false`。v3 的用户授权仅涉及精度带验收表述，作者信息、Paper ID、OpenReview、compute reporting 表单仍属待决项。
