# P1B · 预实验对抗评审（独立会话，standard 模式）

> 角色：`f-research-v1` P1B 阶段**独立预实验对抗评审员**。模式：`ccf-idea-reviewer/SKILL.md` `standard`；依据 `references/strict-idea-review.md`、`rubric.md`、`calibration.md`、`expert-panel.md`、`source-notes.md` 与 `../ccf-common/references/`（`review-output-standards.md`、`privacy-and-evidence.md`、`task-modes.md`、`handoff-modes.md`、`routing.md`），全部已加载。
> 评审对象：`guidance-v2.md`（权威契约）＋ `contract-change-v1-to-v2.md` ＋ v1 第三轮红队 ＋ `contracts/guidance-validation.md` ＋ `protocols/vision_pipeline.py` / `run_experiments.py` ＋ `evidence-snapshots/m0-results.json`，以及本会话**额外实读**的运行目录产物（`results/*.json`、`pipeline-state.json`、`execution-contract-v1.md`、`contracts/core-1028.snapshot.py`、`data/` 磁盘清单）。
> 评审焦点（用户指定）：**预实验可执行性与风险修复条件**。「尚未开始正式 P2/P3 实验」是 guidance 之后 P1B 的正常状态，本评审**不把它本身判为致命缺陷**。
> 硬约束：只报告实际读到的信息；不编造文献、URL、数值、评审意见或录用概率；未发表 1028 成果全程标注「用户提供的未公开先验（未发表、不充当公开证据）」；不把「预注册目标」写成「已得结果」；不把「45 nm 理论算术能耗估算」写成「硬件实测」。
> 本报告内全部专家意见、严格评审意见均为**本评审 panel 基于真实文件作出的独立判断**，不代表任何真实审稿人、meta-review、录用记录或录用概率；不承诺任何分数变化、审稿行为或录用结果。本会话未执行公开检索，未生成任何 URL/DOI/实验数值（数值均照录已读工件），未运行任何训练或推理。

---

## Verdict first:

**结论先给**：按 Q1–Q2 类脑与神经网络期刊档（IEEE TNNLS / Neural Networks 档）评，本 P1B 包的**可执行性显著强于 v1 场景**（官方自带图数据已落盘、实现代码完整、本机 CUDA smoke 已实跑、三个真实缺陷已发现并修复、组件继承逐条写明、能耗被写成可证伪假设而非结论）；但对**「是否存在未解 fatal risk 会阻止进入 P2/P3」这一 P1B 唯一硬门**，判定为 ——

**不存在未解 fatal risk（0 条），不阻止进入 P2/P3（proceed conditional）。**

这一结论与 v1 第三轮红队（`idea-red-team-review-rev3.md`，`**Overall:** 3.4`、0 未解 fatal、`proceed` conditional）**在门禁结论上一致**；但本评审**不沿用其分数、不抬分**：本轮 lens 是「预实验可执行性」，且本轮**有 v1 当时没有的代码与实跑工件可读**，因而把实现层风险如实计入扣分。加权总分 `**Overall:** 3.3`（1–5 加权尺度，一位小数），落在 `calibration.md` 的 3.0–3.6 段 → `pivot-with-rescue-route`。

**必须区分的三件事（防误读）**：
1. `pivot-with-rescue-route` 是 `ccf-idea-reviewer` 对 **idea 当前就绪度**的 5 选 1，由加权分数段机械得出，**不等于「阻止 P2/P3」**；对 P1B 硬门的独立裁决是 **0 条未解 fatal、可 proceed**，二者分属不同体系（沿用 v1 第三轮 `Recommendation` 下 `Startup-decision` 的区分逻辑）。
2. `results/` 下 4 个 JSON 是**单 seed=0、MNIST、小子集、本机 CUDA 的预实验 smoke 产物**，`pipeline-state.json` 显示 P0–P21 **全部 pending** —— 这正好印证「正式 P2/P3 尚未开始」。这些数值**不是已得正式结果**，本评审不把它们写成结论；但它们是**已落盘的真实风险信号**，不能忽视。
3. 全部能耗数值是 **45 nm CMOS 理论算术能耗估算（MAC 4.6 pJ / AC 0.9 pJ）**，`energy_accounting` 的 model 字段已明写 `NOT a hardware measurement`；本评审全程不称其为硬件实测焦耳数。

**五问判定表（完整依据见 `Serious blockers` 末尾「评审任务五问 · 完整依据」）**

| # | 问题 | 判定 |
|---|---|---|
| 1 | 当前是否存在未解 fatal risk 会阻止进入 P2/P3（P1B 唯一硬门） | **否，0 条**。逐条核对见 `Serious blockers` A 段；无「不可修复的结构性 fatal」。但附 **3 条准 fatal 级、必须在进入 P2/P3 前闭合的修复条件**（能耗核算口径、ρ_n 算子类对应、恒等式精度/teacher 门槛）。 |
| 2 | 组合与适配创新在「自带图视觉数据集 ＋ 全套转换方法横评 ＋ ANN/能耗对照」证据包下是否构成可辩护贡献（不要求新数学定理） | **有条件的可辩护（薄、以系统实证与统一协议为主）**。可辩护的是「首个图结构视觉分类上的转换方法统一横评 ＋ 恒等式迁移验证 ＋ 精度/时延/理论能耗三重证据」，**不是**新理论组件，也**不能**声称「组合产生了 prior-art 无法得到的新能力」。且当前实现的 `rho_mean≈0.9987` 与契约「ρ_n 远离 1 的非行随机新算子类」直接矛盾，实验基础尚未落地（见 `Novelty delta`）。 |
| 3 | 能耗主张的最大风险是什么？最小修复/裁定实验？ | **最大风险**：用户预判「一定有优势」与已落盘 smoke **相反信号**（全部 `energy_ratio_ann_over_snn` 未达预注册 ≥5×，在 conversion loss 最小的 T=16 仅 0.28×）；且核算口径**系统性不自洽**（ANN 计全层、SNN 仅计脉冲层 AC 且随 T 线性累加）。**最小裁定实验**：统一口径 ＋ 三口径敏感性 ＋ 绝对量同报 ＋ 在等精度 T 上裁决 ＋ 按契约收窄表述（见五问依据 #3）。 |
| 4 | teacher 68%（子集 2000 图）是否足以支撑 conversion loss 比较？还缺什么？ | **不足以支撑有判别力的正式比较，但作为 P1B smoke 管线验证合格且正常**。磁盘 `gpu_MNIST_seed0.json` 实为 `train 0.689 / val 0.668 / test 0.688`（与用户任务描述「67.5% / 68.2%」不一致，以文件为准）；缺全量 teacher、teacher 验收门槛、1028 回归锚点、统计功效预检、设备噪声量化（见五问依据 #4）。 |
| 5 | 数据/基线/算力路径是否可执行？ | **子集 smoke 级可执行（已实跑），全量路径有条件可执行**。数据两源口径不一致、QCFS 基线在当前实现里数值退化为 naive、缺直训脉冲 GCN 与 Planetoid 回归锚点、无图级 minibatch 使全量扩展需改代码、CUDA 非确定性未量化 —— 均为可修复；3060 12GB ＋ 已授权 4090 是回退保障（见五问依据 #5）。 |

`**Overall:** 3.3`

**综合 recommendation（`ccf-idea-reviewer` 5 选 1）：`pivot-with-rescue-route`**；**P1B 硬门裁决：`proceed`（conditional，附 P2/P3 入口硬条件 H1–H8）**。二者不矛盾，理由见 `Recommendation`。

---

## Target venue/journal and assumptions:

- **目标档位**：Q1–Q2 类脑与神经网络期刊（IEEE TNNLS / Neural Networks 档），非 CCF-A 主会档。依据 `guidance-v2.md` §Title/Topic、`execution-contract-v1.md` §4、v1 第三轮 §0。本评审全程按此档评，不套用 CVPR/ICCV/NeurIPS 主会标尺。
- **Venue family / 领域**：类脑计算 × ANN→SNN 转换 × 图结构视觉分类；贡献类型由 v2 明确定为「**组合与适配创新**」＋「系统实证比较」＋「精度/时延/理论能耗三重证据」。
- **阶段边界（用户硬要求）**：当前为 guidance 之后的 **P1B 预实验对抗评审**。`pipeline-state.json` 中 P0–P21 全为 `pending`；`pipeline-state.md` 第 14 行把 `audits/ccfa-pre-experiment-review.md`（本文件）列为 P1B 证据。按 `f-research-v1` 门禁语义，P1B 的唯一硬门是「是否存在未解 fatal risk 阻止进入 P2/P3」，**不是**「现在有没有跑出正式精度/能耗结果」。本评审严格遵守：不把「0 正式实验」判 fatal，只评估 evidence plan 与实现路径的可执行性、自洽性与诚信边界。
- **成稿隔离（用户硬要求）**：1028 成稿方法组合（`B̂−B = R A (E₁W₂)`、`β*=θ/(2T)`、膜电位解码、确定性两阶段、gauge 等）及其在图节点分类上「`T≤8` 达 `ANN−1.5pp` 带内」等数值，一律为 **「用户提供的未公开先验（未发表、不充当公开证据）」**；仅作方法机制与命题出处核对，不进入 closest-work 公开证据层、不进入打分依据、不替代本文公开视觉实验。`contracts/core-1028.snapshot.py` 是复制进 run root 的本地只读快照，不改变其未发表属性。
- **已读工件真实性核验（本会话）**：
  - 数据：`data/pyg_bench/CIFAR10/raw/CIFAR10_v2.zip` = **316,368,127 B**（与 `execution-contract-v1.md` §5、用户任务描述一致）；MNIST 侧当前目录树中**未直接见到 192,378,381 B 的 zip**，见到 PyG 处理后的 `MNIST/raw/MNIST_v2.pt` = 921,808,681 B 与 `MNIST/processed/{train,val,test}_data.pt`（670,169,669 / 60,970,309 / 121,853,957 B）。三 split 文件齐全、`gpu_MNIST_seed0.json` 的 `n_total` 记 55,000/5,000/10,000，证明 `GNNBenchmarkDataset(split="val")` 在本环境**实际可用**（此项不构成 fatal）。
  - 实跑：`results/` 下 4 个 JSON（smoke/smoke2/smoke3/gpu）全部 `seed=0`、`dataset=MNIST`、本机 CUDA，runtime 9.9 / 47.01 / 64.29 / 66.87 s。
  - 代码：`protocols/vision_pipeline.py`（351 行）、`protocols/run_experiments.py`（158 行）、`contracts/core-1028.snapshot.py`（509 行）已完整读取。
  - M0：`evidence-snapshots/m0-results.json` 为 v1 的**合成算子 float64 数值核验**（meta：C=7, H=24, N=64, T∈{1,2,4,8,16}, ρ∈{0.5,1,2,5,10}, seed 20261110, purpose 明写「no training, no accuracy claim」）。P1 25 格最大绝对残差 `9.880984919163893e-15`；P4 每 T 384 对、5 个 T 合计 1920 对、`violations=0`；P5 20,000 激活 × 5 T、`dtp_conditional_variance_zero=true`、`sum_exact_fraction=1.0`；P6 `fixed_linear_A` 残差 `1.7763568394002505e-15`、`dynamic_A_per_step` `0.7058297672203355`、`max_nonlinear_aggregation` rate-vs-ANN 偏差 `1.1668779395601996`。**M0 不训练、不报分类精度、不证明能耗、不证明单调判据**。
- **数值以文件为准的差异（如实记录，非编造）**：用户任务描述写「修复后 CUDA 训练 hidden=128/lr=0.01/800ep 达 train 67.5%、val 68.2%」；磁盘 `gpu_MNIST_seed0.json` 的 `ann` 实为 `train_acc 0.689 / val_acc 0.668 / test_acc 0.688 / epochs 800 / hidden 128 / gauge_scale 0.5435125759243968`。二者不一致，本评审**以文件为准**（与 v1 第三轮处理 SHA 口径、P4 对数 3840→1920 同款纪律），并把该差异登记为证据工件口径一致性弱点（W11）。
- **本评审未做的事**：未核验目标期刊当年官方 policy / page limit / review form / deadline（依 `source-notes.md`，`guidance-v2.md` §Figure/Table 亦自认「尚未核验」）；未执行公开文献检索；未生成 URL/DOI；未运行任何训练/推理；未修改任何被评审文件；未把未发表 idea 文本用于查询。

---

## Search basis:

- **novelty 状态**：`searched`（**组件层**，依据用户提供的、已由 v1 三轮独立核验的 prior-art 结论；沿用 v1 判定）／**组合与推论层 `not searched`**／**本会话检索动作 `not performed`**。三者不矛盾：前者是状态标签，中者是覆盖边界，后者是本会话事实。
- **边界（必须写明）**：
  1. closest-work 证据来源为**用户提供的独立文献核验结论**与 `guidance-v2.md` §Citation Scope 的 venue/year 清单，本会话未重新执行公开检索，故属 `user-provided only`。
  2. 组件层覆盖「数学组件归属」（β*、零期望偏置、精确等式、膜电位解码、确定性计数、两阶段、跨 CNN+GCN 归谁）；**组合层 / 推论层未针对检索**（如「superpixel graph ANN-to-SNN conversion」「row-sum weighted bias on non-row-stochastic vision graphs」是否已被 2025–2026 工作给出）。
  3. 依 `strict-idea-review.md`「Cap novelty at 3 if closest work was not searched and novelty is decision-critical」，**本评审 novelty 封顶 3、置信度 3**；不做 `high novelty` 断言。
  4. 依 `privacy-and-evidence.md`，未把未发表的私有 idea 表述放入任何检索查询；依 `source-notes.md`，closest-work 表不提供本轮未核验的链接/DOI（禁止编造 URL）；不转录被评审工件中已存在的仓库 URL；不引用 MDPI 来源。
- **literature status label**（checklist #3）：`searched`（组件层）／`user-provided only`（本会话动作用）／**组合与推论层 `not searched`**。
- **public-safe queries**：本会话未执行，无查询记录。若后续需要，按 `strict-idea-review.md` 应以通用公开关键词先行，不粘贴私有措辞。
- **不升级为 `needs-literature-search` 推荐的理由**：novelty 按用户指令标 `searched`（组件层，依据已核验结论），结论为「组件层高重叠 ＋ 组合/证据包薄增量」而非「未知」；组合/推论层未检索作为**边界与置信度**处理（封顶 novelty 3、conf 3），沿用 v1 第三轮 `Recommendation` 的同款处理。本评审焦点为「预实验可执行性」，novelty 的最终裁决留给后续门，不在此预支。

---

## Stage and development potential:

```text
Current conference readiness: low
Development potential: medium
Main reason it is not ready: 核心结果（conversion loss 带内、全套转换横评优势、理论能耗 ≥5×）全部为预注册目标、尚未实测；能耗核算口径不自洽且已落盘 smoke 给出与「一定有优势」相反的信号；rho_mean≈0.9987 与契约「非行随机新算子类」瓶颈矛盾；teacher 为 2000 图子集 68% 级；全套基线忠实度与回归锚点未兑现；组合/推论层 novelty 未检索。
Best rescue route: 以「0 未解 fatal / proceed conditional」进 P2/P3，按 H1–H8 入口条件先闭合能耗口径、ρ_n 算子类、恒等式精度与 teacher 门槛，再按统一协议做 5 seeds 全量横评、逐组件消融、ANN/理论能耗对照与统计检验；把贡献稳定锚在「组合在新算子类/任务类上的可分析性 ＋ 统一横评 ＋ 三重证据」，并预备 honest fallback（收敛为「首个图结构视觉分类上的转换方法统一横评与理论能耗分析」）。
Evidence needed to decide: 统一口径下的 energy_ratio(T) 与 spike 密度、conversion loss–T 曲线（5 seeds 配对 CI/BH）、ρ_n 受控网格上的误差分解、全量 teacher 与 1028 回归锚点一致性、组合层公开检索结果、目标期刊当年官方 policy。
```

**readiness 与 potential 均不升档的说明**：v2 相对 v1 的实质进步（自带图数据规避了 v1 的「冻结 KNN ＋ 线性化 max 聚合」适用条件错位、代码/数据/smoke 实跑就位、0 未解 fatal、能耗写成可证伪假设）是真实的，体现在 `Method soundness 4 / Feasibility 4 / Venue 4` 与门禁结论；但 readiness 仍取 `low`，因为核心实证、能耗口径自洽、算子类对应、teacher 质量、基线忠实度五项就绪条件无一完成。Development potential 取 `medium`：最佳要素（恒等式在图级管线的迁移验证、统一横评、诚实边界、可复算协议）有用且核心问题不需重写，但「ρ_n≈1 削弱 novelty 基础 ＋ 能耗已有反例信号 ＋ 组合必要性未证」三项未知仍在，不能断言「不改核心问题即可变 competitive」。升 `high` 的条件写在 `Confidence` 与 `Score-change conditions`。

---

## Normalized idea:

