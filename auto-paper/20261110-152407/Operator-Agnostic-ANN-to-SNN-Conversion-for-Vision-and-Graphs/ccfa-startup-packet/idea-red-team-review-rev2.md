## Verdict first:

本评审为**第二次独立 idea 红队评审**（与第一次不同的评审会话；standard 模式，依据 `ccf-idea-reviewer/SKILL.md` 及 `references/strict-idea-review.md`、`rubric.md`、`calibration.md`、`expert-panel.md`、`../ccf-common/references/review-output-standards.md`）。评审对象为单篇 idea：rev2 主卡 `idea-cards-rev2.md`（OAC-rev2）。第一次报告 `idea-red-team-review.md` 原文完整保留、不被本评审修改或抬分。本报告内所有专家意见、严格评审意见均为**本红队 panel 基于 idea 文本、第一次报告与用户提供的 prior-art 事实作出的独立判断**，不代表任何真实审稿人、meta-review、录用记录或录用概率；不承诺任何分数变化、审稿行为或录用结果。未执行公开检索，未生成任何 URL / DOI / 实验结果数值。

**结论（先给）**：按 rev2 指定的 **IEEE TNNLS / Q1–Q2 类脑与神经网络期刊档**评，当前 formulation 仍**不具备可接收性**，但**不属于应 abandon 的情形**。相对 rev1（第一次 `**Overall:** 2.5`/5 = 5.0/10）有**实质但有限**的进步：F1 在主张层被真正消解，F3 在设计层被消解，venue 主动对齐，T1/T2 + κ_n 把 novelty 从"纯重述/组合"推进为"薄但真实、可证伪的分析判据"。但三条最重的弱点未闭合：① 核心贡献（理论判据）的严格推导、`‖A‖` 误差上界、κ_n 单调性证明、两解码兼容性、冗余消融**全部处于 M0 实验前纸面待办**，一个以理论判据为核心贡献的 idea 其核心定理尚未证；② T1/T2/κ_n 更接近"放宽 ρ=1 假设后对已知恒等式做代数展开"的产物，"prior-art 无法得到的新推论"这一高标准不成立，且该推论层 novelty 未经针对检索；③ 视觉侧仍无任何正式实验（按用户硬要求，guidance 阶段只评 evidence plan 可信度，不把"零实验"自动判 fatal，但如实记录证据缺口），且 `matched-protocol.md` 未成文、PASCAL/TPP/CS-QCFS/ECL 仍待自行复现、一处可证伪条件存在范畴错位。

加权总分 `**Overall:** 3.2`（1–5 加权尺度，保留一位小数；对应 1–10 尺度约 6.3）。推荐值：**`pivot-with-rescue-route`**（5 选 1）。当前就绪度：low；发展潜力：medium。**关键：3.2 独立落在 `calibration.md` 的 3.0–3.6 段，本推荐由分数段直接得出，不依赖任何 fatal gate 的压顶，也不是把分数抬到 `revise`/`accept-to-develop` 段。** 相对第一次的 +0.7 见 Weighted final score 字段的逐维分解；该变化来自 venue 标尺降级、F1 主张层消解、F3 设计层消解、T1/T2 有限增量与"零实验不判 fatal"这条用户硬要求，**不来自"因为这是修订版就默认更高"**。

**F1 / F2 / F3 逐条判定（先给，完整依据见 Serious blockers 字段）**

| Fatal | 判定 | 一句话依据 |
| --- | --- | --- |
| F1 主张—适用条件错位 | **已解决** | 中心问题收窄到与适用条件 A1/A2 完全一致，禁用 "Operator-Agnostic" 掩盖性命名，原版动态/非线性 ViG 明写为失效边界且不进主结果；bait-and-switch 的结构性矛盾消失。残留的"算子类代表性 / 冻结 KNN 代价"归 Problem importance 扣分，不属 F1。 |
| F2 novelty 重述 / 组合 | **降级为可修复弱点**（最重、最偏 fatal 的一项） | T1/T2/κ_n 把 rev1 的"矩阵记号重述 + 组合"推进为可先验计算、可证伪、含反直觉 ρ-不变性的分析判据，不再是纯重述；但数学深度浅（行和定义 + 尺度抵消）、"一行代数照搬 Deng&Gu 递归" objection 未排除、核心推导全在 M0 未证、推论层未检索、κ_n 与 T2 张力未解。既非"已解决"，也非"仍未解 fatal"。 |
| F3 横评可比性两难 | **降级为可修复弱点** | 可比性两难在设计层被正确消解（所有基线同一批固定骨干 + 同 T/θ/calibration/CL 定义 + 贡献放弃"方法增益"定位，不再用不可比横评支撑方法主张），且 evidence plan 完备；但 "成文 `matched-protocol.md`" 在工件目录中并不存在，PASCAL/TPP/CS-QCFS/ECL 仍为待自行复现的计划，零正式实验，证伪条件范畴错位。均为执行/工件层可修复。 |

**综合 recommendation（5 选 1）：`pivot-with-rescue-route`**。含义：保留最佳要素（T2 的 ρ-不变性 + κ_n 判据 + 统一协议横评 + 失效边界），改变**方法理论**（M0 推导兑现并排除"一行代数" objection）、**证据**（兑现 matched-protocol 工件 + 复现 PASCAL/TPP + 实测 κ_n 单调性）、**novelty 定位**（推论层针对检索 + 接受增量诊断定位）中的至少一组。

---

## Target venue/journal and assumptions:

- **目标**：IEEE TNNLS / Q1–Q2 类脑与神经网络期刊档（rev2 §0 明确）。**本评审按此档评，不再按 CVPR / ICCV / NeurIPS 主会档评**（用户硬要求）。
- **Venue family**：类脑 / SNN 与神经网络期刊向；非 CCF-A 会议族。贡献类型由 rev2 定为「理论判据 + 统一协议横评 + 失效边界」（empirical / diagnostic，接受增量但须充分验证）。
- **领域**：类脑计算 × ANN→SNN 转换的误差分析、校准律适用条件、统一协议横评。
- **标尺声明（关键，防止把降档误读为抬分）**：相对第一次的分数变化，来源可逐条追溯为 (a) venue 标尺从 CCF-A 主会降到 Q1–Q2 期刊、(b) F1 在主张层消解、(c) F3 在设计层消解、(d) T1/T2/κ_n 提供 rev1 没有的可证伪判据、(e) 用户硬要求「视觉侧零实验不自动等同 fatal，只评 evidence plan 可信度」。**以上五条均为可核查的文本事实，不含「因是修订版默认更高」这一项**；`revise` / `accept-to-develop` 段未被触及，推荐仍为 `pivot-with-rescue-route`。
- **评审假设（均由用户提供，本评审不另行假设）**：单卡 RTX 3060 12GB / CUDA 12.8 / torch 2.11，远端 4090 已授权（guidance 阶段不提交）；主战场 CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS、Planetoid 三图；ImageNet-1K 需申请（G2 不可得，rev2 已通过降档处理）；基线 QCFS / FTBC / TPP / Parallel Conversion / DCGS / AdaFire 有官方代码，PASCAL / CS-QCFS / ECL 无代码需自行复现。
- **stage 边界（用户硬要求）**：当前为 guidance / 实验前契约阶段；按 `f-guidance-builder-v1` 只需 evidence plan 可行、机制有可跑路径、最近邻基线可复现。本评审**不把"视觉侧零正式实验"本身自动判 fatal**，但如实评估 evidence plan 是否可信（结论见 Experimental convincibility：plan 完备可信，但含一处未兑现工件与一处逻辑残留）。
- **未发表内部结果的隔离标注（用户硬要求）**：
  1. 「图节点分类 T≤8 达 ANN−1.5pp 带内」一律标注为 **「用户提供的未公开先验（未发表、不充当公开证据）」**，不计入任何证据强度、不计入打分依据、不作为 novelty 支撑。
  2. rev2 卡中出现的「成稿实测」数值（GCN 对称归一化在 Cora 上 ρ_n 最高 5.75；sum 聚合 ρ_n 可达 169；`var(U)=0.082` vs 0.083；`mean(U)=0.481` vs 0.5；θ=1 越界质量 ≤1.01%）以及「成稿 §3.2 已证」「成稿 §5.1 明确记录」等引用，同属**用户提供的未公开先验 / 内部校准**：本 startup packet 工件清单内**无对应成稿文件**，且这些数值与 `claim-evidence-matrix.md`、`strong-result-feasibility-contract.md` 的「全部 `<TBD>`、零实验结果数值」纪律**不一致**。本评审不指控其为编造（属用户提供材料内的陈述），但如实记为内部校准、不进公开证据、不进打分依据，并在 Strict reviewer comments / Evidence 字段要求成文时澄清来源或删除。
- **本评审未做的事**：未核验 TNNLS 等目标期刊当年官方 policy / page limit / review form / deadline（依 `source-notes.md`）；未执行任何公开文献检索；未生成任何 URL / DOI。

---

## Search basis:

- **novelty 状态**：`searched`（按用户硬要求，依据第一次报告与用户提供的、已由独立文献核验得到的 prior-art 结论）。
- **该 `searched` 状态的边界（必须写明）**：
  1. 证据来源为**用户提供的独立文献核验结论**，本评审会话未重新执行公开检索；故严格区分时 closest-work 证据属 `user-provided only`，novelty 判定按用户指令记为 `searched`。二者不矛盾：前者是证据来源，后者是状态标签。
  2. 覆盖边界以第一次报告 8 条 closest-work 与用户列出的核验清单为限：覆盖的是**数学组件归属层**（β*、零期望偏置、精确等式、确定性计数、两阶段、跨 CNN+GCN 归谁）。
  3. **新增边界（本评审指出）**：rev2 的 **T1/T2/κ_n 作为「推论」本身，其 novelty 未经针对该推论的公开检索验证**（例如「非行随机算子上的 conversion bias」「相对误差对聚合尺度不变」「行和/行范数比判据」是否已被 2025–2026 工作给出）。第一次核验的是组件归属，不是推论层。因此依 `strict-idea-review.md`「Cap novelty at 3 if closest work was not searched and novelty is decision-critical」，本评审 **novelty 封顶 3、置信度降为 3**（第一次为 2 / 置信度 5，那是"组件层高重叠"确定时的取值；现在"推论是否超出 prior-art"本身取决于 M0 推导，属未定）。
  4. 依 `privacy-and-evidence.md`，未把未发表的私有 idea 表述放入任何检索查询；依 `source-notes.md`，closest-work 表不提供本轮未核验的链接 / DOI（禁止编造 URL）；不引用 MDPI 来源。
- **literature status label**（checklist #3）：`searched`（novelty 判定用，覆盖组件层）／`user-provided only`（本会话检索动作用）／**推论层 `not searched`**（新增，单独标注）；非 `partially searched`；不做 `high novelty` 断言。
- **public-safe queries**：本会话未执行，无查询记录；如后续需要，按 `strict-idea-review.md` 应以通用公开关键词先行（ANN-to-SNN conversion bias under non-row-stochastic operators / row-sum weighted margin shift / scale-invariance of relative conversion error），不粘贴私有措辞。
- **source policy**：仅使用用户提供的 primary venue/year 信息作为 prior-art 锚点；不把 citation count 当质量；不把推论当事实。

---

## Stage and development potential:

```text
Current conference readiness: low
Development potential: medium
Main reason it is not ready: 核心贡献（理论判据 T1/T2/κ_n）的严格推导、‖A‖ 误差上界、κ_n 单调性证明、两解码兼容性、冗余消融全部处于 M0 实验前纸面待办；视觉侧零正式实验；推论层 novelty 未检索；matched-protocol 工件未兑现。
Best rescue route: 先完成 M0 纸面推导（尤其证明 T1 相对 Deng&Gu 递归的非平凡性、证 κ_n 单调性、解 κ_n 与 T2 张力），再做针对推论层的公开检索，随后按 matched-protocol 优先复现 PASCAL/TPP 并实测 conversion loss–ρ_n/T 曲线；把贡献稳定锚在「可先验计算的何时失效判据 + 统一横评 + 失效边界」的增量诊断定位。
Evidence needed to decide: M0 推导是否兑现 T1/T2 且排除「一行代数照搬」；κ_n 单调性是否成立；推论层检索是否命中近邻；统一协议横评是否显示可归因于该判据的稳定诊断能力。
```

附 development potential 判定（依 `calibration.md`）：medium——最佳要素（ρ-不变性解释、κ_n 判据、统一横评、失效边界）有用且核心问题不再需要重写，但机制 / 证据 / novelty 定位至少一项必须改变并兑现；不是 high（M0 推导存在使 T1 坍缩为已知结论的现实可能，且推论层未检索，尚不能断言"不改核心问题即可变 competitive"），不是 low（不止一个窄片段可复用）。**保持 medium 而非升为 high，是不因"修订版"默认上调的如实取值**；升 high 的条件写在 Confidence 与 Score-change conditions 字段。

