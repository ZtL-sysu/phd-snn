# 用户授权记录 · 精度带验收口径修订（v2 → v3）

> 时间：2026-11-10｜授权方式：会话中明确选择「按证据定稿（需你授权口径）」。
> 本文件是版本化契约变更的授权凭证，必须由 `guidance-v2.md` / `guidance-v3.md` / `execution-contract-v2.md` 共同引用。

## 1. 授权原文与选择

用户在本轮被问及「E1–E18 后四项冻结目标 3 PASS / 1 未达（MNIST 精度带），接下来怎么走」时，明确选择：

> **按证据定稿（需你授权口径）** —— 故事五条定位不变，把精度主张从「1.5pp 带」改为「双 5× 能效约束下实测 CIFAR10 1.57pp / MNIST 3.79pp 转换损失 + 显式精度—能耗 Pareto 前沿」，授权后立刻进 P6–P21 的 CVPR 写作排版链。

## 2. 授权范围（精确边界）

| 项 | 是否变更 | 说明 |
|---|---|---|
| 故事五条定位 | **不变** | 方法核心、自带图视觉数据集、全套转换横评、三重证据、目标档位均不动 |
| 横评目标（T≤4 领先 ≥1.0pp） | **不变** | 已 PASS |
| 能耗目标（带内双口径 ≥5×） | **不变** | 已 PASS |
| 恒等式目标（<1e-10） | **不变** | 已 PASS |
| 精度带验收表述 | **变更（本次授权）** | 从「1.5pp 带达标」改为「在双 5× 能效约束下实测 conversion loss 并显式报告精度—能耗 Pareto 前沿」 |
| 目标档位与模板 | **不变** | CVPR 主会档、官方模板、双盲、正文 ≤8 页 |
| `expected_strong` 数值 | **不下调、不删除** | v2 的 1.5pp 作为历史目标保留；v3 记录实测与授权后的表述，不改写历史结果 |

## 3. 明确禁止（授权不覆盖）

- 不把 CIFAR10 的 **1.57pp** 四舍五入或表述为「达到 1.5pp 带」；
- 不把 MNIST 的 3.79pp（E17）与 E18 的 7.29pp 隐藏或择优呈现 —— E18 是「增大训练规模」假设被证伪的负结果，须一并报告；
- 不把 val-only 结果冒充 test 结果；
- 不把 45 nm 理论算术能耗估算写成硬件实测；
- 不删除零脉冲假优势、退化 teacher 假达标、fp32/fp64 混算等负结果与实现缺陷；
- 不自动投稿、commit、push 或填写作者/Paper ID 等待决项。

## 4. 证据依据（授权时已呈交用户）

- `audits/e17-final-confirmation.md`：四组独立 holdout 中第三组（seeds 10–14）的 5-seed 结果，三项 PASS、精度带 1.57 / 3.79pp。
- `audits/e18-results-and-decision-point.md`：E1–E18 全项目总账、三个可选方向、P5 blocked 状态。
- `results/e17/confirmation.json`、`results/e18/confirmation.json`：逐 seed 原始数值。

## 5. 流水线影响

按 `f-research-v1` 的 Autonomous Correction Loop 与 `research-recovery.md`：

1. 本次为**版本化契约变更** → 新建 `guidance-v3.md` 与 `execution-contract-v2.md`；v2 契约与其 gate 记录标记为 `superseded`（原文保留）。
2. canonical 顺序从 **P0 重新起算**，逐门 `--before` 校验；未受影响的实验证据（E1–E18 的全部结果文件）在核对数据/split/seed/环境/门准则后复用，不重跑昂贵实验。
3. P3A / P4 / P5 / P5A 依 v3 验收口径重新接受；P5 通过后进入 **P6–P21** 写作、引用、TeX、编译与交付链。
4. 所有复用证据须在 `guidance-pipeline-state` 与 `paper-guidance-audit.md` 中登记适用性核对结论。
