---
idea_id: I6
overall: 5.1
confidence: 0.77
verdict: REVISE
scores: {novelty: 3, mechanism: 4, evidence_plan: 3, baselines: 4, cvpr_fit: 4, executability_11d: 2}
fatal_risks: ["全网格多种子空头支票：5×3×2×2=60 格且 cogstim 8 类任务+时序扩展使任务维度远超 2，乘多种子后与执行契约单次≤15分钟冒烟预算及 hardware-profile 整图 BPTT 红线冲突，排名稳定性/复现方差/交互效应等核心卖点无法在 12GB 单卡 11 天内兑现", "若坚持全量独立主会投稿、不先跑 2×2×1 成本外推冒烟、不据实重定义规模与种子数，则该 fatal 不解除，verdict 由 REVISE 转 NO-GO"]
go_conditions: ["先跑 2×2×1 四格各 30 步的成本外推冒烟，记录真实单格耗时/峰值显存/是否 OOM，据此判断 11 天内可完成的网格规模与种子数", "据冒烟实测预注册主假设、判定阈值与统计检验方法（交互效应量/排名稳定性/复现方差口径 + 种子数 + 95% CI），消除可证伪循环", "诚实降级为 mini-benchmark 或 I1 系统附表，撤回需全网格多种子支撑的『首个受控基准 / 排名稳定性 / 复现方差』主张", "补 CVPR 2026 强近期基线（SpikeTrack/TAPFormer）、等参数量 ANN 上界与连接组模型对照点，并明确框架价值超出 train-your-fly 自带 sweep 之处", "澄清『2 类任务』与『cogstim 8 类任务+时序扩展』的维度矛盾，固定网格口径"]
review_execution: independent-agent
---

# Mode

- Review mode: `scientific`（`ccf-paper-reviewer` 标准科学评审，顶会主会级，非 writing/full 模式）。
- Review execution: `independent-agent`——未参考任何其他 agent 的评审结论，独立依据冻结输入判定；与 I5 评审相互独立。
- 输入性质：**idea 卡片，不是论文，没有任何实验结果**。evidence 维度评「证据计划的可行性与完整性」，不把计划/外推写成已观测结论，不编造实验结果、数值或引用。本报告中的算力数字均为**基于卡片字面维度与硬件约束的外推估算**，明确标注为估算而非实测。
- 评审对象：I6 — ConnectomeBench（*ConnectomeBench: A Controlled Benchmark of Topology, Neural Dynamics and Efficiency in Connectome-Constrained Vision*）。
- 隐私边界：冻结输入视为私有用户数据；仅引用输入内已核验来源与任务明确给出的 URL，不做扩展公开检索。

# Venue and assumptions

- 目标：CVPR 2027 **主会**（CVPR-ICCV-ECCV 家族），按 `venue-review-styles.md` 行 60-69 评审：novelty、technical quality、empirical validation、visual evidence、clarity、fair comparison；要求强近期基线、消融、跨数据集、鲁棒性、公平协议。**不用期刊 Q2 标准放水**。
- 时间线（`execution-contract-v1.md` 第 4 节，源 https://cvpr.thecvf.com/Conferences/2027/CallForPapers 访问 2026-11-05）：Registration 2026-11-10 AOE、Submission 2026-11-16 AOE、Supplementary 2026-11-23；当前 2026-11-05，**仅剩 11 天**。
- CFP 主题（任务说明 + `idea-cards.md` I6 行 169-170）：Datasets and Benchmarks / Efficient and scalable vision / AI for Science。I6 自定位为 dataset/benchmark + 系统性归因，直接命中前三个主题；大方向锁定 GNN + SNN + 果蝇连接组 + 视觉。
- Contemporaneous 规则（`prior-art-dedup-log.md` 行 18-21、`execution-contract-v1.md` 行 40-41）：2026-09-15 之后上线论文须引用讨论，高度相似加审；arXiv:2610.10023（2026-10-08）落入此窗口；MaleCNS v1.0（2026-09，`idea-cards.md` I6 行 161）亦属窗口内。
- 硬件/运行信封（`hardware-profile.md`、`execution-contract-v1.md` 第 5 节）：RTX 3060 12 GB、`dyg-cold`（torch 2.11+cu128 / PyG 2.8.0.post1 / spikingjelly）；冒烟预算单次 ≤15 分钟 GPU、显存 ≤10 GB、下载 ≤1.5 GB、不做完整训练/多种子大实验；禁止伪造结果或把预测写成观测。
- 竞争工作：`train-your-fly` / arXiv:2610.10023（https://arxiv.org/abs/2610.10023，无状态 GNN 视觉分类 + 4 种随机图等布线预算对照，**已含 `benchmark_speed.py` 与 sweep**，任务说明）；arXiv:2609.01330（NeurIPS 2025）；Nature 2024 flyvis；BrainTrace / BioReservoir / JEPA-on-connectome；CVPR 2026 SpikeTrack（https://arxiv.org/abs/2602.23963）、TAPFormer（https://arxiv.org/abs/2603.04989）（`literature-baseline-matrix.md` 行 16-17）。
- 特别假设（任务强制）：I6 必须评估「12GB 单卡上全网格多种子实验是否可能」，**不能接受空头支票**。所有 idea 必须回答：相对 arXiv:2610.10023 的增量是否足以撑起 CVPR 主会。

# Paper summary

