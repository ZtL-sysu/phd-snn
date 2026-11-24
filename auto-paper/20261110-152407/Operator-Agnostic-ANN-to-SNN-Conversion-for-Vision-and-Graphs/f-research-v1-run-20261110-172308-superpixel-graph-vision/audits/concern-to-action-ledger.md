# Concern → Action Ledger（P1B / 预实验）

> 来源：`audits/ccfa-pre-experiment-review.md`（独立 `ccf-idea-reviewer standard`，`**Overall:** 3.3`，recommendation `pivot-with-rescue-route`，**P1B 硬门裁决 `proceed` conditional、0 未解 fatal**）与 `audits/ccfa-pre-experiment-integrity.md`。
> 记录 `review_execution: independent-agent`（评审报告）/ `same-agent-role-pass`（本台账与完整性审计）。

| ID | 关切 | 分类 | 是否 fatal | 动作 | Owner | 关闭门 | 状态 |
|---|---|---|---|---|---|---|---|
| A0 | P1B 是否存在未解 fatal 阻止 P2/P3 | gate | 否（0 条） | 允许进 P2/P3，附 H1–H8 | 主会话 | P1B | 已关闭 |
| B1 | 能耗 AC/MAC 核算口径单一切换 | numeric-integrity | 准 fatal 级 | 远端同时报 `primary` 与 `conservative` 两套比值与 spike 密度；禁止挑口径凑 5×；标注理论估算 | novix 20049 / H1 | P3A | 在途 |
| B2 | ρ_n≈1 与「非行随机聚合」机制叙述错位 | mechanism / claim-scope | 准 fatal 级 | 远端加 `sym_norm=False` 原始带权邻接臂，报告 ρ 分布与 conversion loss；不把 ρ≈1 包装成 ρ≠1 | novix 20049 / H2 | P3A | 在途 |
| B3 | 恒等式残差 3.24e-05、teacher 68.8% | evidence / numeric-integrity | 准 fatal 级 | float64 重算 B/B̂ 报残差；teacher <70% 则提 epochs 到 1200 或 n_train 到 8000 | novix 20049 / H3 | P3A | 在途 |
| C1 | `ours_no_beta`/`ours_naive_if` 在 T=8 达 66.2% 高于完整 ours 60.2%（β* 与两阶段疑似冗余） | mechanism | 可修复 | 全量按 seed 报四项消融配对差值与 CI；保留负结果并给机制假设 | novix 20049 | P4/P5 | 在途 |
| C2 | 「一定有优势」预判与已落盘能耗反例信号并存 | claim-scope / 诚信 | 可修复 | 按可证伪假设裁定；任一不开优势则收窄为稀疏活动与 SynOps 代理 | 主会话 + 远端 | P5A | 在途 |
| C3 | 组合/推论层 novelty 未检索 | novelty | 可修复（置信度边界） | P12 前补一次组合层 prior-art 检索；论文定位保持「组合与适配创新」，不声称新数学结果 | P12 | P12 | 待办 |
| C4 | 单 seed 小子集 smoke 不足以支撑正式结论 | evidence | 可修复 | 全量 5 seeds ×2 数据集在 4090 跑；test 一次最终评测 | novix 20049 | P4/P5 | 在途 |
| C5 | CUDA 稀疏归约非确定 | numeric-integrity | 可修复 | 报 5-seed std 与 CI，不报单 seed 最好值 | 远端 + 汇总脚本 | P4 | 在途 |
| C6 | 官方 zip 下载/解析在远端可能失败 | data / compute | 可修复 | query 已写死 URL、字节数与重试；失败须落盘日志并如实报告，不得编造 | novix 20049 | P2 | 在途 |

## 停损规则

- `pivot-with-rescue-route` 是 idea 就绪度 recommendation，**不等于**阻止 P2/P3；P1B 硬门为 0 未解 fatal → `proceed` conditional。
- B1–B3 任一未闭合 → 不得把 P4 结果写进主表，回到 P2/P3 修复。
- P5 未达 `expected_strong` → 进入授权修正回路，禁止进 P6 写作。
- 任何诚信违规（挑 seed、删负结果、调口径凑目标、把理论能耗写成实测）→ S6 停止并回 `validation` 审计。