---

## Normalized idea:

| 要素 | 归一化内容（rev2） |
| --- | --- |
| Problem | 当传播算子固定、非负、线性但行和 ρ_n ≠ 1 时，为行随机（ρ=1）算子导出的转换校准律（偏置、阈值缩放、量化步长）是否仍最优？中心问题收窄，不再声称覆盖数据依赖 / 动态 / 非线性算子。 |
| Gap | 既有 ANN→SNN 误差分析与校准律几乎全部在行随机、逐元素算子上推导（QCFS / FTBC / TPP / Parallel / DCGS / AdaFire）；ρ_n ≠ 1 的视觉图骨干与图消息传递缺少统一协议下的系统检验与「何时失效」判据。 |
| Root challenge | ρ_n ≠ 1 时，为 ρ=1 导出的零期望偏置 / 阈值缩放不再自动成立；系统误差经 A 传播后如何随行和变化、相对误差是否随之放大，缺少可先验计算、逐节点可检验的刻画。 |
| Insight（声称） | T1：闭环偏置 `β*=θ/(2T)` 与 ρ 无关，但均值误差传播过 A 后 margin 平移为 `ρ_n/(2T)·Σ_h DW_c[h]`，系统项按行和加权；T2：margin Δ_n 由同一聚合 logits 算出，故相对误差由 `‖a_n‖₂‖DW‖₂/(T Δ_n)` 控制、ρ-不变（作者原预测 sum 聚合 ρ≈169 会灾难退化、被实测推翻后给出该解释）；由此定义 `κ_n = ρ_n/‖a_n‖₂`，预测 ρ=1 校准律在 κ_n 大且 T≤4 时系统性欠校准、conversion loss 差距随 ρ_n/T 单调增大，ρ≈1 的标准 CNN 上两者等价（非劣效）。 |
| Method mechanism | 继承精确恒等式 `B̂₂−B₂ = A(E₁W₂)`（Dual-Phase 式）、`β*=θ/(2T)`（Deng&Gu）、零期望偏置（QCFS/FTBC）、膜电位累加解码、确定性精确计数（PASCAL）、两阶段（TPP/SpikeConverter）、跨 CNN+GCN（One-Spike SNN）——**全文不声称发明其中任何一项**。视觉侧冻结 KNN 图、线性化聚合，明写为「构造该算子类成员的手段」；图侧用 GCN 消息传递；原版动态 / 非线性 ViG 明写为失效边界诊断实验（不进主结果、不得删）。 |
| Expected evidence | matched-protocol 统一横评（所有基线含自行复现的 PASCAL/TPP/CS-QCFS/ECL，在同一批固定骨干、同 T/θ/calibration 数据、同 conversion loss 定义下重跑）；T1/T2 浮点残差；conversion loss–ρ_n/T 单调性；κ_n 逐节点可检验性；原版 ViG 失效边界；冻结 KNN 相对原版的性能代价量化（R4）。 |
| Limitation（用户已自认） | 适用类仅为固定、非负、线性算子；M0（一般 A 下 β* 严格推导、`‖A‖` 误差上界、两解码兼容性、冗余消融）未过不得进 P4；视觉侧零正式实验；ImageNet-1K 不可得。 |
| 内部先验（隔离标注） | 图节点分类 T≤8 达 ANN−1.5pp 带内；rev2 「成稿实测」数值与「成稿 §3.2 / §5.1」引用 —— 均为「用户提供的未公开先验 / 内部校准（未发表、不充当公开证据）」，不进入 evidence / 打分依据。 |

---

## Closest prior art table:

按 `strict-idea-review.md` 的 closest-work 字段逐条列出 8 条（达到 3–8 要求上限），依据第一次报告与用户提供的已核验结论，**针对 rev2 重新评估 Overlap / Remaining delta / Needed differentiation**。**Link/source 统一说明**：venue/year 与「已做的事」均来自用户提供的独立文献核验结论，本会话未执行公开检索、未附 URL/DOI，不编造链接；依 `privacy-and-evidence.md` 不将未发表 idea 文本用于查询。

**1**
- Closest work: Deng & Gu
- Venue/year: ICLR 2021
- Link/source: 用户提供的已核验 prior-art 结论（本轮未检索 URL/DOI）
- What it already does: `β* = θ/(2T)` 与逐层误差递归。
- Overlap with user idea: rev2 已明确归功 β*，且 T1 的推导起点 `E[E₁]=β−1/(2T)` 与「把误差经传播算子递推」直接来自该脉络；rev2 的核心恒等式亦是该递归的矩阵写法。
- Remaining novelty delta: T1 声称把递归里的（行随机）归一化矩阵换成一般 A 后给出 ρ_n 加权 margin 偏置。**该 delta 成立与否取决于 M0 推导**：若只是 `A·1 = ρ_n·1` 的直接后果 + 零期望偏置，则为假设放宽后的代数展开，不是新结果。
- Risk to the idea: high
- Needed differentiation: 在 M0 中给出 T1 相对 Deng&Gu 递归的**非平凡性证明**（该结论在 ρ=1 文献中退化消失、且带来其无法给出的可证伪预测），而非仅把归一化 A 换成一般 A。

**2**
- Closest work: QCFS
- Venue/year: ICLR 2022
- Link/source: 同上
- What it already does: 零期望误差偏置。
- Overlap with user idea: T1 的 `E[E₁]=β−1/(2T)` 即该结论，rev2 已归功；T1 的「系统项」正是把这一零均值项经 A 传播后的余数。
- Remaining novelty delta: 仅剩「该余数按 ρ_n 加权」这一观察。
- Risk to the idea: high
- Needed differentiation: 证明「按 ρ_n 加权」带来的不是幅度噪声而是有确定方向的 margin 偏置，且给出 QCFS 在 ρ_n≠1 上失效的可测反例。

**3**
- Closest work: FTBC
- Venue/year: ECCV 2024
- Link/source: 同上
- What it already does: 零期望误差偏置（较新视觉侧版本）。
- Overlap with user idea: 同上；且是 matched-protocol 横评必比基线。
- Remaining novelty delta: 无独立 delta。
- Risk to the idea: medium
- Needed differentiation: 在统一协议下把 FTBC 作为必比基线，展示 ρ_n≠1 上的校准差异。

**4**
- Closest work: Dual-Phase
- Venue/year: IEEE TNNLS 2024
- Link/source: 同上
- What it already does: 膜电位累加解码替代计数读出 + 精确误差等式。
- Overlap with user idea: rev2 继承的精确恒等式 `A(E₁W₂)` 是该「精确等式」在抽象 A 上的写法；解码组件亦归功。
- Remaining novelty delta: 仅剩「把等式推广到 ρ_n≠1 的 A 并读出 T1/T2 两条推论」。
- Risk to the idea: high
- Needed differentiation: 给出 Dual-Phase 等式在 ρ=1 下读不出、在 ρ_n≠1 下才出现的推论（即 T2 的 ρ-不变性解释），并数值验证。

**5**
- Closest work: PASCAL
- Venue/year: TMLR 2025
- Link/source: 同上
- What it already does: 确定性精确计数。
- Overlap with user idea: rev2 已放弃「确定性化」作为贡献，改列为横评第一批 must-rerun 基线并自行复现。
- Remaining novelty delta: rev2 相对 PASCAL 不再主张数学组件 delta；但 **§1 可证伪条件第 4 条仍写「与 PASCAL / TPP 等价 → 判据被推翻 / pivot」，这是从 rev1「新方法」定位继承的范畴错位残留**（见 Serious blockers W6）。
- Risk to the idea: medium
- Needed differentiation: 把证伪条件改写为针对「判据」的可测量（conversion loss 与 ρ_n/T 的单调性、κ_n 大样本的欠校准率），而非「与某转换方法等价」。

**6**
- Closest work: TPP（含 SpikeConverter, AAAI 2022 的两阶段脉络）
- Venue/year: ICML 2025（SpikeConverter: AAAI 2022）
- Link/source: 同上
- What it already does: 两阶段转换框架。
- Overlap with user idea: 同上；rev2 已归功两阶段，TPP 列为第一批 must-rerun。
- Remaining novelty delta: 同上（范畴错位残留）。
- Risk to the idea: medium
- Needed differentiation: 在 matched-protocol 中直接对比 TPP，但把比较对象定位为「为 ρ=1 导出的校准律」而非「确定性第二相」。

**7**
- Closest work: One-Spike SNN
- Venue/year: IEEE TETC 2024/2025
- Link/source: 同上
- What it already does: 跨 CNN + GCN 的 ANN→SNN 转换。
- Overlap with user idea: 削弱「同一转换思路跨视觉与图骨干」的新颖性；rev2 已归功，只主张「同一固定线性 A + 统一协议 + 算子类成员的构造」。
- Remaining novelty delta: 仅剩「用 ρ_n≠1 判据贯穿两类骨干」这一诊断视角。
- Risk to the idea: medium
- Needed differentiation: 说明相对 One-Spike SNN，「何时失效判据」提供了其没有的、可先验计算的分析结论。

**8**
- Closest work: Parallel Conversion / DCGS / AdaFire（横评对手集合）
- Venue/year: ICML 2025 / ICML 2025 / AAAI 2025
- Link/source: 同上
- What it already does: 2025 年主流 ANN2SNN 转换方法，均有官方代码可重跑（用户提供）。
- Overlap with user idea: 构成 matched-protocol 必须对齐的基线集合，且代表子领域 2025 年饱和度；这些方法的校准律均为 ρ=1 假设，恰是 rev2 中心问题要检验的对象。
- Remaining novelty delta: 无（横评对象，不是被超越对象）；风险在于横评是否显示 κ_n 判据的诊断能力。
- Risk to the idea: medium
- Needed differentiation: 统一协议必须含同骨干、同 T、同 θ、同 calibration 数据，且须兑现 `matched-protocol.md` 工件（当前目录内不存在）。

**其他纳入但非最近邻的锚点（用户提供）**：CS-QCFS、ECL（无代码需自行复现）；CIFAR10-DVS、Planetoid 三图、Tiny-ImageNet 等数据集约束；G2 排除清单。均按用户提供事实记录，不扩展、不编造。

---

## Novelty delta:

**状态**：`searched`（组件层，依据用户提供的独立文献核验结论；边界见 Search basis；**推论层 `not searched`**）。**结论**：减去最近邻工作后，rev2 的 novelty 从 rev1 的「伪 delta / 组合 delta」升级为「**薄但真实、可证伪的分析增量**」，但**仍不构成「prior-art 无法得到的新数学结果」**。

| 声称的 delta | 复核结论 | 判定 |
| --- | --- | --- |
| T1 · ρ 加权系统性误差 | 由已知恒等式 `A(E₁W₂)` + 已知零期望偏置 `E[E₁]=β−1/(2T)`（QCFS/FTBC）+ 行和定义 `A·1=ρ_n·1` 直接展开得到；把 Deng&Gu 递归里的归一化矩阵换成一般 A 即可照搬。其「新」在于指出该后果对校准律的含义，而非数学本身。 | **假设放宽后的代数展开**（非纯重述，非新机制）；若 M0 推导不能证明非平凡性，则回落为「表述层推广」。 |
| T2 · 相对误差 ρ-不变 | margin Δ_n 由同一聚合 logits 算出，分子分母含同一聚合尺度 → 尺度抵消；属扰动分析中的标准观察，是**解释性结论**（解释「为何 ρ≈169 未灾难退化」），不是新误差界或新能力。诚实记录「原预测被实测推翻后给出正确解释」有 genuine 的分析价值。 | **真实但解释性增量**。 |
| κ_n = ρ_n/‖a_n‖₂ 判据 | 把「绝对按 ρ 加权（T1）」与「相对 ρ-不变（T2）」统一到一个先验可算、逐节点可检验的量，并给出可证伪的单调预测；在 ρ=1 文献框架里该量恒为常数、不会自然出现。这是 rev1 完全没有的分析层。 | **真实但薄的判据增量**；与 T2 存在未量化的内部张力（见下）。 |
| matched-protocol 统一横评 | 属评估 / benchmark 贡献，本身真实且可测；但 rev2 声称「成文 `matched-protocol.md`」在本 startup packet 工件目录中**并不存在**，且最决定性基线待自行复现。 | **真实、增量、工件未兑现**。 |
| 失效边界诊断（C5） | 真实、增量、可测；但依赖恒等式在固定线性 A 上成立这一前提。 | **真实但增量**。 |

### 特别回答：T1/T2 + κ_n 是否构成「prior-art 无法得到的新推论」，还是仍属已知结论的重述？

**这是决定 F2 的关键。本评审的明确结论：介于两者之间，但更靠近「已知结论的假设放宽推论」；它不再是 rev1 那种纯矩阵记号重述，但够不上「prior-art 无法得到的新推论 / 新数学结果」这一高标准。**

