---
idea_id: I2
overall: 4.6
confidence: 0.66
verdict: NO-GO
scores: {novelty: 2, mechanism: 3, evidence_plan: 2, baselines: 3, cvpr_fit: 3, executability_11d: 2}
fatal_risks: ["新颖性边界未解决：prior-art-dedup-log.md 第 14 行 P4 记载 ESA/BioReservoir 已提出『连接组拓扑比随机 reservoir 更抗过拟合』，idea-cards.md 第 187 行漏斗点名 I2『与 P4 泛化结论边界模糊』为最可能被 CCF 判致命；idea-cards.md 第 70-71 行仅写『需明确写清这一区别』，未给出可核验的区分证据。", "实证型机制易被『生物结构 约等于 任意稀疏图』证伪：idea-cards.md 第 62-64、74 行要求度分布匹配但 motif 打乱的随机图对照，若生物图鲁棒性优势落在 95% CI 内、或只在合成腐蚀出现而在真实腐蚀/对抗上消失（第 63 行），中心贡献整体塌缩；且该决定性对照被列为『另需』补做（第 64 行），不在 {生物图,随机图} x {无状态,LIF} 主 2x2 消融内（第 62 行）。", "11 天 + 单次 <=15 分钟预算下实验矩阵不可完成：{生物图,随机图} x {无状态,LIF} + 度匹配对照 + 高斯/亮度/遮挡腐蚀 + FGSM/PGD + ResNet-18/小 ViT 上界 + SNN 对抗训练『若时间允许』 + 多种子 95% CI；execution-contract-v1.md §5 禁止多种子大实验，idea-cards.md 第 75-76 行自评『11 天内工作量大』『低-中』。"]
go_conditions: ["用可核验证据严格界定与 P4 的区别：证明『输入腐蚀鲁棒性』不是『过拟合/泛化』结论的重述，且在真实腐蚀/对抗（非仅合成高斯噪声）上结论成立（对应 idea-cards.md 第 63、70-71 行）。", "把度分布匹配 motif 打乱对照纳入主 2x2 消融并报告 95% CI，排除『只是稀疏所以鲁棒』；定义 FGSM/PGD 的扰动范数与迭代预算，补齐标准 corruption benchmark 协议。", "解除 11 天约束（换周期）或把实验矩阵收窄到单一决定性对照 + 收敛后多种子；在此之前不作为 CVPR 2027 主会主攻，升到 REVISE 需先满足前两条。"]
review_execution: independent-agent
---

# I2 — Wiring-as-Regularizer 独立评审报告

## Mode

- 模式：`scientific`（独立审稿人 / independent-agent review），非 quick review、非 full/writing 合并评审。
- 被评对象：`ideas/idea-cards.md` 中的 **I2 idea 卡片，不是论文，没有任何实验结果**。
- 依据技能：`ccf-paper-reviewer`（scientific），并遵循 `review-output-standards.md`、`universal-review-rubric.md`、`calibration-and-rank.md`、`reviewer-panel.md`、`venue-review-styles.md`。
- 证据口径：因无实验，`evidence_plan` 评的是「**证据计划的可行性与完整性**」，不把计划写成已观测结果；本报告不编造任何数值、消融结论、实验结果或引用。
- 独立性：本报告与 `idea-I1-review.md` 相互独立，未读取同目录下 `idea-I3-review.md` / `idea-I5-review.md`，未做跨 idea 分数对齐或平均；`verdict: NO-GO` 是 I2 自身证据的结论，不是为与 I1 制造差异。
- 边界：不写 rebuttal、不修改 idea、不生成论文文本。

## Venue and assumptions

| 项 | 取值与证据 |
|:---|:---|
| Venue | CVPR 2027 **主会**（顶会，非 workshop / 非期刊 Q2 放水）。venue family = CVPR/ICCV/ECCV；主评分维度 = novelty / technical quality / empirical validation / visual evidence / clarity / fair comparison（`venue-review-styles.md` 第 60-69 行）。鲁棒性是 CVPR 成熟主题，但数字须配强基线与多种子。 |
| 时间线 | 当前 2026-11-05；Registration 2026-11-10 AOE、Submission 2026-11-16 AOE、Supplementary 2026-11-23（`execution-contract-v1.md` §4，来源 https://cvpr.thecvf.com/Conferences/2027/CallForPapers）；距全文仅 **11 天**。 |
| Contemporaneous 规则 | 2026-09-15 后上线论文视为 contemporaneous，须引用讨论、高度相似加审；arXiv:2610.10023（2026-10-08）落入该窗口（`prior-art-dedup-log.md` 第 18-21 行；https://arxiv.org/abs/2610.10023）。 |
| 硬件 / 运行信封 | RTX 3060 12 GB（空闲约 10.8 GB）、12 逻辑核、CUDA 12.8、磁盘约 547 GB（`hardware-profile.md` 第 9-17 行）；`dyg-cold`：torch 2.11+cu128 / PyG 2.8.0.post1 / spikingjelly / cv2（第 28 行）。12 GB 无法对 166k 神经元整图做长序列 BPTT（第 36-37 行）。冒烟预算：单次 <=15 分钟 GPU、<=10 GB、下载 <=1.5 GB、**不做完整训练/多种子大实验**（`execution-contract-v1.md` §5）。用户任务描述另给 31.9 GB RAM，但 `hardware-profile.md` 第 17 行注明 probe 返回 null、未据此推断数值。 |
| 基线兼容性 | 官方 `train-your-fly` pin torch 2.6.0 / PyG 2.6.1 / **torch-sparse 0.6.18**；本机缺 `torch_sparse`，「直接复现官方代码需兼容性验证」（`hardware-profile.md` 第 38-40 行）。 |
| 数据 | G1 全部 PASS 可直下（`dataset-access-log.md`）；cogstim 8 类 512x512 PNG、`--seed` 可复现（https://github.com/eudald-seeslab/cogstim）；公开任务含颜色/形状/数量/朝向（第 30-32 行）；标准规模每类 5000/5000/5000、95% CI（第 33-35 行）。 |
| 大方向锁定 | GNN + SNN + 果蝇连接组 + 视觉；不得漂到纯神经科学仿真或纯图表示学习（`execution-contract-v1.md` §4）。 |
| 竞争工作（URL 均转引自本轮检索记录） | arXiv:2610.10023 / `train-your-fly`（must-rerun，https://arxiv.org/abs/2610.10023、https://github.com/eudald-seeslab/train-your-fly）；arXiv:2609.01330（https://arxiv.org/abs/2609.01330）；Nature 2024 flyvis（https://www.nature.com/articles/s41586-024-07939-3）；**P4 簇**：BrainTrace / BioReservoir / ESA reservoir / MaleCNS X-ray 博客 / JEPA-on-connectome（`prior-art-dedup-log.md` 第 14 行；https://github.com/igdigitallab/bioreservoir）。 |
| 冻结输入 | 已读全部 6 个：`idea-cards.md`、`prior-art-dedup-log.md`、`literature-baseline-matrix.md`、`dataset-access-log.md`、`hardware-profile.md`、`execution-contract-v1.md`。 |
| 评审假设 | 判断基于卡片文本 + 冻结输入；**未重新联网、未运行任何实验、未核验任何代码/数据可下载性**。所有 URL 为本轮检索记录中的已核验条目转引，非本报告重新访问。 |