| 要素 | 归一化内容（P1B 实读版） |
|---|---|
| Problem | 一整套为图节点分类组合起来的 ANN→SNN 转换方法，在**自带图结构的视觉分类**（SuperPixel MNIST/CIFAR10 图级 10 类）上，能否同时保持 ANN 精度、低时延与算术能耗优势，并优于单点转换方法。 |
| Gap | 转换误差理论与校准律集中在 CNN 网格/行随机算子；图结构视觉表示与能效对照缺少统一分析；1028 组合只在引文图节点分类验证、未与全套转换方法横评、未比能耗。 |
| Root challenge | 契约声称视觉 kNN 图的聚合算子行和 ρ_n 远离 1，为 ρ≈1 推导的校准律不再自动成立；同时需精度、时延、能耗三者可查。**实读修正**：`batch_graphs(sym_norm=True)` 的对称归一化使实跑 `rho_mean≈0.9987`，该「远离 1」前提在当前实现里未成立。 |
| Insight（声称） | 「只要读出是线性算子（R），池化不破坏恒等式 `B̂−B=R A (E₁W₂)`」；「非行随机 ρ_n 使闭式偏置与膜电位解码收益更可观测」。二者均为**线性代数的直接后果 / 未实测预测**，非新定理（用户明确不要求新数学定理）。 |
| Method mechanism | 继承精确误差恒等式、`β*=θ/(2T)`、膜电位累加解码、ρ_n 加权系统误差、确定性两阶段 `s[t]=round(tn/T)−round((t−1)n/T)`（n clip 到 T）、gauge 到 `[0,θ]`；**适配**：块对角稀疏邻接、图级线性读出 R、图级交叉熵。全文不声称发明任何单个组件。`vision_pipeline.py` 为**独立重写**实现（未 import 1028 core、无 `vision_core.py`、gauge 为 percentile 缩放而非 1028 的 unit-spectral-gain `gauge_normalize`、check_identity 为单层非逐层）。 |
| Expected evidence | ① 恒等式浮点残差；② conversion loss ≤1.5pp（T≤8）；③ QCFS/FTBC/TPP/Parallel ＋ 朴素 rate ＋ 直训 SNN 同协议横评；④ 逐组件消融；⑤ ANN MAC vs SNN AC/SynOps 理论能耗对照；⑥ 5 seeds 配对 bootstrap CI ＋ sign-flip ＋ BH。**全部为预注册目标，非已得结果**。 |
| Limitation（契约自认 ＋ 实读补强） | 适用类仅固定、非负、线性邻接 ＋ 线性全局池化；能耗为理论算术估算非硬件实测；1028 为未公开先验；视觉侧 0 正式实验。**实读补强**：当前实现用 sum pooling（契约写 mean）、对称归一化使 ρ_n≈1、第一层为连续电流注入、能耗 AC 口径仅覆盖脉冲层、CUDA 稀疏归约非确定性未量化、无图级 minibatch。 |
| 隔离标注 | 1028 成稿及其全部数值、图节点分类 `T≤8` 达 `ANN−1.5pp` 带内、成稿 §3.2/§5.1 引用，均为「**用户提供的未公开先验（未发表、不充当公开证据）**」，不进入 evidence / 打分依据 / 公开实验替代。 |

---

## Closest prior art table:

依 `strict-idea-review.md` 的 closest-work 字段列出 8 条，**针对 v2「组合与适配创新」重评 Overlap / Remaining delta / Needed differentiation**。**Link/source 统一说明**：venue/year 与「已做的事」均来自用户契约 §Citation Scope 与 v1 三轮已核验结论，本会话未执行公开检索、未附 URL/DOI、不编造链接；成稿「用户提供的未公开先验（未发表、不充当公开证据）」不计入本表公开证据层。

**1**
- Closest work: Deng & Gu
- Venue/year: ICLR 2021
- Link/source: 用户契约 citation scope 所列 venue/year（本轮未检索 URL/DOI）
- What it already does: `β*=θ/(2T)` 与逐层误差递归。
- Overlap with user idea: 闭式偏置与「误差经传播算子递推」直接来自该脉络；恒等式是该递归的矩阵写法。
- Remaining novelty delta: v2 不主张发明 β*；仅主张「在图级池化 R 下恒等式仍精确成立」—— 这是 R 线性的直接后果。
- Risk to the idea: medium
- Needed differentiation: 用图级管线上的恒等式浮点残差与 ρ_n 受控网格证明「适配不是重述」，并给出 prior-art 在 ρ_n≠1 上给不出的可测预测（当前未给）。

**2**
- Closest work: QCFS
- Venue/year: ICLR 2022
- Link/source: 同上
- What it already does: clip-floor-shift 量化激活 ＋ 零期望误差偏置。
- Overlap with user idea: M0 P2 的 `mean_E1_no_bias ≈ −1/(2T)`、`mean_E1_with_beta_star ≈ 1e-3` 是该结论的数值复现；v2 把 QCFS 列为横评基线。
- Remaining novelty delta: 仅剩「该余数经 A 传播后按 ρ_n 加权」的观察。
- Risk to the idea: high（**实读补强**：`run_experiments.py` 未给 QCFS 传 `quantize_L`，实跑 `naive_T*` 与 `qcfs_T*` 的 `hidden_spikes`/`ac_ops` 完全相同，QCFS 在当前实现里数值退化为 naive —— 横评忠实度缺口，见 W5）
- Needed differentiation: 按方法要求给 QCFS 重训量化 teacher，并在统一协议下展示与 naive 的可测差异。

**3**
- Closest work: FTBC
- Venue/year: ECCV 2024
- Link/source: 同上
- What it already does: 前向时序偏置（较新视觉侧版本）。
- Overlap with user idea: 零期望偏置机制；`run_experiments.py:calibrate_ftbc_beta` 在 val 上网格搜索其 beta。
- Remaining novelty delta: 无独立 delta（归功继承）。
- Risk to the idea: medium
- Needed differentiation: 在 ρ_n≠1（当前实现未满足）上展示校准差异。

**4**
- Closest work: Dual-Phase
- Venue/year: IEEE TNNLS 2024
- Link/source: 同上
- What it already does: 膜电位累加解码替代计数读出 ＋ 精确误差等式。
- Overlap with user idea: 恒等式 `A(E₁W₂)` 与膜电位解码归功；M0 P1 验证的正是该等式在固定线性 A 上的精确性。
- Remaining novelty delta: 仅剩「把等式推广到图级 R 读出」。
- Risk to the idea: high（**实读补强**：真实管线 float32 恒等式残差为 `3.24e-5 ~ 6.41e-6`，比契约 Traceability 「<1e-12」高 6–7 个数量级，见 W7）
- Needed differentiation: 用 float64 验证路径把图级残差压到 1e-12 内，或重定义门槛并说明量级来源。

**5**
- Closest work: TPP（含 SpikeConverter AAAI 2022 两阶段脉络）
- Venue/year: ICML 2025（SpikeConverter: AAAI 2022）
- Link/source: 同上
- What it already does: 两阶段转换框架。
- Overlap with user idea: 确定性两阶段归功；v2 用 TPP 随机相作消融对照。
- Remaining novelty delta: 仅剩「确定性第二相的零条件方差在图级读出上的系统收益」（待裁定）。
- Risk to the idea: medium
- Needed differentiation: 报告 `Σs=n` 命中率、条件方差与 conversion loss 的配对差值（实跑 `sum_n_hit_rate=1.0` 已给，收益待 5 seeds）。

**6**
- Closest work: PASCAL
- Venue/year: TMLR 2025
- Link/source: 同上
- What it already does: 确定性精确计数。
- Overlap with user idea: 确定性计数归功；M0 P5 验证 Σs=n / 零方差，不主张相对 PASCAL 的新数学性质。
- Remaining novelty delta: 无数学组件 delta。
- Risk to the idea: medium
- Needed differentiation: 现为文献对照（无官方码，未复现），须在论文如实标注「未复现、不进主表」。

**7**
- Closest work: One-Spike SNN
- Venue/year: IEEE TETC 2024/2025
- Link/source: 同上
- What it already does: 跨 CNN ＋ GCN 的 ANN→SNN 转换。
- Overlap with user idea: 削弱「同一转换思路跨视觉与图骨干」的新颖性；v2 已归功。
- Remaining novelty delta: 仅剩「在自带图视觉数据集上的图级读出 ＋ 全套转换方法统一横评 ＋ 理论能耗对照」这一证据包视角。
- Risk to the idea: high（这是「只是把 1028 换个数据集」质疑的最近邻）
- Needed differentiation: 用统一横评 ＋ 消融 ＋ 理论能耗对照正面回答，且须先解决 ρ_n≈1 使「新算子类」论据不成立的问题。

**8**
- Closest work: Parallel Conversion / DCGS / AdaFire / CS-QCFS（横评对手集合）
- Venue/year: ICML 2025 / ICML 2025 / AAAI 2025 / Neural Networks 2025
- Link/source: 同上
- What it already does: 2025 年主流 ANN2SNN 转换方法；契约把前三者列为「适配/文献对照」，CS-QCFS 为文献对照。
- Overlap with user idea: 构成必须对齐的基线集合，代表 2025 年饱和度。
- Remaining novelty delta: 无（横评对象）。
- Risk to the idea: medium（**实读补强**：当前实现只自实现了 naive/qcfs/ftbc/tpp/parallel/ours 六种，DCGS/AdaFire/PASCAL/CS-QCFS 未复现、直训脉冲 GCN 未实现，见 W6）

**其他锚点（用户契约提供，不扩展、不编造）**：SLIC、Benchmarking GNNs（SuperPixel MNIST/CIFAR10 官方 pkl 与 split）、ViG、Horowitz IEEE ISSCC 2014（45 nm MAC/AC energy table）、SpikingGCN、Planetoid。数据集论文与 baseline 全表见 `guidance-v2.md` §Citation Scope（其 `literature-baseline-matrix.md` 本会话未读取，不作断言）。

---

## Novelty delta:

**状态**：`searched`（组件层）／**组合与推论层 `not searched`**。**结论**：减去最近邻工作后，v2 的 novelty 是「**薄但真实、以系统实证与统一协议为主的证据包增量**」，**不构成**「prior-art 无法得到的新数学结果」——这一定位与用户「组合与适配创新、不要求新数学定理」的要求一致，但仍受三处侵蚀。

| 声称的 delta | P1B 复核结论 | 判定 |
|---|---|---|
| 恒等式在图级 R 读出上精确成立 | R 线性 ⇒ `R A (E₁W₂)` 线性，是**一行代数**；M0（float64 合成）验证到 1e-15，真实管线（float32）仅 1e-5 量级（W7）。 | 真实但接近 obvious；精度口径未闭合 |
| 新算子类（非行随机 ρ_n 视觉 kNN 图） | **实读反例**：`batch_graphs` 默认 `sym_norm=True`，4 个 results JSON 全部 split 的 `rho_mean` 恒为 **0.9987**、`rho_max ≤ 1.1012`、`rho_std ≈ 0.0316`。对称归一化 `D^{-1/2}(A+I)D^{-1/2}` 把行和拉回 ≈1，实际算子类**近似行随机/双随机**，与 `guidance-v2.md` §Core Idea / §Mechanism-Level Rationale 反复强调的「ρ_n 远离 1」直接矛盾。 | **实验基础未落地**，是本轮最重的机制—实现错位 |
| 新任务类（图级视觉分类） | 真实：官方 SuperPixel 图 ＋ 图级 10 类；规避了 v1「冻结 KNN ＋ 线性化 max 聚合」的适用条件错位（F1）。这是 v2 相对 v1 最扎实的进步。 | 成立 |
| 全套转换方法统一横评 | 真实可测，属评估/benchmark 贡献；但当前实现 QCFS 退化为 naive、缺直训 SNN/Planetoid 回归锚点、DCGS/AdaFire/PASCAL/CS-QCFS 未复现（W5/W6）。 | 设计成立、实现打折 |
| ANN 上限 ＋ 理论能耗对照 | 45 nm 理论算术能耗是社区标准做法，本身不新；且核算口径不自洽、已落盘 smoke 未支持「≥5×」（W1/W2）。 | 佐证价值有限、风险集中 |
| 组合在新类上的「可分析性」 | 建立在未发表的 1028 组合上；论文须自包含重推恒等式（契约 §3 Method 已规划）方可被外部核验。 | 前提，非已完成 |

### 特别回答（评审任务 #2）：组合与适配创新是否构成可辩护贡献？

**明确结论：有条件的「可辩护」，且是「窄、以系统实证与统一协议为主」的可辩护，不是新理论/新机制贡献。**

- **可辩护的一面**：① 自带图视觉数据集确实消除了 v1 的适用条件错位，恒等式 `R A (E₁W₂)` 在固定线性 A ＋ 线性 R 下精确成立（M0 ＋ 实跑 `sum_n_hit_rate=1.0` 佐证）；② 新任务类（图级视觉分类）＋ 全套转换方法同协议横评 ＋ ANN 上限 ＋ 理论能耗对照，构成一个**可复算、可审计、自限清晰**的证据包，对把 GNN 用于 SNN 的社区有直接复用价值；③ 组件继承逐条写明、不声称发明单组件、能耗写成可证伪假设、理论估算与硬件实测严格区分 —— 这些诚实边界对 Q1–Q2 期刊是加分。按「组合与适配创新、不要求新数学定理」的定位，这足以支撑一个**增量**贡献。
- **不抬分的一面（严格审稿人仍会问）**：① 「池化线性 ⇒ 恒等式不破坏」是线性代数的直接后果，与 v1 第三轮的「一行代数 objection」同源，v2 未消除它，只是把贡献重心从「新推论」移到「新证据包」；② 证据包 ≠ 贡献，全套横评 ＋ ANN/能耗对照容易被读成 benchmark/工程比较而非 main-track 理论贡献，能否成立高度依赖横评是否显示 1028 组合**系统优于**各单点基线（预注册 ≥1.0pp），而该结果尚无；③ One-Spike SNN 已跨 CNN＋GCN、Dual-Phase 已有恒等式＋膜电位解码，组合的**必要性**（哪些组件/交互是在新算子类上才出现、prior-art 给不出）未被消融证明；④ `rho_mean≈0.9987` 使「新算子类」论据在当前实现里不成立，削弱了「适配」二字的实质；⑤ 1028 是未公开先验，可分析性须靠论文自包含重推，否则外部不可核验。
- **边界表述**：可辩护的上限是「首个图结构视觉分类上的转换方法统一横评 ＋ 恒等式迁移验证 ＋ 精度/时延/理论能耗三重证据」；**不能**声称「组合产生了 prior-art 无法得到的新能力」除非「逐组件消融 ＋ 全套横评显示系统优势 ＋ ρ_n 受控网格的非平凡性证据」三者同时支持。若横评未显示组合优势或能耗优势被证伪，按契约 `Story Strength Audit` 的 honest fallback 收敛为「统一横评 ＋ 理论能耗分析」，仍是 Q1–Q2 可接收的增量，但贡献进一步变薄。

**明确不可声称的内容**：不声称发明 β*、逐层误差递归、零期望偏置、膜电位累加解码、精确误差等式、确定性计数、两阶段、跨 CNN+GCN 转换；不声称 M0 或 smoke 证明了 conversion loss 带内/横评优势/能耗优势；不声称 45 nm 估算为硬件实测；不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」；不把「用户提供的未公开先验（未发表、不充当公开证据）」当公开前作。

---

## Serious blockers:

**A. Fatal risks（未解、不可修复的结构性 fatal）：0 条。**

逐条核对依 `calibration.md` Fatal Gates、`strict-idea-review.md` Stage-Aware Verdict Rule、`guidance-v2.md` §Stopping criteria 与用户「P1B 唯一硬门」定义：

| 潜在 fatal / gate | P1B 状态 | 是否构成未解 fatal |
|---|---|---|
| 数据不可得 / 解析失败 | **否**。CIFAR10 zip 316,368,127 B 落盘；MNIST processed 三 split 齐全（55k/5k/10k）；PyG `split="val"` 实跑可用；4 个 smoke 已产出。契约「官方数据解析失败且备选自构图不可用」未触发。 | 否 |
| 机制不可跑 / 恒等式不适用 | **否**。M0 在固定线性算子类 25 格残差 ≤9.88e-15；v2 `check_identity` 在真实管线逐 T 运行且 `sum_n_hit_rate=1.0`；R、A 固定非负线性。 | 否 |
| 方法 soundness 内在矛盾 / 组件冲突 | **否**。β*、膜电位解码、确定性两阶段、gauge 自洽；三个真实缺陷（mean 池化 1/n 稀释梯度、n 未 clip 到 T 致脉冲虚高、激活未 gauge 到 [0,θ]）**已发现并修复**，修复轨迹可由 smoke 的 F/pool/epochs/hidden 变化与 `vision_pipeline.py:88-91, 190-201, 241-244` 注释核对。 | 否 |
| 最近邻基线不可用 / 复现不可行 | **否**。核心横评臂（naive/qcfs/ftbc/tpp/parallel/ours）已实现并可跑；缺项（直训 SNN、Planetoid 锚点、DCGS/AdaFire/PASCAL/CS-QCFS）属契约已预留「无官方码或需重训的适配结果如实标注」的可修复缺口，不是「unavailable baseline」。 | 否 |
| 能耗主张不可证伪 / 诚信门 | **否（但为准 fatal 级入口条件）**。已写成可证伪假设、理论估算≠硬件实测、有 failure signal 与 claim adjustment rule、model 字段明写 `NOT a hardware measurement`。惟 `guidance-v2.md:116` stopping criteria 含「能耗估算口径不自洽时停止并回退到 P2/P3」，而实读口径确不自洽（B1）—— 其正确解读是「**进入 P2/P3 前必须闭合的入口条件**」，而非「阻止进入」，因为当前正在 P1B、修复不需新数据/新算力。 | 否（准 fatal 级条件） |
| evidence plan 不可信 | **否**。冻结 split、5 seeds、bootstrap R=5000、sign-flip 1000、BH q<0.05、test 隔离、trial ledger、`observed_finding` 不早于 P5A、负结果保留齐备。 | 否 |
| Novelty 坍塌为 fatal | **否**。v1 第三轮已判 F2「部分解决、降级为可修复弱点、非 fatal」、0 未解 fatal；v2 改组合与适配定位、novelty 门槛更低（用户明说不要求新定理）。组合/推论层未检索是置信度与边界问题（封顶 novelty 3），非 P1B 硬门 fatal。 | 否 |
| 算力 / 资源不可行 | **否**。子集 smoke 已本机 CUDA 实跑（66.87 s/臂）；3060 12GB ＋ 548 GB ＋ 已授权 4090；`execution-contract-v1.md` §5 明记 torchvision/skimage 不依赖。全量扩展需改代码（W8），属工程修复。 | 否 |
| novelty ≤2 高置信 / method ≤2 / experimental ≤2 无替代证据 / venue ≤2 / feasibility ≤2 | 分别 3 / 4 / 3 / 4 / 4，均不触发 `calibration.md` 数值 gate。 | 否 |
| No identifiable insight beyond known modules / Internal mechanism conflict | **不硬触发但临界**：「池化线性 ⇒ 恒等式迁移」提供薄但可辨识的洞察；`rho_mean≈0.9987` 与瓶颈矛盾属可修复错位；`strict-idea-review.md` 明令「do not translate mechanism under-specified into fatal」。 | 否（临界） |