- 一段概述：I6 主张不抢方法新颖性，而提供一个受控比较框架——5 种图 × 3 种动力学（无状态/LIF/ALIF）× 2 类任务（静态/时序）× 2 个预算轴（wiring cost/synaptic ops）的可复现网格，统一数据、split、seed、读出与统计检验，输出交互效应与排名稳定性，负结果同样有效；定位为 CVPR 2027 Datasets and Benchmarks 投稿。
- Claimed problem（`idea-cards.md` I6 行 161-163）：「MaleCNS（2026-09）与 FlyWire 刚齐备，社区却缺少统一对照……`train-your-fly` 只覆盖了 {生物图, 4 随机图} × 无状态 GNN × wiring cost 这一格」。
- Claimed gap：不同论文用不同图/动力学/任务/指标，导致「生物接线到底值多少」无法比较。
- Method / contribution map（行 164-170）：机制明确标注「基准不是方法」；贡献类型 = dataset/benchmark + 系统性归因；对应 CFP 三主题。
- Evidence package（计划，非结果）：网格设计、统一协议、主指标（等预算 accuracy、交互效应量、排名稳定性、复现方差）与次指标（spike rate、显存、吞吐）（行 171-172）；强基线（行 173）；最小冒烟 = 跑 2×2×1 四格各 30 步、估单格耗时与显存、外推全网格成本、判断 11 天可行性（行 176-177）。**无任何已观测实验数据、无单格耗时/显存实测**。
- Stated limitations（行 174-180，卡片自陈）：「必须证明网格规模与多种子统计在本地 12 GB GPU 上可完成，否则是空头支票」；「benchmark 论文需要大量算力与多种子；11 天内全网格几乎不可能；但可以作为 I1 的副产品先交付一个 mini-benchmark」；「11 天可投性：低（全量）；中（作为 I1 附表）」。

# Likely stance and calibrated score

- Expected outcome / Likely stance: **REVISE**（borderline，`calibration-and-rank.md` 的 5 分区：框架方向真实契合 CFP 且差异化成立，但存在一条可通过重定义范围解除的 fatal 风险——全网格多种子算力空头支票）。**不是 GO**：overall 5.1 < 6.5，且 fatal 未解除。
- Overall: **5.1 / 10**；Confidence: **0.77**（新颖性/定位/证据计划判断可核验度高；但算力可行性为外推估算、缺单格实测，故置信度低于 I5 的 0.83，不因「无实验结果」自动压低）。
- Main accept signal: 直接命中 CVPR 2027 三个 CFP 主题；相对 2610.10023 的差异化是结构性（跨图/跨动力学/跨任务/跨预算）而非换数据集；证据计划含统一协议、交互效应、排名稳定性、负结果有效，并**专门设计了成本外推冒烟实验**（行 176-177）来预先验证可行性。
- Main reject signal: 全网格多种子在 12GB/11 天不可行（行 175、178-180 自陈 + 硬件/契约红线），若以全量形态投稿则核心卖点（统计严谨/排名稳定性/复现方差）无法兑现，正是任务禁止的空头支票；此外无新数据贡献、可证伪表述循环（行 167-168）、与 2610.10023 自带 sweep 的界限未划清。
- Calibration band: CSPaper 风格「average / borderline」，为近似判断、非官方 cutoff；升到「above average」需冒烟外推通过 + 预注册统计 + 补强基线 + 明确超出 sweep 的洞察。不声称接收概率。
- REVISE 的精确定义：fatal 风险（C1）存在**但有明确、可执行的解除路径**——先跑成本外推冒烟、据实重定义网格规模与种子数、诚实降级为 mini-benchmark/I1 附表、预注册统计协议。**若坚持全量独立主会投稿且不缩范围，本评审转为 NO-GO**。GO 在当前 11 天窗口对 I6 不成立。

## 相对 arXiv:2610.10023 的增量判定（明确回答）

**结论：框架方向有真实增量，但在当前 11 天 + 12GB 约束下不足以撑起一篇独立 CVPR 主会 benchmark 论文。** 依据：
1. 增量本身成立且非 incremental：`train-your-fly`（https://arxiv.org/abs/2610.10023）只覆盖「{生物图, 4 随机图} × 无状态 GNN × wiring cost」一格（`idea-cards.md` I6 行 163），I6 把其原配置降为「基准的一个单元格」（行 173），扩展到跨图（FlyWire + MaleCNS）、跨动力学（无状态/LIF/ALIF）、跨任务（静态/时序）、跨预算（wiring cost/synaptic ops）并输出交互效应与排名稳定性（行 164-166）。这契合 `prior-art-dedup-log.md` 行 11 允许的差异轴（时间维度、能效轴、新任务族、机制级交互归因），不属于行 21 警告的「同一模型 + 换数据集」。
2. 但 benchmark 论文的接受度完全依赖**统计充分性的兑现**：核心卖点是「统一协议 + 交互效应量 + 排名稳定性 + 复现方差」（行 166、171），这些需要全网格 × 多种子才能成立。在 12GB 单卡、11 天、单次 ≤15 分钟冒烟预算（`execution-contract-v1.md` 行 51-52）下无法兑现（详见 C1 外推），核心卖点即塌为空头支票。
3. 存活形态（卡片自陈的 mini-benchmark / I1 附表，行 179-180）退化为另一篇论文的附表，不再是「独立撑起主会」的贡献；且无新数据、未承诺具体社区洞察、还需证明框架价值超出 2610.10023 自带的 `benchmark_speed.py` 与 sweep。
4. 综合：作为「想法」值得进入筛选下一轮；作为「11-16 前独立主会全文」= 不可行。故 REVISE（缩范围重定义）而非 GO，坚持全量则 NO-GO。

## 若只有部分正向结果：诚实可发表的下位结论（明确回答）

- 若只跑通 2×2×1 或缩网格、单/少种子：诚实结论只能是一个受限的 pilot / negative result——「在 cogstim 单一任务 + 视叶子图 + T=8 + 有限种子下，{生物图, 度匹配随机图} × {无状态, LIF} 的等预算 accuracy 在 95% CI 内排序不稳定 / 未观察到显著的结构×动力学交互」，并**明确标注为 pilot，不足以支持跨图/跨任务/跨预算的排名稳定性结论**。可作为 I1 论文的系统性附表、或 workshop / benchmark-in-the-wild 短文；不得声称「首个受控基准」「排名稳定性」「复现方差」这些需全网格多种子支撑的主张，也不得外推到 8 类任务。
- 若冒烟外推显示全网格在预算内可行（低概率）：才可能升级为主会 benchmark，但仍需补新评测协议或明确社区会采用的具体洞察，并与 2610.10023 的 sweep 划清界限。
- 诚实边界：`idea-cards.md` I6 行 167-168 称「结构×动力学无交互……这本身是可发表结论」——负结果有效是好立场，但下位结论必须预注册判定阈值，否则「有交互/无交互都算贡献」会削弱可发表结论的科学严谨度（见 C2）。

