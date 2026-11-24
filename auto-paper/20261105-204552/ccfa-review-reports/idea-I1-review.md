---
idea_id: I1
overall: 5.4
confidence: 0.70
verdict: REVISE
scores: {novelty: 3, mechanism: 4, evidence_plan: 3, baselines: 4, cvpr_fit: 3, executability_11d: 2}
fatal_risks: ["11 天到 CVPR 2027 全文截止（11-16 AOE；注册 11-10）+ 单次 <=15 分钟冒烟预算（execution-contract-v1.md §5），与 I1 所需的 2x2 x 消融 x 多种子全文实验不可兼容；idea-cards.md 第 50 行自评『11 天可投性：低』、第 48 行自认『11 天内做不出完整多种子论文』。", "must-rerun 基线 train-your-fly 在本机 dyg-cold（torch 2.11 / PyG 2.8）缺 torch_sparse、官方 pin torch 2.6 / PyG 2.6，hardware-profile.md 第 38-40 行标注『直接复现官方代码需兼容性验证』；基线未验证前，等 synaptic-op 预算对比与 4 随机图 ensemble 无法成立。", "核心增量『结构 x 动力学超可加交互』可证伪且可能为负：idea-cards.md 第 36 行以双因素 ANOVA 交互不显著为证伪条件；若交互不显著，相对 arXiv:2610.10023 退化为『加时间维的复现』，落入 contemporaneous 加审下的 incremental 判定（idea-cards.md 第 49 行自认）。"]
go_conditions: ["先跑最小冒烟实验，确认官方 train-your-fly 在 dyg-cold 可复现（或给出等价替代）、<=20k 视叶子图 LIF T=8/batch=4 不 OOM 且单步 <=15 分钟、生物图 vs 随机图 30 步 loss 可分。", "把交付单元从『完整论文』收窄为 I6 式 mini-benchmark（2x2x1 四格 + 交互项 + 95% CI），并预先接受『交互不显著』的负结果下位结论；或把正式全文延到下一 CVPR 周期以解除 11 天约束。", "相对 arXiv:2610.10023 给出非 incremental 的定量增量：在等 synaptic-op 预算下报告交互效应量与置信区间，而非仅声明『加了时间维与脉冲状态』。"]
review_execution: independent-agent
---

# I1 — FlySpike-T 独立评审报告

## Mode

- 模式：`scientific`（独立审稿人 / independent-agent review），非 quick review、非 full/writing 合并评审。
- 被评对象：`ideas/idea-cards.md` 中的 **I1 idea 卡片，不是论文，没有任何实验结果**。
- 依据技能：`ccf-paper-reviewer`（scientific），并遵循 `review-output-standards.md`、`universal-review-rubric.md`、`calibration-and-rank.md`、`reviewer-panel.md`、`venue-review-styles.md`。
- 证据口径：因无实验，`evidence_plan` 评的是「**证据计划的可行性与完整性**」，不把计划写成已观测结果；本报告不编造任何数值、消融结论、实验结果或引用。
- 独立性：本评审未读取同目录下 `idea-I3-review.md` / `idea-I5-review.md`，未与其他 idea 的分数做对齐或平均，独立成文。
- 边界：不写 rebuttal、不修改 idea、不生成论文文本。

## Venue and assumptions

| 项 | 取值与证据 |
|:---|:---|
| Venue | CVPR 2027 **主会**（顶会，非 workshop / 非期刊 Q2 放水）。venue family = CVPR/ICCV/ECCV；主评分维度 = novelty / technical quality / empirical validation / visual evidence / clarity / fair comparison（`venue-review-styles.md` 第 60-69 行）。 |
| 时间线 | 当前 2026-11-05；Registration 2026-11-10 AOE、Submission 2026-11-16 AOE、Supplementary 2026-11-23（`execution-contract-v1.md` §4，来源 https://cvpr.thecvf.com/Conferences/2027/CallForPapers）；距全文仅 **11 天**。 |
| Contemporaneous 规则 | 2026-09-15 后上线论文视为 contemporaneous，须引用讨论、高度相似会加审；arXiv:2610.10023（2026-10-08）落入该窗口（`prior-art-dedup-log.md` 第 18-21 行；https://arxiv.org/abs/2610.10023）。 |
| 硬件 / 运行信封 | RTX 3060 12 GB（空闲约 10.8 GB）、12 逻辑核、CUDA 12.8、磁盘约 547 GB（`hardware-profile.md` 第 9-17 行）；`dyg-cold`：torch 2.11+cu128 / PyG 2.8.0.post1 / spikingjelly / cv2 齐备（第 28 行）。12 GB 无法对 166k 神经元整图做长序列 BPTT，必须取视叶子图、T=8~16、小 batch（第 36-37 行）。冒烟预算：单次 <=15 分钟 GPU、显存 <=10 GB、下载 <=1.5 GB、**不做完整训练/多种子大实验**（`execution-contract-v1.md` §5）。用户任务描述另给 31.9 GB RAM，但 `hardware-profile.md` 第 17 行注明 probe 返回 null、未据此推断数值。 |
| 基线兼容性 | 官方 `train-your-fly` pin torch 2.6.0 / PyG 2.6.1 / torch-scatter 2.1.2 / **torch-sparse 0.6.18**；本机缺 `torch_sparse`，「直接复现官方代码需兼容性验证，这是冒烟实验必须首先检查的事项」（`hardware-profile.md` 第 38-40 行）。 |
| 数据 | G1 全部 PASS 可直下（`dataset-access-log.md`）；cogstim 8 类 512x512 PNG、按 class 分 train/test、`--seed` 可复现（https://github.com/eudald-seeslab/cogstim）；标准规模每类 5000/5000/5000（第 33-34 行）。 |
| 大方向锁定 | GNN + SNN + 果蝇连接组 + 视觉；不得漂到纯神经科学仿真或纯图表示学习（`execution-contract-v1.md` §4）。 |
| 竞争工作（URL 均转引自本轮检索记录） | arXiv:2610.10023 / `train-your-fly`（must-rerun、代码数据全公开，https://arxiv.org/abs/2610.10023、https://github.com/eudald-seeslab/train-your-fly）；arXiv:2609.01330（https://arxiv.org/abs/2609.01330）；Nature 2024 flyvis（https://www.nature.com/articles/s41586-024-07939-3）；SpikeTrack（https://arxiv.org/abs/2602.23963）；TAPFormer（https://arxiv.org/abs/2603.04989）；BioReservoir（https://github.com/igdigitallab/bioreservoir）。 |
| 冻结输入 | 已读全部 6 个：`idea-cards.md`、`prior-art-dedup-log.md`、`literature-baseline-matrix.md`、`dataset-access-log.md`、`hardware-profile.md`、`execution-contract-v1.md`。 |
| 评审假设 | 判断基于卡片文本 + 冻结输入；**未重新联网、未运行任何实验、未核验任何代码/数据可下载性**。所有 URL 为本轮检索记录中的已核验条目转引，非本报告重新访问。 |