## Paper summary

被评对象是 idea 卡片而非论文，无实验章节；本节概括其**主张与计划**（均为「计划」，非「结果」）：

- **瓶颈**（第 58-59 行）：SNN 视觉的抗腐蚀/对抗鲁棒性通常靠额外训练技巧或集成；连接组的稀疏、重尾度分布、反馈环、ON/OFF 双通路是「**免费**」的结构冗余，但没有人把它与 LIF 的时间去噪联合量化。
- **机制**（第 60-61 行）：生物图稀疏连通限制扰动传播路径、反馈环提供复现/纠错、ON/OFF 分离提供差分冗余；LIF 阈值 + 泄漏对输入噪声做时间低通；二者叠加应降低对高斯噪声、亮度漂移、遮挡、FGSM/PGD 的敏感度。
- **可证伪消融**（第 62-64 行）：等 spike 率 / 等参数量下比较 `{生物图, 随机图} x {无状态, LIF}`；若生物图鲁棒性优势落在 95% CI 内，或只在合成腐蚀上出现、在真实腐蚀/对抗上消失，机制被证伪；另需排除「只是稀疏所以鲁棒」：加入度分布匹配但 motif 打乱的随机图。
- **贡献类型**（第 65 行）：实证型机制发现 + 鲁棒性 benchmark 结论。
- **任务/指标**（第 66-67 行）：cogstim `shapes/colours/ans` + 腐蚀集；主指标 = 干净/腐蚀准确率落差（relative drop、mCE 风格）；次指标 = 对抗鲁棒精度、spike rate 变化。
- **强基线**（第 68-69 行）：`train-your-fly`、随机图 ensemble、ResNet-18 / 小 ViT（ANN 上界）、SNN + 对抗训练（**若时间允许**）。
- **G4 定位**（第 70-71 行）：P1/P2 都没做扰动鲁棒性；但 ESA/BioReservoir 已提出「连接组拓扑比随机 reservoir 更抗过拟合」——那是**过拟合/泛化**而非**输入腐蚀鲁棒性**，且没有 CVPR 级视觉基准；「需明确写清这一区别」。
- **最小冒烟**（第 72-73 行）：生物图 vs 随机图，在 `shapes` 上加 3 档高斯噪声，各跑 30 步训练，比较干净/噪声准确率差与 spike 率。
- **自评风险**（第 74-76 行）：容易被质疑「生物结构 ≈ 任意稀疏图」，需度分布匹配对照才有说服力；CVPR 对鲁棒性数字要求强基线与多种子；11 天内工作量大；「11 天可投性：低-中」。

## Likely stance and calibrated score

- **Likely stance**：weak reject（`calibration-and-rank.md` 第 45-47 行：lean/weak reject 通常 4）。6 维均值 2.5/5 = 5.0/10，因决定性拒绝轴（novelty 边界 + 实证塌缩，`reviewer-panel.md` 第 110 行不得平均掉致命缺陷）下调 0.4 → **4.6**。
- **Overall**：`4.6 / 10`。**Confidence（front matter）**：`0.66`。**Scholarly Confidence**：`3/5`（结构化卡片 + 完整冻结输入 + 已核验 URL，但无论文主体/appendix/代码/结果；且 I2 的关键 novelty 判断依赖 P4 主张的**转述**而非独立核验原文，证据可得性略低于 I1）。**Verdict**：`NO-GO`。
- **判定规则核对**：overall 4.6 < 6.5，且存在 3 条未解决致命风险 → 不可 GO；有致命风险必须 NO-GO 或 REVISE。
- **为何 NO-GO 而非 REVISE**（独立判断，非与 I1 制造差异）：I1 的致命风险主要是**执行/时间线 + 结论符号**，可用「收窄交付单元 + 延周期 + 负结果下位结论」修复；I2 的决定性拒绝轴是 **novelty 边界（与 P4 泛化结论区分）** 与 **实证型贡献在度匹配对照下可能整体塌缩**——两者都需要**新的文献区分证据 + 新的决定性对照结果**才能闭合，属于「重做定位或换单元」，在 11 天 CVPR 2027 主会前提下不可修复；`idea-cards.md` 第 187 行漏斗亦把 I2 列入「最可能被 CCF 判致命」。故本轮淘汰该方向，而非判修订。

**硬性回答 A：相对 arXiv:2610.10023，这个增量是否足以撑起 CVPR 主会？**

**不足以（当前形态），且比 I1 更弱。** 2610.10023 已做「生物图 vs 4 随机图在等布线预算下的准确率对比」（`prior-art-dedup-log.md` 第 11 行；https://arxiv.org/abs/2610.10023）。I2 的增量是「换到输入腐蚀/对抗鲁棒性这一任务族 + 加 LIF 时间去噪」（第 60-67、70 行），属 `prior-art-dedup-log.md` 第 11 行允许的「新任务族」轴。问题有二：

1. **增量落在「同一对照换了个指标轴」**：主消融仍是 `{生物图, 随机图} x {无状态, LIF}`（第 62 行），与 P1 的 `{生物图, 4 随机图} x 无状态 GNN` 是同一对照结构的扩展；相对 P1 只多一个「腐蚀集」与一个 LIF 因子。若生物图优势最终落在 95% CI 内（第 63 行自设证伪条件），则增量归零。
2. ** novelty 被 P4 夹击**：`prior-art-dedup-log.md` 第 14 行已记「连接组拓扑比随机 reservoir 更抗过拟合」，I2 主张「连接组拓扑更抗输入腐蚀」在缺少严格区分证据时，CVPR 主会审稿人最可能读作「把泛化/鲁棒性结论换皮到一个新扰动集」，与漏斗第 187 行「与 P4 泛化结论边界模糊」一致。卡片第 71 行只写「需明确写清这一区别」，把**决定性的定位工作**推迟到写作阶段，而非在 idea 层解决。

因此当前增量**不足以**撑起主会；只有当「度分布匹配 motif 打乱」对照证明生物图显著优于任意稀疏图，且在真实腐蚀/对抗上保持、并与 P4 的泛化结论有可核验区分时，增量才成立。

