# startup-decision.md（终版 v3）

> CCFA-startup 阶段 gate decision｜生成 2026-11-10
> 本文件**取代**本轮早先由 startup 包撰写员生成的同名初版（初版在未整合独立红队结论时写了 `proceed`，依据不足，已整体作废并保留于 `ccfa-startup-conflict-resolution.md` 记录中）。
> 取值集合：`proceed` / `revise` / `pivot-with-rescue-route` / `needs-evidence`（只取其一）。

## Decision

# `proceed`

性质：**conditional proceed / proceed-with-narrowing**。必须附带 §3 全部硬条件 H1–H9；任一条件被违反即回退，见 §4。

## 1. 决策依据（只采信可核查的落盘证据）

| # | 依据 | 来源 |
|---|---|---|
| 1 | 三轮独立 `ccf-idea-reviewer standard` 评审分数依次为 **2.5 / 3.2 / 3.4**（1–5 尺度，即 5.0 / 6.3 / 6.8 于 1–10 尺度）；recommendation 三次均为 `pivot-with-rescue-route`，**未抬分** | `idea-red-team-review.md`、`-rev2.md`、`-rev3.md` |
| 2 | 第三轮明确判定 **未解 fatal risk = 0 条**：F1 已解决、F3 已解决、F2 部分解决且**不构成 fatal**；五条数值 fatal gate 全不触发 | `idea-red-team-review-rev3.md` |
| 3 | 第三轮明确给出 `startup-decision` 建议值 **`proceed`（conditional）**，并说明 `f-guidance-builder-v1` 与 `ccf-idea-reviewer` 是两个体系：低就绪度按前者明文「is not a rejection by itself」，进 G0 的唯一硬标准是「无未解 fatal risk」 | 同上 |
| 4 | 四判据全部满足：0 fatal；机制有本机实跑可跑路径（M0）；第 0 批最近邻基线 PASCAL/TPP 有复现路径且 S2 硬回退；evidence plan 可信（`matched-protocol.md` 冻结版 v1 真实存在） | `matched-protocol.md`、`evidence-snapshots/m0-results.json` |
| 5 | M0 本机实跑（**修正后重跑版**，磁盘字节 SHA-256 `ea4c05a67300766ed9141bb0f1e99b2407760321f32ab95dcdb6c25e5ec7575f`）：恒等式 25 格最大残差 `9.880984919163893e-15`；Hoeffding 上界 0 违反；动态 A_t 残差 `0.7058297672203355`、max 非线性 gap `1.1668779395601996` 显著非零（失效边界成立）；P3 干净隔离后相对误差 ρ=0.5→10 为 `0.3056→0.3111`、argmax 一致率全 1.0 | `protocols/m0_operator_theory_check.py` + `evidence-snapshots/m0-results.json` |
| 6 | 成稿原文确认真实可读，ρ_n=5.75、`var(U)=0.082 vs 0.083`、Hoeffding 3.2–6.7×、ρ-不变性、T≤8 达 ANN−1.5pp 带内等表述逐项核对到 | 第三轮评审报告「成稿核对」段 |

**为什么 recommendation 是 pivot 而 decision 是 proceed（不矛盾）**：`ccf-idea-reviewer` 评的是**当前 idea 就绪度与录用潜力**（3.4/5 落在 `calibration.md` 3.0–3.6 段，故 `pivot-with-rescue-route`）；`f-guidance-builder-v1` 判的是**是否允许进入 G0 做 evidence-first 的后续闸门**。后者明文规定低分本身不构成拒绝，只要无未解 fatal risk。第三轮报告已显式给出这个区分与 `proceed` 建议。**我们不改写、不删除任何一轮评审原文，也不把 pivot 包装成 accept。**

## 2. 为何不取另外三个值

| 候选 | 不取理由 |
|---|---|
| `revise` | 六个 startup 工件本身无需整体重写；第三次评审指出的数值口径问题（SHA / P4 对数 / P3 隔离）已在 `protocols/m0_operator_theory_check.py` 中**实际修正并重跑**，不是待办。novelty 的核心质疑由 G0/G3/G4 的检索与推导处理，属阶段职责而非回炉重做工件。 |
| `pivot-with-rescue-route` | 这是 idea-reviewer 的 recommendation，不是 orchestrator 的 gate decision。第三轮已判定 0 未解 fatal，且「改问题·方法·证据」的救援动作恰由 G0/G3/G4/G7 依次执行；若在此提前 pivot，等于用 idea 分数否决技能明文允许的后续证据门。但保留硬回退：G0 命中近邻、G3 证明 T1 可一行照搬、或 G7 单调性连续落 failure → 立即回退到 `pivot-with-rescue-route`（H9）。 |
| `needs-evidence` | 决定「是否进 G0」所需证据已齐（三轮评审、文献地图、数据集核验、硬件、M0 实跑、统一协议）。视觉侧零正式实验是 guidance 阶段的正常状态，不是「缺证据无法决定」。若第 0 批 PASCAL/TPP 复现失败，由 S2 转 `needs-evidence`。 |

