---
idea_id: I3
overall: 5.2
confidence: 0.80
verdict: REVISE
scores: {novelty: 2, mechanism: 3, evidence_plan: 3, baselines: 3, cvpr_fit: 3, executability_11d: 4}
fatal_risks:
  - "核心 eye 模块（复眼 Voronoi+光谱通道+ON/OFF 双路+R7/R8 互抑制）已由 arXiv:2610.10023 实现且代码数据全公开；I3 增量仅为抽象成可插拔前端+换标准 CV 基准+脉冲预算曲线，属拆模块/换数据集，novelty 相对最强竞争坍塌"
  - "贡献量级 component-level、故事偏小：idea 卡片自承单独发 CVPR 主会偏轻、需至少 2 个下游 backbone+2 个数据集才算站住，而证据计划仅到单个 2 层 LIF+cogstim"
go_conditions:
  - "把贡献单元重构为 train-your-fly 未覆盖、可归因的机制结论（例：生物测量非均匀采样在等输入脉冲预算下、跨 backbone/数据集可复现的精度-资源增益），而非仅解耦移植"
  - "补齐 2×2 backbone×数据集证据矩阵、CVPR 级强基线（SOTA 事件/稀疏编码）、等脉冲数/等参数量公平协议、多种子与 95% CI、视觉 failure cases，并对 arXiv:2610.10023 做正面对比与引用讨论"
  - "冒烟实验一次性通过（含 torch/PyG/torch_sparse 兼容验证）并给出可分辨的几何增益信号；否则按 NO-GO 淘汰"
review_execution: independent-agent
---

# I3 独立评审报告 — Connectome-Measured Photoreceptor Geometry as a Plug-in Neuromorphic Vision Front-end

> 引用约定：下文 `文件名:行号` 均指向 `C:\code\phd-snn\auto-paper\20261105-204552\` 下的冻结输入文件；`references/` 指向 `ccf-paper-reviewer` 技能参考文件。所有 URL 均引自冻结输入中标注为 2026-11-05 已核验的来源，本独立评审未重新抓取、未编造。

## Mode

- 评审模式：`ccf-paper-reviewer` 的 **scientific（standard scientific 输出契约）**，独立单 agent 执行（`review_execution: independent-agent`）。
- 评审对象：**idea 卡片，不是论文**（`ideas/idea-cards.md:80-106`），零实验结果、零图表、零附录、无 Abstract/Intro/Conclusion 正文。
- 证据口径硬约束：`evidence` 维度评「**证据计划的可行性与完整性**」，不把计划写成已观测结果；全文不编造任何实验结果、数值或引用；所有分数为评审打分而非实验测量。
- 量纲：criterion 1-5；overall 1-10（一位小数）；front matter `confidence` 用 0-1（两位小数），正文同时给出 1-5 等价以便与 `calibration-and-rank.md` 对齐。
- 隐私边界：输入全部为本地冻结文件，未将私有文本用于任何联网查询；本轮未做公开检索（理由见 Unresolved or unverified）。

## Venue and assumptions

| 假设 | 来源 | 在本次判断中的效力 |
|:---|:---|:---|
| 目标 CVPR 2027 **主会**（CCF-A/顶会），不得用期刊 Q2 标准放水 | `execution-contract-v1.md:42`；`venue-review-styles.md:60-69`（CVPR 强调 novelty/技术质量/实证/视觉证据/公平比较） | 决定 reject 阈值；component-level 贡献按主会标准衡量 |
| 全文截止 2026-11-16 AOE、注册 11-10，当前 2026-11-05，**仅 11 天** | `execution-contract-v1.md:37-41`；`ideas/idea-cards.md:5`；`https://cvpr.thecvf.com/Conferences/2027/CallForPapers` | 决定 `executability_11d` 与证据计划可达性 |
| 大方向锁定 GNN + SNN + 果蝇连接组 + 视觉，不得漂到纯神经科学仿真或纯图表示学习 | `execution-contract-v1.md:43` | I3 仍含 SNN/LIF 与视觉基准，未硬漂移 |
| 本机仅 RTX 3060 12GB / 31.9GB RAM / `dyg-cold`（torch 2.11+cu128、PyG 2.8.0.post1、spikingjelly）；整图 BPTT 不可行，必须子图化 | `hardware-profile.md:26-41`；`execution-contract-v1.md:47-52` | 冒烟预算单次 ≤15min GPU、显存 ≤10GB、不做完整/多种子大实验 |
| `train-your-fly` 官方 torch 2.6/PyG 2.6/torch-sparse，本机缺 `torch_sparse`，**直接复现需兼容性验证** | `hardware-profile.md:38-40`；`literature-baseline-matrix.md:8` | I3 的 eye 数据依赖官方图包，是冒烟的前置风险 |
| 最强竞争 arXiv:2610.10023（2026-10-08）：复眼 Voronoi + FlyWire 全图无状态 GNN + 4 种随机图对照，代码/数据全公开，must-rerun | `https://arxiv.org/abs/2610.10023`；`literature-baseline-matrix.md:8`；`prior-art-dedup-log.md:11` | 决定 novelty 判断基准 |
| CVPR 2027 将 2026-09-15 后上线论文视为 **contemporaneous**：须引用讨论、高度相似会加审；「同一模型+换数据集」仍判 incremental | `prior-art-dedup-log.md:16-21`；`execution-contract-v1.md:40-41` | 直接约束 I3「解耦+换基准」这一增量 |
| flyvis（Nature 2024）、NeurIPS 2025 连接组+SNN 朝向图、BrainTrace/BioReservoir/MaleCNS X-ray 博客、cocoa/coconatfly 已占据朴素叙事 | `literature-baseline-matrix.md:9-22`；`prior-art-dedup-log.md:13-14` | 压缩「复眼/连接组+视觉」剩余新颖空间 |
| 输入为 idea 卡片，无任何实验结果；G6-G8/validation/handoff 保持 pending，不伪造 pass | `execution-contract-v1.md:28-33`；任务约束 | evidence 只评计划，不评结果 |