# Quantitative scorecard

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|:---|:---:|:---:|:---|:---|
| Novelty | 3 | 4 | I6 行 161-175（框架差异化、把 2610.10023 降为一格）；`prior-art-dedup-log.md` 行 11、21；任务说明 2610.10023 自带 sweep | 结构性差异化真实但属增量式框架、无新数据；详见下方明细 |
| Mechanism | 4 | 4 | I6 行 164-168（网格、统一协议、交互效应、负结果有效）、行 176-177（成本外推冒烟） | 设计清晰；扣分点为可证伪循环与统计口径未定，见下方 score-change |
| Evidence plan | 3 | 3 | I6 行 166、171-172（交互效应量/排名稳定性/复现方差）、行 176-177（冒烟外推） | 计划较完整但统计充分性（多种子）在 12GB/11 天未证明；详见下方明细 |
| Baselines | 4 | 4 | I6 行 173（train-your-fly 一格、4 随机图、ANN/LIF）；`literature-baseline-matrix.md` 行 16-17、31 | 覆盖合理但缺 CVPR 2026 强近期基线与等参数量上界；见 score-change |
| CVPR fit | 4 | 4 | I6 行 169-170（CFP 三主题）；`venue-review-styles.md` 行 60-69；`execution-contract-v1.md` 行 42-43 | 主题直击；扣分点为无新数据、未承诺社区洞察、缺定性/failure 视觉证据；见 score-change |
| Executability (11d) | 2 | 4 | I6 行 164-166（60 格）、行 171-172（8 类任务）、行 175、178-180（自陈）；`hardware-profile.md` 行 36-40；`execution-contract-v1.md` 行 51-52、37-41 | 全网格多种子与 12GB/11 天/冒烟预算冲突；详见下方明细 |

**Overall:** 5.1 / 10  | **Scholarly Confidence:** 4/5（对应 front matter 0.77；算力项为外推，故低于满分）
**Recommendation:** borderline（lean 需先解除 fatal）  | **Verdict:** REVISE；坚持全量独立主会投稿则转 NO-GO

## 低分维度（≤3）扣分与修复明细（每个含 Deduction / Repair condition / Expected score movement）

```text
Dimension: Novelty
Score: 3
Confidence: 4
Evidence basis: idea-cards.md I6 行 161-163（train-your-fly 只覆盖一格）、行 164-166（跨图/动力学/任务/预算网格）、行 173（把 2610.10023 降为一个单元格）、行 174-175（不与 P1-P4 抢方法新颖性）；prior-art-dedup-log.md 行 11 允许差异轴、行 21 incremental 判定；literature-baseline-matrix.md 全表显示 cogstim/MaleCNS/FlyWire 均为已有数据；任务说明 2610.10023 已含 benchmark_speed.py 与 sweep。
Deduction: 差异化是结构性的、真实成立，但贡献单元是「统一协议 + 系统性归因」而非新数据/新标注/新组件，属增量式框架；数据全部现成（dataset-access-log.md 全 PASS 但均为既有资源），且与 2610.10023 自带 sweep 的界限未在卡片中划清（行 174-175 仅笼统称「提供受控比较框架」），novelty 需更锐利定位（rubric 第 1 维 3/5）。
Repair condition: 明确写出框架价值超出一个 sweep 脚本之处（如跨连接组 MaleCNS↔FlyWire 对齐、双预算轴联合控制、预注册交互检验），并给出社区会采用的具体评测协议或洞察。
Expected score movement: 维度 +0.5 to +1（至 3.5-4）若定位收紧；overall +0.3 to +0.5，仍不足以 GO。

Dimension: Evidence plan
Score: 3
Confidence: 3
Evidence basis: idea-cards.md I6 行 166（统一数据/split/seed/读出与统计检验、交互效应与排名稳定性、负结果有效）、行 171-172（主指标含交互效应量/排名稳定性/复现方差）、行 176-177（2×2×1 成本外推冒烟）；dataset-access-log.md 行 35（主指标含 95% CI）。
Deduction: 计划是两 idea 中较完整的（统一协议 + 负结果有效 + 专门的可行性外推冒烟），但核心统计主张所需的种子数、统计检验方法、置信区间口径、单格耗时/显存实测均未给出；「排名稳定性/复现方差」在计划层面仍是承诺而非可执行协议，且其可行性被 executability 维度否决（C1）。属「计划支撑部分故事但暴露核心主张」。
Repair condition: 先跑行 176-177 的成本外推冒烟，据实测固定种子数与网格规模；预注册主假设、判定阈值、统计检验方法与 95% CI 口径；把「交互效应量」的统计模型（如双因素 ANOVA/混合效应）具体化。
Expected score movement: 维度 +0.5 to +1（至 3.5-4）若冒烟外推通过且统计协议预注册；overall +0.3 to +0.5。

Dimension: Executability (11d)
Score: 2
Confidence: 4
Evidence basis: idea-cards.md I6 行 164-166（5 图 × 3 动力学 × 2 任务 × 2 预算轴 = 60 格）、行 171-172（cogstim 8 类任务 + 时序扩展）、行 175（自陈「必须证明…否则是空头支票」）、行 178-180（「11 天内全网格几乎不可能 / 低（全量）」）；hardware-profile.md 行 36-37（整图 BPTT 不可能、须子图化/T=8~16/小 batch）、行 39-40（官方 pin torch 2.6/PyG 2.6 与本机 2.11/2.8 兼容性未验证、缺 torch_sparse）；execution-contract-v1.md 行 51-52（单次 ≤15 分钟、不做完整训练/多种子大实验）、行 37-41（11-10 注册 / 11-16 全文 / 11 天）；dataset-access-log.md 行 33（每类 5000/5000/5000）。
Deduction: 外推估算（非实测）：60 格 × 多种子（排名稳定性/复现方差需 ≥3-5 seeds，卡片未声明）= 180-300 次训练；若按行 171 的 8 类任务展开（5×3×8×2 = 240 格）则更多。每次为连接组 LIF/ALIF BPTT，12GB 下 ALIF+适应状态可能单格即 OOM；整图不可、须子图化；冒烟预算明确「不做完整训练/多种子大实验」，与交付全网格多种子 benchmark 直接冲突；官方代码本机兼容性未验证；11 天含注册与全文截止。卡片自陈「几乎不可能」。→ 全量独立主会投稿不可行，核心卖点不兑现（空头支票）。
Repair condition: 跑 2×2×1 四格各 30 步的成本外推冒烟，记录真实单格耗时/峰值显存/是否 OOM；据实测把网格重定义为 11 天内可完成的规模与种子数，诚实降级为 mini-benchmark / I1 附表，并撤回需全网格支撑的主张。
Expected score movement: 维度 +1 to +2（至 3-4）仅在冒烟外推显示缩规模网格可在预算内完成、且作者接受降级时；overall +0.6 to +1.0（至 5.7-6.1，仍 <6.5，不构成 GO）。若冒烟外推失败或拒绝缩范围，维度维持 2、verdict 转 NO-GO。
```