## Paper summary

被评对象是 idea 卡片而非论文，无 Abstract/Introduction/实验章节，因此本节概括其**主张与计划**（均为「计划」，非「结果」）：

- **瓶颈**（第 24-27 行）：现有连接组视觉模型把连接组当静态结构先验——`train-your-fly` 明写「neurons keep no state between steps」、3 步无状态消息传递 + tanh 读出；而 ON/OFF 分离、方向选择性、looming、适应本质是时间计算；连接组 + 脉冲神经元的工作（arXiv:2609.01330、BrainTrace）只做神经科学仿真，无可训练 CV 任务，也未把「结构」与「动力学」拆开归因。
- **机制**（第 28-32 行）：固定生物图为稀疏有向循环骨架，边权 = `syn_count` x 递质符号(±) x 可学习增益；节点从无状态 tanh 换成 LIF/ALIF；视觉输入按 T 个时间步送入；读出 Kenyon 群体脉冲计数；假设生物图 ON/OFF 分叉、前馈-反馈 motif 与膜时间常数 τ 之间存在「匹配」。
- **关键假设**（第 33 行）：结构与动力学在时序任务上存在**超可加交互**，静态任务上退化为可加。
- **可证伪消融**（第 34-36 行）：2x2 受控设计 `{生物图, 4 种随机图} x {无状态 GNN, LIF, ALIF}`，加 (a) 去泄漏 τ→∞、(b) 打乱递质符号、(c) 固定增益不训练、(d) 打乱输入时间顺序；若时序任务上「生物图优势」在无状态条件下一样大（双因素 ANOVA 交互不显著），机制被证伪。
- **贡献类型**（第 37 行）：新架构 + 一个可归因的机制结论（结构 x 动力学），而非又一个 backbone。
- **任务/指标**（第 38-40 行）：cogstim `lines` 时序化、运动方向/looming 合成序列、可选 CIFAR10-DVS；主指标 = 固定 synaptic-op 预算下 test accuracy；次指标 spike rate、首次正确判别时刻、accuracy-vs-T、参数量/突触操作数。
- **强基线**（第 41-42 行）：`train-your-fly`（must-rerun）、4 随机图 ensemble、spikingjelly LIF、同参 ANN、CVPR 2026 SpikeTrack 思路对照（文献）。
- **最小冒烟**（第 45-47 行）：下真实图 → 抽视叶子图 <=20k 节点 → PyG 稀疏边 → LIF 前向 T=8/batch=4 → 记显存/耗时/spike 率 → 生物图 vs 1 随机图跑 30 步训练看 loss 是否下降、是否可分。
- **自评风险**（第 48-50 行）：166k 节点 BPTT 显存爆炸、τ/阈值/surrogate gradient 超参敏感、11 天做不出完整多种子论文、只差「加了时间维」可能被判 incremental；「11 天可投性：低」。

## Likely stance and calibrated score

- **Likely stance**：borderline，偏 weak-reject 一侧（`calibration-and-rank.md` 第 45-47 行：borderline 通常 5-6）。6 维均值约 3.17/5 ≈ 6.3/10，但按 `calibration-and-rank.md` 第 75 行「overall 跟随最强未解决弱点」及 `reviewer-panel.md` 第 110 行「不得平均掉致命缺陷」，因 3 条未解决致命风险下调约 0.9 → **5.4**。
- **Overall**：`5.4 / 10`。**Confidence（front matter）**：`0.70`。**Scholarly Confidence**：`3/5`（结构化 idea 卡片 + 完整冻结输入 + 已核验 URL，但无论文主体、无 appendix、无代码、无结果；`calibration-and-rank.md` 第 66-67 行 3/5 档）。**Verdict**：`REVISE`。
- **判定规则核对**：overall 5.4 < 6.5，且存在未解决致命风险 → 不可 GO；有致命风险必须 NO-GO 或 REVISE。选 **REVISE** 而非 NO-GO 的理由：I1 的差异化轴（时间维度/脉冲动力学、机制级交互归因、spike-op 能效轴）是 `prior-art-dedup-log.md` 第 11 行**明确允许**的差异轴，且漏斗第 186 行标 I1「机制最硬」；存在可执行的修复路径（收窄为 mini-benchmark + 冒烟先行 + 接受负结果下位结论 + 延周期），故保留科学价值而判修订，不淘汰。

**硬性回答 A：相对 arXiv:2610.10023，这个增量是否足以撑起 CVPR 主会？**

**不足以（当前形态）。** 2610.10023 已做了复眼 Voronoi + FlyWire 全图 + 无状态 GNN + 学习突触增益 + Kenyon 读出 + 生物图 vs 4 随机图等布线预算对比（`prior-art-dedup-log.md` 第 11 行；https://arxiv.org/abs/2610.10023）。I1 的增量是「加时间维 + 换 LIF/ALIF 脉冲状态 + 2x2 交互归因 + 比较轴从 wiring cost 换到 spike/energy」（`idea-cards.md` 第 43-44 行）。其中真正有资格成为主会贡献的只有「**结构 x 动力学超可加交互**」这一可归因机制结论——但它恰恰是卡片自己设定为**可能证伪**的假设（第 36 行）。在 (1) 交互效应量尚无实验、(2) must-rerun 基线在本机兼容性未验证、(3) 11 天无法产出多种子证据包、(4) contemporaneous 高度相似加审（`prior-art-dedup-log.md` 第 18-21 行）四条同时成立时，一个 CVPR 主会审稿人最可能的判词是「same model + added time axis + one possibly-negative ANOVA term = incremental」，与卡片第 49 行自认一致。因此当前增量**不足以**撑起主会；只有当交互项在等 synaptic-op 预算下显著且带 CI 时，增量才从「加了个维度」变为「发现了一条机制」。

