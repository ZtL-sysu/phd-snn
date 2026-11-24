---
idea_id: I4
overall: 2.8
confidence: 0.88
verdict: NO-GO
scores: {novelty: 2, mechanism: 2, evidence_plan: 1, baselines: 2, cvpr_fit: 1, executability_11d: 1}
fatal_risks:
  - "CVPR fit 致命：idea 自承 CVPR fit 明显更弱、容易被 desk reject 为不是 CV，主线漂向 graph representation learning/计算神经科学、丢失 SNN 成分，违反 execution-contract-v1.md 锁定的 GNN+SNN+视觉方向"
  - "11 天完全不可行：链条 对齐→共聚类→motif 提取→注入→验证 + 多数据集 + 辅助任务，在单次 ≤15min GPU、不做完整/多种子训练的冒烟预算下无法产出任何支撑核心主张的证据"
  - "因果链薄弱且自埋负结果：生物学结论与 CV 收益之间因果链薄弱，消融自定「若只在极小模型上有差异或跨数据集排序不稳定则证伪」正是稀疏先验常见负结果"
go_conditions:
  - "改投 venue 或彻底重构为视觉问题驱动、含 SNN/脉冲成分的贡献，使 topic 回到 CVPR 主会；否则维持 desk-reject 风险（等于换题）"
  - "把主张压缩到单一可证伪结论，并在远超 11 天、另起算力的窗口下完成 对齐→motif→注入→同参数量公平对照→跨数据集多种子验证"
  - "先与 cocoa/coconatfly、Nature 2024 跨连接组 cell typing、flyvis/Reiser 通路刻画、arXiv:2610.10023 随机图对照做正面对比，证明跨图共识 motif 的独立增量"
review_execution: independent-agent
---

# I4 独立评审报告 — Evolutionarily Conserved Visual Motifs as Transferable Sparse Priors for Vision Backbones

> 引用约定：下文 `文件名:行号` 均指向 `C:\code\phd-snn\auto-paper\20261105-204552\` 下的冻结输入文件；`references/` 指向 `ccf-paper-reviewer` 技能参考文件。所有 URL 均引自冻结输入中标注为 2026-11-05 已核验的来源，本独立评审未重新抓取、未编造。

## Mode

- 评审模式：`ccf-paper-reviewer` 的 **scientific（standard scientific 输出契约）**，独立单 agent 执行（`review_execution: independent-agent`）；与 I3 报告相互独立，未读取或复用其结论。
- 评审对象：**idea 卡片，不是论文**（`ideas/idea-cards.md:110-131`），零实验结果、零图表、零附录、无 Abstract/Intro/Conclusion 正文。
- 证据口径硬约束：`evidence` 维度评「**证据计划的可行性与完整性**」，不把计划写成已观测结果；全文不编造任何实验结果、数值或引用；所有分数为评审打分而非实验测量。
- 量纲：criterion 1-5；overall 1-10（一位小数）；front matter `confidence` 用 0-1（两位小数），正文同时给出 1-5 等价以便与 `calibration-and-rank.md` 对齐。
- 隐私边界：输入全部为本地冻结文件，未将私有文本用于任何联网查询；本轮未做公开检索（理由见 Unresolved or unverified）。

## Venue and assumptions

| 假设 | 来源 | 在本次判断中的效力 |
|:---|:---|:---|
| 目标 CVPR 2027 **主会**（CCF-A/顶会），不得用期刊 Q2 标准放水 | `execution-contract-v1.md:42`；`venue-review-styles.md:60-69`（CVPR 强调 novelty/技术质量/实证/视觉证据/公平比较） | 决定 reject 阈值；venue-fit 按主会口径从严 |
| 大方向锁定 GNN + SNN + 果蝇连接组 + 视觉，**不得漂到纯神经科学仿真或纯图表示学习** | `execution-contract-v1.md:43` | I4 丢失 SNN、视觉仅作下游验证，直接触发硬约束 |
| 全文截止 2026-11-16 AOE、注册 11-10，当前 2026-11-05，**仅 11 天** | `execution-contract-v1.md:37-41`；`ideas/idea-cards.md:5`；`https://cvpr.thecvf.com/Conferences/2027/CallForPapers` | 决定 `executability_11d`；卡片自承「11 天完全不可行」 |
| 本机仅 RTX 3060 12GB；**无法对 166k 神经元 / 5450 万突触整图做长序列 BPTT 或对齐，必须子图化** | `hardware-profile.md:34-40`；`execution-contract-v1.md:47-52` | 两图对齐/共聚类规模与显存冲突 |
| 冒烟预算：单次 ≤15min GPU、显存 ≤10GB、下载 ≤1.5GB，**不做完整训练/多种子大实验**；远程算力 opt-in 本轮不用 | `execution-contract-v1.md:51-52`；`hardware-profile.md:41` | I4 完整链条远超该信封 |
| 最强竞争 arXiv:2610.10023（2026-10-08）：复眼 Voronoi + FlyWire 全图无状态 GNN + 4 种随机图等布线预算对照，must-rerun | `https://arxiv.org/abs/2610.10023`；`literature-baseline-matrix.md:8`；`prior-art-dedup-log.md:11` | 决定「生物图 vs 随机稀疏」对照是否已被做过 |
| 2026-09-15 后上线论文视为 **contemporaneous**，须引用讨论、高度相似加审；「同一模型+换数据集」仍判 incremental | `prior-art-dedup-log.md:16-21`；`execution-contract-v1.md:40-41` | 约束 I4 相对 P1 的增量定位 |
| cocoa / coconatfly 跨连接组比较工具、Nature 2024 跨连接组 cell typing、flyvis/Reiser 视叶通路刻画、P4 MaleCNS 图分析已存在 | `ideas/idea-cards.md:126`；`literature-baseline-matrix.md:12,14,20`；`prior-art-dedup-log.md:13-14` | 压缩「跨连接组共识 motif」剩余新颖空间 |
| 输入为 idea 卡片，无任何实验结果；G6-G8/validation/handoff 保持 pending，不伪造 pass | `execution-contract-v1.md:28-33`；任务约束 | evidence 只评计划，不评结果 |