## Paper summary

I3 主张把 `train-your-fly`（arXiv:2610.10023）里与全脑 GNN 绑定的复眼模型，抽象为一个**与连接组图解耦、可插拔、通用**的脉冲视觉前端：从 FlyWire 光感受器位置投影、以 R7 为种子做非均匀 Voronoi 小眼划分，按光谱通道与 ON/OFF 双路做脉冲编码，等价替代手工事件编码 / patch embedding，参数量近乎为零（`ideas/idea-cards.md:82-91`）。贡献类型自定为「新的输入编码层 / 计算成像视角」（`:94`），任务为 CIFAR-10 / CIFAR10-DVS / cogstim `shapes`，主指标为等输入脉冲数下的 accuracy（`:95-96`）。

- **Claimed problem**：SNN/事件视觉把输入当规则网格 patch，忽略传感器几何（`:84-85`）。
- **Claimed gap**：`train-your-fly` 有复眼模型但「与全脑 GNN 死绑在一起，从未被当作通用、可插拔、与连接组图解耦的视觉前端在标准 CV 基准上验证」（`:86-87`，原句）。
- **Method / contribution map**：Voronoi 非均匀采样 + 光谱/ON/OFF 脉冲编码 → 接任意 SNN 或轻量 CNN → 脉冲预算-精度曲线（`:88-99`）。
- **Evidence package（计划，非结果）**：可证伪消融 (a)规则网格 (b)随机 Voronoi 种子 (c)去 ON/OFF (d)去光谱 (e)打乱小眼-通道对应（`:92-93`）；强基线为规则网格 rate coding / TTFS / Poisson / patch embedding / `train-your-fly` eye 原样（`:97`）；最小冒烟为用图包 `right_visual_positions_all_neurons.csv` 重建 Voronoi → 2 层 LIF + 线性头跑 50 步 → 对比规则网格 loss 与脉冲数（`:101-103`）。
- **Stated limitations（卡片自承）**：eye 数据依赖官方图包；「通用前端」需 ≥2 backbone + 2 数据集才算站住；「单独发 CVPR 主会偏轻，容易被判 component-level」；「11 天可投性中-高——但故事偏小」；「风险是仍被看成拆了别人一个模块」（`:100/:104-106`）。
- **可恢复性**：idea 卡片本身结构清晰、可一次读懂；但无正文/图表/结果，故 Clarity/Format 相关维度只按「卡片表述 + 未来投稿要求」评估，并标注 not available 项。

## Likely stance and calibrated score

- **Expected outcome**：`verdict: REVISE`（**选题筛选层的 revise-and-rescreen，不是论文层 minor revision**）；overall **5.2 / 10**，confidence **0.80（≈4/5）**。按 `calibration-and-rank.md:43-47` 落在 borderline / lean-reject 之间；因存在 2 条未解决 fatal risk，规则禁止 GO，故取 REVISE 并附硬性 go_conditions——**若仅按卡片当前形态（拆模块+换基准）推进，等价于 NO-GO，不建议投 CVPR 2027 主会**。
- **Main accept signal**：全套 idea 里最具体、最快、最省算力且可证伪的冒烟（`ideas/idea-cards.md:101-103`），消融 (a)(b) 能干净隔离「几何是否有用」，等脉冲预算曲线贴 CVPR 效率口味。
- **Main reject signal**：核心 eye 计算全部来自 contemporaneous 的 arXiv:2610.10023，增量=解耦+换基准；卡片自承 component-level、故事偏小（`:100/:105-106`）。

**Q1｜相对 arXiv:2610.10023，这个增量是否足以撑起 CVPR 主会？→ 否。** 依据链：`train-your-fly` 已实现「复眼 Voronoi + 光谱/ON/OFF + R7/R8 互抑制」且代码数据全公开（`literature-baseline-matrix.md:8`；`prior-art-dedup-log.md:11`）；I3 自己把差异定义为「把它抽象成与脑图解耦的、在标准 CV 基准上可比较的前端，并给出脉冲预算-精度曲线；这是不同的贡献单元」（`ideas/idea-cards.md:98-99`），同时承认「风险是仍被看成拆了别人一个模块」（`:100`）。这恰好落入 `prior-art-dedup-log.md:21`「如果只做同一模型 + 换数据集，仍会被判 incremental」以及 `:18-20` 的 contemporaneous 高度相似加审。未引入新机制、新算法、新知识，也未承诺 `train-your-fly` 未覆盖的可归因发现（对比 I1 的 2×2 结构×动力学交互归因，`ideas/idea-cards.md:33-37`）。按顶会主会 novelty 标准（`universal-review-rubric.md:22/52`），该增量不足以撑起主会。