**硬性回答 B：若只有部分正向结果，诚实可发表的下位结论是什么？**

按卡片第 36 行与 I6 第 167-168 行的「负结果同样有效」逻辑，可诚实交付的三档下位结论（均为**待验证的计划性表述，非已观测**）：

1. **最强可保结论（交互不显著）**：「在等突触操作预算与固定 T 下，连接组拓扑对时序视觉的增益与脉冲动力学**可加而非超可加**；结构与动力学可独立替换，生物接线对时间计算不具特权。」——这削弱而非支持 I1 的中心假设，但作为受控负结果对社区有用（`idea-cards.md` 第 36 行证伪条件的直接对应）。
2. **次强（时序任务涨、静态任务不涨）**：「脉冲状态引入的收益仅在时序判别上出现，且对输入时间顺序打乱敏感（消融 d），与生物图无关。」——此时贡献退化为「SNN 在 cogstim 时序任务上的验证」，须降级为 workshop / mini-benchmark，不能称机制发现。
3. **最弱（只有可分 loss、无统计结论）**：只能交付 I6 式 **mini-benchmark**（2x2x1 四格 + 复现方差 + 单格耗时/显存外推，`idea-cards.md` 第 176-177 行 / `idea-cards.md` I6），如实标注「underpowered、单种子、不足以支持交互主张」。

任何情况下都**不得**把「loss 在 30 步下降」写成「结构 x 动力学交互成立」——那是把计划写成结果。

## Quantitative scorecard

表 A（本次 front matter 指定的 6 个决策维度，1-5）与表 B（`calibration-and-rank.md` 第 85-102 行**强制**的 7 维通用 scorecard）维度命名不同、分数独立给出；语义对应大致为 mechanism→Soundness、evidence_plan→Evidence、baselines→Evidence/Reproducibility、cvpr_fit→Significance、executability_11d 为本次新增的时间线维度，不并入通用 7 维。

**表 A — 决策维度**

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|:---|:---:|:---:|:---|:---|
| novelty | 3 | 3 | `idea-cards.md` 第 43-44、49 行；`prior-art-dedup-log.md` 第 11、21 行 | 差异化轴合规但相对 2610.10023 仍是「同模型 + 时间维 + 统计归因」，卡片自认 incremental 风险；修复见下方 D1 |
| mechanism | 4 | 4 | `idea-cards.md` 第 28-36 行（2x2 + 4 消融 + ANOVA 交互项 + 明确证伪条件） | 机制级可归因设计完整；保留项：「匹配」为未预验证猜想、τ 无定量定义 |
| evidence_plan | 3 | 3 | `idea-cards.md` 第 34-42、48-50 行；`execution-contract-v1.md` §5 | 完整性高、可行性低（11 天/12 GB/多种子冲突）；修复见 D2 |
| baselines | 4 | 4 | `idea-cards.md` 第 41-42 行；`literature-baseline-matrix.md` 第 26-31 行 | 强基线齐全且非 toy ANN；保留项：must-rerun 兼容性未验、SpikeTrack 仅文献对照、缺 TAPFormer |
| cvpr_fit | 3 | 3 | `idea-cards.md` 第 38-40 行；`venue-review-styles.md` 第 60-69 行 | 合成小图任务 + 能效轴偏效率/AI-for-Science + 无真实视觉基准；修复见 D3 |
| executability_11d | 2 | 4 | `execution-contract-v1.md` §4-§5；`hardware-profile.md` 第 36-40 行；`idea-cards.md` 第 50 行 | 11 天 + 单次 <=15 分钟 + 基线未验 → 完整证据包不可得；修复见 D4 |

**表 B — 强制通用 scorecard**

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|:---|:---:|:---:|:---|:---|
| Novelty | 3 | 3 | `idea-cards.md` 第 43-44、49 行 | 增量需靠交互效应量坐实；否则 incremental |
| Soundness | 4 | 3 | 第 28-36 行 2x2 + 消融 + 证伪条件 | 「匹配」假设与 surrogate/reset 配置未给；补齐可到 4 |
| Evidence | 2 | 4 | 无任何实验结果；`execution-contract-v1.md` §5 禁止多种子大实验 | 证据**计划**可行但**证据**为空；`calibration` 第 108 行 1-2 档 |
| Significance | 3 | 3 | `prior-art-dedup-log.md` 第 25-27 行定位语句 | 交互若成立有社区价值，若证伪则价值转负结果 |
| Clarity | 4 | 4 | 第 20-50 行结构完整、瓶颈/机制/消融/指标分列 | 「匹配」「超可加」需可操作定义，见 Writing concerns |
| Reproducibility | 3 | 4 | 第 41、45-47 行；`hardware-profile.md` 第 38-40 行 | 官方 pin 与本机不一致、缺 torch_sparse；冒烟须首先验证 |
| Ethics / Limitations | 4 | 4 | 第 48-50 行自列风险；`dataset-access-log.md` 全 CC-BY/MIT/Apache | 无人类受试/敏感数据；限制披露诚实 |

**Overall:** 5.4/10 | **Scholarly Confidence:** 3/5 | **Recommendation:** borderline→weak-reject | **Verdict:** 交互效应量坐实且基线可复现可 +1；交互证伪或基线不可复现 -1 或转 NO-GO。

**<=3 分数的扣分 / 修复 / 预期移动（硬性要求 #1）**

