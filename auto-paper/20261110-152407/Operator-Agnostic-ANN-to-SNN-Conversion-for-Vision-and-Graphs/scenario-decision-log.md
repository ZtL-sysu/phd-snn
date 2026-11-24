# Scenario Decision Log

> 生成 2026-11-10｜按 `f-guidance-builder-v1` 的 canonical 顺序：CCFA-startup → G0 → … → G8 → validation → handoff。
> 失败的候选保留其失败门，不推进；场景更换必须从 CCFA-startup 重跑。**本轮没有静默跳过任何门。**

## 1. 候选场景（用户给定：技术 = 我们的 ANN→SNN 转换算法；领域 = 视觉；任务 = 与别的转换算法对比）

| ID | 场景 | 数据集 | 机制理由 | 决定性风险 |
|---|---|---|---|---|
| S1 | 标准 CNN 视觉骨干上做全套转换方法横评 | CIFAR-10/100 | 基线齐、复现易、审稿人熟 | ρ≈1 上我们的 ρ 加权资产完全用不上；数学组件已被占；易读成 benchmark 表 |
| S2 | **固定线性算子类（冻结 KNN 图的线性化 ViG + GCN 消息传递）统一误差刻画 + 横评**，标准 CNN 作 ρ≈1 对照臂，原版动态/非线性 ViG 作失效边界 | CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS（可选）、Planetoid 三图 | ρ_n≠1 时系统误差按 ρ 加权、相对误差 ρ-不变；为行随机算子导出的校准律缺统一检验 | 冻结/线性化削弱 ViG 表征力；PASCAL/TPP 复现；novelty 窄 |
| S3 | 纯事件视觉时序转换 | CIFAR10-DVS / N-MNIST | 异步到达与时序错位直观 | 无官方 split、8.38 GB、与图/算子资产无关；R91 历史已证伪 degree 轴 |

## 2. 场景打分（G0–G4 硬门过后，1–5 加权，权重来自 `fail-fast-gates.md`）

| 准则 | 权重 | S1 | S2 | S3 |
|---|---:|---:|---:|---:|
| 数据集可达性与质量 | 5 | 5 | 5 | 3 |
| 理论契合 | 5 | 2 | 4 | 2 |
| 新颖性余量 | 5 | 1 | 3 | 2 |
| 实验可行性 | 4 | 5 | 4 | 3 |
| 基线/消融强度 | 4 | 5 | 5 | 3 |
| 当前研究热度 | 3 | 4 | 4 | 3 |
| 故事清晰度 | 5 | 2 | 4 | 2 |
| Q2+ 期刊契合 | 4 | 2 | 4 | 2 |
| **加权总分** | | **103** | **151** | **87** |

**选 S2**；S1 保留为 S2 内部的 ρ≈1 对照臂（B1），S3 降为可选稳健性臂（B5）。二者不独立成篇。

## 3. CCFA-startup：三轮独立评审与一次冲突治理

| 轮次 | 输入 | `**Overall:**`（1–5 / 1–10） | recommendation | 新增/未解 fatal | 处置 |
|---|---|---|---|---|---|
| 第 1 轮 | rev1 原始主张（"统一数据依赖邻域聚合" + Operator-Agnostic 命名） | 2.5 / 5.0 | `pivot-with-rescue-route` | F1 主张—适用条件错位、F2 novelty 重述/组合、F3 横评可比性两难 | 不进 G0；按最小可行修复路线做 problem-refinement |
| 第 2 轮 | `idea-cards-rev2.md`（收窄中心问题、降 venue、引入 T1/T2/κ_n） | 3.2 / 6.3 | `pivot-with-rescue-route` | F1 **已解决**；F2 降级为可修复（最重）；F3 降级为可修复。无 fatal gate 压顶，卡在 3.0–3.6 分数段 | 补 M0 实跑推导 + 成文 `matched-protocol.md` |
| 第 3 轮 | rev2 + M0 本机实跑 + `matched-protocol.md` + 成稿原文核对 | 3.4 / 6.8 | `pivot-with-rescue-route`（idea 就绪度） | **未解 fatal = 0**；F3 已解决、F2 部分解决；明确建议 `startup-decision = proceed (conditional)` + H1–H9 | 采纳 `proceed`，按 H1–H9 收紧 |

**冲突治理**：startup 包撰写员初版 `startup-decision.md` 在未整合红队结论时写了 `proceed`，依据不足。该初版**整体作废**并被终版 v3 取代（终版写明三轮分数、0 fatal 依据、H1–H9 与回退映射）。全过程见 `ccfa-startup-conflict-resolution.md`。**任何一轮评审原文均未修改、未抬分。**

**口径区分（关键）**：`ccf-idea-reviewer` 的 `pivot-with-rescue-route` 评的是 idea 当前就绪度；`f-guidance-builder-v1` 的 `proceed` 判的是能否进入 G0 做后续证据门。后者明文「low current-readiness score is not a rejection by itself」，进 G0 唯一硬标准是「无未解 fatal risk」。第三轮报告显式给出这个区分。

## 4. G0–G8 逐门记录（S2，canonical 顺序）