**Q2｜若只有部分正向结果，诚实可发表的下位结论是什么？** 可写成一条**计算成像/输入编码层的对照结论**：「在等输入脉冲数预算下，果蝇复眼测量导出的非均匀 Voronoi 采样相对规则网格编码，在 `shapes`/CIFAR-10-DVS 上给出（或不给出）可复现的精度-脉冲数权衡；该增益可由 (a)(b) 消融归因于几何而非光谱/ON/OFF。」无论正负，这是 `train-your-fly` 未单独报告、对神经形态传感/事件编码社区有用的分析性结果，适合 workshop、神经形态/传感 venue，或作为 `train-your-fly` 类系统的分析附录；**但不得据此声称「通用可插拔前端提升 CV backbone」，也不足以单独构成 CVPR 主会论文**。

**Q3｜最小冒烟实验是否值得跑：GO。** 计划见 `ideas/idea-cards.md:101-103`（用图包 CSV 重建 Voronoi 采样器 → 对 cogstim 生成脉冲张量 → 2 层 LIF+线性头 50 步 → 对比规则网格 loss 曲线与脉冲数）；`dataset-access-log.md:13` 标注图包含光感受器 2D 坐标且 PASS，`hardware-profile.md:28` 标注 `dyg-cold` 三方依赖齐备，成本符合 `execution-contract-v1.md:51-52`。**可证伪失败信号**：在等输入脉冲数、固定 seed 的 50 步内，Voronoi 前端与规则网格前端在 `shapes` 上的 loss 下降曲线/最终精度差落在 seed 波动或 95% CI（`dataset-access-log.md:35`）之内，或消融 (a)(b) 无差异（`ideas/idea-cards.md:92-93` 自定判据）→「生物几何有用」被证伪，按 `execution-contract-v1.md:72` 失败即淘汰、不事后改写目标。执行层失败信号另记：`hardware-profile.md:38-40` 的 torch/PyG/torch_sparse 兼容验证失败或 1.3GB 图包下载失败（记为执行失败，非机制证伪）。

## Quantitative scorecard

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction & Repair condition | Expected score movement |
|:---|:---:|:---:|:---|:---|:---|
| novelty | 2 | 5 | `ideas/idea-cards.md:86-87,98-100`；`prior-art-dedup-log.md:11,21`；`https://arxiv.org/abs/2610.10023` | **Deduction**：核心 eye 计算（Voronoi+光谱+ON/OFF+R7/R8 互抑制）已由 `train-your-fly` 实现且全公开；差异仅是解耦成可插拔前端+换 CV 基准+加一条曲线，属 `prior-art-dedup-log.md:21` 判 incremental 的情形，且为 contemporaneous 高度相似触发加审。**Repair condition**：把贡献单元重构为 `train-your-fly` 未覆盖、可归因的机制结论（生物测量非均匀采样在等脉冲预算下的因果增益），并与 arXiv:2610.10023 正面对比，而非仅移植模块。 | +1（→3）仅当新增可归因机制结论且正面对比成立；单纯加实验对 overall +0 ~ +0.5 |
| mechanism | 3 | 4 | `ideas/idea-cards.md:88-93`；`literature-baseline-matrix.md:31` | **Deduction**：机制描述（非均匀 Voronoi=「中央凹式」资源分配、光谱/ON/OFF、R7/R8 互抑制）与消融 (a)-(e) 清楚且可证伪，但机制本身非新（复眼模型已属 `train-your-fly`；「中央凹/非均匀采样」在计算成像为已知概念），且卡片未引用任何 foveated/非均匀采样 prior art，缺「几何为什么有用」的因果论证。**Repair condition**：补机制级假设（如非均匀采样与任务空间频率/亮度统计的匹配）、因果消融，并纳入并对齐计算成像侧相关工作。 | +0.5 ~ +1（→3.5-4）当机制假设被实证支持；overall 仅在此时 +0.5 |
| evidence_plan | 3 | 5 | `ideas/idea-cards.md:101-106`；`dataset-access-log.md:33-37`；`execution-contract-v1.md:51-52` | **Deduction**：冒烟最具体可实现，但「通用前端」自承需 ≥2 backbone+2 数据集（`:104`），计划只到单个 2 层 LIF + 单 cogstim + 50 步（`:102-103`）；未提多种子/95% CI/跨数据集复现/视觉 failure cases，主张与计划缺口大。**Repair condition**：补 2×2 backbone×数据集矩阵、等脉冲预算公平协议、多种子与 95% CI、failure cases；按 `execution-contract-v1.md:72` 记录真实 stdout/stderr。 | +1（→4）当矩阵与统计协议齐备；overall +0.5 ~ +1，仅在 11 天内补齐时（但见 executability 约束） |
| baselines | 3 | 4 | `ideas/idea-cards.md:97`；`literature-baseline-matrix.md:26-31` | **Deduction**：列了规则网格 rate/TTFS/Poisson/patch embedding/`train-your-fly` eye 原样，方向合理；但缺 CVPR 级 SOTA 事件/稀疏编码强基线与「等输入脉冲数/等参数量」双预算公平协议，`literature-baseline-matrix.md:31` 明确「不可仅与 ANN toy baseline 比较，CVPR 主会评审不会接受」。**Repair condition**：加入 SOTA 事件/稀疏脉冲编码 + 等脉冲数/等参数量双预算 + ResNet-18/小 ViT 上界 + 95% CI。 | +1（→4）当强基线与公平协议落地；overall +0.5 |
| cvpr_fit | 3 | 4 | `ideas/idea-cards.md:95-96,105`；`venue-review-styles.md:60-69`；`execution-contract-v1.md:42` | **Deduction**：有标准视觉基准与等脉冲数精度/精度-脉冲预算曲线，贴 CVPR 效率口味，优于纯神经科学仿真；但「复眼前段/计算成像」更偏传感/神经形态，且卡片自承 component-level、偏轻（`:105`），主会 reviewer 会质疑视觉增益幅度与贡献完整度。**Repair condition**：在标准基准上给出显著、可复现、跨数据集的精度-资源增益 + 强基线 + 视觉 failure cases，并证明其为完整贡献而非组件。 | +1（→4）当贡献量级与视觉证据达标；overall +0.5 |
| executability_11d | 4 | 4 | `ideas/idea-cards.md:106`；`hardware-profile.md:28,38-40`；`execution-contract-v1.md:37-41,51-52` | **Deduction（>3，仍说明）**：本项最高分——实现最快、数据现成、无需训练大图 SNN、冒烟最省算力（`:106`）。不满分原因：「通用前端」完整证据矩阵 + novelty 重定位 + 与 contemporaneous 正面对比，在 11 天、单次 ≤15min GPU、不做完整/多种子训练（`execution-contract-v1.md:51-52`）下难以补全；且 `hardware-profile.md:38-40` 的 torch/torch_sparse 兼容验证是前置阻塞。**Repair condition**：兼容验证一次性通过并把范围收敛到「1 backbone + 1 数据集」的诚实下位结论，可维持 4；不承诺升到 5。 | 0 ~ +0.5（维持 4 或 4.5）；完整矩阵窗口内不可达，故不评估 +1 |