```
Dimension: novelty
Score: 3
Confidence: 3
Evidence basis: idea-cards.md 第 43-44 行把差异定义为「时间维度与脉冲状态」；第 49 行自认「与 arXiv:2610.10023 只差加了时间维可能被判 incremental」；prior-art-dedup-log.md 第 21 行「如果只做同一模型 + 换数据集仍会被判 incremental」。
Deduction: 差异轴虽在允许列表内，但贡献单元仍是「P1 的模型 + 时间维 + 统计检验」，尚未给出任何把增量与 P1 定量分开的证据（交互效应量/CI 均无）；contemporaneous 加审放大该扣分。
Repair condition: 在等 synaptic-op 预算下报告 2x2 的双因素 ANOVA 交互效应量 + 95% CI，并明确写出「交互显著」与 P1「生物图 vs 随机图主效应」是不同结论单元。
Expected score movement: +0.5 to +1.0 dimension-only（3→4）；仅当交互显著才可能带动 overall +0.5 to +1.0，否则不动。
```

```
Dimension: evidence_plan
Score: 3
Confidence: 3
Evidence basis: idea-cards.md 第 34-36 行（2x2 + 4 消融 + ANOVA）、第 39-40 行（多指标）、第 41-42 行（多基线）显示完整性高；但第 48 行「11 天内做不出完整多种子论文」、第 50 行「可投性：低」，与 execution-contract-v1.md §5「不做完整训练/多种子大实验」、dataset-access-log.md 第 35 行「含 95% CI」直接冲突。
Deduction: 完整性约 4/5、可行性约 2/5，加权为 mixed=3；扣分主要来自「计划所需的多种子 + 等预算 + 强基线复现」与「单次 <=15 分钟冒烟预算」不可兼容，而非计划设计本身缺项。
Repair condition: 把计划显式降级为 I6 式 mini-benchmark（2x2x1 四格 + 固定 seed + 复现方差 + 单格耗时/显存外推），并把「完整多种子」移出本轮、标注为下一周期工作。
Expected score movement: +0.5 dimension-only（3→3.5/4）；对 overall 的影响 <= +0.3，因可行性受硬时间约束压制。
```

```
Dimension: cvpr_fit
Score: 3
Confidence: 3
Evidence basis: idea-cards.md 第 38 行任务为「cogstim lines 时序化、运动方向/looming 合成序列、可选 CIFAR10-DVS」；第 39 行主指标为「固定 synaptic-op 预算下 test accuracy」；venue-review-styles.md 第 66-68 行要求 figures/qualitative examples/failure cases/visual comparisons 作为证据并要求 cross-dataset tests。
Deduction: 主结果为合成刺激 + 效率轴，缺标准真实视觉基准与定性视觉证据/失败案例；「可选 CIFAR10-DVS」为留白；能效/机制归因更贴 NeurIPS/ICLR/AI-for-Science 口味。
Repair condition: 固定至少一个标准事件/时序视觉基准为主结果（非「可选」），补 accuracy-vs-T 曲线、首次判别时刻可视化与 failure cases，并把「结构 x 动力学」结论落到 CV 可度量的效率/精度收益上。
Expected score movement: +0.5 to +1.0 dimension-only（3→4）；overall +0.3 to +0.5，需与 novelty 的修复同时发生才改变 stance。
```

```
Dimension: executability_11d
Score: 2
Confidence: 4
Evidence basis: execution-contract-v1.md §4（11-10 注册 / 11-16 全文 / 仅 11 天）与 §5（单次 <=15 分钟 GPU、<=10 GB、不做多种子）；hardware-profile.md 第 36-40 行（12 GB 无法整图 BPTT、必须子图化、官方代码缺 torch_sparse 需兼容性验证）；idea-cards.md 第 50 行自评「低」。
Deduction: 在「11 天冲 CVPR 2027 主会」这一固定前提下，完整 2x2 x 消融 x 多种子 x must-rerun 证据包不可完成；给 2 而非 1 是因为最小冒烟实验（第 45-47 行）本身在预算内可执行。
Repair condition: 解除 11 天约束（延到下一周期）或把交付单元收窄为 mini-benchmark + 明确负结果下位结论；同时先跑冒烟验证基线兼容性。
Expected score movement: 本周期内 dimension-only 基本不动（2）；若解除时间约束并给出可复现 mini-grid，+1.0 to +1.5（2→3/3.5），overall +0.5 to +1.0。
```

**Score-change condition 表（`calibration-and-rank.md` 第 112-120 行）**

| Change | Condition | Likely affected dimensions | Expected movement |
|:---|:---|:---|:---|
| Raise score | 冒烟确认 must-rerun 可复现 + 等 synaptic-op 预算下 ANOVA 交互显著并带 95% CI | novelty, evidence_plan, cvpr_fit | +0.5 to +1.0 overall |
| Lower score | 官方基线因 torch_sparse 缺失不可复现，或 2x2 交互项不显著且无可归因增益 | novelty, baselines, evidence_plan | -0.5 to -1.0 overall 或转 NO-GO |
| No quick change | 补齐全规模多种子 + 标准真实视觉基准 + 定性证据（需新实验/新周期） | evidence_plan, executability_11d | 2026-11-16 前 unlikely |

## Top strengths

1. **可归因的机制级设计，而非再一个 backbone**（`idea-cards.md` 第 34-37 行）：2x2 受控 `{生物图, 4 随机图} x {无状态, LIF, ALIF}` + 双因素 ANOVA 交互项 + 4 个隔离消融（去泄漏 / 打乱递质符号 / 固定增益 / 打乱时间顺序）+ 明确证伪条件，把「结构」与「动力学」拆成可独立检验的因子，正对 `prior-art-dedup-log.md` 第 11 行允许的「机制级交互归因」差异轴。这是本轮卡片里最硬的科学设计（漏斗第 186 行亦标 I1「机制最硬」）。
2. **差异化轴与去重结论对齐、未踩「换数据集」红线**（第 43-44 行）：明确把比较轴从 wiring cost 换到 spike/energy、相对 P2 增加「可训练 CV 任务 + 受控 2x2 归因」，并声明「不是再跑一次仿真」；对照 `prior-art-dedup-log.md` 第 21 行「只做同一模型 + 换数据集仍会被判 incremental」，I1 至少在主张层面避开了最朴素的 incremental 形态。
3. **强基线矩阵符合顶会底线**（第 41-42 行）：`train-your-fly` must-rerun + 4 随机图 ensemble + spikingjelly LIF + 同参 ANN + CVPR 2026 SpikeTrack 文献对照；满足 `literature-baseline-matrix.md` 第 31 行「不可仅与 ANN toy baseline 比较」。
4. **工程风险被显式识别且给出缓解路径**（第 45-48 行）：主动标注 166k 节点 BPTT 显存爆炸并要求「必须子图化」、τ/阈值/surrogate 超参敏感、冒烟先记录显存/耗时/spike 率；与 `hardware-profile.md` 第 36-37 行结论一致，非掩蔽风险。