## Paper summary

I4 主张用两个独立完整连接组——雄 MaleCNS（166,691 神经元 / 1.25 亿突触）与雌 FlyWire（139,255 神经元 / 5450 万突触）——配合 `ol_annotations` 跨数据集视叶 cell-type 匹配，提取「跨个体稳定出现」的视觉 motif（前馈链、反馈环、ON/OFF 分叉），再把 motif 分布作为**稀疏 MLP / 稀疏注意力的拓扑生成器**注入 CV backbone，假设保守 motif 携带对视觉统计有用的归纳偏置、在参数受限时优于同稀疏度随机图（`ideas/idea-cards.md:110-119`）。贡献类型自定为「结构先验发现 + 架构迁移」（`:122`），任务为 CIFAR-10/100、ImageNet-100 子集的参数量-精度权衡，辅助任务为细胞类型/递质预测（`:123`）。

- **Claimed problem**：一个连接组只是「一个个体的接线」，现有工作都在单图上建模，没人把跨图共识 motif 提取成可注入 CV backbone 的稀疏先验（`:114-116`）。
- **Claimed gap**：两个完整连接组 + 跨数据集 cell-type 匹配「第一次让『哪些视觉 motif 是保守的』可被测量」（`:115-116`，原句）。
- **Method / contribution map**：GNN 在两图上对齐/共聚类 → 提取保守 motif 分布 → 作为稀疏 MLP/注意力拓扑生成器替代随机稀疏或手工局部性（`:117-119`）。
- **Evidence package（计划，非结果）**：可证伪消融「保守 motif vs 单图 motif vs 度匹配随机稀疏 vs 稠密」，判据「若只在极小模型上有差异、或跨数据集排序不稳定，机制被证伪」（`:120-121`）；强基线为随机稀疏/ER/小世界、ViT 稀疏注意力、`train-your-fly` 随机图 ensemble（`:124`）；最小冒烟为加载 MaleCNS 与 FlyWire 两图的度/motif 统计，验证两图视叶子图 motif 分布相关性是否显著高于随机对照（`:127-128`）。
- **Stated limitations（卡片自承）**：「CVPR fit 明显更弱（更像 graph representation learning / 计算神经科学），且 cocoa、coconatfly 等比较连接组工具已存在」（`:125-126`）；「链条长（对齐→motif→注入→验证）；生物学结论与 CV 收益之间因果链薄弱；11 天完全不可行；容易被 desk reject 为『不是 CV』」（`:129-130`）；「11 天可投性：极低」（`:131`）；漏斗提示「最可能被 CCF 判致命：I4（CVPR fit）」（`:187`）。
- **可恢复性**：卡片结构清晰、自承限制充分；但无正文/图表/结果，Clarity/Format 相关维度只按「卡片表述 + 未来投稿要求」评估，并标注 not available 项。

## Likely stance and calibrated score

- **Expected outcome**：`verdict: NO-GO`；overall **2.8 / 10**，confidence **0.88（≈4.5/5）**。按 `calibration-and-rank.md:43-47` 落在 clear reject / desk-reject-level；存在 3 条未解决 fatal risk，规则禁止 GO。置信度偏高是因为致命点由卡片**自承**且与冻结输入（硬件、时间线、去重日志、基线矩阵）一致，判断不依赖缺失的实验结果。
- **Main accept signal**：跨连接组「保守 motif 作为可迁移稀疏先验」的提法有一定概念新意；消融设计可证伪；冒烟为只读统计、成本极低，可作为廉价一票否决。
- **Main reject signal**：CVPR fit 致命（含方向漂移）、11 天完全不可行、因果链薄弱 + prior art 拥挤。

**Q1｜相对 arXiv:2610.10023，这个增量是否足以撑起 CVPR 主会？→ 否，且比 I3 更弱。** 依据链：I4 自定「避开 P1-P4 的任务与主张」（`ideas/idea-cards.md:125`），但（a）P1 已做 FlyWire 全图 + 生物图 vs 4 种随机图在等布线预算下的对照（`literature-baseline-matrix.md:8`；`prior-art-dedup-log.md:11`），I4 的「注入稀疏 MLP/注意力 + 同稀疏度随机对照」与该轴高度相邻；（b）I4 的增量是「加第二张图 + 跨图共识 + 迁移到通用 backbone」，属**数据/分析维度扩展**，既未解决 CV 社区关心的视觉问题、也未承诺可归因的机制结论（对比 I1 的 2×2 交互归因，`ideas/idea-cards.md:33-37`）；（c）cocoa/coconatfly（`:126`）、Nature 2024 跨连接组 cell typing（`literature-baseline-matrix.md:12`）、flyvis/Reiser 视叶通路刻画（`prior-art-dedup-log.md:13`）、P4 MaleCNS 图分析（`literature-baseline-matrix.md:20`）已占据跨连接组比较与视叶组织空间；（d）CVPR fit「明显更弱」（`:125`）。因此该增量不仅不足以撑起主会，venue 错配更使其可能连主审都进不了（`:130`）。

**Q2｜若只有部分正向结果，诚实可发表的下位结论是什么？** 可写成一条**跨连接组描述性结论**：「MaleCNS 与 FlyWire 视叶子图在度/motif 分布上的相关性显著高于度匹配随机对照（或否），保守 motif 以 X 类为主；单图 motif 与跨图共识 motif 在稳定性上存在差异（或否）。」无论正负，这是计算神经科学 / 连接组学可用的描述性（含负结果）结论，适合专用 venue 或作为数据集附注（`ideas/idea-cards.md:127-128` 的冒烟即指向此）。**但不得据此声称「保守 motif 作为可迁移稀疏先验提升 CV backbone」——冒烟相关性不触及注入 backbone 的 CV 收益，核心主张仍无证据；更不是 CVPR 主会论文。**