**Overall: 5.2 / 10 | Confidence: 0.80（≈4/5 scholarly confidence）**
**Recommendation（顶会主会口径）：weak-reject / borderline——当前形态不可投。**
**Verdict: REVISE（选题层）**；规则依据：overall 5.2 < 6.5 且 2 条 fatal risk 未解决 → 不可 GO；致命风险存在 → 必须 NO-GO 或 REVISE。因存在「重构贡献单元 + 补证据」的窄修复路径且冒烟值得跑，取 REVISE；`go_conditions` 任一不满足即退化为 NO-GO。

**Score-change conditions（conservative，见 `calibration-and-rank.md:112-120`）**

| Change | Condition | Likely affected dimensions | Expected movement |
|:---|:---|:---|:---|
| Raise score | 重构为可归因机制结论 + 2×2 backbone×数据集矩阵 + 强基线 + 多种子 95%CI + 对 arXiv:2610.10023 正面对比 | novelty / mechanism / evidence_plan / baselines / cvpr_fit | 各维度 +1；overall +1.0 ~ +1.5（→6.2-6.7，仍需复查 fatal 是否解除） |
| Lower score | 冒烟显示 Voronoi 与规则网格无稳定差异（(a)(b) 无差异）或兼容验证失败无法启动 | mechanism / evidence_plan / executability_11d | overall −1.0 ~ −1.5 或转 NO-GO/fatal |
| No quick change | 「拆模块+换基准」定位不改，核心 eye 计算仍全部来自 contemporaneous 工作 | novelty / cvpr_fit | 提交前 unlikely 改变，维持 REVISE→NO-GO |

## Top strengths

1. **最可执行的证据计划**：`ideas/idea-cards.md:101-103` 给出具体 CSV、具体网络（2 层 LIF+线性头）、具体步数（50）、具体对照（规则网格 loss 与脉冲数）；`dataset-access-log.md:13` 图包含光感受器坐标且 PASS，`hardware-profile.md:28` `dyg-cold` 三方依赖齐备——这是全套 idea 中唯一能在 ≤15min GPU 预算内启动的冒烟。
2. **干净、可证伪的消融**：`ideas/idea-cards.md:92-93` 的 (a)规则网格 /(b)随机 Voronoi 种子直接隔离「几何是否有用」，(c)-(e) 分离 ON/OFF、光谱、小眼-通道对应；判据「若 (a)(b) 无差异，则几何有用被证伪」是明确的自设证伪条件，符合 `universal-review-rubric.md:80-93` 的 claim-evidence 纪律。
3. **与 CVPR 效率口味有接触点**：`ideas/idea-cards.md:95-96` 选等输入脉冲数 accuracy、脉冲数/参数量/时延、低输入率精度保持，比纯神经科学仿真更贴 `venue-review-styles.md:60-69` 的「效率 + 可检验证据」。
4. **数据零摩擦**：`dataset-access-log.md:13,15,35` 标注 FlyWire 图包、cogstim、固定 seed 与 95% CI 协议均 PASS/可用，G1/G2 硬门槛已满足。

> 注：以上均为「计划质量」评价，**不代表任何已观测结果**；输入零实验。

## Major-fatal concerns

**F1 [fatal] Novelty 相对 arXiv:2610.10023 坍塌，增量=拆模块+换基准。**
- Evidence basis：`ideas/idea-cards.md:86-87`（「train-your-fly 有复眼模型，但它与全脑 GNN 死绑在一起…」原句）、`:98-100`（「这是不同的贡献单元」/「风险是仍被看成拆了别人一个模块」）；`prior-art-dedup-log.md:11`（P1 已含复眼几何+无状态 GNN+4 随机图）、`:18-21`（contemporaneous 规则 + 「同一模型+换数据集仍判 incremental」）；`literature-baseline-matrix.md:8`（代码/数据全公开、must-rerun）；`https://arxiv.org/abs/2610.10023`。
- Reviewer deduction：Voronoi、光谱通道、ON/OFF 双路、R7/R8 互抑制这些**全部计算**已在 `train-your-fly` 中实现；I3 的「抽象成可插拔前端」是工程解耦，加「换标准 CV 基准」与「脉冲预算-精度曲线」是评测层改动，三者均非新机制/新算法/新知识。按 `universal-review-rubric.md:22`（weak novelty / unclear difference from close prior work）与 `:52`（novelty 可能坍塌）属独立可拒。
- Required fix：把贡献单元重构为 `train-your-fly` 未覆盖、可归因的机制结论，并以正面对比证明；或诚实降级为 Q2 所述的下位结论 / 改投更贴切 venue。
- Score-change condition：F1 解除（novelty ≥4）才可能把 overall 抬过 6.5；否则维持 REVISE/NO-GO。