**结论：无未解 fatal risk，满足进入 P2/P3 的唯一硬标准。** 但下列 B 段 3 条为**进入 P2/P3 前必须闭合的准 fatal 级条件**，C/D 段为可修复弱点与隔离项。

**B. 准 fatal 级、进入 P2/P3 前必须闭合（否则 P4 主表不可信；均可在无新数据/新算力下修复）**

- **B1 · 能耗核算口径不自洽，且已落盘 smoke 给出与「一定有优势」相反的信号**（最重）。
  - 口径：`_ann_macs`（`vision_pipeline.py:322-325`）计 ANN **一次前向全部层**（`E·F + N·F·H + E·H + N·H·C + N·C`）；`ac_ops`（`:295`）每个 T 步只累加 `ns·W2.shape[0] + ns·deg_mean·W2.shape[1]`，即**仅 hidden spikes × W2 与邻居聚合**，漏算第一层连续电流注入（`:275` `inst1 = B1`）、输出层 `R@Z + b2`、膜电位累加/重置；且 `ac_ops` 随 T 线性累积而 `ann_macs` 为常数 → T 越大比值越差。两侧分母不同，`energy_ratio_ann_over_snn` 不可直接解释。
  - 实读信号：`gpu_MNIST_seed0.json` energy 段 `ours_T1 1.6049× / T2 1.2958× / T4 0.8629× / T8 0.5077× / T16 0.2768×`；`smoke` 0.6878×、`smoke2` 0.3425×、`smoke3` 0.4215×。**全部已落盘预实验中该比值从未达到预注册「≥5×」，且在 conversion loss 最小的 T=16（2.0pp）处仅 0.28×（SNN 理论算术能耗约为 ANN 的 3.6 倍）**，直接命中契约 failure signal「理论算术能耗比 ANN 无优势（≤1×）」。用户预判「一定有优势」与已有信号相反。
  - 定性：这是**单 seed 小子集 smoke 值、非正式裁决**（`pipeline-state.json` 全 pending），故不判 fatal、不写成「已被证伪的结论」；但它意味着「实测裁决尚未完成」不能继续被表述为「优势待确认」，而应表述为「已有反例信号，须先统一口径再裁定」。若带着「一定有优势」预设或修改口径凑 5× 进入 P2/P3，会命中 `execution-contract-v1.md` §2/§9「不把用户预判的能耗优势写成已得结论」与契约 §8 S6 诚信门。
- **B2 · `rho_mean≈0.9987` 与核心瓶颈/新算子类声称矛盾**。契约 §Core Idea、§Mechanism-Level Rationale、§Theoretical Feasibility Audit 反复以「ρ_n 远离 1」为领域瓶颈与新算子类依据；`batch_graphs(sym_norm=True)`（`:101-104`）实施对称归一化，4 个 results JSON 全部 split 的 `rho_mean` 恒为 0.9987、`rho_max ≤ 1.1012`、`rho_std ≈ 0.0316`。实际算子类近似行随机，与 CNN 网格差异远小于契约声称。若不修正，「组合在新算子类上的可分析性」与「ρ_n 加权使 β*/膜电位解码收益更可观测」均失去实验基础。可修：关闭 `sym_norm`、或按契约 robustness 变体显式构造 ρ_n 网格（对称归一化/mean/sum 三算子），并在论文如实报告实际 ρ_n 分布。
- **B3 · 恒等式验证精度未达契约门槛 ＋ teacher 质量无护栏**。契约 Traceability（`:144`）要求恒等式残差「类内 <1e-12」；真实管线 float32 残差为 `3.242e-5(T1) → 6.407e-6(T16)`（`gpu_MNIST_seed0.json` identity 段），高 6–7 个数量级（M0 的 1e-15 是 float64 合成）。可修：全 float64 验证路径或重定义门槛并说明量级。teacher 方面：契约无「teacher 达到某精度门槛方可进主表」的护栏，而实跑 teacher 仅 68% 级、2000 图子集、单 seed，conversion loss 在 T=8 为 8.6pp、T=16 为 2.0pp，均远超 minimum「T≤8 ≤3.0pp」与 strong「≤1.5pp」。可修：设 teacher 验收门槛 ＋ 全量阶梯扩展 ＋ 统计功效预检。

**C. Fixable weaknesses（可修复，不改变中心主张）**

- W1 能耗主张：口径不对称（B1）＋ 45 nm 常数仅纯算术、不含 spike 路由/内存/膜电位状态/T 步时间；用单一标量外推「能耗优势」会高估。
- W2 「一定有优势」预判与已落盘反例信号并存；须防把预注册假设写成已得结论、防调口径凑 5×。
- W3 `rho_mean≈0.9987` 削弱新算子类论据（B2）。
- W4 数据集表不一致：`guidance-v2.md:61-62` 写 `data.dgl.ai/.../MNIST.pkl` 1.39 GB / CIFAR10.pkl 2.51 GB / CIFAR10 85–150 节点；实现与 `execution-contract-v1.md:32,51` 用 `data.pyg.org/datasets/benchmarking-gnns/{MNIST,CIFAR10}_v2.zip`（192,378,381 B ＋ 316,368,127 B ≈ 509 MB），MNIST 实跑约 70.7 节点/图（`N=141366 / G=2000`）。复现者可能拿错数据源。
- W5 QCFS 基线忠实度：`train_ann`（`:129-135`）有 `quantize_L`（docstring 明写「so the QCFS baseline trains its own source ANN」），但 `run_experiments.py:method_config` 对 qcfs 只返回 count readout ＋ beta=0，`run_one:66` 未传 `quantize_L`；实跑 `naive_T*` 与 `qcfs_T*` 的 `hidden_spikes`/`ac_ops` 完全相同（如 T1 均 22472 / 5279973.75），QCFS 数值退化为 naive。
- W6 「全套转换方法横评」打折：实现仅 6 种自实现方法；契约要求的技术族基线「直接训练的脉冲 GCN」、Traceability 的「Cora/CiteSeer/PubMed 复现 1028 shipped numbers 到 0.003pp」（`core-1028.snapshot.py:10-12` 记 1028 有 `wp0_reproduce.py` gate PASS 到 0.000–0.003 pp）、literature context 的 DCGS/AdaFire/PASCAL/CS-QCFS、以及 robustness 消融（3 归一化 / 2 池化 / 3 θ）与 error analysis，`run_experiments.py`（choices 仅 MNIST/CIFAR10、T==8 仅 4 个消融）均未覆盖。
- W7 恒等式真实管线精度 1e-5 量级 vs 契约 <1e-12（B3）。
- W8 CUDA 非确定性未量化：`core-1028.snapshot.py:34-38` 明写 CUDA 稀疏归约使 PubMed ANN 移动 `+0.69 pp`（7 seeds）、「larger than the effect sizes reported here, so the frozen protocol trains on CPU」；v2 `train_ann` 默认 `device="cuda"`、`run_experiments.py:134` 默认 cuda、`gpu` 结果 environment `"device":"cuda"`，note 仅称「报 std/CI」，**未做 device-pair 噪声量化、未固定 reduction、未改 CPU**。预注册「T≤4 优于最强基线 ≥1.0pp 且配对 bootstrap CI 下界 >0」与 0.69 pp 设备噪声同量级，裁定可信度受威胁。
- W9 全量扩展结构缺口：`batch_graphs`（`:67-111`）把整个 split 拼成**一个**块对角系统一次前向（`:162` 注释「full train batch」），无图级 minibatch/DataLoader；2000 图 `N=141366` 可跑，全量 55,000 图约 2.75M 节点，3060 12GB 有显存风险，扩展不是简单调 cap、需改代码。契约 §Scaling fallback「先子集再扩到可用规模」未说明此结构改动；4090 授权是回退。
- W10 池化措辞不一致：契约全篇写「全局平均池化 / linear global-mean pooling」，实际 `pool="sum"`（`:67,91`、`run_experiments.py:135`、gpu environment `"pool":"sum"`）—— 已修复 bug 未同步契约正文（恒等式对两者均线性成立，但影响 teacher 精度与 margin）。
- W11 证据工件口径一致性：用户任务描述「train 67.5% / val 68.2%」与磁盘 `gpu_MNIST_seed0.json` `0.689 / 0.668` 不一致（以文件为准）；MNIST 192,378,381 B zip 在当前目录树未直接见到（见 `Target venue/journal`）；`guidance-v2.md` 数据集表与实现数据源/尺寸/节点数不一致（W4）。
- W12 「直接复用 1028 实现」在代码层未兑现：契约 §Implementation notes 与 `contract-change-v1-to-v2.md` 称「复用 `core.py` 的 `train_ann`/`convert`/`check_identity`/`gauge_normalize`，仅新增 `vision_core.py`」；实读 `vision_pipeline.py` 为**独立重写**（未 import 1028 core、无 `vision_core.py`、gauge 为 percentile 缩放而非 1028 的 unit-spectral-gain `gauge_normalize`、`check_identity` 单层非逐层、无回归锚点）。方法命题级继承成立（module docstring 写明 lineage），代码复用级与回归锚点级未兑现；论文「组件继承逐条写明」时 gauge 一条须标为「改编」而非「复用」。

**D. 隔离项**：1028 成稿及其全部数值、图节点分类 `T≤8` 达 `ANN−1.5pp` 带内、`core-1028.snapshot.py` 中的 shipped numbers，均为「**用户提供的未公开先验（未发表、不充当公开证据）**」；`results/*.json` 为**单 seed 小子集预实验 smoke**，非已得正式结果，`pipeline-state.json` 全 pending。二者既非 fatal 也非 weakness 证据，不参与打分、不替代公开视觉实验。

### 评审任务五问 · 完整依据

**#1 是否存在未解 fatal risk 阻止进入 P2/P3？—— 否，0 条。**
见 A 段 9 行逐条核对表：数据、机制、soundness、基线、能耗可证伪性、evidence plan、novelty、算力、五条 `calibration.md` 数值 gate、两条临界 gate 全部不构成未解 fatal。**关键判定逻辑**：B1 的「能耗估算口径不自洽」命中契约 §Stopping criteria，但契约原文是「停止并**回退到 P2/P3**」，而当前**正在 P1B、尚未进入 P2/P3**，故其正确落点是「进入 P2/P3 前的入口条件」而非「阻止」；且该修复不需新数据/新算力（改 `ac_ops` 分层明细 ＋ 统一口径 ＋ 三口径敏感性即可）。B2/B3 同理为可修复错位。「0 正式实验」按用户硬要求与 `pipeline-state.json` 全 pending 不判 fatal。结论：**proceed conditional，可进 P2/P3**，附 H1–H8（见 `Recommendation`）。

**#2 组合与适配创新是否构成可辩护贡献？—— 有条件的可辩护（薄、系统实证型）。**
见 `Novelty delta` 特别回答。可辩护的是「统一横评 ＋ 恒等式迁移验证 ＋ 三重证据」这一证据包，不是新理论；四个侵蚀点（一行代数、证据包≠贡献、组合必要性未证、ρ_n≈1 削弱新算子类）使贡献偏窄。不要求新数学定理的定位成立，但「组合产生 prior-art 无法得到的新能力」不可声称。

**#3 能耗主张的最大风险是什么？最小修复/裁定实验？**
**最大风险**（三层，按严重度）：
1. **核算口径系统性偏向 SNN 且不对称**（B1/W1）：ANN 计全层一次、SNN 仅计脉冲层 AC 且随 T 线性累加；漏算第一层连续电流注入与输出层/膜电位。任何 `energy_ratio` 都是口径产物，不足以支撑「优势」结论。
2. **稀疏性未证、`ac_ops` 随 T 线性增长**：gauge 到 `[0,θ]` 后 `n=clip(round((inst1+beta)·T/θ),0,T)`（`:244`），每神经元 T 步最多 T 脉冲；实跑 `hidden_spikes` 随 T 从 T1 的 1,468,024 增至 T16 的 8,511,199，SNN AC 在 T=16 达 `1,999,773,375` vs ANN MAC `108,303,651`，能耗比降至 0.28×。契约 failure signal 已含「spike 密度未显著低于 ANN 激活密度」但尚无正式实测。
3. **预判与反例信号并存、诚信风险**（W2）：用户「一定有优势」、契约预注册「≥5×」，而全部已落盘 smoke 的 `energy_ratio_ann_over_snn` 为 `0.28×–1.60×`（gpu 5 个 T ＋ 3 个 smoke 各 1 值），从未达 5×，且在 conversion loss 最小的 T 上 <1×。若把预注册写成结论、或在 P2/P3 调口径凑 5×，命中诚信门。另 45 nm 常数（MAC 4.6 pJ / AC 0.9 pJ）是纯算术，不含 SNN 路由/内存/状态更新/T 步时间，外推「能耗优势」会高估；全程须标「理论算术能耗估算，非硬件实测」（代码 model 字段已做，论文须一致）。

**最小修复/裁定实验（纸面 ＋ 代码级、无需大规模算力，可先进 P2 执行）**：
1. **口径对齐**：SNN 侧补齐第一层输入（`A@X@W1`）、输出层 `R@Z` 与 bias、膜电位累加/重置，或改为「两侧同用 dense-equivalent 逐层操作计数 × 活动率」；`ac_ops` 输出分层明细而非单一标量。
2. **三口径敏感性**：在「仅脉冲层 AC（当前）/ 全层 AC / 含路由-内存代理」三种口径下分别给 `energy_ratio(T)` 曲线，看 5× 是否在所有合理口径下成立。
3. **绝对量同报**：spike 密度、SynOps、`total_spikes`、`ac_ops`、`ann_macs`、`wall-clock`、峰值显存（契约 §Metrics 已要求）；把比值放在「ANN−1.5pp 带内的最小 T」处，而非任意 T。
4. **可证伪裁定**：若任一合理口径下比值 ≤1×（契约 failure signal）或 spike 密度 ≥ ANN 激活密度 → 按 `Claim adjustment rule`（`guidance-v2.md:124`）收窄为「稀疏活动与 SynOps 代理指标」，**不得保留「能耗优势」结论**；保留全部负结果，不下调阈值、不挑 seed、不删负结果（`:123`）。
5. **标注纪律**：`observed_finding` 不早于 P5A、理论估算 ≠ 硬件实测、`expected_strong` 全标预注册。