**Q3｜最小冒烟实验是否值得跑：NO-GO。** 计划见 `ideas/idea-cards.md:127-128`（加载 MaleCNS 与 FlyWire 两图度/motif 统计，验证视叶子图 motif 分布相关性是否显著高于随机对照）。判定理由：（a）即便相关性显著为正，也只验证「motif 保守」这一生物学前提，**完全不触及**「注入 backbone 有 CV 收益」的核心主张，结果无法翻转 NO-GO；（b）verdict 已因 venue-fit（F1）与 11 天不可行（F2）而致命，这两项独立于该统计结果；（c）占用 11 天窗口与 ≤1.5GB 下载预算（`execution-contract-v1.md:51`）的产出比为负。诚实补充：若把它当作「1 次只读统计、零训练、≤15min 的一票否决检查」，成本极低且具证伪价值；但鉴于两个致命项不依赖其结果，仍不推荐占用主会窗口。**可证伪失败信号**：两图视叶子图 motif 分布相关性与度匹配随机对照无显著差异（p 不显著），或跨数据集排序不稳定（`ideas/idea-cards.md:121` 自定判据）→「保守 motif 存在且稳定」前提被证伪，整个 idea 归零；**但即便为正也因 F1/F2 不转为 GO**。

## Quantitative scorecard

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction & Repair condition | Expected score movement |
|:---|:---:|:---:|:---|:---|:---|
| novelty | 2 | 4 | `ideas/idea-cards.md:115-116,125-126`；`prior-art-dedup-log.md:11,13-14`；`literature-baseline-matrix.md:8,12,14,20` | **Deduction**：「两个完整连接组让保守 motif 可测量」有一定概念新意（`:115-116`），但被 cocoa/coconatfly（`:126`）、Nature 2024 跨连接组 cell typing（`literature-baseline-matrix.md:12`）、P3 flyvis/Reiser 视叶通路刻画（`prior-art-dedup-log.md:13`）、P1 生物图 vs 随机图对照（`:11`）、P4 MaleCNS 图分析拥挤（`literature-baseline-matrix.md:20`）压缩；差异化轴窄且未与这些工作正面对比。**Repair condition**：证明跨图共识 motif 相对单图 motif/随机稀疏有独立、可迁移的增量，并与 cocoa/coconatfly、arXiv:2610.10023 正面对比。 | +1（→3）仅当独立增量被实证支持；单纯改 venue 不改变 novelty 分 |
| mechanism | 2 | 4 | `ideas/idea-cards.md:117-121,129`；`execution-contract-v1.md:43` | **Deduction**：对齐/共聚类算法未定义（`:117` 仅「用 GNN 做对齐/共聚类」一句）；`:129` 自承「生物学结论与 CV 收益之间因果链薄弱」；无脉冲/动力学成分、偏离锁定方向（`execution-contract-v1.md:43`）；消融自定「若只在极小模型上有差异、或跨数据集排序不稳定，机制被证伪」（`:121`）恰是稀疏先验文献常见负结果，核心主张（`:119` 保守 motif 携带视觉有用归纳偏置）缺机制保证。**Repair condition**：给出「保守 motif → 视觉归纳偏置」的因果机制与中介量、定义对齐/共聚类算法、恢复 SNN/脉冲成分或明确视觉问题驱动。 | +1（→3）当因果论证 + 消融支持成立；overall 仅在此时 +0.5 |
| evidence_plan | 1 | 5 | `ideas/idea-cards.md:117-123,127-131`；`hardware-profile.md:36`；`execution-contract-v1.md:51-52,37-41` | **Deduction**：`:130-131` 自承「11 天完全不可行」「极低」；链条 4 段（对齐→共聚类→motif→注入→验证）+ 3 个数据集（`:123`）+ 辅助任务（细胞类型/递质预测），在单次 ≤15min GPU、不做完整/多种子训练（`execution-contract-v1.md:51-52`）下无法产出任何支撑核心主张的证据；`hardware-profile.md:36` 12GB 无法整图对齐需子图化；冒烟（`:127-128`）只验证 motif 相关性、不触及核心主张。**Repair condition**：在远超 11 天、另起算力的窗口下完成完整链条 + 同参数量公平对照 + 跨数据集多种子 + 95% CI。 | 11 天内 0；窗口外完整证据包最多 +2（→3），但不解除 CVPR fit 致命 |
| baselines | 2 | 4 | `ideas/idea-cards.md:120,124`；`literature-baseline-matrix.md:31`；`dataset-access-log.md:35` | **Deduction**：列了随机稀疏/ER/小世界、ViT 稀疏注意力、`train-your-fly` 随机图 ensemble（`:124`），方向可识别；但缺「同稀疏度/同参数量」公平协议细节、缺「单图 motif vs 跨图共识 motif」隔离对照的实现、缺 CVPR 视觉强基线与多种子 95% CI（`dataset-access-log.md:35`），且 `literature-baseline-matrix.md:31` 明确「不可仅与 ANN toy baseline 比较」。**Repair condition**：补双预算公平协议 + 单图/跨图 motif 隔离 + 视觉强基线 + 95% CI。 | +1（→3）当协议与隔离对照落地 |
| cvpr_fit | 1 | 5 | `ideas/idea-cards.md:125-126,130,187`；`execution-contract-v1.md:42-43`；`universal-review-rubric.md:76`；`desk-checks.md:23-25` | **Deduction**：卡片自承「CVPR fit 明显更弱（更像 graph representation learning / 计算神经科学）」（`:125`）、「容易被 desk reject 为『不是 CV』」（`:130`）、漏斗「最可能被 CCF 判致命：I4（CVPR fit）」（`:187`）；主线为 GNN 对齐/共聚类 + 结构先验 + 架构迁移，视觉任务仅下游验证，且丢失 SNN 成分违反 `execution-contract-v1.md:43` 锁定方向。按 `universal-review-rubric.md:76`（venue fit is wrong）与 `desk-checks.md` 主题相容性，属独立可拒。**Repair condition**：改投 venue 或彻底重构为视觉问题驱动、含 SNN/脉冲成分的贡献，使 topic 回到 CVPR 主会。 | +1 ~ +2（→2-3）仅在彻底重构（等于换题）后；当前窗口内 unlikely |
| executability_11d | 1 | 5 | `ideas/idea-cards.md:130-131,117-123`；`hardware-profile.md:36`；`execution-contract-v1.md:51-52,37-41` | **Deduction**：自承「11 天完全不可行」「极低」（`:130-131`）；两图 166k/139k 在 12GB 上无法整图对齐（`hardware-profile.md:36`）；多数据集 + 辅助任务 + 4 段链条远超「单次 ≤15min GPU、不做完整训练」预算（`execution-contract-v1.md:51-52`）。**Repair condition**：无 11 天内路径；需另起窗口与算力，且须先解决 venue-fit。 | 11 天内 0；窗口外 +1 ~ +2 但不解 F1 |