**F2 [fatal] 贡献量级 component-level、故事偏小。**
- Evidence basis：`ideas/idea-cards.md:104`（「通用前端需要至少 2 个下游 backbone + 2 个数据集才算站住」原句）、`:105`（「单独发 CVPR 主会偏轻，容易被判 component-level」）、`:106`（「11 天可投性中-高——但故事偏小」）。
- Reviewer deduction：卡片**自承**未达主会贡献量级；证据计划只到单个 2 层 LIF + 单 cogstim（`:102-103`），与「通用可插拔」主张之间存在结构性缺口，按 `universal-review-rubric.md:70`（central contribution is unclear / main claim lacks evidence）与 `calibration-and-rank.md:47`（clear reject）独立可拒。
- Required fix：补齐 2×2 backbone×数据集矩阵 + 跨数据集可复现增益 + 机制结论；窗口内不可达则 NO-GO。
- Score-change condition：F2 与 F1 需同时解除；任一留存则不可 GO。

**M3 [major] 计算成像 / 非均匀采样 prior art 缺口。**
- Evidence basis：`ideas/idea-cards.md:88-91` 的机制描述（「中央凹式空间资源分配」「亮度自适应」）未引用任何 foveated imaging / 非均匀采样 / 事件编码工作；`literature-baseline-matrix.md:31`（不可仅与 ANN toy baseline 比较）；`prior-art-dedup-log.md:9-14`。
- Reviewer deduction：「非均匀采样=中央凹式资源分配」在计算成像为已知概念，若不对照，「几何有用」的 novelty 与机制都进一步被削弱；按 `fixed-output-format.md:73-83` 记为 potentially missing related work（status: unverified，见 Unresolved）。
- Required fix：检索并纳入 foveated/非均匀采样/事件编码 SOTA，明确 I3 与之差异（真实生物测量 vs 手工设计）。
- Score-change condition：mechanism / baselines 各 +0.5 ~ +1；overall +0.5。

**M4 [major] 证据计划到「通用」主张的缺口 + 基线偏弱。**
- Evidence basis：`ideas/idea-cards.md:95-97,102-104`；`dataset-access-log.md:35`（主指标含 95% CI）；`execution-contract-v1.md:51-52`（不做完整/多种子训练）。
- Reviewer deduction：冒烟是单 backbone、单数据集、单 50 步，未提多种子/CI/跨数据集复现/视觉 failure cases；强基线缺 SOTA 事件/稀疏编码与等脉冲数公平协议，无法支撑「通用前端」或 `train-your-fly` eye 原样接入的公平比较。
- Required fix：见 evidence_plan / baselines 的 Repair condition。
- Score-change condition：evidence_plan / baselines 各 +1；overall +0.5 ~ +1。

**M5 [major] 执行前置风险：官方环境兼容性未验证。**
- Evidence basis：`hardware-profile.md:38-40`（官方 torch 2.6/PyG 2.6/torch-sparse，本机 2.11/2.8 缺 `torch_sparse`，「直接复现官方代码需兼容性验证，这是冒烟实验必须首先检查的事项」）；`literature-baseline-matrix.md:8`；`ideas/idea-cards.md:104`（eye 数据依赖官方图包）。
- Reviewer deduction：I3 的全部输入数据来自官方图包，若兼容验证失败，冒烟无法启动，F1/F2 的证据缺口更无从补齐。
- Required fix：冒烟第一步固定为兼容性验证 + 1.3GB 图包下载核验，记录真实 stdout/stderr（`execution-contract-v1.md:72`）。
- Score-change condition：不影响 novelty 判断；失败则 executability_11d −1 且转 NO-GO。

## Writing and presentation concerns

- 输入为 idea 卡片、无论文正文/图表/附录，故本维度只评「卡片表述清晰度 + 未来投稿可恢复性」；页数、匿名、模板、figure/table narration 标 **not available**，不虚构。
- **主张口径风险**：`ideas/idea-cards.md:86-87,99` 的「通用、可插拔、与连接组图解耦」「不同的贡献单元」是定位句；若进入论文，须避免把「解耦/移植」写成「新机制」，否则构成 `universal-review-rubric.md:93` 所禁止的「对 unsupported claim 做修辞加强」。硬规则：未支持主张应弱化、删除或补证据，不得仅改措辞。
- **相对主张未定义基线**：`ideas/idea-cards.md:91`「参数量近乎为零」未说明相对谁（patch embedding？事件编码？全图 GNN？）；`:90`「中央凹式空间资源分配」「亮度自适应（R7/R8 互抑制）」为机制断言但卡片无因果证据、无引用——按 claim-evidence audit 均为 absent/weak，须在写作前补证据或降级为假设。
- **术语稳定性**：「可插拔前端 / 输入编码层 / 计算成像视角 / 与连接组图解耦」四种表述在卡片中并存（`:82,86,94,98`），进入论文需统一，否则 `review-output-standards.md:73` 的 terminology stability 风险。
- 遵守任务：本报告不写 rebuttal、不修改 idea、不生成论文文本。

## Format-venue concerns