## Major-fatal concerns

> 每条均绑定具体句子或冻结输入中已核验的 URL；severity 按 `universal-review-rubric.md` 第 66-77 行 Fatal-Risk Triage。

| # | Severity | Concern | Evidence basis | Affected criterion | Fix class | Owner skill |
|:---|:---|:---|:---|:---|:---|:---|
| F1 | **fatal** | 时间线 / 预算与所需证据包不可兼容：完整 2x2 x 消融 x 多种子 x must-rerun 在 11 天内不可交付 | `idea-cards.md` 第 48 行「11 天内做不出完整多种子论文」、第 50 行「11 天可投性：低」；`execution-contract-v1.md` §4（11-16 AOE，11 天）与 §5（单次 <=15 分钟、不做多种子大实验）；`dataset-access-log.md` 第 35 行要求 95% CI | Evidence / evaluation；Executability | 收窄交付单元或延周期（scope change） | `f-guidance-builder-v1`（筛选循环）/ 复评 `ccf-paper-reviewer` |
| F2 | **fatal** | must-rerun 基线在本机可能不可复现，等 synaptic-op 预算与 4 随机图 ensemble 对比前提未成立 | `hardware-profile.md` 第 38-40 行「官方 pin torch 2.6 / PyG 2.6 / torch-sparse 0.6.18；本机 dyg-cold torch 2.11 / PyG 2.8，**缺 torch_sparse**，直接复现官方代码需兼容性验证」；`literature-baseline-matrix.md` 第 8、26-27 行把该基线定为 must-rerun；https://github.com/eudald-seeslab/train-your-fly | Reproducibility；strongest baseline / comparison | 冒烟首先验证 + 等价替代方案 | 冒烟执行（`execution-contract-v1.md` §2 授权） |
| F3 | **fatal** | 中心增量「结构 x 动力学超可加交互」可证伪且可能为负；若交互不显著，相对 2610.10023 塌缩为 incremental | `idea-cards.md` 第 33、36 行（以「双因素 ANOVA 交互不显著」为证伪条件）、第 49 行「只差加了时间维可能被判 incremental」；https://arxiv.org/abs/2610.10023；`prior-art-dedup-log.md` 第 18-21 行 contemporaneous 加审 | Novelty / positioning；central claim evidence | 预先接受负结果下位结论 + 定量交互效应量 | `ccf-paper-reviewer` 复评 |
| M1 | major | 「匹配」假设与 LIF 训练细节未定义：τ 与 motif 尺度无定量关系，surrogate gradient / reset / 阈值未给 | `idea-cards.md` 第 31-32 行「假设生物图的 ON/OFF 分叉、前馈-反馈 motif 与膜时间常数 τ 之间存在匹配」；第 48 行「τ、阈值、surrogate gradient 超参敏感」 | Technical soundness | 补可操作定义与配置 | `f-research-v1`（选定后） |
| M2 | major | 缺标准真实视觉基准与 CV 定性证据；「可选 CIFAR10-DVS」为留白 | `idea-cards.md` 第 38 行；`venue-review-styles.md` 第 66-68 行（figures / qualitative examples / failure cases / cross-dataset tests 作为证据） | Venue fit；Evidence | 固定主基准 + 补 failure cases | `ccf-paper-writer`（仅编辑动作，非本轮生成论文） |

## Writing and presentation concerns

被评对象是 idea 卡片，本节只评「贡献可恢复性 / 术语稳定性 / claim-evidence 可见性」，**不改写 idea、不生成论文文本**（`reviewer-panel.md` Writing/Clarity Reviewer 职责；`universal-review-rubric.md` 第 41-46 行）。

1. 「**匹配**」未经界定（第 31-32 行）：「ON/OFF 分叉、前馈-反馈 motif 与膜时间常数 τ 之间存在匹配」是中心机制词，但卡片未给出可测量量（τ 与 motif 路径长度？传播步数？）。若进入写作阶段，读者无法重建该假设的证伪条件——与第 36 行的 ANOVA 证伪条件不在同一可操作层级。
2. 「**超可加交互 / 退化为可加**」（第 33 行）与「**固定 synaptic-op 预算下 test accuracy**」（第 39 行）分属统计结论与工程指标，卡片未说明二者如何映射到同一张结果表；claim-evidence 可见性依赖后续补一张明确的「因子 x 指标」对照表。
3. **预算术语双轨**：G4 第 43 行称「把比较轴从 wiring cost 换成 spike/energy」，但第 39-40 行仍并列「参数量/突触操作数」与「spike rate」，写作阶段需统一主预算口径，否则等预算公平性不可复核（`dataset-access-log.md` 第 36 行亦并列两套预算）。
4. **贡献单元与任务单元错位**：第 37 行声明贡献是「机制结论而非 backbone」，但第 38 行任务清单以「可选」承载 CIFAR10-DVS；负结果下位结论（见 Likely stance B）在卡片中未预留表述位置，易被读者默认读成「必然正向」。

## Format-venue concerns

