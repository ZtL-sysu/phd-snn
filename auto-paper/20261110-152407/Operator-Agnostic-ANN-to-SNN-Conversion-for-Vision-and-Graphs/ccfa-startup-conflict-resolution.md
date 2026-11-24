# CCFA Startup 冲突治理记录

> 生成 2026-11-10｜本文件如实记录本轮出现的**决策冲突、事实分歧与修订**，不删除任何历史证据，不静默改写结论。

## 1. 冲突一：`startup-decision.md` 初版 vs 独立红队

| 项 | 内容 |
|---|---|
| 初版 | startup 包撰写员 Agent 在**未整合独立红队结论**时写了 `proceed`（性质标注 conditional proceed / proceed-with-narrowing），依据列了 G4、数据、基线、资源、C1–C5 可证伪等 6 条 |
| 同期独立红队 | 第 1 轮 `ccf-idea-reviewer standard`：**`**Overall:** 2.5`/5（=5.0/10），recommendation `pivot-with-rescue-route`**，三条 fatal（F1 主张—适用条件错位、F2 novelty 重述/组合、F3 横评可比性两难） |
| 规则 | `f-guidance-builder-v1`：「Only `proceed` may enter G0. A low current-readiness score is not a rejection by itself, but **an unaddressed fatal risk** ... is a block」；且「Use the named CCFA skills for their owning responsibilities; do not replace their output with a generic internal summary」 |
| 判定 | 初版 `proceed` **依据不足，不能静默生效**；三条 fatal 未解 → 该场景当时不得进 G0 |
| 处置 | 初版**整体作废**，由 `startup-decision.md` 终版 v3 取代；终版写明三轮分数、0 fatal 依据、H1–H9 硬条件与回退映射。**三轮评审原文一字未改、未抬分** |

## 2. 冲突二：资料库报告声称的既有产物 vs 本地实况

| 项 | 内容 |
|---|---|
| 资料库报告 | `DNmhLQWbiipm5eE1efL8oW` 称 `auto-paper/20261110-145235/Deterministic-Two-Phase-ANN-to-SNN-Conversion/` 下 v3 guidance 20 文件、`--strict --packet` valid、12 门全 passed、`--complete` PASS |
| 本地实测 | `auto-paper/` 下只有 `20261028-171500`、`20261104-060416`、`20261105-111502`、`20261105-204552`、`20261107-141018`、`20261107-154000` 六个目录；`20261110-145235` **不存在**；`**/*DTP*`、`**/*R91*`、`**/goal-ledger.md` 均无命中 |
| 环境反证 | 报告写「本机 conda MPS」，本机实查为 Windows 11 + RTX 3060 + CUDA 12.8；报告提到 `data_batch_1` 缺失等也是另一套环境 |
| 判定 | 该报告属**另一会话/另一台机器**的记录，只作参考材料（前作地图、基线清单、DTP 思路、已证伪的 degree 轴）；其「已通过校验」的结论**不作为本地事实** |
| 处置 | 本轮从零按 `f-guidance-builder-v1` 生成完整 guidance 包；报告只读快照落 `_library_gnn2snn_vision_report.txt`，资料库节点未修改 |

## 3. 冲突三：三轮独立红队 recommendation 始终为 `pivot`，但最终 `startup-decision = proceed`

| 轮次 | `**Overall:**` | recommendation | 变化 |
|---|---|---|---|
| 第 1 轮 | 2.5 / 5（5.0/10） | `pivot-with-rescue-route` | 3 条 fatal |
| 第 2 轮 | 3.2 / 5（6.3/10） | `pivot-with-rescue-route` | F1 已解；F2/F3 降级为可修复；分数段 3.0–3.6 |
| 第 3 轮 | 3.4 / 5（6.8/10） | `pivot-with-rescue-route`（idea 就绪度） | **未解 fatal = 0**；明确建议 `startup-decision = proceed (conditional)` + H1–H9 |