- **CVPR 2027 主会格式**：`venue-guides/cvpr.md:73-96` 为 8 页上限（不含 references/appendix）、双盲、`cvpr.sty`、rebuttal 期；但该文件 `:12-13` 明示为 **2026 legacy、投稿前须按当年官方政策复核**，故以 `https://cvpr.thecvf.com/Conferences/2027/CallForPapers` 为准（本评审未独立复核官方页，见 Unresolved）。idea 卡片阶段这些项均 **not applicable / not available**。
- **contemporaneous 引用义务（硬约束）**：`prior-art-dedup-log.md:18-21` 与 `execution-contract-v1.md:40-41` 要求必须引用讨论 arXiv:2610.10023，且高度相似会加审——这是 I3 进入主会时的 format/related-work 硬门槛，与 F1 直接关联。
- **视觉证据要求**：`venue-review-styles.md:66-69` 要求把 figures/定性样例/failure cases 当作证据；`ideas/idea-cards.md:95-96` 的证据计划只列数值指标（accuracy、脉冲数、时延），未规划定性对比或 failure cases，属 `fixed-output-format.md:94-106` 实验审计缺项。
- **时间线**：注册 11-10、全文 11-16（`execution-contract-v1.md:37-38`）；即便按 REVISE 重定位，11 天内产出主会级 evidence package（2×2 矩阵 + 强基线 + 多种子 + 正面对比）窗口极紧，是 `executability_11d` 未给满分的直接原因。
- **Desk verdict（针对 idea 阶段）**：`desk-checks.md:47-51` — Desk rejection risk: **medium**（topic 相容但 venue-fit/贡献量级存疑，F2）；Can be fixed before review? **partly**（重定位 + 补证据可缓解，但窗口受限）。

## Multi-reviewer panel

> 三名审稿人先独立成形再综合；结论差异来自各自 lens 的权重，非人为制造分歧或强行夸奖（`review-output-standards.md:27-38`、`reviewer-panel.md:1-5`）。

**R1 — 计算成像 / 传感器专家**
- Lens：非均匀采样、传感器几何、几何编码的因果贡献与 prior art 定位。
- Score tendency：5/10（borderline，略偏 reject）。
- Confidence：0.75（缺实验结果与 foveated 相关工作面，标 insufficient evidence）。
- Main positive signal：消融 (a)规则网格 /(b)随机 Voronoi 种子（`ideas/idea-cards.md:92-93`）直接隔离「几何是否有用」，等输入脉冲数/脉冲预算-精度曲线（`:95-96`）是干净的计算成像对照设计。
- Main negative signal：「非均匀 Voronoi=中央凹式资源分配」（`:90`）在计算成像为已知概念，卡片未引用 foveated/非均匀采样工作；「参数量近乎为零」（`:91`）未定义比较基线，机制非新。
- Evidence basis：`ideas/idea-cards.md:88-93`；`literature-baseline-matrix.md:31`。
- Score-change condition：若给出相对 SOTA 事件/非均匀编码、在等脉冲数下显著且跨数据集可复现的增益，并补相关工作面 → +1。

**R2 — SNN / 神经形态专家**
- Lens：脉冲编码、脉冲预算、训练稳定性、LIF 实现可行性。
- Score tendency：5/10（borderline）。
- Confidence：0.70（surrogate gradient/τ/阈值/50 步收敛性未定义，标 insufficient evidence）。
- Main positive signal：2 层 LIF + 线性头 + cogstim 的冒烟最小可跑（`ideas/idea-cards.md:101-103`），「等输入脉冲数 accuracy」与脉冲数/低输入率精度保持（`:95-96`）是该社区认账的评价轴；`hardware-profile.md:28` 依赖齐备。
- Main negative signal：R7/R8 互抑制、ON/OFF、光谱通道在 `train-your-fly` 已实现（`https://arxiv.org/abs/2610.10023`；`prior-art-dedup-log.md:11`），「可插拔」是工程解耦而非脉冲机制创新；T/τ/阈值/替代梯度与 50 步是否收敛未定，且 `hardware-profile.md:36-37` 限定 T=8~16 子序列。
- Evidence basis：`ideas/idea-cards.md:89-90,97,101-103`；`hardware-profile.md:34-40`。
- Score-change condition：若生物几何在等脉冲预算下改变脉冲效率/首次正确判别时刻（超出规则网格），→ +0.5 ~ +1。

**R3 — CV 架构 / 效率专家**
- Lens：标准 CV 基准、强基线、公平协议、贡献量级与 venue fit。
- Score tendency：4/10（lean reject）。
- Confidence：0.85（卡片自承多条限制，证据充分）。
- Main positive signal：用 CIFAR-10 / CIFAR10-DVS 与精度-脉冲预算曲线（`ideas/idea-cards.md:95-96`）比纯神经科学仿真更贴 CVPR 效率口味。
- Main negative signal：强基线缺 SOTA 事件/稀疏编码且缺等脉冲数公平协议（`:97`；`literature-baseline-matrix.md:31`「不可仅与 ANN toy baseline 比较」）；「通用前端需 ≥2 backbone+2 数据集」（`:104`）而计划只到 1 个（`:102-103`），自承 component-level（`:105`）；相对 arXiv:2610.10023 增量=拆模块+换基准（`prior-art-dedup-log.md:21`）。
- Evidence basis：`ideas/idea-cards.md:95-106`；`prior-art-dedup-log.md:18-21`；`execution-contract-v1.md:42`。
- Score-change condition：补齐 2×2 矩阵 + 多种子 95%CI + 强基线 + 跨数据集显著增益 **且** novelty 重定位成立 → +1 ~ +1.5；否则维持 reject。