**为什么不是纯重述（相对 rev1 的实质进步，如实承认）**
1. ρ_n、κ_n 在 ρ=1 的 row-stochastic 推导里恒为常数、整项退化消失；把这些量显式引入并作为「何时失效」的自变量，是 prior-art 假设域内不会出现的分析维度。
2. κ_n 给出**先验可算、逐节点/逐样本可检验**的判据与可证伪的单调预测（conversion loss 差距随 ρ_n/T 增大），不是一句「换了个算子」；这比 rev1 的「层类型无关统一」具体得多。
3. T2 的 ρ-不变性是一个**反直觉、可证伪**的结论，且 rev2 诚实记录了「原预测 sum 聚合 ρ≈169 会灾难退化 → 实测推翻 → 给出 ρ-不变的正确解释」这一预测-证伪-修正过程，说明不是事后套公式。

**为什么够不上「prior-art 无法得到」（决定 F2 不能判「已解决」）**
1. **T1 的一行代数 objection 未被排除**：`A(E₁W₂)`（Dual-Phase/Deng&Gu）+ `E[E₁]=β−1/(2T)`（QCFS/FTBC）+ `A·1=ρ_n·1`（行和定义）三者放在一起即得 T1；把 Deng&Gu 递归中的归一化矩阵替换为一般非负 A 同样照搬。更准确地说，row-stochastic 文献「给不出」是因为**其 ρ=1 假设使该项退化为常数、不值得单列**，而非「理论上推不出」。
2. **T2 是尺度抵消的标准观察**，属解释性结论，不产生新误差界或新能力。
3. **κ_n 与 T2 存在未量化的内部张力**：若 `‖a_n‖₂` 随 ρ_n 增长（行和增大通常行范数也增大），κ_n 可能近似不变，则「conversion loss 差距随 ρ_n/T 单调增大」的预测可能不成立；这一张力**未列入 M0 待解项**。
4. **核心理论全部处于 M0 未证**：一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性证明、两解码兼容性命题、冗余消融均为「实验前必须完成、未过不得进 P4」。一个以理论判据为核心贡献的 idea，核心定理尚未证。
5. **推论层 novelty 未经针对检索**：第一次核验的是组件归属，不是「ρ_n 加权 margin 偏置 / 相对误差尺度不变 / 行和-行范数比判据」是否已被 2025–2026 工作给出。
6. **证伪条件范畴错位（W6）**：rev2 §1 第 4 条与 §4 F2 行仍以「与 PASCAL / TPP 等价 → 判据被推翻」作为裁决，但 rev2 已放弃「新方法」定位（贡献 = 判据 + 横评 + 边界）；一个**分析判据**不能与一个**转换方法**「等价」。这是从 rev1 继承时未更新的逻辑残留，说明 F2 的修复并未完全自洽。

**因此 F2 判「降级为可修复弱点」而非「已解决」/「仍未解 fatal」**：T1/T2/κ_n 提供了 rev1 完全没有的可证伪判据与反直觉结论，不再是「坍缩为纯重述/组合」；但 novelty 封顶 3、置信度 3，并设**反向条件**：若 M0 推导显示 T1 可一行照搬、或推论层检索命中近邻、或 κ_n 单调性被实测推翻、或 κ_n 与 T2 张力不可调和 → novelty 回落 2、F2 回潮为 fatal、整体分数回落约 2.6–2.7。

**明确不可声称的内容（用户硬要求，rev2 已遵守）**：不声称发明 `β* = θ/(2T)`、逐层误差递归、零期望误差偏置、膜电位累加解码、精确误差等式、确定性精确计数、两阶段框架、跨 CNN+GCN 转换。本评审在此之上追加：**不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」**，除非 M0 推导 + 推论层检索 + 单调性实测三者同时支持。

**最强 novelty delta 的诚实表述**：在显式写出「仅适用固定、非负、线性 ρ_n≠1 算子」的前提下，本 idea 剩下的可辩护贡献是「一个可先验计算、可证伪的『何时失效』判据（κ_n），配以 T2 的 ρ-不变性解释、统一协议横评与失效边界诊断」——这是一个**窄、增量、以诊断与协议为主**的贡献，按 Q1–Q2 期刊档可接收，但不是新理论组件。

---

## Serious blockers:

**Fatal risks（当前 formulation）：0 条结构性未解 fatal。** 依 `calibration.md` / `strict-idea-review.md`，第一次的三条 fatal 在 rev2 中：F1 已解决、F2 与 F3 降级为可修复弱点。下文给出逐条判定与依据，随后列出「准 fatal 级最重弱点」（尚未构成结构性 fatal，但任一恶化都会把推荐压回 1.0–2.9 段）。

### F1 / F2 / F3 逐条判定（用户硬要求 #2）

| Fatal | rev2 处理 | 判定（三选一） | 判定依据 | 残留 / 生效条件 |
| --- | --- | --- | --- | --- |
| **F1 主张—适用条件错位** | 中心问题改为「固定线性但 ρ_n≠1 时 ρ=1 校准律是否仍最优」；冻结 KNN / 线性化明写为「构造算子类成员」；原版动态/非线性 ViG 明写为失效边界（不进主结果、不得删）；禁用 "Operator-Agnostic" 命名；贡献类型改为理论判据 + 横评 + 边界。 | **已解决** | 第一次 F1 的结构性矛盾是「用限制假设规避所声称要解决的难点」（bait-and-switch）。rev2 把中心主张收窄到与适用条件 A1/A2 **完全一致**，并**不再声称覆盖**被削掉的数据依赖 / 动态 / 非线性算子，还把原版 ViG 正面定位为边界诊断而非隐藏。主张与适用条件不再错位，该特定 fatal 不成立。 | 残留「算子类在真实部署中的代表性」「冻结 KNN 相对原版 ViG 的性能代价（R4）」归 Problem importance 扣分，不属 F1。真正自洽须由 M0 推导 + C5 边界实验在执行层确认。 |
| **F2 novelty 重述 / 组合** | 引入 T1/T2 两条推论与 κ_n 可算判据；全文删除「发明数学组件」措辞；接受 Q1–Q2 期刊增量定位；诚实记录 ρ≈169 预测被推翻。 | **降级为可修复弱点**（最重、最偏 fatal 的一项） | 不判「仍未解 fatal」：T1/T2/κ_n 提供了 rev1 完全没有的、可先验计算且可证伪的判据与反直觉结论（ρ-不变性），delta 从「伪 / 组合」变为「薄但真实」，按 Q1–Q2 期刊档可接收增量诊断。不判「已解决」：见 Novelty delta 特别回答六条 —— 一行代数 objection 未排除、核心推导全在 M0 未证、推论层未检索、κ_n 与 T2 张力未解、证伪条件范畴错位。 | 生效条件：M0 推导兑现 T1/T2 非平凡性 + 推论层检索无近邻命中 + κ_n 单调性实测成立 → 可升为「已解决」并触发 novelty 分数上移；任一反向结果 → F2 回潮为 fatal。 |
| **F3 横评可比性两难** | 成文 matched-protocol（所有基线含自行复现的 PASCAL/TPP/CS-QCFS/ECL 在同一批固定骨干、同 T/θ/calibration/CL 定义重跑）；PASCAL 与 TPP 列第一批 must-rerun；贡献放弃「方法增益」定位。 | **降级为可修复弱点** | 第一次 F3 的两难是「基线原始骨干 / OAC 修改骨干 → 不可比；全移同骨干 → 增益来源不明」。rev2 在**设计层**给出正确消解：所有方法同骨干同协议，且**放弃方法增益定位**（贡献 = 判据 + 横评 + 边界），从而不再需要「不可比横评支撑方法主张」，两难的逻辑前提消失。evidence plan（C1–C5、基线矩阵、消融、5 seeds、bootstrap/BH、S1–S7、全部 TBD）完备可信。 | 残留四项执行/工件层可修复：(i) 声称「成文 `matched-protocol.md`」但工件目录内**无此文件**；(ii) PASCAL/TPP/CS-QCFS/ECL 仍为「待自行复现」计划；(iii) 零正式实验（按用户硬要求不判 fatal）；(iv) 证伪条件范畴错位。 |

### 准 fatal 级最重弱点（未构成结构性 fatal，但压住升档）

- **Q1 · 核心理论判据全部处于 M0 未证**：一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性证明、两解码兼容性命题、冗余消融均为「实验前必须完成、未过不得进 P4」。**这是「理论判据型贡献 + 定理未证」的根本未就绪**，是 Method soundness / Novelty / Acceptance 不得高于 3 的主因。
- **Q2 · 推论层 novelty 未检索 + 「一行代数」objection 未排除**：见 Novelty delta 特别回答。
- **Q3 · κ_n 与 T2 的内部张力未量化、未列入 M0**：若 `‖a_n‖₂` 随 ρ_n 增长，κ_n 近似不变，「随 ρ_n/T 单调增大」可能不成立。
- **Q4 · 可证伪条件范畴错位（W6）**：「与 PASCAL/TPP 等价 → 判据被推翻」是 rev1 新方法定位的残留，与 rev2 贡献类型不自洽。

**Fixable weaknesses（可修复，不改变中心主张）**

- W1 视觉侧零正式实验（用户明述；按硬要求不判 fatal，记为证据缺口）→ 补统一协议下完整视觉侧实验。
- W2 「成文 `matched-protocol.md`」未兑现 → 补写该工件（明确同骨干 / 同 T / 同 θ / 同 calibration / 同 CL 定义 / 全部基线清单）。
- W3 PASCAL / TPP / CS-QCFS / ECL 无官方代码 → 自行复现并纳入第一批 must-rerun。
- W4 M0 四项未闭合（β* 一般 A 推导、`‖A‖` 误差上界、两解码兼容性、冗余消融）→ 纸面推导 + 数值验证，未过不进 P4。
- W5 κ_n 单调性未证 + κ_n 与 T2 张力未解 → 补证明 / 反例条件，并显式列入 M0。
- W6 第 4 条证伪条件范畴错位 → 改写为针对判据的可测量。
- W7 冻结 KNN 相对原版 ViG 的性能代价未量化（R4）→ 定量报告，不得隐瞒。
- W8 组件冗余（膜电位累加解码 vs 确定性计数 s[t]）未消融（A5）→ 消融后删冗余。
- W9 推论层 novelty 未检索 → 针对推论做一次公开检索（不粘贴私有措辞）。
- W10 官方当年 venue policy / review form 未核验 → 成文前核验。
- W11 rev2 卡「成稿实测」数值 / 「成稿 §3.2、§5.1」引用与 packet 内「全部 `<TBD>`、零实验数值」纪律冲突、且无对应成稿工件 → 成文时澄清来源或删除，不得写入公开证据 / 结果栏。

**隔离项**：图节点分类 T≤8 ANN−1.5pp 带内、以及 rev2 「成稿实测」数值，均为「用户提供的未公开先验（未发表、不充当公开证据）」，既非 fatal 也非 weakness 证据，不参与判定。

---

## Per-expert reviewer notes:

> 以下五个角色**独立**给出判断，先各自发言、后综合（依 `expert-panel.md` 与 `review-output-standards.md` 的 panel 纪律）。每个角色的 **Score tendency（分数倾向）与 Confidence（置信度）分开报**，不强行制造一致、赞扬或拒稿。全部内容为本红队 panel 的独立判断，非真实审稿记录。

**Field Expert**
- Role: 领域专家（类脑计算 × ANN2SNN 转换）
- Score tendency: 3 / 5
- Best possible argument for the idea: 把中心问题从「统一数据依赖邻域聚合」收窄到「ρ_n≠1 时 ρ=1 校准律是否仍最优」，是一个真实、具体、可测且与方法能力对齐的问题；「何时失效」框架对把 GNN / ViG 用于 SNN 的社区有实用价值，比 rev1 的空泛「算子无关」诚实得多。
- Strict rejection-grade concern: **算子类代表性**。冻结 KNN 的 ViG 已不是 ViG 的数据依赖表征（R4 自认削弱），sum 聚合 ρ≈169 是人为构造的极端设置；审稿人会问「这个固定线性 ρ_n≠1 算子类在真实部署里占多大比重」。若答案只是「为套恒等式而构造的一类骨干」，问题会被读成 self-imposed 而非社区瓶颈。
- Anchor: rev2 §1 Bottleneck、A1/A2、R4；第一次 Field 专家「gap 是理论瓶颈还是工程缺口」之问。
- Why this matters: 决定 Problem importance 能否从 3 升 4；写完 related work 后 gap 是否还站得住。
- Fatal risk if any: 无独立 fatal（F1 已消解）。
- Most valuable repair or pivot: 给出「非行随机算子在主流 GNN / ViG 中普遍存在」的公开证据 + 冻结 KNN 代价量化（R4），把问题从「人为构造类」锚到「真实部署类」。
- Development-potential note: 中；问题代表性可提升主轴，不消除 F2。
- Confidence: 4 / 5（问题文本与适用条件由 rev2 明确给出）