| 门 | 判定 | 关键证据 | 说明 |
|---|---|---|---|
| **G0** 近期文献与基线地图 | **pass** | `literature-baseline-matrix.md` | 6 个 2022–2025 官方码 must-rerun（QCFS/FTBC/TPP/Parallel/DCGS/AdaFire）；3 个 2025 adaptation-attempt（PASCAL/CS-QCFS/ECL）；2026 预印本仅关注。区分 direct-rerun 与 literature-only。**纠正两处题面**：FTBC 全称、QCFS venue/预印本年份 |
| **G1** 公开数据集 | **pass** | `dataset-access-log.md` | 5 组 G1 数据集/资产直链实测（含字节数）；ImageNet-1K / ImageNet-100 / DVS128 判 G2 并排除；N-MNIST 待补证。无任何需审批数据 |
| **G2** 任务与评估有效性 | **pass** | `matched-protocol.md` §4–§5 | 主指标 conversion loss（pp，越低越好）；5 冻结 seeds + 配对 bootstrap R=5000 + sign-flip 1000 + BH；CIFAR 无官方 val 已预注册切分；test 只用一次 |
| **G3** 理论契合与可行性证明 | **pass（带 H2 硬前置）** | `theoretical-feasibility-audit.md`、`evidence-snapshots/m0-results.json` | 机制级理由 = ρ_n 加权系统误差 + ρ-不变相对误差；M0 实跑恒等式残差 `9.88e-15`、Hoeffding 0 违反、P3 干净隔离 `0.3056→0.3111`/argmax 1.0、失效边界 `0.7058`/`1.1669`。**H2 待办**（κ_n 单调性、T1 非平凡性、‖A‖ 严格界、推论层检索）必须在 P4 前关闭，未过不得进主表 |
| **G4** 新颖性与非重复 | **pass-with-narrowing** | `literature-baseline-matrix.md` §4、`novelty-feasibility-report.md` | 7 条最近邻占满数学组件；剩余 3 处真空白；目标档位降为 IEEE TNNLS / Q1–Q2；**不声称发明 β*/零期望偏置/膜电位解码/确定性计数/两阶段/跨 CNN+GCN**。G0 若命中新近邻或 G3 证明 T1 可一行照搬 → 回退 pivot（H9） |
| **G5** 硬件与运行时 | **pass（带 G6 blocker）** | `hardware-profile.md` | 3060 12GB / CUDA 12.8 / torch 2.11 / 548 GB 空闲；本机 smoke 已实跑 M0；全量转用户授权的远端 4090；缩放策略明确。`torchvision` 缺失列为 G6 blocker |
| **G6** 强基线与消融 | **pass（带执行前条件）** | `matched-protocol.md` §6–§7 | 简单基线（朴素 rate 转换）、匹配内部对照（A1–A7 七项消融）、6 个官方码强基线、3 个自行复现基线；**第 0 批 PASCAL/TPP 必跑**且 S2 硬回退。QCFS 回归测试锁定统一 env |
| **G7** 有效性与强结果可信度 | **pass（预注册，非实测）** | `ccfa-startup-packet/strong-result-feasibility-contract.md` | `expected_strong` 一律「预注册目标 / 非实测」、G7 pilot 复现基线后锁阈值；有 M0 机制支撑、prototype M0–M4、5 seeds + bootstrap、S1–S7 stop-and-return。**本次视觉侧 0 正式实验，不产生任何结果数值** |
| **G8** 目标档位故事强度 | **pass（收窄后）** | `story-strength-audit.md` | 中心问题为「ρ_n≠1 时行随机校准律是否仍最优」；最强 incrementality 威胁 = One-Spike SNN + Dual-Phase + PASCAL；决定性实验 = 第 0 批 PASCAL/TPP 同协议横评 + ρ_n/T 单调性 + B4 失效边界。诚实风险与 Q1–Q2 增量定位已写明 |

## 5. 失败与被拒路径（全部保留）

- S1 独立成篇：G4/G8 弱（novelty 低、纯 benchmark 表）→ 不推进，降为 S2 的 B1 对照臂。
- S3 独立成篇：G1 条件性 + G3 弱 → 不推进，降为可选 B5 稳健性臂。
- rev1 原始主张：CCFA-startup 第 1 轮 `blocked`（3 条 fatal）→ 不进 G0，全部保留为决策记录。
- ImageNet-1K / ImageNet-100 / DVS128 Gesture：G1 硬门失败 → 明确排除，不用任何"申请后可用"的措辞。
- 无「跳过」状态的门；每次 revisit 均从更早门重新核验（见第 3 节三轮评审）。

## 6. 场景总分与选择

S2 加权 151 > S1 103 > S3 87，且 S2 的 G1–G4 全部硬门通过。**选定 S2**。主风险 = novelty 窄 + 冻结/线性化的表征代价；回退 = 第 0 批 PASCAL/TPP 复现失败转 `needs-evidence`，或单调判据连续 failure / G0 命中近邻 / G3 证明 T1 平凡 → `pivot-with-rescue-route`（收敛为纯 benchmark + 失效边界故事）。