**硬性回答 B：若只有部分正向结果，诚实可发表的下位结论是什么？**

按第 62-64 行证伪条件，可诚实交付的三档下位结论（均为**待验证的计划性表述，非已观测**）：

1. **最强可保结论（度匹配对照抹平优势）**：「连接组拓扑在输入腐蚀下的表观鲁棒性可由**度分布/稀疏度**解释，ON/OFF、反馈环等 motif 不提供超出任意稀疏图的额外鲁棒性。」——这直接证伪 I2 的中心机制，但作为负结果对「生物接线是否有特权」的讨论有用，须降级为 workshop / mini-benchmark 附表的负结果，不能称机制发现。
2. **次强（仅合成高斯噪声显著、真实腐蚀/对抗消失）**：「LIF 阈值+泄漏的时间低通只对加性高斯噪声有效，对亮度漂移/遮挡/PGD 无稳健收益。」——此时贡献退化为「SNN 在合成噪声上的验证」，与第 63 行证伪条件直接对应，须如实标注「合成-only、不可外推」。
3. **最弱（30 步冒烟只有可分趋势）**：只能交付「生物图 vs 随机图在 `shapes` 加噪下的**未收敛**趋势 + spike 率」，明确标注 underpowered、单种子、无 CI，**不得**写成「生物结构带来鲁棒性」。

任何情况下都**不得**把「干净/噪声准确率差较小」写成「生物结构提供免费正则化」——那是把计划写成结果，且与第 63 行的 95% CI 门槛冲突。

## Quantitative scorecard

表 A（front matter 指定的 6 个决策维度）与表 B（`calibration-and-rank.md` 第 85-102 行**强制**的 7 维通用 scorecard）维度命名不同、分数独立给出；语义对应：mechanism→Soundness、evidence_plan→Evidence、baselines→Evidence/Reproducibility、cvpr_fit→Significance、executability_11d 为时间线新增维度。

**表 A — 决策维度**

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|:---|:---:|:---:|:---|:---|
| novelty | 2 | 3 | `idea-cards.md` 第 70-71、187 行；`prior-art-dedup-log.md` 第 14 行 P4 | 与 P4 泛化结论边界模糊、漏斗点名最可能致命；修复见 D1 |
| mechanism | 3 | 3 | `idea-cards.md` 第 60-64 行 | 机制合理但四组件未隔离归因、决定性对照「另需」补做；修复见 D2 |
| evidence_plan | 2 | 4 | `idea-cards.md` 第 62-69、75-76 行；`execution-contract-v1.md` §5 | 计划未收敛（「若时间允许」「另需」）+ 矩阵过大不可行；修复见 D3 |
| baselines | 3 | 3 | `idea-cards.md` 第 68-69 行；`literature-baseline-matrix.md` 第 31 行 | 有 ANN 上界是亮点，但 must-rerun 未验、攻击预算未定义、上界基线留白；修复见 D4 |
| cvpr_fit | 3 | 3 | `idea-cards.md` 第 66-67 行；`venue-review-styles.md` 第 66-68 行 | 鲁棒性主题 fit，但合成数据非标准 corruption benchmark、mCE 为借用术语；修复见 D5 |
| executability_11d | 2 | 4 | `execution-contract-v1.md` §4-§5；`idea-cards.md` 第 75-76 行 | 11 天 + 单次 <=15 分钟 + 多种子禁止 → 矩阵不可完成；修复见 D6 |

**表 B — 强制通用 scorecard**

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|:---|:---:|:---:|:---|:---|
| Novelty | 2 | 3 | `idea-cards.md` 第 70-71、187 行 | 须先与 P4 严格区分，否则 novelty collapse |
| Soundness | 3 | 3 | 第 60-64 行机制链与证伪条件 | 四机制组件未隔离、类比性断言无预证据 |
| Evidence | 2 | 4 | 无任何实验结果；`execution-contract-v1.md` §5 禁止多种子大实验 | 证据为空且计划含 2 处未收敛留白，修复后上限低于 I1 |
| Significance | 3 | 3 | `prior-art-dedup-log.md` 第 11-12 行「新任务族」真空 | 若边界厘清有社区价值，若塌缩则转负结果 |
| Clarity | 4 | 4 | 第 54-76 行结构完整、证伪条件具体（95% CI / 合成 vs 真实） | 卡片本身可恢复性好；「mCE 风格」等术语需落地 |
| Reproducibility | 3 | 4 | 第 68、72-73 行；`hardware-profile.md` 第 38-40 行 | must-rerun 兼容性未验、FGSM/PGD 预算未定义 |
| Ethics / Limitations | 4 | 4 | 第 74-76 行自列风险；`dataset-access-log.md` 全公开许可 | 无人类受试/敏感数据；限制披露诚实 |

**Overall:** 4.6/10 | **Scholarly Confidence:** 3/5 | **Recommendation:** weak-reject | **Verdict:** 与 P4 边界厘清 + 度匹配对照显著 + 收敛后多种子可升 REVISE；度匹配对照抹平优势或只在合成噪声显著则维持 NO-GO。

**<=3 分数的扣分 / 修复 / 预期移动（硬性要求 #1；I2 六个维度全部 <=3，逐项给出）**

```
Dimension: novelty
Score: 2
Confidence: 3
Evidence basis: prior-art-dedup-log.md 第 14 行 P4「ESA/BioReservoir 已提出连接组拓扑比随机 reservoir 更抗过拟合」；idea-cards.md 第 70-71 行自述该区别「需明确写清」但未给证据；第 187 行漏斗把 I2 列为「最可能被 CCF 判致命...与 P4 泛化结论边界模糊」。
Deduction: 「输入腐蚀鲁棒性」与「泛化/过拟合」的区分目前只是一句定位声明，没有可核验的判据（不同指标？不同扰动模型？不同失效模式？）；contemporaneous 加审 + P4 夹击下，novelty 与 close prior work 的差别不清，命中 universal-review-rubric.md 第 22 行 2 分档。
Repair condition: 给出逐字文献证据界定 P4 的具体结论（过拟合/泛化在何种指标、何种数据上），并证明 I2 的输入腐蚀/对抗结论在失效模式与指标上不重叠；在 Related Work 中把该区别写成可检验命题而非措辞。
Expected score movement: +1.0 dimension-only（2→3）；若同时有度匹配对照正向结果，可带动 overall +0.5 to +1.0；仅靠措辞澄清不加分。
```