**#4 teacher 68%（2000 图子集）是否足以支撑 conversion loss 比较？还缺什么？—— 不足以支撑有判别力的正式比较，但作为 P1B smoke 管线验证合格。**
- 实读：磁盘 `gpu_MNIST_seed0.json` `train 0.689 / val 0.668 / test 0.688`（`hidden=128, epochs=800, lr 默认 0.01, pool=sum, F=3, gauge_scale=0.5435`，split 2000/500/500）；用户任务描述写「67.5% / 68.2%」，**以文件为准**（W11）。smoke 轨迹 `0.235 → 0.263 → 0.297 → 0.689` 印证三个缺陷修复真实、工程自净能力成立。
- **为何不足**：① teacher 为 10 类图级分类的弱基线（未收敛到该 benchmark 的合理精度区间），conversion loss 以 teacher top-1 为分母基准，弱 teacher 的低 margin 与高方差会污染差值判别力与外部效度；② 2000 train / 500 test 子集、单 seed，统计功效低（500 test 上 proportion≈0.69 的 95% CI 半宽约 4pp 量级），预注册「T≤4 优于最强基线 ≥1.0pp 且配对 bootstrap CI 下界 >0」在这种噪声下难以达到；③ 契约无 teacher 验收门槛，退化 teacher 上的横评可机械满足「同 teacher」却失去意义；④ 实跑 `ours` conversion loss `T1 58.0 / T2 46.8 / T4 27.0 / T8 8.6 / T16 2.0 pp`，全部远超 minimum「T≤8 ≤3.0pp」与 strong「≤1.5pp」，`naive/qcfs/tpp` 约 57–58pp、`ftbc/parallel` 47–52pp，说明低 T 保真度与 teacher 质量共同未达标；⑤ `argmax_agreement` 仅 0.126(T1)→0.878(T16)，SNN 与 ANN 决策一致率在目标 T≤8 区间偏低。
- **按用户硬要求**：这些**不判 fatal**（0 正式实验是 P1B 正常状态，契约 §Expected Results 已备「保留负结果、检查数据对齐/阈值/池化/基线、加强基线、调参、补消融后重跑」路径）。
- **还缺**：(a) 全量 55k/5k/10k teacher 训练 ＋ **teacher 验收门槛**（用该 benchmark 已发表公开 GNN 数值作下界，须检索或用户提供，本评审不编造）；(b) 子集→全量的阶梯扩展与 5 seeds；(c) 统计功效预检（在计划样本量下 1pp 差值的 CI 宽度）；(d) Cora/CiteSeer/PubMed 回归锚点（W6，1028 有 gate PASS 到 0.003pp）；(e) CPU/CUDA device-pair 噪声量化（W8）；(f) 只在 val 选超参、test 仅最终一次（契约已有，实现 `calibrate_ftbc_beta` 在 val 网格搜索、符合）。

**#5 数据/基线/算力路径是否可执行？—— 子集 smoke 级可执行（已实跑），全量有条件可执行。**
- **数据**：官方 SuperPixel MNIST/CIFAR10 图已落盘、PyG 三 split 可用、8-NN 带权、10 类、官方 55k/5k/10k —— **可执行**。残留：W4 数据源/尺寸/节点数口径不一致（dgl pkl 表 vs pyg zip 实现）、MNIST 192 MB zip 未在目录树直接见到（但 processed 三文件齐全，非缺失）、W10 池化措辞。修：统一 `guidance-v2.md` 数据集表与实现/execution-contract，冻结 SHA-256 与图索引（契约已有）。
- **基线**：6 种方法已实现可跑、T 网格 `{1,2,4,8,16}`、FTBC beta 在 val 校准、消融 T=8 四臂、`check_identity` 逐 T —— **核心路径可执行**。残留：W5 QCFS 退化、W6 缺直训 SNN/Planetoid 回归锚点/DCGS/AdaFire/PASCAL/CS-QCFS/robustness 消融、W12 代码复用级未兑现。修：按契约把「无官方码或需重训」如实标注、补回归锚点与消融、QCFS 重训。
- **算力/工程**：3060 12GB ＋ CUDA 12.8 ＋ Python 3.13.13 / numpy 2.4.4 / PyG 2.8.0.post1 ＋ 548 GB 空闲、单臂 66.87 s（2000 图）、4090 已授权、torchvision/skimage 不依赖 —— **smoke 级可执行**。残留：W8 CUDA 非确定性、W9 无图级 minibatch 使全量 55k 扩展需改代码（不是简单调 cap）。修：按 1028 教训固定/量化设备噪声、实现图级 minibatch 或分块、全量转 4090 并登记 `infeasible-with-evidence` 回退。

---

## Per-expert reviewer notes:

> 5 个必需角色**独立**判断，先各自发言、后综合（依 `expert-panel.md` 与 `review-output-standards.md`）；每个角色的 Score tendency 与 Confidence 分开报，不强行制造一致、赞扬或拒稿；每块附 Score-change condition。全部为本 panel 独立判断，非真实审稿记录。

**Field Expert**
- Role: 领域专家（类脑计算 × ANN2SNN 转换 × 图视觉）
- Score tendency: 3 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: 中心问题「一整套图转换组合在自带图视觉分类上能否同时保精度/低时延/能耗」真实、具体、可测；用官方 SuperPixel 图（自带图结构）规避了 v1 的适用条件错位，是领域内干净的适配；组件继承逐条写明、能耗写成可证伪假设，诚实自限少见。
- Strict rejection-grade concern: **新算子类的实验基础不成立**。契约以「ρ_n 远离 1」为瓶颈与新类依据，但实跑 4 个 JSON 全部 `rho_mean≈0.9987`（对称归一化把行和拉回 1）。写完 related work 后，审稿人会问「这个算子类与 ρ≈1 的 CNN 网格差在哪、图结构视觉表示的部署普遍性证据在哪」。M0 只在合成随机 A 上验证，未答。
- Anchor: `guidance-v2.md` §Core Idea / §Mechanism-Level Rationale；`vision_pipeline.py:101-104`；`results/gpu_MNIST_seed0.json` `graph_stats`；`m0-results.json` P6。
- Why this matters: 决定 Problem importance 能否从 3 升 4，也决定「组合在新算子类上」是否站得住。
- Fatal risk if any: 无独立 fatal；B2 为进入 P2/P3 前必须闭合的准 fatal 级可修复错位。
- Most valuable repair or pivot: 关闭 `sym_norm` 或按契约 robustness 变体显式构造 ρ_n 网格，给出「非行随机算子在图视觉中普遍存在」的**公开**证据，并在论文如实报告实际 ρ_n 分布。
- Score-change condition: 上述公开证据 ＋ ρ_n 受控网格上的误差分解落地 → 3→4；不承诺。
- Development-potential note: 中；ρ_n 修正可提升主轴，不消除组合 novelty 薄的问题。

**Method Expert**
- Role: 方法专家（误差分析 / 机制正确性 / 效率核算）
- Score tendency: 4 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: 核心代数机制自洽且已实跑：M0 在固定线性算子类 25 格恒等式残差 ≤9.88e-15、β* 与 ρ 无关、Hoeffding 上界 0 违反、确定性两阶段 Σs=n/零方差（v1 合成）；v2 真实管线 `sum_n_hit_rate=1.0` 逐 T 成立、恒等式残差随 T 单调下降（`3.24e-5→6.41e-6`）、三个真实缺陷（mean 池化稀释、n 未 clip、未 gauge）已发现并修复，代码注释可核。R 线性 ⇒ 恒等式 `R A (E₁W₂)` 精确成立，是最扎实的机制进步。
- Strict rejection-grade concern: **效率核算口径不自洽，且数值验证 ≠ 定理/判据成立**。`_ann_macs` 计 ANN 全层一次，`ac_ops` 只累加脉冲层 AC 且随 T 线性增长，漏算第一层连续电流注入与输出层/膜电位 —— `energy_ratio_ann_over_snn` 是口径产物。另：真实管线 float32 恒等式残差 1e-5 量级 vs 契约「<1e-12」；gauge 为 percentile 缩放而非 1028 的 unit-spectral-gain `gauge_normalize`，契约「复用 gauge_normalize」在代码层未兑现；契约自列 critical failure mode「图级池化改变 margin 结构使 β* 不再最优」未闭合。
- Anchor: `vision_pipeline.py:275, 295, 322-336`；`results/gpu_MNIST_seed0.json` energy/identity 段；`contracts/core-1028.snapshot.py:251-288`；`guidance-v2.md:188, 144`；`m0-results.json` meta「no training, no accuracy claim」。
- Why this matters: 数值/代数 soundness 已闭合，但效率核算 soundness、恒等式精度口径、gauge 归属未闭合；一个以「三重证据」为贡献的 idea，其能耗一维不可直接解释会直接被审稿人抓住。
- Fatal risk if any: 无独立 fatal；B1/B3 为准 fatal 级入口条件。
- Most valuable repair or pivot: 统一 ANN/SNN 操作计数口径并输出分层明细；float64 验证路径把图级残差压到 1e-12 内（或重定义门槛）；把 gauge 明确标为「改编」；补「一般 A 下图级 margin 下 β* 最优性」的解析或反例条件。
- Score-change condition: 口径统一 ＋ 残差达标 ＋ β* 图级最性闭合 → 4→5（本维）；反向则 4→3；不承诺。
- Development-potential note: 中—高；纸面/代码为主、无算力成本，最可修复。

**Experiment Expert**
- Role: 实验专家（证据设计 / 基线 / 可行性 / 统计）
- Score tendency: 3 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: evidence plan 设计完整：冻结官方 split、5 seeds、配对 bootstrap R=5000、sign-flip 1000、BH q<0.05、test 隔离、trial ledger、逐组件消融、恒等式残差、ANN/理论能耗对照、Traceability 表齐备；M0 ＋ 4 个 smoke JSON 证明「可跑路径」已过（66.87 s/臂）。按用户硬要求，**不把 0 正式实验判 fatal**。
- Strict rejection-grade concern: 四处**可执行性定义**缺口叠加：(a) QCFS 未传 `quantize_L`，实跑 `naive_T*` 与 `qcfs_T*` 的 `hidden_spikes`/`ac_ops` 完全相同，基线数值退化（W5）；(b) 缺直训脉冲 GCN、Planetoid 回归锚点、DCGS/AdaFire/PASCAL/CS-QCFS、robustness 消融与 error analysis（W6）；(c) `core-1028.snapshot.py:34-38` 记 CUDA 稀疏归约使 ANN 移动 +0.69 pp「larger than the effect sizes」，而 v2 默认 cuda、未做 device-pair 噪声量化，预注册「≥1.0pp 且 CI 下界>0」与设备噪声同量级（W8）；(d) teacher 68%/2000 图子集、恒等式残差 1e-5、能耗 smoke 反例（0.28×–1.60×）使「主表能否改信」存疑。阴性结果（能耗 ≤1×、conversion loss 超标）本身会直接裁定核心假设。
- Anchor: `run_experiments.py:29-52, 66, 107-118, 126-137`；`results/*.json`；`core-1028.snapshot.py:34-38`；`guidance-v2.md` §Metrics / §Required Ablations / §Expected Results；`pipeline-state.json` 全 pending。
- Why this matters: plan 可信但含「基线忠实度 / 统计可信度 / 精度门槛 / 能耗口径」四类可执行性缺口；若不先闭合，P4 主表不可信。
- Fatal risk if any: 无独立 fatal（按硬要求不把零实验判 fatal）。
- Most valuable repair or pivot: 按 H1–H8 补 QCFS 重训、回归锚点、device-pair 噪声量化、teacher 门槛、能耗口径；报告 conversion loss–T 曲线、κ/ρ_n 分桶误差、spike 密度、三口径 energy_ratio(T)；第 0 批复现关键基线。
- Score-change condition: 上述定义补齐 ＋ 5 seeds 全量横评支持判据 ＋ 能耗口径自洽 → 3→4（本维）；预注册目标被系统性推翻 → 3→2；不承诺。
- Development-potential note: 高；最明确、最可执行的补齐路径。

**AC / Venue Expert**
- Role: AC / venue 专家（贡献品味 / 匹配 / 讨论后存活）
- Score tendency: 4 / 5
- Confidence: 3 / 5
- Best possible argument for the idea: 主动对齐 Q1–Q2 期刊档（TNNLS / Neural Networks）、贡献收敛为「组合适配 ＋ 统一横评 ＋ 三重证据」单一主轴、理论能耗与硬件实测严格区分、1028 隔离标注、冻结协议与停止回退对期刊可审计性加分；`expected_strong` 全标预注册、`observed_finding` 不早于 P5A，符合期刊对负结果诚实性的期待。
- Strict rejection-grade concern: (a) 贡献仍是「适配 / 横评 / 能耗」三块并列，带 benchmark 味，混合评审中可能被读成应用/比较短文而非 main-track 理论贡献；(b) 核心结果全部预注册未实测、能耗已有反例信号、`rho_mean≈1` 削弱新类论据，能否 survive discussion 存疑；(c) 未核验目标期刊当年官方 policy / review form（契约自认 `venue policy 未核验`），按通用 contribution taste 推理；(d) 若能耗优势被证伪且横评无系统优势，只剩「统一横评」这一较薄落点。
- Anchor: `guidance-v2.md` §Paper Story / §Story Strength Audit / §Figure-Table 第 134 行；`execution-contract-v1.md` §4；v1 第三轮 AC note。
- Why this matters: venue 对齐消除了 mismatch，但 readiness 仍低，二者不可混为一谈。
- Fatal risk if any: 无独立 fatal。
- Most valuable repair or pivot: 结构上把三块贡献绑定为「一个可分析框架贯穿横评与能耗」的单一叙事；成文前核验当年官方 policy；预备 honest fallback 表述。
- Score-change condition: 单一叙事落地 ＋ 官方 policy 核验 ＋ 核心结果兑现 → 维持 4（本维已接近该档上限）；不承诺升 5。
- Development-potential note: 中。

**Skeptical Prior-Art Expert**
- Role: 怀疑型 prior-art 专家（novelty 坍塌 / 命名掩盖 / 是否已属已知）
- Score tendency: 2 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: 全文不声称发明任何已占组件、逐条写明继承（Deng&Gu、QCFS/FTBC、Dual-Phase、TPP、PASCAL、One-Spike SNN）、禁用掩盖性命名、把 1028 标为未公开先验、能耗写成可证伪假设、M0/smoke 数值自洽未编造；「自带图视觉数据集 ＋ 全套横评 ＋ ANN/能耗对照」是 v1 主卡没有的证据包层增量。
- Strict rejection-grade concern: **最强「this is already known」objection 在 v2 后未被削弱**：把 Deng&Gu 递推里的归一化矩阵换成一般 A、`A·1=ρ_n·1` 立刻给出 ρ_n 加权项，配合 QCFS 零期望偏置就是全部；「池化线性 ⇒ 恒等式不破坏」是一行代数；One-Spike SNN 已跨 CNN＋GCN、Dual-Phase 已有恒等式＋膜电位解码，组合到超像素图 ＋ 加横评，仍是「已知组件 ＋ 新数据集 ＋ 新比较表」。追加：(a) 组合/推论层 novelty 未经针对检索；(b) 实跑 `rho_mean≈0.9987` 使「新算子类」论据更弱；(c) `results` 中 `naive` 与 `qcfs` 数值相同，横评「全套」打折；(d) 成稿「用户提供的未公开先验（未发表、不充当公开证据）」中已给出 margin 定理与 ρ-不变解释，须澄清「本文新推论」与「内部已有结果」边界，避免自我重复定位。
- Anchor: 用户契约 §Citation Scope / v1 三轮 closest-work 表；`vision_pipeline.py:6-13` docstring；`results/gpu_MNIST_seed0.json` methods；`m0-results.json` P2/P3；Search basis 组合层边界。
- Why this matters: 决定 novelty 是否 ≤2 与是否「beyond applying known modules」；本角色是压住 novelty 不升分的主因。
- Fatal risk if any: F2 仍是最重的一项，但本角色认同「已降级为可修复弱点」而非 fatal（v1 第三轮判定延续）。
- Most valuable repair or pivot: 对组合本身做公开检索（通用关键词、不粘贴私有措辞）；给出「组合在新算子类上产生 prior-art 给不出的可测预测」的证据（受控 ρ_n 网格 ＋ 逐组件消融 ＋ 横评系统优势）；全文一致不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」。
- Score-change condition: 组合层检索无近邻 ＋ 非平凡性/系统优势证据成立 → 2→3；命中近邻或组合坍缩 → 维持 2 并回潮 F2；不承诺。
- Development-potential note: 低—中。

**Panel Synthesis**（依 `expert-panel.md` / `review-output-standards.md`，不平均掉致命弱点）

```text
Agreement: 五位专家一致认为 (1) v2 相对 v1 的可执行性进步真实（自带图数据规避适用条件错位、代码/数据/smoke 实跑就位、三缺陷已修、0 未解 fatal）；(2) 但核心结果全部预注册未实测，且本轮实读发现三处实现—声称错位（能耗核算口径不自洽、rho_mean≈1 与新算子类矛盾、恒等式精度/teacher 门槛未闭合）；(3) 一致认为不应 abandon（中心主张可测、修复路线可命名）；(4) 一致认为按 P1B 硬门「无未解 fatal」可 proceed 进 P2/P3，但须附入口硬条件。
Disagreement: Method(4) 与 AC(4) 评「核心代数机制自洽 / venue 对齐」；Field(3)、Experiment(3) 评「问题代表性 / 证据包可执行性缺口」；Skeptical(2) 评「novelty 薄、组合层未检索」。分歧来自「评哪个轴」，不是对事实的分歧；未强行制造一致或赞扬。
Strongest accept axis / Decisive accept axis: 恒等式 `R A (E₁W₂)` 在图级线性读出上精确成立（M0 1e-15 ＋ 实跑 sum_n_hit_rate=1.0）＋ 自带图视觉数据集规避 v1 适用条件错位 ＋ 冻结协议/统计/诚实边界，构成一个可复算、可审计、自限清晰的 Q1–Q2 增量系统实证契约。
Strongest reject axis / Decisive reject axis: 组件全继承 ＋ 「池化线性」洞察为一行代数 ＋ rho_mean≈0.9987 使新算子类论据不成立 ＋ 能耗口径不自洽且 smoke 已给反例信号（0.28×–1.60×、从未达 5×）＋ 全套横评打折（QCFS 退化为 naive）；若组合层检索命中近邻或 P4 主表无系统优势，novelty 回 2、整体回约 3.0–3.1。
Score-relevant uncertainty / Unresolved evidence: 统一口径下的 energy_ratio(T) 与 spike 密度；5 seeds 全量 conversion loss–T 曲线与配对 CI/BH；ρ_n 受控网格误差分解；全量 teacher 与 1028 回归锚点；device-pair 噪声量化；组合层公开检索；目标期刊当年官方 policy。
Most valuable next evidence: 先做纸面/代码级：统一能耗核算口径 ＋ 三口径敏感性（B1）、修正 ρ_n 算子类（B2）、float64 恒等式验证 ＋ teacher 验收门槛（B3）；再做 5 seeds 子集横评（含 QCFS 重训、device-pair 噪声）裁定 conversion loss 与能耗；最后全量扩 4090 ＋ 组合层检索。
Final calibrated stance / Panel-calibrated recommendation: ccf-idea-reviewer = pivot-with-rescue-route（与加权 3.3 落在 calibration 3.0–3.6 段一致）；P1B 硬门 = proceed（conditional，带 H1–H8）。
```