**Method Expert**
- Role: 方法专家（误差分析 / 机制正确性）
- Score tendency: 2 / 5
- Best possible argument for the idea: 假设 A1–A5 逐条列明且可被检验；恒等式 `A(E₁W₂)` 在固定线性 A 下代数自洽；M0「未过不得进 P4」是诚实的自我约束；T1/T2 把误差分析推向 ρ_n≠1 方向是对的。
- Strict rejection-grade concern: 核心贡献（理论判据）的定理**全部未证**：一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性证明、两解码兼容性、冗余消融全是 M0 待办。三点更尖锐：(a) T1 可能只是 `A·1=ρ_n·1` 的行和定义 + QCFS 零期望偏置，即「一行代数」；(b) T2 的 ρ-不变性可能只是分子分母共同聚合尺度的抵消；(c) **κ_n 与 T2 的内部张力** —— 若 `‖a_n‖₂` 随 ρ_n 增长则 κ_n 近似不变，「随 ρ_n/T 单调增大」可能不成立，而这一张力**未列入 M0 待解项**。
- Anchor: rev2 §1 R1/R2/R3、M0、A3、κ_n 定义与 T2；`calibration.md` fatal gate「Method soundness <= 2」的边界。
- Why this matters: 一个以理论判据为核心贡献的 idea，核心定理处于「待推导」状态，method soundness 不能高。
- Fatal risk if any: 若 M0 推导显示 T1 可由 Deng&Gu 递归一行照搬，则 F2 回潮为 fatal。
- Most valuable repair or pivot: 先做 M0 纸面推导（β* 一般 A、`‖A‖` 界、T1/T2 严格证明、κ_n 单调性条件与成立区间），并把「κ_n 与 T2 张力」列为显式待解项 + 数值验证。
- Development-potential note: 中—高；最可修复的一条（纸面为主，无算力成本）。
- Confidence: 3 / 5（部分判断基于对未给出推导的推断，可检验证据不足）

**Experiment Expert**
- Role: 实验专家（证据设计 / 基线 / 可行性）
- Score tendency: 3 / 5
- Best possible argument for the idea: evidence plan 相当完备（C1–C5 可证伪主张、基线矩阵、匹配内部对照、5 seeds、配对 bootstrap `R=5000` + sign-flip + BH、S1–S7 stop-and-return、全部 `<TBD>` 不编造、matched-protocol 设计）；按 guidance 阶段「只需 evidence plan 可行」的标准，plan 可行且可信；用户硬要求「零实验不自动判 fatal」，本角色遵守。
- Strict rejection-grade concern: 四处具体缺口：(a) 「成文 `matched-protocol.md`」在工件目录中**不存在**，F3「设计层已解决」缺一个兑现的工件；(b) 最决定性基线 PASCAL / TPP / CS-QCFS / ECL 全部「待自行复现」、无官方代码；(c) **可证伪条件范畴错位** —— §1 第 4 条「与 PASCAL/TPP 等价 → 判据被推翻」是 rev1「新方法」定位的残留，但 rev2 已放弃新方法定位，一个分析判据不能与一个转换方法「等价」，正确证伪应是「conversion loss 与 ρ_n/T 无单调关系」或「κ_n 大样本未显示欠校准」；(d) κ_n 单调性、冻结 KNN 代价（R4）、原版 ViG 边界（C5）均待实测。
- Anchor: 工件目录文件清单（无 `matched-protocol.md`）；rev2 §1 Falsification 第 4 条与 §4 F2 行；`claim-evidence-matrix.md` / `strong-result-feasibility-contract.md`。
- Why this matters: plan 可信但含一处未兑现工件与一处逻辑残留；阴性结果（单调性不成立）会直接推翻核心判据。
- Fatal risk if any: 无独立 fatal（按用户硬要求，不把零实验判 fatal）。
- Most valuable repair or pivot: 补写 `matched-protocol.md`（所有基线在同一批固定骨干、同 T/θ/calibration/CL 定义），把第 4 条证伪条件改写为针对判据的可测量，优先复现 PASCAL / TPP，报告 conversion loss–ρ_n/T 曲线与 κ_n 逐节点欠校准率。
- Development-potential note: 高；最明确、最可执行的补齐路径。
- Confidence: 4 / 5（工件清单与基线代码状态由用户提供，plan 文本可直接核查）

**AC / Venue Expert**
- Role: AC / venue 专家（贡献品味 / 匹配 / 讨论后存活）
- Score tendency: 4 / 5
- Best possible argument for the idea: 主动降到 IEEE TNNLS / Q1–Q2 档、ImageNet-1K 不再是硬要求、贡献收敛为「何时失效判据 + 统一横评 + 失效边界」单一主轴 —— 这正是第一次 AC 专家指出的自洽落点，venue-switch 完成得干净；TNNLS 档（类脑 + 理论 + 容较小数据集 + 篇幅容纳横评）接受增量诊断型贡献。
- Strict rejection-grade concern: (a) 贡献仍是三块并列（判据 / 横评 / 边界），「主轴收敛」更多在措辞而非结构；(b) 统一协议横评带 benchmark 味，混合评审中可能被读成 benchmark / 诊断短文而非理论主贡献；(c) 核心理论 M0 未过 + 零实验，能否 survive discussion 存疑；(d) 未核验 TNNLS 当年官方 policy / review form，按通用 contribution taste 推理。
- Anchor: rev2 §0、§1 Contribution type；prior-art venue 分布（TNNLS/TMLR/ICML/AAAI/TETC）；未核验当年官方政策。
- Why this matters: venue 对齐消除了第一次的 mismatch，但 readiness 仍低，二者不可混为一谈。
- Fatal risk if any: 无独立 fatal。
- Most valuable repair or pivot: 结构上把三块贡献绑定为「一个 κ_n 判据贯穿横评与边界」的单一叙事，而非三章并列；成文前核验当年官方政策。
- Development-potential note: 中。
- Confidence: 3 / 5（官方当年政策未核验，依据贡献品味推理）

**Skeptical Prior-Art Expert**
- Role: 怀疑型 prior-art 专家（novelty 坍塌 / 命名掩盖 / 是否已属已知）
- Score tendency: 2 / 5
- Best possible argument for the idea: rev2 禁用 "Operator-Agnostic" 掩盖性命名、全文不声称发明任何已占组件、诚实记录「原预测 ρ≈169 会灾难退化、被实测推翻后给出 ρ-不变解释」——这种自我约束降低了被当场 scoop 的风险；T1/T2 确实是 rev1 主卡里没有的分析层，不能简单说「仍属重述」。
- Strict rejection-grade concern: **最强「this is already known」objection**：把 Deng&Gu 逐层误差递归里的（行随机）归一化矩阵换成一般非负矩阵 A，`A·1 = ρ_n·1` 立刻给出 T1 的 ρ_n 加权项，配合 QCFS 零期望偏置 `E[E₁]=β−1/(2T)` 就是 T1 的全部；T2 是分子分母含同一聚合尺度的归一化抵消；κ_n 是两个已知统计量的比值。三者都是「放宽 ρ=1 假设 + 对已知恒等式做代数展开」的产物，而非新数学机制 —— prior-art「给不出」更准确是「其假设使该项退化、不值得写」。追加两点：(a) **推论层 novelty 未经针对检索**（第一次核验的是组件归属）；(b) 若 M0 推导兑现不了（一行代数照搬成立），F2 回潮为 fatal。
- Anchor: 用户核验 prior-art 表（Deng&Gu / QCFS / Dual-Phase / PASCAL / TPP）；rev2 T1/T2/κ_n、M0；Search basis 的推论层边界。
- Why this matters: 决定 novelty 是否 <= 2 与是否「beyond applying known modules」。
- Fatal risk if any: F2 仍是最重的一项；但本角色认同「已降级为可修复弱点」而非 fatal，因 T1/T2 提供了 rev1 没有的可证伪判据。
- Most valuable repair or pivot: 针对推论本身做一次公开检索（row-sum weighted conversion bias / non-row-stochastic ANN-SNN / scale-invariance of relative conversion error），并在 M0 里给出 T1 相对 Deng&Gu 递归的**非平凡性证明**（不是换记号）。
- Development-potential note: 低—中。
- Confidence: 4 / 5（组件层重叠明确；推论层未检索，故不给 5）

**Panel Synthesis**（依 `expert-panel.md` 与 `review-output-standards.md`，不平均掉致命弱点）

```text
Agreement: 五位专家一致认为 F1 已在主张层消解、venue 主动对齐是真实进步、evidence plan 完备可信、核心理论 M0 未证 + 零实证使 readiness 仍为 low；一致认为不应 abandon（中心判据可测、M0 路线可命名、stage-aware 规则不满足）。
Disagreement: AC 给 4（评 venue 对齐后的 fit），Field 与 Experiment 给 3（评问题代表性 / plan 兑现度），Method 与 Skeptical 给 2（评理论未闭合 / novelty 坍塌风险）。分歧来自「评哪个轴」，不是对事实的分歧；未强行制造一致或赞扬。
Strongest accept axis / Decisive accept axis: T2 的 ρ-不变性 + κ_n 判据给出一个在 ρ=1 假设域内不会出现、先验可算、可证伪的「何时失效」量；配统一协议横评与失效边界，对 Q1–Q2 期刊档是够得着的增量诊断贡献。
Strongest reject axis / Decisive reject axis: T1/T2 可能只是「放宽 ρ=1 假设 + 已知恒等式代数展开」的产物，推论层未检索、核心定理全在 M0 未证、κ_n 与 T2 张力未解、证伪条件范畴错位；若 M0 推导不利，novelty 回 2、整体回 2.6–2.7、F2 回潮为 fatal。
Score-relevant uncertainty / Unresolved evidence: M0 推导结果；推论层检索；κ_n 单调性与 κ_n–T2 张力；matched-protocol.md 兑现；PASCAL/TPP 复现；冻结 KNN 代价；官方当年 venue policy。
Most valuable next evidence: 先做 M0 纸面推导（尤其 T1 非平凡性 + κ_n 单调性），再做推论层针对检索，再按 matched-protocol 复现 PASCAL/TPP 并测 conversion loss–ρ_n/T 曲线。
Final calibrated stance / Panel-calibrated recommendation: pivot-with-rescue-route（与加权 3.2 落在 calibration 3.0–3.6 段一致，且与各专家独立分数不矛盾）。
```

---

## Rubric scores:

权重取 `rubric.md` 默认表（合计 100），未作调整（无官方 venue review form 要求调整）。**标尺按 rev2 的 Q1–Q2 期刊档**。

| Dimension | Weight | Score (1-5) | Confidence (1-5) | Deduction / evidence basis | Repair condition |
| --- | ---: | ---: | ---: | --- | --- |
| Problem importance | 12 | 3 | 4 | 问题已与方法能力对齐，但算子类代表性存疑（冻结 KNN 的 ViG、ρ≈169 的 sum 聚合偏人为构造）；R4 代价未量化 | 给出「非行随机算子在主流 GNN/ViG 中普遍存在」的公开证据 + R4 量化 |
| Novelty against likely prior work | 14 | 3 | 3 | T1/T2/κ_n 是薄但真实的可证伪判据，非纯重述；但一行代数 objection 未排除、推论层未检索、核心推导在 M0 未证 | M0 证明 T1 非平凡性 + 推论层检索无近邻 + κ_n 单调性实测成立 |
| Conceptual innovation | 12 | 3 | 3 | κ_n 判据与 ρ-不变性解释是 rev1 没有的概念层增量；但 κ_n 仅为两个已知量之比、与 T2 有未解张力 | 证 κ_n 带来 prior-art 无法给出的解释或预测，并解决 κ_n–T2 张力 |
| Method soundness | 14 | 3 | 3 | 假设 A1–A5 清楚、矛盾被显式管理（R4/C5）、M0 设门；但核心定理（β* 一般 A、‖A‖ 界、T1/T2 证明、κ_n 单调性、两解码兼容性）全未证 | 完成 M0 全部纸面推导 + 数值验证，并把 κ_n–T2 张力列入待解项 |
| Elegance and simplicity | 8 | 3 | 4 | 收敛到单一 κ_n 判据比 rev1 四组件拼盘更简洁；但组件冗余（解码 vs 确定性计数）未消融，三块贡献未结构化绑定 | 消融 A5 删冗余，并把判据/横评/边界绑定为单一叙事 |
| Feasibility under resources | 8 | 4 | 4 | 数据/算力/多数基线代码齐备，evidence plan 与里程碑 M0–M4 齐备；ImageNet 不可得已由降档消解；GCN 来源 TBD、torchvision 待补装、3 个基线待复现 | 确认 ViG-SNN 与全套基线在 3060/4090 可跑通，补齐 GCN 实现来源 |
| Experimental convincibility | 10 | 3 | 4 | plan 完备可信、可比性设计层已定义、零实验按硬要求不判 fatal；但无实证、决定性基线待复现、matched-protocol.md 未成文、证伪条件范畴错位、单调性未证 | 兑现 matched-protocol 工件 + 复现 PASCAL/TPP + 改写第 4 条证伪条件 + 报告单调性曲线 |
| Venue and audience fit | 8 | 4 | 3 | 主动对齐 TNNLS/Q1–Q2 档、主轴收敛、ImageNet 消解，正是第一次 AC 指出的自洽落点；但三块贡献仍并列、横评带 benchmark 味、当年官方政策未核验 | 结构化绑定单一叙事 + 核验当年官方 policy / review form |
| Timeliness and topic heat | 6 | 3 | 4 | 方向热但 2024/2025 prior-art 密集；「何时失效」诊断角度相对不那么饱和，但子领域整体仍拥挤 | 把「为什么是现在」绑定到 ρ_n≠1 算子在视觉图网络中的真实普遍性 |
| Risk-adjusted acceptance potential | 8 | 3 | 4 | fatal 从 3 条降为 0 条（F1 已解、F2/F3 降级）、venue 降档；但核心理论未证 + 零实证 + novelty 薄 + 范畴错位仍在 | M0 过门 + 推论层检索无命中 + 横评显示判据诊断能力，三者齐备方可升档 |