## Score-change conditions

| Change | Condition | Likely affected dimensions | Expected movement |
| --- | --- | --- | --- |
| Raise score | 2×2×1 成本外推冒烟显示缩规模网格 + 多种子可在 12GB/11 天完成；预注册统计协议；补 CVPR 2026 强基线；明确超出 2610.10023 sweep 的洞察；澄清任务维度矛盾 | Executability (11d), Evidence plan, Novelty, Baselines | overall +0.6 to +1.0（至 5.7-6.1，borderline 上沿，仍非 GO） |
| Lower score | 冒烟外推显示单格 >10GB/OOM 或全网格 GPU 时长超出 11 天窗口；或坚持全量独立投稿不缩范围 | Executability (11d), Evidence plan | overall -0.5 to -1.0（至 4.1-4.6）或触发 fatal → NO-GO |
| No quick change | 无新数据贡献、可证伪循环需预注册、与 2610.10023 sweep 的界限需新协议 | Novelty, Mechanism, CVPR fit | 11 天内 unlikely；靠重定义而非补实验 |

# Top strengths

- **venue fit 直击 CFP**：贡献类型明确对应 CVPR 2027「Datasets and Benchmarks / Efficient and scalable vision / AI for Science」（`idea-cards.md` I6 行 169-170），且大方向锁定符合 `execution-contract-v1.md` 行 42-43；「负结果同样有效」（行 166）契合 benchmark track 口味。
- **相对 2610.10023 的差异化是结构性的**：把 `train-your-fly` 原配置降为「基准的一个单元格」（行 173），扩展到跨图/跨动力学/跨任务/跨预算网格（行 164-166），契合 `prior-art-dedup-log.md` 行 11 允许的差异轴，规避行 21 的 incremental 判定。
- **证据计划是两 idea 中较完整的，且自带可行性自检**：统一数据/split/seed/读出与统计检验、交互效应量/排名稳定性/复现方差、负结果有效（行 166、171），并专门设计「跑 2×2×1 四格各 30 步 → 估单格耗时与显存 → 外推全网格成本 → 判断 11 天可行性」的冒烟（行 176-177）——这正是任务要求的「不能接受空头支票」的自检机制。
- **定位诚实**：卡片自陈「必须证明网格规模与多种子统计在本地 12 GB GPU 上可完成，否则是空头支票」（行 175）与「11 天内全网格几乎不可能 / 低（全量）；中（作为 I1 附表）」（行 178-180），主动暴露致命风险而非过度承诺（`review-output-standards.md` 对 limitation honesty 的正面信号）。以上为真实优势，不据此掩盖 C1。

# Major-fatal concerns

- **C1 · Severity: fatal · 全网格多种子在 12GB 单卡 / 11 天不可行（空头支票）**
  - Concern: 以「独立、全量、多种子 ConnectomeBench 主会投稿」形态，核心卖点（统计严谨、排名稳定性、复现方差、交互效应）无法在硬件/时间/预算内兑现。
  - Evidence basis: `idea-cards.md` I6 行 164-166（5×3×2×2=60 格）、行 171-172（cogstim 8 类任务 + 时序扩展使任务维度远超 2）、行 166/171（排名稳定性/复现方差/交互效应量 → 需多种子，卡片未声明种子数）、行 175/178-180（自陈「几乎不可能 / 低（全量）」「否则是空头支票」）；`hardware-profile.md` 行 36-37（整图 BPTT 不可能、须子图化/T=8~16/小 batch）、行 39-40（官方 pin torch 2.6/PyG 2.6 与本机 2.11/2.8 需兼容性验证、缺 torch_sparse）；`execution-contract-v1.md` 行 51-52（单次 ≤15 分钟、不做完整训练/多种子大实验）、行 37-41（11-10 注册 / 11-16 全文 / 11 天）；`dataset-access-log.md` 行 33（每类 5000/5000/5000）；`literature-baseline-matrix.md` 行 8（must-rerun 兼容性）。
  - Reviewer deduction: 外推估算（非实测）：60 格 × ≥3-5 seeds = 180-300 次训练，8 类任务展开则更多；每次 LIF/ALIF BPTT 在 12GB 下可能单格 OOM；冒烟预算明确排除完整训练/多种子大实验，与交付全网格 benchmark 直接冲突。benchmark 论文的可信度恰依赖统计充分性，兑现不了即核心贡献塌为空头支票（`universal-review-rubric.md` fatal triage「study design / evaluation protocol 无效」「paper 对 claim type 不可复现」）。
  - Required fix: 先跑行 176-177 的成本外推冒烟，据实测重定义网格规模与种子数，诚实降级为 mini-benchmark / I1 附表并撤回全网格主张；否则转 NO-GO。