---

## Rubric scores:

权重取 `rubric.md` 默认表（合计 100），未作调整（无官方 venue review form 要求调整）。**标尺按 Q1–Q2 期刊档**；**分数与置信度分列**；聚焦「预实验可执行性与风险修复条件」，不以「0 正式实验」压分。

| Dimension | Weight | Score (1-5) | Confidence (1-5) | Deduction / evidence basis | Repair condition |
| --- | ---: | ---: | ---: | --- | --- |
| Problem importance | 12 | 3 | 4 | 图结构视觉 ＋ 低时延转换 ＋ 能效对照是真实交叉缺口，自带图 benchmark 比 v1 人为构造代表性强；但「ρ_n 远离 1」瓶颈被实跑 `rho_mean≈0.9987` 抵消，新算子类/部署普遍性无公开证据 | 关闭 `sym_norm` 或显式 ρ_n 网格 ＋ 非行随机算子普遍性的公开证据 ＋ 如实报告实际 ρ_n |
| Novelty against likely prior work | 14 | 3 | 3 | 组合与适配定位、组件全继承、「池化线性」为一行代数、证据包为薄增量；组合/推论层 `not searched`，依 `strict-idea-review.md` 封顶 3 | 组合层公开检索无近邻 ＋ 非平凡性/系统优势证据；三者齐备方可升 4 |
| Conceptual innovation | 12 | 3 | 3 | 「池化线性 ⇒ 恒等式迁移」干净但接近 obvious；「ρ_n 使 β*/膜电位收益更可观测」因 ρ≈1 未成立；组合必要性未证 | 受控 ρ_n 网格给出 prior-art 给不出的可测预测 ＋ 逐组件消融证明非冗余 |
| Method soundness | 14 | 4 | 4 | **给 4 依据**：M0（float64 合成，25 格 ≤9.88e-15）＋ 真实管线 `sum_n_hit_rate=1.0` ＋ 三缺陷已修 ＋ 恒等式残差随 T 单调下降，核心代数子集已兑现。**仍扣 1**：效率核算口径不自洽（B1）、真实管线残差 1e-5 未达 <1e-12、gauge 为改编非复用、契约自列「图级池化改变 margin 使 β* 不再最优」未闭合 | 统一能耗口径 ＋ float64 验证 ＋ 图级 margin 下 β* 最性解析/反例 |
| Elegance and simplicity | 8 | 3 | 4 | 6 类组件（恒等式/β*/膜电位/ρ_n/两阶段/池化）偏拼盘；`run_experiments.py` T==8 仅 4 个消融，膜电位解码 vs 确定性计数冗余未隔离；组合必要性未证 | 补 A/B 变体与 robustness 消融、删冗余、把三块贡献绑定单一叙事 |
| Feasibility under resources | 8 | 4 | 4 | **给 4 依据**：CIFAR10 zip 316,368,127 B ＋ MNIST processed 三 split 落盘、PyG `split="val"` 实跑可用、代码完整、4 个 smoke 本机 CUDA 实跑（66.87 s/臂）、3060 12GB ＋ 548 GB ＋ 授权 4090、torchvision/skimage 不依赖。**仍扣 1**：W4 数据源/尺寸口径不一致、W9 无图级 minibatch 使全量扩展需改代码、W8 CUDA 非确定性未量化 | 统一数据口径、实现图级 minibatch/分块、固定或量化设备噪声、全量转 4090 并登记回退 |
| Experimental convincibility | 10 | 3 | 4 | 证据包设计完整（冻结 split/5 seeds/bootstrap/BH/test 隔离/消融/恒等式/ANN 能耗对照）且 M0 ＋ smoke 验证可跑路径，**按用户硬要求不因 0 正式实验判 2**。**扣到 3**：W5 QCFS 退化为 naive、W6 缺直训 SNN/Planetoid 锚点/robustness 消融、W8 设备噪声与 ≥1.0pp 效应同量级、teacher 68% 子集且 conversion loss T8 8.6pp/T16 2.0pp 远超门槛、恒等式 1e-5 未达 1e-12、B1 能耗口径不自洽且 smoke 反例 | 补 H1–H8 入口条件；5 seeds 全量横评；conversion loss–T、ρ_n 分桶、三口径 energy_ratio(T)、device-pair 噪声 |
| Venue and audience fit | 8 | 4 | 3 | 主动对齐 TNNLS/Q1–Q2 档、理论能耗≠硬件实测、1028 隔离标注、冻结协议与停止回退对期刊可审计性加分。**仍扣 1**：三块贡献并列带 benchmark 味、核心结果预注册未实测、当年官方 policy/review form 未核验 | 单一叙事绑定 ＋ 核验当年官方 policy ＋ 预备 honest fallback |
| Timeliness and topic heat | 6 | 3 | 4 | 方向热但 2024/2025 prior-art 密集（FTBC'24、Dual-Phase'24、TPP'25、Parallel'25、DCGS'25、AdaFire'25、PASCAL'25、CS-QCFS'25、One-Spike SNN'24/25）；组合层未检索，scoop 风险未消 | 「为什么是现在」绑定 ρ_n 真实普遍性公开证据 ＋ 组合层针对检索 |
| Risk-adjusted acceptance potential | 8 | 3 | 4 | 0 未解 fatal、可执行路径、诚实边界已分别计入 Method/Feasibility/Venue，避免重复计分；但 novelty 薄且未检索、核心结果预注册未实测、能耗已有反例信号、`rho_mean≈1` 削弱新类论据、QCFS 退化、口径不自洽 —— 多个决策相关 gap 叠加，严格审稿人主拒稿轴仍是「组件都是别人的 ＋ 洞察是一行代数 ＋ 能耗是理论估算」 | G3 类解析闭合 ＋ 组合层检索无命中 ＋ P4 横评显示系统优势与稳健能耗结论，三者齐备方可升档 |

### 每个 ≤3 分项的扣分明细（依 `rubric.md` Deduction Format 与 `review-output-standards.md`；四项齐全 ＋ Why / Development effect）

本表共 **7 个 ≤3 分项**（Problem / Novelty / Conceptual / Elegance / Experimental / Timeliness / Acceptance），预期变化均为**条件性、非承诺**。

**Problem importance（3 / conf 4）**
- 扣分理由：把大而难的问题换成小而具体的问题未提升绝对重要性；契约「ρ_n 远离 1 的非行随机新算子类」被 `rho_mean≈0.9987` 抵消，新类代表性无公开证据。
- 证据基础 / Anchor：`guidance-v2.md` §Core Idea / §Mechanism；`vision_pipeline.py:101-104`；4 个 results JSON `graph_stats`；`m0-results.json` P6。
- 为什么重要：Q1–Q2 期刊要求瓶颈「真实且被本文真正检验」；写完 related work 后若 gap 只剩「没人系统测过该组合」，会被判窄诊断。
- 修复条件：给「非行随机算子在图视觉中普遍存在」的公开证据 ＋ 显式 ρ_n 受控网格 ＋ 如实报告实际 ρ_n。
- 预期分数变化：条件性 3→4，Overall 约 +0.12；不承诺。
- Development-potential effect：中。

**Novelty against likely prior work（3 / conf 3）**
- 扣分理由：组合与适配定位下组件全继承，「池化线性」洞察为一行代数，证据包为薄但真实的增量；组合/推论层 `not searched`，依 `strict-idea-review.md` 封顶 3。
- 证据基础 / Anchor：Closest prior art table 8 条；`Novelty delta`；`m0-results.json` P2/P3；`rubric.md`「do not score above 3 when closest work not checked」。
- 为什么重要：决定 F2 是否回潮；`calibration.md`「Novelty ≤2 高置信」当前不触发但反向条件会拉回。
- 修复条件：组合层公开检索无近邻 ＋ 非平凡性证明/系统优势证据 ＋ ρ_n 受控网格的可测新预测，三者缺一维持 3。
- 预期分数变化：条件性 3→4（三条件齐备）Overall 约 +0.14；反向 3→2 约 −0.14；不承诺。
- Development-potential effect：低—中。

**Conceptual innovation（3 / conf 3）**
- 扣分理由：「池化线性 ⇒ 恒等式迁移」为干净但接近 obvious 的观察；「非行随机 ρ_n 使收益更可观测」因 `rho_mean≈0.9987` 未成立；组合必要性未被消融证明。
- 证据基础 / Anchor：`guidance-v2.md` §Core Idea / §Mechanism；`results/*.json` `rho_mean`；`rubric.md`「penalize pure module recombination unless combination creates a new capability or explanation」。
- 为什么重要：若组合不带来 prior-art 给不出的解释或预测，概念创新读成「把已知组件拼到新数据集」。
- 修复条件：受控 ρ_n 网格给可测新预测 ＋ 逐组件消融证明非冗余 ＋ 澄清与 1028 未公开先验的边界。
- 预期分数变化：条件性 3→4，Overall 约 +0.12；不承诺。
- Development-potential effect：中。

**Elegance and simplicity（3 / conf 4）**
- 扣分理由：6 类组件拼盘；实现只做 4 个消融，膜电位解码 vs 确定性计数冗余未隔离；「适配/横评/能耗」三块未结构化绑定。
- 证据基础 / Anchor：`vision_pipeline.py` METHODS；`run_experiments.py:107-118`；`guidance-v2.md` §Required Ablations；`rubric.md` elegance「necessary parts and coherent insight」。
- 为什么重要：冗余组件会被核减为实现细节，削弱「组合必要性」。
- 修复条件：补 A/B 变体与 robustness 消融、删冗余、绑定单一叙事。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；不承诺。
- Development-potential effect：低—中。

**Experimental convincibility（3 / conf 4）**
- 扣分理由：证据包设计完整且可跑路径已过，但四类可执行性缺口叠加 —— QCFS 实跑退化为 naive（W5）、缺直训 SNN/Planetoid 锚点/robustness 消融（W6）、CUDA 设备噪声 +0.69 pp 与 ≥1.0pp 效应同量级且未量化（W8）、teacher 68%/2000 图子集且 conversion loss T8 8.6pp/T16 2.0pp 远超门槛 ＋ 恒等式 1e-5 未达 1e-12 ＋ 能耗口径不自洽且 smoke 反例（B1/B3）。**不因「0 正式实验」扣到 2**（用户硬要求）。
- 证据基础 / Anchor：`run_experiments.py`；`results/*.json`；`core-1028.snapshot.py:34-38`；`guidance-v2.md` §Expected Results / §Traceability；`pipeline-state.json` 全 pending。
- 为什么重要：该维反映「能否产出改变 reviewer 信念的证据」；缺口不闭合则 P4 主表不可信。
- 修复条件：H1–H8 入口条件 ＋ 5 seeds 全量横评 ＋ conversion loss–T/ρ_n 分桶/三口径 energy_ratio(T)/device-pair 噪声同报。
- 预期分数变化：条件性 3→4（补齐且曲线支持）Overall 约 +0.10；预注册目标被系统性推翻 → 3→2；不承诺。
- Development-potential effect：高（最明确的可执行补齐路径）。

**Timeliness and topic heat（3 / conf 4）**
- 扣分理由：方向热但 2024/2025 prior-art 密集，组合层未检索、scoop 风险未消；「为什么是现在」缺 ρ_n 真实普遍性的公开量化。
- 证据基础 / Anchor：契约 §Citation Scope 的 venue/year 列表；`rubric.md` timeliness「risk of saturation」；Search basis 组合层边界。
- 为什么重要：密集 prior art 提高 novelty 坍塌与 scoop 风险。
- 修复条件：把「为什么是现在」绑定公开普遍性证据 ＋ 组合层针对检索。
- 预期分数变化：条件性 3→4，Overall 约 +0.06；不承诺。
- Development-potential effect：低。

**Risk-adjusted acceptance potential（3 / conf 4）**
- 扣分理由：0 未解 fatal、venue 对齐、M0/协议/实跑兑现已分别计入其他维（不重复计分）；但 F2 的 novelty 核心质疑未消解、核心结果预注册未实测、能耗已有反例信号、`rho_mean≈1` 削弱新类论据、QCFS 退化、口径不自洽叠加。`calibration.md` 五条数值 gate 均不触发，两条临界 gate（beyond-known-modules、internal mechanism conflict）处于临界。
- 证据基础 / Anchor：`Serious blockers` A/B/C/D；Fatal gates 清单；Panel Synthesis；Skeptical/Experiment 两位专家 notes。
- 为什么重要：该维是叠加效应而非重复计罚；严格审稿人主拒稿轴仍是「代数展开 ＋ 组件继承 ＋ 理论能耗」。
- 修复条件：G3 类解析闭合 ＋ 组合层检索无命中 ＋ P4 横评显示系统优势与稳健能耗结论，三者齐备方可升档。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；若 F2 回潮为 fatal → 3→2 约 −0.08；不承诺。
- Development-potential effect：中（依赖 P4 结果）。

> `Method soundness`(4)、`Feasibility under resources`(4)、`Venue and audience fit`(4) 为 >3 项，不触发明细块要求；其扣分 / 修复条件已在上方表格给出。

---

## Weighted final score:

依 `rubric.md` / `calibration.md`：`weighted_score = sum(score_i × weight_i) / 100`

```text
12×3 = 36   (Problem importance)
14×3 = 42   (Novelty against likely prior work)
12×3 = 36   (Conceptual innovation)
14×4 = 56   (Method soundness)
 8×3 = 24   (Elegance and simplicity)
 8×4 = 32   (Feasibility under resources)
10×3 = 30   (Experimental convincibility)
 8×4 = 32   (Venue and audience fit)
 6×3 = 18   (Timeliness and topic heat)
 8×3 = 24   (Risk-adjusted acceptance potential)
合计 = 330 → 330 / 100 = 3.30 → 3.3（保留一位小数）
```

`**Overall:** 3.3`（1–5 加权尺度；可选 1–10 尺度 ≈ 6.6）

```text
Current conference readiness: low
Development potential: medium
```

**分数与推荐的一致性说明**：3.30 → 3.3 落在 `calibration.md` **3.0–3.6 段 → `pivot-with-rescue-route`**，由分数段直接得出，不依赖 fatal gate 压顶（五条数值 gate 均不触发、两条临界）。不取 `revise`（需 3.7+，即 novelty 站稳 ＋ 核心结果实证 ＋ 能耗口径闭合，未达）；不取 `accept-to-develop`；不取 `needs-literature-search`（组件层按用户指令标 `searched`、组合层未检索作边界/置信度处理，沿用 v1 第三轮）；不取 `abandon`（中心主张可测、H1–H8 路线可命名，依 `strict-idea-review.md` 不满足「无可测主张且无重构」）。

**与 v1 第三轮 `**Overall:** 3.4` 的关系（不攀比、不抬分、不刻意压分）**：两轮分数**不可直接比较** —— 不同场景（v1 冻结 KNN ViG vs v2 自带图 SuperPixel）、不同证据边界（v1 无 v2 的代码与实跑工件可读）、不同评审 lens（v1「guidance 契约就绪度」vs 本轮「P1B 预实验可执行性」）。本轮 3.3 的取值逻辑：
- v2 的**真实进步**体现在 `Method soundness 4`（M0 ＋ 实跑兑现核心代数子集、三缺陷已修）、`Feasibility 4`（数据/代码/smoke/3060/4090 就位）、`Venue 4`（Q1–Q2 对齐 ＋ 诚实边界），以及**门禁结论「0 未解 fatal、可 proceed」**；
- 本轮把 v1 当时**无法看到**的实现层风险计入扣分：`rho_mean≈0.9987` 与瓶颈矛盾（Problem/Conceptual）、能耗核算口径不自洽 ＋ smoke 反例 ＋ QCFS 退化 ＋ CUDA 噪声（Experimental）、恒等式精度/teacher 门槛（B3）；
- 没有「因是修订版默认更高」的项，没有 +2 跳升，`Novelty / Conceptual / Acceptance` 三个压档维刻意留在 3；`Experimental convincibility` 按用户硬要求**不因 0 正式实验压到 2**（给 3，扣在实现层缺口）。