### 每个 ≤3 分项的扣分明细（依 `rubric.md` Deduction Format 与 `review-output-standards.md` 定量反馈；用户硬要求四项齐全）

本表共 8 个 ≤3 分项（Problem / Novelty / Conceptual / Method / Elegance / Experimental / Timeliness / Acceptance），每项含**扣分理由 / 证据基础 / 修复条件 / 预期分数变化**四项，另附 Why it matters 与 Development-potential effect。全部预期变化为**条件性、非承诺**（依 `privacy-and-evidence.md`）。

**Problem importance（Score 3 / Confidence 4）**
- 扣分理由：rev2 把主张与适用条件对齐了（F1 已解），但**并未提升问题的绝对重要性** —— 它把一个大而难的问题换成一个小而具体的问题。算子类「固定、非负、线性、ρ_n≠1」的真实代表性存疑：冻结 KNN 的 ViG 已失去数据依赖表征（R4 自认削弱），sum 聚合 ρ≈169 偏人为构造的极端设置。若该类只是「为套恒等式而构造」，问题读成 self-imposed 而非社区瓶颈。
- 证据基础 / Anchor：rev2 §1 Bottleneck、A1/A2、R4；第一次 Field 专家「gap 是理论瓶颈还是工程缺口」之问。
- 为什么重要：Q1–Q2 期刊同样要求瓶颈「真实且被本文真正检验」；写完 related work 后若 gap 只剩「没人系统测过 ρ_n≠1」，会被判为窄诊断而非重要性贡献。
- 修复条件：给出「非行随机算子在主流 GNN / ViG 部署中普遍存在」的公开证据，并量化冻结 KNN 相对原版 ViG 的性能代价（R4）。
- 预期分数变化：条件性 3→4，Overall 约 +0.12；**不承诺**。
- Development-potential effect：中；提升主轴清晰度，不消除 F2。

**Novelty against likely prior work（Score 3 / Confidence 3）**
- 扣分理由：T1/T2/κ_n 把 rev1 的「伪 / 组合 delta」推进为薄但真实、可证伪的分析判据（这是相对第一次 2→3 的实质依据），但够不上「prior-art 无法得到的新推论」：T1 可由 `A(E₁W₂)` + QCFS 零期望偏置 + 行和定义一行代数照搬 Deng&Gu 递归；T2 是尺度抵消的标准观察；κ_n 是两个已知量之比。**推论层 novelty 未经针对检索**，依 `strict-idea-review.md` 封顶 3；核心推导全在 M0 未证，故置信度 3 而非 5。
- 证据基础 / Anchor：Closest prior art table 8 条（组件层高重叠）；Novelty delta 特别回答六条；`rubric.md`「do not score above 3 when closest work was not checked and novelty is central」；Search basis 推论层边界。
- 为什么重要：这是决定 F2 的关键维度；`calibration.md` fatal gate「Novelty <= 2 with high confidence」当前不触发，但反向条件会把它拉回。
- 修复条件：M0 给出 T1 相对 Deng&Gu 递归的非平凡性证明 + 推论层针对检索无近邻命中 + κ_n 单调性实测成立。三者缺一，维持 3；任一反向结果回落 2。
- 预期分数变化：条件性 3→4（三条件齐备），Overall 约 +0.14；反向条件 3→2，Overall 约 −0.14；**不承诺**。
- Development-potential effect：低—中；fatal gate 的临界项。

**Conceptual innovation（Score 3 / Confidence 3）**
- 扣分理由：κ_n 判据与 T2 的 ρ-不变性解释是 rev1 没有的概念层增量（相对第一次 2→3），且禁用了掩盖性命名；但 κ_n = ρ_n/‖a_n‖₂ 只是两个已知统计量的比值，ρ-不变性是标准归一化观察，且 **κ_n 与 T2 存在未量化的内部张力**（‖a_n‖₂ 随 ρ_n 增长时 κ_n 近似不变，单调预测可能不成立），该张力未列入 M0。
- 证据基础 / Anchor：rev2 §1 T1/T2/κ_n、M0 待办清单；`rubric.md`「penalize pure module recombination unless the combination creates a new capability or explanation」。
- 为什么重要：若判据不能带来 prior-art 无法给出的解释或预测，概念创新读成「把两个量相除」。
- 修复条件：证明 κ_n 带来 prior-art 无法给出的可证伪预测（如逐节点欠校准率），并显式解决 κ_n–T2 张力（给出单调性成立的 ‖a_n‖₂ / ρ_n 条件区间）。
- 预期分数变化：条件性 3→4，Overall 约 +0.12；**不承诺**。
- Development-potential effect：中。

**Method soundness（Score 3 / Confidence 3）**
- 扣分理由：假设 A1–A5 逐条可检验、恒等式代数自洽、组件目标冲突被显式管理（R4 代价量化 + C5 边界）、M0「未过不得进 P4」是诚实的自我约束（这些是相对第一次 2→3 的依据）；但**核心贡献的定理全部未证**：一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性证明、两解码兼容性命题、冗余消融均为 M0 待办。一个以理论判据为核心贡献的 idea，核心定理处于「待推导」，method soundness 不能高。
- 证据基础 / Anchor：rev2 §1 R1/R2/R3、M0、A3；κ_n 与 T2 张力；`calibration.md` fatal gate「Method soundness <= 2」当前不触发但临界。
- 为什么重要：M0 是作者自己设的硬门；门未过，任何「理论判据」主张都未成立。
- 修复条件：完成 M0 全部纸面推导 + 数值验证，并把「κ_n 与 T2 张力 / 单调性成立区间」列为显式待解项。
- 预期分数变化：条件性 3→4（M0 全过），Overall 约 +0.14；若 β* 对一般 A 不成立且无替代闭式、或 T1 坍缩为一行代数 → 3→2 并触发 fatal gate，Overall 约 −0.14；**不承诺**。
- Development-potential effect：中—高；最可修复的一条（纸面为主）。

**Elegance and simplicity（Score 3 / Confidence 4）**
- 扣分理由：收敛到单一 κ_n 判据、全文不再声称发明任何组件，比 rev1 的「恒等式 + 偏置 + 解码 + 确定性 s[t]」四组件拼盘更简洁、更有解释力；但组件冗余（膜电位累加解码 vs 确定性计数 s[t]）未消融（A5 待办），且「判据 / 横评 / 边界」三块贡献仍并列、未结构化绑定为单一叙事。
- 证据基础 / Anchor：rev2 §1 Contribution type、R3/A5；用户核验的 Dual-Phase（膜电位读出）与 PASCAL（确定性计数）。
- 为什么重要：`rubric.md` elegance 要求 necessary parts and coherent insight；冗余组件会被核减为实现细节。
- 修复条件：消融 A5 删除被证明冗余的组件；把三块贡献绑定为「一个 κ_n 判据贯穿横评与边界」的单一叙事。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；**不承诺**。
- Development-potential effect：低—中。

**Experimental convincibility（Score 3 / Confidence 4）**
- 扣分理由：evidence plan 完备可信（C1–C5、基线矩阵、匹配内部对照、5 seeds、bootstrap/BH、S1–S7、全部 `<TBD>` 不编造），可比性在**设计层**已定义，且按用户硬要求「视觉侧零实验不自动判 fatal」（这些是相对第一次 2→3 的依据，且遵守硬要求）；但仍**无任何实证**，最决定性基线 PASCAL/TPP/CS-QCFS/ECL 待自行复现，声称「成文 `matched-protocol.md`」在工件目录中并不存在，第 4 条证伪条件范畴错位，κ_n 单调性 / R4 代价 / C5 边界均待实测。
- 证据基础 / Anchor：工件目录文件清单（无 `matched-protocol.md`）；rev2 §1 Falsification 第 4 条与 §4 F3 行；`claim-evidence-matrix.md` / `strong-result-feasibility-contract.md`；用户硬要求（guidance 阶段只评 plan 可行性）。
- 为什么重要：plan 可信但含一处未兑现工件与一处逻辑残留；阴性结果（conversion loss 与 ρ_n/T 无单调关系）会直接推翻核心判据。
- 修复条件：补写 `matched-protocol.md`（所有基线同骨干、同 T/θ/calibration/CL 定义），把第 4 条证伪条件改写为针对判据的可测量，优先复现 PASCAL/TPP，报告 conversion loss–ρ_n/T 曲线、恒等式残差、κ_n 逐节点欠校准率、C5 边界与 R4 代价。
- 预期分数变化：条件性 3→4（横评支持判据诊断能力），Overall 约 +0.10；若单调性被推翻 → 3→2 并坐实 F2，Overall 约 −0.10；**不承诺**。
- Development-potential effect：高；最明确、最可执行的补齐路径。

**Timeliness and topic heat（Score 3 / Confidence 4）**
- 扣分理由：方向热但饱和风险高；用户列出的强相关 prior-art 中 2024/2025 年密集（FTBC ECCV'24、Dual-Phase TNNLS'24、PASCAL TMLR'25、TPP ICML'25、Parallel Conversion ICML'25、DCGS ICML'25、AdaFire AAAI'25、One-Spike SNN TETC'24/25）。「何时失效」诊断角度相对不那么饱和，但子领域整体仍拥挤，scoop 风险未消。
- 证据基础 / Anchor：用户提供的 prior-art 年份与 venue 列表；`rubric.md` timeliness 的「risk of saturation」。
- 为什么重要：密集 prior art 提高 novelty 坍塌与 scoop 风险，尤其对推论层未检索的 T1/T2。
- 修复条件：把「为什么是现在」绑定到 ρ_n≠1 算子在视觉图网络 / GNN 中的真实普遍性证据，并做推论层针对检索。
- 预期分数变化：条件性 3→4，Overall 约 +0.06；**不承诺**。
- Development-potential effect：低。

**Risk-adjusted acceptance potential（Score 3 / Confidence 4）**
- 扣分理由：fatal 从 3 条降为 0 条（F1 已解、F2/F3 降级为可修复弱点）、venue 主动对齐 Q1–Q2 档、M0 门显式（这些是相对第一次 2→3 的依据）；但核心理论判据全部 M0 未证、零实证、novelty 薄且推论层未检索、κ_n–T2 张力未解、证伪条件范畴错位、matched-protocol 工件未兑现仍叠加。`calibration.md` 五条 fatal gate 当前**均不硬触发**（novelty 3、method 3、experimental 3、fit 4、feasibility 4），但「No identifiable insight beyond known modules」与「Internal mechanism conflict」两条处于临界。
- 证据基础 / Anchor：本报告 Serious blockers（F1/F2/F3 判定 + Q1–Q4）、fatal gates 清单、Panel Synthesis。
- 为什么重要：该维度反映「考虑致命弱点与评审分歧后的分数」，是叠加效应而非重复计罚。
- 修复条件：M0 过门 + 推论层检索无命中 + matched-protocol 兑现 + 横评显示判据诊断能力，四者齐备方可升档；任一反向结果回落。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；若 F2 回潮为 fatal → 3→2，Overall 约 −0.08；**不承诺**。
- Development-potential effect：中（依赖 M0 与横评结果）。

> Feasibility under resources（4）与 Venue and audience fit（4）为 >3 项，不触发明细块要求；其扣分 / 修复条件已在上方表格给出。

---

## Weighted final score:

依 `rubric.md` / `calibration.md`：`weighted_score = sum(score_i × weight_i) / 100`