```
Dimension: mechanism
Score: 3
Confidence: 3
Evidence basis: idea-cards.md 第 60-61 行列四个机制组件（稀疏限传播 / 反馈环纠错 / ON/OFF 差分冗余 / LIF 时间低通）；第 62 行主消融仅 {生物图,随机图} x {无状态,LIF} 的 2x2；第 64 行把「度分布匹配但 motif 打乱」写成「另需」补做。
Deduction: 2x2 只能分离「图类型」与「是否有脉冲状态」，无法把四个机制组件各自归因；「复现/纠错」「差分冗余」「免费」是类比性断言、无预证据；且唯一能排除「只是稀疏」的决定性对照被降级为主消融之外的「另需」项，机制可证伪性被削弱。
Repair condition: 把度分布匹配 motif 打乱对照纳入主消融（成为第三/第四格），并补「只去反馈环」「只去 ON/OFF 双路」的隔离消融，使四个组件各自有可观测落点；对「免费」给出相对基线不增参数的定量说明。
Expected score movement: +0.5 to +1.0 dimension-only（3→4）；overall +0.3 to +0.5，需与 novelty 修复共同发生才改变 stance。
```

```
Dimension: evidence_plan
Score: 2
Confidence: 4
Evidence basis: idea-cards.md 第 62-69 行（2x2 + 度匹配对照 + 高斯/亮度/遮挡腐蚀 + FGSM/PGD + ResNet-18/小 ViT 上界 + SNN 对抗训练「若时间允许」）、第 63 行（多种子 95% CI 隐含要求）、第 75-76 行（「工作量大」「低-中」）；execution-contract-v1.md §5「不做完整训练/多种子大实验」；dataset-access-log.md 第 35 行要求 95% CI。
Deduction: 计划本身**未收敛**——「若时间允许」「另需」两处留白意味着核心对照与核心基线未定稿；矩阵规模（腐蚀 x 对抗 x ANN 上界 x 对抗训练 x 度匹配 x 多种子）在单次 <=15 分钟预算下不可完成；完整性与可行性同时偏弱，故 2 分（I1 因完整性高给 3，此处不复制）。
Repair condition: 定稿单一决定性对照（生物图 vs 度匹配 motif 打乱图）并删除「若时间允许」留白；把矩阵收窄为「1 个任务 x 1 个决定性对照 x 收敛后 3 种子 x 干净/腐蚀/对抗 3 档」，其余标注为下一周期。
Expected score movement: +0.5 to +1.0 dimension-only（2→3）；本周期内对 overall 影响 <= +0.3，因受硬时间约束压制。
```

```
Dimension: baselines
Score: 3
Confidence: 3
Evidence basis: idea-cards.md 第 68-69 行列 train-your-fly / 随机图 ensemble / ResNet-18 / 小 ViT / SNN+对抗训练（若时间允许）；hardware-profile.md 第 38-40 行 must-rerun 兼容性未验；literature-baseline-matrix.md 第 31 行「不可仅与 ANN toy baseline 比较」。
Deduction: 有 ANN 上界（ResNet-18 / 小 ViT）是正确方向、优于 toy ANN；但 (a) must-rerun 在本机缺 torch_sparse 未验证，(b) FGSM/PGD 未定义扰动范数/迭代预算/对 SNN 的 surrogate 梯度，(c)「SNN + 对抗训练（若时间允许）」把最强鲁棒性基线变成留白，(d) 未列任何已建立的 corruption/SNN 鲁棒性强基线锚点。
Repair condition: 冒烟先验证 must-rerun；定稿攻击协议（epsilon、迭代数、范数、surrogate）；把「SNN + 对抗训练」从「若时间允许」提为必需基线；补一条同赛道已公开鲁棒性基线作为标尺。
Expected score movement: +0.5 to +1.0 dimension-only（3→4）；overall +0.3 左右。
```

```
Dimension: cvpr_fit
Score: 3
Confidence: 3
Evidence basis: idea-cards.md 第 66-67 行任务为 cogstim shapes/colours/ans + 腐蚀集、指标为 relative drop / 「mCE 风格」；dataset-access-log.md 第 30-32 行确认输入为 512x512 合成 PNG；venue-review-styles.md 第 66-68 行要求 figures / qualitative examples / failure cases / cross-dataset tests。
Deduction: 鲁棒性是 CVPR 主会成熟主题（正向），但数据集是合成形状/颜色/数量、不是标准 corruption benchmark，「mCE 风格」只是借用术语、未定义腐蚀类型与严重度；卡片未规划定性腐蚀样例或 failure cases；贡献为「实证型机制发现」，若效应量小易被判 thin。
Repair condition: 接入至少一个标准 corruption benchmark 为主结果并定义腐蚀类型/严重度；给出干净/腐蚀/对抗的定性视觉对比与 failure cases；把 relative drop / mCE 落到具体可复算表格。
Expected score movement: +0.5 to +1.0 dimension-only（3→4）；overall +0.3 to +0.5。
```

```
Dimension: executability_11d
Score: 2
Confidence: 4
Evidence basis: execution-contract-v1.md §4（11-10 注册 / 11-16 全文 / 仅 11 天）与 §5（单次 <=15 分钟 GPU、<=10 GB、不做多种子）；idea-cards.md 第 75 行「CVPR 对鲁棒性数字要求强基线与多种子；11 天内工作量大」、第 76 行「低-中」；hardware-profile.md 第 36-40 行。
Deduction: 在「11 天冲 CVPR 2027 主会」前提下，含对抗训练 + ANN 上界 + 度匹配对照 + 多种子 CI 的矩阵不可完成；给 2 而非 1 是因为第 72-73 行的 30 步冒烟本身在预算内可跑（但见冒烟判定：信息量不足以改变决策）。
Repair condition: 解除 11 天约束（换周期），或收窄为单一决定性对照 + 收敛后多种子；否则本维度不加分。
Expected score movement: 本周期内 2 不动；解除时间约束并给出可复现决定性对照后 +1.0 to +1.5（2→3/3.5），overall +0.5 左右。
```

**Score-change condition 表（`calibration-and-rank.md` 第 112-120 行）**

| Change | Condition | Likely affected dimensions | Expected movement |
|:---|:---|:---|:---|
| Raise score | 与 P4 边界被逐字证据厘清 + 度匹配 motif 打乱对照在收敛后多种子下显著 + 真实腐蚀/对抗结论保持 | novelty, mechanism, evidence_plan | +0.5 to +1.0 overall（可升 REVISE 带） |
| Lower score | 度匹配对照抹平生物图优势，或优势仅在合成高斯噪声出现 | novelty, mechanism, baselines | -0.5 overall 或维持 NO-GO |
| No quick change | 补齐全规模多种子 + 标准 corruption benchmark + 对抗训练基线（需新周期） | evidence_plan, executability_11d, cvpr_fit | 2026-11-16 前 unlikely |