**Fatal gates 生效清单（`calibration.md`，逐条核对）**：
- Novelty ≤2 高置信 → **不触发**（3 / conf 3）。
- Method soundness ≤2 → **不触发**（4）。
- Experimental convincibility ≤2 且无替代证据 → **不触发**（3，且 M0 实跑 ＋ evidence plan 完备）。
- Venue fit ≤2 → **不触发**（4）。
- Feasibility ≤2 → **不触发**（4）。
- No identifiable insight beyond applying known modules → **不硬触发但临界**（「池化线性」提供薄但可辨识洞察；组合层未检索、`rho_mean≈1` 削弱新类论据）。
- Internal mechanism conflict → **不硬触发但临界**（能耗口径不自洽、ρ_n 实现与声称错位，均可修复）。
- Novelty unknown 且无 closest-work search → **不适用**（组件层 `searched`；组合层未检索已降置信度并封顶 novelty 3，按用户指令不升级为 `needs-literature-search` 推荐）。

---

## Score-change conditions:

全部为**条件性、非承诺**（依 `privacy-and-evidence.md`，不保证分数变化 / 录用概率 / 审稿人行为）。按影响排序：

| 条件（可测） | 影响维度 | 预期分数变化（条件性区间） |
|---|---|---|
| C1 统一 ANN/SNN 操作计数口径并输出分层明细；在「仅脉冲层 / 全层 / 含路由-内存代理」三口径下给 `energy_ratio(T)`；报告 spike 密度、SynOps、`total_spikes`、`ac_ops`、`ann_macs`、wall-clock；在等精度 T 上裁决 | Method / Experimental / Acceptance | 口径自洽后 Method 4→5（若全过）、Experimental 3→4；Overall 约 +0.24 |
| C2 关闭 `sym_norm` 或按 robustness 变体显式构造 ρ_n 受控网格，给「非行随机算子在图视觉中普遍存在」的公开证据，并如实报告实际 ρ_n 分布 | Problem / Conceptual / Novelty | Problem 3→4、Conceptual 3→4；Overall 约 +0.24 |
| C3 补 QCFS 重训（`quantize_L`）、直训脉冲 GCN、Planetoid 回归锚点、robustness 消融、device-pair 噪声量化；5 seeds 全量横评给 conversion loss–T 配对 CI/BH | Experimental / Acceptance | Experimental 3→4（若曲线支持）、Acceptance 3→4；Overall 约 +0.18 |
| C4 全量 teacher ＋ teacher 验收门槛 ＋ 统计功效预检；float64 验证路径把图级恒等式残差压到 <1e-12（或重定义门槛并说明量级） | Method / Experimental | 辅助 C1/C3；Overall 约 +0.05~+0.10 |
| C5 组合/推论层公开检索无近邻命中 ＋ 逐组件消融证明组合必要性（prior-art 给不出的可测预测） | Novelty / Conceptual / Confidence | Novelty 3→4；Overall 约 +0.14；反向 3→2 |
| C6 结构上把「适配 / 横评 / 能耗」绑定为单一叙事 ＋ 核验当年官方 policy / review form | Venue / Elegance | Venue 维持 4、Elegance 3→4；Overall 约 +0.08 |
| C7 统一数据源/尺寸/节点数口径（W4）、池化措辞（W10）、teacher 数值与 zip 记录口径（W11）、gauge 归属标注（W12） | Evidence integrity（不直接改维度分） | 消除复现核验假阳性；不承诺分数变化 |

**反向条件（会坐实 fatal / 降分，是「不因修订版默认更高」的护栏）**：
- 若组合层检索命中近邻（已有工作给出「超像素图 ANN2SNN 转换统一横评 ＋ 能耗对照」或 ρ_n 加权 margin 偏置）→ Novelty 3→2、F2 回潮，整体回约 3.0–3.1，重新触发 novelty / beyond-modules 两条 gate。
- 若统一口径后 energy_ratio 在所有合理口径下仍 ≤1×、或 spike 密度 ≥ ANN 激活密度 → 按 `Claim adjustment rule` 收窄为「稀疏活动与 SynOps 代理指标」，「三重收益」降为「二重」，Acceptance 回落；不得调口径凑 5×。
- 若 P4 全量横评显示 1028 组合无系统优势（T≤4 未优于最强基线 ≥1.0pp 或 CI 下界 ≤0）→ pivot 为纯 benchmark 故事（契约 §Story Strength Audit 已备用）。
- 若 ρ_n 受控网格显示「非行随机」论据不成立、或对称归一化被移除后恒等式/β* 失效 → 中心机制须重述，Method 4→3 或更低并触发 gate。
- 若 CUDA 设备噪声量化显示 ≥1.0pp 效应不可与设备波动区分 → 预注册统计裁定失效，须改 CPU 冻结协议或计入噪声。
- 若把「用户提供的未公开先验（未发表、不充当公开证据）」写入公开证据/结果栏、把 smoke 值写成「已得正式结果」、把理论能耗写成硬件实测、或把「一定有优势」写成结论 → 依 `execution-contract-v1.md` §2 / 契约 §8 S6 诚信门停止，不升分。
- 若第 0 批关键基线无法复现 → 依契约停止回退 `needs-evidence`。

**说明**：C1–C3 是升到 `revise` 段（3.7+）的必要非充分条件；即便三条全过，仍需 Q1–Q2 档下 novelty 站稳与实证稳健才可能改推荐。本评审不预判其结果。

---

## Confidence:

- **综合 Confidence：Medium**（依 `calibration.md` 标签）。
- 理由：(i) **可直接核查的事实显著增多且置信度高**：本会话完整读取了契约、变更、v1 第三轮、P1 报告、两份实现、M0 JSON、1028 core 快照、4 个 results JSON、pipeline-state、execution-contract 与数据目录磁盘清单；所有引用数值均照录工件、差异如实记录（teacher 67.5/68.2 vs 文件 0.689/0.668、MNIST zip 192 MB 未直接见到、dgl pkl 表 vs pyg zip 实现）；代码行号可核。(ii) **但核心仍属「未给出的结果 / 未检索的 novelty / 未核验的 venue 规则」**：conversion loss 带内、横评系统优势、能耗 ≥5×、组合层 novelty、官方当年 policy 全属未知，故 Novelty / Conceptual 置信度仅 3、Venue 仅 3。(iii) 组合/推论层 novelty 未检索，上限被封顶、置信度下调。(iv) `results/*.json` 为单 seed 小子集 smoke、pipeline-state 全 pending，实验判断是「plan 可信 ＋ 实跑风险信号 ＋ 证据缺口」而非「结果已知」。
- **依公平规则**：不因 confidence 为 Medium 而下调 idea 分数；分数（3.3）与置信度（Medium）分开报；低置信度单独引导下一步检查（见 `Optional next-module decision` 与 `Evidence that would change my score`）。
- 各维度 Confidence 已在 `Rubric scores` 表逐维列出，分数与置信度不在此重复。
- **Development potential 保持 medium 而非 high 的置信度说明**：升 high 需「C1 口径闭合 ＋ C2 ρ_n 修正 ＋ C3 全量横评支持 ＋ C5 组合层检索无近邻」多项同时支持；当前均未知，故 medium 是如实取值。

---

## Strict reviewer comments:

> 依 `strict-idea-review.md` Harsh Reviewer Lens：短、诊断式、每条带 anchor，不作动机性缓冲；每条批评指向具体 claim / 机制 / prior-art / 缺失工件 / 逻辑残留 / 口径差异 / 可行性约束并给修复。

1. **关于「新算子类」的实验基础**（Anchor：`guidance-v2.md` §Core Idea / §Mechanism-Level Rationale；`vision_pipeline.py:101-104`；4 个 results JSON `graph_stats`）：你反复以「ρ_n 远离 1 的非行随机视觉 kNN 图」为领域瓶颈与新算子类依据，但 `batch_graphs(sym_norm=True)` 的对称归一化使实跑 `rho_mean` 在全部数据/全部 split 恒为 0.9987、`rho_std≈0.0316`。实际算子类近似行随机，与 ρ≈1 的 CNN 网格差异远小于契约声称。请先关闭 `sym_norm` 或显式构造 ρ_n 网格并如实报告分布，否则「适配到新算子类」无处落脚，这是「只是换个数据集」质疑的实证把柄。
2. **关于能耗核算口径**（Anchor：`vision_pipeline.py:275, 295, 322-336`；`results/gpu_MNIST_seed0.json` energy 段）：`_ann_macs` 计 ANN 全层一次前向，`ac_ops` 每 T 步只累加 `ns·H + ns·deg·C`、漏算第一层连续电流注入与输出层/膜电位，且随 T 线性增长而 `ann_macs` 为常数 —— 两侧分母不同，`energy_ratio_ann_over_snn` 是口径产物。请输出分层明细、统一口径，并在三种口径下给 `energy_ratio(T)` 曲线；不要在单一标量上外推「能耗优势」。
3. **关于「一定有优势」与已有反例信号**（Anchor：`results/gpu_MNIST_seed0.json` `ours_T1 1.6049× … T16 0.2768×`；smoke 0.6878/0.3425/0.4215×；`guidance-v2.md:120-125`；`execution-contract-v1.md:18, 83`）：全部已落盘预实验中该比值从未达到预注册 ≥5×，在 conversion loss 最小的 T=16 仅 0.28×（SNN 理论算术能耗约 ANN 的 3.6 倍），直接命中契约 failure signal「≤1×」。这些是单 seed 小子集 smoke、非正式裁决，但「实测裁决尚未完成」不能继续表述为「优势待确认」；请把它表述为「已有反例信号，须先统一口径再裁定」，并按 `Claim adjustment rule` 预备收窄，不得调口径凑 5×、不得把预注册写成结论。
4. **关于 QCFS 基线忠实度**（Anchor：`vision_pipeline.py:129-135, 170-172`；`run_experiments.py:29-41, 66`；`results/gpu_MNIST_seed0.json` `naive_T*` vs `qcfs_T*`）：`train_ann` 明写 `quantize_L` 是「so the QCFS baseline trains its own source ANN」，但 runner 从未传它；实跑 `naive_T1` 与 `qcfs_T1` 的 `hidden_spikes`/`ac_ops` 完全相同（22472 / 5279973.75）。所谓「全套转换方法横评」里 QCFS 数值退化为 naive。请给 QCFS 重训量化 teacher 并展示与 naive 的可测差异，否则横评归因不可信。
5. **关于恒等式精度与契约门槛**（Anchor：`guidance-v2.md:144` Traceability「<1e-12」；`results/gpu_MNIST_seed0.json` identity 段 `3.242e-5→6.407e-6`；`m0-results.json` meta）：M0 的 1e-15 是 float64 合成算子；真实图级管线 float32 残差是 1e-5 量级，高 6–7 个数量级。请给 float64 验证路径把图级残差压到 1e-12 内，或重定义门槛并说明量级来源；不要混用「合成验证精度」与「真实管线精度」。
6. **关于 teacher 质量与 conversion loss 判别力**（Anchor：`results/gpu_MNIST_seed0.json` `ann 0.689/0.668/0.688`、`ours_T8 8.6pp`、`ours_T16 2.0pp`；`guidance-v2.md:120-122`）：teacher 是 2000 图子集、单 seed、68% 级，T≤8 conversion loss 8.6pp 远超 minimum 3.0pp 与 strong 1.5pp，`argmax_agreement` 仅 0.744(T8)。契约没有 teacher 验收门槛，退化 teacher 上的横评可机械满足「同 teacher」却失去意义。请设 teacher 验收门槛（公开 benchmark 数值作下界，须检索或用户提供）、全量阶梯扩展、统计功效预检，并报告 Cora/CiteSeer/PubMed 回归锚点。
7. **关于 CUDA 非确定性与统计裁定**（Anchor：`contracts/core-1028.snapshot.py:34-38`; `vision_pipeline.py:129` / `run_experiments.py:134` 默认 cuda；gpu 结果 environment `"device":"cuda"`）：1028 core 自述 CUDA 稀疏归约使 PubMed ANN 移动 +0.69 pp（7 seeds）「larger than the effect sizes reported here, so the frozen protocol trains on CPU」；v2 默认 cuda 且只说「报 std/CI」，未做 device-pair 噪声量化。预注册「T≤4 优于最强基线 ≥1.0pp 且配对 bootstrap CI 下界 >0」与 0.69 pp 设备噪声同量级。请固定 reduction / 改 CPU 冻结 teacher / 显式量化 device-pair 噪声并计入 CI，否则该裁定不可信。
8. **关于「直接复用 1028」与 gauge 归属**（Anchor：`contract-change-v1-to-v2.md:15`；`guidance-v2.md:85`；`contracts/core-1028.snapshot.py:251-288`；`vision_pipeline.py:190-201`）：契约写「复用 `train_ann`/`convert`/`check_identity`/`gauge_normalize`，仅新增 `vision_core.py`」，实际 `vision_pipeline.py` 是独立重写（未 import 1028 core、无 `vision_core.py`、`check_identity` 单层非逐层），且 gauge 是 percentile 缩放压到 `[0,θ]` 而非 1028 的 unit-spectral-gain 重参数化。方法命题级继承成立，但「组件继承逐条写明」时 gauge 一条须标「改编」；并补 Planetoid 回归锚点（1028 有 gate PASS 到 0.003pp）以坐实代码等价性。
9. **关于数据源与池化口径**（Anchor：`guidance-v2.md:61-62` 数据集表；`execution-contract-v1.md:32, 51`；`vision_pipeline.py:67, 91`; `run_experiments.py:135`; gpu environment `"pool":"sum"`）：契约表格写 `data.dgl.ai` pkl 1.39/2.51 GB、CIFAR10 85–150 节点、全篇写「全局平均池化」，实现用 `data.pyg.org` zip（192 MB ＋ 316 MB）、`pool="sum"`。复现者会拿错数据、论文会写错读出算子。请统一表格/实现措辞、冻结 SHA-256 与图索引，并说明 sum pooling 下不同图节点数导致的 logits 尺度差异。
10. **关于全量扩展与 smoke 定位**（Anchor：`vision_pipeline.py:67-111, 162`「full train batch」；`pipeline-state.json` 全 pending；`guidance-v2.md:115` Scaling fallback）：实现把整个 split 拼成一个块对角系统一次前向、无图级 minibatch；2000 图 `N=141366` 可跑（66.87 s），全量 55,000 图约 2.75M 节点，3060 12GB 上有显存风险，「先子集再扩到可用规模」不是简单调 cap。请实现图级 minibatch/分块、登记 `infeasible-with-evidence` 回退，并全程把 `results/*.json` 标为单 seed 小子集 smoke、非已得正式结果。

---

## Fixability table:

依 `calibration.md` 字段。Owner skill 仅列建议归属，**未执行任何 handoff**（见 `Optional next-module decision`）。

| Issue | Affected dimension | Severity | Fix class | Can fix before writing? | Required evidence or design change | Risk-reduction condition | Development-potential impact | Owner skill |
|---|---|---|---|---|---|---|---|---|
| B1 能耗核算口径不自洽 ＋ smoke 反例信号（0.28×–1.60×、从未达 5×） | Method / Experimental / Acceptance | high（准 fatal，P2 入口条件） | method-redesign | yes（代码/纸面） | 分层 `ac_ops` 明细 ＋ 统一 ANN/SNN 口径 ＋ 三口径 energy_ratio(T) ＋ 绝对量同报 ＋ 等精度 T 裁决 | 5× 在所有合理口径下稳健，或按 claim adjustment rule 收窄表述 | 高 | ccf-experiment-designer |
| B2 `rho_mean≈0.9987` 与新算子类声称矛盾 | Problem / Conceptual / Novelty | high（准 fatal，P2 入口条件） | problem-refinement | yes（配置/受控设计） | 关闭 `sym_norm` 或 ρ_n 受控网格 ＋ 非行随机算子普遍性的公开证据 ＋ 如实报告 ρ_n 分布 | 新算子类获实验基础、ρ_n 加权可测 | 高 | ccf-idea-optimizer |
| B3 恒等式真实残差 1e-5 未达 <1e-12 ＋ teacher 无验收门槛 | Method / Experimental | high（准 fatal，P2 入口条件） | method-redesign | yes | float64 验证路径（或重定义门槛）＋ 全量 teacher ＋ 验收门槛 ＋ 功效预检 | 残差达标、teacher 判别力可辩护 | 中—高 | ccf-experiment-designer |
| W5 QCFS 退化为 naive（`quantize_L` 未启用） | Experimental | high | evidence-design | yes（代码） | 给 QCFS 重训量化 teacher，展示与 naive 可测差异 | 横评归因不被退化基线污染 | 高 | ccf-experiment-designer |
| W6 缺直训 SNN / Planetoid 回归锚点 / robustness 消融 / literature 基线复现 | Experimental / Elegance | high | evidence-design | no（需实现） | 补齐基线臂 ＋ 回归锚点（1028 gate PASS 0.003pp 范式）＋ 3 归一化/2 池化/3 θ 消融 | 「全套横评」名实相符、组合必要性可测 | 高 | ccf-experiment-designer |
| W8 CUDA 设备噪声 +0.69 pp 未量化，与 ≥1.0pp 效应同量级 | Experimental / Acceptance | high | evidence-design | yes | device-pair 噪声量化 ＋ 固定 reduction 或 CPU 冻结 teacher ＋ 计入 CI | 配对 CI 下界 >0 的裁定可信 | 中—高 | ccf-experiment-designer |
| W9 无图级 minibatch，全量扩展需改代码 | Feasibility | medium | feasibility-check | no（需实现） | 图级 minibatch/分块 ＋ 3060→4090 提交路径 ＋ `infeasible-with-evidence` 回退 | 全量 55k 可跑且不 OOM | 中 | ccf-experiment-designer |
| W4 数据源/尺寸/节点数口径不一致；W10 池化措辞；W11 teacher 数值/zip 口径；W12 gauge 归属与代码复用级未兑现 | Evidence integrity | medium | evidence-design | yes | 统一契约表格与实现；冻结 SHA；把 gauge 标「改编」；以文件为准登记数值差异 | 复现核验无假阳性、继承表述诚实 | 低—中 | ccf-integrity-auditor |
| 组合/推论层 novelty `not searched` | Novelty / Confidence | high | novelty-grounding | no（需检索） | 针对组合本身做公开检索（通用关键词、不粘贴私有措辞） | 组合层 `not searched` 边界关闭 | 中 | ccf-literature-searcher（若授权） |
| 目标期刊当年官方 policy / review form 未核验 | Venue fit | low | venue-switch | yes | 核验 TNNLS / Neural Networks 当年官方页 | venue 定位与官方规则自洽 | 低 | ccf-submission-checker（若授权） |
| W2 预判与反例信号并存、诚信门 | Acceptance / Evidence integrity | high | evidence-design | yes | 全程「预注册目标 / 非实测」＋「理论算术能耗估算，非硬件实测」；`observed_finding` 不早于 P5A；不调口径凑 5× | 诚信门 S6 不触发 | 中 | ccf-integrity-auditor（若授权） |