```text
12×3 = 36   (Problem importance)
14×3 = 42   (Novelty against likely prior work)
12×3 = 36   (Conceptual innovation)
14×3 = 42   (Method soundness)
 8×3 = 24   (Elegance and simplicity)
 8×4 = 32   (Feasibility under resources)
10×3 = 30   (Experimental convincibility)
 8×4 = 32   (Venue and audience fit)
 6×3 = 18   (Timeliness and topic heat)
 8×3 = 24   (Risk-adjusted acceptance potential)
合计 = 316 → 316 / 100 = 3.16 → 3.2（保留一位小数）
```

**Overall:** 3.2（1–5 加权尺度；可选 1–10 尺度 ≈ 6.3）

```text
Current conference readiness: low
Development potential: medium
```

**分数与推荐的一致性说明**：3.16 → 3.2 落在 `calibration.md` 的 **3.0–3.6 段 → `pivot-with-rescue-route`**。本推荐**由分数段直接得出，不依赖任何 fatal gate 压顶**（五条 gate 当前均不硬触发，见下）。不取 `revise`（需 3.7+，即核心理论兑现 + 实证 + novelty 站稳，未达）；不取 `accept-to-develop`；不取 `needs-literature-search`（novelty 按用户指令标 `searched` 且结论为「组件层高重叠 / 推论层薄增量」而非「未知」，推论层未检索作为边界与置信度处理，不升级为推荐值）；不取 `abandon`（判据可测、M0 路线可命名，依 `strict-idea-review.md` Stage-Aware Verdict Rule 不满足「无可测主张且无重构」）。

**相对第一次 `**Overall:** 2.5` 的 +0.7 逐维分解（证明非「修订版默认更高」）**：

| 维度 | rev1 → rev2 | 加权贡献 | 强制该变化的文本事实 |
| --- | --- | --- | --- |
| Novelty | 2 → 3 | +0.14 | rev1 为「矩阵记号重述 + PASCAL/TPP 组合」；rev2 新增 T1/T2/κ_n 可证伪判据 + ρ-不变性反直觉结论 + 全文归功已占组件。 |
| Conceptual | 2 → 3 | +0.12 | 禁用 "Operator-Agnostic" 掩盖命名 + 提出 κ_n 单一判据。 |
| Method | 2 → 3 | +0.14 | 假设 A1–A5 逐条列明、组件冲突显式管理（R4/C5）、M0「未过不得进 P4」设门。 |
| Experimental | 2 → 3 | +0.10 | 可比性设计层定义 + evidence plan 完备可信 + 用户硬要求「零实验不自动判 fatal」。 |
| Venue fit | 3 → 4 | +0.08 | 主动降 TNNLS/Q1–Q2 档 + 主轴收敛 + ImageNet 硬要求消解。 |
| Acceptance | 2 → 3 | +0.08 | fatal 由 3 条降为 0 条（F1 已解、F2/F3 降级）+ venue 降档。 |
| Problem / Elegance / Feasibility / Timeliness | 3/3/4/3 保持不变 | +0.00 | 问题绝对重要性未提升；冗余未消融；资源未变；子领域仍拥挤。 |

合计 +0.66 → 2.5 + 0.66 = 3.16 ≈ 3.2。**六个 +1 全部由可核查的文本事实或用户硬要求强制，四个维度保持不变，无任何 +2 跳升，且推荐未升出 `pivot-with-rescue-route` 段**。这是「如实承认有限进步 + 不迎合抬分」的取值，而非「因是修订版默认更高」。

**Fatal gates 生效清单（`calibration.md`，逐条核对）**：
- Novelty <= 2 with high confidence → **不触发**（3 / conf 3）。
- Method soundness <= 2 → **不触发**（3），临界。
- Experimental convincibility <= 2 且无替代证据 → **不触发**（3，且 evidence plan 完备）。
- Venue fit <= 2 → **不触发**（4）。
- Feasibility <= 2 → **不触发**（4）。
- No identifiable insight beyond applying known modules → **不硬触发但临界**（T1/T2/κ_n 提供了薄但可辨识的判据；若 M0 推导显示 T1 一行照搬，则触发）。
- Internal mechanism conflict → **不硬触发但临界**（κ_n–T2 张力、冻结 KNN vs 表征力已被 R4/C5 显式管理，但张力未量化）。
- Novelty unknown 且无 closest-work search → **不适用**（组件层 `searched`；推论层未检索已降置信度并封顶 novelty 3，依 `strict-idea-review.md` 处理，不升级为 `needs-literature-search` 推荐）。

---

## Score-change conditions:

全部为**条件性、非承诺**（依 `privacy-and-evidence.md`，不保证分数变化 / 录用概率 / 审稿人行为）。按影响排序：

| 条件（可测） | 影响维度 | 预期分数变化（条件性区间） |
| --- | --- | --- |
| C1 完成 M0 全部纸面推导：一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性成立区间、两解码兼容性、冗余消融；并数值验证 | Method / Novelty / Conceptual | Method 3→4、Novelty 3→4（若同时 C2 成立）、Conceptual 3→4；Overall 约 +0.3~+0.4 |
| C2 证明 T1 相对 Deng&Gu 递归的**非平凡性**（非仅把归一化 A 换成一般 A），且推论层针对检索无近邻命中 | Novelty / Conceptual | Novelty 3→4；Overall 约 +0.14；反向则 3→2 |
| C3 兑现 `matched-protocol.md` 工件，优先复现 PASCAL / TPP / CS-QCFS / ECL，报告 conversion loss–ρ_n/T 单调曲线、恒等式残差、κ_n 逐节点欠校准率、C5 边界、R4 代价 | Experimental / Acceptance | Experimental 3→4（若曲线支持判据）；Overall 约 +0.10~+0.18 |
| C4 把第 4 条证伪条件从「与 PASCAL/TPP 等价」改写为针对判据的可测量，并显式解决 κ_n–T2 张力 | Experimental / Method / Elegance | Experimental 3→4、Method 3→4 的辅助条件；Overall 约 +0.05~+0.10 |
| C5 给出「非行随机算子在主流 GNN / ViG 中普遍存在」的公开证据 + 冻结 KNN 代价量化 | Problem / Timeliness | Problem 3→4、Timeliness 3→4；Overall 约 +0.18 |
| C6 结构上把「判据 / 横评 / 边界」绑定为单一叙事并核验当年官方 policy | Venue / Elegance | Venue 维持 4、Elegance 3→4；Overall 约 +0.08 |
| C7 消融 A5 删除冗余组件（膜电位累加解码 vs 确定性计数） | Elegance | Elegance 3→4；Overall 约 +0.08 |

**反向条件（会坐实 fatal / 降分，是「不因修订版默认更高」的护栏）**：
- 若 M0 推导显示 T1 可由 `A(E₁W₂)` + QCFS 零期望偏置 + 行和定义一行代数照搬 Deng&Gu 递归 → F2 回潮为 fatal，Novelty 3→2、Conceptual 3→2、Method 3→2、Acceptance 3→2，加权回落约 **2.6–2.7**（= 1.0–2.9 段），并重新触发 novelty / method / beyond-modules 三条 fatal gate。
- 若推论层针对检索命中近邻（已有工作给出 ρ_n 加权 margin 偏置 / 相对误差尺度不变 / 行和-行范数比判据）→ Novelty 3→2，F2 回潮。
- 若实测 conversion loss 与 ρ_n/T 无单调关系、或 ρ≈1 的 CNN 上出现「我们显著更好」 → 核心判据被推翻，pivot 为纯 benchmark 故事（rev2 §1 自设条件）。
- 若 κ_n 与 T2 张力不可调和（`‖a_n‖₂` 随 ρ_n 增长使 κ_n 近似不变）→ 单调预测不成立，Conceptual / Method 降 1。
- 若原版动态 / 非线性 ViG 上恒等式仍成立 → 适用边界写错，须扩展算子类或放弃 T1/T2（rev2 §1 自设条件）。
- 若 β* 对一般 A 不成立且无替代闭式 → Method 3→2 并触发 fatal gate。
- 若把内部先验（T≤8 ANN−1.5pp 带内、或「成稿实测」数值）写入公开证据 / 结果栏 → 依 S6 诚信门停止，不升分。

**说明**：C1–C4 是升到 `revise` 段（3.7+）的必要非充分条件；即便四条全过，仍需 Q1–Q2 档下的实证与 novelty 站稳才可能改推荐。本评审不预判其结果。

---

## Confidence:

- **综合 Confidence：Medium**（依 `calibration.md` 标签）。
- 理由：(i) 组件层 closest-work 覆盖明确（用户提供独立核验结论），F1/F3 的文本变化可直接核查，工件清单可直接核查（无 `matched-protocol.md`），evidence plan 文本可直接核查 —— 这些判断置信度高；(ii) **但 M0 核心推导尚未做**，T1/T2/κ_n 是否超出 prior-art、κ_n 单调性是否成立、κ_n–T2 张力是否可解，全属「未给出的机制 / 未证定理」，Method / Novelty / Conceptual 的置信度仅 3；(iii) **推论层 novelty 未检索**，novelty 上限被封顶、置信度下调；(iv) 各目标期刊当年官方 policy / review form 未核验（AC conf 3）；(v) 视觉侧无任何正式实验，实验判断是「plan 可信 + 证据缺失」而非「结果已知」。
- **依公平规则**：不因 confidence 为 Medium 而下调 idea 分数；分数（3.2）与置信度（Medium）分开报；低置信度单独引导下一步检查（见 Optional next-module decision 与 Evidence that would change my score）。
- 各维度 Confidence 已在 Rubric scores 表逐维列出，分数与置信度不在此重复。
- **Development potential 保持 medium 而非 high 的置信度说明**：升 high 需「M0 推导兑现 T1/T2 + 推论层检索无近邻 + κ_n 单调性成立」三项同时支持；当前均未知，故 medium 是如实取值。

---

## Strict reviewer comments:

> 依 `strict-idea-review.md` Harsh Reviewer Lens：短、诊断式、每条带 anchor，不作动机性缓冲。

1. **关于 T1 的非平凡性**（Anchor：Deng&Gu ICLR 2021、QCFS/FTBC、Dual-Phase TNNLS 2024，用户提供核验）：把逐层误差递归里的归一化矩阵换成一般非负 A，`A·1=ρ_n·1` 加 `E[E₁]=β−1/(2T)` 即得你的 ρ_n 加权项。请指出 T1 中哪一步是 prior-art 递归推不出的，而不是「把 ρ=1 假设放宽后写下来」；M0 里请给非平凡性证明，否则这是表述而非新推论。
2. **关于 T2 与 κ_n 的一致性**（Anchor：rev2 §1 T2 与 κ_n 定义、M0 待办清单）：你一边说相对误差 ρ-不变（由 `‖a_n‖₂‖DW‖₂/(TΔ_n)` 控制），一边预测 conversion loss 差距随 ρ_n/T 单调增大。若 `‖a_n‖₂` 随 ρ_n 增长，κ_n 近似不变，单调预测从何而来？请把 κ_n–T2 张力列入 M0 并给出单调性成立的区间条件。
3. **关于核心理论尚未证明**（Anchor：rev2 §1 R1/R2/R3、M0「未过不得进 P4」）：本文的核心贡献是「理论判据」，但一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性、两解码兼容性、冗余消融全部列为实验前待办。定理未证而主张「何时失效判据」，method soundness 不成立；请先把 M0 做完再谈判据。
4. **关于 novelty 检索边界**（Anchor：Search basis 推论层 `not searched`）：closest-work 表核验的是组件归属（β*、偏置、等式、计数、两阶段归谁），不是「ρ_n 加权 margin 偏置 / 相对误差尺度不变 / 行和-行范数比判据」是否已被 2025–2026 工作给出。请针对推论本身做一次检索，别用组件层的 `searched` 覆盖推论层。
5. **关于证伪条件的范畴错位**（Anchor：rev2 §1 Falsification 第 4 条、§4 F2 行）：你已把贡献改为「判据 + 横评 + 边界」，不再主张新方法，却仍用「与 PASCAL / TPP 等价 → 判据被推翻」作裁决。一个分析判据不能与一个转换方法等价。请改写为「conversion loss 与 ρ_n/T 无单调关系」或「κ_n 大样本未显示欠校准」这类针对判据的可测量。
6. **关于工件与证据兑现**（Anchor：工件目录清单、rev2 §4 F3 行、用户硬要求）：F3 声称「成文 `matched-protocol.md`」，但 startup packet 目录内无此文件；PASCAL / TPP / CS-QCFS / ECL 仍为「待自行复现」计划；视觉侧零正式实验（按硬要求不判 fatal，但请如实记为证据缺口）。另：rev2 卡中「成稿 §3.2 已证」「成稿 §5.1 实测」及 ρ_n=5.75/169、`var(U)=0.082` 等数值，在本包内无对应成稿，且与 `claim-evidence-matrix.md` 的「全部 `<TBD>`、零实验结果数值」纪律冲突 —— 成文时请澄清来源或删除，不得写入公开证据 / 结果栏。
7. **关于 venue 与主轴**（Anchor：rev2 §0、§1 Contribution type）：降到 TNNLS / Q1–Q2 档、ImageNet 消解是对的；但贡献仍是「判据 / 横评 / 边界」三章并列，主轴收敛更多在措辞。请把三者绑定为「一个 κ_n 判据贯穿横评与边界」的单一叙事，别让讨论阶段把它读成 benchmark 短文。