## Top strengths

> 公平记录真实正向信号，不强行贬低；也不因存在真空而抬升 verdict（`review-output-standards.md` 第 34-35 行）。

1. **扰动鲁棒性在 P1/P2 是真实真空**（`idea-cards.md` 第 70 行；`prior-art-dedup-log.md` 第 11-12 行允许「新任务族」差异轴）：P1 只做等布线预算的干净准确率、P2 是朝向图仿真，都未做输入腐蚀/对抗鲁棒性；这是 I2 相对 2610.10023 最干净的差异化入口。
2. **证伪条件具体且主动识别混淆**（第 62-64 行）：等 spike 率 / 等参数量控制、以 95% CI 为门槛、明确「只在合成腐蚀出现、真实腐蚀/对抗上消失即证伪」、并提出「度分布匹配但 motif 打乱」排除「只是稀疏所以鲁棒」。这种自我证伪意识在 idea 卡片层是加分的。
3. **基线方向正确**（第 68 行）：列入 ResNet-18 / 小 ViT 作为 ANN 上界、SNN + 对抗训练作为鲁棒性强基线，符合 `literature-baseline-matrix.md` 第 31 行「不可仅与 ANN toy baseline 比较」；指标用 relative drop / mCE 风格（第 66-67 行）是 CV 社区通用语言。
4. **贡献单元与 I1 不重叠**（第 65 行）：定位为「实证型机制发现 + 鲁棒性 benchmark 结论」，与 I1 的架构/机制归因贡献构成组合选题的互补，而非重复（漏斗第 186 行把 I6/I1 列为有搞头，I2 被单列为边界模糊，二者不冲突）。

## Major-fatal concerns

> 每条均绑定具体句子或冻结输入中已核验的 URL；severity 按 `universal-review-rubric.md` 第 66-77 行 Fatal-Risk Triage。

| # | Severity | Concern | Evidence basis | Affected criterion | Fix class | Owner skill |
|:---|:---|:---|:---|:---|:---|:---|
| F1 | **fatal** | 新颖性与 P4 泛化结论边界未解决，novelty 可能 collapse | `prior-art-dedup-log.md` 第 14 行 P4「连接组拓扑比随机 reservoir 更抗过拟合」；`idea-cards.md` 第 70-71 行「需明确写清这一区别」（未给证据）、第 187 行漏斗点名 I2「与 P4 泛化结论边界模糊」为最可能被 CCF 判致命；https://github.com/igdigitallab/bioreservoir | Contribution and novelty；Positioning / related work | 需新文献区分证据 + 重新定位 | `ccf-paper-reviewer` 复评 / 文献核验 |
| F2 | **fatal** | 「生物结构 ≈ 任意稀疏图」未排除，实证型贡献可能整体塌缩；决定性对照被降级 | `idea-cards.md` 第 62 行主 2x2 仅 `{生物图,随机图} x {无状态,LIF}`、第 63 行「优势落在 95% CI 内即证伪」、第 64 行度匹配 motif 打乱对照写作「**另需**」补做、第 74 行自认「容易被质疑生物结构 ≈ 任意稀疏图」 | Central claim evidence；Evaluation protocol | 把决定性对照纳入主消融 | `f-research-v1`（选定后）/ 冒烟 |
| F3 | **fatal** | 实验矩阵在 11 天 / 单次 <=15 分钟 / 禁止多种子下不可完成 | `idea-cards.md` 第 62-69 行（腐蚀 x 对抗 x ANN 上界 x 对抗训练「若时间允许」 x 度匹配 x 多种子）、第 75-76 行；`execution-contract-v1.md` §4-§5；`dataset-access-log.md` 第 35 行 95% CI | Evidence and evaluation；Executability | 收窄矩阵或延周期 | `f-guidance-builder-v1`（筛选循环） |
| M1 | major | 四个机制组件未隔离归因，类比性断言无预证据 | `idea-cards.md` 第 60-61 行「稀疏限制扰动传播 / 反馈环提供复现纠错 / ON/OFF 差分冗余 / LIF 时间低通」；第 62 行 2x2 不足以分离四者 | Technical soundness；Mechanism clarity | 补隔离消融与可操作定义 | `f-research-v1`（选定后） |
| M2 | major | 攻击/腐蚀协议未定义、合成数据非标准 corruption benchmark | `idea-cards.md` 第 61、66-67 行「FGSM/PGD」「mCE 风格」未给扰动范数/迭代/严重度；`dataset-access-log.md` 第 30-32 行输入为 cogstim 合成 512x512；`venue-review-styles.md` 第 66-68 行 | Reproducibility；Venue fit | 定稿协议 + 接标准 benchmark | `ccf-paper-writer`（仅编辑动作，非本轮生成论文） |

## Writing and presentation concerns

被评对象是 idea 卡片，本节只评「贡献可恢复性 / 术语稳定性 / claim-evidence 可见性」，**不改写 idea、不生成论文文本**。

1. 「**免费**的结构冗余」「**复现/纠错**」「**差分冗余**」「**时间低通**」（第 58-61 行）是类比性措辞，卡片未给可测量量；它们与第 63 行的 95% CI 证伪条件不在同一可操作层级，读者无法把四个词映射到结果表的一行。
2. 「**mCE 风格**」（第 66-67 行）为借用术语，未定义腐蚀类型、严重度档位与聚合方式；「**relative drop**」与「**对抗鲁棒精度**」并列为主/次指标，但未说明二者是否同一测试集口径，claim-evidence 可见性弱。
3. **决定性定位被推迟到写作阶段**：第 71 行「需明确写清这一区别」把与 P4 的区分留给未来文本，而卡片当前没有可重建该区分的证据；第 64 行「另需」、第 69 行「若时间允许」两处留白使「贡献单元边界」不稳定，读者无法确定哪些对照是承诺、哪些是备选。
4. **正负主张并存未对齐**：第 60 行「生物图的稀疏连通限制扰动传播路径」与第 74 行「容易被质疑生物结构 ≈ 任意稀疏图」是同一命题的正反两面，卡片未把它们对应到同一张对照表；若进入写作，须以「度匹配」一列同时承载二者。

## Format-venue concerns