> 「用户提供的未公开先验（未发表、不充当公开证据）」与 `results/*.json` 单 seed smoke 值，不列入任何 Issue 的 required evidence；不得用其替代公开实验或写成已得正式结果。

---

## Upgrade / pivot actions:

依 `SKILL.md` workflow #8 标签分类，每条为具体动作，不含通用套话。

- **[problem-refinement]**：关闭 `sym_norm` 或按契约 robustness 变体显式构造 ρ_n 受控网格（对称归一化 / mean / sum 三算子），给「非行随机算子在图视觉中普遍存在」的**公开**证据，把中心问题从「被归一化抹平的 ρ≈1 类」锚到「真实部署类」；全程如实报告实际 `rho_mean/rho_max/rho_std`。
- **[method-redesign]**：统一 ANN/SNN 操作计数口径（`ac_ops` 分层明细、补第一层与输出层、三口径敏感性）；float64 验证路径把图级恒等式残差压到 <1e-12（或重定义门槛并说明量级）；补「一般 A 下图级 margin 下 β* 最优性」的解析/反例条件；把 gauge 明确标为「改编」并补 Planetoid 回归锚点做代码等价性验证。
- **[novelty-grounding]**：对组合本身做一次公开检索（通用关键词，不粘贴私有措辞），确认「超像素图 ANN2SNN 统一横评 ＋ 能耗对照 / ρ_n 加权 margin 偏置」无近邻命中；全文一致声明不发明任何已占组件，不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」；澄清「本文新推论」与 1028 未公开先验的边界。
- **[evidence-design]**：按 H1–H8 执行 —— QCFS 重训、直训脉冲 GCN、Planetoid 回归锚点、robustness 消融、device-pair 噪声量化、teacher 验收门槛与全量阶梯扩展；报告 conversion loss–T 曲线（5 seeds 配对 CI/BH）、ρ_n 分桶误差分解、三口径 `energy_ratio(T)` 与 spike 密度/SynOps/wall-clock；统一数据源/池化/teacher 数值口径；保留全部负结果。
- **[feasibility-check]**：实现图级 minibatch/分块，确认 3060 12GB 子集与 4090 全量可跑通；固定 reduction 或 CPU 冻结 teacher；登记 `infeasible-with-evidence` 回退；核验 `dyg-cold` 环境快照与数据 SHA-256。
- **[venue-switch]**：维持主投 Q1–Q2 期刊档；结构上把「适配 / 横评 / 能耗」绑定为单一叙事；成文前核验当年官方 policy / review form；预备 honest fallback（收敛为「首个图结构视觉分类上的转换方法统一横评与理论能耗分析」）。
- **[pivot]**：若组合层检索命中近邻、或统一口径后能耗优势被证伪、或 P4 横评无系统优势，则放弃「三重收益」定位，pivot 为「统一协议横评 ＋ 失效边界/理论能耗分析」型贡献，并把 novelty 完全收敛到横评与诚实边界（契约 §Story Strength Audit 已备用）。
- 不输出 **[abandon]**：中心主张可测（恒等式残差、conversion loss–T、ρ_n 分桶、三口径能耗比、5 seeds CI）、H1–H8 路线可命名、0 未解 fatal，stage-aware 规则不满足 abandon 条件。

**最小可行修复路线（按依赖顺序，纸面/代码优先、无大规模算力成本）**：
1. **先做 [method-redesign] 的 B1**：统一能耗核算口径 ＋ 三口径 `energy_ratio(T)` ＋ 绝对量同报，并在等精度 T 上按 `Claim adjustment rule` 预备裁决 —— 这是判定「三重收益」是否成立最便宜、最决定性的一步；若所有合理口径下比值 ≤1×，直接执行 [pivot] 的能耗收窄，不必再为凑 5× 跑后续实验。
2. **同时做 [problem-refinement] 的 B2**：关闭 `sym_norm` 或显式 ρ_n 受控网格，确认「新算子类」有实验基础；与第 1 步共同决定 Problem / Conceptual / Novelty 是否可站稳。
3. **再做 [evidence-design] 的 B3 ＋ W5/W8**：float64 恒等式验证、teacher 验收门槛与全量阶梯、QCFS 重训、device-pair 噪声量化；随后仅先跑 5 seeds 子集横评（含关键基线复现），测 conversion loss–T 与三口径能耗曲线 —— 这是判定核心假设是否被实测推翻的最小可测实验。
4. **依据第 3 步结果决定**：若判据成立且有系统优势 → 补齐全套基线 ＋ 全量扩 4090 ＋ robustness 消融 ＋ 组合层检索，主投 Q1–Q2 档（`revise` 方向）；若被推翻或与近邻等价 → 执行 [pivot]，保留全部负结果。
5. 全程：不把「用户提供的未公开先验（未发表、不充当公开证据）」写入证据/结果栏；不把 `results/*.json` smoke 值写成已得正式结果；不把理论能耗写成硬件实测；不把「一定有优势」写成结论；统一 W4/W10/W11/W12 口径。

---

## Evidence that would change my score:

**会升分的证据（全部需公开可复算、非编造）**
- 统一口径后在三种合理口径下 `energy_ratio(T)` 稳健、且在 ANN−1.5pp 带内的最小 T 上比值 ≥5×，同时 spike 密度显著低于 ANN 激活密度（影响 Method / Experimental / Acceptance）。
- ρ_n 受控网格显示非行随机算子上系统误差按 ρ_n 加权、β*/膜电位解码收益可测，且「非行随机算子在图视觉中普遍存在」的公开证据成立（影响 Problem / Conceptual / Novelty）。
- 5 seeds 全量横评显示 1028 组合在 T≤4 相对最强单点基线 conversion loss 低 ≥1.0pp、配对 bootstrap CI 下界 >0、BH q<0.05，且逐组件消融方向一致（影响 Experimental / Acceptance / Elegance）。
- float64 验证把图级恒等式残差压到 <1e-12（或门槛被合理重定义），teacher 达验收门槛且 Cora/CiteSeer/PubMed 复现 1028 shipped numbers 到 0.003pp（影响 Method / Experimental / Feasibility）。
- 组合/推论层公开检索无近邻命中 ＋ 逐组件消融证明组合必要性（影响 Novelty / Conceptual / Confidence）。
- QCFS 重训后与 naive 出现可测差异、直训 SNN 与 Planetoid 锚点补齐、device-pair 噪声被量化且 ≥1.0pp 效应可区分（影响 Experimental）。

**会坐实 fatal / 降分的证据**
- 组合层检索命中近邻或「组合」坍缩为已知组件拼装 → Novelty 3→2、F2 回潮，整体回约 3.0–3.1。
- 统一口径后能耗比在所有合理口径下 ≤1×、或 spike 密度 ≥ ANN 激活密度 → 「三重收益」降为「二重」、Acceptance 回落，须按 `Claim adjustment rule` 收窄。
- P4 全量横评无系统优势、或 ρ_n 受控网格显示新算子类论据不成立、或移除对称归一化后恒等式/β* 失效 → pivot 为纯 benchmark 故事或 Method 降分。
- CUDA 设备噪声使 ≥1.0pp 效应不可区分 → 预注册统计裁定失效。
- 把「用户提供的未公开先验（未发表、不充当公开证据）」写入公开证据/结果栏、把 smoke 值外推为「已得正式结果」、把理论能耗写成硬件实测、把「一定有优势」写成结论、或调口径凑 5× → 依诚信门停止，不升分。

**明确不作为证据的项**：任何录用概率、真实审稿人意见、meta-review、未核验的官方当年规则、编造的 URL/DOI/实验数值；以及「用户提供的未公开先验（未发表、不充当公开证据）」—— 即 1028 成稿及其全部数值、图节点分类 `T≤8` 达 `ANN−1.5pp` 带内、成稿 §3.2/§5.1 引用、`core-1028.snapshot.py` 中的 shipped numbers；以及 `results/*.json` 作为「单 seed 小子集预实验 smoke」被外推为正式结果。本报告未生成上述任何一类，也未生成任何新的实验结果数值（全部数值照录已读工件）。

---

## Recommendation:

**`pivot-with-rescue-route`**（`ccf-idea-reviewer` 5 选 1 之内，由加权 3.3 落在 3.0–3.6 段直接得出）。

理由（与分数、fatal gates、stage-aware 规则一致）：
- 3.30 → 3.3 落在 `calibration.md` 3.0–3.6 段 → `pivot-with-rescue-route`，**不依赖 fatal gate 压顶**；不是把分数抬到 `revise`（3.7+），也不是靠 gate 强行压回。
- 不取 `needs-literature-search`：组件层按用户指令标 `searched`，结论「高重叠 ＋ 薄增量」而非「未知」；组合层未检索作边界/置信度处理（封顶 novelty 3、conf 3），沿用 v1 第三轮。
- 不取 `abandon`：中心主张可测（恒等式残差、conversion loss–T、ρ_n 分桶、三口径能耗比、5 seeds CI），存在具名修复路线（H1–H8 / 最小可行路线），依 `strict-idea-review.md` 不满足「无可测主张且无重构」。
- 不取 `revise` / `accept-to-develop`：F2 novelty 核心质疑未消解、核心结果预注册未实测、能耗口径不自洽且已有反例信号、`rho_mean≈1` 削弱新类论据、全套横评打折、teacher 质量与统计可信度未闭合。

**含义**：保留最佳要素（自带图视觉数据集规避 v1 适用条件错位、恒等式在图级 R 读出上的精确迁移、统一协议横评、诚实边界、可复算协议），改变**方法/证据/口径**（B1 能耗口径、B2 ρ_n 算子类、B3 恒等式精度与 teacher 门槛、QCFS 重训与 device-pair 噪声、全量扩展）与 **novelty 定位**（组合层检索、接受 Q1–Q2 增量系统实证定位）中的至少一组；而这些恰在 P2/P3/P4 执行，与 `proceed` 不矛盾。

### P1B 硬门裁决（用户指定的唯一硬门）

**裁决：`proceed`（conditional proceed / proceed-with-narrowing）—— 0 条未解 fatal，不阻止进入 P2/P3。**

**为何两个结论不矛盾**：`ccf-idea-reviewer` 的 `pivot-with-rescue-route` 评「idea 当前就绪度、是否值得按当前 formulation 直接发展」；P1B 硬门评「是否存在未解 fatal risk 阻止进入 P2/P3 去执行后续门」。用户明确「是否仍存在未解 fatal risk 是能否进 P2/P3 的唯一硬标准」，且「实验尚未开始是正常状态、不把尚无结果当致命缺陷」。因此 3.3 / `pivot-with-rescue-route` 的就绪度**不阻塞** `proceed`；`pivot` 所要求的「改变问题/方法/证据/novelty 中至少一组」恰由 P2（数据/协议/口径）、P3（基线复现）、P4（全量横评/消融/能耗）执行。此区分沿用 v1 第三轮 `Recommendation` 下 `Startup-decision` 的体系划分。

**四条 P1B 判据逐条核验**：

| 判据 | 核验结论 | 依据 |
|---|---|---|
| 是否有未解 fatal risk（唯一硬标准） | **无，0 条** | `Serious blockers` A 段 9 行逐条核对；五条数值 fatal gate 全不触发、两条临界属可修复；B1–B3 为准 fatal 级但已列为 P2/P3 入口可执行待办，非「unaddressed fatal」；0 正式实验按硬要求不判 fatal。 |
| 机制是否有可跑路径 | **有，且已实跑** | M0（float64 合成，25 格 ≤9.88e-15）＋ 4 个 `results/*.json` 本机 CUDA smoke（66.87 s/臂）＋ `sum_n_hit_rate=1.0` 逐 T 成立 ＋ 三个真实缺陷已发现并修复；`check_identity` 在真实管线逐 T 运行。 |
| 最近邻基线是否可复现 / 可用 | **核心路径可跑，全套打折可修复** | 6 种方法已实现、T∈{1,2,4,8,16}、FTBC beta 在 val 校准、T=8 四消融；QCFS 退化（W5）、缺直训 SNN/Planetoid 锚点/文献基线（W6）属契约已预留「如实标注」的可修复缺口，非「unavailable baseline」。 |
| evidence plan 是否可信 | **可信但含入口条件** | 冻结官方 split、5 seeds、配对 bootstrap R=5000、sign-flip 1000、BH q<0.05、test 隔离、trial ledger、逐组件消融、恒等式残差、ANN/理论能耗对照、Traceability 齐备；但须先闭合 B1–B3 与 W5/W8 方可产出可信 P4 主表。 |

**P2/P3 入口硬条件（H1–H8，全部为约束，非分数承诺）**：
- **H1 · 能耗口径硬门（诚信 ＋ 契约 stopping criteria）**：进入 P2 前统一 ANN/SNN 操作计数口径（`ac_ops` 分层明细、补第一层与输出层/膜电位），给三口径 `energy_ratio(T)` 与 spike 密度/SynOps/wall-clock；全程标「45 nm 理论算术能耗估算，非硬件实测」；**不得**把「一定有优势」写成结论、不得调口径凑 5×；若任一合理口径下 ≤1× 或 spike 密度未显著低于 ANN 激活密度，按 `Claim adjustment rule` 收窄为「稀疏活动与 SynOps 代理指标」并保留全部负结果。
- **H2 · ρ_n 算子类硬门**：关闭 `sym_norm` 或按 robustness 变体显式构造 ρ_n 受控网格，如实报告实际 `rho_mean/rho_max/rho_std`；「新算子类 / ρ_n 加权」表述须与实际 A 一致，不得沿用「ρ_n 远离 1」而实现给 ρ≈1。
- **H3 · 恒等式精度与 teacher 门槛**：float64 验证路径把图级残差压到契约 <1e-12（或版本化重定义门槛并说明量级）；设 teacher 验收门槛（公开 benchmark 数值作下界，须检索或用户提供，不得编造）＋ 全量 55k/5k/10k 阶梯扩展 ＋ 统计功效预检。
- **H4 · 基线忠实度与回归锚点**：给 QCFS 传 `quantize_L` 重训并展示与 naive 可测差异；补直训脉冲 GCN、Cora/CiteSeer/PubMed 回归锚点（对齐 1028 `wp0_reproduce.py` gate PASS 0.003pp 范式）；DCGS/AdaFire/PASCAL/CS-QCFS 等「无官方码或需重训」如实标注、不进主表。
- **H5 · 统计可信度**：量化 CUDA device-pair 噪声（1028 记 +0.69 pp）并计入配对 CI，或固定 reduction / CPU 冻结 teacher；「≥1.0pp 且 CI 下界 >0」须与设备噪声可区分；5 seeds、配对 bootstrap、sign-flip、BH 完整报告，不挑 seed、不调参到显著。
- **H6 · 口径一致性**：统一 `guidance-v2.md` 数据集表与实现/execution-contract（数据源、尺寸、节点数）、池化措辞（sum vs mean）、teacher 数值与 zip 记录（以文件为准）、gauge 归属（标「改编」）；冻结数据/图索引 SHA-256 与环境快照。
- **H7 · 全量扩展可行性**：实现图级 minibatch/分块，确认 3060 子集与 4090 全量可跑通；登记 `infeasible-with-evidence` 回退；单臂 ≤30 min / 远端 ≤6 h 预算不虚报。
- **H8 · 隔离与阶段纪律**：1028 全程标「用户提供的未公开先验（未发表、不充当公开证据）」；`results/*.json` 标「单 seed 小子集预实验 smoke、非已得正式结果」，`pipeline-state.json` 全 pending 不得被写成已过门；`expected_strong` 全标「预注册目标 / 非实测」、`observed_finding` 不早于 P5A；组合层 novelty 检索留给后续门，`proceed` 不等于 novelty 已站稳；成文前核验当年官方 venue policy。