---

## Fixability table:

依 `calibration.md` 字段。Owner skill 仅列出建议归属，**未执行任何 handoff**（见 Optional next-module decision）。

| Issue | Affected dimension | Severity | Fix class | Can fix before writing? | Required evidence or design change | Risk-reduction condition | Development-potential impact | Owner skill |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 核心理论 M0 未证（β* / ‖A‖ 界 / T1T2 证明 / κ_n 单调性 / 兼容性） | Method / Novelty / Acceptance | high（准 fatal） | method-redesign | yes（纸面） | 完成 M0 全部推导 + 数值验证；证明 T1 非平凡性 | 推导自洽、非平凡、数值通过 | 中—高 | ccf-idea-optimizer |
| Q2 推论层 novelty 未检索 + 一行代数 objection | Novelty / Conceptual | high（准 fatal） | novelty-grounding | no（需检索 + 推导） | 推论层公开检索 + T1 相对 Deng&Gu 的非平凡性证明 | 无近邻命中且非平凡性成立 | 低—中 | ccf-literature-searcher（若授权）/ ccf-idea-optimizer |
| Q3 κ_n 与 T2 张力未量化、单调性未证 | Method / Conceptual / Experimental | medium | method-redesign | yes（纸面 + 数值） | 给出单调性成立的 ‖a_n‖₂/ρ_n 区间 + 数值验证 | 张力可解释、预测成立 | 中 | ccf-idea-optimizer |
| F2（降级后）novelty 薄增量 | Novelty / Acceptance | medium | novelty-grounding | no | 接受 Q1–Q2 增量诊断定位；全文一致不声称「prior-art 无法得到的新结果」 | novelty 主张与核验 / 检索结论一致 | 中 | ccf-idea-optimizer |
| W2 `matched-protocol.md` 未成文 | Experimental / Acceptance | medium | evidence-design | yes | 补写工件：同骨干 / 同 T / 同 θ / 同 calibration / 同 CL 定义 / 全基线清单 | 协议可复算、可比、工件存在 | 高 | ccf-experiment-designer |
| W3 PASCAL/TPP/CS-QCFS/ECL 待自行复现 | Experimental | high | evidence-design | no（需实现） | 第一批 must-rerun 复现并纳入横评 | 最决定性基线可复算 | 高 | ccf-experiment-designer |
| W1 视觉侧零正式实验 | Experimental | medium（按硬要求不判 fatal） | evidence-design | no | 统一协议下完整视觉侧实验 + conversion loss–ρ_n/T 曲线 | 中心判据获得实证支撑 | 高 | ccf-experiment-designer |
| W6 证伪条件范畴错位 | Experimental / Method | medium | evidence-design | yes | 第 4 条改写为针对判据的可测量 | 证伪条件与贡献类型自洽 | 中 | ccf-experiment-designer |
| W7 冻结 KNN 代价未量化（R4） | Problem / Method | medium | evidence-design | no | 定量报告相对原版 ViG 的性能代价 | 适用类代表性被实证界定 | 中 | ccf-experiment-designer |
| W8 组件冗余未消融（A5） | Elegance | low | method-redesign | partly | 消融膜电位解码 vs 确定性计数 | 冗余组件被删除 | 低—中 | ccf-idea-optimizer |
| W10 官方当年 venue policy 未核验 | Venue fit | low | venue-switch | yes | 核验 TNNLS 当年官方 policy / review form | venue 定位与官方规则自洽 | 低 | ccf-submission-checker（若授权） |
| W11 「成稿实测」数值 / 章节引用与全 `<TBD>` 纪律冲突 | Evidence integrity | medium | evidence-design | yes | 澄清来源或删除；不得写入公开证据 / 结果栏 | 全包零编造、纪律一致 | 中 | ccf-integrity-auditor（若授权） |

> 「用户提供的未公开先验（图节点分类 T≤8 ANN−1.5pp 带内；rev2「成稿实测」数值，未发表）」不列入任何 Issue 的 required evidence；不得用它替代公开实验。

---

## Upgrade / pivot actions:

依 `SKILL.md` workflow #8 标签分类。每条为具体动作，不含通用套话。

- **[problem-refinement]**：给出「非行随机算子（ρ_n≠1）在主流 GNN / ViG 部署中普遍存在」的公开证据，把中心问题从「人为构造的算子类」锚到「真实部署类」；量化冻结 KNN 相对原版 ViG 的性能代价（R4），不得隐瞒。
- **[method-redesign]**：完成 M0 全部纸面推导 —— 一般 A 下 β* 严格推导或反例条件、`‖A‖` 跨层误差上界、T1/T2 严格证明、**T1 相对 Deng&Gu 递归的非平凡性证明**、κ_n 单调性成立区间、两解码兼容性命题、A5 冗余消融；显式列入并解决 κ_n 与 T2 的内部张力。
- **[novelty-grounding]**：针对推论本身做一次公开检索（通用关键词，不粘贴私有措辞），确认「ρ_n 加权 margin 偏置 / 相对误差尺度不变 / 行和-行范数比判据」无近邻命中；全文一致声明不发明任何已占组件，**且不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」**，除非 M0 + 检索 + 单调性实测三者同时支持。
- **[evidence-design]**：补写 `matched-protocol.md` 工件（所有基线含 PASCAL/TPP/CS-QCFS/ECL 在同一批固定骨干、同 T/θ/calibration/CL 定义重跑）；把 §1 第 4 条证伪条件从「与 PASCAL/TPP 等价」改写为「conversion loss 与 ρ_n/T 无单调关系」或「κ_n 大样本未显示欠校准」；报告 conversion loss–ρ_n/T 曲线、恒等式浮点残差、κ_n 逐节点欠校准率、C5 失效边界、R4 代价；补视觉侧正式实验。
- **[feasibility-check]**：确认 RTX 3060 12GB / 远端 4090（已授权，guidance 阶段不提交）上 ViG-SNN 与全套基线可跑通；补齐 GCN 消息传递实现来源（当前 `TBD/需确认`）与 `torchvision` 补装。
- **[venue-switch]**：维持主投 IEEE TNNLS / Q1–Q2 档；结构上把「判据 / 横评 / 边界」绑定为单一叙事；成文前核验当年官方 policy / review form。
- **[pivot]**：若 M0 推导显示 T1 可一行照搬、或推论层检索命中近邻、或 conversion loss–ρ_n/T 无单调关系，则放弃「理论判据」定位，pivot 为「统一协议 benchmark + 失效边界诊断」型贡献，并把 novelty 完全收敛到横评与边界（rev2 §1 已备用此路线）。
- 不输出 **[abandon]**：中心判据可测（残差、单调性、κ_n 逐节点检验、C5 边界）、M0 路线可命名、stage-aware 规则不满足 abandon 条件。

**最小可行修复路线（按依赖顺序，纸面优先、无算力成本）**：
1. **先做 [method-redesign] 的 M0 第 1 步**：一般 A 下 β* 推导 + **T1 相对 Deng&Gu 递归的非平凡性证明** + κ_n 单调性条件 —— 这是判定 F2 是否回潮的最便宜、最决定性一步；若 T1 坍缩为一行代数，直接转 [pivot]，不必再做后续实验。
2. **同时做 [novelty-grounding] 的推论层检索**：通用公开关键词确认无近邻命中；与第 1 步结果共同决定 novelty 是否可站稳 3。
3. **再做 [evidence-design] 的第 1 步**：补写 `matched-protocol.md` 工件 + 修正第 4 条证伪条件；**仅先复现 PASCAL 与 TPP** 两个最决定性基线，在同一批固定骨干上跑 CIFAR-10/100 + Planetoid 的最小横评，测 conversion loss–ρ_n/T 曲线 —— 这是判定判据是否被实测推翻的最小可测实验。
4. **依据第 3 步结果决定**：若单调性成立且有可归因诊断能力 → 继续补齐全套基线 + 视觉侧实验 + C5/R4 量化，主投 TNNLS 档（`revise` 方向）；若单调性被推翻或与近邻等价 → 执行 [pivot]，把贡献收敛为「统一协议横评 + 失效边界」。
5. 全程不把「用户提供的未公开先验（T≤8 ANN−1.5pp 带内；rev2「成稿实测」数值）」写入任何证据表或结果栏；成文时按 W11 澄清或删除「成稿」引用。

---

## Evidence that would change my score:

**会升分的证据（全部需为公开可复算、非编造）**
- M0 全部纸面推导通过：一般 A 下 β* 严格推导、`‖A‖` 误差上界、T1/T2 严格证明、κ_n 单调性成立区间、两解码兼容性、A5 消融（影响 Method / Novelty / Conceptual / Acceptance）。
- T1 相对 Deng&Gu 递归的**非平凡性证明**（该结论在 ρ=1 文献中退化消失、并带来其无法给出的可证伪预测）（影响 Novelty / Conceptual，是 F2 的唯一实质解）。
- 推论层针对检索无近邻命中（影响 Novelty / Confidence）。
- matched-protocol 统一横评（含 PASCAL / TPP 自行复现）显示 conversion loss 与 ρ_n/T 的单调关系、κ_n 大样本欠校准率符合预测（影响 Experimental / Acceptance）。
- 「非行随机算子在主流 GNN / ViG 中普遍存在」的公开证据 + 冻结 KNN 代价量化（影响 Problem / Timeliness）。
- 原版动态 / 非线性 ViG 失效边界（C5）的定量报告（影响 Method / Experimental）。
- 组件消融证明每个组件独立不可替代（影响 Elegance）。

**会坐实 fatal / 降分的证据**
- M0 推导显示 T1 可一行代数照搬、或推论层检索命中近邻 → F2 回潮为 fatal，Novelty 3→2，整体回 2.6–2.7。
- conversion loss 与 ρ_n/T 无单调关系、或 ρ≈1 的 CNN 上「我们显著更好」 → 核心判据被推翻，pivot 为纯 benchmark 故事。
- κ_n 与 T2 张力不可调和（κ_n 近似不变） → 单调预测不成立，Conceptual / Method 降 1。
- 原版动态 / 非线性 ViG 上恒等式仍成立 → 适用边界写错，须扩展算子类或放弃 T1/T2。
- β* 对一般 A 不成立且无替代闭式 → Method 3→2 并触发 fatal gate。
- 把内部先验或「成稿实测」数值写入公开证据 / 结果栏 → 依 S6 诚信门停止，不升分。

**明确不作为证据的项**：任何录用概率、真实审稿人意见、meta-review、未核验的官方当年规则、以及「用户提供的未公开先验（图节点分类 T≤8 ANN−1.5pp 带内；rev2「成稿实测」数值与「成稿 §3.2/§5.1」引用，未发表、不充当公开证据）」。本报告未生成上述任何一类，也未生成任何实验结果数值。

---

## Recommendation:

**`pivot-with-rescue-route`**（5 选 1 之内；用户硬要求）

理由（与分数、fatal gates、stage-aware 规则一致）：
- 加权 3.2（3.16）落在 `calibration.md` 的 **3.0–3.6 段 → `pivot-with-rescue-route`**，**由分数段直接得出，不依赖 fatal gate 压顶**（五条 gate 当前均不硬触发，两条临界）；这不是把分数抬到 `revise`（3.7+）段，也不是靠 gate 强行压回 `pivot`。
- 不取 `needs-literature-search`：novelty 按用户指令标 `searched`（组件层，依据用户提供的独立核验结论），结论是「高重叠 + 薄增量」而非「未知」；推论层未检索作为边界与置信度处理（封顶 novelty 3、conf 3），不升级为推荐值。
- 不取 `abandon`：中心判据可测（恒等式残差、conversion loss–ρ_n/T 单调性、κ_n 逐节点检验、C5 边界），且存在具名修复路线（见最小可行修复路线），依 `strict-idea-review.md` 不满足「无可测主张且无重构」条件。
- 不取 `revise` / `accept-to-develop`：核心理论判据全部 M0 未证、视觉侧零正式实验、novelty 薄且推论层未检索、κ_n–T2 张力未解、matched-protocol 工件未兑现；任一未解都不足以升档。