**Overall: 2.8 / 10 | Confidence: 0.88（≈4.5/5 scholarly confidence）**
**Recommendation（顶会主会口径）：reject / desk-reject-level。**
**Verdict: NO-GO**；规则依据：overall 2.8 < 6.5 且 3 条 fatal risk 未解决 → 不可 GO；致命风险存在且**无窗口内可修复路径**（F1 venue 错配 + F2 11 天不可行均为结构性），故取 NO-GO 而非 REVISE。`go_conditions` 均为「改投/换题/另起窗口」级条件，本轮 CVPR 2027 主会 11 天内不可达。

**Score-change conditions（conservative，见 `calibration-and-rank.md:112-120`）**

| Change | Condition | Likely affected dimensions | Expected movement |
|:---|:---|:---|:---|
| Raise score | 彻底改投 venue 或重构为视觉问题驱动含脉冲成分 + 窗口外完整证据包 + 因果机制结论 + 正面对比 | cvpr_fit / mechanism / evidence_plan / executability_11d | 各维度 +1 ~ +2；overall +1.5 ~ +2.5（→4.3-5.3，仍远低于 6.5，且等于换题） |
| Lower score | 冒烟显示两图 motif 相关性与度匹配随机对照无显著差异，或跨数据集排序不稳定 | novelty / mechanism / evidence_plan | overall −0.5 ~ −1 或维持 fatal |
| No quick change | CVPR fit 错配与 11 天不可行是结构性、窗口内不可改 | cvpr_fit / executability_11d | 提交前 unlikely 改变，维持 NO-GO |

## Top strengths

1. **概念角度有一定新意**：`ideas/idea-cards.md:115-116`「两个独立完整连接组 + `ol_annotations` 跨数据集视叶 cell-type 匹配，第一次让『哪些视觉 motif 是保守的』可被测量」；`dataset-access-log.md:10-12,17` 标注 MaleCNS 全图/标注/递质预测与 `ol_annotations` 均 PASS，数据零摩擦。
2. **消融可证伪**：`ideas/idea-cards.md:120-121`「保守 motif vs 单图 motif vs 度匹配随机稀疏 vs 稠密；若只在极小模型上有差异、或跨数据集排序不稳定，机制被证伪」——判据明确，符合 `universal-review-rubric.md:80-93` 的 claim-evidence 纪律。
3. **冒烟只读、零训练、成本极低**：`ideas/idea-cards.md:127-128` 仅加载两图度/motif 统计做相关性检验，符合 `execution-contract-v1.md:51-52` 预算，作为一票否决检查有信息价值（但不改变 verdict，见 Q3）。
4. **去重意识与自承诚实**：`ideas/idea-cards.md:125,129-131` 主动避开 P1-P4 任务并逐条列出致命限制（链条长、因果链薄弱、11 天不可行、desk reject 风险），便于筛选轮快速淘汰。

> 注：以上均为「计划/定位质量」评价，**不代表任何已观测结果**；且按 `review-output-standards.md:34`（不强行夸奖），这些优点均不足以抵消 F1/F2/F3 三条致命风险。

## Major-fatal concerns

**F1 [fatal] CVPR fit / venue 错配（含方向漂移）。**
- Evidence basis：`ideas/idea-cards.md:125-126`（「CVPR fit 明显更弱（更像 graph representation learning / 计算神经科学）」原句）、`:130`（「容易被 desk reject 为『不是 CV』」）、`:187`（漏斗「最可能被 CCF 判致命：I4（CVPR fit）」）；`execution-contract-v1.md:42-43`（顶会标准 + 锁定 GNN+SNN+视觉、不得漂到纯图表示学习）；`universal-review-rubric.md:76`（venue fit is wrong 独立可拒）；`desk-checks.md:23-25`（主题相容性）；`venue-review-styles.md:60-69`。
- Reviewer deduction：主线是 GNN 对齐/共聚类 + motif 结构先验 + 架构迁移，视觉任务（CIFAR/ImageNet-100）只是下游验证而非问题驱动；卡片**自承**明显更弱且可能被 desk reject；且 I4 无 SNN/脉冲成分，违背 `execution-contract-v1.md:43` 硬约束。按 fatal-risk triage 独立可拒，且可能未进入主审即被 desk reject。
- Required fix：改投 venue 或彻底重构为视觉问题驱动、含 SNN/脉冲成分的贡献；等于换题。
- Score-change condition：结构性、窗口内 unlikely；F1 不解除则 overall 不可能接近 6.5。

