## Verdict first:

本评审为**独立 idea 红队评审**（standard 模式，依据 `ccf-idea-reviewer/SKILL.md` 及 `references/strict-idea-review.md`、`rubric.md`、`calibration.md`、`expert-panel.md`、`../ccf-common/references/review-output-standards.md` 等）。评审对象为单篇 idea：OAC（Operator-Agnostic Conversion）。本报告内所有专家意见、严格评审意见均为**本红队 panel 基于 idea 文本与用户提供的 prior-art 事实作出的独立判断**，不代表任何真实审稿人、meta-review、录用记录或录用概率；本报告不承诺任何分数变化或录用结果。

**结论（先给）**：当前 formulation 在 CCF-A 主会 / Q1 期刊档（CVPR / ICCV / NeurIPS / IEEE TNNLS 档）**不具备可接收性**，但**不属于应 abandon 的情形**。三条 fatal risk 同时成立：① 中央科学问题（"非网格、数据依赖邻域聚合的统一算子级误差刻画"）被方法自身的"固定、非负、线性矩阵 A + 冻结 KNN 图 + 线性化 max-relative"适用条件抽空，方法与问题存在主张级错位；② novelty 的用户提供核验结论显示数学组件大半已被占，剩余 delta 主要是已知结论的矩阵记号重述 + 两个已知模块的确定性化组合 + 新数据集应用；③ 统一协议 conversion loss 横评存在"基线在原始骨干 / OAC 在被修改骨干"的可比性两难，且最相关的 PASCAL、TPP 尚无官方代码需自行复现。视觉侧**尚无任何正式实验**（用户明述），使中心新颖主张零实证支撑。但中心主张仍可测（恒等式数值验证、统一协议横评、失效边界实验），且存在明确、可命名的最小可行修复路线，故按 stage-aware 规则不判 `abandon`。

加权总分 `**Overall:** 2.5`（1–5 加权尺度，保留一位小数；对应 1–10 尺度为 5.0）。推荐值：`pivot-with-rescue-route`。当前会议就绪度：low；发展潜力：medium。

---

## Target venue/journal and assumptions:

