# P1B · Pre-Experiment Claim Integrity Audit

> 模式：`ccf-integrity-auditor` claim-audit 语义；**所有声明一律标记为 planned evidence，不是 reported evidence**。
> 审计对象：`../guidance-v2.md`、`contracts/claim-evidence-matrix-v2.md`、`contracts/strong-result-feasibility-lock.md`、`contracts/guidance-validation.md`、`novix/query-header.md`。

## 1. planned vs reported 扫描

| 位置 | 声明 | 标记 | 判定 |
|---|---|---|---|
| `guidance-v2.md` §Expected Results | minimum / strong / failure 三档 | 全部写「预注册目标 / 非实测」 | ✅ planned |
| `guidance-v2.md` §Paper Story | `Finding to assess after experiments (leave unresolved until evidence exists)` | 明确留空 | ✅ planned |
| `guidance-v2.md` 能耗假设 | 「用户预判一定有优势」→ 写成带 failure 的可证伪假设 | 明确「理论算术能耗估算，非硬件实测」 | ✅ planned，且未预设结论 |
| `claim-evidence-matrix-v2.md` | 结果栏全部「待 P4」 | 无数值 | ✅ planned |
| `strong-result-feasibility-lock.md` | 5/5 claims pass | 指**可行性路径** pass，不是结果达标 | ✅ 需与 P5 区分，已注明 |
| `novix/query-header.md` §5 | 本机 smoke 数值（ANN 68.8%、能耗比 1.605→0.277 等） | 明确标注「预实验 smoke 数值，不是正式结果，不得写进 result.json 冒充全量」 | ✅ 隔离 |
| `results/*.json` | 单 seed、小子集、本机 CUDA 的 smoke | 文件名带 `smoke`/`gpu` 标签；台账标注非正式结果 | ✅ 隔离 |
| `audits/ccfa-pre-experiment-review.md` | 3.3/5、`pivot-with-rescue-route`、0 未解 fatal | 独立评审原文，未抬分未删除 | ✅ 历史证据 |

**未发现**把 planned claim 写成 reported finding、把 smoke 冒充全量、把理论能耗写成硬件实测、或把用户预判写成已得结论的情况。

## 2. 数字与出处一致性

- 两个官方 zip 字节数（192,378,381 / 316,368,127）在 `execution-contract-v1.md`、`novix/query-header.md`、`in-flight-task.md` 一致，且与本机 `ls -l` 实测一致。
- 45 nm 能耗常数（MAC 4.6 pJ / AC 0.9 pJ）在 `vision_pipeline.py`、`guidance-v2.md`、`query-header.md` 一致；均标注为理论估算。
- 组件继承出处（Deng&Gu、QCFS/FTBC、Dual-Phase、TPP、PASCAL、One-Spike SNN）在各处一致，无「发明单个组件」的措辞。
- 1028 成稿全程标注「用户提供的未公开先验（未发表、不充当公开证据）」。

## 3. 口径风险（P1B 独立评审的准 fatal 条件，已转为入口条件）

| ID | 风险 | 处置 | Owner |
|---|---|---|---|
| B1 | 能耗 AC/MAC 口径单一切换可能自洽性不足 | 远端同时报 primary 与 conservative 两套，禁止只挑有利口径 | novix 20049 / H1 |
| B2 | 对称归一化下 ρ_mean≈0.9987 与「非行随机瓶颈」叙述错位 | 远端加 `sym_norm=False` 原始带权臂并报告 ρ 分布 | novix 20049 / H2 |
| B3 | 恒等式残差 3.24e-05 未达浮点精度、teacher 68.8% 偏低 | float64 重算；teacher 门槛 ≥70%，否则加 epochs/数据 | novix 20049 / H3 |

## 4. Gate verdict

**P1B integrity pass（planned-evidence 审计）**：无 claim/结果混淆、无编造数值、无口径隐瞒。三项准 fatal 条件已写入 `audits/concern-to-action-ledger.md` 并成为远端任务的 H1–H3 硬要求；在进入 P3A/P4 主表前必须闭合。