**F2 [fatal] 11 天完全不可行 / 证据计划无法产出核心证据。**
- Evidence basis：`ideas/idea-cards.md:130-131`（「11 天完全不可行」「极低」）、`:117-123`（4 段链条 + CIFAR-10/100/ImageNet-100 + 细胞类型/递质预测辅助任务）、`:127-128`（冒烟只验证 motif 相关性）；`hardware-profile.md:36`（12GB 无法整图、须子图化）；`execution-contract-v1.md:51-52`（≤15min GPU、不做完整/多种子训练）；`:37-41`（11 天）。
- Reviewer deduction：完整链条 + 多数据集 + 辅助任务远超冒烟预算；即便跑通冒烟也只验证生物学前提，核心主张「注入 backbone 提升 CV」仍无任何证据，按 `universal-review-rubric.md:72`（main claim lacks evidence）与 `:74`（invalid evaluation protocol）独立可拒。
- Required fix：无 11 天内路径；需另起窗口与算力。
- Score-change condition：11 天内 0；F1 与 F2 同时存在即确定 NO-GO。

**F3 [fatal] 因果链薄弱且消融自埋负结果。**
- Evidence basis：`ideas/idea-cards.md:129`（「生物学结论与 CV 收益之间因果链薄弱」原句）、`:119`（假设「保守 motif 携带对视觉统计有用的归纳偏置」）、`:121`（「若只在极小模型上有差异、或跨数据集排序不稳定，机制被证伪」）。
- Reviewer deduction：核心假设缺机制保证与中介量；而自设证伪条件恰是稀疏/结构先验文献中最常见的负结果形态（增益只在极小模型、跨数据集不稳），等于预埋机制失败。按 `universal-review-rubric.md:70`（central contribution unclear / claim lacks evidence）独立可拒。
- Required fix：给出「保守 motif → 视觉归纳偏置」的因果机制与可测中介量，并把消融改为能正面支持机制的判据。
- Score-change condition：+1 mechanism 当因果论证成立；不改变 F1/F2。

**M4 [major] Novelty 被 prior art 拥挤压缩 / 缺正面对比。**
- Evidence basis：`ideas/idea-cards.md:126`（cocoa、coconatfly 已存在）、`:115-116`（「第一次」主张）；`prior-art-dedup-log.md:11,13-14`；`literature-baseline-matrix.md:8,12,14,20`；`https://arxiv.org/abs/2610.10023`。
- Reviewer deduction：跨连接组比较工具、Nature 2024 跨连接组 cell typing、flyvis/Reiser 视叶 ON/OFF/层级/通路刻画、P4 MaleCNS 图分析、P1 生物图 vs 随机图对照已占据空间；I4 的「第一次让保守 motif 可测量」若不收窄并与上述工作正面对比，构成 `fixed-output-format.md:73-83` 的 potentially missing related work 与 overstated priority claim（status: unverified，见 Unresolved）。
- Required fix：正面对比 cocoa/coconatfly、Nature 2024 cell typing、arXiv:2610.10023，证明跨图共识 motif 的独立增量；把「第一次」收窄到「作为可注入 CV 先验」。
- Score-change condition：novelty +0.5 ~ +1；overall +0.5。

**M5 [major] Baselines / 公平协议缺口。**
- Evidence basis：`ideas/idea-cards.md:120,124`；`literature-baseline-matrix.md:31`（不可仅与 ANN toy baseline 比较）；`dataset-access-log.md:35`（主指标含 95% CI）。
- Reviewer deduction：缺「同稀疏度/同参数量」双预算公平协议、缺「单图 motif vs 跨图共识 motif」隔离对照实现、缺 CVPR 视觉强基线与多种子 95% CI；参数量-精度权衡主张（`:123`）在弱基线下不可信。
- Required fix：补双预算协议 + 隔离对照 + 视觉强基线 + 多种子 95% CI。
- Score-change condition：baselines +1；overall +0.5（但仍受 F1/F2 封顶）。

## Writing and presentation concerns

- 输入为 idea 卡片、无论文正文/图表/附录，故本维度只评「卡片表述清晰度 + 未来投稿可恢复性」；页数、匿名、模板、figure/table narration 标 **not available**，不虚构。
- **优先声明风险**：`ideas/idea-cards.md:115-116`「第一次让『哪些视觉 motif 是保守的』可被测量」是 first/priority 主张，但 cocoa/coconatfly（`:126`）与 Nature 2024 跨连接组 cell typing（`literature-baseline-matrix.md:12`）已做跨连接组比较/cell typing。若进入论文须把「第一次」收窄为「跨图共识 motif 作为可注入 CV 先验」，否则按 `universal-review-rubric.md:93` 属对 unsupported claim 做修辞加强，硬规则要求弱化/删除/补证据。
- **假设须标为假设**：`ideas/idea-cards.md:119`「保守 motif 携带对视觉统计有用的归纳偏置」为未证假设；写作时不得写成结论，须与 `:121` 的证伪判据对齐。
- **术语/判据稳定性**：「motif / 稀疏先验 / 拓扑生成器 / 共聚类 / 保守」需统一定义，「保守」须给统计判据并与 `:128` 的相关性检验一致，否则 `review-output-standards.md:73` 的 terminology stability 风险。
- 遵守任务：本报告不写 rebuttal、不修改 idea、不生成论文文本。

## Format-venue concerns