- **目标**：CCF-A 主会 / Q1 期刊，用户点名档位为 CVPR / ICCV / NeurIPS / IEEE TNNLS。
- **Venue family**（依 `ccf-a-venue-map.md`）：主属 "AI, ML, CV, NLP" 族（AAAI / NeurIPS / ICML / ICLR / CVPR / ICCV）；IEEE TNNLS 属类脑/SNN 期刊向，非该表内 CCF-A 会议族，本报告按用户点名的"Q1 期刊档"处理。
- **领域**：类脑计算 × 视觉表征；具体子域 ANN→SNN 转换的误差分析与转换协议。
- **评审假设（均由用户在本请求中提供，本评审不另行假设）**：单卡 RTX 3060 12GB / CUDA 12.8 / torch 2.11，大规模可上远端 4090（用户已授权）；主战场为 CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS、Planetoid 三图；ImageNet-1K 需申请（G2 不可用）；基线 QCFS / FTBC / TPP / Parallel Conversion (ICML'25) / DCGS (ICML'25) / AdaFire (AAAI'25) 有官方代码，PASCAL / CS-QCFS / ECL 无代码需自行复现。
- **未发表内部结果的标注约定**：用户提供的"同一转换思路在图节点分类上 T≤8 达到 ANN−1.5pp 带内"一律标注为 **「用户提供的未公开先验（未发表、不充当公开证据）」**，不计入任何证据强度、不计入打分依据、不作为 novelty 支撑。
- **本评审未做的事**：未核验各目标会议/期刊当年官方 policy、page limit、review form、deadline（依 `source-notes.md`，此类当年政策须查官方页；本任务为 idea 阶段评审，按通用 contribution taste 推理，不引用任何具体当年规则）。未执行任何公开文献检索，未生成任何 URL / DOI。

---

## Search basis:

- **novelty 状态**：`searched`（按用户硬要求，依据用户提供的、已由独立文献核验得到的 prior-art 结论）。
- **该 `searched` 状态的边界（必须写明）**：
  1. 证据来源为**用户提供的独立文献核验结论**（"用户提供的 prior-art coverage"），**本评审会话未重新执行公开检索**；故严格区分时，closest-work 证据属于 `user-provided only` 而 novelty 判定按用户指令记为 `searched`。二者不矛盾：前者是证据来源，后者是 novelty 状态标签。
  2. 覆盖边界以用户列出的核验清单为限：不覆盖该清单之外的"算子级统一误差理论"专门文献，不覆盖 2025 年之后的工作，不覆盖未列入核验的 arXiv 预印本。
  3. 依 `privacy-and-evidence.md`，未把未发表的私有 idea 表述放入任何检索查询；依 `source-notes.md`，closest-work 表不提供本轮未核验的链接/DOI（禁止编造 URL）；不引用 MDPI 来源。
  4. 因此 novelty 置信度标为高（5/5）仅表示"在用户给定核验覆盖内，重叠结论明确"；不表示"全库无遗漏"。综合 Confidence 另见 Confidence 字段。
- **literature status label**（checklist #3）：`searched`（novelty 判定用）／`user-provided only`（本会话检索动作用），非 `partially searched`、非 `not searched`；不做 `high novelty` 断言。
- **public-safe queries**：本会话未执行，故无查询记录；如后续需要，按 `strict-idea-review.md` 应以通用公开关键词（ANN-to-SNN conversion error / operator-agnostic / spiking ViG / KNN graph message passing / conversion loss benchmark）先行，不粘贴私有措辞。
- **source policy**：仅使用用户提供的 primary venue/year 信息作为 prior-art 锚点；不把 citation count 当质量；不把推论当事实。

---

## Stage and development potential:

```text
Current conference readiness: low
Development potential: medium
Main reason it is not ready: 三条 fatal risk 同时成立（主张-适用条件错位、novelty 重述/组合、横评可比性两难），且视觉侧零正式实验，中心新颖主张无实证支撑。
Best rescue route: 把中心主张从"统一非网格数据依赖邻域聚合"收敛为"固定线性传播算子类上的算子级精确误差统一 + 该类算子上与全套基线的统一协议横评 + 明确失效边界"，并把 ② 的确定性化做成相对 PASCAL/TPP 的可测增益；同时补齐 PASCAL/TPP 自行复现与视觉侧实验。
Evidence needed to decide: 同一冻结/线性化骨干、同 T、同 θ、同 calibration 数据下的全套 conversion loss 横评是否显示可归因于"算子级统一"的稳定增益，以及 β* 对一般 A（行和≠1）的推导是否成立。
```

附 development potential 判定（依 `calibration.md`）：medium——最佳要素（固定线性算子的统一误差视角、统一协议横评、失效边界分析）有用，但问题、机制、venue 或证据路径至少一项必须改变；不是 high（无法在不改核心问题的前提下变 competitive），不是 low（不止一个窄片段可复用）。

---

## Normalized idea:

| 要素 | 归一化内容 |
| --- | --- |
| Problem | ANN→SNN 转换的误差分析长期绑定规则网格上的逐元素算子；当骨干引入非网格、数据依赖邻域聚合（ViG KNN 图、ViT attention、GNN 消息传递）时，缺少统一的算子级误差刻画与统一协议下的横评。 |
| Gap | 现有转换方法各自校准自己的算子；用户核验后认定的真空白仅三处：① 固定线性传播算子的算子级精确统一（层类型无关）；② TPP 第二相的特定确定性化（零条件方差、无 RNG）；③ 首次 ViG 脉冲化 + 同一算子跨视觉骨干与图消息传递的统一协议 conversion loss 横评。 |
| Root challenge | 数据依赖、动态、非线性邻域聚合（KNN 图随输入变化、max-relative 含 max、softmax attention 随样本变化）使传播算子不再固定线性，逐元素误差递推无法直接迁移。 |
| Insight（声称） | 把传播算子抽象为固定、非负、线性矩阵 A，则转换误差有精确恒等式 `B̂₂ − B₂ = A (E₁ W₂)`，`E₁ = count₁/T − ReLU(B₁)`；误差只通过 A 线性传播，故可层类型无关地统一刻画。 |
| Method mechanism | 由恒等式推出闭式前向偏置 `β* = θ/(2T)`、膜电位累加解码替代计数解码、确定性两阶段时间误差扩散 `s[t] = round(t·n/T) − round((t−1)·n/T)`（`n = round(a/θ)`，Σs[t]=n 精确成立、条件方差 0）。视觉侧冻结 ViG 的 KNN 图并线性化 max-relative 聚合使其落入算子类；图侧用标准 GCN 消息传递；同一算子跨两类骨干，在统一协议下与全套主流 ANN2SNN 方法比较 conversion loss。 |
| Expected evidence | 统一协议 conversion loss 横评（CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS、Planetoid 三图）、恒等式数值残差验证、s[t] 零方差验证、原版 ViG（动态 KNN + max 非线性）失效边界实验。 |
| Limitation（用户已自认） | 原版 ViG 的 max 非线性与动态 KNN 图会破坏"线性 + 固定算子"假设；必须显式写适用条件并把原版 ViG 作为失效边界实验。视觉侧尚无任何正式实验。 |
| 内部先验（隔离标注） | 图节点分类 T≤8 达到 ANN−1.5pp 带内 —— 「用户提供的未公开先验（未发表、不充当公开证据）」，不进入 evidence / 打分依据。 |

---

## Closest prior art table:

按 `strict-idea-review.md` 的 closest-work 字段逐条列出，共 8 条（达到 3–8 要求上限）。**Link/source 统一说明**：以下 venue/year 与"已做的事"均来自**用户提供的独立文献核验结论**，本会话未执行公开检索、未附 URL/DOI，不编造链接；依 `privacy-and-evidence.md` 不将未发表 idea 文本用于查询。

**1**
- Closest work: Deng & Gu
- Venue/year: ICLR 2021
- Link/source: 用户提供的已核验 prior-art 结论（本轮未检索 URL/DOI）
- What it already does: `β* = θ/(2T)` 与逐层误差递归。
- Overlap with user idea: 直接占用 OAC 声称"由恒等式推出"的闭式前向偏置与逐层误差传播形式。
- Remaining novelty delta: 仅剩"把逐层递归写成固定线性矩阵 A 的算子级记号"，属表述层推广。
- Risk to the idea: fatal
- Needed differentiation: 需证明一般 A（行和≠1）下 β* 有不同形式或更优闭式，否则该组件不可声称新。

**2**
- Closest work: QCFS
- Venue/year: ICLR 2022
- Link/source: 同上
- What it already does: 零期望误差偏置。
- Overlap with user idea: 占用 `β*` 的统计最优性/零均值论证。
- Remaining novelty delta: 无独立 delta；仅适用算子类不同。
- Risk to the idea: high
- Needed differentiation: 需给出 QCFS 在一般 A 上失效而 OAC 成立的可测反例。

**3**
- Closest work: FTBC
- Venue/year: ECCV 2024
- Link/source: 同上
- What it already does: 零期望误差偏置（较新版本）。
- Overlap with user idea: 同上，且为视觉侧近年基线。
- Remaining novelty delta: 无独立 delta。
- Risk to the idea: high
- Needed differentiation: 统一协议下需把 FTBC 作为必比基线，而非仅列在 related work。

**4**
- Closest work: Dual-Phase
- Venue/year: IEEE TNNLS 2024
- Link/source: 同上
- What it already does: 膜电位累加解码替代计数读出 + 精确误差等式。
- Overlap with user idea: 同时占用 OAC 的两个核心组件（替代解码 + 精确误差恒等式）。
- Remaining novelty delta: 仅剩"把精确等式推广到抽象 A"，需证明该推广非平凡。
- Risk to the idea: fatal
- Needed differentiation: 需给出 Dual-Phase 等式无法覆盖、而 `A(E₁W₂)` 能覆盖的具体算子类并给出新推论。

**5**
- Closest work: PASCAL
- Venue/year: TMLR 2025
- Link/source: 同上
- What it already does: 确定性精确计数。
- Overlap with user idea: 直接占用 OAC 的 ②（确定性化、Σs[t]=n、零 RNG）的核心思想。
- Remaining novelty delta: 仅剩"把确定性计数放进 TPP 第二相"这一组合动作，以及累计取整的具体写法。
- Risk to the idea: fatal
- Needed differentiation: 必须在统一协议下直接对比 PASCAL，显示 OAC 在低 T / latency / energy 上有可归因增益；用户注明 PASCAL 无官方代码，需自行复现。

**6**
- Closest work: TPP（含 SpikeConverter, AAAI 2022 的两阶段脉络）
- Venue/year: ICML 2025（SpikeConverter: AAAI 2022）
- Link/source: 同上
- What it already does: 两阶段转换框架。
- Overlap with user idea: 占用 OAC 的"确定性两阶段时间误差扩散"框架归属。
- Remaining novelty delta: 仅剩"第二相的特定确定性化（零条件方差、无 RNG）"。
- Risk to the idea: fatal
- Needed differentiation: 需证明该确定性化带来 TPP 随机第二相无法达到的性质（零条件方差下的可复现性 / 低 T 精度），并排除其只是 PASCAL 计数的移植。

**7**
- Closest work: One-Spike SNN
- Venue/year: IEEE TETC 2024/2025
- Link/source: 同上
- What it already does: 跨 CNN + GCN 的 ANN→SNN 转换。
- Overlap with user idea: 占用"同一转换思路跨视觉与图骨干"的先例，削弱 ③ 中"跨两类骨干统一"的新颖性。
- Remaining novelty delta: 仅剩"用同一个被显式抽象的算子 A + 统一协议横评"，以及"首次 ViG（而非 CNN）脉冲化"。
- Risk to the idea: high
- Needed differentiation: 需说明相对 One-Spike SNN，算子级误差刻画与统一协议横评提供了什么其没有的结论。

**8**
- Closest work: Parallel Conversion / DCGS / AdaFire（横评对手集合）
- Venue/year: ICML 2025 / ICML 2025 / AAAI 2025
- Link/source: 同上
- What it already does: 2025 年主流 ANN2SNN 转换方法，均有官方代码可重跑（用户提供）。
- Overlap with user idea: 构成 OAC "统一协议横评"必须对齐的基线集合，且代表该子领域 2025 年的饱和度。
- Remaining novelty delta: 无（它们是横评对象，不是被超越对象）；风险在于横评是否显示 OAC 增益。
- Risk to the idea: medium
- Needed differentiation: 统一协议必须含同骨干、同 T、同 θ、同 calibration 数据，否则横评不可比。

**其他纳入但非最近邻的锚点（用户提供）**：CS-QCFS、ECL（无代码需自行复现）；CIFAR10-DVS、Planetoid 三图、Tiny-ImageNet 等数据集约束；上文"baseline 现状"整段。均按用户提供事实记录，不扩展、不编造。

---

## Novelty delta:

**状态**：`searched`（依据用户提供的独立文献核验结论；边界见 Search basis 字段）。**结论**：在给定核验覆盖内，重叠为**高**，novelty 判定为低而非未知。

减去最近邻工作后，三处"真空白"逐条复核：

| 声称的真空白 | 复核结论 | 判定 |
| --- | --- | --- |
| ① 固定线性传播算子的算子级精确统一（层类型无关） | Deng & Gu 已有逐层误差递归、Dual-Phase 已有精确误差等式、One-Spike SNN 已跨 CNN+GCN。当 A 被限制为固定线性矩阵时，`B̂₂ − B₂ = A(E₁W₂)` 是把已知逐层传播写成矩阵记号；误差源 E₁ 未变，A 未引入新误差机制。 | **伪 delta（表述层重述）**，除非证明该统一带来 prior-art 无法得到的新误差界 / 新校准律 / 新可覆盖算子类。 |
| ② TPP 第二相的特定确定性化（零条件方差、无 RNG） | PASCAL 已做确定性精确计数，TPP 已有两阶段。`s[t] = round(t·n/T) − round((t−1)·n/T)` 为累计取整（均匀分配）；Σs[t]=n 由 telescoping 平凡成立，"条件方差 0"是"确定性"的同义反复。 | **组合 delta**，相对 PASCAL + TPP 不产生新数学性质；仅当带来可测的系统级增益（低 T 精度 / 可复现性 / 能耗）才成立。 |
| ③ 首次 ViG 脉冲化 + 同一算子跨视觉骨干与图消息传递的统一协议横评 | 属实证 / benchmark 贡献，本身新且可测；但"首次把 X 脉冲化 + 横评"在 CCF-A 主会通常读作增量应用或 benchmark 工程，除非伴随非平凡洞察。且 One-Spike SNN 已跨 CNN+GCN。 | **真实但增量**，且当前零正式实验支撑。 |

**明确不可声称的内容（用户硬要求）**：不得声称发明 `β* = θ/(2T)`、逐层误差递归、零期望误差偏置、膜电位累加解码替代计数、精确误差等式、确定性精确计数、两阶段框架、跨 CNN+GCN 转换。这些均归用户提供核验的 prior-art。

**最强 novelty delta 的诚实表述**：在显式写出"仅适用固定、非负、线性传播算子"的前提下，本 idea 剩下的可辩护贡献是"对该算子类给出层类型无关的统一误差表述，并在统一协议下做 ViG / GCN 两类骨干的 conversion loss 横评与失效边界分析"——这是一个**窄、增量、以协议与边界分析为主**的贡献，而非新数学组件。

---

## Serious blockers:

**Fatal risks（对当前 formulation；不能靠"补实验"解决，必须改主张 / 改方法 / 改证据结构）**

- **F1 · 主张—适用条件错位（problem-method bait-and-switch）**：中央科学问题点名"非网格、数据依赖的邻域聚合"（ViG 动态 KNN、ViT attention、GNN 消息传递）；方法为取得统一，把 A 限制为固定、非负、线性，并在视觉侧**冻结 KNN 图 + 线性化 max-relative**。一旦按用户要求"显式写适用条件"，方法覆盖的是被削成固定线性代理的骨干，而非原问题中最难、对社区最有价值的部分。审稿人会判定"用限制假设规避了所声称要解决的难点"。修复需改变中心主张或扩展算子类，非补实验可解。
- **F2 · Novelty 坍缩到重述 / 组合**：见 Novelty delta 字段。`A(E₁W₂)` 是已知逐层递归 + 精确等式的矩阵记号；确定性 s[t] 是 PASCAL 计数 + TPP 框架的组合；Σs[t]=n 与零条件方差是确定性计数的平凡性质。依 `calibration.md` fatal gate「No identifiable insight beyond applying known modules」与「Novelty <= 2 with high confidence」，推荐封顶于 `pivot-with-rescue-route`。
- **F3 · 横评可比性两难（贡献自洽性）**：OAC 在冻结/线性化骨干上评估，而 QCFS / FTBC / TPP / Parallel Conversion / DCGS / AdaFire 为原始算子设计。若基线跑原始骨干、OAC 跑修改骨干，则 conversion loss 横评不可比；若全部移到同一修改骨干，则 OAC 相对这些数学同源方法的增益来源不明。两难不解决，横评这一核心证据无法支撑结论；且 PASCAL（② 的最近邻）与 TPP（② 的框架来源）无官方代码需自行复现，恰是最决定性、当前最缺的比较。

**Fixable weaknesses（可修复，不改变中心主张）**

- W1 视觉侧零正式实验（用户明述）→ 补统一协议下的完整视觉侧实验。
- W2 PASCAL / CS-QCFS / ECL 无官方代码 → 自行复现并纳入横评，尤其 PASCAL 与 TPP。
- W3 β* 对一般 A（行和≠1）的推导、‖A‖ 放大的误差界、两种解码的兼容性命题尚未给出 → 理论补强。
- W4 原版 ViG（动态 KNN + max 非线性）失效边界尚未定量报告 → 用户已计划，属可执行。
- W5 ImageNet-1K 不可得（G2 不可用）→ 通过 venue 定位或等价规模证据处理。
- W6 统一协议细节（同骨干 / 同 T / 同 θ / 同 calibration 数据 / 同 conversion loss 定义）尚未写成正式 protocol。
- W7 组件冗余（膜电位累加解码 vs 确定性计数是否重复）未消融。

**隔离项**：图节点分类 T≤8 ANN−1.5pp 带内为「用户提供的未公开先验（未发表、不充当公开证据）」，既非 fatal 也非 weakness 证据，不参与判定。

---

## Per-expert reviewer notes:

> 以下五个角色**独立**给出判断，先各自发言、后综合（依 `expert-panel.md` 与 `review-output-standards.md` 的 panel 纪律）。每个角色的 **Score tendency（分数倾向）与 Confidence（置信度）分开报**，不强行制造一致、赞扬或拒稿。全部内容为本红队 panel 的独立判断，非真实审稿记录。

**Field Expert**
- Role: 领域专家（类脑计算 × 视觉表征 / ANN2SNN 转换）
- Score tendency: 3 / 5（问题重要性偏中）
- Best possible argument for the idea: 把误差分析从"逐元素算子"提升到"传播算子"层级，对同时做视觉图网络与 GNN 的社区确实提供了一个可复用的表述与横评平台；ViG 脉冲化本身是该子领域尚未被覆盖的设置。
- Strict rejection-grade concern: 写完 related work 段落后，"现有方法各自校准自己的算子、缺少统一刻画"这一 gap 是否还成立？Deng & Gu 已有逐层递归、Dual-Phase 已有精确等式、One-Spike SNN 已跨 CNN+GCN；若 gap 只剩"没人做过统一协议横评"，那是 benchmark 缺口而非科学瓶颈，CCF-A 主会不会把"缺横评"当主贡献。
- Anchor: 用户提供的 prior-art 核验结论（Deng & Gu ICLR 2021；Dual-Phase TNNLS 2024；One-Spike SNN TETC 2024/2025）＋ idea 的 gap 陈述。
- Why this matters: 领域是否从本文学到超出局部改进的东西，取决于 gap 是理论性的还是工程性的。
- Fatal risk if any: 与 F1 部分重叠——问题的重要性被方法适用条件收缩后无法兑现。
- Most valuable repair or pivot: 给出"逐算子校准确实导致可测量 conversion loss 不一致"的前提证据，并把问题重述为理论瓶颈（为何误差需在算子级而非层类型级统一）。
- Development-potential note: 中；问题重述可提升主轴，但不消除 F2。
- Confidence: 4 / 5（gap 性质判断基于用户提供的核验清单，覆盖边界明确）

**Method Expert**
- Role: 方法专家（误差分析 / 机制正确性）
- Score tendency: 2 / 5
- Best possible argument for the idea: 在固定线性 A 假设下 `B̂₂ − B₂ = A(E₁W₂)` 代数上自洽，E₁ 经 A 线性传播这一观察确实给出了层类型无关的统一写法；确定性 s[t] 保证 Σs[t]=n，消除随机发放带来的实现噪声。
- Strict rejection-grade concern: 三处未闭合：(a) `β* = θ/(2T)` 的零期望 / 最优性推导在 A 行和≠1 时（GCN 度归一化、ViG 聚合权重）是否仍成立？用户未提供一般 A 的推导；(b) A 非负**不**控制误差放大，‖A‖>1 时 E₁ 经 A 的跨层累积界缺失；(c) "膜电位累加解码替代计数解码"与"Σs[t]=n 的确定性计数"是否只是同一机制的两种实现，替代收益未界定。另存在组件目标冲突：冻结 KNN 图以保线性 vs ViG 的数据依赖表征能力（原卖点）。
- Anchor: 缺失机制（一般 A 下 β* 推导、‖A‖ 误差界、解码兼容性命题）；idea 的 A 定义与"冻结/线性化"处理。此处为"未给出"而非"断言其错误"。
- Why this matters: 触发 fatal gate「Method soundness <= 2」与「Internal mechanism conflict」，二者均封顶推荐。
- Fatal risk if any: F1（组件目标冲突）＋ 若一般 A 下 β* 不成立，闭式偏置这一支柱失效。
- Most valuable repair or pivot: 补 (i) 一般 A 下 β* 推导或反例条件、(ii) ‖A‖ 相关误差上界并数值验证、(iii) 两解码等价性/差异命题、(iv) 冻结/线性化相对原版 ViG 的性能代价量化；删除被证明冗余的组件。
- Development-potential note: 中—高；这是三条 fatal 中最可修复的一条。
- Confidence: 3 / 5（部分判断基于对未给出推导的推断，可检验证据不足）

**Experiment Expert**
- Role: 实验专家（证据设计 / 基线 / 可行性）
- Score tendency: 2 / 5
- Best possible argument for the idea: 统一协议 conversion loss 横评 + 恒等式浮点残差 + s[t] 零方差 + 失效边界，证据设计意图完整；数据（CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS、Planetoid）与算力（3060 + 已授权 4090）可支撑执行，多数基线有官方代码。
- Strict rejection-grade concern: 视觉侧**尚无任何正式实验**，中心新颖主张（首次 ViG 脉冲化 + 统一横评）零实证；**单一最致命缺失比较**是与 PASCAL（确定性精确计数）和 TPP（两阶段）在同一协议下的直接对比——OAC 的 ②③ 恰是这两者组合，缺此对比则 novelty delta 不可判定；且 PASCAL / CS-QCFS / ECL 无代码需自行复现。另有可比性未定义（基线原始骨干 vs OAC 修改骨干）、原版 ViG 失效边界未定量、CVPR/ICCV 档缺 ImageNet-1K。
- Anchor: 用户明述"本次视觉侧尚无任何正式实验"＋ 基线代码现状＋ 数据集/硬件约束（均用户提供）。
- Why this matters: 触发 fatal gate「Experimental convincibility <= 2」；这是"缺一个比较就拒稿"的典型，且阴性结果（横评显示与 PASCAL/TPP 等价）会反噬 F2。
- Fatal risk if any: F3（可比性两难）。
- Most valuable repair or pivot: 先固定统一 protocol（同骨干、同 T、同 θ、同 calibration 数据、同 conversion loss 定义），再补全套基线含 PASCAL / TPP 自行复现；报告 conversion loss–T 曲线、恒等式残差、零方差验证、原版 ViG 失效边界量化。
- Development-potential note: 高；这是最明确、最可执行的补齐路径。
- Confidence: 5 / 5（视觉侧零实验与基线代码状态由用户明确给出）

**AC / Venue Expert**
- Role: AC / venue 专家（贡献品味 / 匹配 / 讨论后存活）
- Score tendency: 3 / 5
- Best possible argument for the idea: 误差理论 + 转换方法 + 视觉 + 图 + 横评的组合对 IEEE TNNLS 档（类脑理论 + 允许较小数据集 + 篇幅容纳横评）是自洽的；统一协议横评对社区有实用价值。
- Strict rejection-grade concern: 贡献为拼盘（等式重述 + 确定性技巧 + 首次脉冲化 + 横评），缺单一深主轴。CVPR/ICCV 主会在无 ImageNet-1K 的情况下会读成小规模增量 SNN 应用；NeurIPS 会嫌理论不新（组件大半已占）；"统一协议横评"是 benchmark 味，可能被判为 benchmark/工作坊级或 track 不匹配；混合评审后能否 survive discussion 存疑。desk-reject 风险主要来自主轴不清而非格式。
- Anchor: 用户指定目标档位＋数据集约束＋ prior-art 的 venue 分布（TNNLS/TMLR/ICML/AAAI/TETC）。注：未核验各会当年官方 policy / review form，按通用 contribution taste 推理。
- Why this matters: venue mismatch 是混合评审后无法存活的高频原因；venue fit <= 2 会触发 venue-switch gate。
- Fatal risk if any: 无独立 fatal；但主轴不清会放大 F2。
- Most valuable repair or pivot: 明确主投 TNNLS 档并把贡献主轴收敛为"算子类上的统一误差理论 + 统一协议横评 + 失效边界"；若坚持 CVPR/ICCV，需补 ImageNet-1K 或等价规模证据并证明视觉侧增益。
- Development-potential note: 中。
- Confidence: 3 / 5（官方当年政策未核验，依据贡献品味推理）

**Skeptical Prior-Art Expert**
- Role: 怀疑型 prior-art 专家（novelty 坍塌 / 命名掩盖 / 是否已属已知）
- Score tendency: 2 / 5
- Best possible argument for the idea: 用户已主动完成独立文献核验并如实承认"数学组件大半已被占"，且明确把真空白收窄到三处——这种自我约束本身降低了被当场 scoop 的风险；三处中 ③（首次 ViG 脉冲化）在给定核验覆盖内确实未见先例。
- Strict rejection-grade concern: 最强"this is already known" objection：`B̂₂ − B₂ = A(E₁W₂)` 可直读为 Deng & Gu 逐层递归 + Dual-Phase 精确等式的矩阵重述；`s[t] = round(t·n/T) − round((t−1)·n/T)` 是累计取整 / 均匀分配，Σs[t]=n 是 telescoping 平凡恒等式，"零条件方差"只是确定性的同义反复；"Operator-Agnostic（算子无关）"这一命名掩盖了"仅适用固定、非负、线性算子"的强假设。三处 delta 在减去最近邻后不构成新数学结果或新能力。
- Anchor: 用户提供的独立核验结论全表（见 Closest prior art table）＋ idea 中 A 的定义与命名。
- Why this matters: 决定 novelty 是否 <= 2（fatal gate）与是否「beyond applying known modules」（fatal gate）。
- Fatal risk if any: F2。
- Most valuable repair or pivot: 要么扩展算子类到至少一类数据依赖 / 非线性算子（哪怕弱形式）并给出新推论，要么把 novelty 主张降级为"统一协议与横评 + 失效边界"并接受增量定位；同时删除任何"发明数学组件"的措辞。用户已要求后者的一半，需落实为全文一致。
- Development-potential note: 低—中。
- Confidence: 5 / 5（重叠结论由用户明确核验给出，覆盖边界清楚）

**Panel Synthesis**（依 `expert-panel.md` 与 `review-output-standards.md`，不平均掉 fatal）

```text
Agreement: 五位专家一致认为 F1（主张-适用条件错位）与 F2（novelty 重述/组合）成立，且视觉侧零实验使任何正向判断都缺乏实证支撑；一致认为不应 abandon，因中心主张可测且有可命名修复路线。
Disagreement: Field 与 AC 对"问题重要性 / venue 落点"给出 3 分（认为收敛到 TNNLS 档后仍有价值）；Method、Experiment、Skeptical 给出 2 分（认为机制未闭合、证据空缺、novelty 坍塌）。分歧来自"评当前就绪度"还是"评收敛后的潜力"，不是对事实的分歧。
Strongest accept axis / Decisive accept axis: 统一协议横评 + 失效边界分析对类脑/SNN 社区有可复用价值，且 ViG 脉冲化在给定核验覆盖内确属未覆盖设置；若横评显示可归因于算子级统一的稳定增益，主张可重新站住。
Strongest reject axis / Decisive reject axis: 在"固定线性 A"下，恒等式只是已知结论的矩阵重述，确定性 s[t] 只是 PASCAL+TPP 的组合，而"算子无关"的命名掩盖了适用条件的收缩；写完 related work 后贡献所剩无几。
Score-relevant uncertainty / Unresolved evidence: β* 对一般 A 是否成立（Method conf 3/5）；官方当年 venue policy 未核验（AC conf 3/5）；本会话未重新公开检索，prior-art 覆盖以用户核验清单为界。
Most valuable next evidence: 同一修改骨干、同 T / θ / calibration 数据下，含 PASCAL 与 TPP 自行复现的全套 conversion loss 横评；以及一般 A 下 β* 的推导。
Final calibrated stance / Panel-calibrated recommendation: pivot-with-rescue-route（与单独打分和 fatal gates 一致）。
```

---

## Rubric scores:

权重取 `rubric.md` 默认表（合计 100），未作调整（无官方 venue review form 要求调整）。

| Dimension | Weight | Score (1-5) | Confidence (1-5) | Deduction / evidence basis | Repair condition |
| --- | ---: | ---: | ---: | --- | --- |
| Problem importance | 12 | 3 | 4 | gap 中"逐算子校准导致可测量损失"前提未证实；"缺横评"属工程缺口；适用条件收缩使问题重要性无法兑现 | 给出跨两类骨干的"校准不一致"实测前提，并把问题重述为理论瓶颈 |
| Novelty against likely prior work | 14 | 2 | 5 | 用户核验结论显示数学组件大半已占，剩余 delta 为重述/组合/增量应用 | 扩展算子类至至少一类数据依赖算子并给出新推论，否则接受增量定位 |
| Conceptual innovation | 12 | 2 | 4 | A 为固定线性矩阵是标准视角；"算子无关"命名掩盖强假设；属模块组合 | 提出仅当 A 显式抽象才出现的新概念（如 ‖A‖–β*–T 闭式关系）并解释新现象 |
| Method soundness | 14 | 2 | 3 | 一般 A 下 β* 推导、‖A‖ 误差界、两解码兼容性未给出；冻结 KNN 与 ViG 表征能力目标冲突 | 补四项机制命题 / 推导 / 数值验证，删除冗余组件 |
| Elegance and simplicity | 8 | 3 | 4 | 简洁性来自排除难点而非解决难点；组件必要性未消融 | 消融证明每组件独立不可替代，删冗余 |
| Feasibility under resources | 8 | 4 | 4 | 数据/算力/多数基线代码齐备（用户提供）；仅 ImageNet-1K 不可得、ViG-SNN 需自实现、3 个基线需复现 | 确认 3060/4090 上 ViG-SNN 与全套基线可跑通；以 TNNLS 档规避 ImageNet 硬要求 |
| Experimental convincibility | 10 | 2 | 5 | 视觉侧零正式实验；缺 PASCAL / TPP 同协议直接对比；可比性未定义；失效边界未定量 | 固定统一 protocol，补齐全套基线含自行复现，报告曲线/残差/零方差/失效边界 |
| Venue and audience fit | 8 | 3 | 3 | 贡献拼盘缺深主轴；CVPR/ICCV 缺 ImageNet；NeurIPS 嫌理论不新；横评偏 benchmark 味 | 明确主投 TNNLS 档并收敛主轴；或补 ImageNet-1K 级证据 |
| Timeliness and topic heat | 6 | 3 | 4 | 方向热但 2024/2025 prior-art 密集，饱和与 scoop 风险高 | 把"为什么是现在"绑定到 ViG 表征进展给出的新必要性，否则接受拥挤子领域增量定位 |
| Risk-adjusted acceptance potential | 8 | 2 | 4 | 三条 fatal 叠加 + 视觉侧零实验；多条 fatal gate 同时封顶 | 先解 F1、F3 再补视觉侧实验；三者任一未解不升档 |

### 每个 ≤3 分项的扣分明细（依 `rubric.md` Deduction Format 与 `review-output-standards.md` 定量反馈；用户硬要求四项齐全）

**Problem importance（Score 3 / Confidence 4）**
- 扣分理由：gap 的真实性依赖"逐算子校准确实造成可测量 conversion loss 缺口"这一未证实前提；"缺统一协议横评"是工程/基准缺口而非理论瓶颈；更关键的是方法把适用类收缩到固定线性算子，恰把问题中最难、最有价值的数据依赖/动态/非线性邻域聚合排除，问题的重要性无法被方法兑现。
- 证据基础 / Anchor：idea 的中央科学问题段与适用条件；用户提供核验的 One-Spike SNN（已跨 CNN+GCN）、Dual-Phase（已有精确误差等式）。
- 为什么重要：CCF-A 主会要求瓶颈"重要且被本文真正解决"；写完 related work 后若 gap 只剩"没人做过统一横评"，会被判为 benchmark gap。
- 修复条件：给出跨两类骨干的"现有逐算子校准方法在统一协议下 conversion loss 显著不一致/次优"的实测前提，并把中心问题重述为"为何误差需在算子级而非层类型级统一"。
- 预期分数变化：条件性 3→4，Overall 约 +0.1；不承诺（依 `privacy-and-evidence.md` 仅作条件性表述）。
- Development-potential effect：中；提升主轴清晰度，不消除 F2。

**Novelty against likely prior work（Score 2 / Confidence 5）**
- 扣分理由：用户核验结论显示 β*=θ/(2T)、逐层递归、零期望偏置、膜电位累加解码、精确误差等式、确定性精确计数、两阶段框架、跨 CNN+GCN 均已被占；三处剩余 delta 在减去最近邻后不构成新数学结果或新能力，主要是矩阵记号重述 + 已知模块组合 + 新数据集应用。
- 证据基础 / Anchor：用户提供的独立核验结论全表（Closest prior art table 8 条）；`calibration.md` fatal gate「No identifiable insight beyond applying known modules」「Novelty <= 2 with high confidence」。
- 为什么重要：`rubric.md` 5 分 anchor 要求 closest-work 比较后仍有 meaningful novelty delta；此处 delta 为伪/组合/增量。
- 修复条件：证明 `A(E₁W₂)` 在"固定+非负+线性"之外还能覆盖至少一类数据依赖或非线性算子（哪怕弱形式），或给出该统一带来的、prior-art 无法得到的新误差界 / 新校准律；否则把 novelty 主张降级为"统一协议与横评 + 失效边界"并接受增量定位。
- 预期分数变化：条件性 2→3（仅当算子类扩展被验证），Overall 约 +0.0~+0.15；若只补实验不改主张，维持 2；不承诺。
- Development-potential effect：低—中；fatal gate 触发项。

**Conceptual innovation（Score 2 / Confidence 4）**
- 扣分理由：把传播算子记为固定非负线性矩阵 A 是图信号处理 / 数值线性代数的标准视角；"Operator-Agnostic"命名掩盖"仅适用固定线性算子"的强假设，概念上的简洁来自排除难点而非提出新机制。
- 证据基础 / Anchor：idea 中 A 的定义（固定、非负、线性）＋ 视觉侧"冻结 KNN 图 / 线性化 max-relative"处理；`rubric.md`「penalize pure module recombination unless the combination creates a new capability or explanation」。
- 为什么重要：若组合不产生新能力或新解释，概念创新不成立，方法读成工程实现细节。
- 修复条件：提出一个只有当 A 被显式抽象时才会出现的新概念（例如算子谱范数 ‖A‖ 与最优偏置 β*、时间步 T 之间的闭式关系，或跨视觉/图的统一误差相图），并用它解释至少一个现有方法无法解释的现象。
- 预期分数变化：条件性 2→3，Overall 约 +0.1；不承诺。
- Development-potential effect：中。

**Method soundness（Score 2 / Confidence 3）**
- 扣分理由：三处机制疑问未闭合——(a) β*=θ/(2T) 的零期望/最优性推导在 A 行和≠1（GCN 度归一化、ViG 聚合权重）时是否成立未给出；(b) A 非负不控制误差放大，‖A‖>1 时 E₁ 经 A 的跨层累积界缺失；(c) "膜电位累加解码替代计数解码"与"Σs[t]=n 的确定性计数"可能只是同一机制的两种实现，替代收益未界定。另有组件目标冲突：冻结 KNN 图保线性 vs ViG 数据依赖表征能力。
- 证据基础 / Anchor：idea 给出的恒等式与组件清单；β* 对一般 A 的推导、误差界、兼容性证明均属**缺失机制**（非断言其错误）；`calibration.md` fatal gate「Method soundness <= 2」「Internal mechanism conflict」。
- 为什么重要：两条 fatal gate 同时把推荐封顶于 `pivot-with-rescue-route`。
- 修复条件：给出 (i) 一般 A 下 β* 的推导或反例条件、(ii) ‖A‖ 相关误差上界并数值验证、(iii) 两解码等价性/差异命题、(iv) 冻结/线性化相对原版 ViG 的性能代价量化。
- 预期分数变化：条件性 2→3，Overall 约 +0.15；若发现 β* 在一般 A 下不成立且不可修，降至 1 并触发 venue/pivot 重判；不承诺。
- Development-potential effect：中—高；三条 fatal 中最可修复的一条。

**Elegance and simplicity（Score 3 / Confidence 4）**
- 扣分理由：归约到单一矩阵 A 确实简洁，但简洁性来自把 ViG/ViT/GNN 的难点（动态图、softmax、max 非线性）冻结/线性化后排除；组件必要性未论证，尤其"膜电位累加解码"与"确定性 s[t]"是否冗余未消融。
- 证据基础 / Anchor：idea 组件清单；用户核验的 Dual-Phase（已含膜电位读出）与 PASCAL（已含确定性计数）。
- 为什么重要：`rubric.md` elegance 要求 necessary parts and coherent insight；冗余组件会被核减为实现细节。
- 修复条件：消融证明每个组件对 conversion loss / 方差 / latency 有独立且不可替代的贡献，删去被证明冗余的组件。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；不承诺。
- Development-potential effect：低—中。

**Experimental convincibility（Score 2 / Confidence 5）**
- 扣分理由：视觉侧尚无任何正式实验（用户明述），中心新颖主张（首次 ViG 脉冲化 + 统一协议横评）零实证支撑；最致命缺失比较是与 PASCAL（确定性精确计数）和 TPP（两阶段）在同一协议下的直接对比——OAC 的 ②③ 恰是这两者组合，缺此对比 delta 不可判定；基线在原始骨干 vs OAC 在冻结/线性化骨干的可比性未定义；原版 ViG（动态 KNN + max）失效边界尚未定量报告。
- 证据基础 / Anchor：用户明述"本次视觉侧尚无任何正式实验"＋ 基线代码现状（PASCAL/CS-QCFS/ECL 无代码需自行复现）＋ 数据集/硬件约束；`calibration.md` fatal gate「Experimental convincibility <= 2」。
- 为什么重要：这是"缺一个比较就拒稿"的典型；阴性结果（横评显示与 PASCAL/TPP 等价）会反噬 F2。
- 修复条件：统一协议（同骨干、同 T、同 θ、同 calibration 数据、同 conversion loss 定义）下补齐全套基线含 PASCAL 与 TPP 自行复现；报告 conversion loss–T 曲线、恒等式浮点残差、s[t] 零方差验证、原版 ViG 失效边界量化。
- 预期分数变化：条件性 2→4（若横评显示可归因于统一算子的稳定增益），Overall 约 +0.2；若横评显示与 PASCAL/TPP 等价，维持 2 并坐实 F2；不承诺。
- Development-potential effect：高；最明确的补齐路径。

**Venue and audience fit（Score 3 / Confidence 3）**
- 扣分理由：贡献为拼盘（误差恒等式重述 + 确定性技巧 + 首次脉冲化 + 横评），缺单一深主轴；CVPR/ICCV 主会缺 ImageNet-1K（用户注明需申请、G2 不可用）易读成小规模增量 SNN 应用；NeurIPS 会嫌理论不新；"统一协议横评"是 benchmark 味，可能被判为 benchmark/工作坊级或 track 不匹配。IEEE TNNLS 档（类脑 + 理论 + 容较小数据集 + 篇幅容纳横评）是更自洽落点。
- 证据基础 / Anchor：用户指定目标档位＋数据集约束＋ prior-art venue 分布；注：本评审未核验各会官方当年 policy / review form，按通用 contribution taste 推理。
- 为什么重要：venue mismatch 是 desk-reject / 混合评审后无法 survive discussion 的高频原因。
- 修复条件：明确主投 TNNLS 档并把贡献主轴收敛为"算子类上的统一误差理论 + 统一协议横评 + 失效边界"；若坚持 CVPR/ICCV，需补 ImageNet-1K 或等价规模证据并证明视觉侧增益。
- 预期分数变化：条件性 3→4（venue 明确化 + 主轴收敛后），Overall 约 +0.08；不承诺。
- Development-potential effect：中。

**Timeliness and topic heat（Score 3 / Confidence 4）**
- 扣分理由：方向热但饱和风险高；用户列出的强相关 prior-art 中 2024/2025 年密集（FTBC ECCV'24、Dual-Phase TNNLS'24、PASCAL TMLR'25、TPP ICML'25、Parallel Conversion ICML'25、DCGS ICML'25、AdaFire AAAI'25、One-Spike SNN TETC'24/25），一年内多篇占据误差分析/偏置/两阶段/确定性计数/跨骨干，"再次统一"易被读成 survey/benchmark 而非新洞察。
- 证据基础 / Anchor：用户提供的 prior-art 年份与 venue 列表；`rubric.md` timeliness 的 "risk of saturation"。
- 为什么重要：密集 prior art 提高 novelty 坍塌与 scoop 风险。
- 修复条件：把"为什么是现在"绑定到 ViG/视觉图网络在 2024–2025 的表征进展，并给出该进展使"固定线性代理算子"成为必要的新证据；否则接受"拥挤子领域中的增量"定位。
- 预期分数变化：条件性 3→4，Overall 约 +0.06；不承诺。
- Development-potential effect：低。

**Risk-adjusted acceptance potential（Score 2 / Confidence 4）**
- 扣分理由：三条 fatal risk（F1 主张-适用条件错位、F2 novelty 重述/组合、F3 横评可比性两难）叠加视觉侧零实验；任一未解都足以在 CCF-A 主会档触发拒稿；`calibration.md` 多条 fatal gate 同时封顶。
- 证据基础 / Anchor：本报告 Serious blockers＋fatal gates（novelty≤2、method≤2、experimental≤2、insight-beyond-modules、internal conflict）。
- 为什么重要：该维度是"考虑 fatal risk 与评审分歧后的分数"，反映叠加效应而非重复计罚。
- 修复条件：先解决 F1（主张改写/算子类扩展）与 F3（统一骨干 + PASCAL/TPP 复现），再补齐视觉侧实验；三者任一未解不升档。
- 预期分数变化：条件性 2→3（三条 fatal 转可修复弱点后），Overall 约 +0.1；若 F2 被横评证实为"与 PASCAL/TPP 等价"，维持 2 或降 1；不承诺。
- Development-potential effect：中（依赖 fatal 是否可解）。

> Feasibility under resources 为 4 分（>3），不触发明细块要求；其扣分/修复条件已在上方表格给出：数据、算力、多数基线代码齐备是加分基础，扣分来自 ImageNet-1K 不可得、ViG-SNN 需自实现、3 个基线需自行复现、官方当年 venue policy 未核验。

---

## Weighted final score:

依 `rubric.md` / `calibration.md`：`weighted_score = sum(score_i × weight_i) / 100`

```text
12×3 = 36
14×2 = 28
12×2 = 24
14×2 = 28
 8×3 = 24
 8×4 = 32
10×2 = 20
 8×3 = 24
 6×3 = 18
 8×2 = 16
合计 = 250 → 250 / 100 = 2.5
```

**Overall:** 2.5（1–5 加权尺度，X 保留一位小数；可选 1–10 尺度 = 2.5 × 2 = 5.0）

```text
Current conference readiness: low
Development potential: medium
```

分数与推荐的一致性说明：2.5 落在 `calibration.md` 的「1.0–2.9 high-risk reformulate by default」段，但用户硬要求推荐值限定为 5 选 1，且多条 fatal gate（novelty≤2 高置信、method≤2、experimental≤2、beyond-modules、internal conflict）均把推荐封顶为 `pivot-with-rescue-route`；同时中心主张可测、存在可命名修复路线，不满足 `abandon` 条件，novelty 已按用户指令标 `searched` 故不取 `needs-literature-search`。因此取 `pivot-with-rescue-route`，含义为"保留最佳要素并改变问题 / 方法 / 证据 / venue"，与 2.5 分一致。

---

## Score-change conditions:

全部为**条件性、非承诺**（依 `privacy-and-evidence.md`，不保证分数变化 / 录用概率 / 审稿人行为）。按影响排序：

| 条件（可测） | 影响维度 | 预期分数变化（条件性区间） |
| --- | --- | --- |
| C1 把中心主张改写为"固定线性传播算子类上的算子级精确统一 + 该类算子上统一协议横评 + 失效边界"，并把冻结/线性化定位为"算子类成员"而非"ViG 脉冲化" | Problem / Conceptual / Acceptance | Problem 3→4、Conceptual 2→3、Acceptance 2→3；Overall 约 +0.2~+0.3 |
| C2 给出一般 A（行和≠1）下 β* 的推导或反例条件 + ‖A‖ 相关误差上界 + 两解码兼容性命题，并数值验证 | Method soundness | 2→3（若 β* 不成立且不可修则降至 1）；Overall 约 +0.15 |
| C3 固定统一 protocol（同骨干 / 同 T / 同 θ / 同 calibration 数据 / 同 conversion loss 定义），补齐含 PASCAL 与 TPP 自行复现的全套基线，报告 conversion loss–T 曲线、恒等式残差、s[t] 零方差、原版 ViG 失效边界 | Experimental convincibility | 2→4（若显示可归因于统一算子的稳定增益）；Overall 约 +0.2 |
| C4 横评显示 OAC 相对 PASCAL / TPP 在低 T 精度、可复现性或能耗上有可归因增益 | Novelty / Acceptance | Novelty 2→3、Acceptance 2→3；Overall 约 +0.15~+0.25 |
| C5 明确主投 TNNLS 档并收敛贡献主轴；或补 ImageNet-1K 级证据 | Venue fit | 3→4；Overall 约 +0.08 |
| C6 消融删除冗余组件（膜电位累加解码 vs 确定性计数） | Elegance | 3→4；Overall 约 +0.08 |
| C7 把"为什么是现在"绑定到 2024–2025 ViG 表征进展的必要性证据 | Timeliness | 3→4；Overall 约 +0.06 |

**反向条件（会坐实 fatal / 降分）**：若 C3 横评显示 OAC 与 PASCAL / TPP 在统一协议下等价 → F2 坐实，Novelty 维持 2 或降 1，Acceptance 降 1；若 C2 发现 β* 对一般 A 不成立且无替代闭式 → Method soundness 降 1；若坚持原中心主张「统一非网格数据依赖邻域聚合」而不写适用条件 → F1 保持 fatal，不接受任何升分。

**Fatal gates 生效清单**（`calibration.md`）：Novelty 2 / 高置信 → 封顶 pivot；Method soundness 2 → 封顶 pivot；Experimental convincibility 2 → 封顶 pivot；No identifiable insight beyond known modules → 封顶 pivot；Internal mechanism conflict → 封顶 pivot（至解决）。以上任一未解，推荐不得升为 `revise` 或 `accept-to-develop`。

---

## Confidence:

- **综合 Confidence：Medium**（依 `calibration.md` 标签）。
- 理由：close work 覆盖明确（用户提供独立核验结论，novelty 维度 conf 5/5）、视觉侧零实验这一事实明确（Experiment conf 5/5）；但 (i) 本会话未重新执行公开检索，prior-art 覆盖以用户核验清单为界；(ii) β* 对一般 A 的推导、两解码兼容性属未给出的机制，Method conf 仅 3/5；(iii) 各目标会议/期刊当年官方 policy / review form 未核验，AC conf 3/5；(iv) 视觉侧无任何正式实验，实验判断是"证据缺失"而非"结果已知"。
- **依公平规则**：不因 confidence 为 Medium 而下调 idea 分数；分数（2.5）与置信度（Medium）分开报；低置信度单独引导下一步检查（见 Optional next-module decision 与 Evidence that would change my score）。
- 各维度 Confidence 已在 Rubric scores 表逐维列出，分数与置信度不再此处重复。

---

## Strict reviewer comments:

> 依 `strict-idea-review.md` Harsh Reviewer Lens：短、诊断式、每条带 anchor，不作动机性缓冲。

1. **关于中心主张**（Anchor：idea 适用条件 + 用户自认硬风险）：论文声称解决"数据依赖邻域聚合"的误差统一，方法却要求 A 固定线性、并要求冻结 KNN 图与线性化 max-relative。显式写出适用条件后，方法覆盖的是被简化后的代理骨干；这不是统一了难点，而是把难点移出适用范围。请改写主张或给出覆盖数据依赖算子的机制。
2. **关于恒等式**（Anchor：Deng & Gu ICLR 2021、Dual-Phase TNNLS 2024，用户提供核验）：在固定线性 A 下 `B̂₂ − B₂ = A(E₁W₂)` 是已知逐层误差递归与精确误差等式的矩阵记号重述。请指出该写法带来哪一条 prior-art 无法得到的推论（新误差界、新校准律或新可覆盖算子类）；若没有，这属于表述而非贡献。
3. **关于确定性计数**（Anchor：PASCAL TMLR 2025、TPP ICML 2025，用户提供核验）：`s[t]` 是累计取整，Σs[t]=n 由 telescoping 平凡成立，"零条件方差"是确定性的同义反复。请给出相对 PASCAL 与 TPP 的可测增益，并直接对比；用户已注明 PASCAL 无官方代码，请自行复现而非在 related work 中一笔带过。
4. **关于机制闭合**（Anchor：缺失机制）：β*=θ/(2T) 的推导在 A 行和≠1 时未给出；A 非负不限制 ‖A‖，误差被放大的界缺失；"膜电位累加解码替代计数解码"与"确定性计数"是否冗余未消融。请补齐推导、误差界与消融，否则 method soundness 不成立。
5. **关于证据与可比性**（Anchor：用户明述视觉侧零正式实验 + 基线代码现状）：视觉侧无任何正式实验，中心新颖主张零支撑；横评未定义"所有方法是否在同一被修改骨干上"。请固定统一 protocol 后再谈 conversion loss，并定量报告原版 ViG（动态 KNN + max）失效边界。
6. **关于 venue 与主轴**（Anchor：贡献拼盘 + 数据集约束）：理论重述、确定性技巧、首次脉冲化、横评四者并列，缺单一深主轴；无 ImageNet-1K 的 CVPR/ICCV 投稿会被读成小规模增量应用。请收敛主轴并明确落点，或补等价规模证据。

---

## Fixability table:

依 `calibration.md` 字段。Owner skill 仅列出建议归属，**未执行任何 handoff**（见 Optional next-module decision）。

| Issue | Affected dimension | Severity | Fix class | Can fix before writing? | Required evidence or design change | Risk-reduction condition | Development-potential impact | Owner skill |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 主张—适用条件错位 | Problem / Conceptual / Acceptance | high（fatal） | problem-refinement + method-redesign | partly | 改写中心主张为"固定线性算子类上的统一 + 失效边界"；或扩展算子类至至少一类数据依赖算子 | 主张与适用条件自洽，且不再声称覆盖原版动态/非线性 ViG | 中（解此条是升档前提） | ccf-idea-optimizer |
| F2 novelty 重述 / 组合 | Novelty / Conceptual | high（fatal） | novelty-grounding | no（需实验/推导证据） | 给出统一带来的新推论，或降级为"统一协议 + 横评 + 边界"增量定位；全文删除"发明数学组件"措辞 | 相对 PASCAL / TPP 有可归因增益，或 novelty 主张与核验结论一致 | 低—中 | ccf-literature-searcher（若用户授权重检）/ ccf-idea-optimizer |
| F3 横评可比性两难 | Experimental / Acceptance | high（fatal） | evidence-design | partly | 固定统一 protocol；所有基线同一被修改骨干；PASCAL / TPP / CS-QCFS / ECL 自行复现 | 横评可在同骨干、同 T、同 θ、同 calibration 数据下复算 | 高 | ccf-experiment-designer |
| W3 机制未闭合（β* / ‖A‖ / 解码冗余） | Method soundness / Elegance | medium | method-redesign | partly | 一般 A 下 β* 推导或反例、‖A‖ 误差上界、两解码兼容性命题、组件消融 | 推导自洽且数值验证通过；冗余组件被删除 | 中—高 | ccf-idea-optimizer |
| W1 视觉侧零正式实验 | Experimental convincibility | high | evidence-design | no | CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS 上的完整视觉侧实验 + conversion loss–T 曲线 | 视觉侧中心主张获得实证支撑 | 高 | ccf-experiment-designer |
| W4 原版 ViG 失效边界未定量 | Method / Experimental | medium | evidence-design | yes | 原版动态 KNN + max 非线性作为失效边界的定量报告 | 适用条件被实证界定，而非仅文字声明 | 中 | ccf-experiment-designer |
| W5 ImageNet-1K 不可得 | Venue fit / Feasibility | medium | venue-switch | yes | 明确主投 TNNLS 档；或补等价规模证据 | venue 定位与数据规模自洽 | 中 | ccf-idea-optimizer（定位）/ ccf-submission-checker（官方规则核验） |
| W6 统一 protocol 未成文 | Experimental convincibility | medium | evidence-design | yes | 同骨干 / 同 T / 同 θ / 同 calibration / 同 conversion loss 定义的正式 protocol | protocol 可复算、可比 | 中—高 | ccf-experiment-designer |

> 「用户提供的未公开先验（图节点分类 T≤8 ANN−1.5pp 带内，未发表）」不列入任何 Issue 的 required evidence；不得用它替代公开实验。

---

## Upgrade / pivot actions:

依 `SKILL.md` workflow #8 标签分类。每条为具体动作，不含通用套话。

- **[problem-refinement]**：把中心主张从"统一非网格、数据依赖邻域聚合的算子级误差"改写为"固定、非负、线性传播算子类上的层类型无关精确误差统一 + 该类算子上与全套基线的统一协议 conversion loss 横评 + 明确失效边界"；把 ViG 的"冻结 KNN 图 + 线性化 max-relative"定位为"算子类成员构造"，不再表述为"原版 ViG 脉冲化"。
- **[method-redesign]**：补一般 A（行和≠1）下 β* 的推导或反例条件、‖A‖ 相关跨层误差上界、膜电位累加解码与确定性计数 s[t] 的等价性/差异命题；用消融删除被证明冗余的组件。
- **[novelty-grounding]**：在统一协议下量化"现有逐算子校准方法 conversion loss 不一致/次优"这一前提；把 ② 的确定性化做成相对 PASCAL / TPP 的可测增益（低 T 精度、零 RNG 可复现性、能耗），而非性质重述；全文一致声明不发明任何已被占的数学组件。
- **[evidence-design]**：成文统一 protocol（同骨干 / 同 T / 同 θ / 同 calibration 数据 / 同 conversion loss 定义）；补齐含 PASCAL、TPP、CS-QCFS、ECL 自行复现的全套基线；报告 conversion loss–T 曲线、`B̂₂−B₂=A(E₁W₂)` 浮点残差、Σs[t]=n 与零方差验证、原版 ViG 失效边界量化；补视觉侧正式实验。
- **[feasibility-check]**：确认 RTX 3060 12GB / 远端 4090（已授权）上 ViG-SNN 实现与全套基线可跑通；评估 KNN 图冻结为预处理后脉冲域是否仍保留图结构开销，避免实现与主张不符。
- **[venue-switch]**：明确主投 IEEE TNNLS 档（类脑 + 理论 + 容较小数据集 + 篇幅容纳横评）；若坚持 CVPR/ICCV/NeurIPS，需先补 ImageNet-1K 级证据并解决 F2。
- **[pivot]**：若 C3 横评显示 OAC 与 PASCAL / TPP 在统一协议下等价，则放弃"新方法"定位，pivot 为"统一协议 benchmark + 失效边界分析"型贡献，并把 novelty 主张完全收敛到 ③。
- 不输出 **[abandon]**：中心主张可测、存在上述修复路线，依 `strict-idea-review.md` Stage-Aware Verdict Rule 不满足 abandon 条件。

**最小可行修复路线（用户硬要求，按依赖顺序）**：
1. 先做 **[problem-refinement]**（改主张 + 显式写适用条件 + 把原版 ViG 定为失效边界）——不耗实验即可消除 F1 的表述层致命性；
2. 再做 **[evidence-design]** 的第 1 步：固定统一 protocol，并**仅先复现 PASCAL 与 TPP 两个最决定性基线**（二者是 ②③ 的最近邻），在同一被修改骨干上跑 CIFAR-10/100 + Planetoid 的最小横评——这是判定 F2 / F3 是否可解的最小可测实验；
3. 同时做 **[method-redesign]** 的第 1 步：给出一般 A 下 β* 的推导或反例条件（纸面工作，无算力成本）；
4. 依据第 2 步结果决定：若有可归因增益 → 继续补齐全套基线 + 视觉侧实验 + 主投 TNNLS 档（`revise` 方向）；若与 PASCAL / TPP 等价 → 执行 **[pivot]**，把贡献收敛为"统一协议横评 + 失效边界"。
5. 全程不把「用户提供的未公开先验（未发表）」写入任何证据表。

---

## Evidence that would change my score:

**会升分的证据（全部需为公开可复算、非编造）**
- 统一 protocol 下含 PASCAL / TPP 自行复现的全套 conversion loss 横评，显示 OAC 有可归因于"算子级统一"的稳定增益（影响 Experimental / Novelty / Acceptance）。
- 一般 A（行和≠1）下 β* 的严格推导 + ‖A‖ 误差上界 + 数值验证（影响 Method soundness）。
- `A(E₁W₂)` 在"固定+非负+线性"之外覆盖至少一类数据依赖或非线性算子的证明与实验（影响 Novelty / Conceptual，是 F2 的唯一实质解）。
- 跨两类骨干的"逐算子校准导致 conversion loss 不一致"实测前提（影响 Problem importance）。
- 原版 ViG（动态 KNN + max）失效边界的定量报告（影响 Method / Experimental）。
- 组件消融证明每个组件独立不可替代（影响 Elegance）。

**会坐实 fatal / 降分的证据**
- 横评显示 OAC 与 PASCAL / TPP 等价 → F2 坐实，Novelty 维持 2 或降 1。
- β* 对一般 A 不成立且无替代闭式 → Method soundness 降 1。
- 坚持原中心主张而不写适用条件 → F1 保持 fatal，全部升分条件失效。

**明确不作为证据的项**：任何录用概率、真实审稿人意见、meta-review、未核验的官方当年规则、以及「用户提供的未公开先验（图节点分类 T≤8 ANN−1.5pp 带内，未发表、不充当公开证据）」。本报告未生成上述任何一类，也未生成任何实验结果数值。

---

## Recommendation:

**`pivot-with-rescue-route`**（5 选 1 之内；用户硬要求）

理由（与分数、fatal gates、stage-aware 规则一致）：
- 加权 2.5 落在 `calibration.md` 的 1.0–2.9 段，默认 high-risk reformulate，但用户限定 5 选 1，且五条 fatal gate（novelty≤2 高置信、method≤2、experimental≤2、beyond-modules、internal conflict）同时把推荐封顶为 `pivot-with-rescue-route`；
- 不取 `needs-literature-search`：novelty 已按用户指令标 `searched`（依据用户提供的独立核验结论），且结论是"高重叠"而非"未知"；
- 不取 `abandon`：中心主张可测（恒等式数值验证、统一协议横评、失效边界），且存在具名修复路线（见最小可行修复路线），依 `strict-idea-review.md` 不满足"无可测主张且无重构"条件；
- 不取 `revise` / `accept-to-develop`：三条 fatal risk 未解、视觉侧零正式实验，任一未解都不足以升档。

含义：保留最佳要素（固定线性算子的统一误差视角、统一协议横评、失效边界分析），改变**问题表述**（收敛主张）、**方法**（补一般 A 推导 / 扩展算子类）、**证据**（统一 protocol + PASCAL/TPP 复现 + 视觉侧实验）与**venue**（主投 TNNLS 档）中的至少一组。

---

## Optional next-module decision:

- **CCFA Handoff Mode: PARTIAL**（依 `SKILL.md` 与 `handoff-modes.md`）。本任务为**独立红队评审**，用户未请求任何 sibling-skill 切换，也未授权把未发表 idea 文本用于检索；依 workflow #10「if a module is denied, stop at verdict, risks, and action queue」，本评审**停止在 verdict / risks / action queue，不执行任何 handoff**。
- 未切换的模块：`ccf-idea-optimizer`（主张收敛 / method-redesign）、`ccf-experiment-designer`（统一 protocol 横评）、`ccf-literature-searcher`（若用户要求重新公开检索以扩展 closest-work 覆盖）、`ccf-submission-checker`（核验目标 venue 当年官方 policy / review form / page limit）。
- 若用户**显式授权**后续切换，按 PARTIAL 模式建议顺序：`ccf-idea-optimizer`（先解 F1 / W3，纸面为主）→ `ccf-experiment-designer`（再解 F3 / W1，含 PASCAL / TPP 复现）→ 视横评结果决定是否进入 `ccf-paper-writer`。本评审不代写、不模拟上述模块的输出，也不预判其结果。
- 隔离声明：上述建议不含任何已执行的检索、实验或写作，不含任何录用概率与真实审稿记录。

---

## Checklist status:

依 `SKILL.md` Mandatory Review Checklist（standard 模式 10 条）逐条如实标注。

| # | 检查项 | 状态 | 说明 |
| --- | --- | --- | --- |
| 1 | Target venue/journal、venue family、field、assumptions 明确 | pass | 见 Target venue/journal and assumptions；官方当年 policy 未核验已注明 |
| 2 | 每个 idea 归一化为 problem / gap / root challenge / insight / method mechanism / expected evidence / limitation | pass | 见 Normalized idea（7 要素 + 内部先验隔离标注） |
| 3 | Literature status 标注为 searched / partially searched / user-provided only / not searched | pass | novelty = `searched`（用户指令）；本会话检索动作 = `user-provided only`；边界见 Search basis |
| 4 | standard 模式有来自 public-safe literature search 的 closest-work table，除非用户禁止浏览或隐私阻止 | **partial** | closest-work 表已建（8 条，字段齐全），但来源为**用户提供的独立文献核验结论**，本会话未执行公开检索；依据：用户明确指定 search basis 并已提供核验结论，且依 `privacy-and-evidence.md` 未把未发表 idea 文本用于查询。未编造任何 URL/DOI |
| 5 | 五个专家角色独立应用：field / method / experiment / AC-venue / skeptical prior-art | pass | 见 Per-expert reviewer notes，各自独立 + Panel Synthesis，置信度与分数分开 |
| 6 | 所有 rubric 维度 1–5 打分或标注 n/a 与理由；每个 ≤3 含 deduction / evidence basis / repair condition / 预期分数变化 | pass | 10 维全打；9 个 ≤3 项均有完整明细块（扣分理由 / 证据基础 / 为什么重要 / 修复条件 / 预期分数变化 / development-potential effect）；Feasibility=4 在表内给出 deduction 与 repair |
| 7 | Fatal risks 与可修复弱点、局部细化分开 | pass | 见 Serious blockers（F1–F3 fatal；W1–W7 fixable） |
| 8 | Confidence 与 score 分开报 | pass | 综合 Confidence=Medium 单列；各维 Confidence 在 rubric 表；未因置信度下调分数 |
| 9 | 推荐值为 5 选 1 之一；`abandon` 仅用于无可测主张且无重构 | pass | `pivot-with-rescue-route`；abandon 条件已论证不满足 |
| 10 | 任何可选模块切换遵循 CCFA handoff mode；若被禁用则只输出 upgrade actions | pass | PARTIAL 模式，未执行 handoff，仅输出 Upgrade / pivot actions 与建议 owner |

补充标准模式 `task-modes.md` 状态：Mode = standard；Checks run = 完整 mandatory checklist + 输出契约 21 字段 + 定量反馈 + panel 纪律 + fatal gates + Output Quality Gate；Checks skipped = 无（除 #4 标 partial）；Unresolved risks = 官方当年 venue policy 未核验、一般 A 下 β* 推导缺失、视觉侧零正式实验、本会话未重新公开检索。

---

## Output self-check:

依 `review-output-standards.md` Output Quality Gate 与 `task-modes.md` Output Quality Gate 逐项自检（作为读者通读一遍后确认）。

| # | 检查项 | 结果 | 具体确认 |
| --- | --- | --- | --- |
| 1 | 小节顺序匹配承诺的输出契约 | ✓ | 从 `## Verdict first:` 到 `## Output self-check:` 共 21 个契约字段，顺序与 `SKILL.md` Output Contracts（单 idea / standard）完全一致；首字段即 Verdict first，末字段即 Output self-check |
| 2 | 每个表格有合法 Markdown 分隔符且每行列数一致 | ✓ | Rubric 表 6 列、Closest-work 为字段块（非表）、Fixability 表 9 列、Score-change 表 3 列、Checklist 表 4 列、本表 4 列；逐行核对列数一致，单元格内无裸 ASCII `|` 破坏分隔 |
| 3 | 分数、置信度、推荐内部一致 | ✓ | 加权计算 250/100=2.5 复核无误；`**Overall:** 2.5`（一位小数）；1–10 转换 5.0；综合 Confidence=Medium 与各维 Confidence 分开；2.5 + 五条 fatal gate → `pivot-with-rescue-route`，且已在 Weighted final score 字段解释分数段与 5 选 1 的映射，无矛盾 |
| 4 | 项目符号语法平行、动作风格一致 | ✓ | Upgrade / pivot actions 统一用 `[标签] + 动作动词` 开头；Fixability / Score-change 用名词短语或条件句 |
| 5 | 因果/递进逻辑显式（问题→原因→后果→行动） | ✓ | 每个 ≤3 块按"扣分理由→证据基础→为什么重要→修复条件→预期变化"排列；Serious blockers 按 fatal→fixable 分层；最小可行修复路线按依赖顺序编号 |
| 6 | 语言内标点一致 | ✓ | 正文中文全角标点（，。；：）；公式、字段名、文献名、venue、英文缩写、代码标识符保留半角；Markdown 表格分隔符与代码块为半角（属格式必需） |
| 7 | 无 TBD / TODO / [fill] / 空标题占位 | ✓ | 无占位符；所有字段均有实质内容；代码块内的 `high / medium / low` 为契约模板值，均已填具体值 |
| 8 | 无通用套话（"需要更多实验 / 创新性不足 / 进一步完善 / 加强 related work"等）无锚点残留 | ✓ | Strict reviewer comments 6 条均带 Anchor；每条批评均指向具体 claim / 机制 / prior-art / 缺失比较 / 可行性约束，并给出对应修复或 pivot |
| 9 | 每个 ≤3 分项含扣分理由 / 证据基础 / 修复条件 / 预期分数变化（用户硬要求） | ✓ | 9 个 ≤3 维度各一个明细块，四项齐全，另附 Why it matters 与 Development-potential effect |
| 10 | 五个专家角色独立、各自给具体拒稿级质疑或说明为何没有；置信度与分数分开 | ✓ | 5 个角色均含 Score tendency（分数）与 Confidence（置信度）两行；均给出 strict rejection-grade concern + Anchor + Why + Fatal + Repair + Development note；无角色被强行安排"无质疑" |
| 11 | fatal risk 与可修复弱点明确区分；含 score-change conditions 与最小可行修复路线 | ✓ | Serious blockers 的 F1–F3 / W1–W7；Score-change conditions 表含升分与反向降分条件；Upgrade / pivot actions 内含按依赖排序的"最小可行修复路线"5 步 |
| 12 | 推荐值仅为 5 选 1 之一 | ✓ | `pivot-with-rescue-route` |
| 13 | 禁止编造：文献 / 数值 / 实验结果 / 评审意见 / 录用概率 | ✓ | 全部文献仅来自用户提供的核验清单（venue/year 照录，未附 URL/DOI）；无实验结果数值、无录用概率、无真实审稿人/meta-review 引用；专家意见与 Strict reviewer comments 已声明为"本红队 panel 独立判断"；加权分数与预期变化为按 rubric 计算/条件性表述，非实验结果 |
| 14 | novelty 状态标为 searched 并写明边界 | ✓ | Search basis 字段标 `searched`，并写明 4 条边界（证据来源为用户核验结论、本会话未重新检索、覆盖范围、禁止编造 URL）；Novelty delta 字段复核三处空白为"伪 / 组合 / 真实但增量" |
| 15 | 未发表内部结果仅标注为「用户提供的未公开先验」 | ✓ | Normalized idea、Serious blockers、Fixability、Upgrade actions、Evidence 中凡提及 T≤8 ANN−1.5pp 均标注"用户提供的未公开先验（未发表、不充当公开证据）"，且明确不进入 evidence / 打分依据 |
| 16 | 文件用中文撰写、保留技能要求的全部字段标题 | ✓ | 21 个英文契约字段标题原样保留（Verdict first: … Output self-check:），正文全部中文 |
| 17 | Verdict first 给结论、回复含 `**Overall:**` 行与 recommendation | ✓ | Verdict first 段含完整结论与推荐；`**Overall:** 2.5` 在 Weighted final score 字段以独立行给出；聊天回复另给 `**Overall:**` 行与 recommendation |

**最终一致性确认**：本报告为独立红队评审，未由主会话代写或模拟打分，未抬分；所有分数证据基础可追溯至用户提供的 idea 文本与用户提供的 prior-art 核验结论；未把未发表内部结果当公开证据；未越权执行任何模块切换；未生成任何编造内容。