- **C2 · Severity: major · 可证伪性循环，主假设未预注册**
  - Concern: 「有交互 → 可发表；无交互 → 也可发表」使框架无论结果都「有贡献」，削弱科学严谨度。
  - Evidence basis: `idea-cards.md` I6 行 167-168「若所有组合排序稳定、结构×动力学无交互，则『生物接线有特权』这一说法被削弱——这本身是可发表结论」；行 166「负结果同样有效」。
  - Reviewer deduction: 主假设、判定阈值、统计检验方法未预注册，交互效应量/排名稳定性易被 post-hoc 解释；benchmark 类工作须预先固定主指标与阈值（`review-output-standards.md` 定量反馈、`reviewer-panel.md` 统计严谨 lens）。
  - Required fix: 预注册主假设、交互显著性阈值、统计检验与 95% CI 口径。
- **C3 · Severity: major · 无新数据贡献，与 2610.10023 自带 sweep 的界限未划清**
  - Concern: 数据全部现成，且竞争工作已有 `benchmark_speed.py` 与 sweep，框架价值需证明超出「把 sweep 表格做大」。
  - Evidence basis: `dataset-access-log.md` 全表（cogstim、FlyWire 图包、MaleCNS feather 均 PASS，但均为已有资源）；`idea-cards.md` I6 行 174-175（仅笼统称「提供受控比较框架」，未具体区分）；任务说明 https://arxiv.org/abs/2610.10023 已含 `benchmark_speed.py` 与 sweep；`venue-review-styles.md` 行 60-69（CVPR 要求与近期 CV 工作的清晰关系）。
  - Reviewer deduction: Datasets and Benchmarks 通常期待新数据/新标注/新协议 + 社区会采用的洞察；I6 未承诺具体正向洞察，novelty 停留在增量式框架。
  - Required fix: 明确框架超出 sweep 之处（跨连接组对齐、双预算轴联合控制、预注册交互检验），并给出社区会采用的协议。
- **C4 · Severity: moderate · 任务维度自相矛盾，网格口径不自洽**
  - Concern: 「2 类任务」与「cogstim 8 类任务 + 时序扩展」冲突，导致网格规模与算力估算不可复核。
  - Evidence basis: `idea-cards.md` I6 行 164-166（「2 类任务（静态 / 时序）」）vs 行 171-172（「cogstim 8 类任务 + 时序扩展」）。
  - Reviewer deduction: 预算外推的分母不确定，C1 的可行性判断无法被精确审计。
  - Required fix: 固定网格口径，明确 2 类任务是「任务族」还是「任务实例」。
- **C5 · Severity: moderate · 强基线清单缺 CVPR 2026 近期基线与上界**
  - Concern: `train-your-fly` 一格 + 4 随机图 + ANN/LIF 不足以覆盖 CVPR 主会要求的强近期基线。
  - Evidence basis: `idea-cards.md` I6 行 173；`literature-baseline-matrix.md` 行 16-17（SpikeTrack https://arxiv.org/abs/2602.23963、TAPFormer https://arxiv.org/abs/2603.04989 为 strong recent SNN baseline）、行 31「不可仅与 ANN toy baseline 比较：CVPR 主会评审不会接受」、行 10/15（flyvis / BrainTrace 可作框架对照点）。
  - Reviewer deduction: 对 benchmark 论文，基线全景是可信度前提；缺等参数量 ANN 上界与其他连接组模型对照点。
  - Required fix: 补 CVPR 2026 强近期基线、等参数量 ANN 上界与连接组模型对照点。
- **C6 · Severity: moderate · 统计协议未定**
  - Concern: 主指标「交互效应量 / 排名稳定性 / 复现方差」（行 171）未给统计检验方法、种子数、置信区间口径。
  - Evidence basis: `idea-cards.md` I6 行 166、171-172；`dataset-access-log.md` 行 35（主指标含 95% CI 为标准口径）。
  - Reviewer deduction: benchmark 的这些统计量是必需件，计划层面仍是承诺（呼应 C1/C2）。
  - Required fix: 指定统计模型（如双因素 ANOVA / 混合效应）、种子数、95% CI 与排名稳定性度量。

# Writing and presentation concerns

- 「机制（基准不是方法）」（`idea-cards.md` I6 行 164）是好的澄清，但标题中 *Topology, Neural Dynamics and Efficiency* 的「Efficiency」未在机制里定义为独立维度：行 164-166 的两个预算轴（wiring cost / synaptic ops）与行 172 次指标（显存/吞吐）与「Efficiency」的对应关系需显式化，否则术语松散。
- 「负结果同样有效」（行 166）是好立场，但与行 167-168「这本身是可发表结论」连读，易被读成「无论结果都算贡献」；claim-evidence 呈现需收紧并预注册阈值（呼应 C2）。`universal-review-rubric.md` hard rule：不得靠修辞强化无证据支撑的主张。
- 行 164-166「2 类任务」与行 171-172「cogstim 8 类任务 + 时序扩展」数字/术语不一致（C4），转成论文表格后必暴露（`review-output-standards.md` 输出质量门第 6 点）。
- 边界说明：以上是 **idea 卡片** 表述，不是已存在论文的章节；本节评的是「若照此写成论文会暴露的呈现风险」，未把卡片当论文文本评审，未生成任何论文文本。

# Format-venue concerns

- CVPR Datasets and Benchmarks 期待新数据/新标注/新协议 + 社区会采用的洞察 + 强基线全景；I6 无新数据（C3）。`venue-review-styles.md` 行 66-68 要求 cross-dataset tests、robustness、failure analysis——I6 有跨图/跨任务设计，但缺定性 failure-case 视觉证据。
- Contemporaneous 引用义务：arXiv:2610.10023（2026-10-08，https://arxiv.org/abs/2610.10023）与 MaleCNS v1.0（2026-09，行 161）须诚实引用讨论（`execution-contract-v1.md` 行 40-41）。
- 时间线：Registration 11-10、Submission 11-16 AOE、Supplementary 11-23（`execution-contract-v1.md` 行 37-38）；benchmark 论文常把大规模表格放 supp，但 supp 也在 11-23，不解决 11 天算力。
- Desk-reject 风险：低-中。主题兼容（`desk-checks.md` topic compatibility = pass），但纯 benchmark 若不能兑现统计充分性，主会评审会质疑「不是完整 benchmark」（minimum quality = uncertain，因无实验、无单格实测）。
- 不写 rebuttal、不修改 idea、不生成论文文本（任务硬性约束与 `ccf-paper-reviewer` Core Rule）。