- **Contemporaneous 引用义务**（已核验）：`prior-art-dedup-log.md` 第 18-21 行 + `execution-contract-v1.md` §4 要求必须引用讨论 arXiv:2610.10023（2026-10-08）；I2 与该文共用 `{生物图, 随机图}` 对照结构，Related Work 须逐条区分，否则触发 novelty 加审。
- **鲁棒性论文的 evidence 形态**（`venue-review-styles.md` 第 66-68 行）：CVPR 要求 figures / qualitative examples / failure cases / visual comparisons 作为证据并 penalize 缺 failure analysis；I2 卡片未规划任何干净/腐蚀/对抗的定性视觉对比或失败案例，是 venue-facing 缺口。
- **对抗鲁棒数字可复核性**：`idea-cards.md` 第 61、67 行提 FGSM/PGD 与「对抗鲁棒精度」但未定义扰动范数、迭代预算或对 SNN 的梯度替代；CVPR 主会评审无法据此复核数字。
- **补充材料与素材截止**（已核验）：`execution-contract-v1.md` §4 给 Supplementary 2026-11-23；腐蚀集、多种子、spike rate 表需规划进 suppl，卡片第 66-67 行次指标无载体规划。
- **注册门槛**（已核验）：Registration 2026-11-10 AOE（`execution-contract-v1.md` §4）早于全文，属流程硬门槛。
- 主文页数 / 双盲细则：本轮冻结输入未逐条核验，列入 Unresolved，不写死数值。

## Multi-reviewer panel

四位审稿人在综合前独立给分，Lens 不同、不强行制造分歧或夸奖（`review-output-standards.md` 第 29-38 行；`reviewer-panel.md` 第 1-5 行）。

```
Reviewer: R1 — 连接组 / 神经科学专家
Lens: 稀疏/重尾度/反馈环/ON/OFF 的生物学真实性，以及与 P4 reservoir 结论是否同一现象
Score tendency: 4.6/10 (weak reject)
Confidence: 0.66
Main positive signal: 生物图稀疏连通、反馈环、ON/OFF 双通路（idea-cards.md 第 58-60 行）是有生物学依据的结构冗余；卡片第 70-71 行主动区分「输入腐蚀鲁棒性」与 P4「过拟合/泛化」，未把两者混为一谈。
Main negative signal: prior-art-dedup-log.md 第 14 行 P4 已记「连接组拓扑比随机 reservoir 更抗过拟合」，漏斗第 187 行点名 I2 边界模糊最可能致命；「反馈环提供复现/纠错」「ON/OFF 分离提供差分冗余」（第 60 行）是类比性断言，无机制隔离与预证据。
Evidence basis: idea-cards.md 第 58-60、70-71、187 行；prior-art-dedup-log.md 第 14 行；https://github.com/igdigitallab/bioreservoir。
Score-change condition: 若给出可核验的、与 P4 不重叠的定量定义 + 度匹配对照结果 → ≈5.6；若边界仍只靠措辞 → ≈4.0。
```

```
Reviewer: R2 — SNN / 脉冲动力学专家
Lens: LIF 阈值+泄漏作为时间低通、等 spike 率公平性、FGSM/PGD 对 SNN 的适用性与 surrogate 梯度
Score tendency: 4.4/10 (weak reject)
Confidence: 0.68
Main positive signal: 「LIF 阈值 + 泄漏对输入噪声做时间低通」（第 61 行）是可检验的物理机制；「等 spike 率 / 等参数量」（第 62 行）主动控制了脉冲率这一混淆变量。
Main negative signal: FGSM/PGD 对脉冲网络的梯度需 surrogate，「对抗鲁棒精度」（第 67 行）在 SNN 上的定义与实现未给；「若生物图鲁棒性优势落在 95% CI 内……机制被证伪」（第 63 行）意味着中心贡献可能整体塌缩；LIF 时间低通与「生物图结构冗余」的叠加未在 2x2 之外单独归因。
Evidence basis: idea-cards.md 第 61-67 行；hardware-profile.md 第 28 行（spikingjelly 可用）。
Score-change condition: 定义攻击预算 + surrogate + 收敛后多种子 → ≈5.4；若 LIF 低通被证明只吃加性高斯噪声 → ≈4.0 或更低。
```

```
Reviewer: R3 — CV 架构 / 效率专家（CVPR reviewer taste）
Lens: 鲁棒性基准、ANN 上界、真实 vs 合成腐蚀、相对 2610.10023 的 venue 增量
Score tendency: 4.3/10 (weak reject)
Confidence: 0.65
Main positive signal: 列入 ResNet-18 / 小 ViT 作为 ANN 上界（第 68 行）对鲁棒性论文方向正确；relative drop / mCE 风格（第 66-67 行）是 CV 社区通用指标；P1/P2 未做鲁棒性（第 70 行）确为真空。
Main negative signal: 数据是 cogstim 合成 shapes/colours/ans（第 66 行；dataset-access-log.md 第 30-32 行），非标准 corruption benchmark；「mCE 风格」仅为借用术语、未定义腐蚀类型/严重度/协议；CVPR 要求 visual comparisons / failure cases（venue-review-styles.md 第 66-68 行）而卡片无规划；相对 https://arxiv.org/abs/2610.10023 只是「同一 {生物图,随机图} 对照 + 腐蚀集 + LIF 因子」，易判 incremental。
Evidence basis: idea-cards.md 第 62、66-70 行；https://arxiv.org/abs/2610.10023；venue-review-styles.md 第 60-69 行。
Score-change condition: 接入标准 corruption benchmark + 定性腐蚀样例/failure case + 定量交互或增量表 → ≈5.5；否则维持 ≈4.2。
```

```
Reviewer: R4 — 实验 / 统计与复现专家
Lens: 度匹配对照、95% CI、多种子、证伪条件的决定性、实验矩阵可行性
Score tendency: 4.0/10 (weak reject / reject 边界)
Confidence: 0.72
Main positive signal: 「若优势落在 95% CI 内、或只在合成腐蚀出现而在真实腐蚀/对抗上消失，机制被证伪」（第 63 行）与「加入度分布匹配但 motif 打乱的随机图」（第 64 行）给出了具体、可执行的证伪条件，优于泛泛的「做更多实验」。
Main negative signal: 度匹配对照被写成「另需」补做（第 64 行）、不在主 2x2（第 62 行）内，**决定性对照被降级**；「SNN + 对抗训练（若时间允许）」（第 69 行）是留白；30 步训练（第 72-73 行冒烟）远未收敛，无法支撑 relative drop；矩阵（腐蚀 + 对抗 + ANN 上界 + 对抗训练 + 度匹配 + 多种子 CI）在单次 <=15 分钟预算下不可完成（execution-contract-v1.md §5，第 75-76 行自认）。
Evidence basis: idea-cards.md 第 62-64、69、72-76 行；execution-contract-v1.md §5；dataset-access-log.md 第 35 行。
Score-change condition: 把度匹配对照纳入主消融 + 收敛后多种子 + 收窄矩阵 → ≈5.0；若 30 步冒烟被用来下结论 → ≈3.5。
```