- **Contemporaneous 引用义务**（已核验）：`prior-art-dedup-log.md` 第 18-21 行 + `execution-contract-v1.md` §4 要求必须引用讨论 arXiv:2610.10023（2026-10-08），高度相似会受额外审查；I1 与该文同模型族，主会投稿的 Related Work 必须逐条列出差异轴，否则触发 novelty 加审。
- **补充材料与素材截止**（已核验）：`execution-contract-v1.md` §4 给 Supplementary 2026-11-23；多种子、消融、accuracy-vs-T 曲线、spike rate 表需规划进 suppl，卡片第 39-40 行的次指标目前无载体规划。
- **Visual evidence 作为证据**（`venue-review-styles.md` 第 66-68 行）：CVPR 要求 figures / qualitative examples / failure cases / visual comparisons 作为证据而非装饰，并 penalize 缺 failure analysis；I1 卡片未规划任何定性可视化、时序脉冲栅图或失败案例，是 venue-facing 缺口。
- **注册门槛**（已核验）：Registration 2026-11-10 AOE（`execution-contract-v1.md` §4）早于全文，属流程硬门槛而非科学问题，但 11 天窗口内不可忽略。
- 主文页数 / 双盲细则：本轮冻结输入未逐条核验，列入 Unresolved，不写死数值。

## Multi-reviewer panel

四位审稿人在综合前独立给分，Lens 不同、不强行制造分歧或夸奖（`review-output-standards.md` 第 29-38 行；`reviewer-panel.md` 第 1-5 行）。

```
Reviewer: R1 — 连接组 / 神经科学专家
Lens: 生物图作为稀疏骨架的合理性、递质符号、视叶子图切分、ON/OFF 与前馈-反馈 motif 的生物学真实性
Score tendency: 6.0/10 (borderline positive)
Confidence: 0.72
Main positive signal: 边权 = syn_count x 递质符号(±) x 可学习增益、以 FlyWire/MaleCNS 真实连接组为骨架（idea-cards.md 第 28 行），并与 P3/Reiser 视叶 ON/OFF 组织一致（literature-baseline-matrix.md 第 14 行）；硬件风险被显式子图化（第 45-48 行）。
Main negative signal: 「ON/OFF 分叉、前馈-反馈 motif 与 τ 之间存在匹配」（第 31-32 行）是无生物学/动力学预证据的猜想；且 <=20k 节点视叶子图切分（第 45 行）可能恰好切断长程反馈 motif，抹掉所声称的机制。
Evidence basis: idea-cards.md 第 28-32、45-48 行；https://arxiv.org/abs/2609.01330（连接组 + SNN + 视觉刺激已做仿真）。
Score-change condition: 若给出 τ 与 motif 尺度的定量匹配预测并被冒烟数据支持 → ≈6.8；若子图化后反馈环被切断且无替代 → ≈5.0。
```

```
Reviewer: R2 — SNN / 脉冲动力学专家
Lens: LIF/ALIF 实现、surrogate gradient、BPTT 显存、tau/阈值超参、spike rate 指标有效性
Score tendency: 4.8/10 (weak reject)
Confidence: 0.70
Main positive signal: 明确把无状态 tanh 换成 LIF/ALIF、T 步输入、Kenyon 脉冲计数读出（第 29-30 行）；「去掉泄漏 tau->inf」消融（第 35 行 a）能隔离膜时间常数贡献；spikingjelly 在 dyg-cold 可用（hardware-profile.md 第 28 行）。
Main negative signal: tau/阈值/surrogate gradient 超参敏感（第 48 行自认）；166k 节点 BPTT 显存爆炸（第 48 行）；T=8/batch=4 的 30 步冒烟（第 46-47 行）远不足判断 LIF 稳定收敛；未给 surrogate 函数、reset 机制、阈值自适应配置。
Evidence basis: idea-cards.md 第 29-30、35、46-48 行；hardware-profile.md 第 36-40 行。
Score-change condition: 冒烟确认 <=20k 子图 T=8 在 12 GB 内且补 surrogate/reset 配置 → ≈5.8；若 OOM 或 spike 率饱和/全零 → ≈3.5 或 fatal。
```

```
Reviewer: R3 — CV 架构 / 效率专家（CVPR reviewer taste）
Lens: 相对 2610.10023 的 novelty、真实视觉基准、效率轴、定性证据、venue fit
Score tendency: 4.5/10 (weak reject)
Confidence: 0.68
Main positive signal: 把比较轴从 wiring cost 换到 spike/energy 并设「固定 synaptic-op 预算下 test accuracy」为主指标（第 39、43 行），是 CVPR「Efficient and scalable vision」可解释的效率结论；差异轴与 prior-art-dedup-log.md 第 11 行允许轴对齐。
Main negative signal: 主任务是 cogstim lines 时序化 + 运动/looming 合成序列（第 38 行），非标准 CV 基准；「可选 CIFAR10-DVS」为留白；相对 https://arxiv.org/abs/2610.10023 只差「加时间维 + 脉冲状态」（第 49 行自认）易判 incremental 且属 contemporaneous 加审；无定性可视化/failure case 规划（venue-review-styles.md 第 66-68 行）。
Evidence basis: idea-cards.md 第 38-43、49 行；https://arxiv.org/abs/2610.10023；prior-art-dedup-log.md 第 18-21 行。
Score-change condition: 等 synaptic-op 预算下给出交互效应量 + 至少一个标准事件视觉基准 + failure cases → ≈6.0；若仅复现 P1 + 加脉冲 → 维持 ≈4.0 或更低。
```

```
Reviewer: R4 — 实验 / 统计与复现专家
Lens: 2x2 设计、ANOVA 交互项、多种子/CI、等预算公平性、基线可复现性
Score tendency: 5.2/10 (borderline)
Confidence: 0.74
Main positive signal: 2x2 受控 + 双因素 ANOVA 交互项 + 明确证伪条件（第 34-36 行）是本轮最可归因的设计；4 个额外消融（第 35 行）能隔离机制；强基线含 must-rerun（第 41 行）符合 literature-baseline-matrix.md 第 26-31 行。
Main negative signal: 多种子 95% CI（dataset-access-log.md 第 35 行）与 execution-contract-v1.md §5「不做多种子大实验」直接冲突；must-rerun 官方代码缺 torch_sparse 未验证（hardware-profile.md 第 38-40 行），等预算对比前提未成立；「固定 synaptic-op 预算」未定义计数口径（是否含脉冲稀疏度/读出层）。
Evidence basis: idea-cards.md 第 34-42 行；dataset-access-log.md 第 35-37 行；hardware-profile.md 第 38-40 行；execution-contract-v1.md §5。
Score-change condition: 冒烟验证基线兼容 + 给出 synaptic-op 计数定义 + 固定 seed 的 3 种子 mini-grid → ≈6.0；若基线不可复现 → ≈4.0。
```