# Multi-reviewer panel

```text
Reviewer: SNN 训练专家
Lens: LIF/ALIF BPTT 在 12GB 的可行性、surrogate gradient、显存峰值、版本兼容性
Score tendency: lean reject（约 4/10）
Confidence: 0.70
Main positive signal: 网格把「动力学」作为显式轴（无状态/LIF/ALIF，行 164-166）且统一 seed（行 166），利于可复现对比；行 176-177 的成本外推冒烟正是先测显存/耗时再决定是否扩大规模。
Main negative signal: ALIF + BPTT 在 T=8~16 视叶子图上显存/稳定性未经实测，hardware-profile.md 行 36-37 已警告整图不可能、行 39-40 兼容性未验证；60 格 × 多种子的训练量在 11 天不现实（行 178-180 自陈）。
Evidence basis: idea-cards.md I6 行 164-166、176-180；hardware-profile.md 行 36-40；execution-contract-v1.md 行 51-52。
Score-change condition: 若 2×2×1 冒烟实测 4 格峰值显存均 ≤10GB、单格 30 步稳定且外推总时长落在 11 天窗口内 → executability 与 evidence_plan 上调，overall 上调；若出现 OOM 或超窗 → 下调并转 NO-GO。

Reviewer: benchmark / 评测专家
Lens: 统计充分性、多种子、排名稳定性、预注册、可证伪性
Score tendency: borderline（约 5/10）
Confidence: 0.75
Main positive signal: 统一数据/split/seed/读出与统计检验 + 交互效应量/排名稳定性/复现方差 + 负结果有效 + 专门的成本外推冒烟（行 166、171-172、176-177），是两 idea 中最完整的证据计划。
Main negative signal: 种子数/统计检验方法/95% CI 口径未定（行 171）、可证伪表述循环（行 167-168）、全网格多种子不可行（C1）；「排名稳定性/复现方差」在计划层面是承诺而非可执行协议。
Evidence basis: idea-cards.md I6 行 166-168、171-172、176-180；dataset-access-log.md 行 35。
Score-change condition: 预注册主假设+阈值+统计检验、据冒烟实测固定种子数与网格规模 → evidence_plan 上调至 3.5-4；若坚持全量不缩 → 下调/NO-GO。

Reviewer: CV 顶会架构 / venue-fit 专家
Lens: CVPR 主会 bar、Datasets & Benchmarks、视觉证据、强近期基线
Score tendency: borderline-positive（约 5.5/10）
Confidence: 0.70
Main positive signal: 直击 CFP 三主题（行 169-170）、把 2610.10023 降为单元格（行 173）、跨图/跨预算设计（行 164-166）、负结果有效（行 166）——主题契合度是本轮最高。
Main negative signal: 无新数据（dataset-access-log.md 全为既有资源）、缺 CVPR 2026 强基线 SpikeTrack/TAPFormer（literature-baseline-matrix.md 行 16-17）、缺定性/failure 视觉证据、与 2610.10023 自带 sweep 界限不清（行 174-175）。
Evidence basis: idea-cards.md I6 行 164-175；venue-review-styles.md 行 60-69；literature-baseline-matrix.md 行 16-17、31；prior-art-dedup-log.md 行 21。
Score-change condition: 补强近期基线 + 明确框架超出 sweep 的洞察/新协议 + 补 failure 视觉证据 → cvpr_fit/baselines 上调，overall 上调。

Reviewer: novelty / positioning 专家
Lens: 相对 arXiv:2610.10023 与 contemporaneous 工作的增量、是否 incremental
Score tendency: borderline（约 5/10）
Confidence: 0.80
Main positive signal: 差异化轴（跨图 MaleCNS+FlyWire / 跨动力学 / 跨任务 / 跨预算）是结构性而非换数据集，符合 prior-art-dedup-log.md 行 11 允许差异轴、不触发行 21 的 incremental 判定；把竞争工作纳入框架作为一格（行 173）是诚实定位。
Main negative signal: 数据全现成、无新贡献单元、未承诺具体社区洞察；2610.10023 已含 benchmark_speed.py 与 sweep，框架价值需证明；cards 行 174-175 未具体划界。
Evidence basis: idea-cards.md I6 行 161-175；prior-art-dedup-log.md 行 11、18-21；literature-baseline-matrix.md 行 8、22；https://arxiv.org/abs/2610.10023。
Score-change condition: 产出社区会采用的具体洞察或新评测协议、划清与 sweep 的界限 → novelty 上调至 3.5-4。

Panel synthesis:
Agreement: 四位评审一致认为「框架方向真实契合 CFP、相对 2610.10023 的差异化结构性成立（非换数据集）」，且一致认为「全量多种子算力是当前不可绕过的瓶颈」；一致认为「先跑成本外推冒烟」是决定 verdict 的必要下一步。
Disagreement: venue-fit 专家给分最高（约 5.5，主题价值权重高），SNN 训练专家给分最低（约 4，硬件兑现权重高）；这不是强行制造，而是 lens 不同且双方证据都指向卡片同一处（行 164-180）。另有一处真实张力：novelty 专家视「负结果有效」为诚实中立立场，评测专家视行 167-168 为可证伪性软肋——二者对同一句文本的评价不同，源于「定位价值」与「统计严谨」两套标准，非人为夸奖或贬低。
Decisive accept axis: 若 2×2×1 冒烟外推证明缩规模网格 + 多种子可在 12GB/11 天完成，并预注册统计协议、补 CVPR 2026 强基线、给出超出 2610.10023 sweep 的具体洞察 → 可升级为可讨论的主会 benchmark（overall 上限约 5.7-6.1，仍不构成 GO）。
Decisive reject axis: 若坚持全量独立主会投稿且不跑/跑不过成本外推冒烟 → 空头支票，核心卖点（统计严谨/排名稳定性/复现方差）不兑现 → NO-GO。
Unresolved evidence: 无任何冒烟实测（单格耗时/峰值显存/OOM）、种子数与统计检验方法未定、与 2610.10023 sweep 的具体差异未写、任务维度 2 vs 8 未澄清、官方与本机 torch-PyG 兼容性未验证。
Final calibrated stance: REVISE（overall 5.1, confidence 0.77）；fatal 风险 C1 经「先跑冒烟外推 → 据实重定义规模/种子 → 诚实降级 mini-benchmark/I1 附表 → 预注册统计」可解除；若拒绝缩范围则转 NO-GO。合成遵循「最强未解决关注点决定最终立场」，未把 C1 被主题契合度平均掉；GO 在当前 11 天窗口不成立。
```

