# Strong-Result No-Retreat Policy（用户 2026-11-10 18:42 指令固化）

> 用户原话：「好，你就盯着 novix 的吧，目标肯定是冲强结果的，我们目前的故事不能再退」。
> 本文件是 `execution-contract-v1.md` 的**补充约束**（不改变契约版本，因为不新增资源、数据、方法族或权限，只是收紧目标策略）；与 `guidance-v2.md` 的 `expected_strong` 一致，且优先级高于 v2 里预留的「honest fallback 低档故事」表述。

## 1. 故事冻结（不可退让的定位）

以下五条构成本篇的**冻结定位**，任何后续阶段（P5/P5A/P9/P10/P19 的评审与修订）都不得改写、收窄或降级：

1. **方法核心**：完整沿用 1028 成稿那套 GNN→SNN 转换组合（精确误差恒等式、闭式偏置 `β*=θ/(2T)`、膜电位解码、邻域时序错位/ρ_n 加权分析），**组合与适配创新**是主张，组件继承逐条写明但不声称发明单个组件。
2. **场景**：自带图结构的视觉数据集（官方 SuperPixel MNIST / CIFAR10），图级 10 类视觉分类；不退回纯 CNN 网格、不换成非视觉数据集。
3. **对比对象**：全套 ANN→SNN 转换方法（naive / QCFS / FTBC / TPP / Parallel / ours）在同一超像素图骨干、同一 teacher、同一 T/θ/split 下的横评，外加直训 SNN 与 ANN teacher 上限。
4. **三重证据**：精度（conversion loss）、时延（T 网格）、与 ANN 的**理论算术能耗对照**，三者缺一不可。
5. **目标档位**：Q1–Q2 类脑与神经网络期刊（IEEE TNNLS / Neural Networks 档）。

**明确作废**：`guidance-v2.md` §Story Strength Audit 中「honest fallback story if only partially successful → 收敛为纯 benchmark / 诊断型论文」以及 novelty-feasibility-report、v1 三轮红队里任何「回退为统一横评 + 失效边界」的降级路线。这些文字保留作为历史记录，但**不再是可执行选项**。

## 2. 强结果目标冻结（不得下调）

`guidance-v2.md` §Expected Results 的 `expected_strong` 为绑定目标，冻结为：

| 维度 | 目标 |
|---|---|
| 精度 | 两数据集 T≤8 达 **ANN−1.5pp 带内**；T≤4 相对最强单点转换基线 conversion loss 低 **≥1.0pp**（配对 bootstrap CI 下界 >0、BH q<0.05） |
| 能耗 | 与 ANN 的理论算术能耗比 **≥5×** |
| 理论 | 恒等式残差在浮点精度内（float64 后 <1e-10），ρ_n 加权判据成立 |
| 消融 | 逐组件方向一致、负结果如实报告 |

**禁止**：因首次尝试未达标而下调阈值、把 5× 改成 1.6×、把 1.5pp 放宽到 2.0pp、挑 seed、删负结果、调能耗口径凑数、把理论估算写成硬件实测。

## 3. 唯一允许的「冲强结果」路径：改进，不是退让

按 `f-research-v1` 的 Autonomous Correction Loop 与 `research-recovery.md`，P5 未达标时**必须**先走以下改进并重跑，且不得改故事或目标：

| 序 | 改进轴 | 具体动作 | 位置 |
|---|---|---|---|
| 1 | 数据/实现对齐 | 检查 split、特征、gauge、阈值尺度、池化线性；修实现 bug | 本机 3060 秒级验证 |
| 2 | teacher 质量 | 加 epochs / 训练图 / hidden / 更好的初始化与 lr schedule，把 test acc 从 68.8% 往上推 | 本机 + 4090 |
| 3 | **β* 与两阶段冗余（3-seed 已证实）** | `audits/strengthen-candidate-report.md`：所有 `no_beta` 组合 conversion loss 2–3pp，对应 `beta_star` 为 10–25pp；确定性两阶段已精确实现发放率，β* 构成双重校正。主臂改为 `beta=0`，`beta_star` 保留为显式消融臂。这属于**组合内部重认定**，不是换方法族、不是退故事 | 本机已验证；改进臂待 `20049` 终态后派发 |
| 4 | **低 T 精度** | 目前 ours 只在 T=16 接近 ANN，T≤4 差距大：改进量化/偏置/解码使 T≤4 进 1.5pp 带 | 本机 + 4090 |
| 5 | **稀疏化换能耗** | 用 1028 的 sparsity penalty / 激活正则降低 spike 密度，使 ANN/SNN 理论能耗比在低 T 与 T≤8 都站上 5×；同时用 primary 与 conservative 两套口径如实报告 | 本机 + 4090 |
| 6 | 加强基线与消融 | 补 PASCAL/CS-QCFS/ECL 自行复现、补 ρ≠1 的 raw 带权算子臂、补统计检验 | 4090 |
| 7 | 规模与算力 | 全量 5 seeds 在 `exp-4090`；必要时追加轮次（须记录 trial ledger） | novix |

**每条改进都必须记录**：触发条件、证据、改动变量、证伪条件、预测成本、剩余预算；保留前一次失败证据。

## 4. 诚信红线（冲强结果不等于凑结果）

- 结果只能由实跑产生；`observed_finding` 不早于 P5A。
- 「一定有优势」是**待裁定的预判**，不是已得结论；当前 smoke 只在 T≤2 有 1.3–1.6× 优势，必须靠方法改进把优势扩到 T≤8 并达 5×，而不是改口径或改目标。
- 负结果（β* 冗余、能耗反转、恒等式残差 1e-5 量级）全部保留并解释，用于指导改进；不得删除以美化主表。
- 理论能耗明确标注「45 nm 算术能耗估算，非硬件实测」。
- 1028 成稿为未发表内部成果，只作方法出处与 baseline-calibrated 锚点。

## 5. 与 `f-research-v1` 门禁的关系

- 本政策**收紧**了 P5 的通过条件（目标不变、允许改进不允许退让），**没有**放宽任何 gate。
- P5 未达 `expected_strong` → 回到 P2/P4 按第 3 节改进重跑，**不得进 P6 写作**。
- 若穷尽改进与预算仍无法达标，须向用户报告具体缺口与剩余选项；**不得**自动降级故事或自动下调阈值。只有用户明确授权才能版本化变更契约。
- P1B/P3A/P5A 的独立评审若给 `pivot-with-rescue-route`，按本政策只允许「改进型 rescue」，不允许「改定位/降档型 rescue」。

## 6. 当前在途状态

novix task **`20049`**（`exp-4090`）：主 API `processing/steps 0`；带外 `placement.state=queued`、`diagnosis=NO_ALLOCATION`、`eligible_nodes=2`、`dispatch_paused=false`、`backend.status=processing`、工作区尚未创建 → **排队等 sandbox，未失败**。带外建议「不要重复提交」，故不重提、不换题、不并行提交同 idea 任务。