- **CVPR 2027 主会格式**：`venue-guides/cvpr.md:73-96` 为 8 页上限（不含 references/appendix）、双盲、`cvpr.sty`、rebuttal 期；但 `:12-13` 明示为 **2026 legacy、投稿前须按当年官方政策复核**，故以 `https://cvpr.thecvf.com/Conferences/2027/CallForPapers` 为准（本评审未独立复核官方页，见 Unresolved）。idea 卡片阶段这些项均 **not applicable / not available**。
- **venue-fit 是本节核心（硬约束）**：`venue-review-styles.md:60-69` 要求视觉证据、强近期基线、公平比较、与近邻 CV 工作清晰关联；I4 证据计划（`:123-124`）为参数量-精度权衡 + 细胞类型/递质预测辅助任务，更像 graph representation learning / 计算神经科学，与 CVPR 主会视觉贡献口径错配；`desk-checks.md` 主题相容性 fail → **Desk rejection risk: likely**（`:47-51`），Can be fixed before review? **no**（需换题/换 venue）。
- **大方向锁定**：`execution-contract-v1.md:43` 不得漂到纯图表示学习/纯神经科学仿真，I4 丢失 SNN、视觉仅下游验证，触发硬约束；这是与 I3 的关键区别（I3 仍含 LIF/脉冲与视觉基准）。
- **contemporaneous 引用义务**：`prior-art-dedup-log.md:18-21`、`execution-contract-v1.md:40-41`——若涉及 arXiv:2610.10023 须引用讨论；I4 的「随机稀疏 vs 生物图」轴与之高度相邻，须正面对比。
- **时间线**：注册 11-10、全文 11-16（`execution-contract-v1.md:37-38`）；即便重构，11 天内产出主会级证据包不可达（F2）。

## Multi-reviewer panel

> 三名审稿人先独立成形再综合；结论差异来自各自 lens 的权重，非人为制造分歧或强行夸奖（`review-output-standards.md:27-38`、`reviewer-panel.md:1-5`）。I4 的三人一致偏负，差异仅在负面程度与是否计入生物学描述价值。

**R1 — 连接组 / 计算神经科学专家**
- Lens：跨连接组比较、motif 保守性、生物学有效性、数据可得性。
- Score tendency：5/10（borderline，本 panel 相对最高，但仅限生物学描述层）。
- Confidence：0.80（两图 motif 相关性未跑、cocoa/coconatfly 重叠未核验，部分标 insufficient evidence）。
- Main positive signal：`ideas/idea-cards.md:115-116` 两个完整连接组 + `ol_annotations` 让保守 motif 可测量；`dataset-access-log.md:10-12,17` 数据全部 PASS；`:127-128` 冒烟只读统计可廉价检验相关性——作为纯科学描述问题有独立价值。
- Main negative signal：`ideas/idea-cards.md:126` cocoa/coconatfly 已存在、`prior-art-dedup-log.md:13` P3 flyvis/Reiser 已系统刻画视叶 ON/OFF/层级/通路、`literature-baseline-matrix.md:12` 跨连接组 cell typing 已发表 → 「发现保守 motif」的生物学空间被压缩；`:129` 生物学结论与 CV 收益因果链薄弱。
- Evidence basis：`ideas/idea-cards.md:115-116,126,129`；`dataset-access-log.md:10-12,17`；`prior-art-dedup-log.md:13`；`literature-baseline-matrix.md:12`。
- Score-change condition：若证明跨图共识 motif 相对单图 motif 有独立、统计稳健的增量并对 cocoa/coconatfly 正面对比 → +1；若仅看纯科学价值、不计 venue/时间可到 6，但本轮是 CVPR 主会选题筛选，故压到 5。

**R2 — GNN / 图表示学习专家**
- Lens：对齐/共聚类方法、motif 提取、稀疏先验注入、方法链条有效性。
- Score tendency：4/10（lean reject）。
- Confidence：0.78（对齐算法未定义、整图规模显存冲突，标 insufficient evidence）。
- Main positive signal：`ideas/idea-cards.md:117-119` 把 motif 分布作为稀疏 MLP/注意力拓扑生成器、`:120-121` 消融隔离「单图/跨图/随机/稠密」，方法链条自洽且可证伪。
- Main negative signal：`:117`「用 GNN 在两图上做对齐/共聚类」算法未定义；两图 166k/139k（`:114-115`）在 12GB 上整图对齐不可行（`hardware-profile.md:36`）；`:129` 链条长、因果链薄弱；`:121` 自定证伪条件恰是稀疏先验常见负结果；P4 MaleCNS 图分析已拥挤（`literature-baseline-matrix.md:20`）。
- Evidence basis：`ideas/idea-cards.md:114-121,129`；`hardware-profile.md:36`；`literature-baseline-matrix.md:20`。
- Score-change condition：给出对齐算法定义 + 保守 motif 的因果中介量 + 同参数量公平对照 → +1。

**R3 — CV 架构 / 效率专家（兼 AC 视角）**
- Lens：标准 CV 基准、强基线、公平协议、venue fit、贡献量级、可执行性。
- Score tendency：2/10（strong reject / desk-reject）。
- Confidence：0.90（卡片自承多条致命点且与冻结输入一致，依据充分）。
- Main positive signal：`ideas/idea-cards.md:123-124` 列了 CIFAR-10/100、ImageNet-100 与随机稀疏/ER/小世界/ViT 稀疏注意力/`train-your-fly` ensemble，基线方向可识别（诚实但弱）。
- Main negative signal：`ideas/idea-cards.md:125,130,187` 自承 CVPR fit 明显更弱、desk reject 为不是 CV、漏斗判致命；`execution-contract-v1.md:43` 丢失 SNN/漂向图表示学习；`literature-baseline-matrix.md:31`「不可仅与 ANN toy baseline 比较」；`:130-131` 11 天完全不可行；相对 arXiv:2610.10023 增量不解决视觉问题（`prior-art-dedup-log.md:11,21`）。
- Evidence basis：`ideas/idea-cards.md:123-125,130-131,187`；`execution-contract-v1.md:43`；`literature-baseline-matrix.md:31`；`prior-art-dedup-log.md:11,21`。
- Score-change condition：彻底改投/重构为视觉问题驱动 + 窗口外完整证据包 → +1 ~ +2；当前窗口内 unlikely。