**Panel synthesis**

```
Agreement: 四位一致认为「2x2 + ANOVA 交互项 + 隔离消融」的机制级归因是 I1 的真实强项，且一致认为 11 天 / 12 GB / 基线兼容性使完整多种子证据包当前不可得；无人认为当前形态达到 CVPR 主会 GO 门槛（>=6.5 且无致命风险）。
Disagreement: R1（神经科学 Lens）给 6.0 borderline positive，R2/R3 给 4.5-4.8 weak reject；差异来自 Lens 权重（生物骨架合理性 vs 工程可实现性 / venue 增量），不是对同一证据的矛盾解读，符合「不强行制造分歧」。
Decisive accept axis: 结构 x 动力学超可加交互在等 synaptic-op 预算下显著（ANOVA 交互项 + 效应量 + 95% CI），使相对 2610.10023 存在非 incremental 的机制结论，R3 的增量质疑即被解除。
Decisive reject axis: must-rerun 基线在本机不可复现、交互项不显著、或 11 天无法产出多种子证据包——任一成立即无法支撑 CVPR 主会；strongest unresolved concern = 时间线 x 基线可行性 x 交互符号（reviewer-panel.md 第 110 行不得平均掉致命缺陷）。
Unresolved evidence: 交互效应量（无实验）、官方代码在 dyg-cold 的兼容性（未实跑）、「匹配」假设的可测量定义（未给）、标准视觉基准结果（「可选」）。
Final calibrated stance: REVISE，overall 5.4；由最强未解决弱点而非四维均值决定。保留科学价值但当前形态不可投主会。
```

## Concern-to-action table

| Concern | Severity | Evidence basis | Affected criterion | Action | Owner | Score-impact condition |
|:---|:---|:---|:---|:---|:---|:---|
| F1 时间线/预算不可兼容 | fatal | `idea-cards.md` 第 48、50 行；`execution-contract-v1.md` §4-§5 | Evidence, Executability | 交付单元收窄为 I6 式 mini-benchmark，或全文延到下一周期；本标注明 underpowered | `f-guidance-builder-v1` | 收窄后 evidence_plan +0.5；解除时间约束后 executability_11d +1.0~1.5 |
| F2 must-rerun 基线可能不可复现 | fatal | `hardware-profile.md` 第 38-40 行；`literature-baseline-matrix.md` 第 8、26-27 行；https://github.com/eudald-seeslab/train-your-fly | Reproducibility, Baselines | 冒烟第一步验证 import/复现；若失败给出等价 4 随机图 ensemble 替代并记录 stdout | 冒烟执行 | 验证通过 baselines 保持 4；失败则 baselines -1 且转 NO-GO |
| F3 交互可能为负致 incremental | fatal | `idea-cards.md` 第 33、36、49 行；https://arxiv.org/abs/2610.10023；`prior-art-dedup-log.md` 第 18-21 行 | Novelty, Central claim | 预先写入负结果下位结论；结果报告交互效应量 + CI 而非只报主效应 | `ccf-paper-reviewer` 复评 | 交互显著 novelty 3→4；不显著且无下位结论 → NO-GO |
| M1 「匹配」/LIF 配置未定义 | major | `idea-cards.md` 第 31-32、48 行 | Soundness | 给出 tau 与 motif 尺度定量关系、surrogate/reset/阈值配置 | `f-research-v1`（选定后） | Soundness 4 维持或 +0.5 |
| M2 缺标准基准与定性证据 | major | `idea-cards.md` 第 38 行；`venue-review-styles.md` 第 66-68 行 | Venue fit, Evidence | 固定一个标准事件视觉基准 + 补 accuracy-vs-T 可视化与 failure cases | `ccf-paper-writer`（仅编辑动作） | cvpr_fit 3→4，overall +0.3~0.5 |

**最小冒烟实验判定（硬性要求 #5）：GO（值得跑）**

- 理由：第 45-47 行的冒烟是唯一能在 <=15 分钟 / <=10 GB 预算内同时验证**三个硬门槛**的低成本动作——(a) 官方 `train-your-fly` 在 `dyg-cold` 能否 import/复现（F2 前提，`hardware-profile.md` 第 38-40 行）；(b) <=20k 视叶子图上 LIF T=8 / batch=4 的显存与单步耗时（`hardware-profile.md` 第 36-37 行）；(c) 生物图 vs 1 随机图 30 步训练的 loss 是否下降且曲线可分（`idea-cards.md` 第 46-47 行）。三者都是 REVISE 能否继续的**决策相关**信号，成本与信息量匹配，故 GO。
- **可证伪失败信号**（任一出现即触发 NO-GO 复评）：官方 `train-your-fly` 因缺 `torch_sparse` / torch 2.11 与 PyG 2.8 版本差无法 import 或复现；或 LIF 前向在 12 GB 内 OOM、单步 >15 分钟；或生物图与随机图 30 步 loss 曲线在 spike 率非退化的前提下无可分辨差距。注意：loss 下降**不等于**交互成立，冒烟只验证可行性/可分性，不产出机制结论。

## Recommended next CCFA owner

本轮是 idea-screening round（`execution-contract-v1.md` §3），**不**在本阶段生成 `guidance.md`、不生成论文文本、不写 rebuttal。