**为什么不矛盾**：`ccf-idea-reviewer` 评的是 **idea 当前就绪度与录用潜力**；`f-guidance-builder-v1` 判的是**是否允许进入 G0 做 evidence-first 的后续闸门**。后者明文「low current-readiness score is not a rejection by itself」，进 G0 的唯一硬标准是「无未解 fatal risk」。第三轮报告自己给出了这个区分、`proceed` 建议值与 H1–H9。

**我们做了什么让 0 fatal 成立**（不是靠改口径）：
1. problem-refinement 消除 F1：中心问题收窄到「ρ_n≠1 的固定线性算子上校准律是否最优」，禁用 "Operator-Agnostic" 命名，原版动态/非线性 ViG 明写为失效边界；
2. 补 M0 本机实跑：恒等式 25 格残差 `9.88e-15`、Hoeffding 0 违反、P3 干净隔离 `0.3056→0.3111` / argmax 1.0、失效边界 `0.7058` / `1.1669`；
3. 成文 `matched-protocol.md` 冻结版 v1：所有基线同骨干/同 teacher/同 T/同 θ/同 calibration/同 conversion loss，第 0 批 PASCAL/TPP 必跑 + S2 硬回退；
4. 把成稿真实路径交给第 3 轮评审核对（第 2 轮因未获路径而误判「无对应成稿」，已澄清）。

## 4. 第三轮红队指出的两处数值/口径问题（已实际修正）

| 问题 | 修正 | 结果 |
|---|---|---|
| M0 的 P3 每个 ρ 重新采样 problem，无法干净检验 ρ-不变（相对误差 0.2591–0.5648 波动、argmax 0.828–1.0） | 改为**同一份 problem，只把行和为 1 的 A0 整体乘 ρ**，使 ρ 成为唯一变量 | 重跑后 `0.3056 / 0.3085 / 0.3099 / 0.3108 / 0.3111`，argmax 全 `1.0`；并写明读法约束（合成算子的整体缩放 ≠ 真实聚合算子的 ρ 变化，须 G3 重做） |
| SHA 用的是内存字符串哈希，与 Windows CRLF 磁盘字节不一致 | 权威口径改为**磁盘字节 SHA-256**，内存规范化哈希仅备查 | 结果 JSON 权威哈希 `ea4c05a67300766ed9141bb0f1e99b2407760321f32ab95dcdb6c25e5ec7575f` |
| 任务描述曾把 P4 检查对数写成 3840 | 以结果文件为准：5 个 T × 384 对 = **1920 对** | 已在 `startup-decision.md` H8 记录 |
| P6 数值因随机数消耗顺序改变而变化 | 以修正后重跑的文件为准 | 动态 A_t `0.7058297672203355`、max gap `1.1668779395601996`（旧值 0.7476 / 1.1051 作废，未混用） |

## 5. 未采纳/未掩盖的结论

- **不把红队 `pivot` 写成 accept**：三轮 recommendation 与分数原样保留在 `ccfa-startup-packet/`。
- **不声称 novelty 已站稳**：第三轮明确 T1/T2/κ_n「介于重述与新推论之间，更靠近已知结论的假设放宽推论，**不构成 prior-art 无法得到的新数学结果**」；全文按 H7 不写「新数学结果」。
- **不把未发表成稿当公开证据**：H1 要求全程标注「用户提供的未公开先验（未发表、不充当公开证据）」，仅作机制/命题出处核对。
- **不把零实验包装成结果**：所有 `expected_strong` 标「预注册目标 / 非实测」，视觉侧 0 正式实验。
- **不静默改契约**：rev1 → rev2 是 repair，从 CCFA-startup 重新起算；`matched-protocol.md` 后续若升 v2 须记 `reopen`（H4）。

## 6. 保留的回退路径

G0 命中新近邻 / G3 证明 T1 可一行照搬 / G7 单调性连续落 failure / 第 0 批横评与 PASCAL·TPP 等价 → 立即回退 `pivot-with-rescue-route`，收敛为「统一协议横评 + 实测失效边界」的 Q2 诊断型故事（H9、S3、S4）。全部负结果保留。