# Concern-to-action table

| ID | Severity | Concern | Evidence basis | Affected criterion | Fix class | Required action | Owner skill | Score-change condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | fatal | 全网格多种子在 12GB/11 天不可行，核心卖点不兑现（空头支票） | idea-cards.md I6 行 164-166、171-172、175、178-180；hardware-profile.md 行 36-40；execution-contract-v1.md 行 37-41、51-52；dataset-access-log.md 行 33 | Executability (11d) / Evidence plan | reproducibility | 跑 2×2×1 成本外推冒烟，据实测重定义网格与种子数，降级 mini-benchmark/I1 附表并撤回全网格主张 | f-research-v1 | 外推通过且接受降级时 executability +1~+2、overall +0.6~+1.0；否则转 NO-GO |
| C2 | major | 可证伪性循环，主假设/阈值未预注册 | idea-cards.md I6 行 166、167-168 | Mechanism / Evidence plan | method/soundness | 预注册主假设、交互显著性阈值、统计检验与 95% CI 口径 | ccf-paper-writer | 预注册完成后 mechanism 维持 4、evidence_plan +0.5~+1 |
| C3 | major | 无新数据贡献，与 2610.10023 自带 sweep 界限未划清 | dataset-access-log.md 全表；idea-cards.md I6 行 174-175；https://arxiv.org/abs/2610.10023；venue-review-styles.md 行 60-69 | Novelty / Positioning | related-work | 明确框架超出 sweep 之处并给出社区会采用的协议或洞察 | ccf-paper-writer | 定位收紧后 novelty +0.5~+1 |
| C4 | moderate | 「2 类任务」vs「cogstim 8 类任务+时序扩展」维度矛盾 | idea-cards.md I6 行 164-166 vs 行 171-172 | Mechanism / Evidence plan | writing | 固定网格口径，明确任务族 vs 任务实例 | ccf-paper-writer | 口径固定后 C1 外推可复核，无直接分数移动 |
| C5 | moderate | 缺 CVPR 2026 强近期基线与等参数量上界 | idea-cards.md I6 行 173；literature-baseline-matrix.md 行 16-17、31 | Baselines | experiment | 补 SpikeTrack/TAPFormer、等参数量 ANN 上界与连接组模型对照点 | f-research-v1 | 补齐后 baselines 维持 4、overall +0.2~+0.3 |
| C6 | moderate | 交互效应量/排名稳定性/复现方差的统计协议未定 | idea-cards.md I6 行 166、171-172；dataset-access-log.md 行 35 | Evidence plan | experiment | 指定统计模型、种子数、95% CI 与排名稳定性度量 | f-research-v1 | 协议固定后 evidence_plan +0.5~+1 |

# Recommended next CCFA owner

- 下一责任方：`f-research-v1`（先执行行 176-177 的 2×2×1 成本外推冒烟、记录真实单格耗时/峰值显存/OOM、据实测设计缩规模网格与种子数、补强近期基线）与 `ccf-paper-writer`（重定义后的贡献定位、预注册主假设与统计口径、划清与 2610.10023 sweep 的界限）。
- Handoff: PARTIAL。本轮结论为 **REVISE**：不是可写论文状态，而是「先跑冒烟外推 → 据实重定义 → 诚实降级」的筛选动作；若冒烟外推失败或作者坚持全量独立主会投稿，则改判 NO-GO 并返回 idea-screening 循环另选候选（任务说明的原流程）。
- 不写 rebuttal（交 `ccf-rebuttal-writer` 的前提不成立）；不修改 idea 卡片；不生成论文文本。

## Minimum smoke-test decision（GO / NO-GO + 可证伪失败信号）

- 该 idea 的最小冒烟实验（「跑通网格中 2×2×1 的 4 个单元格各 30 步，估计单格耗时与显存，外推全网格成本，判断 11 天内是否可完成」，idea-cards.md I6 行 176-177）：**GO，值得跑**。
- 理由：该冒烟**直接命中 I6 唯一的致命风险 C1（算力空头支票）**，成本可控（4 格 × 30 步，符合 `execution-contract-v1.md` 行 51-52 的单次 ≤15 分钟 / ≤10GB / 不做完整训练），且其结果决定 verdict（外推通过 → REVISE 可升级；失败 → NO-GO）。它是决策相关的，与 I5 那种「只验代码跑通、不触及致命风险」的冒烟性质不同。
- 一个可证伪的失败信号：若 4 个单元格中任一在 T=8、batch=4、视叶子图（几千~几万节点）下峰值显存 >10 GB 或出现 OOM，或据单格 30 步实测外推的「60 格 × ≥3 seeds」总 GPU 时长明显超出 11 天剩余窗口（`execution-contract-v1.md` 行 51-52 的 ≤15 分钟/次封顶使该外推更易越界），则「全网格多种子 benchmark 在 12GB 单卡 / 11 天可完成」这一前提被证伪 → 必须降级为 mini-benchmark / I1 附表，或按 REVISE→NO-GO 处理。该信号是可测判定（显存数值 / 外推时长），而非泛泛「需要更多实验」。

# Checks run