**Panel synthesis**
- Agreement: 核心 eye 计算全部来自 `train-your-fly`；I3 增量主要是解耦/换基准/换指标；证据计划与「通用前端」主张缺口大；强基线偏弱；F1+F2 独立可拒；冒烟值得跑且能证伪「几何有用」。三人对「当前形态不足以撑起 CVPR 主会」无实质分歧。
- Disagreement: 仅**权重**差异，非结论对立——R1/R2 认为「几何 vs 规则网格在等脉冲预算下的对照」本身有（哪怕偏小的）独立价值，R3 认为按主会贡献量级不足以单独成篇；R2 额外关注训练可行性，R1 额外关注计算成像 prior art。
- Decisive accept axis: 重构后产生 `train-your-fly` 未覆盖、可归因的机制结论（生物非均匀采样在等脉冲预算下跨 backbone/数据集可复现的增益），并被强基线正面对比支持。
- Decisive reject axis: 维持「可插拔前端=拆模块+换基准」定位、无新机制/新发现、证据停在单 backbone 单数据集 → novelty 坍塌（F1）+ component-level（F2）独立可拒。
- Unresolved evidence: 零实验结果；CVPR 2027 主会对 component-level 输入编码层的实际接受阈值；foveated/非均匀采样/事件编码 SOTA 的重叠程度；`train-your-fly` 官方代码在本机的兼容性（`hardware-profile.md:38-40` 标注需验证、未实测）。
- Final calibrated stance: **REVISE（选题层），overall 5.2 / confidence 0.80**；按 `reviewer-panel.md:108-110` 不把致命缺陷平均掉，最终立场跟随最强未解决关切（F1/F2）。当前形态投 CVPR 主会 = 实质 NO-GO。

## Concern-to-action table

| ID | Severity | Concern | Evidence basis | Affected criterion | Fix class | Required action | Owner skill | Score-change condition |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| F1 | fatal | 核心 eye 模块来自 arXiv:2610.10023，增量=拆模块+换基准 | `ideas/idea-cards.md:86-87,98-100`；`prior-art-dedup-log.md:11,21`；`https://arxiv.org/abs/2610.10023` | novelty / cvpr_fit | related-work | 重构贡献单元为可归因机制结论并正面对比，或诚实降级为下位结论 | `f-guidance-builder-v1`（作者侧重定位，非本评审改 idea） | novelty ≥4 方可考虑抬过 6.5 |
| F2 | fatal | component-level、故事偏小，证据矩阵不达「通用前端」 | `ideas/idea-cards.md:104-106,102-103` | evidence_plan / cvpr_fit | experiment | 补 2×2 backbone×数据集矩阵 + 跨数据集可复现增益 | 本地冒烟执行 + `f-research-v1`（完整阶段） | F1 与 F2 同时解除方可 GO |
| M3 | major | 缺 foveated/非均匀采样/事件编码 prior art 对照 | `ideas/idea-cards.md:88-91`；`literature-baseline-matrix.md:31` | novelty / baselines | related-work | 公开检索并纳入 SOTA 对照，明确「真实生物测量 vs 手工设计」差异 | `ccf-paper-reviewer`（定位复审）/ 作者侧 | mechanism/baselines +0.5 ~ +1 |
| M4 | major | 冒烟单 backbone/单数据集/无多种子 CI，强基线偏弱 | `ideas/idea-cards.md:95-97,102-104`；`dataset-access-log.md:35`；`execution-contract-v1.md:51-52` | evidence_plan / baselines | experiment / reproducibility | 补多种子 95%CI、等脉冲数/等参数量双预算、失败信号记录、视觉 failure cases | 本地冒烟执行（记录真实 stdout/stderr） | evidence_plan/baselines +1；overall +0.5 ~ +1 |
| M5 | major | 官方环境兼容性未验证、eye 数据依赖官方图包 | `hardware-profile.md:38-40`；`literature-baseline-matrix.md:8`；`ideas/idea-cards.md:104` | executability_11d | reproducibility | 冒烟第一步固定为 torch/PyG/torch_sparse 兼容验证 + 1.3GB 图包下载核验 | 本地冒烟执行 | 失败则 executability −1 且转 NO-GO |
| Q1 | fatal-adjacent | 相对 arXiv:2610.10023 增量不足以撑起主会 | `prior-art-dedup-log.md:18-21`；`ideas/idea-cards.md:100` | novelty / cvpr_fit | venue-mismatch | 明确回答「否」，并按下位结论重写投稿定位或改 venue | `f-guidance-builder-v1` / 作者侧 | 与 F1 同 |
| Q3 | moderate | 冒烟 GO 但须先过兼容验证与可证伪判据 | `ideas/idea-cards.md:101-103,92-93`；`execution-contract-v1.md:72` | evidence_plan | experiment | 失败即淘汰，不事后改写目标 | 本地冒烟执行 | 几何增益可分辨 → evidence_plan +0.5 |

## Recommended next CCFA owner