**Panel synthesis**
- Agreement: CVPR fit 致命（F1）、11 天完全不可行（F2）、因果链薄弱（F3）、prior art 拥挤、相对 arXiv:2610.10023 增量不足以撑起主会——三人一致；无强行制造的分歧。
- Disagreement: 仅**程度/镜头**差异，非结论对立——R1 认为「跨连接组保守 motif 的可测量性」作为纯科学描述仍有价值（其 lens 不评 venue/可行性，故给 5），R2 从方法有效性给 4，R3 因同时计入 venue 与可执行性给 2；三人均不改「NO-GO」终局。
- Decisive accept axis: **当前形态无现实 accept 轴**；理论上需视觉问题驱动 + 含脉冲成分（解 F1）+ 另起窗口完成完整证据包（解 F2）+ 因果机制结论（解 F3），且等于换题/换 venue。
- Decisive reject axis: F1（venue-fit 错配）+ F2（11 天不可行）+ F3（因果链薄弱）任一独立可拒；`:130`「desk reject 为不是 CV」使其可能连主审都进不了。
- Unresolved evidence: 零实验结果；cocoa/coconatfly、Nature 2024 cell typing 与 I4 的确切重叠（未检索核验）；两图 motif 相关性是否显著（未跑）；CVPR 2027 主会对「结构先验/图表示学习」类稿件的 desk 边界；官方政策页未复核。
- Final calibrated stance: **NO-GO，overall 2.8 / confidence 0.88**；按 `reviewer-panel.md:108-110` 不把致命缺陷平均掉，最终立场跟随最强未解决关切（F1 venue + F2 可行性），且因无窗口内修复路径取 NO-GO 而非 REVISE。

## Concern-to-action table

| ID | Severity | Concern | Evidence basis | Affected criterion | Fix class | Required action | Owner skill | Score-change condition |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| F1 | fatal | CVPR fit 明显更弱、desk reject 为不是 CV、漂移出锁定方向 | `ideas/idea-cards.md:125-126,130,187`；`execution-contract-v1.md:42-43`；`universal-review-rubric.md:76` | cvpr_fit / novelty | venue-mismatch | 改投 venue 或彻底重构为视觉问题驱动、含 SNN/脉冲成分（等于换题） | `f-guidance-builder-v1`（另起选题，非本评审改 idea） | 结构性，窗口内 unlikely |
| F2 | fatal | 11 天完全不可行，完整链条远超冒烟预算，核心主张无证据 | `ideas/idea-cards.md:117-123,127-131`；`hardware-profile.md:36`；`execution-contract-v1.md:51-52` | evidence_plan / executability_11d | experiment | 无 11 天内路径；另起窗口与算力并完成完整证据包 | 本地冒烟执行（零训练只读检查仅作一票否决）/ `f-research-v1`（窗口外） | 11 天内 0 |
| F3 | fatal | 因果链薄弱 + 消融自埋负结果 | `ideas/idea-cards.md:119,121,129` | mechanism | method/soundness | 给出「保守 motif → 视觉归纳偏置」因果机制与中介量，重设能正面支持机制的消融判据 | `f-guidance-builder-v1` / 作者侧 | +1 mechanism 当成立 |
| M4 | major | cocoa/coconatfly、跨连接组 cell typing、P1 随机图对照已占据空间；缺正面对比 | `ideas/idea-cards.md:126`；`prior-art-dedup-log.md:11,13-14`；`literature-baseline-matrix.md:8,12,20`；`https://arxiv.org/abs/2610.10023` | novelty / baselines | related-work | 正面对比并收窄「第一次」主张，证明跨图共识 motif 独立增量 | `ccf-paper-reviewer`（定位复审）/ 作者侧 | novelty +0.5 ~ +1 |
| M5 | major | 缺同参数量/同稀疏度公平协议、单图/跨图隔离对照、视觉强基线、多种子 CI | `ideas/idea-cards.md:120,124`；`literature-baseline-matrix.md:31`；`dataset-access-log.md:35` | baselines / evidence_plan | experiment / reproducibility | 补双预算协议 + 隔离对照 + 强基线 + 95% CI | 本地冒烟执行 / `f-research-v1`（窗口外） | baselines +1；overall +0.5（受 F1/F2 封顶） |
| Q1 | fatal-adjacent | 相对 arXiv:2610.10023 增量不足以撑起主会 | `prior-art-dedup-log.md:11,21`；`ideas/idea-cards.md:125`；`https://arxiv.org/abs/2610.10023` | novelty / cvpr_fit | venue-mismatch | 明确回答「否」，按下位结论改投或换题 | `f-guidance-builder-v1` / 作者侧 | 与 F1 同 |
| Q3 | moderate | 冒烟 NO-GO（只读相关性不触及核心主张、不翻转 verdict） | `ideas/idea-cards.md:127-128,121`；`execution-contract-v1.md:51-52,72` | evidence_plan | experiment | 不占用主会窗口；若做，仅作一票否决并记录可证伪失败信号 | 本地冒烟执行 | 相关性不显著 → 前提证伪、idea 归零；为正亦不转 GO |

## Recommended next CCFA owner

- **主 owner**：选题筛选轮**淘汰 I4**——依据 `execution-contract-v1.md:28-32`（本轮为 idea-screening round）与 `ideas/idea-cards.md:187` 漏斗提示（I4 CVPR fit 最可能致命）。不进入完整实验、不占用 CVPR 2027 主会 11 天窗口。本评审不修改 idea、不生成论文文本、不写 rebuttal。
- **若保留跨连接组分析兴趣**：另起「计算神经科学 / 图表示学习」venue 的选题（非本轮、非 CVPR 2027 主会），由 `f-guidance-builder-v1` 另开目录，并先完成 M4 的正面对比与 Q2 的下位结论定位。
- **不交接**：`ccf-rebuttal-writer`（任务不写 rebuttal）、`ccf-paper-writer`（任务不生成论文文本）。
- **建议优先级**：转 `ideas/idea-cards.md:186-188` 的 I1（机制最硬）/ I6（I1 的 mini-benchmark 副产品）/ I3（需按 REVISE 重构），均比 I4 更贴锁定方向与窗口。
- **量纲/交接说明**：本报告为 `CCFA Handoff Mode: PARTIAL` 下的独立评审产物，G6-G8/validation/handoff 保持 pending（`execution-contract-v1.md:30-33`），不伪造 pass。