- **立即下一步（本轮内）**：执行 I1 最小冒烟实验（`execution-contract-v1.md` §2 授权），记录真实 stdout/stderr、显存、单步耗时、spike 率、30 步 loss 曲线；这是 `f-guidance-builder-v1` 筛选循环「冒烟 → 复评」步。冒烟失败即按 §7「失败即淘汰并记录，不许事后改写目标」处理。
- **若冒烟通过且出现正向可分信号**：另起带标题目录，交 `f-guidance-builder-v1` 重走 canonical gates 生成 `guidance.md`，再按 §3 交 `f-research-v1`；期间用 `ccf-paper-reviewer` 对收窄后的 mini-benchmark 复评（REVISE → 再判）。
- **若交互不显著 / 只有部分正向结果**：按 I6 的「负结果同样有效」路径交付下位结论（`idea-cards.md` 第 167-168 行），交 `ccf-paper-reviewer` 复评，不升格为机制发现。
- **明确不路由**：`ccf-rebuttal-writer`（用户禁止 rebuttal）、`ccf-paper-writer` 生成论文文本（用户禁止）；写作章节仅作编辑动作登记。

## Checks run

- 已调用 Skill `ccf-paper-reviewer`（scientific）；已读取 `SKILL.md` 输出契约及 `review-output-standards.md`、`universal-review-rubric.md`、`calibration-and-rank.md`、`reviewer-panel.md`、`venue-review-styles.md`。
- 已读取全部 6 个冻结输入：`idea-cards.md`、`prior-art-dedup-log.md`、`literature-baseline-matrix.md`、`dataset-access-log.md`、`hardware-profile.md`、`execution-contract-v1.md`。
- 已核对 front matter 字段齐全、类型合法（overall 一位小数、confidence 两位小数、scores 六键 1-5、fatal_risks/go_conditions 为字符串数组、review_execution 固定值）。
- 已核对判定规则：overall 5.4 < 6.5 且有未解决致命风险 → 非 GO；REVISE 合规。
- 已核对 15 个章节标题与用户指定顺序逐项一致；表格分隔符与每行列数一致。
- 已核对 4 个 <=3 分数均含 Deduction / Repair condition / Expected score movement；表 B 7 维无跳过。
- 已核对 panel 4 个独立角色（>=3）含全部指定字段 + 6 项 synthesis。
- 已核对每条 concern 绑定 idea 行号或冻结输入已核验 URL；无「需要更多实验」类泛泛语。
- 独立性：未读取 `idea-I3-review.md` / `idea-I5-review.md`，未与 I2 报告交叉校准。
- **未做**：未重新联网检索、未运行任何实验、未核验任何代码/数据可下载性、未生成任何实验结果或数值、未编造引用。

## Unresolved or unverified

- arXiv:2609.01330 标注「Has Code（本轮未核验直链）」（`literature-baseline-matrix.md` 第 9 行）；BrainTrace / Reiser 期刊页「本轮未核验」（第 14-15 行）；flyvis 神经活动响应数据「暂不作为 G1 依据」（`dataset-access-log.md` 第 25 行）。
- 官方 `train-your-fly` 在 `dyg-cold`（torch 2.11 / PyG 2.8 / 缺 `torch_sparse`）的兼容性**未实跑验证**（`hardware-profile.md` 第 38-40 行）——这是 F2 的关键未决项，只能由冒烟实验闭合。
- CVPR 2027 主文页数、双盲细则、supplementary 具体格式未逐条核验（`execution-contract-v1.md` §4 仅给截止日期与 contemporaneous 规则）；本报告未写死任何页数/匿名条款。
- 物理内存 31.9 GB 来自用户任务描述，`hardware-profile.md` 第 17 行注明 probe 在 Windows 返回 `memory_bytes=null`、未据此推断数值。
- P4 相关「ESA/BioReservoir 更抗过拟合」等陈述（`prior-art-dedup-log.md` 第 14 行）的逐字出处未独立核验；本报告未把它作为 I1 的定量依据。
- 所有 idea **无任何实验结果**；`evidence_plan` 评的是计划质量，不代表结果成立；交互效应量、τ 匹配关系、标准基准结果、spike-op 计数口径均未给。
- 本报告 URL 均为冻结输入中本轮已核验条目的**转引**，未重新访问；若需作为正式引用，须按 `execution-contract-v1.md` §6 记录重新核对。

## Output self-check

1. 章节顺序：Mode → Venue and assumptions → Paper summary → Likely stance and calibrated score → Quantitative scorecard → Top strengths → Major-fatal concerns → Writing and presentation concerns → Format-venue concerns → Multi-reviewer panel → Concern-to-action table → Recommended next CCFA owner → Checks run → Unresolved or unverified → Output self-check，**15 项齐全且顺序一致** ✓
2. 表格：表 A/B、score-change、Major-fatal、Concern-to-action 均为合法 Markdown 分隔符、每行同列数 ✓
3. 内部一致：overall 5.4 由 6 维均值 6.3 减去致命风险约 0.9 得到；confidence 0.70 对应 Scholarly Confidence 3/5；verdict REVISE 与「<6.5 + 有致命风险」一致 ✓
4. <=3 分数（novelty 3 / evidence_plan 3 / cvpr_fit 3 / executability_11d 2）逐个含 Deduction、Repair condition、Expected score movement；移动区间保守、无接受概率表述 ✓
5. Panel：4 角色独立成块、字段齐全、未强行制造分歧或夸奖；synthesis 含 Agreement / Disagreement / Decisive accept axis / Decisive reject axis / Unresolved evidence / Final calibrated stance ✓
6. 每条 concern 绑定具体行号或已核验 URL（https://arxiv.org/abs/2610.10023 等）；无泛泛「需要更多实验」 ✓
7. 硬性要求 #4：明确回答「相对 arXiv:2610.10023 增量是否足以撑起 CVPR 主会 = 不足以（当前形态）」，并给 3 档诚实下位结论 ✓
8. 硬性要求 #5：最小冒烟实验判定 GO + 三个可证伪失败信号 ✓
9. 无 TBD / TODO / 空标题 / 占位符；无编造结果、数值、引用；未把计划写成已观测 ✓
10. 未写 rebuttal、未修改 idea、未生成论文文本； Bullet 语法并列、中文标点统一、因果链「问题→理由→后果→动作」显式 ✓