**Panel synthesis**

```
Agreement: 四位一致认为「扰动鲁棒性」在 P1/P2 是真实真空、且证伪条件写得具体；同时一致认为与 P4 的边界未被当前卡片解决、度匹配 motif 打乱对照被降级为「另需」、以及 11 天矩阵不可行；无人认为当前形态达到 CVPR 主会 GO 门槛。
Disagreement: R1 因「卡片主动区分 P4」（第 70-71 行）给相对最高 4.6，R4 因决定性对照被降级 + 矩阵不可行给最低 4.0；差异来自 Lens 权重（生物学合理性 vs 统计决定性/可行性），不是对同一证据的矛盾解读，符合「不强行制造分歧」。
Decisive accept axis: 度分布匹配 motif 打乱的随机图在收敛后多种子下，生物图的 relative drop 显著更优（超出 95% CI），且优势在真实腐蚀/对抗上保持，并与 P4 泛化结论有可核验区分 → 「不是任意稀疏图」成立，novelty 与机制同时立住。
Decisive reject axis: 与 P4 泛化结论无法严格区分 / 度匹配对照抹平优势 / 优势只在合成高斯噪声出现 / 11 天无法产出多种子 → 任一成立即塌缩；strongest unresolved concern = novelty 边界（漏斗第 187 行点名）+ 实证型贡献在决定性对照下可能为负（reviewer-panel.md 第 110 行不得平均掉致命缺陷）。
Unresolved evidence: 度匹配对照结果、真实腐蚀/对抗结果、与 P4 的逐字区别证据、FGSM/PGD 攻击预算定义、收敛后多种子结果。
Final calibrated stance: NO-GO，overall 4.6；由决定性拒绝轴（novelty 边界 + 实证塌缩）决定，不因「鲁棒性是真空」这一正向信号被平均掉。
```

## Concern-to-action table

| Concern | Severity | Evidence basis | Affected criterion | Action | Owner | Score-impact condition |
|:---|:---|:---|:---|:---|:---|:---|
| F1 与 P4 边界未解决 | fatal | `prior-art-dedup-log.md` 第 14 行；`idea-cards.md` 第 70-71、187 行；https://github.com/igdigitallab/bioreservoir | Novelty, Positioning | 补逐字文献证据界定 P4 结论边界，把区别写成可检验命题；否则本方向淘汰 | `ccf-paper-reviewer` 复评 | 厘清后 novelty 2→3；仅措辞澄清不加分 |
| F2 决定性对照被降级 / 实证塌缩 | fatal | `idea-cards.md` 第 62-64、74 行 | Central claim, Evaluation | 把度分布匹配 motif 打乱对照纳入主 2x2，报告 95% CI；预先写入塌缩时的负结果下位结论 | `f-research-v1`（选定后）/ 冒烟 | 对照显著 mechanism 3→4；抹平优势则维持 NO-GO |
| F3 实验矩阵 / 11 天不可完成 | fatal | `idea-cards.md` 第 62-69、75-76 行；`execution-contract-v1.md` §4-§5 | Evidence, Executability | 收窄为「1 任务 x 1 决定性对照 x 3 种子 x 3 档扰动」或延周期；删除「若时间允许」留白 | `f-guidance-builder-v1` | 收窄后 evidence_plan +0.5~1.0；解除时间约束 executability_11d +1.0~1.5 |
| M1 四机制组件未隔离 | major | `idea-cards.md` 第 60-62 行 | Soundness | 补「只去反馈环」「只去 ON/OFF 双路」隔离消融与可测量定义 | `f-research-v1`（选定后） | Soundness 3→4 |
| M2 攻击/腐蚀协议未定义 | major | `idea-cards.md` 第 61、66-67 行；`venue-review-styles.md` 第 66-68 行 | Reproducibility, Venue fit | 定稿 FGSM/PGD 范数/迭代/surrogate；接标准 corruption benchmark + 定性 failure cases | `ccf-paper-writer`（仅编辑动作） | cvpr_fit 3→4、baselines 3→4 |

**最小冒烟实验判定（硬性要求 #5）：NO-GO（本轮不值得把有限冒烟预算投给它）**

- 理由：第 72-73 行的冒烟是「生物图 vs 随机图、`shapes` 加 3 档高斯噪声、各跑 30 步训练、比较干净/噪声准确率差与 spike 率」。它存在三处与决策不匹配的缺陷：(a) **30 步远未收敛**，未收敛的「干净/噪声准确率差」无法区分「机制成立」与「只是没训练好」；(b) 冒烟只含「随机图」而**不含第 64 行的度分布匹配 motif 打乱对照**，即不触及 F2 这个决定性对照，跑完仍无法排除「只是稀疏」；(c) 它**完全不触及 F1（与 P4 的 novelty 边界）** 这一决定性拒绝轴——那是文献/定位问题，不是 GPU 能产出的信号。在 `execution-contract-v1.md` §5 的有限预算下，其优先级低于能同时验证基线兼容性与可行性的 I1 冒烟（见 I1 报告），故判 NO-GO。**NO-GO 仅指「本轮不投入预算」，不主张「永不验证」**；若升到 REVISE 重评，应先重写冒烟为「收敛后 + 度匹配对照 + 多种子」再跑。
- **可证伪失败信号**（若仍决定跑，对应第 62-64 行的证伪条件）：度分布匹配但 motif 打乱的随机图与生物图在收敛后的干净/噪声准确率差（relative drop）落在 95% CI 内；或生物图的鲁棒性优势仅在合成高斯噪声档出现、在遮挡 / 亮度漂移 / FGSM 上消失；或生物图与随机图 30 步 loss 曲线在 spike 率非退化前提下无可分辨差距。任一出现即机制被证伪，方向应淘汰（`execution-contract-v1.md` §7「失败即淘汰并记录，不许事后改写目标」）。

## Recommended next CCFA owner

本轮是 idea-screening round（`execution-contract-v1.md` §3），**不**在本阶段生成 `guidance.md`、不生成论文文本、不写 rebuttal；且本方向 verdict 为 **NO-GO**。