含义：保留最佳要素（T2 的 ρ-不变性解释、κ_n 可先验计算判据、统一协议横评、失效边界诊断），改变**方法理论**（M0 推导兑现 + 排除一行代数 objection）、**证据**（兑现 matched-protocol 工件 + 复现 PASCAL/TPP + 实测单调性）、**novelty 定位**（推论层检索 + 接受 Q1–Q2 增量诊断定位）中的至少一组。F1 已解决、F2/F3 降级为可修复弱点，但**没有任何一条「已解决」到足以让整体升出 `pivot-with-rescue-route` 段**。

---

## Optional next-module decision:

- **CCFA Handoff Mode: PARTIAL**（依 `SKILL.md` 与 `handoff-modes.md`）。本任务为**独立红队评审**，用户未请求任何 sibling-skill 切换，也未授权把未发表 idea 文本用于检索；依 workflow #10「if a module is denied, stop at verdict, risks, and action queue」，本评审**停止在 verdict / risks / action queue，不执行任何 handoff**。
- 未切换的模块：`ccf-idea-optimizer`（M0 推导 / 主张收敛）、`ccf-experiment-designer`（matched-protocol 工件 + 横评）、`ccf-literature-searcher`（推论层针对检索，需用户显式授权）、`ccf-submission-checker`（核验目标期刊当年官方 policy / review form）、`ccf-integrity-auditor`（W11 全包纪律一致性）。
- 若用户**显式授权**后续切换，按 PARTIAL 模式建议顺序：`ccf-idea-optimizer`（先做 M0 第 1 步，纸面为主、无算力成本）→ `ccf-literature-searcher`（推论层检索，公共关键词）→ `ccf-experiment-designer`（再解 W2/W3，含 PASCAL/TPP 复现）→ 视单调性结果决定是否进入后续写作。本评审不代写、不模拟上述模块的输出，也不预判其结果。
- 隔离声明：上述建议不含任何已执行的检索、实验或写作，不含任何录用概率与真实审稿记录。

---

## Checklist status:

依 `SKILL.md` Mandatory Review Checklist（standard 模式 10 条）逐条如实标注。

| # | 检查项 | 状态 | 说明 |
| --- | --- | --- | --- |
| 1 | Target venue/journal、venue family、field、assumptions 明确 | pass | 见 Target venue/journal and assumptions；按 Q1–Q2 期刊档评 + 标尺声明 + 官方当年政策未核验已注明 |
| 2 | 每个 idea 归一化为 problem / gap / root challenge / insight / method mechanism / expected evidence / limitation | pass | 见 Normalized idea（7 要素 + 内部先验隔离标注） |
| 3 | Literature status 标注为 searched / partially searched / user-provided only / not searched | pass | novelty = `searched`（组件层，用户指令）；本会话检索动作 = `user-provided only`；**推论层 = `not searched`**（新增边界）；见 Search basis |
| 4 | standard 模式有来自 public-safe literature search 的 closest-work table，除非用户禁止浏览或隐私阻止 | **partial** | closest-work 表已建（8 条，字段齐全，针对 rev2 重评），但来源为**用户提供的独立文献核验结论**，本会话未执行公开检索，且推论层未检索；依据：用户明确指定 search basis 与已核验结论，依 `privacy-and-evidence.md` 未把未发表 idea 文本用于查询；未编造任何 URL/DOI |
| 5 | 五个专家角色独立应用：field / method / experiment / AC-venue / skeptical prior-art | pass | 见 Per-expert reviewer notes，各自独立 + Panel Synthesis，分数与置信度分开 |
| 6 | 所有 rubric 维度 1–5 打分或标注 n/a 与理由；每个 ≤3 含 deduction / evidence basis / repair condition / 预期分数变化 | pass | 10 维全打；8 个 ≤3 项均有完整明细块（扣分理由 / 证据基础 / 为什么重要 / 修复条件 / 预期分数变化 / development-potential effect）；Feasibility=4、Venue=4 在表内给出 deduction 与 repair |
| 7 | Fatal risks 与可修复弱点、局部细化分开 | pass | 见 Serious blockers：F1 已解决 / F2、F3 降级为可修复弱点（逐条判定表）+ Q1–Q4 准 fatal 弱点 + W1–W11 fixable + 隔离项 |
| 8 | Confidence 与 score 分开报 | pass | 综合 Confidence=Medium 单列；各维 Confidence 在 rubric 表；未因置信度下调分数 |
| 9 | 推荐值为 5 选 1 之一；`abandon` 仅用于无可测主张且无重构 | pass | `pivot-with-rescue-route`；abandon 条件已论证不满足 |
| 10 | 任何可选模块切换遵循 CCFA handoff mode；若被禁用则只输出 upgrade actions | pass | PARTIAL 模式，未执行 handoff，仅输出 Upgrade / pivot actions 与建议 owner |

补充标准模式 `task-modes.md` 状态：
```text
Mode: standard
Checks run: 完整 mandatory checklist + 输出契约 21 字段 + 定量反馈 + panel 纪律 + fatal gates + 分数段映射 + 逐维变化分解 + Output Quality Gate
Checks skipped: 无（除 #4 标 partial）
Unresolved risks: M0 核心推导未做、推论层未检索、κ_n 单调性与 κ_n–T2 张力未解、matched-protocol.md 未兑现、PASCAL/TPP 待复现、视觉侧零正式实验、官方当年 venue policy 未核验、「成稿实测」数值与全 <TBD> 纪律冲突
```

---

## Output self-check:

依 `review-output-standards.md` Output Quality Gate 与 `task-modes.md` Output Quality Gate 逐项自检（作为读者通读一遍后确认）。

| # | 检查项 | 结果 | 具体确认 |
| --- | --- | --- | --- |
| 1 | 小节顺序匹配承诺的输出契约 | ✓ | 从 `## Verdict first:` 到 `## Output self-check:` 共 **21 个契约字段**，顺序与 `SKILL.md` Output Contracts（单 idea / standard）完全一致；首字段即 Verdict first，末字段即 Output self-check |
| 2 | 每个表格有合法 Markdown 分隔符且每行列数一致 | ✓ | Rubric 表 6 列、Closest-work 为字段块（非表）、F1/F2/F3 判定表 5 列、逐维分解表 3 列、Score-change 表 3 列、Fixability 表 9 列、Checklist 表 4 列、本表 4 列；逐行核对列数一致，单元格内无裸 ASCII `\|` 破坏分隔（公式内 `‖A‖`、`ρ_n/T`、`κ_n` 等不含竖线） |
| 3 | 分数、置信度、推荐内部一致 | ✓ | 加权计算 316/100 = 3.16 → `**Overall:** 3.2`（一位小数）；1–10 转换 ≈ 6.3；综合 Confidence=Medium 与各维 Confidence 分开；3.2 落在 calibration 3.0–3.6 段 → `pivot-with-rescue-route`，五条 fatal gate 均不硬触发、两条临界，已在 Weighted final score 字段解释分数段与 5 选 1 的映射，无矛盾；相对第一次 +0.7 的逐维分解合计 +0.66 与 3.16 一致 |
| 4 | 项目符号语法平行、动作风格一致 | ✓ | Upgrade / pivot actions 统一用 `[标签] + 动作动词` 开头；Fixability / Score-change 用名词短语或条件句 |
| 5 | 因果/递进逻辑显式（问题→原因→后果→行动） | ✓ | 每个 ≤3 块按「扣分理由→证据基础→为什么重要→修复条件→预期变化」排列；F1/F2/F3 判定按「处理→判定→依据→残留」；最小可行修复路线按依赖顺序编号 |
| 6 | 语言内标点一致 | ✓ | 正文中文全角标点（，。；：）；公式、字段名、文献名、venue、英文缩写、代码标识符保留半角；Markdown 表格分隔符与代码块为半角（属格式必需） |
| 7 | 无 TBD / TODO / [fill] / 空标题占位 | ✓ | 无占位符；所有字段均有实质内容；引用他工件中的 `<TBD>` 属「描述其纪律」而非本报告的占位符 |
| 8 | 无通用套话（「需要更多实验 / 创新性不足 / 进一步完善 / 加强 related work」等）无锚点残留 | ✓ | Strict reviewer comments 7 条均带 Anchor；每条批评均指向具体 claim / 机制 / prior-art / 缺失工件 / 逻辑残留 / 可行性约束，并给出对应修复或 pivot |
| 9 | 每个 ≤3 分项含扣分理由 / 证据基础 / 修复条件 / 预期分数变化（用户硬要求） | ✓ | 8 个 ≤3 维度各一个明细块，四项齐全，另附 Why it matters 与 Development-potential effect；Feasibility=4、Venue=4 不触发 |
| 10 | 五个专家角色独立、各自给具体拒稿级质疑或说明为何没有；置信度与分数分开 | ✓ | 5 个角色均含 Score tendency（分数）与 Confidence（置信度）两行；均给出 strict rejection-grade concern + Anchor + Why + Fatal + Repair + Development note；无角色被强行安排「无质疑」或赞扬，Panel Synthesis 未平均掉致命弱点 |
| 11 | fatal risk 与可修复弱点明确区分；含 score-change conditions 与最小可行修复路线 | ✓ | Serious blockers 的 F1 已解决 / F2、F3 降级 + Q1–Q4 准 fatal 弱点 + W1–W11 fixable + 隔离项；Score-change conditions 表 C1–C7 含升分与反向降分；Upgrade / pivot actions 内含按依赖排序的「最小可行修复路线」5 步 |
| 12 | 推荐值仅为 5 选 1 之一 | ✓ | `pivot-with-rescue-route`（accept-to-develop / revise / pivot-with-rescue-route / abandon / needs-literature-search 五者之一） |
| 13 | 禁止编造：文献 / 数值 / 实验结果 / 评审意见 / 录用概率 | ✓ | 全部文献仅来自用户提供的核验清单（venue/year 照录，未附 URL/DOI）；无实验结果数值、无录用概率、无真实审稿人 / meta-review 引用；专家意见与 Strict reviewer comments 已声明为「本红队 panel 独立判断」；加权分数与预期变化为按 rubric 计算 / 条件性表述，非实验结果；rev2「成稿实测」数值仅作用户提供材料陈述被隔离标注，未被本报告当作结果引用 |
| 14 | novelty 状态标为 searched 并写明边界 | ✓ | Search basis 标 `searched`（组件层），并写明 4 条边界（证据来源为用户核验结论、本会话未重新检索、覆盖范围、**推论层 `not searched`** 并据此封顶 novelty 3 / conf 3）；Novelty delta 逐条复核 delta 为「假设放宽展开 / 解释性增量 / 薄判据增量 / 工件未兑现 / 真实但增量」 |
| 15 | 未发表内部结果仅标注为「用户提供的未公开先验」 | ✓ | Target venue 假设、Normalized idea、Serious blockers、Fixability、Upgrade actions、Evidence 中凡提及 T≤8 ANN−1.5pp 带内及 rev2「成稿实测」数值 / 「成稿 §3.2 / §5.1」引用，均标注「用户提供的未公开先验（未发表、不充当公开证据）」，且明确不进入 evidence / 打分依据；W11 记录其与全 `<TBD>` 纪律的冲突 |
| 16 | 文件用中文撰写、保留技能要求的全部字段标题 | ✓ | 21 个英文契约字段标题原样保留（Verdict first: … Output self-check:），正文全部中文 |
| 17 | Verdict first 给结论、回复含 `**Overall:**` 行与 recommendation | ✓ | Verdict first 段含完整结论、F1/F2/F3 逐条判定表与综合 recommendation；`**Overall:** 3.2` 在 Weighted final score 字段以独立行给出；聊天回复另给 `**Overall:**` 行、recommendation 与 F1/F2/F3 逐条判定 |
| 18 | F1/F2/F3 逐条判定（三选一）+ T1/T2 + κ_n 特别回答（用户硬要求） | ✓ | Verdict first 与 Serious blockers 各给一张逐条判定表，明确 F1=已解决 / F2=降级为可修复弱点 / F3=降级为可修复弱点并附依据；Novelty delta 设「特别回答」小节，明确结论为「介于两者之间、更靠近已知结论的假设放宽推论、不构成 prior-art 无法得到的新数学结果」，并给 6 条不可判「已解决」的依据 + 反向条件 |

**最终一致性确认**：本报告为**第二次独立红队评审**，未由第一次会话代写或模拟打分，未修改第一次报告；如实承认 rev2 的有限进步（F1 主张层消解、F3 设计层消解、venue 对齐、T1/T2 有限增量），同时逐条论证「+0.7」全部由可核查文本事实与用户硬要求强制、四个维度保持不变、无 +2 跳升、推荐仍为 `pivot-with-rescue-route`；未把未发表内部结果或「成稿实测」数值当公开证据；未把「视觉侧零实验」自动判 fatal（遵循用户硬要求，仅如实记为证据缺口并评估 plan 可信度）；未越权执行任何模块切换；未生成任何编造文献 / URL / DOI / 实验结果数值 / 录用概率；所有分数证据基础可追溯至 rev2 文本、第一次报告、用户提供的 prior-art 核验结论与工件目录清单。