## Checks run

- 已加载并遵循 `ccf-paper-reviewer`(scientific) 及其 `review-output-standards.md` / `universal-review-rubric.md` / `calibration-and-rank.md` / `reviewer-panel.md` / `venue-review-styles.md` / `review-workflow.md` / `fixed-output-format.md` / `desk-checks.md` / `venue-guides/cvpr.md`。
- 已读全部 6 个冻结输入：`ideas/idea-cards.md`、`prior-art-dedup-log.md`、`literature-baseline-matrix.md`、`dataset-access-log.md`、`hardware-profile.md`、`execution-contract-v1.md`。
- 四遍读（`review-workflow.md:24-29`）：desk / contribution / evidence / adversarial 均执行；因无正文，evidence pass 针对「计划」而非结果。
- 执行 audits：claim-evidence（针对 `:115-116` 优先声明、`:119` 假设、`:129` 限制）、related-work positioning（cocoa/coconatfly、P1/P3/P4、contemporaneous 规则）、venue fit（desk checks）、reproducibility、output quality gate。
- 对每个 ≤3 分维度（本 idea 6 项全部 ≤3）给出 Deduction / Repair condition / Expected score movement；给出 score-change conditions 表。
- Multi-reviewer panel 3 角色独立成形 + synthesis 六要素；不强行制造分歧/夸奖（R1 的相对正面已明确限定在生物学描述层）。
- 未跑任何实验、未联网检索、未生成论文文本或 rebuttal、未修改任何已有项目文件（仅新建本报告）；与 I3 报告相互独立。

## Unresolved or unverified

- **零实验结果**：输入为 idea 卡片（任务约束），`evidence` 维度只评「证据计划的可行性与完整性」；文中所有「若能补 X 实验/若出现 Y 结果」均为**条件**，非既成事实；全文未编造任何结果、数值或引用。
- **URL 核验状态**：`https://arxiv.org/abs/2610.10023` 等 URL 由 `literature-baseline-matrix.md:8` 与 `execution-contract-v1.md:54-65` 标注为 2026-11-05 已核验的公开来源；本独立评审**未重新联网抓取**，作为输入事实引用（不声称独立复核）。
- **missing related work（status: unverified）**：cocoa / coconatfly、Nature 2024 跨连接组 cell typing、JEPA-on-connectome 等与 I4 的确切重叠未做公开检索（输入部分提供、不得编造引用），列为 M4 的未决风险；`:115-116`「第一次」优先声明亦未核验。
- **CVPR 2027 官方政策**：`venue-guides/cvpr.md:12-13` 为 2026 legacy、要求按当年官方页复核；页数/匿名/模板/desk 边界以 `https://cvpr.thecvf.com/Conferences/2027/CallForPapers` 为准，本评审未独立复核官方页；对「结构先验/图表示学习」类稿件的 desk 边界尤其不确定。
- **两图 motif 相关性**：`ideas/idea-cards.md:127-128` 冒烟未跑（Q3 判 NO-GO），「保守 motif 是否统计稳健」未验证。
- **硬件/对齐规模**：`hardware-profile.md:36` 标注 12GB 无法整图对齐需子图化，具体子图化方案卡片未给，未实测。
- **贡献量级阈值**：CVPR 2027 主会对「结构先验发现 + 架构迁移」类稿件的实际接受阈值无法从输入推定，采保守顶会口径并结合卡片自承（`:125,130`）判断。

## Output self-check

1. 章节顺序：Mode → Venue and assumptions → Paper summary → Likely stance and calibrated score → Quantitative scorecard → Top strengths → Major-fatal concerns → Writing and presentation concerns → Format-venue concerns → Multi-reviewer panel → Concern-to-action table → Recommended next CCFA owner → Checks run → Unresolved or unverified → Output self-check — 共 15 节，与契约一致 ✓
2. 所有表格 Markdown 分隔符有效、各行列数一致 ✓
3. 分数/confidence/建议内部一致：overall 2.8 < 6.5 且 3 条未解决 fatal、无窗口内修复路径 → 取 NO-GO 而非 REVISE/GO；front matter 与正文分数逐项一致 ✓
4. 列表平行语法、因果链（problem → reason → consequence → action）显式 ✓
5. 标点一致（中文全角，URL/路径/标识符/代码保留半角）✓
6. 无待填占位符、待办标记、空标题或填空符 ✓
7. 无「需要更多实验」类泛泛填充：每条 concern 均绑定 `文件:行号` 或已核验 URL ✓
8. 硬性要求核对：YAML front matter 字段严格（idea_id/overall/confidence/verdict/scores 六维/fatal_risks/go_conditions/review_execution）✓；每个 ≤3 分数含 Deduction/Repair/Expected movement ✓；panel ≥3 角色且 synthesis 含 Agreement/Disagreement/Decisive accept axis/Decisive reject axis/Unresolved evidence/Final calibrated stance ✓；明确回答 arXiv:2610.10023 增量（否，且更弱）+ 下位结论 ✓；冒烟 GO/NO-GO（NO-GO）+ 可证伪失败信号 ✓；未写 rebuttal / 未改 idea / 未生成论文文本 ✓；未编造结果/数值/引用 ✓；与 I3 报告相互独立 ✓