- 已读：`ccf-paper-reviewer/SKILL.md`（经 Skill 加载）、`ccf-common/references/review-output-standards.md`、`references/universal-review-rubric.md`、`calibration-and-rank.md`、`reviewer-panel.md`、`venue-review-styles.md`、`review-workflow.md`、`fixed-output-format.md`、`desk-checks.md`；以及 6 个冻结输入（idea-cards.md、prior-art-dedup-log.md、literature-baseline-matrix.md、dataset-access-log.md、hardware-profile.md、execution-contract-v1.md）。
- 已做的审计：desk checks、contribution-novelty、claim-evidence（行 161-180 各主张）、evidence-plan 完整性与可行性（含 12GB 单卡全网格多种子的外推核算）、related-work positioning、reproducibility、calibration 一致性、panel 独立性、score-change 条件、输出质量门。
- 三遍阅读 + 对抗性 pass：novelty collapse、missing closest work、unsupported central claims、invalid study design、空头支票核查（任务强制项）。
- 算力核算为**基于卡片字面维度与硬件约束的外推估算，非实测**：60 格（5×3×2×2）、8 类任务展开更多、≥3-5 seeds、180-300 次训练量级；已在正文明确标注为估算，未写成观测结果。
- 未做新的公开网络检索：定位证据已由冻结的 `prior-art-dedup-log.md` 与 `literature-baseline-matrix.md`（访问 2026-11-05，已核验）提供；扩展检索会违反 `execution-contract-v1.md` 第 7 节「链接可追溯到本轮检索记录、不得编造」。仅引用输入内已核验 URL 与任务明确给出的 https://arxiv.org/abs/2610.10023。
- 未修改任何已有项目文件；仅新建本报告文件；与 I5 报告相互独立。

# Unresolved or unverified

- **无任何实验结果、单格耗时/显存实测、外推实测值**：输入是 idea 卡片；本报告算力数字为外推估算，未把估算写成观测，未编造任何结果。
- 种子数、统计检验方法、95% CI 口径、排名稳定性度量：卡片均未声明（行 166、171-172），属未验证。
- 官方 pin torch 2.6/PyG 2.6/torch-sparse 与本机 `dyg-cold` torch 2.11/PyG 2.8（缺 torch_sparse）兼容性未验证（`hardware-profile.md` 行 39-40）；`train-your-fly` must-rerun 可行性未实测。
- 「arXiv:2610.10023 含 `benchmark_speed.py` 与 sweep」来自任务说明与卡片共享底座描述，本轮未逐文件核验其仓库内容。
- `literature-baseline-matrix.md` 中标注「本轮未核验」的条目：arXiv:2609.01330 Has Code 直链（行 9）、Reiser Cell 2026 中文解读且未核验出版页（行 14）、BrainTrace 报道且未核验期刊页（行 15）、flyvis 响应数据（`dataset-access-log.md` 行 25）；JEPA-on-connectome 为未同行评审工作论文（行 22）。
- 任务维度「2 类任务」vs「8 类任务 + 时序扩展」矛盾未澄清，故 60 格仅为字面下限。
- CVPR 2027 注册/截止/contemporaneous 规则据 `execution-contract-v1.md`（访问 CFP 2026-11-05），本评审未重新访问 CFP 页面核验。

# Output self-check

- 章节顺序：Mode / Venue and assumptions / Paper summary / Likely stance and calibrated score / Quantitative scorecard / Top strengths / Major-fatal concerns / Writing and presentation concerns / Format-venue concerns / Multi-reviewer panel / Concern-to-action table / Recommended next CCFA owner / Checks run / Unresolved or unverified / Output self-check —— 与契约一致，无缺无增。
- YAML front matter：字段严格为 idea_id / overall（一位小数 5.1）/ confidence（两位小数 0.77）/ verdict（REVISE）/ scores 六维 / fatal_risks / go_conditions / review_execution，位于文件开头。
- 每个 ≤3 分数（novelty 3、evidence_plan 3、executability_11d 2）均写明 Deduction / Repair condition / Expected score movement（保守区间）；mechanism/baselines/cvpr_fit 为 4，在 scorecard 表与 score-change 表中给出依据与条件。
- 每个维度有可核验 evidence basis（卡片行号 / 去重日志 / 文献矩阵 / 硬件契约 / URL），未写「需要更多实验」式泛泛表述。
- Multi-reviewer panel：4 个角色（SNN 训练 / benchmark 评测 / CV 顶会架构 / novelty positioning），每人含 Lens / Score tendency / Confidence / Main positive signal / Main negative signal / Evidence basis / Score-change condition；Panel synthesis 含 Agreement / Disagreement / Decisive accept axis / Decisive reject axis / Unresolved evidence / Final calibrated stance；分歧来自真实 lens 权重差异，未强行制造或夸奖。
- Concern-to-action table：9 列，每行 9 个单元格，分隔符一致；每条 concern 绑定具体卡片句子或已核验 URL。
- 明确回答了「相对 arXiv:2610.10023 增量是否足以撑起 CVPR 主会」（框架增量真实但当前 11 天/12GB 下不足以撑起独立主会，四点依据）与「若只有部分正向结果的诚实下位结论」（受限 pilot/negative result 模板）。
- 明确给出最小冒烟实验 GO/NO-GO（GO + 理由）与一个可证伪失败信号（>10GB/OOM 或外推超 11 天窗口）。
- 严评了任务强制项「12GB 单卡全网格多种子是否可能、不能接受空头支票」：以外推核算判定不可行并列为 fatal（C1），verdict REVISE 附明确缩范围条件，坚持全量则 NO-GO。
- 不写 rebuttal、不修改 idea、不生成论文文本；未把计划/估算写成观测；未编造结果/数值/引用。
- Overall 5.1 < 6.5 且存在未解除 fatal → verdict REVISE（非 GO），与判定规则一致；confidence 0.77 与「算力为外推、缺实测」一致。
- 表格列数一致、无 TBD/TODO/空标题、中文标点统一、无占位符残留；与 I5 报告独立判定，未互相引用结论。