**与 v1 第三轮 `startup-decision = proceed`（conditional）的关系**：本评审**独立复核后确认门禁结论一致**（0 未解 fatal / proceed conditional），但**不照抄其分数或 H1–H9**：v1 的 H 条件针对 ViG/κ_n/推论层解析；本轮 H1–H8 针对 v2 的**实现层可执行性风险**（能耗口径、ρ_n、恒等式精度、基线忠实度、CUDA 噪声、全量扩展），二者互补。v1 三轮红队原文与分数（2.5 / 3.2 / 3.4）完整保留、未抬分、未删除。

---

## Optional next-module decision:

- **CCFA Handoff Mode: PARTIAL**（依 `SKILL.md` 与 `handoff-modes.md`）。本任务为**独立预实验对抗评审**，用户未请求任何 sibling-skill 切换，也未授权把未发表 idea 文本用于检索；依 workflow #10「if a module is denied, stop at verdict, risks, and action queue」，本评审**停止在 verdict / risks / action queue，不执行任何 handoff**。
- 未切换的模块：`ccf-idea-optimizer`（B2 受控设计 / 主张收敛）、`ccf-literature-searcher`（组合层针对检索，需用户显式授权）、`ccf-experiment-designer`（H1–H8 协议升版 ＋ 基线复现 ＋ 全量横评）、`ccf-submission-checker`（核验目标期刊当年官方 policy）、`ccf-integrity-auditor`（W4/W10/W11/W12 口径一致性与隔离标注）。
- 若用户**显式授权**后续切换，按 PARTIAL 模式建议顺序：`ccf-experiment-designer`（先做 H1 能耗口径 ＋ H3 恒等式/teacher，纸面/代码为主）→ `ccf-idea-optimizer`（H2 ρ_n 受控设计）→ `ccf-literature-searcher`（组合层公开检索，公共关键词）→ `ccf-experiment-designer`（H4/H5 基线复现与统计）→ 视 P4 结果决定是否进入后续写作。本评审不代写、不模拟上述模块的输出，也不预判其结果。
- 隔离声明：上述建议不含任何已执行的检索、实验或写作，不含录用概率与真实审稿记录；未生成任何 URL / DOI；未修改任何被评审文件。

---

## Checklist status:

依 `SKILL.md` Mandatory Review Checklist（standard 模式 10 条）逐条如实标注。

| # | 检查项 | 状态 | 说明 |
|---|---|---|---|
| 1 | Target venue/journal、venue family、field、assumptions 明确 | pass | Q1–Q2 期刊档 ＋ 阶段边界（P1B、全 pending）＋ 成稿隔离标注 ＋ 数值以文件为准的差异说明；官方当年政策未核验已注明 |
| 2 | 每个 idea 归一化为 problem / gap / root challenge / insight / method mechanism / expected evidence / limitation | pass | 见 `Normalized idea`（7 要素 ＋ 隔离标注 ＋ 实读修正 ρ_n≈1、sum pooling、代码独立重写） |
| 3 | Literature status 标注为 searched / partially searched / user-provided only / not searched | pass | 组件层 `searched`、本会话动作 `not performed`、组合/推论层 `not searched`；见 `Search basis` |
| 4 | standard 模式有来自 public-safe literature search 的 closest-work table，除非用户禁止浏览或隐私阻止 | **partial** | closest-work 表已建（8 条，字段齐全，针对 v2 重评），但来源为**用户契约 §Citation Scope 与 v1 三轮已核验结论**，本会话未执行公开检索、组合层未检索；依 `privacy-and-evidence.md` 未把未发表 idea 文本用于查询；未编造任何 URL/DOI |
| 5 | 五个专家角色独立应用：field / method / experiment / AC-venue / skeptical prior-art | pass | 见 `Per-expert reviewer notes`：5 个必需角色各自独立 ＋ Panel Synthesis，分数与置信度分开；用户明确 5 个，未强加第 6 个 |
| 6 | 所有 rubric 维度 1–5 打分或标注 n/a 与理由；每个 ≤3 含 deduction / evidence basis / repair condition / 预期分数变化 | pass | 10 维全打；**7 个 ≤3 项**均有完整明细块（扣分理由 / 证据基础 / 为什么重要 / 修复条件 / 预期变化 / development effect）；3 个 >3 项在表内给 deduction / repair |
| 7 | Fatal risks 与可修复弱点、局部细化分开 | pass | 见 `Serious blockers`：A 段 0 条 fatal（含 9 行逐条核对表）、B 段 3 条准 fatal 入口条件、C 段 W1–W12 fixable、D 段隔离项 |
| 8 | Confidence 与 score 分开报 | pass | 综合 Confidence=Medium 单列；各维 Confidence 在 rubric 表；各专家 Score tendency 与 Confidence 分行；未因置信度下调分数 |
| 9 | 推荐值为 5 选 1 之一；`abandon` 仅用于无可测主张且无重构 | pass | `pivot-with-rescue-route`；abandon 条件已论证不满足；另按用户 P1B 硬门独立给 `proceed`（conditional）＋ H1–H8，两体系已显式区分 |
| 10 | 任何可选模块切换遵循 CCFA handoff mode；若被禁用则只输出 upgrade actions | pass | PARTIAL 模式，未执行 handoff，仅输出 `Upgrade / pivot actions` 与建议 owner |

补充 `task-modes.md` 状态：
```text
Mode: standard
Checks run: 完整 mandatory checklist + 输出契约 21 字段 + 定量反馈 + panel 纪律 + fatal gates + 分数段映射 + 逐维扣分明细 + 实读工件真实性核验（数据字节/results JSON/代码行号/1028 core 快照/pipeline-state）+ 五问逐条展开 + Output Quality Gate
Checks skipped: 无（除 #4 标 partial）
Unresolved risks: 能耗核算口径不自洽且 smoke 反例信号、rho_mean≈1 与新算子类矛盾、恒等式真实残差未达 1e-12、teacher 门槛与全量扩展、QCFS 退化与全套基线缺口、CUDA 设备噪声未量化、组合层 novelty 未检索、官方当年 venue policy 未核验、数据/池化/teacher 数值口径不一致、目标期刊当年官方规则
```

---

## Output self-check:

依 `review-output-standards.md` Output Quality Gate 与 `task-modes.md` Output Quality Gate 逐项自检（作为读者通读一遍后确认）。

| # | 检查项 | 结果 | 具体确认 |
|---|---|---|---|
| 1 | 小节顺序匹配承诺的输出契约 | ✓ | 从 `## Verdict first:` 到 `## Output self-check:` 共 **21 个契约字段**，顺序与 `SKILL.md` Output Contracts（单 idea / standard）完全一致；首字段即 Verdict first，末字段即 Output self-check；`### 评审任务五问 · 完整依据`、`### P1B 硬门裁决`、`### 特别回答` 为三级标题、嵌在对应二级字段内，不破坏 21 个二级字段契约 |
| 2 | 每个表格有合法 Markdown 分隔符且每行列数一致 | ✓ | 五问判定表 3 列、Normalized idea 2 列、A 段 fatal 核对表 3 列、Rubric 表 6 列、Score-change 表 3 列、Fixability 表 9 列、Checklist 表 4 列、本表 4 列、P1B 判据表 3 列；逐行核对列数一致，单元格内无裸 ASCII `\|` 破坏分隔（公式 `R A (E₁W₂)`、`ρ_n`、`β*=θ/(2T)`、`D^{-1/2}(A+I)D^{-1/2}` 不含竖线） |
| 3 | 分数、置信度、推荐内部一致 | ✓ | 加权计算 330/100 = 3.30 → `**Overall:** 3.3`（一位小数）；1–10 转换 ≈ 6.6；综合 Confidence=Medium 与各维 Confidence 分开；3.3 落在 calibration 3.0–3.6 段 → `pivot-with-rescue-route`，五条数值 fatal gate 均不触发、两条临界，已在 `Weighted final score` 解释分数段与 5 选 1 映射；`proceed`（conditional）属 P1B 硬门独立体系，已显式说明「不矛盾」及划分，无矛盾 |
| 4 | 项目符号语法平行、动作风格一致 | ✓ | `Upgrade / pivot actions` 统一用 `[标签] + 动作动词` 开头；Fixability / Score-change 用名词短语或条件句；H1–H8 统一用「主题 · 动作」＋ 约束句；`Strict reviewer comments` 10 条统一「关于 X（Anchor：…）：… 请 …」结构 |
| 5 | 因果/递进逻辑显式（问题→原因→后果→行动） | ✓ | 每个 ≤3 块按「扣分理由→证据基础→为什么重要→修复条件→预期变化」排列；Serious blockers 按 fatal(0)→准 fatal(B1–B3)→fixable(W1–W12)→隔离(D) 分层；五问依据按「判定→实读证据→为何/还缺→按硬要求不判 fatal」；最小可行修复路线按依赖顺序编号 |
| 6 | 语言内标点一致 | ✓ | 正文中文全角标点（，。；：）；公式、字段名、文件名、venue、英文缩写、代码标识符、数值/SHA 保留半角；Markdown 表格分隔符与代码块为半角（格式必需）；保留 21 个英文字段标题 |
| 7 | 无 TBD / TODO / [fill] / 空标题占位 | ✓ | 无占位符；所有字段均有实质内容；未把被评审工件中的 `<TBD>`/`TBD` 当本报告占位符 |
| 8 | 无通用套话（「需要更多实验 / 创新性不足 / 进一步完善 / 加强 related work」等）无锚点残留 | ✓ | `Strict reviewer comments` 10 条均带 Anchor（文件:行号或字段名）；每条批评指向具体 claim / 机制 / prior-art / 缺失工件 / 口径差异 / 可行性约束并给对应修复；Closest prior art 8 条均带字段块 |
| 9 | 每个 ≤3 分项含扣分理由 / 证据基础 / 修复条件 / 预期分数变化 | ✓ | 7 个 ≤3 维度各一个明细块，四项齐全，另附 Why it matters 与 Development-potential effect；3 个 >3 项不触发且已在表内给 deduction / repair |
| 10 | 五个专家角色独立、各自给具体拒稿级质疑或说明为何没有；置信度与分数分开 | ✓ | 5 必需角色均含 Score tendency（分数）与 Confidence（置信度）两行 ＋ Score-change condition；均给 strict rejection-grade concern ＋ Anchor ＋ Why ＋ Fatal ＋ Repair ＋ Development note；无角色被强行安排「无质疑」或赞扬，Panel Synthesis 未平均掉致命弱点 |
| 11 | fatal risk 与可修复弱点明确区分；含 score-change conditions 与最小可行修复路线 | ✓ | `Serious blockers` A 段 0 条 fatal（9 行逐条核对）＋ B 段 3 条准 fatal 入口条件 ＋ C 段 W1–W12 ＋ D 段隔离；`Score-change conditions` 表 C1–C7 含升分与反向降分；`Upgrade / pivot actions` 内含按依赖排序的「最小可行修复路线」5 步 |
| 12 | 推荐值仅为 5 选 1 之一 | ✓ | `pivot-with-rescue-route`（accept-to-develop / revise / pivot-with-rescue-route / abandon / needs-literature-search 五者之一）；P1B 硬门裁决 `proceed`（conditional）为独立体系，已标注并说明不矛盾 |
| 13 | 禁止编造：文献 / 数值 / 实验结果 / 评审意见 / 录用概率 | ✓ | 全部文献仅来自用户契约 §Citation Scope 与 v1 三轮已核验结论（venue/year 照录，未附 URL/DOI、未转录已存在的仓库 URL）；所有数值照录 `results/*.json`、`m0-results.json`、`guidance-v2.md`、`execution-contract-v1.md`、`core-1028.snapshot.py`、数据目录磁盘清单，未改动；无录用概率、无真实审稿人 / meta-review 引用；专家意见与 Strict reviewer comments 已声明为「本 panel 独立判断」；加权分数与预期变化为按 rubric 计算 / 条件性表述，非实验结果 |
| 14 | novelty 状态标为 searched 并写明边界 | ✓ | `Search basis` 标 `searched`（组件层）＋ 组合/推论层 `not searched` ＋ 本会话 `not performed` ＋ 4 条边界，据此封顶 novelty 3 / conf 3；`Novelty delta` 设「特别回答：组合与适配创新是否构成可辩护贡献」 |
| 15 | 未发表内部结果全程标注为「用户提供的未公开先验（未发表、不充当公开证据）」 | ✓ | `Target venue/journal`、`Normalized idea`、`Closest prior art table`、`Novelty delta`、`Serious blockers`（D 段）、各专家 notes、`Strict reviewer comments`、`Fixability`、`Upgrade / pivot actions`、`Evidence that would change my score`、`Recommendation`（H8）、`Output self-check` 中凡提及 1028 成稿 / 数值 / §3.2 / §5.1 / `T≤8` 带内 / `core-1028.snapshot.py` shipped numbers，均带完整标注；明确不进入 evidence / 打分依据、不替代公开视觉实验、不当公开前作 |
| 16 | 「预期结果」不写成「已得结果」；「理论能耗」不写成「硬件实测」 | ✓ | 全文把 conversion loss ≤1.5pp、横评 ≥1.0pp、能耗 ≥5× 标「预注册目标 / 非实测」；`results/*.json` 标「单 seed 小子集预实验 smoke、非已得正式结果」并注 `pipeline-state.json` 全 pending；全部能耗称「45 nm 理论算术能耗估算（MAC 4.6 pJ / AC 0.9 pJ）」并引 `model: NOT a hardware measurement`；H1 设为诚信硬门 |
| 17 | 文件用中文撰写、保留技能要求的全部字段标题 | ✓ | 21 个英文契约字段标题原样保留（Verdict first: … Output self-check:），正文全部中文；写入 `audits/ccfa-pre-experiment-review.md` |
| 18 | Verdict first 给结论、含 `**Overall:**` 行与 recommendation；五问逐条明确回答 | ✓ | `Verdict first` 含完整结论、五问判定表、0 未解 fatal 明确结论、三个必须区分、`**Overall:** 3.3` 独立行、综合 recommendation 与 P1B 硬门裁决；`**Overall:** 3.3` 另在 `Weighted final score` 独立行给出；五问完整依据在 `Serious blockers` 末尾「评审任务五问 · 完整依据」逐条展开 |
| 19 | 聚焦「预实验可执行性与风险修复条件」，不把「尚无实验结果」当致命缺陷 | ✓ | 全篇以 P1B 可执行性为 lens；`Target venue/journal` 记 `pipeline-state.json` 全 pending；A 段逐条核对明确「0 正式实验按硬要求不判 fatal」；`Experimental convincibility` 给 3 而非 2 并写明「按用户硬要求不因 0 正式实验压到 2」；`Stage and development potential`、`Recommendation` 备用 honest fallback |
| 20 | 实读工件真实性核验、差异不隐藏、以文件为准 | ✓ | 数据字节（CIFAR10 zip 316,368,127 B；MNIST processed 三文件；MNIST raw .pt 921,808,681 B）、4 个 results JSON 的 teacher/conversion loss/energy/identity/runtime、代码行号、1028 core 快照、pipeline-state 全 pending 均照录；用户「67.5% / 68.2%」与文件 `0.689 / 0.668` 差异以文件为准并登记 W11；MNIST 192 MB zip 未直接见到的差异如实记录；dgl pkl 表 vs pyg zip 实现差异登记 W4；能耗 smoke 反例信号（0.28×–1.60×、从未达 5×）如实点出而非隐藏 |
| 21 | 不迎合、不抬分；与 v1 第三轮分数不可直接比较的说明 | ✓ | `**Overall:** 3.3` 由 10 维加权 330/100 机械得出，无 +2 跳升、无「修订版默认更高」项、Novelty/Conceptual/Acceptance 三个压档维刻意留在 3；`Weighted final score` 明确「两轮分数不可直接比较（不同场景/证据边界/lens）」及本轮把 v1 无法看到的实现层风险计入扣分的逻辑；v1 三轮原文与分数（2.5/3.2/3.4）保留、未抬分 |

**最终一致性确认**：本报告为 **P1B 独立预实验对抗评审**，未由其他会话代写或模拟打分，未修改任何被评审文件，未抬分、未迎合；如实承认 v2 相对 v1 的可执行性进步（自带图数据规避 F1、代码/数据/smoke 实跑就位、三缺陷已修、0 未解 fatal、能耗写成可证伪假设），同时逐条论证**三处实现—声称错位**（能耗核算口径不自洽且已有反例信号、`rho_mean≈0.9987` 与新算子类矛盾、恒等式精度/teacher 门槛未闭合）与**全套横评打折**（QCFS 退化为 naive、缺回归锚点、CUDA 噪声未量化）；明确回答五问；**P1B 唯一硬门结论：0 条未解 fatal、不阻止进入 P2/P3（proceed conditional，附 H1–H8）**；严格区分「单 seed 小子集预实验 smoke」与「已得正式结果」、「预注册目标」与「已得结论」、「45 nm 理论算术能耗估算」与「硬件实测」；1028 全程隔离标注为「用户提供的未公开先验（未发表、不充当公开证据）」；未执行任何模块切换；未生成任何编造文献 / URL / DOI / 实验结果数值 / 录用概率；所有分数证据基础可追溯至契约、变更、v1 第三轮、P1 报告、两份实现、M0 JSON、1028 core 快照、4 个 results JSON、pipeline-state、execution-contract 与数据目录磁盘清单。