- **主 owner**：`f-guidance-builder-v1` / 作者侧——在选题筛选轮内**重构 I3 的贡献单元与 novelty 定位**（execution-contract-v1.md:28-32 将本轮定位为 idea-screening round，非完整 guidance build）。本评审不修改 idea、不生成论文文本、不写 rebuttal。
- **次 owner**：本地冒烟执行（`execution-contract-v1.md:16,51-52`；`hardware-profile.md:28` `dyg-cold`），按 Q3/M5 先做兼容验证再跑 Voronoi vs 规则网格对照，记录真实 stdout/stderr 与失败信号，失败即淘汰（`execution-contract-v1.md:72`）。
- **不交接**：`ccf-rebuttal-writer`（任务不写 rebuttal）、`ccf-paper-writer`（任务不生成论文文本）。
- **若 `go_conditions` 任一不满足或 novelty 仍坍塌**：淘汰 I3，转 `ideas/idea-cards.md:186-188` 漏斗提示的 I1/I6，或把下位结论改投 workshop/神经形态传感 venue；不占用 CVPR 2027 主会 11 天窗口。
- **量纲/交接说明**：本报告为 `CCFA Handoff Mode: PARTIAL` 下的独立评审产物，G6-G8/validation/handoff 保持 pending（`execution-contract-v1.md:30-33`），不伪造 pass。

## Checks run

- 已加载并遵循 `ccf-paper-reviewer`(scientific) 及其 `review-output-standards.md` / `universal-review-rubric.md` / `calibration-and-rank.md` / `reviewer-panel.md` / `venue-review-styles.md` / `review-workflow.md` / `fixed-output-format.md` / `desk-checks.md` / `venue-guides/cvpr.md`。
- 已读全部 6 个冻结输入：`ideas/idea-cards.md`、`prior-art-dedup-log.md`、`literature-baseline-matrix.md`、`dataset-access-log.md`、`hardware-profile.md`、`execution-contract-v1.md`。
- 四遍读（`review-workflow.md:24-29`）：desk / contribution / evidence / adversarial 均执行；因无正文，evidence pass 针对「计划」而非结果。
- 执行 audits：claim-evidence（针对卡片主张句）、related-work positioning（P1/P3/P4 与 contemporaneous 规则）、venue fit、reproducibility、desk checks、output quality gate。
- 对每个 ≤3 分维度给出 Deduction / Repair condition / Expected score movement；给出 score-change conditions 表。
- Multi-reviewer panel 3 角色独立成形 + synthesis 六要素；不强行制造分歧/夸奖。
- 未跑任何实验、未联网检索、未生成论文文本或 rebuttal、未修改任何已有项目文件（仅新建本报告）。

## Unresolved or unverified

- **零实验结果**：输入为 idea 卡片（任务约束），`evidence` 维度只评「证据计划的可行性与完整性」；文中所有「若能补 X 实验/若出现 Y 结果」均为**条件**，非既成事实；全文未编造任何结果、数值或引用。
- **URL 核验状态**：`https://arxiv.org/abs/2610.10023` 等 URL 由 `literature-baseline-matrix.md:8` 与 `execution-contract-v1.md:54-65` 标注为 2026-11-05 已核验的公开来源；本独立评审**未重新联网抓取**，作为输入事实引用（不声称独立复核）。
- **CVPR 2027 官方政策**：`venue-guides/cvpr.md:12-13` 为 2026 legacy、要求按当年官方页复核；页数/匿名/模板/政策以 `https://cvpr.thecvf.com/Conferences/2027/CallForPapers` 为准，本评审未独立复核官方页。
- **本机兼容性**：`hardware-profile.md:38-40` 标注 torch 2.6→2.11 / 缺 `torch_sparse` 需验证，未实测；直接影响 M5 与冒烟是否可启动。
- **missing related work（status: unverified）**：foveated imaging / 非均匀采样 / 事件编码 SOTA 与 I3 的重叠程度未做公开检索（输入未提供且不得编造引用），列为 M3 的未决风险。
- **contemporaneous 加审尺度**：`prior-art-dedup-log.md:18-21` 给出规则，但「高度相似」的具体裁量未知。
- **机制断言未验证**：`:90-91` 的「中央凹式资源分配 / 亮度自适应 / 参数量近乎为零」无因果证据与比较基线定义，未核验。
- **contribution 量级阈值**：CVPR 2027 主会对 component-level 输入编码层的实际接受阈值无法从输入推定，采保守顶会口径。

## Output self-check

1. 章节顺序：Mode → Venue and assumptions → Paper summary → Likely stance and calibrated score → Quantitative scorecard → Top strengths → Major-fatal concerns → Writing and presentation concerns → Format-venue concerns → Multi-reviewer panel → Concern-to-action table → Recommended next CCFA owner → Checks run → Unresolved or unverified → Output self-check — 共 15 节，与契约一致 ✓
2. 所有表格 Markdown 分隔符有效、各行列数一致 ✓
3. 分数/confidence/建议内部一致：overall 5.2 < 6.5 且有 2 条未解决 fatal → 取 REVISE 而非 GO；front matter 与正文分数逐项一致 ✓
4. 列表平行语法、因果链（problem → reason → consequence → action）显式 ✓
5. 标点一致（中文全角，URL/路径/标识符/代码保留半角）✓
6. 无待填占位符、待办标记、空标题或填空符 ✓
7. 无「需要更多实验」类泛泛填充：每条 concern 均绑定 `文件:行号` 或已核验 URL ✓
8. 硬性要求核对：YAML front matter 字段严格 ✓；每个 ≤3 分数含 Deduction/Repair/Expected movement ✓；panel ≥3 角色且 synthesis 含 Agreement/Disagreement/Decisive accept axis/Decisive reject axis/Unresolved evidence/Final calibrated stance ✓；明确回答 arXiv:2610.10023 增量（否）+ 下位结论 ✓；冒烟 GO/NO-GO（GO）+ 可证伪失败信号 ✓；未写 rebuttal / 未改 idea / 未生成论文文本 ✓；未编造结果/数值/引用 ✓