- **本轮处置**：不进入论文写作 / 复现链。按 `execution-contract-v1.md` §1 用户原话「实验不理想就换 idea」，I2 作为 CVPR 2027 主会主攻方向本轮淘汰，并按 §7 记录淘汰理由（novelty 边界 + 决定性对照降级 + 11 天矩阵不可行），不事后改写目标。
- **低成本保留路径（非立项）**：把「腐蚀鲁棒性」作为一格对照并入 I1 / I6 的 mini-benchmark（`idea-cards.md` 第 179 行 I6「可以作为 I1 的副产品先交付一个 mini-benchmark」），用同一套度匹配控制顺带收集，不单独立项、不单独占冒烟预算。
- **若坚持保留**：先补齐 (1) 与 P4 的逐字文献区分证据、(2) 度匹配对照纳入主消融的设计、(3) 攻击与腐蚀协议定义，再交 `ccf-paper-reviewer` 以 **REVISE** 重评；重评通过后才交 `f-guidance-builder-v1` 走 canonical gates。
- **明确不路由**：`ccf-rebuttal-writer`（用户禁止 rebuttal）、`ccf-paper-writer` 生成论文文本（用户禁止）；写作/格式章节仅作编辑动作登记。

## Checks run

- 已调用 Skill `ccf-paper-reviewer`（scientific）；已读取 `SKILL.md` 输出契约及 `review-output-standards.md`、`universal-review-rubric.md`、`calibration-and-rank.md`、`reviewer-panel.md`、`venue-review-styles.md`。
- 已读取全部 6 个冻结输入：`idea-cards.md`、`prior-art-dedup-log.md`、`literature-baseline-matrix.md`、`dataset-access-log.md`、`hardware-profile.md`、`execution-contract-v1.md`。
- 已核对 front matter 字段齐全、类型合法（overall 一位小数、confidence 两位小数、scores 六键 1-5、fatal_risks/go_conditions 为字符串数组、review_execution 固定值）。
- 已核对判定规则：overall 4.6 < 6.5 且有 3 条未解决致命风险 → 非 GO；NO-GO 合规，并写明「为何 NO-GO 而非 REVISE」。
- 已核对 15 个章节标题与用户指定顺序逐项一致；表格分隔符与每行列数一致。
- 已核对 **6 个 <=3 分数全部**含 Deduction / Repair condition / Expected score movement；表 B 7 维无跳过。
- 已核对 panel 4 个独立角色（>=3）含全部指定字段 + 6 项 synthesis。
- 已核对每条 concern 绑定 idea 行号或冻结输入已核验 URL；无「需要更多实验」类泛泛语。
- 独立性：未读取 `idea-I1-review.md` / `idea-I3-review.md` / `idea-I5-review.md` 的内容做分数对齐；I2 结论由自身证据独立得出。
- **未做**：未重新联网检索、未运行任何实验、未核验任何代码/数据可下载性、未生成任何实验结果或数值、未编造引用。

## Unresolved or unverified

- **对 I2 决定性**：P4「ESA/BioReservoir 已提出连接组拓扑比随机 reservoir 更抗过拟合」的**逐字出处未独立核验**，来自 `prior-art-dedup-log.md` 第 14 行转述 + https://github.com/igdigitallab/bioreservoir（`literature-baseline-matrix.md` 第 19 行仅列「MaleCNS 固定 reservoir + LIF」）。F1 的最终判定依赖该文献证据；本报告按「边界未解决」保守处理，未把 P4 主张当作已证事实引用为定量依据。
- arXiv:2609.01330「Has Code（本轮未核验直链）」（`literature-baseline-matrix.md` 第 9 行）；BrainTrace / Reiser 期刊页「本轮未核验」（第 14-15 行）；flyvis 神经活动数据「暂不作为 G1 依据」（`dataset-access-log.md` 第 25 行）。
- 官方 `train-your-fly` 在 `dyg-cold`（torch 2.11 / PyG 2.8 / 缺 `torch_sparse`）的兼容性**未实跑验证**（`hardware-profile.md` 第 38-40 行）。
- FGSM/PGD 的扰动范数、迭代预算、对 SNN 的 surrogate 梯度，以及「mCE 风格」的腐蚀类型/严重度/聚合方式，卡片均未定义（`idea-cards.md` 第 61、66-67 行）。
- CVPR 2027 主文页数、双盲细则、supplementary 具体格式未逐条核验（`execution-contract-v1.md` §4 仅给截止日期与 contemporaneous 规则）；本报告未写死任何页数/匿名条款。
- 物理内存 31.9 GB 来自用户任务描述，`hardware-profile.md` 第 17 行注明 probe 返回 `memory_bytes=null`、未据此推断数值。
- 所有 idea **无任何实验结果**；`evidence_plan` 评的是计划质量，不代表结果成立；度匹配对照结果、真实腐蚀/对抗结果、收敛后多种子、spike 率变化均未给。
- 本报告 URL 均为冻结输入中本轮已核验条目的**转引**，未重新访问；若需作为正式引用，须按 `execution-contract-v1.md` §6 记录重新核对。

## Output self-check

1. 章节顺序：Mode → Venue and assumptions → Paper summary → Likely stance and calibrated score → Quantitative scorecard → Top strengths → Major-fatal concerns → Writing and presentation concerns → Format-venue concerns → Multi-reviewer panel → Concern-to-action table → Recommended next CCFA owner → Checks run → Unresolved or unverified → Output self-check，**15 项齐全且顺序一致** ✓
2. 表格：表 A/B、score-change、Major-fatal、Concern-to-action 均为合法 Markdown 分隔符、每行同列数 ✓
3. 内部一致：overall 4.6 由 6 维均值 5.0 减去决定性拒绝轴约 0.4 得到；confidence 0.66 略低于 I1 的 0.70（因 F1 依赖 P4 转述而非独立核验）；verdict NO-GO 与「<6.5 + 致命风险 + 修复需重做定位」一致 ✓
4. <=3 分数（6 个维度全部）逐个含 Deduction、Repair condition、Expected score movement；移动区间保守、无接受概率表述 ✓
5. Panel：4 角色独立成块、字段齐全、未强行制造分歧或夸奖；synthesis 含 Agreement / Disagreement / Decisive accept axis / Decisive reject axis / Unresolved evidence / Final calibrated stance ✓
6. 每条 concern 绑定具体行号或已核验 URL（https://arxiv.org/abs/2610.10023、https://github.com/igdigitallab/bioreservoir 等）；无泛泛「需要更多实验」 ✓
7. 硬性要求 #4：明确回答「相对 arXiv:2610.10023 增量是否足以撑起 CVPR 主会 = 不足以（且比 I1 更弱）」，并给 3 档诚实下位结论 ✓
8. 硬性要求 #5：最小冒烟实验判定 NO-GO（含「不投入预算 ≠ 永不验证」的限定） + 三个可证伪失败信号 ✓
9. 无 TBD / TODO / 空标题 / 占位符；无编造结果、数值、引用；未把计划写成已观测；Top strengths 公平记录正向信号、未强行贬低 ✓
10. 未写 rebuttal、未修改 idea、未生成论文文本；Bullet 语法并列、中文标点统一、因果链「问题→理由→后果→动作」显式 ✓