## 3. 硬条件 H1–H9（第三轮评审原样落地，全部为硬约束）

- **H1** 成稿 `p7-draft.md` / `guidance-v3.md` 及其中六项数值与结论，全程标注「用户提供的未公开先验（未发表、不充当公开证据）」；仅作机制/命题出处核对，不进公开证据、不进打分、不替代公开视觉实验。违反 → S6 停止。
- **H2** M0 边界不得外推为精度/判据/能耗已证。κ_n 单调性、κ_n–T2 张力、两解码兼容性、A5 消融、T1 非平凡性、`‖A‖` 界的严格证明、推论层检索，须列为 G3/G4 显式待办；未过不得进 P4/G7 主表。
- **H3** 第 0 批 PASCAL / TPP 必跑（任一未通不得进主表，S2 回退），并补 PASCAL 可判定验收锚。
- **H4** `matched-protocol.md` 升 v2 补齐「ρ=1 校准律在 ρ≠1 聚合上的适配语义」（不得针对 ρ 重调），并记 `reopen`。
- **H5** 把「单调」的趋势检验、比较单元与统计判据写入协议 §4，统一 §8 S4 与 `idea-cards-rev2.md` §1 第 4 条口径。
- **H6** B4 / C5 原版 ViG 失效边界实验不得删除；冻结 KNN + 线性化相对原版的精度代价（R4/A6）必须量化。
- **H7** 所有 `expected_strong` 一律「预注册目标 / 非实测」，G7 pilot 复现基线后锁阈值；SynOps / spike count / 显存一律标 proxy；不声称精度 SOTA、不声称发明已被占的数学组件、**不声称 T1/T2/κ_n 是「prior-art 无法得到的新数学结果」**。
- **H8** 统一哈希口径：以**磁盘字节 SHA-256** 为权威，内存规范化字符串哈希仅备查（Windows CRLF 造成二者不同，属编码差异）；M0 的 P4 对数以结果文件为准（5 个 T × 384 对 = 1920 对，任务描述里曾误写 3840）；收敛 P2/P3/P5 三处过表述。
- **H9** `proceed` ≠ novelty 已站稳。G0 检索命中近邻、G3 证明 T1 可一行照搬、或 G7 单调性连续落 failure → 按 S4 回退 `pivot-with-rescue-route`。

## 4. Stop-and-return → decision 回退映射

| 触发 | 回退后取值 |
|---|---|
| S1（M0 恒等式残差超容差）/ S7（数据协议违规） | `revise` |
| S2（第 0 批 PASCAL/TPP 复现失败）/ S5（资源未就绪） | `needs-evidence` |
| S3（原版动态/非线性 ViG 上恒等式仍成立）/ S4（单调判据连续落 failure）/ H9 | `pivot-with-rescue-route` |
| S6（任何诚信违规） | 停止，不可 handoff，回 `validation` 审计 |

## 5. 未决事项（不阻塞 proceed，须在对应门关闭）

| 项 | 类别 | 关闭门 |
|---|---|---|
| 具体 target venue / tier（现按 IEEE TNNLS / Q1–Q2 期刊档设计） | `must-know` | G8 / validation 前 |
| `torchvision` 补装 | `must-know`（G6 blocker） | G6 |
| 6 个官方基线仓库在 torch 2.11 下的兼容性 | `must-know`（QCFS 回归测试） | G6 |
| ρ=1 校准律的 ρ≠1 适配语义（协议 v2） | `must-know` | G3 / G6 |
| T1 非平凡性、κ_n–T2 张力、‖A‖ 严格界、推论层检索 | `must-know` | G3 / G4 |
| C1–C5 全部实验数值 | 执行产物，一律 `TBD` | G7 / P4 |
| 远端 4090 提交时机 | G7 之后按需；guidance 阶段不提交 | G7 |

## 6. 一致性自检

- 三轮评审原文、分数与 recommendation 全部保留，未修改未抬分；本文件只做 orchestrator 的 gate decision。
- 未出现任何虚构实验结果数值、虚构评审分数、虚构 URL；未把未发表内部先验当公开证据；未声称发明已占组件。
- 交付范围：CCFA packet 7 件（含 `idea-red-team-review.md`）+ 3 份增补评审 + `idea-cards-rev2.md` + `feasibility-contract.json` + 主会话的 8 份审计与 `guidance.md`。
