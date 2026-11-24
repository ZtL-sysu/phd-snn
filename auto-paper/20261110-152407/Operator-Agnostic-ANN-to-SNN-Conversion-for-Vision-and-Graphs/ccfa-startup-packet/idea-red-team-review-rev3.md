# Idea Red-Team Review · rev3（第三次独立评审）

> 本文件由**第三次独立 idea 红队评审会话**生成，与前两次（`idea-red-team-review.md`、`idea-red-team-review-rev2.md`）不同会话。前两次报告原文完整保留，本评审不修改、不覆盖、不抬分。
> 模式：`ccf-idea-reviewer/SKILL.md` 的 `standard` 模式；依据 `references/strict-idea-review.md`、`rubric.md`、`calibration.md`、`expert-panel.md`、`source-notes.md`、`../ccf-common/references/review-output-standards.md`、`task-modes.md`、`privacy-and-evidence.md`、`handoff-modes.md`、`routing.md`。
> 评审对象：**rev2 主卡 + 新增 M0 本机实跑证据 + 已存在的 `matched-protocol.md`** 这一整体；目标档位按 rev2 的 **IEEE TNNLS / Q1–Q2 期刊档**（非 CCF-A 主会）。
> 阶段：`f-guidance-builder-v1` 的 **guidance / 实验前契约**阶段；判定重点为「未解 fatal risk / 机制可跑路径 / 最近邻基线可复现 / evidence plan 可信度」，**不以「现在有没有跑出精度」为判据**。

---

## Verdict first:

本评审为**第三次独立 idea 红队评审**。本报告内所有专家意见、严格评审意见均为**本红队 panel 基于真实文件作出的独立判断**，不代表任何真实审稿人、meta-review、录用记录或录用概率；不承诺任何分数变化、审稿行为或录用结果。未执行公开检索，未生成任何 URL / DOI / 实验数值；未把成稿内部结果当公开证据。

**结论（先给）**：新增证据是**真实、可核查、且实质性改变了局部结论**，但**没有改变整体档位**。按 IEEE TNNLS / Q1–Q2 期刊档评，当前 formulation 仍**不具备可接收性**，也**不属于应 abandon 的情形**；加权总分 `**Overall:** 3.4`（1–5 加权尺度，一位小数；1–10 尺度 ≈ 6.8），仍落在 `calibration.md` 的 **3.0–3.6 段 → `pivot-with-rescue-route`**。相对第二次 `**Overall:** 3.2`（3.16）的 **+0.24**，**只来自两个被新增证据直接兑现的维度**：`Method soundness` 3→4（M0 数值核验把「核心定理全未证」推进为「代数/概率命题层已实跑验证」）与 `Experimental convincibility` 3→4（`matched-protocol.md` 冻结版工件从「不存在」变为「兑现」＋ M0 可复算实跑 ＋ 第 0 批/S2 硬回退）；**其余 8 维（尤其 Novelty、Conceptual innovation、Risk-adjusted acceptance potential）一律不变**，因为 M0 与协议**不触及 F2 的核心 novelty 质疑**。无 +2 跳升，无「因是修订版默认更高」的项，推荐未升出 `pivot-with-rescue-route` 段。

**必须明确回答的四问（先给，完整依据见后文对应字段）**

| # | 问题 | 判定 |
|---|---|---|
| 1 | 第二次 F2 核心质疑（T1/T2/κ_n 不构成新推论、核心推导全在 M0 未证）在 M0 实跑后 | **部分解决** |
| 2 | F3（可比性两难）在 `matched-protocol.md` 真实存在后 | **已解决（到 guidance / 实验前契约阶段所要求的程度）**；仍有可修复残留，须由硬条件兜住 |
| 3 | 是否仍存在未解 fatal risk（能否进 G0 的唯一硬标准） | **无未解结构性 fatal（0 条）**；F1 已解决、F2 部分解决且不构成 fatal、F3 已解决；余项为准 fatal 级可修复弱点与执行期产物 |
| 4 | `startup-decision` 建议值 | **`proceed`（conditional proceed / proceed-with-narrowing）**，附 H1–H9 硬条件；按 `f-guidance-builder-v1`「Only `proceed` may enter G0」 |

**关键区分（用户硬要求 #1，严格区分两件事）**：M0 **证明了**「精确误差恒等式在固定线性算子类上精确成立」（P1，25 格最大绝对残差 `9.880984919163893e-15`）、「β\* 与 ρ 无关并消除 E₁ 的系统项」（P2）、「Hoeffding 型上界 sound」（P4，0 违反）、「确定性两阶段 Σs=n / 零条件方差」（P5）、「动态 A_t 与 max 非线性聚合落在适用类外」（P6，残差 `0.7476370778501276`、偏差 `1.105089450044243`）。M0 **没有证明**、其自述也明确否认「**ρ_n/T 单调判据在真实训练网络上成立**」——`m0-theory-check.md` 第 35 行原文：「不证明 ρ_n/T 单调判据在真实训练网络上成立（那需要 P4 全量实验）」；脚本 docstring 亦写明「不训练、不报告分类精度」。**恒等式精确成立 ≠ 单调判据成立**；前者是算子类上的代数事实，后者是真实训练网络 + 全套基线横评下的经验/诊断命题。M0 更没有回答「T1/T2/κ_n 是否构成 prior-art 无法得到的新推论」——它不含任何 prior-art 检索、非平凡性证明或推论层检索，且 P2 的数值恰与「`A·1=ρ_n·1` ＋ QCFS 零期望偏置 ⇒ ρ 加权 margin 平移」这一「一行代数」objection 相符。

**F1 / F2 / F3 逐条判定**

| Fatal | 判定 | 一句话依据 |
|---|---|---|
| F1 主张—适用条件错位 | **已解决**（沿用第二次判定，新增证据进一步坐实） | rev2 中心问题与适用条件 A1/A2 完全一致；M0 P6 把「动态 KNN + max 非线性不适用」从文字声明变为可测数值边界（0.7476 / 1.1051），`matched-protocol.md` §2 把原版 ViG 定为 B4 失效边界且「不进主结果、不得删」。 |
| F2 novelty 重述 / 组合 | **部分解决**（相对第二次「降级为可修复弱点」有推进，但**仍未解到可升 novelty 分**） | 已解决的一半：M0 把「核心推导全在 M0 未证」中的**数值/代数子集**兑现（P1/P2/P4/P5/P6 实跑），method soundness 风险实质下降。未解决的一半：① 单调判据在真实网络未测（M0 自认）；② T1/T2/κ_n 的「prior-art 无法得到」质疑完全未被触及，P2 数值反而佐证「一行代数」；③ P3 未干净复现 ρ-不变（相对误差随 ρ 变化 `0.2591–0.5648`、argmax 一致率 `0.828–1.0` 波动）；④ κ_n 单调性/κ_n–T2 张力/两解码兼容性/冗余消融/T1 非平凡性证明/推论层检索仍缺。 |
| F3 横评可比性两难 | **已解决（设计层＋工件层）**，带可修复残留 | 第二次 F3 的四项残留中，(i)「`matched-protocol.md` 不存在」**已消除**：文件真实存在、冻结版 v1、10 节；(ii) 同骨干/同 T/同 θ/同 calibration/同 conversion loss 定义已在 §2–§4 写死；(iii) 第 0 批 PASCAL/TPP must-rerun ＋「任一未跑通不得进主表」＋ §8 S2 硬回退 `needs-evidence`；(iv) §8 S4 已把裁决从「与 PASCAL/TPP 等价」改为「单调性连续落 failure」，**在协议层修正了范畴错位**。残留：ρ=1 校准律在 ρ≠1 聚合上的适配语义、PASCAL 复现验收锚、单调性操作化、rev2 §1 第 4 条原文口径、执行层零实验——均为可修复弱点，按 guidance 阶段不构成 fatal。 |

**综合 recommendation（`ccf-idea-reviewer` 5 选 1）：`pivot-with-rescue-route`**。**`startup-decision`（`f-guidance-builder-v1` 4 选 1）：`proceed`（conditional）**。二者**分属不同体系、并不矛盾**：前者评「idea 当前就绪度、是否值得按当前 formulation 直接发展」，后者评「能否进入 G0 去执行后续门」；`f-guidance-builder-v1` 明文规定「A low current-readiness score is not a rejection by itself」。详见 `Recommendation` 字段下的 `### Startup-decision` 与 `### Hard conditions for proceed`。

`**Overall:** 3.4`

---

## Target venue/journal and assumptions:

- **目标档位**：IEEE TNNLS / Q1–Q2 类脑与神经网络期刊档（rev2 §0 明确），**不是 CCF-A 主会档**；本评审全程按此档评，不套用 CVPR/ICCV/NeurIPS 主会标尺。
- **Venue family**：类脑 / SNN 与神经网络期刊向；贡献类型由 rev2 定为「理论判据 ＋ 统一协议横评 ＋ 失效边界」（empirical / diagnostic，接受增量但须充分验证）。
- **领域**：类脑计算 × ANN→SNN 转换的误差分析、校准律适用条件、统一协议横评。
- **标尺声明（防止把「降档」误读为「抬分」，也防止把「新增证据」误读为「必须升档」）**：相对第二次的 +0.24，**逐条可追溯**为 (a) M0 本机实跑把恒等式/β\*/上界/确定性/失效边界从「纸面待办」变为「可复算数值证据」→ Method +1；(b) `matched-protocol.md` 冻结版工件兑现 ＋ M0 可复算实跑 ＋ 第 0 批/S2 硬回退 → Experimental +1。其余 8 维**零变化**。**不含**「因是第三次评审 / 因前两次已给分 / 因是修订版默认更高」任何一项；`revise`（3.7+）与 `accept-to-develop` 段未被触及。
- **阶段边界（用户硬要求）**：当前为 guidance / 实验前契约阶段。按 `f-guidance-builder-v1` 的 CCFA Startup Deliberation 规则，`startup-decision.md` 取 `proceed` / `revise` / `pivot-with-rescue-route` / `needs-evidence` 四值之一，**Only `proceed` may enter G0**；「A low current-readiness score is not a rejection by itself, but an unaddressed fatal risk, missing mechanism, unavailable baseline, or infeasible evidence plan is a block」。因此**视觉侧零正式实验是正常状态**，本评审不把它自动判 fatal，只评估 evidence plan 可信度。
- **成稿文件的可读性确认（用户要求先确认）**：`C:/code/phd-snn/auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv/writing/p7-draft.md`（450 行，完整可读）与 `C:/code/phd-snn/auto-paper/20261028-171500/Spiking-GNN-Conversion/guidance-v3.md`（58 行，完整可读）**均确认真实可读**，第二次评审「无对应成稿」的工件判断在本轮已被纠正。
- **成稿原文数值核对结果（逐项，见 `Output self-check` #19 完整表）**：ρ_n（Cora 最高 5.75）、`var(U)=0.082 vs 0.083`、`mean(U)=0.481 vs 0.5`、Hoeffding 松弛 3.2–6.7×、ρ-不变性反直觉发现、`T≤8` 达 `ANN−1.5pp` 带内，**全部在成稿原文中找到对应表述**。
- **未公开先验的隔离标注（用户硬要求，全程贯彻）**：上述成稿及其全部数值、「成稿 §3.2 已证」「成稿 §5.1 明确记录」等引用，以及「图节点分类 `T≤8` 达 `ANN−1.5pp` 带内」，一律标注为 **「用户提供的未公开先验（未发表、不充当公开证据）」**；仅可作**方法机制与理论命题的出处核对**，**不得当公开前作、不得当公开证据、不得进入任何证据强度与打分依据、不得替代本文的公开视觉实验**。
- **新增证据真实性核验（本机实跑，本会话已复核）**：
  - `protocols/m0_operator_theory_check.py`、`evidence-snapshots/m0-results.json`、`evidence-snapshots/m0-theory-check.md`、`matched-protocol.md` 均真实存在并已完整读取；`m0-results.json` 数值与 `m0-theory-check.md` 叙述内部一致，与用户任务描述中列出的 P1/P2/P5/P6 数值一致。
  - **SHA-256 口径差异（如实记录，非伪造）**：用户任务描述与 `m0-theory-check.md` 第 4 行记 `2498875f1e69312a6280671c6d5f776d7cc672b47e20135337e052cc8885b81e`；本会话对磁盘文件直接 `sha256sum` 得 `aecfa88e6741394be8b99f25b62c30e04681bacdeddbe08f20f96b592751fd1b`。根因已查明：脚本 `sha = hashlib.sha256(raw.encode("utf-8"))` 对**内存中的 LF 字符串 `raw`（不含尾随换行）**计算，而 `Path.write_text` 在 Windows 上将 `\n` 翻译为 CRLF（本文件 497 处 `\r\n`）并额外写 1 个尾随换行。将文件字节规范化为 LF 并去掉尾随换行后重算 = `2498875f...`，且 `json.dumps(json.loads(file), ensure_ascii=False, indent=2, sort_keys=True)` 的规范化重序列化 SHA 亦 = `2498875f...`，与声明值完全一致 → **文件内容未被篡改、数值未被改动**，差异纯属「字符串 raw SHA」与「磁盘文件字节 SHA」的口径/平台二义性。属可修复的复现性弱点（见 W10、H8），**不是 fatal**。
  - **P4 对数的描述差异（以文件为准）**：用户任务描述写「共 3840 对」；`m0-results.json` 每个 T 的 `checked_pairs = 384`（N=64 × (C−1)=6），5 个 T 合计 **1920 对**，`m0-theory-check.md` 第 19 行明写「共 1920 对」。依「以文件为准」采用 **1920 对（每 T 384 对 × 5）**；`violations = 0`、实测/上界最大比 `0.7766068749112546`（T=1）不变，结论不受影响。
- **本评审未做的事**：未核验 TNNLS 等目标期刊当年官方 policy / page limit / review form / deadline（依 `source-notes.md`）；未执行任何公开文献检索；未生成任何 URL / DOI；未运行任何训练或精度实验；未转录 `matched-protocol.md` §6 中已存在的任何仓库 URL（不新增、不编造）。

---

## Search basis:

- **novelty 状态**：`searched`（组件层，依据用户提供的、已由独立文献核验得到的 prior-art 结论；沿用第一次与第二次的判定）。
- **边界（必须写明）**：
  1. 证据来源为**用户提供的独立文献核验结论**，本评审会话未重新执行公开检索；故 closest-work 证据属 `user-provided only`，novelty 判定按用户指令记为 `searched`。二者不矛盾：前者是证据来源，后者是状态标签。
  2. 覆盖边界以用户列出的核验清单（8 条 closest-work）为限：覆盖的是**数学组件归属层**（β\*、零期望偏置、精确等式、确定性计数、两阶段、跨 CNN+GCN 归谁）。
  3. **推论层 `not searched`（沿用第二次的新增边界，M0 未改变此项）**：T1/T2/κ_n 作为「推论」本身，其 novelty 未经针对检索（如「非行随机算子上的 conversion bias」「相对误差对聚合尺度不变」「行和/行范数比判据」是否已被 2025–2026 工作给出）。**M0 是数值核验，不是文献检索，对此项零贡献**。故依 `strict-idea-review.md`「Cap novelty at 3 if closest work was not searched and novelty is decision-critical」，**本评审 novelty 维持封顶 3、置信度 3**。
  4. 依 `privacy-and-evidence.md`，未把未发表的私有 idea 表述放入任何检索查询；依 `source-notes.md`，closest-work 表不提供本轮未核验的链接 / DOI（禁止编造 URL）；不引用 MDPI 来源。
- **literature status label**（checklist #3）：`searched`（组件层）／`user-provided only`（本会话检索动作用）／**推论层 `not searched`**；非 `partially searched`；不做 `high novelty` 断言。
- **public-safe queries**：本会话未执行，无查询记录；如后续需要，按 `strict-idea-review.md` 应以通用公开关键词先行（ANN-to-SNN conversion bias under non-row-stochastic operators / row-sum weighted margin shift / scale-invariance of relative conversion error），不粘贴私有措辞。
- **source policy**：仅使用用户提供的 primary venue/year 信息作为 prior-art 锚点；不把 citation count 当质量；不把推论当事实；**成稿 / 内部数值一律为「用户提供的未公开先验（未发表、不充当公开证据）」，不进入 closest-work 的公开证据层**。

---

## Stage and development potential:

```text
Current conference readiness: low
Development potential: medium
Main reason it is not ready: 核心判据（ρ_n/T 单调、κ_n 大样本欠校准）在真实训练网络上未测；T1/T2/κ_n 的「prior-art 无法得到」质疑未被 M0 触及；推论层 novelty 未检索；κ_n 单调性 / κ_n–T2 张力 / 两解码兼容性 / 冗余消融 / T1 非平凡性证明仍为解析层待办；视觉侧零正式实验；PASCAL/TPP 等待复现。
Best rescue route: 以 `proceed` 进 G0 后，按 G0（推论层针对检索）→ G3（M0 解析推导补齐：β* 一般 A、‖A‖ 界、T1 非平凡性、κ_n 单调性成立区间、兼容性、消融）→ G4（非重复门）→ G7（按 matched-protocol 第 0 批复现 PASCAL/TPP 并实测 conversion loss–ρ_n/T 曲线）顺序兑现；把贡献稳定锚在「可先验计算的何时失效判据 ＋ 统一横评 ＋ 失效边界」的增量诊断定位。
Evidence needed to decide: 推论层检索是否命中近邻；T1 是否可由 Deng&Gu 递归一行照搬；κ_n 单调性是否成立；统一协议横评是否显示可归因于该判据的稳定诊断能力；原版 ViG（C5）与冻结代价（R4/A6）的定量结果。
```

**readiness 与 potential 均不升档的说明（不因修订版默认上调）**：M0 与 `matched-protocol.md` 把「机制可跑路径」从**计划**推进到**已实跑 + 已工件化**，这是实质进步；但 readiness 标签仍取 `low`，因为核心判据的实证、novelty 定位、视觉侧正式实验三项就绪条件无一完成。Development potential 保持 `medium`：最佳要素（ρ-不变性解释、κ_n 判据、统一横评、失效边界）有用且核心问题不再需要重写，但「M0 未排除一行代数 objection ＋ 推论层未检索 ＋ 单调性未测」这三项未知仍在，不能断言「不改核心问题即可变 competitive」，故不升 `high`。升 `high` 的条件写在 `Confidence` 与 `Score-change conditions` 字段。

---

## Normalized idea:

| 要素 | 归一化内容（rev3：rev2 ＋ M0 实跑 ＋ matched-protocol 冻结版） |
|---|---|
| Problem | 当传播算子固定、非负、线性但行和 ρ_n ≠ 1 时，为行随机（ρ=1）算子导出的转换校准律（偏置、阈值缩放、量化步长）是否仍最优？中心问题不声称覆盖数据依赖 / 动态 / 非线性算子。 |
| Gap | 既有 ANN→SNN 误差分析与校准律几乎全部在行随机、逐元素算子上推导（QCFS / FTBC / TPP / Parallel / DCGS / AdaFire）；ρ_n ≠ 1 的视觉图骨干与图消息传递缺少统一协议下的系统检验与「何时失效」判据。 |
| Root challenge | ρ_n ≠ 1 时，为 ρ=1 导出的零期望偏置 / 阈值缩放不再自动成立；系统误差经 A 传播后如何随行和变化、相对误差是否随之放大，缺少可先验计算、逐节点可检验的刻画。 |
| Insight（声称） | T1：`β*=θ/(2T)` 与 ρ 无关，但均值误差传播过 A 后 margin 平移按 ρ_n 加权；T2：相对误差由 `‖a_n‖₂‖DW‖₂/(TΔ_n)` 控制、ρ-不变（「用户提供的未公开先验（未发表、不充当公开证据）」中记录的原预测被实测推翻）；由此定义 `κ_n = ρ_n/‖a_n‖₂`，预测 ρ=1 校准律在 κ_n 大且 T≤4 时系统性欠校准、conversion loss 差距随 `ρ_n/T` 单调增大，ρ≈1 的 CNN 上非劣效。 |
| Method mechanism | 继承精确恒等式 `B̂₂−B₂ = A(E₁W₂)`（Dual-Phase 式）、`β*=θ/(2T)`（Deng&Gu）、零期望偏置（QCFS/FTBC）、膜电位累加解码、确定性精确计数（PASCAL）、两阶段（TPP/SpikeConverter）、跨 CNN+GCN（One-Spike SNN）——**全文不声称发明其中任何一项**。视觉侧冻结 KNN 图、线性化聚合，明写为「构造该算子类成员的手段」；图侧用 GCN 消息传递；原版动态 / 非线性 ViG 明写为失效边界诊断（不进主结果、不得删）。**新增**：M0 实跑 `m0_operator_theory_check.py`（NumPy 2.4.4 / seed 20261110 / N=64,H=24,C=7,θ=1.0）在 ρ∈{0.5,1,2,5,10}×T∈{1,2,4,8,16} 上验证 P1–P6；`matched-protocol.md` 冻结版 v1 规定唯一比较协议（B1–B5 臂、§3 同 teacher/T/θ/calibration、§4 唯一 conversion loss 口径 + 5 seeds + bootstrap R=5000 + sign-flip 1000 + BH q<0.05、§6 第 0 批、§7 A1–A7 消融、§8 S1–S7 停止回退）。 |
| Expected evidence | matched-protocol 统一横评（所有基线含自行复现 PASCAL/TPP/CS-QCFS/ECL，在同一批固定骨干、同 T/θ/calibration 数据、同 conversion loss 定义下重跑）；M0 已有的 P1 恒等式残差、P2 β\*、P4 上界、P5 确定性、P6 失效边界；**待补**：conversion loss–ρ_n/T 单调性、κ_n 逐节点欠校准率、C5 原版 ViG 边界、R4/A6 冻结代价、A5 组件消融、推论层检索。 |
| Limitation（用户已自认 ＋ M0 自述） | 适用类仅为固定、非负、线性算子；**M0 不训练、不报告分类精度、不证明能耗、不证明 ρ_n/T 单调判据在真实训练网络成立**；视觉侧零正式实验；ImageNet-1K 不可得；`matched-protocol.md` §10「明确不做」；P5 的 Bernoulli 对照为简化时变概率实现，非 TPP 官方代码逐字复现。 |
| 内部先验（隔离标注） | 图节点分类 `T≤8` 达 `ANN−1.5pp` 带内；成稿 `p7-draft.md` / `guidance-v3.md` 中 ρ_n=5.75、sum 聚合 ρ≈169、`var(U)=0.082 vs 0.083`、`mean(U)=0.481 vs 0.5`、Hoeffding 3.2–6.7×、ρ-不变性反直觉发现、`T≤8` 达 `ANN−1.5pp` 带内、以及「成稿 §3.2 / §5.1」引用 —— 均为「**用户提供的未公开先验（未发表、不充当公开证据）**」，仅作方法机制与理论命题出处核对，不进入 evidence / 打分依据 / 公开实验替代。 |

---

## Closest prior art table:

按 `strict-idea-review.md` 的 closest-work 字段逐条列出 8 条（3–8 要求上限），依据第一次报告与用户提供的已核验结论，**针对 rev3（M0 实跑后）重新评估 Overlap / Remaining delta / Needed differentiation**。**Link/source 统一说明**：venue/year 与「已做的事」均来自**用户提供的独立文献核验结论**，本会话未执行公开检索、未附 URL/DOI、不编造链接；依 `privacy-and-evidence.md` 不将未发表 idea 文本用于查询。成稿「用户提供的未公开先验（未发表、不充当公开证据）」不计入本表公开证据层。

**1**
- Closest work: Deng & Gu
- Venue/year: ICLR 2021
- Link/source: 用户提供的已核验 prior-art 结论（本轮未检索 URL/DOI）
- What it already does: `β* = θ/(2T)` 与逐层误差递归。
- Overlap with user idea: rev2 已归功 β\*；T1 起点 `E[E₁]=β−1/(2T)` 与「把误差经传播算子递推」直接来自该脉络；核心恒等式是该递归的矩阵写法。
- Remaining novelty delta: T1 声称把递归里的（行随机）归一化矩阵换成一般 A 后给出 ρ_n 加权 margin 偏置。**M0 的 P2 数值（`mean_margin_shift_no_bias` 在 T=1 由 ρ=0.5 的 −0.7182 放大到 ρ=10 的 −19.2461）恰是 `A·1=ρ_n·1` 的直接后果，未出现该递归推不出的新项** → delta 仍取决于 G3 的非平凡性证明。
- Risk to the idea: high
- Needed differentiation: 在 G3 给出 T1 相对 Deng&Gu 递归的**非平凡性证明**（该结论在 ρ=1 文献中退化消失、且带来其无法给出的可证伪预测），而非仅把归一化 A 换成一般 A。

**2**
- Closest work: QCFS
- Venue/year: ICLR 2022
- Link/source: 同上
- What it already does: 零期望误差偏置。
- Overlap with user idea: T1 的 `E[E₁]=β−1/(2T)` 即该结论，rev2 已归功；M0 P2 的 `mean_E1_no_bias ≈ −1/(2T)` 与 `mean_E1_with_beta_star ≈ 1e-3` 是该结论的数值复现。
- Remaining novelty delta: 仅剩「该余数按 ρ_n 加权」这一观察；M0 未给出 QCFS 在 ρ_n≠1 上失效的可测反例（P2 只测 β=0 vs β\*，未跑 QCFS 转换方法）。
- Risk to the idea: high
- Needed differentiation: 在 matched-protocol 下把 QCFS 作为必比基线，展示 ρ_n≠1 上的校准差异，并证明「按 ρ_n 加权」是有确定方向的 margin 偏置而非幅度噪声。

**3**
- Closest work: FTBC
- Venue/year: ECCV 2024
- Link/source: 同上
- What it already does: 零期望误差偏置（较新视觉侧版本）。
- Overlap with user idea: 同上；且是 matched-protocol §6 第 1 批必比基线。
- Remaining novelty delta: 无独立 delta。
- Risk to the idea: medium
- Needed differentiation: 在统一协议下展示 ρ_n≠1 上的校准差异；「用户提供的未公开先验（未发表、不充当公开证据）」中把 β\* 机制归于 FTBC，本文沿用归功。

**4**
- Closest work: Dual-Phase
- Venue/year: IEEE TNNLS 2024
- Link/source: 同上
- What it already does: 膜电位累加解码替代计数读出 ＋ 精确误差等式。
- Overlap with user idea: rev2 继承的精确恒等式 `A(E₁W₂)` 是该「精确等式」在抽象 A 上的写法；解码组件亦归功。**M0 P1 验证的正是该等式在固定线性 A 上的精确性（残差 ≤ 9.88e-15）**，即 M0 强化的是继承命题的数值可信度，不是新命题。
- Remaining novelty delta: 仅剩「把等式推广到 ρ_n≠1 的 A 并读出 T1/T2 两条推论」。
- Risk to the idea: high
- Needed differentiation: 给出 Dual-Phase 等式在 ρ=1 下读不出、在 ρ_n≠1 下才出现的推论（T2 的 ρ-不变性解释），并数值验证；**注意 M0 P3 未干净复现该强主张（见 Novelty delta）**。

**5**
- Closest work: PASCAL
- Venue/year: TMLR 2025
- Link/source: 同上
- What it already does: 确定性精确计数。
- Overlap with user idea: rev2 已放弃「确定性化」作为贡献，改列为 `matched-protocol.md` **第 0 批 must-rerun 基线（无官方码、自行复现）**；M0 P5 只验证确定性 s[t] 的代数性质（Σs=n 命中率 100%、重建误差 `0.49999812148232436`、条件方差 0），不主张相对 PASCAL 的新数学性质。
- Remaining novelty delta: rev2 相对 PASCAL 不再主张数学组件 delta；**但 rev2 §1 可证伪条件第 4 条仍写「与 PASCAL / TPP 等价 → 判据被推翻 / pivot」，范畴错位残留**（协议 §8 S4 已在协议层改为单调性裁决，两处口径未统一，见 W5）。
- Risk to the idea: medium
- Needed differentiation: 把证伪条件统一改写为针对「判据」的可测量；并补齐 PASCAL 复现验收锚（见 W2 / H3）。

**6**
- Closest work: TPP（含 SpikeConverter, AAAI 2022 的两阶段脉络）
- Venue/year: ICML 2025（SpikeConverter: AAAI 2022）
- Link/source: 同上
- What it already does: 两阶段转换框架。
- Overlap with user idea: 同上；rev2 已归功两阶段，TPP 列为 `matched-protocol.md` **第 0 批 must-rerun**（§6 已记录官方仓库，本评审不转录 URL）。
- Remaining novelty delta: 同上（范畴错位残留）。
- Needed differentiation: 在 matched-protocol 中直接对比 TPP，但把比较对象定位为「为 ρ=1 导出的校准律」而非「确定性第二相」；M0 自述 P5 的 Bernoulli 对照「是简化的时变概率实现，不是 TPP 官方代码的逐字复现」，不得当 TPP 复现证据。

**7**
- Closest work: One-Spike SNN
- Venue/year: IEEE TETC 2024/2025
- Link/source: 同上
- What it already does: 跨 CNN + GCN 的 ANN→SNN 转换。
- Overlap with user idea: 削弱「同一转换思路跨视觉与图骨干」的新颖性；rev2 已归功，只主张「同一固定线性 A ＋ 统一协议 ＋ 算子类成员的构造」。
- Remaining novelty delta: 仅剩「用 ρ_n≠1 判据贯穿两类骨干」这一诊断视角。
- Risk to the idea: medium
- Needed differentiation: 说明相对 One-Spike SNN，「何时失效判据」提供了其没有的、可先验计算的分析结论；「用户提供的未公开先验（未发表、不充当公开证据）」中的 GNN 转换结果不得充当前作。

**8**
- Closest work: Parallel Conversion / DCGS / AdaFire（横评对手集合）
- Venue/year: ICML 2025 / ICML 2025 / AAAI 2025
- Link/source: 同上
- What it already does: 2025 年主流 ANN2SNN 转换方法，均有官方代码可重跑（用户提供，`matched-protocol.md` §6 已记录仓库，本评审不转录 URL）。
- Overlap with user idea: 构成 matched-protocol 必须对齐的基线集合，且代表该子领域 2025 年饱和度；这些方法的校准律均为 ρ=1 假设，恰是 rev2 中心问题要检验的对象。
- Remaining novelty delta: 无（横评对象，不是被超越对象）；风险在于横评是否显示 κ_n 判据的诊断能力。
- Risk to the idea: medium
- Needed differentiation: 统一协议须含同骨干、同 T、同 θ、同 calibration 数据（`matched-protocol.md` §3 已写死），且须解决「ρ=1 校准律在 ρ≠1 聚合上如何适配」的语义规则（见 W3 / H4）。

**其他纳入但非最近邻的锚点（用户提供）**：CS-QCFS、ECL（无代码需自行复现，`matched-protocol.md` §6 第 2 批）；CIFAR10-DVS、Planetoid 三图、Tiny-ImageNet 等数据集约束；G2 排除清单。均按用户提供事实记录，不扩展、不编造。

---

## Novelty delta:

**状态**：`searched`（组件层）／**推论层 `not searched`**（M0 未改变此项）。**结论**：减去最近邻工作后，rev3 的 novelty 相对 rev2 **无实质变化**——仍为「**薄但真实、可证伪的分析增量**」，**仍不构成「prior-art 无法得到的新数学结果」**。

| 声称的 delta | rev3 复核结论 | 判定（相对 rev2） |
|---|---|---|
| T1 · ρ 加权系统性误差 | 由已知恒等式 `A(E₁W₂)` ＋ 已知零期望偏置 `E[E₁]=β−1/(2T)` ＋ 行和定义 `A·1=ρ_n·1` 直接展开得到。**M0 P2 的数值（margin 平移随 ρ 放大、β\* 与 ρ 无关）恰与这一「一行代数」预期一致，未出现新项**；M0 未提供非平凡性证明、未提供 QCFS 在 ρ_n≠1 上的失效反例。 | **未变**（仍是「假设放宽后的代数展开」；M0 提供数值确认，非 novelty 增量） |
| T2 · 相对误差 ρ-不变 | margin Δ_n 由同一聚合 logits 算出，分子分母含同一聚合尺度 → 尺度抵消；属解释性结论。**M0 P3 未干净复现该强主张**（见下）。 | **未变，且新增张力证据** |
| κ_n = ρ_n/‖a_n‖₂ 判据 | 把绝对按 ρ 加权（T1）与相对 ρ-不变（T2）统一到一个先验可算、逐节点可检验的量，并给出可证伪的单调预测；在 ρ=1 文献框架里该量恒为常数。这是 rev1 完全没有的分析层。 | **未变**（M0 未测 κ_n 单调性、未解 κ_n–T2 张力） |
| matched-protocol 统一横评 | 属评估 / benchmark 贡献，真实且可测；**`matched-protocol.md` 冻结版 v1 现已真实存在**（第二次的「工件不存在」已消除）。 | **工件兑现**（设计/工件层，非 novelty 层） |
| 失效边界诊断（C5 / B4） | 真实、增量、可测；**M0 P6 把它从文字声明推进为可测数值预测**：固定线性 A 残差 `1.1657341758564144e-15`，每步动态 A_t 残差 `0.7476370778501276`，max 非线性聚合「脉冲率输出 vs ANN 输出」最大绝对偏差 `1.105089450044243`。 | **实质推进**（增强 F1 自洽性，non-novelty 层） |

### 特别回答：M0 是否改变了「T1/T2/κ_n 是否构成 prior-art 无法得到的新推论」这一 F2 核心质疑？

**明确结论：没有改变，且部分证据反而强化了原质疑。** M0 是「固定线性算子类上的代数/概率命题与失效边界」的**数值核验**，不是 prior-art 检索、不是非平凡性证明、不是推论层检索、不是真实网络判据实测。三点具体：

1. **M0 没有、也不可能回答「prior-art 能否推出」**。该问题需要 (a) 推论层针对检索，(b) T1 相对 Deng&Gu 递归的非平凡性证明。M0 脚本不含任何文献比对或证明。依 `strict-idea-review.md`「Cap novelty at 3 if closest work was not searched」，**novelty 维持 3 / conf 3**。
2. **P2 数值与「一行代数」objection 相符，未排除它**。`make_operator` 把行和缩放为 ρ，`shift0 = (A@(E0@W2))[c\*] − (A@(E0@W2))[rival]`，数值显示 `mean_margin_shift_no_bias` 随 ρ 放大（T=1：ρ=0.5 为 −0.7182071214201277，ρ=10 为 −19.246128582448655）、`mean_E1_with_beta_star` 各格约 1e-3 趋零、`beta_star` 仅随 T 变（0.5 / 0.25 / 0.125 / 0.0625 / 0.03125）与 ρ 无关。这些正是「`A·1=ρ_n·1` ＋ QCFS 零期望偏置」的**可预期代数后果**。M0 确证了「成立」，但「成立」与「prior-art 推不出」是两个命题。
   - 附带一处**过表述需收敛**：`m0-theory-check.md` 写「加 β\* 后系统项在各 ρ 下同时趋零」；JSON 中 `mean_E1_with_beta_star` 确趋零，但 `mean_margin_shift_with_beta_star` 在 T=1/ρ=10 仍为 `−1.4342617365394417`、T=8/ρ=10 为 `−0.10160205236319639`（非零）。精确表述应为「**E₁ 均值的系统项趋零；margin 平移残差仍随 ρ/T 变化**」。此残差与 T1 的 ρ 加权主张一致，但「完全消除」措辞须收敛。
3. **P3 未干净复现 T2 的 ρ-不变强主张，反而暴露 κ_n–T2 张力（第二次 Q3 的实证回声）**。JSON `P3_relative_error_rho_invariance`（T=4）：
   - `mean_relative_error`：ρ=0.5 → `0.3056259618769926`；ρ=1.0 → `0.5647821132047228`；ρ=2.0 → `0.31873982388454947`；ρ=5.0 → `0.30343107673628567`；ρ=10.0 → `0.259106600887706`。**跨 ρ 变化近 2.2 倍，且 ρ=1 处反常最高**，并非恒定。
   - `argmax_agreement`：`1.0 / 0.921875 / 0.828125 / 0.984375 / 0.90625`，非单调、在 0.828–1.0 间波动。
   - **设计局限**：脚本对每个 ρ 重新调用 `make_problem(rho)`（RNG 延续但 B1 / W2 独立采样），并非「固定同一 problem、只缩放 A 的行和」。因此 P3 **在构造上不能严格检验「分子分母同尺度抵消」意义上的 ρ-不变性**，只能给方向性佐证。
   - 故 `m0-theory-check.md` 第 16 行「这复现了成稿 §5.1 记录的反直觉结论」应降级为「**提供了方向性、非严格的数值佐证**」；「用户提供的未公开先验（未发表、不充当公开证据）」中的 §5.1 表述仅作理论命题出处核对，不作公开证据。

**因此 F2 判「部分解决」而非「已解决」/「仍未解」**：M0 把第二次「核心推导全在 M0 未证」中的**数值/代数子集**兑现（P1/P2/P4/P5/P6），使 F2 的「未证」一半得到实质缓解、并使 F1 的失效边界从声明变可测；但 F2 的「novelty 是否为 prior-art 无法得到的新推论」一半**完全未动**，且 P2/P3 数值未提供反证、反而与「一行代数」及 κ_n–T2 张力相容。故 novelty / conceptual / acceptance 三维**一分不升**。

**明确不可声称的内容（用户硬要求，rev2 已遵守，本评审追加）**：不声称发明 `β* = θ/(2T)`、逐层误差递归、零期望误差偏置、膜电位累加解码、精确误差等式、确定性精确计数、两阶段框架、跨 CNN+GCN 转换；**追加**：不声称 M0 证明了 ρ_n/T 单调判据、不声称 M0 排除了「一行代数」objection、不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」（除非 G3 解析证明 ＋ G0 推论层检索 ＋ G7 单调性实测三者同时支持）。

**最强 novelty delta 的诚实表述（不变）**：在显式写出「仅适用固定、非负、线性 ρ_n≠1 算子」的前提下，本 idea 剩下的可辩护贡献是「一个可先验计算、可证伪的『何时失效』判据（κ_n），配以 T2 的 ρ-不变性解释、统一协议横评与失效边界诊断」——这是一个**窄、增量、以诊断与协议为主**的贡献，按 Q1–Q2 期刊档可接收，但不是新理论组件。

---

## Serious blockers:

**A. Fatal risks（未解结构性 fatal）：0 条。**

依 `calibration.md` / `strict-idea-review.md` / `f-guidance-builder-v1`「Only `proceed` may enter G0 … an unaddressed fatal risk, missing mechanism, unavailable baseline, or infeasible evidence plan is a block」，逐条核对：

| 原 fatal / gate | rev3 状态 | 是否构成未解 fatal |
|---|---|---|
| F1 主张—适用条件错位 | **已解决**。rev2 主张与 A1/A2 一致；M0 P6 把不适用类变成可测数值边界；`matched-protocol.md` §2 把 B4 原版 ViG 定为失效边界「不进主结果、不得删」。 | 否 |
| F2 novelty 重述 / 组合 | **部分解决，降级为可修复弱点**（第二次已降级，M0 推进数值层、未推进 novelty 层）。T1/T2/κ_n 提供可证伪判据，不再是纯重述；「一行代数」objection 未排除、推论层未检索、单调性未测。 | 否（依 `strict-idea-review.md`「Do not mark abandon / do not translate mechanism under-specified into fatal」，且第二次已判非 fatal） |
| F3 横评可比性两难 | **已解决（设计层 ＋ 工件层）**。`matched-protocol.md` 冻结版 v1 真实存在，§2–§4 写死同骨干/同 teacher/同 T/同 θ/同 calibration/同 conversion loss 定义，§6 第 0 批 must-rerun，§8 S2 硬回退。 | 否 |
| `calibration.md` fatal gate: Novelty ≤ 2 高置信 | 不触发（3 / conf 3） | 否 |
| Method soundness ≤ 2 | 不触发（4） | 否 |
| Experimental convincibility ≤ 2 且无替代证据 | 不触发（4，且 M0 实跑 ＋ evidence plan 完备） | 否 |
| Venue fit ≤ 2 / Feasibility ≤ 2 | 不触发（4 / 4） | 否 |
| No identifiable insight beyond applying known modules | **不硬触发但临界**：T1/T2/κ_n 提供薄但可辨识的判据；M0 P2 未排除「一行代数」 | 否（临界，须由 G3 非平凡性证明解决） |
| Internal mechanism conflict | **不硬触发但临界**：κ_n–T2 张力、冻结 KNN vs 表征力已由 R4/C5/A5/A6 显式管理，但张力未量化；M0 P3 数据显相对误差随 ρ 变化近 2.2 倍 | 否（临界） |
| Novelty unknown 且无 closest-work search | 不适用（组件层 `searched`；推论层 `not searched` 已封顶 novelty 3 / conf 3，按用户指令不升级为 `needs-literature-search`） | 否 |

**结论：无未解 fatal risk，满足进 G0 的唯一硬标准**（详见 `Recommendation` 字段 `### Startup-decision`）。

**B. 准 fatal 级最重弱点（压住升档；按 guidance 阶段属 G0/G3/G4/G7 可执行产物，不构成进 G0 阻塞）**

- **Q1′ · 核心判据仍未被实测、M0 只兑现数值子集**：M0 证明恒等式精确成立与失效边界，但**未证明 ρ_n/T 单调判据在真实训练网络成立**（M0 自述第 35 行）。仍缺：一般 A 下 β\* 的严格解析推导、`‖A‖` 误差上界的证明（M0 P4 只做数值检查 0 违反，未重证上界）、T1 相对 Deng&Gu 的非平凡性证明、κ_n 单调性证明与成立区间、两解码兼容性命题、A5 冗余消融、推论层针对检索。一个以理论判据为核心贡献的 idea，其**解析层与系统层**仍未闭合。
- **Q2′ · 推论层 novelty 未检索 ＋「一行代数」objection 未被排除**：M0 零贡献；P2 数值与该 objection 相符。若 G0 检索命中近邻或 G3 证明 T1 可一行照搬，F2 回潮为 fatal、novelty 3→2、整体回落约 3.0–3.1。
- **Q3′ · κ_n 与 T2 的内部张力未量化，且 M0 P3 提供新的张力证据**：相对误差随 ρ 变化 `0.2591–0.5648`、argmax 一致率 `0.828–1.0` 波动；P3 设计（每 ρ 重采样 problem）不能严格检验尺度抵消。若 `‖a_n‖₂` 随 ρ_n 增长使 κ_n 近似不变，「随 ρ_n/T 单调增大」可能不成立。
- **Q4′ · 证伪条件范畴错位（协议层已修正、主卡原文残留）**：`matched-protocol.md` §8 S4 已把裁决改为「主判据（conversion loss 差距随 ρ_n/T 单调）连续落 failure → `pivot-with-rescue-route`」，**实质消化了 W6**；但 rev2 §1 第 4 条「与 PASCAL / TPP 等价 → 判据被推翻 / pivot」原文未改，两处口径未统一。

**C. Fixable weaknesses（可修复，不改变中心主张）**

- W1 视觉侧零正式实验（guidance 阶段正常状态，按硬要求**不判 fatal**，记为证据缺口）→ G7 按统一协议补完整视觉侧实验。
- W2 `matched-protocol.md` §6 第 0 批 PASCAL「无官方码、自行复现」，但**缺可判定的复现验收锚**（同批 TPP 有官方仓库、第 1 批 QCFS 有 `91.18%@T=2 / 93.96%@T=4` 回归测试范式，PASCAL 无等价阈值）；§8 S2 只定义「失败 → needs-evidence」，未定义「成功」。
- W3 **可比性适配规则未补**：协议控制了 teacher / T / θ / calibration / 骨干，但**未规定「为 ρ=1 网格算子设计的转换校准律（QCFS/FTBC/TPP/PASCAL…）在 ρ_n≠1 的 B2/B3 聚合上如何原样应用、不得针对 ρ 重调、无法实现则单列」**。而检验「ρ=1 校准律是否失效」恰是中心问题，若适配方式由作者自选，存在选择性自由度，可能污染横评归因。
- W4 核心判据「conversion loss 差距随 ρ_n/T 单调」的**操作化未写入 §4 指标定义**：缺趋势检验方法、比较单元（跨 ρ 网格 / 跨方法）、统计判据；§8 S4 使用了它但未定义测法。
- W5 rev2 §1 第 4 条与 `matched-protocol.md` §8 S4 的证伪口径未统一（同 Q4′）。
- W6 冻结 / 线性化相对原版 ViG 的 ANN teacher 精度代价（R4 / A6）未量化，协议 §2 只要求「在论文中量化、不得隐瞒」，尚未兑现。
- W7 组件冗余（膜电位累加解码 vs 确定性计数 s[t]）未消融（A5 待办）；M0 P5 只验证确定性性质，未做两者对比。
- W8 推论层 novelty 未针对检索（G0 / G4 待办）。
- W9 官方当年 venue policy / review form 未核验（成文前须核验）。
- W10 **证据工件口径一致性**：(a) `m0-results.json` 的 SHA-256 声明值与 `sha256sum` 文件字节值因 Windows CRLF ＋ 尾随换行而不一致（已查明非篡改，见 `Target venue/journal and assumptions`），须统一记录口径；(b) 用户任务描述「3840 对」与文件「1920 对」不一致（以文件为准）；(c) `m0-theory-check.md` 三处轻微过表述（P2「系统项同时趋零」、P3「复现 §5.1 反直觉结论」、P5「Bernoulli 对照方差 >0」在 T=16 时 JSON 为 `0.0`）——须收敛措辞；(d) `m0-theory-check.md` 第 34 行两个 bullet 挤在同一行（格式）。
- W11 成稿「用户提供的未公开先验（未发表、不充当公开证据）」隔离标注须在 guidance / 成文全过程贯彻；第二次 W11「全 `<TBD>` 纪律冲突」在成稿真实存在后已澄清为「跨项目内部校准引用」，仍不得写入公开证据 / 结果栏。

**D. 隔离项**：图节点分类 `T≤8` 达 `ANN−1.5pp` 带内、成稿 `p7-draft.md` / `guidance-v3.md` 及其全部数值，均为「**用户提供的未公开先验（未发表、不充当公开证据）**」，既非 fatal 也非 weakness 证据，不参与打分。

---

## Per-expert reviewer notes:

> 以下 5 个必需角色**独立**给出判断，先各自发言、后综合（依 `expert-panel.md` 与 `review-output-standards.md` 的 panel 纪律）；另依 `expert-panel.md`「Add only when relevant: Theory/proof expert」加第 6 位 **Theory / Proof Expert**（M0 为理论核验，直接相关）。每个角色的 **Score tendency（分数倾向）与 Confidence（置信度）分开报**，不强行制造一致、赞扬或拒稿；每块附 `Score-change condition`。全部内容为本红队 panel 的独立判断，非真实审稿记录。

**Field Expert**
- Role: 领域专家（类脑计算 × ANN2SNN 转换）
- Score tendency: 3 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: 中心问题「ρ_n≠1 时 ρ=1 校准律是否仍最优」真实、具体、可测且与方法能力对齐；「何时失效」框架对把 GNN / ViG 用于 SNN 的社区有实用价值；M0 P6 把失效边界从声明变数值，是领域内少见的诚实自限。
- Strict rejection-grade concern: **算子类代表性**。冻结 KNN 的 ViG 已失去数据依赖表征（R4 自认削弱），ρ≈169 的 sum 聚合是「用户提供的未公开先验（未发表、不充当公开证据）」中的人为极端设置；审稿人会问「固定线性 ρ_n≠1 算子类在真实部署中占多大比重」。M0 未回答（只在合成随机 A 上验证）。
- Anchor: rev2 §1 Bottleneck、A1/A2、R4；`m0-results.json` P6；第一次 Field 专家「gap 是理论瓶颈还是工程缺口」之问。
- Why this matters: 决定 Problem importance 能否从 3 升 4；写完 related work 后 gap 是否还站得住。
- Fatal risk if any: 无独立 fatal（F1 已消解）。
- Most valuable repair or pivot: 给出「非行随机算子在主流 GNN / ViG 中普遍存在」的**公开证据** ＋ 冻结 KNN 代价量化（R4/A6），把问题从「为套恒等式而构造的类」锚到「真实部署类」。
- Score-change condition: 上述公开证据 ＋ R4 量化落地 → 3→4；不承诺。
- Development-potential note: 中；问题代表性可提升主轴，不消除 F2。

**Method Expert**
- Role: 方法专家（误差分析 / 机制正确性）
- Score tendency: 4 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: **M0 是实质进步**：P1 在 25 格上恒等式残差最大 `9.880984919163893e-15`（浮点精度内）、P2 β\* 与 ρ 无关且 E₁ 系统项趋零、P4 Hoeffding 上界 0 违反（最大比 `0.7766068749112546`）、P5 确定性 Σs=n 命中率 100% / 重建误差 `0.49999812148232436` / 条件方差 0、P6 失效边界显著非零（`0.7476370778501276` / `1.105089450044243`）。第二次给 2–3 分的核心理由「核心定理全未证」中的**代数/概率数值子集**已被实跑兑现，且脚本可复算（seed 20261110、NumPy 2.4.4）。
- Strict rejection-grade concern: **M0 是数值核验，不是严格推导**。仍缺：一般 A 下 β\* 解析推导、`‖A‖` 上界的证明（P4 只检查未重证）、T1 相对 Deng&Gu 的非平凡性证明、κ_n 单调性证明、两解码兼容性、A5 消融；更关键的是 **M0 明确不证明 ρ_n/T 单调判据在真实训练网络成立**，而那正是核心贡献。另 P2 的 margin 平移残差在 T=1/ρ=10 仍 `−1.4342617365394417`，P3 相对误差随 ρ 变化近 2.2 倍，说明「系统项趋零 / ρ-不变」的强表述需收敛。
- Anchor: `m0-theory-check.md`「本核验不能证明什么」第 33–36 行；`m0-results.json` P1–P6；rev2 §1 R1/R2/R3、M0；第二次 Method 专家意见。
- Why this matters: 数值 soundness 已闭合，但解析 soundness 与核心判据未闭合；一个以理论判据为核心贡献的 idea，其定理层仍待 G3。
- Fatal risk if any: 若 G3 证明 T1 可一行照搬、或 G7 单调性被推翻 → F2 回潮为 fatal，本维 4→3。
- Most valuable repair or pivot: 在 G3 完成 M0 解析层：β\* 一般 A 推导、`‖A‖` 界证明、T1 非平凡性、κ_n 单调性成立区间（含 κ_n–T2 张力）、两解码兼容性、A5 消融；把 P3 改为「固定 problem 只缩放 A 行和」的受控设计以严格检验尺度抵消。
- Score-change condition: G3 全过 ＋ 单调性实测成立 → 4→5（本维）；反向则 4→3；不承诺。
- Development-potential note: 中—高；纸面为主、无算力成本，是最可修复的一条。

**Experiment Expert**
- Role: 实验专家（证据设计 / 基线 / 可行性）
- Score tendency: 4 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: **`matched-protocol.md` 冻结版 v1 真实存在且相当完备**：§2 B1–B5 臂（B4 原版 ViG 为失效边界、不得删）、§3 唯一 teacher ＋ 同 T 网格 `{1,2,4,8,16}` ＋ 同 θ/scale/calibration（固定 512 张 train 子集、种子固定）＋ QCFS 重训同种子同增广、§4 唯一 `conversion loss = ANN top-1 − SNN top-1`（pp，越低越好）＋ 5 冻结 seeds ＋ 配对 bootstrap `R=5000` ＋ sign-flip 1000 ＋ BH `q<0.05`、§5 防泄漏划分、§6 **第 0 批 PASCAL（自行复现）＋ TPP（官方码）must-rerun 且「二者任一未跑通不得进主表」**、§7 A1–A7 消融（A7 专检 ρ≈1 CNN 臂非劣效）、§8 S1–S7 停止回退、§9 复现产物、§10 明确不做。叠加 M0 可复算实跑，evidence plan 可信度显著高于第二次。
- Strict rejection-grade concern: 四处具体缺口：(a) **W3** 协议未规定 ρ=1 校准律在 ρ≠1 聚合上的适配语义（同 θ/calibration 只控数据侧，未控「校准律适配」侧，恰恰是中心问题所在）；(b) **W2** PASCAL 无官方码且缺复现验收锚，S2 只定义失败回退、未定义成功；(c) **W4** 核心判据「单调」未操作化写入 §4 指标定义，§8 S4 用了却未定义测法；(d) 视觉侧零正式实验、PASCAL/TPP/CS-QCFS/ECL 待复现、C5/R4/A6 待实测（按用户硬要求，guidance 阶段不判 fatal）。
- Anchor: `matched-protocol.md` §2–§10；`m0-results.json`；rev2 §1 Falsification 第 4 条与 §8 S4 口径差；用户硬要求（guidance 阶段只评 plan 可行性）。
- Why this matters: plan 可信但含三处「可执行性定义」缺口；阴性结果（单调性不成立）会直接推翻核心判据。
- Fatal risk if any: 无独立 fatal（按硬要求，不把零实验判 fatal）。
- Most valuable repair or pivot: 按 H3/H4/H5 补「适配语义规则」「PASCAL 验收锚」「单调性操作化」；第 0 批复现 PASCAL/TPP；报告 conversion loss–ρ_n/T 曲线、κ_n 逐节点欠校准率、C5 边界、R4 代价。
- Score-change condition: 三项定义补齐 ＋ 第 0 批跑通 ＋ 曲线支持判据 → 4→5（本维）；单调性被推翻 → 4→3；不承诺。
- Development-potential note: 高；最明确、最可执行的补齐路径。

**AC / Venue Expert**
- Role: AC / venue 专家（贡献品味 / 匹配 / 讨论后存活）
- Score tendency: 4 / 5
- Confidence: 3 / 5
- Best possible argument for the idea: 主动降到 IEEE TNNLS / Q1–Q2 档、ImageNet-1K 不再是硬要求、贡献收敛为「何时失效判据 ＋ 统一横评 ＋ 失效边界」单一主轴；`matched-protocol.md` 的冻结版 ＋ S1–S7 停止回退对期刊审稿是加分（可复算、可审计），M0 实跑提供了理论门的可核查证据。
- Strict rejection-grade concern: (a) 贡献仍是三块并列（判据 / 横评 / 边界），主轴收敛更多在措辞而非结构；(b) 统一协议横评带 benchmark 味，混合评审中可能被读成 benchmark / 诊断短文而非理论主贡献；(c) 核心判据未实测 ＋ 视觉侧零实验，能否 survive discussion 存疑；(d) 未核验 TNNLS 当年官方 policy / review form，按通用 contribution taste 推理。
- Anchor: rev2 §0、§1 Contribution type；`matched-protocol.md` §10；prior-art venue 分布；未核验当年官方政策。
- Why this matters: venue 对齐消除了第一次的 mismatch，但 readiness 仍低，二者不可混为一谈。
- Fatal risk if any: 无独立 fatal。
- Most valuable repair or pivot: 结构上把三块贡献绑定为「一个 κ_n 判据贯穿横评与边界」的单一叙事；成文前核验当年官方政策。
- Score-change condition: 单一叙事落地 ＋ 官方政策核验 → 维持 4（本维已接近该档上限）；不承诺升 5。
- Development-potential note: 中。

**Skeptical Prior-Art Expert**
- Role: 怀疑型 prior-art 专家（novelty 坍塌 / 命名掩盖 / 是否已属已知）
- Score tendency: 2 / 5
- Confidence: 4 / 5
- Best possible argument for the idea: rev2 禁用 "Operator-Agnostic" 掩盖性命名、全文不声称发明任何已占组件、诚实记录「原预测 ρ≈169 会灾难退化、被实测推翻」（「用户提供的未公开先验（未发表、不充当公开证据）」）；T1/T2 确实是 rev1 主卡里没有的分析层；M0 数值自洽、未编造结果。
- Strict rejection-grade concern: **最强「this is already known」objection 在 M0 后完全未被削弱**：把 Deng&Gu 逐层误差递归里的（行随机）归一化矩阵换成一般非负 A，`A·1 = ρ_n·1` 立刻给出 T1 的 ρ_n 加权项，配合 QCFS 零期望偏置 `E[E₁]=β−1/(2T)` 就是 T1 的全部；T2 是分子分母含同一聚合尺度的归一化抵消；κ_n 是两个已知统计量的比值。**M0 P2 的数值正是这一「放宽 ρ=1 假设 ＋ 已知恒等式代数展开」的可预期结果**，不构成反证。追加：(a) 推论层 novelty 未经针对检索；(b) P3 未干净复现 ρ-不变（相对误差 0.2591–0.5648、argmax 0.828–1.0 波动）；(c) 成稿「用户提供的未公开先验（未发表、不充当公开证据）」中已给出 margin 定理与 ρ-不变解释，本文的 T1/T2/κ_n 与之高度同源，更需澄清「本文新推论」与「内部已有结果」的边界，避免自我重复定位。
- Anchor: 用户核验 prior-art 表（Deng&Gu / QCFS / Dual-Phase / PASCAL / TPP）；`m0-results.json` P2/P3；rev2 T1/T2/κ_n；Search basis 推论层边界；成稿隔离标注。
- Why this matters: 决定 novelty 是否 ≤ 2 与是否「beyond applying known modules」；本角色是压住 novelty 不升分的主因。
- Fatal risk if any: F2 仍是最重的一项，但本角色认同「已降级为可修复弱点」而非 fatal。
- Most valuable repair or pivot: G0 针对推论本身做公开检索（row-sum weighted conversion bias / non-row-stochastic ANN-SNN / scale-invariance of relative conversion error），并在 G3 给出 T1 相对 Deng&Gu 递归的非平凡性证明；全文一致不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」。
- Score-change condition: 推论层检索无近邻 ＋ 非平凡性证明成立 → 2→3；命中近邻或 T1 坍缩 → 维持 2 并回潮 F2；不承诺。
- Development-potential note: 低—中。

**Theory / Proof Expert（optional，因 M0 为理论核验而加）**
- Role: 理论 / 证明专家（命题—证明对应、数值证据的证明力边界）
- Score tendency: 3 / 5
- Confidence: 5 / 5（数值与文件可直接核查）
- Best possible argument for the idea: M0 把「恒等式在固定线性算子类上精确成立」证明到浮点精度（P1 25 格），把 Hoeffding 型上界验证为 sound（P4，1920 对 0 违反、最大比 0.7766），把确定性第二相的 Σs=n / 零条件方差验证为确定（P5，20,000 激活 × 5 个 T），并把失效边界量化（P6）。这些都是**真命题且证据确凿**。
- Strict rejection-grade concern: **数值验证不等于定理证明，更不等于判据成立**。P1 验证的是 `b2_snn_rate` 与 `b2_ann` 在脚本定义下恒等，属「实现—恒等式一致性」，不是对一般 A 的解析推导；P4 的 `bound` 公式直接来自「用户提供的未公开先验（未发表、不充当公开证据）」中的 §3.6，M0 只检查违反数，未证明该界；**κ_n 单调性、κ_n–T2 张力、T1 非平凡性、两解码兼容性在 M0 中完全没有对应命题**；`m0-theory-check.md` 第 35 行自认不证明 ρ_n/T 单调判据。另 P3 的受控设计缺陷（每 ρ 重采样 problem）使其不能严格检验尺度抵消。
- Anchor: `m0_operator_theory_check.py` 全文（尤其 P3 `make_problem(rho)` 逐 ρ 重采样、P6 的 `max_resid` 恒为 0 的占位实现）；`m0-results.json` P1/P3/P4；`m0-theory-check.md` 第 33–36 行。
- Why this matters: 若把「M0 实跑」误读为「核心理论已证」，会把 method soundness 与 acceptance 高估一整档；这是本轮最需要防的抬分来源。
- Fatal risk if any: 无独立 fatal；但若 G3 无法给出 κ_n 单调性的成立区间，核心判据不可证伪化，F2 回潮。
- Most valuable repair or pivot: G3 补解析层（见 Method Expert），P3 改为受控单变量设计；`max_resid` 的占位实现（`(max_B2 - max_B2)`）改为真实非线性残差定义或明确标注「未定义」。
- Score-change condition: 解析层全过 ＋ 受控 P3 复现尺度抵消 → 3→4；不承诺。
- Development-potential note: 中（纸面为主）。

**Panel Synthesis**（依 `expert-panel.md` 与 `review-output-standards.md`，不平均掉致命弱点）

```text
Agreement: 六位专家一致认为 (1) M0 与 matched-protocol.md 是真实、可核查的实质进步，F1 已解决、F3 已解决到设计+工件层、method 与 evidence plan 的可信度显著上升；(2) 但 M0 只兑现数值/代数子集，不触及 F2 的 novelty 核心，也不证明 ρ_n/T 单调判据在真实训练网络成立；(3) 一致认为不应 abandon（中心判据可测、G0/G3/G4/G7 路线可命名）；(4) 一致认为按 f-guidance-builder 的 startup 规则无未解 fatal，可 proceed 进 G0。
Disagreement: Method(4) 与 Experiment(4) 评「新增证据直接兑现的维度」；Field(3)、AC(4) 评「问题代表性 / venue 对齐后的 fit」；Skeptical(2) 与 Theory(3) 评「novelty 未变 / 数值≠证明」。分歧来自「评哪个轴」，不是对事实的分歧；未强行制造一致或赞扬。
Strongest accept axis / Decisive accept axis: 恒等式在固定线性算子类上精确成立（P1 9.88e-15）＋ 失效边界可测（P6）＋ 冻结版统一协议与第 0 批/S2 硬回退，构成一个可复算、可审计、自限清晰的 Q1–Q2 增量诊断研究契约。
Strongest reject axis / Decisive reject axis: T1/T2/κ_n 仍可读作「放宽 ρ=1 假设 ＋ 已知恒等式代数展开」，推论层未检索、κ_n 单调性未测、κ_n–T2 张力未解、P3 未干净复现 ρ-不变；若 G0/G3 结果不利，novelty 回 2、整体回约 3.0–3.1、F2 回潮为 fatal。
Score-relevant uncertainty / Unresolved evidence: G3 解析推导结果；G0 推论层检索；G7 单调性与 κ_n 逐节点欠校准率；PASCAL/TPP 复现与验收锚；C5/R4/A6 量化；官方当年 venue policy。
Most valuable next evidence: 先做 G3 纸面（T1 非平凡性 ＋ κ_n 单调性成立区间 ＋ 受控 P3），再做 G0 推论层检索，再按 matched-protocol 第 0 批复现 PASCAL/TPP 并测 conversion loss–ρ_n/T 曲线。
Final calibrated stance / Panel-calibrated recommendation: ccf-idea-reviewer = pivot-with-rescue-route（与加权 3.4 落在 calibration 3.0–3.6 段一致）；f-guidance-builder startup-decision = proceed（conditional，带 H1–H9）。
```

---

## Rubric scores:

权重取 `rubric.md` 默认表（合计 100），未作调整（无官方 venue review form 要求调整）。**标尺按 rev2 的 Q1–Q2 期刊档**；**分数与置信度分列**。

| Dimension | Weight | Score (1-5) | Confidence (1-5) | Deduction / evidence basis | Repair condition |
| --- | ---: | ---: | ---: | --- | --- |
| Problem importance | 12 | 3 | 4 | 问题与方法能力对齐（F1 已解），但算子类代表性存疑；M0 只在合成随机 A 上验证，未给「非行随机算子在主流 GNN/ViG 中普遍存在」的公开证据；R4/A6 代价未量化 | 给公开普遍性证据 ＋ R4/A6 冻结代价量化 |
| Novelty against likely prior work | 14 | 3 | 3 | T1/T2/κ_n 是薄但真实的可证伪判据，非纯重述；但「一行代数」objection 未被 M0 排除（P2 数值反与之相符）、推论层未检索、P3 未干净复现 ρ-不变、κ_n 单调性未测 | G0 推论层检索无近邻 ＋ G3 非平凡性证明 ＋ G7 单调性实测，三者齐备方可升 4 |
| Conceptual innovation | 12 | 3 | 3 | κ_n 判据与 ρ-不变解释是 rev1 没有的概念层增量；但 κ_n 仅为两个已知量之比，与 T2 张力未解，且 M0 P3 显相对误差随 ρ 变化 0.2591–0.5648、argmax 0.828–1.0 波动 | 解 κ_n–T2 张力（给单调性成立的 ‖a_n‖₂/ρ_n 区间）＋ 证 κ_n 带来 prior-art 无法给出的可证伪预测 |
| Method soundness | 14 | 4 | 4 | **升 1 分依据**：M0 实跑把「核心定理全未证」中的代数/概率子集兑现（P1 25 格残差 ≤ 9.88e-15、P2 β\*、P4 1920 对 0 违反、P5 确定性、P6 失效边界），脚本可复算。**仍扣 1 分**：数值核验 ≠ 解析推导；一般 A 下 β\* 推导、`‖A‖` 界证明、T1 非平凡性、κ_n 单调性、两解码兼容性、A5 消融未做；M0 自认不证明单调判据 | G3 完成解析层 ＋ 受控 P3 设计；P2/P3 过表述收敛 |
| Elegance and simplicity | 8 | 3 | 4 | 收敛到单一 κ_n 判据比 rev1 四组件拼盘简洁；但组件冗余（膜电位解码 vs 确定性计数）未消融 A5，三块贡献未结构化绑定；M0 P5 未做两解码对比 | A5 消融删冗余；判据/横评/边界绑定为单一叙事 |
| Feasibility under resources | 8 | 4 | 4 | 数据/算力/多数基线代码齐备；M0 脚本在本机 NumPy 2.4.4 / seed 20261110 实跑通过，佐证可跑路径；evidence plan 与里程碑齐备；ImageNet 不可得已由降档消解。仍扣：GCN 实现来源 `TBD`、`torchvision` 待补装、3 个基线待复现、官方当年 policy 未核验 | 确认 ViG-SNN 与全套基线在 3060/4090 可跑通；补齐 GCN 来源与 `torchvision` |
| Experimental convincibility | 10 | 4 | 4 | **升 1 分依据**：`matched-protocol.md` 冻结版 v1 真实兑现（§2–§10 同 teacher/T/θ/calibration、唯一 CL 口径、5 seeds/bootstrap/BH、第 0 批 must-rerun、S1–S7、复现产物、明确不做），叠加 M0 可复算实跑。**仍扣 1 分**：视觉侧零正式实验（guidance 阶段不判 fatal）、PASCAL 复现验收锚缺（W2）、ρ=1 校准律在 ρ≠1 聚合的适配语义未定义（W3）、单调性未操作化（W4）、C5/R4/A6 待实测 | 补 H3/H4/H5 三项定义；第 0 批复现 PASCAL/TPP；报告单调曲线、κ_n 欠校准率、C5/R4 |
| Venue and audience fit | 8 | 4 | 3 | 主动对齐 TNNLS/Q1–Q2 档、主轴收敛、ImageNet 消解；冻结协议与 S1–S7 对期刊可审计性加分。仍扣：三块贡献仍并列、横评带 benchmark 味、当年官方政策未核验 | 结构化绑定单一叙事 ＋ 核验当年官方 policy / review form |
| Timeliness and topic heat | 6 | 3 | 4 | 方向热但 2024/2025 prior-art 密集（FTBC'24、Dual-Phase'24、PASCAL'25、TPP'25、Parallel'25、DCGS'25、AdaFire'25、One-Spike SNN'24/25）；「何时失效」角度相对不饱和，但推论层未检索，scoop 风险未消 | 把「为什么是现在」绑定到 ρ_n≠1 算子真实普遍性的公开证据 ＋ G0 推论层检索 |
| Risk-adjusted acceptance potential | 8 | 3 | 4 | fatal 从 3 条降为 0 条、venue 对齐、M0/协议兑现（这些已由 Method/Experimental 计分）；但**F2 的 novelty 核心质疑未被 M0 消解**、核心判据未实测、零视觉实验、κ_n–T2 张力未解、范畴错位残留。rubric 4 要求「one material gap remains」，此处多个决策相关 gap 叠加，且严格审稿人仍会问「这是不是代数展开」，故**不升分** | G3 过门 ＋ G0 检索无命中 ＋ G7 横评显示判据诊断能力，三者齐备方可升档 |

### 每个 ≤3 分项的扣分明细（依 `rubric.md` Deduction Format 与 `review-output-standards.md` 定量反馈；用户硬要求四项齐全）

本表共 **6 个 ≤3 分项**（Problem / Novelty / Conceptual / Elegance / Timeliness / Acceptance），每项含**扣分理由 / 证据基础 / 修复条件 / 预期分数变化**四项，另附 Why it matters 与 Development-potential effect。全部预期变化为**条件性、非承诺**（依 `privacy-and-evidence.md`）。

**Problem importance（Score 3 / Confidence 4）**
- 扣分理由：rev2 把主张与适用条件对齐（F1 已解），但把一个大而难的问题换成小而具体的问题，未提升绝对重要性。算子类「固定、非负、线性、ρ_n≠1」的真实代表性存疑：冻结 KNN 的 ViG 已失去数据依赖表征（R4 自认削弱），ρ≈169 的 sum 聚合属「用户提供的未公开先验（未发表、不充当公开证据）」中的人为极端设置。**M0 只在合成随机 A 上验证，未提供该类在真实部署中普遍存在的公开证据**。
- 证据基础 / Anchor：rev2 §1 Bottleneck、A1/A2、R4；`m0-results.json` P1–P6（合成算子）；第一次 Field 专家之问。
- 为什么重要：Q1–Q2 期刊同样要求瓶颈「真实且被本文真正检验」；写完 related work 后若 gap 只剩「没人系统测过 ρ_n≠1」，会被判为窄诊断。
- 修复条件：给出「非行随机算子在主流 GNN / ViG 部署中普遍存在」的**公开**证据，并量化冻结 KNN 相对原版 ViG 的 ANN 精度代价（R4/A6）。
- 预期分数变化：条件性 3→4，Overall 约 +0.12；**不承诺**。
- Development-potential effect：中；提升主轴清晰度，不消除 F2。

**Novelty against likely prior work（Score 3 / Confidence 3）**
- 扣分理由：T1/T2/κ_n 把 rev1 的「伪 / 组合 delta」推进为薄但真实、可证伪的分析判据（这是第一次 2→3 的依据），但够不上「prior-art 无法得到的新推论」：T1 可由 `A(E₁W₂)` ＋ QCFS 零期望偏置 ＋ 行和定义一行代数照搬 Deng&Gu 递归；T2 是尺度抵消的标准观察；κ_n 是两个已知量之比。**本轮新增证据对此项零贡献**：M0 不含推论层检索、不含非平凡性证明；P2 数值反与「一行代数」相符；P3 未干净复现 ρ-不变（相对误差 `0.3056/0.5648/0.3187/0.3034/0.2591`，argmax `1.0/0.9219/0.8281/0.9844/0.90625`）。依 `strict-idea-review.md` 封顶 3、置信度 3。
- 证据基础 / Anchor：Closest prior art table 8 条（组件层高重叠）；`Novelty delta` 特别回答三条；`m0-results.json` P2/P3；`rubric.md`「do not score above 3 when closest work was not checked and novelty is central」；Search basis 推论层边界。
- 为什么重要：这是决定 F2 的关键维度；`calibration.md` fatal gate「Novelty <= 2 with high confidence」当前不触发，但反向条件会把它拉回。
- 修复条件：G3 给出 T1 相对 Deng&Gu 递归的非平凡性证明 ＋ G0 推论层针对检索无近邻命中 ＋ G7 κ_n 单调性实测成立。三者缺一，维持 3；任一反向结果回落 2。
- 预期分数变化：条件性 3→4（三条件齐备），Overall 约 +0.14；反向条件 3→2，Overall 约 −0.14；**不承诺**。
- Development-potential effect：低—中；fatal gate 的临界项。

**Conceptual innovation（Score 3 / Confidence 3）**
- 扣分理由：κ_n 判据与 T2 的 ρ-不变性解释是 rev1 没有的概念层增量（第一次 2→3），且禁用掩盖性命名；但 κ_n = ρ_n/‖a_n‖₂ 只是两个已知统计量的比值，ρ-不变性是标准归一化观察，且 **κ_n 与 T2 存在未量化的内部张力**。**M0 P3 反而给出新的张力证据**：相对误差跨 ρ 变化近 2.2 倍、argmax 一致率 0.828–1.0 波动，且 P3 每 ρ 重采样 problem 的设计不能严格检验尺度抵消；`‖a_n‖₂` 随 ρ_n 增长时 κ_n 近似不变，单调预测可能不成立。张力仍未列入 G3 待解项。
- 证据基础 / Anchor：rev2 §1 T1/T2/κ_n；`m0-results.json` P3；`m0_operator_theory_check.py` 第 126–141 行；`rubric.md`「penalize pure module recombination unless the combination creates a new capability or explanation」。
- 为什么重要：若判据不能带来 prior-art 无法给出的解释或预测，概念创新读成「把两个量相除」。
- 修复条件：证明 κ_n 带来 prior-art 无法给出的可证伪预测（如逐节点欠校准率），显式解决 κ_n–T2 张力（给出单调性成立的 ‖a_n‖₂/ρ_n 条件区间），并把 P3 改为固定 problem 只缩放 A 行和的受控设计。
- 预期分数变化：条件性 3→4，Overall 约 +0.12；**不承诺**。
- Development-potential effect：中。

**Elegance and simplicity（Score 3 / Confidence 4）**
- 扣分理由：收敛到单一 κ_n 判据、全文不再声称发明任何组件，比 rev1 四组件拼盘更简洁、更有解释力；但组件冗余（膜电位累加解码 vs 确定性计数 s[t]）未消融（A5 待办），「判据 / 横评 / 边界」三块贡献仍并列、未结构化绑定。**M0 P5 只验证确定性 s[t] 的代数性质（Σs=n 100%、重建误差 0.49999812148232436、条件方差 0），未做两解码对比**，对冗余问题零贡献。
- 证据基础 / Anchor：rev2 §1 Contribution type、R3/A5；`m0-results.json` P5；用户核验的 Dual-Phase（膜电位读出）与 PASCAL（确定性计数）。
- 为什么重要：`rubric.md` elegance 要求 necessary parts and coherent insight；冗余组件会被核减为实现细节。
- 修复条件：A5 消融删除被证明冗余的组件；把三块贡献绑定为「一个 κ_n 判据贯穿横评与边界」的单一叙事。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；**不承诺**。
- Development-potential effect：低—中。

**Timeliness and topic heat（Score 3 / Confidence 4）**
- 扣分理由：方向热但饱和风险高；2024/2025 prior-art 密集（FTBC ECCV'24、Dual-Phase TNNLS'24、PASCAL TMLR'25、TPP ICML'25、Parallel Conversion ICML'25、DCGS ICML'25、AdaFire AAAI'25、One-Spike SNN TETC'24/25）。「何时失效」诊断角度相对不那么饱和，但**推论层未检索**，M0 未改变此项，scoop 风险未消。
- 证据基础 / Anchor：用户提供的 prior-art 年份与 venue 列表；`rubric.md` timeliness 的「risk of saturation」；Search basis 推论层边界。
- 为什么重要：密集 prior art 提高 novelty 坍塌与 scoop 风险，尤其对推论层未检索的 T1/T2。
- 修复条件：把「为什么是现在」绑定到 ρ_n≠1 算子在视觉图网络 / GNN 中的真实普遍性公开证据，并在 G0 做推论层针对检索。
- 预期分数变化：条件性 3→4，Overall 约 +0.06；**不承诺**。
- Development-potential effect：低。

**Risk-adjusted acceptance potential（Score 3 / Confidence 4）**
- 扣分理由：fatal 从 3 条降为 0 条（F1 已解、F2 部分解决、F3 已解）、venue 主动对齐 Q1–Q2 档、M0 与 `matched-protocol.md` 兑现（这些已分别计入 Method 4 / Experimental 4，避免重复计分）；但**F2 的 novelty 核心质疑「T1/T2/κ_n 是否为 prior-art 无法得到的新推论」完全未被 M0 消解**、核心判据（ρ_n/T 单调）未实测、视觉侧零正式实验、κ_n–T2 张力未解、范畴错位主卡残留、PASCAL 验收锚与适配语义缺口仍在叠加。`calibration.md` 五条 fatal gate 当前均不硬触发（novelty 3、method 4、experimental 4、fit 4、feasibility 4），但「No identifiable insight beyond known modules」与「Internal mechanism conflict」两条处于临界。
- 证据基础 / Anchor：本报告 `Serious blockers`（A 段 0 fatal、B 段 Q1′–Q4′、C 段 W1–W11）、fatal gates 清单、Panel Synthesis、Skeptical / Theory 两位专家 notes。
- 为什么重要：该维度反映「考虑致命弱点与评审分歧后的分数」，是叠加效应而非重复计罚；严格审稿人仍会以「这是不是代数展开」为主拒稿轴。
- 修复条件：G3 过门 ＋ G0 推论层检索无命中 ＋ G7 横评显示判据诊断能力，三者齐备方可升档；任一反向结果回落。
- 预期分数变化：条件性 3→4，Overall 约 +0.08；若 F2 回潮为 fatal → 3→2，Overall 约 −0.08；**不承诺**。
- Development-potential effect：中（依赖 G3 与 G7 结果）。

> `Method soundness`(4)、`Feasibility under resources`(4)、`Experimental convincibility`(4)、`Venue and audience fit`(4) 为 >3 项，不触发明细块要求；其扣分 / 修复条件已在上方表格给出（Method 与 Experimental 的「升 1 分依据」亦在表内写明）。

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
10×4 = 40   (Experimental convincibility)
 8×4 = 32   (Venue and audience fit)
 6×3 = 18   (Timeliness and topic heat)
 8×3 = 24   (Risk-adjusted acceptance potential)
合计 = 340 → 340 / 100 = 3.40 → 3.4（保留一位小数）
```

`**Overall:** 3.4`（1–5 加权尺度；可选 1–10 尺度 ≈ 6.8）

```text
Current conference readiness: low
Development potential: medium
```

**分数与推荐的一致性说明**：3.40 → 3.4 落在 `calibration.md` 的 **3.0–3.6 段 → `pivot-with-rescue-route`**。本推荐**由分数段直接得出，不依赖任何 fatal gate 压顶**（五条数值 gate 当前均不触发，两条临界 gate 见 `Serious blockers` A 段）。不取 `revise`（需 3.7+，即 novelty 站稳 ＋ 核心判据实证 ＋ 视觉侧实验，未达）；不取 `accept-to-develop`；不取 `needs-literature-search`（novelty 按用户指令标 `searched` 且结论为「组件层高重叠 / 推论层薄增量」而非「未知」，推论层未检索作为边界与置信度处理，不升级为推荐值）；不取 `abandon`（判据可测、G0/G3/G4/G7 路线可命名，依 `strict-idea-review.md` Stage-Aware Verdict Rule 不满足「无可测主张且无重构」）。

**相对第二次 `**Overall:** 3.2`（3.16）的 +0.24 逐维分解（证明「不因修订版默认更高」「不抬分」）**：

| 维度 | rev2 → rev3 | 加权贡献 | 强制该变化的文本事实 |
|---|---|---|---|
| Method soundness | 3 → 4 | +0.14 | M0 本机实跑：P1 25 格恒等式残差 ≤ `9.880984919163893e-15`、P2 β\* 与 ρ 无关、P4 1920 对 0 违反、P5 确定性、P6 失效边界 `0.7476` / `1.1051`；脚本可复算（NumPy 2.4.4 / seed 20261110）。第二次给 3 的核心理由「核心定理全未证」中的数值/代数子集已兑现。 |
| Experimental convincibility | 3 → 4 | +0.10 | `matched-protocol.md` 冻结版 v1 真实存在（§2–§10），第二次给 3 的「工件未成文」已消除；叠加 M0 可复算实跑、第 0 批 must-rerun、S1–S7 硬回退。 |
| Problem / Novelty / Conceptual / Elegance / Feasibility / Venue / Timeliness / Acceptance | 3/3/3/3/4/4/3/3 全部**保持不变** | +0.00 | M0 不触及问题代表性、不触及推论层 novelty、未解 κ_n–T2 张力、未做消融、未改资源与 venue、未检索、未消除「代数展开」质疑；故这 8 维一分不升。 |

合计 +0.24 → 3.16 + 0.24 = 3.40 ≈ 3.4。**仅两个 +1，全部由「新增证据直接兑现的维度」强制；零个 +2 跳升；novelty / conceptual / acceptance 三个压档维度刻意不升；推荐仍为 `pivot-with-rescue-route`，未升出 3.0–3.6 段**。这是「如实承认局部进步 ＋ 不迎合抬分」的取值。

**Fatal gates 生效清单（`calibration.md`，逐条核对）**：
- Novelty <= 2 with high confidence → **不触发**（3 / conf 3）。
- Method soundness <= 2 → **不触发**（4）。
- Experimental convincibility <= 2 且无替代证据 → **不触发**（4，且 M0 实跑 ＋ evidence plan 完备）。
- Venue fit <= 2 → **不触发**（4）。
- Feasibility <= 2 → **不触发**（4）。
- No identifiable insight beyond applying known modules → **不硬触发但临界**（T1/T2/κ_n 提供薄但可辨识的判据；M0 P2 未排除「一行代数」，若 G3 证明 T1 可照搬则触发）。
- Internal mechanism conflict → **不硬触发但临界**（κ_n–T2 张力、冻结 KNN vs 表征力已由 R4/C5/A5/A6 显式管理，但张力未量化，M0 P3 提供新张力证据）。
- Novelty unknown 且无 closest-work search → **不适用**（组件层 `searched`；推论层未检索已降置信度并封顶 novelty 3，依 `strict-idea-review.md` 处理，不升级为 `needs-literature-search` 推荐）。

---

## Score-change conditions:

全部为**条件性、非承诺**（依 `privacy-and-evidence.md`，不保证分数变化 / 录用概率 / 审稿人行为）。按影响排序：

| 条件（可测） | 影响维度 | 预期分数变化（条件性区间） |
|---|---|---|
| C1 完成 G3 解析层：一般 A 下 β\* 严格推导、`‖A‖` 误差上界证明、T1 相对 Deng&Gu 的非平凡性证明、κ_n 单调性成立区间（含 κ_n–T2 张力）、两解码兼容性、A5 消融；并把 P3 改为固定 problem 只缩放 A 行和的受控设计 | Method / Conceptual | Method 4→5（若全过）、Conceptual 3→4；Overall 约 +0.26 |
| C2 G0 推论层针对检索无近邻命中 ＋ 非平凡性成立（T1 在 ρ=1 文献中退化消失、并带来其无法给出的可证伪预测） | Novelty / Conceptual / Acceptance | Novelty 3→4；Overall 约 +0.14；反向则 3→2 |
| C3 按 `matched-protocol.md` 第 0 批复现 PASCAL / TPP，补齐验收锚（H3）、适配语义（H4）、单调性操作化（H5），报告 conversion loss–ρ_n/T 单调曲线、κ_n 逐节点欠校准率、C5 边界、R4/A6 代价 | Experimental / Acceptance | Experimental 4→5（若曲线支持判据）、Acceptance 3→4；Overall 约 +0.18 |
| C4 把 rev2 §1 第 4 条证伪条件与 §8 S4 统一为针对判据的可测量；显式解决 κ_n–T2 张力 | Experimental / Method / Elegance | 辅助 C1/C3；Overall 约 +0.05~+0.10 |
| C5 给出「非行随机算子在主流 GNN / ViG 中普遍存在」的公开证据 ＋ 冻结 KNN 代价量化 | Problem / Timeliness | Problem 3→4、Timeliness 3→4；Overall 约 +0.18 |
| C6 结构上把「判据 / 横评 / 边界」绑定为单一叙事 ＋ 核验当年官方 policy / review form | Venue / Elegance | Venue 维持 4、Elegance 3→4；Overall 约 +0.08 |
| C7 A5 消融删除冗余组件（膜电位累加解码 vs 确定性计数） | Elegance | Elegance 3→4；Overall 约 +0.08 |
| C8 收敛 `m0-theory-check.md` 三处过表述、统一 SHA 记录口径、修正 P4 对数描述（以文件 1920 对为准） | Evidence integrity（不直接改维度分） | 消除复现核验假阳性；不承诺分数变化 |

**反向条件（会坐实 fatal / 降分，是「不因修订版默认更高」的护栏）**：
- 若 G3 证明 T1 可由 `A(E₁W₂)` ＋ QCFS 零期望偏置 ＋ 行和定义一行代数照搬 Deng&Gu 递归 → F2 回潮为 fatal，Novelty 3→2、Conceptual 3→2、Method 4→3、Acceptance 3→2，加权回落约 **3.0–3.1**，并重新触发 novelty / beyond-modules 两条 fatal gate；按 `startup-decision.md` §4 / `matched-protocol.md` §8 S4 回退到 `pivot-with-rescue-route`。
- 若 G0 推论层针对检索命中近邻（已有工作给出 ρ_n 加权 margin 偏置 / 相对误差尺度不变 / 行和-行范数比判据）→ Novelty 3→2，F2 回潮。
- 若 G7 实测 conversion loss 与 ρ_n/T 无单调关系、或 ρ≈1 的 CNN 臂出现「我们显著更好」 → 核心判据被推翻，pivot 为纯 benchmark 故事（rev2 §1 自设条件、协议 §8 S4）。
- 若 κ_n 与 T2 张力不可调和（`‖a_n‖₂` 随 ρ_n 增长使 κ_n 近似不变）→ 单调预测不成立，Conceptual / Method 降 1。
- 若原版动态 / 非线性 ViG 上恒等式仍成立 → 适用边界写错，须扩展算子类或放弃 T1/T2（协议 §8 S3 回 G3）。
- 若 β\* 对一般 A 不成立且无替代闭式 → Method 4→3 或更低并触发 fatal gate。
- 若把「用户提供的未公开先验（未发表、不充当公开证据）」写入公开证据 / 结果栏，或把 M0 数值外推为「精度 / 判据已证」 → 依 §8 S6 诚信门停止，不升分。
- 若第 0 批 PASCAL / TPP 任一无法复现 → 依 §8 S2 转 `needs-evidence`，startup-decision 回退。

**说明**：C1–C3 是升到 `revise` 段（3.7+）的必要非充分条件；即便三条全过，仍需 Q1–Q2 档下的实证与 novelty 站稳才可能改推荐。本评审不预判其结果。

---

## Confidence:

- **综合 Confidence：Medium**（依 `calibration.md` 标签）。
- 理由：(i) 本轮**可直接核查的事实显著增多且置信度高**：M0 脚本 / JSON / md / `matched-protocol.md` 四个工件真实存在并已完整读取，JSON 数值与 md 叙述内部一致，SHA 口径差异已用 `sha256sum` ＋ 规范化重序列化双向核实为非篡改，成稿两个文件确认可读且原文数值逐项核对到，P4 对数以文件为准核定 1920 对 —— 这些判断置信度高；(ii) **但 F2 的核心仍属「未给出的机制 / 未证定理 / 未检索的推论层」**：T1 是否超出 prior-art、κ_n 单调性是否成立、κ_n–T2 张力是否可解、G0 检索是否命中近邻，全属未知，故 Novelty / Conceptual 的置信度仅 3；(iii) 推论层 novelty 未检索，novelty 上限被封顶、置信度下调；(iv) 各目标期刊当年官方 policy / review form 未核验（AC conf 3）；(v) 视觉侧无任何正式实验，实验判断是「plan 可信 ＋ M0 数值证据 ＋ 证据缺口」而非「结果已知」。
- **依公平规则**：不因 confidence 为 Medium 而下调 idea 分数；分数（3.4）与置信度（Medium）分开报；低置信度单独引导下一步检查（见 `Optional next-module decision` 与 `Evidence that would change my score`）。
- 各维度 Confidence 已在 `Rubric scores` 表逐维列出，分数与置信度不在此重复。
- **Development potential 保持 medium 而非 high 的置信度说明**：升 high 需「G3 解析推导兑现 T1/T2 ＋ G0 推论层检索无近邻 ＋ G7 κ_n 单调性成立」三项同时支持；当前均未知，故 medium 是如实取值。

---

## Strict reviewer comments:

> 依 `strict-idea-review.md` Harsh Reviewer Lens：短、诊断式、每条带 anchor，不作动机性缓冲。

1. **关于「M0 实跑」的证明力边界**（Anchor：`m0-theory-check.md` 第 33–36 行「本核验不能证明什么」；脚本 docstring）：你证明了 `B̂₂−B₂=A(E₁W₂)` 在固定线性算子上精确到 `9.88e-15`，但你**没有证明** ρ_n/T 单调判据在真实训练网络上成立——文件自己写了「那需要 P4 全量实验」。请勿把 P1–P6 写成「判据已证 / 精度已测 / 能耗已证」；M0 不训练、不报告分类精度。
2. **关于 T1 的非平凡性**（Anchor：Deng&Gu ICLR 2021、QCFS/FTBC、Dual-Phase TNNLS 2024，用户提供核验；`m0-results.json` P2）：P2 中 margin 平移随 ρ 放大（T=1 由 −0.7182 到 −19.2461）、β\* 仅随 T 变，正是 `A·1=ρ_n·1` 加 `E[E₁]=β−1/(2T)` 的直接后果。M0 确证了「成立」，没有回答「prior-art 推不出」。请在 G3 给出 T1 相对 Deng&Gu 递归的非平凡性证明，并在 G0 针对推论本身检索；否则这是表述而非新推论。
3. **关于 T2 与 κ_n 的一致性**（Anchor：`m0-results.json` P3；`m0_operator_theory_check.py` 第 126–141 行；rev2 §1 T2 与 κ_n 定义）：一边说相对误差 ρ-不变，一边预测 conversion loss 差距随 ρ_n/T 单调增大；P3 实测相对误差跨 ρ 为 `0.2591–0.5648`（近 2.2 倍）、argmax 一致率 `0.828–1.0` 波动，且每个 ρ 重新采样 problem，构造上不能检验尺度抵消。请把 κ_n–T2 张力列入 G3、给出单调性成立的 ‖a_n‖₂/ρ_n 区间，并把 P3 改成固定 problem 只缩放 A 行和的受控设计；`m0-theory-check.md` 第 16 行「复现了 §5.1 反直觉结论」应降级为「方向性、非严格的数值佐证」。
4. **关于 P2 的过表述**（Anchor：`m0-results.json` `P2_rho_weighted_systematic_error`）：「加 β\* 后系统项在各 ρ 下同时趋零」不准确——`mean_E1_with_beta_star` 各格约 1e-3 确趋零，但 `mean_margin_shift_with_beta_star` 在 T=1/ρ=10 仍 `−1.4343`、T=8/ρ=10 仍 `−0.1016`。请精确表述为「E₁ 均值的系统项趋零；margin 平移残差仍随 ρ/T 变化」。
5. **关于可比性适配语义**（Anchor：`matched-protocol.md` §3、§2 B2/B3）：协议写死了同 teacher、同 T、同 θ、同 calibration、同骨干，却未规定「为 ρ=1 网格算子导出的校准律（QCFS/FTBC/TPP/PASCAL…）在 ρ_n≠1 的 KNN 图 / GCN 聚合上如何原样应用、不得针对 ρ 重调、无法实现则单列」。检验「ρ=1 校准律是否失效」正是本文中心问题，适配方式若由作者自选，横评归因不可信。请升 v2 补此规则并记 `reopen`。
6. **关于最近邻基线与验收**（Anchor：`matched-protocol.md` §6、§8 S2）：第 0 批 PASCAL 无官方码、自行复现，但只写了「跑不通 → needs-evidence」，**没有「复现成功」的可判定锚**；QCFS 有 `91.18%@T=2 / 93.96%@T=4` 回归测试，PASCAL 应有等价阈值或明确 `not_applicable` 且不计入主表。另 P5 的 Bernoulli 对照是简化实现、非 TPP 官方复现，不得当 TPP 复现证据。
7. **关于核心判据的操作化与口径**（Anchor：`matched-protocol.md` §4、§8 S4；rev2 §1 Falsification 第 4 条）：§8 S4 用「conversion loss 差距随 ρ_n/T 单调连续落 failure」作裁决，但 §4 未定义单调性的趋势检验、比较单元与统计判据；rev2 §1 第 4 条仍写「与 PASCAL / TPP 等价 → 判据被推翻」，一个分析判据不能与一个转换方法等价。请统一口径并把测法写入 §4。
8. **关于证据工件一致性**（Anchor：`m0-results.json` 文件字节；`m0-theory-check.md` 第 4/19/34 行；本会话 `sha256sum` 复核）：声明 SHA `2498875f…` 是内存 LF 字符串 `raw` 的哈希，磁盘文件因 Windows CRLF ＋ 尾随换行，`sha256sum` 得 `aecfa88e…`；内容经规范化重序列化核对一致、非篡改，但**须统一记录口径**否则复现核验会假阳性。另：P4 对数文件为 1920 对（每 T 384×5），任务描述写 3840 对；P5「Bernoulli 方差 >0」在 T=16 时 JSON 为 `0.0`；第 34 行两个 bullet 挤在一行。请逐项收敛。
9. **关于内部先验的隔离**（Anchor：`p7-draft.md`、`guidance-v3.md`；用户硬要求）：成稿中的 ρ_n=5.75、`var(U)=0.082 vs 0.083`、`mean(U)=0.481 vs 0.5`、Hoeffding 3.2–6.7×、ρ-不变性反直觉发现、`T≤8` 达 `ANN−1.5pp` 带内，全部为「用户提供的未公开先验（未发表、不充当公开证据）」。可作方法机制与理论命题的出处核对，**不得当公开前作、不得进公开证据 / 结果栏、不得替代本文的公开视觉实验**。第二次「无对应成稿」的误判已纠正，但这不改变其未发表属性。
10. **关于 venue 与主轴**（Anchor：rev2 §0、§1 Contribution type；`matched-protocol.md` §10）：降到 TNNLS / Q1–Q2 档、ImageNet 消解是对的；但贡献仍是「判据 / 横评 / 边界」三章并列，主轴收敛更多在措辞。请把三者绑定为「一个 κ_n 判据贯穿横评与边界」的单一叙事，别让讨论阶段把它读成 benchmark 短文；成文前核验当年官方 policy。

---

## Fixability table:

依 `calibration.md` 字段。Owner skill 仅列出建议归属，**未执行任何 handoff**（见 `Optional next-module decision`）。

| Issue | Affected dimension | Severity | Fix class | Can fix before writing? | Required evidence or design change | Risk-reduction condition | Development-potential impact | Owner skill |
|---|---|---|---|---|---|---|---|---|
| Q1′ 核心判据（ρ_n/T 单调）未实测、M0 只兑现数值子集；G3 解析层待办（β\* 一般 A、`‖A‖` 界证明、T1 非平凡性、κ_n 单调性、兼容性、A5 消融） | Method / Novelty / Acceptance | high（准 fatal） | method-redesign | yes（G3 纸面） | 完成 G3 全部推导 ＋ 受控 P3 设计；G7 实测单调曲线 | 推导自洽、非平凡、数值通过、单调性成立 | 中—高 | ccf-idea-optimizer |
| Q2′ 推论层 novelty 未检索 ＋ 一行代数 objection 未排除 | Novelty / Conceptual | high（准 fatal） | novelty-grounding | no（需 G0 检索 ＋ G3 推导） | G0 推论层公开检索 ＋ T1 相对 Deng&Gu 的非平凡性证明 | 无近邻命中且非平凡性成立 | 低—中 | ccf-literature-searcher（若授权）/ ccf-idea-optimizer |
| Q3′ κ_n 与 T2 张力未量化、单调性未证（M0 P3 提供新张力证据） | Method / Conceptual / Experimental | medium | method-redesign | yes（G3 纸面 ＋ 数值） | 给单调性成立的 ‖a_n‖₂/ρ_n 区间 ＋ 受控 P3 重做 | 张力可解释、预测成立 | 中 | ccf-idea-optimizer |
| Q4′ 证伪条件范畴错位（协议 §8 S4 已修正、rev2 §1 第 4 条残留） | Experimental / Method | medium | evidence-design | yes | 统一两处口径为针对判据的可测量 | 证伪条件与贡献类型自洽 | 中 | ccf-experiment-designer |
| W1 视觉侧零正式实验 | Experimental | medium（按硬要求不判 fatal） | evidence-design | no | G7 统一协议下完整视觉实验 ＋ conversion loss–ρ_n/T 曲线 | 中心判据获得实证支撑 | 高 | ccf-experiment-designer |
| W2 PASCAL 无官方码、缺复现验收锚 | Experimental | high | evidence-design | no（需实现） | 第 0 批 must-rerun 复现 ＋ 可判定验收锚（或 `not_applicable` 单列） | 最决定性基线可复算、成功可判定 | 高 | ccf-experiment-designer |
| W3 ρ=1 校准律在 ρ≠1 聚合上的适配语义未定义 | Experimental / Acceptance | high | evidence-design | yes（协议升 v2） | 补 §3.x：原样应用、不得针对 ρ 重调、无法实现则单列；记 `reopen` | 横评归因不被选择性适配污染 | 高 | ccf-experiment-designer |
| W4 核心判据「单调」未操作化 | Experimental / Method | medium | evidence-design | yes | 把趋势检验、比较单元、统计判据写入 §4 指标定义 | 核心判据可证伪、可复算 | 中—高 | ccf-experiment-designer |
| W6 冻结 KNN 代价未量化（R4/A6） | Problem / Method | medium | evidence-design | no | 定量报告相对原版 ViG 的 ANN teacher 精度代价 | 适用类代表性被实证界定 | 中 | ccf-experiment-designer |
| W7 组件冗余未消融（A5） | Elegance | low | method-redesign | partly | 消融膜电位解码 vs 确定性计数 | 冗余组件被删除 | 低—中 | ccf-idea-optimizer |
| W8 推论层 novelty 未检索（G0/G4 待办） | Novelty / Confidence | high | novelty-grounding | no | 针对推论做一次公开检索（不粘贴私有措辞） | 推论层 `not searched` 边界关闭 | 中 | ccf-literature-searcher（若授权） |
| W9 官方当年 venue policy 未核验 | Venue fit | low | venue-switch | yes | 核验 TNNLS 当年官方 policy / review form | venue 定位与官方规则自洽 | 低 | ccf-submission-checker（若授权） |
| W10 证据工件口径一致性（SHA / P4 对数 / 三处过表述 / 格式） | Evidence integrity | medium | evidence-design | yes | 统一 SHA 记录口径；以文件 1920 对为准；收敛 P2/P3/P5 措辞；修第 34 行格式 | 全包零编造、复现核验无假阳性 | 低—中 | ccf-integrity-auditor（若授权） |
| W11 成稿隔离标注须全程贯彻 | Evidence integrity | medium | evidence-design | yes | 全程标注「用户提供的未公开先验（未发表、不充当公开证据）」；不得进公开证据 / 结果栏 | 诚信门 S6 不被触发 | 中 | ccf-integrity-auditor（若授权） |

> 「用户提供的未公开先验（图节点分类 `T≤8` 达 `ANN−1.5pp` 带内；成稿 `p7-draft.md` / `guidance-v3.md` 及其全部数值，未发表、不充当公开证据）」不列入任何 Issue 的 required evidence；不得用它替代公开实验。

---

## Upgrade / pivot actions:

依 `SKILL.md` workflow #8 标签分类。每条为具体动作，不含通用套话。

- **[problem-refinement]**：给出「非行随机算子（ρ_n≠1）在主流 GNN / ViG 部署中普遍存在」的**公开**证据，把中心问题从「人为构造的算子类」锚到「真实部署类」；量化冻结 KNN 相对原版 ViG 的 ANN 精度代价（R4/A6），不得隐瞒。
- **[method-redesign]**：在 G3 完成 M0 **解析层**——一般 A 下 β\* 严格推导或反例条件、`‖A‖` 跨层误差上界的证明（非仅数值检查）、T1/T2 严格证明、**T1 相对 Deng&Gu 递归的非平凡性证明**、κ_n 单调性成立区间、两解码兼容性命题、A5 冗余消融；显式列入并解决 κ_n 与 T2 的内部张力；把 P3 改为「固定 problem 只缩放 A 行和」的受控设计；修正 P6 中 `max_resid` 的占位实现（`max_B2 - max_B2` 恒为 0）。
- **[novelty-grounding]**：G0 针对推论本身做一次公开检索（通用关键词，不粘贴私有措辞），确认「ρ_n 加权 margin 偏置 / 相对误差尺度不变 / 行和-行范数比判据」无近邻命中；全文一致声明不发明任何已占组件，**且不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」**，除非 G3 证明 ＋ G0 检索 ＋ G7 单调性实测三者同时支持；澄清「本文新推论」与「用户提供的未公开先验（未发表、不充当公开证据）」中已有 margin 定理 / ρ-不变解释的边界，避免自我重复定位。
- **[evidence-design]**：按 `matched-protocol.md` 冻结版执行；升 v2 补 §3.x 适配语义（W3/H4）、§4 单调性操作化（W4/H5）、PASCAL 验收锚（W2/H3）；统一 rev2 §1 第 4 条与 §8 S4 证伪口径；保留 B4/C5 失效边界（不得删）；报告 conversion loss–ρ_n/T 曲线、κ_n 逐节点欠校准率、恒等式浮点残差、C5 边界、R4/A6 代价；补视觉侧正式实验。
- **[feasibility-check]**：确认 RTX 3060 12GB / 远端 4090（已授权，guidance 阶段不提交）上 ViG-SNN 与全套基线可跑通；补齐 GCN 消息传递实现来源（当前 `TBD/需确认`）与 `torchvision` 补装；M0 已在 NumPy 2.4.4 实跑通过，可作为原型里程碑已过的登记证据。
- **[venue-switch]**：维持主投 IEEE TNNLS / Q1–Q2 档；结构上把「判据 / 横评 / 边界」绑定为单一叙事；成文前核验当年官方 policy / review form。
- **[pivot]**：若 G3 证明 T1 可一行照搬、或 G0 推论层检索命中近邻、或 G7 conversion loss–ρ_n/T 无单调关系，则放弃「理论判据」定位，pivot 为「统一协议 benchmark ＋ 失效边界诊断」型贡献，并把 novelty 完全收敛到横评与边界（rev2 §1、协议 §8 S4 已备用此路线）。
- 不输出 **[abandon]**：中心判据可测（残差、单调性、κ_n 逐节点检验、C5 边界）、G0/G3/G4/G7 路线可命名、stage-aware 规则不满足 abandon 条件。

**最小可行修复路线（按依赖顺序，纸面优先、无算力成本；用户硬要求）**：
1. **先做 [method-redesign] 的 G3 第 1 步**：一般 A 下 β\* 推导 ＋ **T1 相对 Deng&Gu 递归的非平凡性证明** ＋ κ_n 单调性条件（含 κ_n–T2 张力）＋ 受控 P3 设计 —— 这是判定 F2 是否回潮的最便宜、最决定性一步；若 T1 坍缩为一行代数，直接转 [pivot]，不必再做后续实验。
2. **同时做 [novelty-grounding] 的 G0 推论层检索**：通用公开关键词确认无近邻命中；与第 1 步结果共同决定 novelty 是否可站稳 3。
3. **再做 [evidence-design] 的协议升 v2**：补适配语义（H4）、PASCAL 验收锚（H3）、单调性操作化（H5）、证伪口径统一；随后**仅先复现 PASCAL 与 TPP** 两个最决定性基线，在同一批固定骨干上跑 CIFAR-10/100 ＋ Planetoid 的最小横评，测 conversion loss–ρ_n/T 曲线 —— 这是判定判据是否被实测推翻的最小可测实验。
4. **依据第 3 步结果决定**：若单调性成立且有可归因诊断能力 → 继续补齐全套基线 ＋ 视觉侧实验 ＋ C5/R4/A6 量化，主投 TNNLS 档（`revise` 方向）；若单调性被推翻或与近邻等价 → 执行 [pivot]，把贡献收敛为「统一协议横评 ＋ 失效边界」。
5. 全程不把「用户提供的未公开先验（未发表、不充当公开证据）」写入任何证据表或结果栏；不把 M0 数值外推为精度 / 判据已证；统一 SHA 与 P4 对数口径（H8）。

---

## Evidence that would change my score:

**会升分的证据（全部需为公开可复算、非编造）**
- G3 全部解析推导通过：一般 A 下 β\* 严格推导、`‖A‖` 误差上界证明、T1/T2 严格证明、κ_n 单调性成立区间、两解码兼容性、A5 消融、受控 P3 复现尺度抵消（影响 Method / Conceptual / Acceptance）。
- T1 相对 Deng&Gu 递归的**非平凡性证明**（该结论在 ρ=1 文献中退化消失、并带来其无法给出的可证伪预测）＋ G0 推论层针对检索无近邻命中（影响 Novelty / Conceptual / Confidence，是 F2 的唯一实质解）。
- 按 `matched-protocol.md`（含 PASCAL / TPP 自行复现与验收锚）的横评显示 conversion loss 与 ρ_n/T 的单调关系、κ_n 大样本欠校准率符合预测（影响 Experimental / Acceptance）。
- 「非行随机算子在主流 GNN / ViG 中普遍存在」的**公开**证据 ＋ 冻结 KNN 代价量化（影响 Problem / Timeliness）。
- 原版动态 / 非线性 ViG 失效边界（C5）与冻结/线性化代价（R4/A6）的定量报告（影响 Method / Experimental / Problem）。
- 组件消融证明每个组件独立不可替代（影响 Elegance）。

**会坐实 fatal / 降分的证据**
- G3 证明 T1 可一行代数照搬、或 G0 推论层检索命中近邻 → F2 回潮为 fatal，Novelty 3→2，整体回约 3.0–3.1。
- G7 实测 conversion loss 与 ρ_n/T 无单调关系、或 ρ≈1 的 CNN 臂「我们显著更好」 → 核心判据被推翻，pivot 为纯 benchmark 故事。
- κ_n 与 T2 张力不可调和（κ_n 近似不变） → 单调预测不成立，Conceptual / Method 降 1。
- 原版动态 / 非线性 ViG 上恒等式仍成立 → 适用边界写错，须扩展算子类或放弃 T1/T2。
- β\* 对一般 A 不成立且无替代闭式 → Method 降分并触发 fatal gate。
- 把「用户提供的未公开先验（未发表、不充当公开证据）」写入公开证据 / 结果栏，或把 M0 数值外推为「精度 / 判据 / 能耗已证」 → 依 §8 S6 诚信门停止，不升分。

**明确不作为证据的项**：任何录用概率、真实审稿人意见、meta-review、未核验的官方当年规则、任何编造的 URL/DOI/实验数值；以及「用户提供的未公开先验（未发表、不充当公开证据）」——即图节点分类 `T≤8` 达 `ANN−1.5pp` 带内、成稿 `p7-draft.md` / `guidance-v3.md` 中 ρ_n=5.75 / ρ≈169 / `var(U)=0.082 vs 0.083` / `mean(U)=0.481 vs 0.5` / Hoeffding 3.2–6.7× / ρ-不变性反直觉发现 / `T≤8` 达 `ANN−1.5pp` 带内，以及「成稿 §3.2 / §5.1」引用。本报告未生成上述任何一类，也未生成任何实验结果数值。

---

## Recommendation:

**`pivot-with-rescue-route`**（`ccf-idea-reviewer` 5 选 1 之内；用户硬要求）

理由（与分数、fatal gates、stage-aware 规则一致）：
- 加权 3.4（3.40）落在 `calibration.md` 的 **3.0–3.6 段 → `pivot-with-rescue-route`**，**由分数段直接得出，不依赖 fatal gate 压顶**（五条数值 gate 当前均不触发，两条临界）；这不是把分数抬到 `revise`（3.7+）段，也不是靠 gate 强行压回 `pivot`。
- 不取 `needs-literature-search`：novelty 按用户指令标 `searched`（组件层，依据用户提供的独立核验结论），结论是「高重叠 ＋ 薄增量」而非「未知」；推论层未检索作为边界与置信度处理（封顶 novelty 3、conf 3），不升级为推荐值。
- 不取 `abandon`：中心判据可测（恒等式残差、conversion loss–ρ_n/T 单调性、κ_n 逐节点检验、C5 边界），且存在具名修复路线（见最小可行修复路线），依 `strict-idea-review.md` 不满足「无可测主张且无重构」条件。
- 不取 `revise` / `accept-to-develop`：F2 的 novelty 核心质疑未被 M0 消解、核心判据未实测、视觉侧零正式实验、κ_n–T2 张力未解、推论层未检索；任一未解都不足以升档。

含义：保留最佳要素（T2 的 ρ-不变性解释、κ_n 可先验计算判据、统一协议横评、失效边界诊断），改变**方法理论**（G3 解析推导兑现 ＋ 排除一行代数 objection）、**证据**（按 matched-protocol 升 v2 ＋ 复现 PASCAL/TPP ＋ 实测单调性）、**novelty 定位**（G0 推论层检索 ＋ 接受 Q1–Q2 增量诊断定位）中的至少一组。F1 已解决、F3 已解决、F2 部分解决，但**没有任何一条「已解决」到足以让整体升出 `pivot-with-rescue-route` 段**。

### Startup-decision（f-guidance-builder-v1，独立体系）

**建议值：`proceed`（conditional proceed / proceed-with-narrowing）**。

**必须先说明「为何两个结论不矛盾」**：`ccf-idea-reviewer` 的 `pivot-with-rescue-route` 评的是「idea 当前就绪度、是否值得按当前 formulation 直接发展」；`f-guidance-builder-v1` 的 `startup-decision` 评的是「能否进入 G0 去执行后续门」。该技能明文规定：「`startup-decision.md` must be `proceed`, `revise`, `pivot-with-rescue-route`, or `needs-evidence`. **Only `proceed` may enter G0. A low current-readiness score is not a rejection by itself, but an unaddressed fatal risk, missing mechanism, unavailable baseline, or infeasible evidence plan is a block.**」用户亦明确「是否仍存在未解 fatal risk 是能否进 G0 的唯一硬标准」。因此 3.4 / `pivot-with-rescue-route` 的就绪度**不阻塞** `proceed`；而 `pivot` 所要求的「改变问题 / 方法 / 证据 / novelty 中的至少一组」，恰好由 G0（推论层检索＝novelty-grounding）、G3（理论审计＝method-redesign）、G4（非重复门）、G7（横评与消融＝evidence-design）在后续门中执行。

**四条 startup 判据逐条核验**：

| 判据（用户指定） | 核验结论 | 依据 |
|---|---|---|
| 是否有未解 fatal risk（唯一硬标准） | **无，0 条** | F1 已解决；F2 部分解决且依第二次判定为可修复弱点（非 fatal）；F3 已解决；`calibration.md` 五条数值 fatal gate 全不触发，两条临界 gate 属可修复；Q1′–Q4′ 为准 fatal 级但已被 G0/G3/G4/G7 显式列为可执行待办，非「unaddressed fatal」。 |
| 机制是否有可跑路径 | **有，且已实跑** | `m0_operator_theory_check.py` 在 NumPy 2.4.4 / seed 20261110 下产出 P1–P6 全套数值、JSON 与 md 一致、SHA 内容核对非篡改；`matched-protocol.md` §7 A1–A7 把机制拆成可测消融；§8 S1 定义「M0 残差超容差 → 回 G3」。 |
| 最近邻基线是否可复现 | **计划层面可复现（guidance 阶段标准）** | §6 第 0 批 PASCAL（无官方码→自行复现，第一批 must-rerun）＋ TPP（官方仓库已记录），「二者任一未跑通不得进主表」；§3 唯一 teacher / 同 T 网格 / 同 θ / 同 calibration；§8 S2「任一无法复现 → 停止主表，转 `needs-evidence`」；§6 第 1 批 QCFS/FTBC/Parallel/DCGS/AdaFire 有官方码与回归数值。残留 W2/W3 由 H3/H4 硬条件兜住，属「可修复」而非「unavailable baseline」。 |
| evidence plan 是否可信 | **可信** | 冻结版 v1（10 节）：§2 五臂含 B4 失效边界、§3 前置统一、§4 唯一 CL 口径 ＋ 5 冻结 seeds ＋ 配对 bootstrap `R=5000` ＋ sign-flip 1000 ＋ BH `q<0.05`、§5 防泄漏划分、§6 批次与代码状态、§7 消融、§8 S1–S7 停止回退、§9 复现产物、§10 明确不做；叠加 `claim-evidence-matrix.md` / `strong-result-feasibility-contract.md` 的全 `<TBD>` 不编造纪律与 M0 实跑证据。 |

**为何不取另外三个值**：
- 不取 `revise`：6 个 startup 工件与新增的 M0 / `matched-protocol.md` 无事实性错误或结构缺陷需回炉重写；「视觉侧 0 正式实验」「expected_strong 预注册、G7 pilot 后锁定阈值」是 guidance 阶段**设计如此**，不是待修订缺陷。
- 不取 `pivot-with-rescue-route`：三处真空白仍成立、主攻方向未失效、最硬的 ViG 风险已有冻结/线性化 ＋ C5 边界诊断 ＋ M0 P6 数值坐实；`pivot` 在 S3/S4 命中（理论定位崩塌或单调性连续落 failure）时才触发，当前未触发。**注意**：此处 `pivot-with-rescue-route` 是 startup 值，与 `ccf-idea-reviewer` 的 recommendation 同名但不同体系，不要混读。
- 不取 `needs-evidence`：决定「是否推进」所需的证据已具备（novelty 组件层判定、数据可得性、排除清单、基线与官方数值、硬件、M0 实跑、冻结协议）；剩余缺口属 G0–G7 执行期产物或待确认项，且 S2/S5 已定义失败回退到 `needs-evidence`，不是现在预支。

**与 `startup-decision.md` 现有取值的关系（独立核验，非照抄）**：该文件已取 `proceed`（conditional proceed / proceed-with-narrowing），其 §3 列 10 条 narrowing、§4 列 S1–S7 回退映射。本评审**独立复核后确认 `proceed` 与新证据一致**，且 M0 实跑与 `matched-protocol.md` 兑现**强化**了其中「机制有可跑路径」「F3 工件兑现」两条依据；但本评审要求在其 §3 之外**追加 H1–H9 硬条件**（下列），因其 §3 未覆盖推论层检索、适配语义、单调性操作化、SHA 口径与成稿隔离等本轮新发现。

### Hard conditions for proceed（H1–H9，全部为硬约束）

- **H1 · 内部先验隔离（诚信硬门）**：成稿 `p7-draft.md` / `guidance-v3.md` 及其中全部数值（ρ_n=5.75、sum 聚合 ρ≈169、`var(U)=0.082 vs 0.083`、`mean(U)=0.481 vs 0.5`、Hoeffding 3.2–6.7×、ρ-不变性反直觉发现、`T≤8` 达 `ANN−1.5pp` 带内）与「成稿 §3.2 / §5.1」引用，全程标注「**用户提供的未公开先验（未发表、不充当公开证据）**」；仅作方法机制与理论命题出处核对；**不得当公开前作 / 公开证据、不得进任何公开证据表 / 结果栏 / 打分依据、不得替代本文的公开视觉实验**。违反 → 依 §8 S6 停止，回 `validation` 审计。
- **H2 · M0 边界不得外推**：M0 只验证固定线性算子类上的代数/概率命题与失效边界；**不得**把 P1–P6 写成「分类精度 / ρ_n/T 单调判据已被证明 / 能耗已证」。κ_n 单调性、κ_n–T2 张力、两解码兼容性、A5 消融、T1 非平凡性证明、`‖A‖` 上界证明、推论层针对检索 → 必须列入 G3 理论审计与 G4 novelty 门的**显式待办**，未过不得进 P4 / G7 主表。
- **H3 · 第 0 批必跑 ＋ 硬回退 ＋ 验收锚**：PASCAL（自行复现）与 TPP（官方码）第 0 批 must-rerun，二者任一未跑通不得进主表（§6 / §8 S2 → `needs-evidence`）；补齐 PASCAL 的**可判定复现验收锚**（对齐 QCFS `91.18%@T=2 / 93.96%@T=4` 回归测试范式；无法给出则单列 `not_applicable` 且不进主表）。
- **H4 · 可比性适配规则补写（协议升 v2）**：在 `matched-protocol.md` 补 §3.x，明确「为 ρ=1 网格算子导出的校准律在 ρ_n≠1 的 B2/B3 聚合上如何原样应用、不得针对 ρ 重调、无法实现则单列」，防止选择性适配污染中心问题的检验；任何偏离须版本化升 v2 并在 `pipeline-state.json` 记 `reopen`（协议 §0 已规定，须落实）。
- **H5 · 核心判据操作化 ＋ 口径统一**：把「conversion loss 差距随 ρ_n/T 单调」的趋势检验、比较单元（跨 ρ 网格 / 跨方法）、统计判据写入 §4 指标定义；统一 rev2 §1 第 4 条与 §8 S4 的证伪口径，消除范畴错位残留。
- **H6 · 失效边界与代价不得删／不得隐瞒**：原版 ViG（动态 KNN ＋ max-relative）作为 B4 / C5 失效边界诊断保留、不进主结果、不得删（M0 P6 已给可测预测：`0.7476370778501276` / `1.105089450044243`）；冻结 / 线性化相对原版 ViG 的 ANN teacher 精度代价（R4 / A6）须量化报告。
- **H7 · 结果与效率口径**：全部 `expected_strong` 写「预注册目标 / 非实测」＋ baseline-calibrated 依据 ＋ failure signal，阈值由 G7 pilot 后锁定，**现在不得填任何绝对 headline gain**；SynOps / spike count / 峰值显存 / wall-clock 一律标 proxy，不写能耗实测 / 硬件收益 / 精度 SOTA；不声称发明任何已被占组件，不声称 T1/T2/κ_n 为「prior-art 无法得到的新数学结果」。
- **H8 · 证据工件口径一致**：统一 `m0-results.json` 的 SHA-256 记录口径（同时记「规范化 LF 无尾随换行 raw SHA = `2498875f…`」与「磁盘文件字节 SHA = `aecfa88e…`」，或统一改为二进制字节口径）；P4 对数以文件为准（1920 对 / 每 T 384 对）；收敛 `m0-theory-check.md` 三处过表述（P2「系统项同时趋零」、P3「复现 §5.1」、P5「Bernoulli 方差 >0」在 T=16 为 `0.0`）与第 34 行格式；把 M0 结果、`matched-protocol.md`、成稿隔离标注统一登记进 `claim-evidence-matrix.md`。
- **H9 · novelty 硬门留给 G0 / G4，proceed 不等于 novelty 已站稳**：`proceed` 只表示「可进 G0」；G0 推论层针对检索与 G4 非重复门若命中近邻，或 G3 证明 T1 可一行代数照搬，或 G7 单调性连续落 failure，按 §8 S4 / `startup-decision.md` §4 回退到 `pivot-with-rescue-route`；G0 前另须核验官方当年 venue policy / review form（W9）。

---

## Optional next-module decision:

- **CCFA Handoff Mode: PARTIAL**（依 `SKILL.md` 与 `handoff-modes.md`）。本任务为**独立红队评审**，用户未请求任何 sibling-skill 切换，也未授权把未发表 idea 文本用于检索；依 workflow #10「if a module is denied, stop at verdict, risks, and action queue」，本评审**停止在 verdict / risks / action queue，不执行任何 handoff**。
- 未切换的模块：`ccf-idea-optimizer`（G3 推导 / 主张收敛 / 受控 P3）、`ccf-literature-searcher`（G0 推论层针对检索，需用户显式授权）、`ccf-experiment-designer`（`matched-protocol.md` 升 v2 ＋ 第 0 批复现 ＋ 横评）、`ccf-submission-checker`（核验目标期刊当年官方 policy / review form）、`ccf-integrity-auditor`（W10 全包口径一致性 / W11 隔离标注）。
- 若用户**显式授权**后续切换，按 PARTIAL 模式建议顺序：`ccf-idea-optimizer`（先做 G3 第 1 步，纸面为主、无算力成本）→ `ccf-literature-searcher`（G0 推论层检索，公共关键词）→ `ccf-experiment-designer`（再解 W2/W3/W4，含 PASCAL/TPP 复现）→ 视单调性结果决定是否进入后续写作。本评审不代写、不模拟上述模块的输出，也不预判其结果。
- 隔离声明：上述建议不含任何已执行的检索、实验或写作，不含任何录用概率与真实审稿记录；未生成任何 URL / DOI。

---

## Checklist status:

依 `SKILL.md` Mandatory Review Checklist（standard 模式 10 条）逐条如实标注。

| # | 检查项 | 状态 | 说明 |
|---|---|---|---|
| 1 | Target venue/journal、venue family、field、assumptions 明确 | pass | 按 Q1–Q2 期刊档评 ＋ 标尺声明 ＋ guidance 阶段边界 ＋ 成稿可读性/隔离标注 ＋ SHA/数值核验结论；官方当年政策未核验已注明 |
| 2 | 每个 idea 归一化为 problem / gap / root challenge / insight / method mechanism / expected evidence / limitation | pass | 见 `Normalized idea`（7 要素 ＋ 内部先验隔离标注 ＋ rev3 新增证据） |
| 3 | Literature status 标注为 searched / partially searched / user-provided only / not searched | pass | novelty = `searched`（组件层，用户指令）；本会话检索动作 = `user-provided only`；**推论层 = `not searched`**；见 `Search basis` |
| 4 | standard 模式有来自 public-safe literature search 的 closest-work table，除非用户禁止浏览或隐私阻止 | **partial** | closest-work 表已建（8 条，字段齐全，针对 rev3 重评），但来源为**用户提供的独立文献核验结论**，本会话未执行公开检索，且推论层未检索；依据：用户明确指定 search basis 与已核验结论，依 `privacy-and-evidence.md` 未把未发表 idea 文本用于查询；未编造任何 URL/DOI |
| 5 | 五个专家角色独立应用：field / method / experiment / AC-venue / skeptical prior-art | pass | 见 `Per-expert reviewer notes`：5 个必需角色 ＋ 1 个 optional Theory/Proof Expert，各自独立 ＋ Panel Synthesis，分数与置信度分开 |
| 6 | 所有 rubric 维度 1–5 打分或标注 n/a 与理由；每个 ≤3 含 deduction / evidence basis / repair condition / 预期分数变化 | pass | 10 维全打；**6 个 ≤3 项**均有完整明细块（扣分理由 / 证据基础 / 为什么重要 / 修复条件 / 预期分数变化 / development-potential effect）；4 个 >3 项在表内给出 deduction 与 repair，Method/Experimental 另写明「升 1 分依据」 |
| 7 | Fatal risks 与可修复弱点、局部细化分开 | pass | 见 `Serious blockers`：A 段 0 条 fatal（含逐条核对表）、B 段 Q1′–Q4′ 准 fatal、C 段 W1–W11 fixable、D 段隔离项 |
| 8 | Confidence 与 score 分开报 | pass | 综合 Confidence=Medium 单列；各维 Confidence 在 rubric 表；各专家 Score tendency 与 Confidence 分行；未因置信度下调分数 |
| 9 | 推荐值为 5 选 1 之一；`abandon` 仅用于无可测主张且无重构 | pass | `pivot-with-rescue-route`；abandon 条件已论证不满足；另按 `f-guidance-builder-v1` 独立给 `startup-decision = proceed`（4 选 1），两体系已显式区分 |
| 10 | 任何可选模块切换遵循 CCFA handoff mode；若被禁用则只输出 upgrade actions | pass | PARTIAL 模式，未执行 handoff，仅输出 `Upgrade / pivot actions` 与建议 owner |

补充标准模式 `task-modes.md` 状态：
```text
Mode: standard
Checks run: 完整 mandatory checklist + 输出契约 21 字段 + 定量反馈 + panel 纪律 + fatal gates + 分数段映射 + 逐维变化分解 + 新增证据真实性核验（SHA/CRLF/数值/成稿可读性）+ Output Quality Gate
Checks skipped: 无（除 #4 标 partial）
Unresolved risks: G3 解析推导未做、G0 推论层未检索、κ_n 单调性与 κ_n–T2 张力未解、PASCAL/TPP 待复现与验收锚缺、ρ=1 校准律适配语义未定义、单调性未操作化、视觉侧零正式实验、官方当年 venue policy 未核验、SHA/P4 对数/三处过表述口径待统一
```

---

## Output self-check:

依 `review-output-standards.md` Output Quality Gate 与 `task-modes.md` Output Quality Gate 逐项自检（作为读者通读一遍后确认）。

| # | 检查项 | 结果 | 具体确认 |
|---|---|---|---|
| 1 | 小节顺序匹配承诺的输出契约 | ✓ | 从 `## Verdict first:` 到 `## Output self-check:` 共 **21 个契约字段**，顺序与 `SKILL.md` Output Contracts（单 idea / standard）完全一致；首字段即 Verdict first，末字段即 Output self-check；`### Startup-decision` 与 `### Hard conditions for proceed` 为三级标题、嵌在 `## Recommendation:` 内，不破坏 21 个二级字段契约 |
| 2 | 每个表格有合法 Markdown 分隔符且每行列数一致 | ✓ | Rubric 表 6 列、Closest-work 为字段块（非表）、F1/F2/F3 与四问判定表 3 列、Serious blockers A 段 3 列、专家 Panel Synthesis 为代码块、逐维分解表 3 列、Score-change 表 3 列、Startup 判据表 3 列、Fixability 表 9 列、Checklist 表 4 列、本表 4 列；逐行核对列数一致，单元格内无裸 ASCII `\|` 破坏分隔（公式 `‖A‖`、`ρ_n/T`、`κ_n`、`A·1=ρ_n·1` 不含竖线） |
| 3 | 分数、置信度、推荐内部一致 | ✓ | 加权计算 340/100 = 3.40 → `**Overall:** 3.4`（一位小数）；1–10 转换 ≈ 6.8；综合 Confidence=Medium 与各维 Confidence 分开；3.4 落在 calibration 3.0–3.6 段 → `pivot-with-rescue-route`，五条数值 fatal gate 均不触发、两条临界，已在 `Weighted final score` 解释分数段与 5 选 1 的映射；相对第二次 +0.24 的逐维分解（+0.14 +0.10）与 3.40 一致；`startup-decision = proceed` 属另一体系，已显式说明「不矛盾」及映射，无矛盾 |
| 4 | 项目符号语法平行、动作风格一致 | ✓ | `Upgrade / pivot actions` 统一用 `[标签] + 动作动词` 开头；Fixability / Score-change 用名词短语或条件句；H1–H9 统一用「主题 · 动作」＋ 硬约束句 |
| 5 | 因果/递进逻辑显式（问题→原因→后果→行动） | ✓ | 每个 ≤3 块按「扣分理由→证据基础→为什么重要→修复条件→预期变化」排列；Serious blockers 按 fatal(0)→准 fatal→fixable→隔离分层；Startup 按「四判据→三值排除→H1–H9」；最小可行修复路线按依赖顺序编号 |
| 6 | 语言内标点一致 | ✓ | 正文中文全角标点（，。；：）；公式、字段名、文献名、venue、英文缩写、代码标识符、SHA 值保留半角；Markdown 表格分隔符与代码块为半角（格式必需） |
| 7 | 无 TBD / TODO / [fill] / 空标题占位 | ✓ | 无占位符；引用他工件中的 `<TBD>`、`TBD/需确认` 属「描述其纪律 / 待办」而非本报告的占位符；所有字段均有实质内容 |
| 8 | 无通用套话（「需要更多实验 / 创新性不足 / 进一步完善 / 加强 related work」等）无锚点残留 | ✓ | `Strict reviewer comments` 10 条均带 Anchor；每条批评均指向具体 claim / 机制 / prior-art / 缺失工件 / 逻辑残留 / 口径差异 / 可行性约束，并给出对应修复或 pivot |
| 9 | 每个 ≤3 分项含扣分理由 / 证据基础 / 修复条件 / 预期分数变化（用户硬要求） | ✓ | 6 个 ≤3 维度各一个明细块，四项齐全，另附 Why it matters 与 Development-potential effect；4 个 >3 项不触发且已在表内给 deduction / repair |
| 10 | 五个专家角色独立、各自给具体拒稿级质疑或说明为何没有；置信度与分数分开 | ✓ | 5 必需角色 ＋ 1 optional（Theory/Proof，因 M0 相关而加）均含 Score tendency（分数）与 Confidence（置信度）两行 ＋ Score-change condition；均给 strict rejection-grade concern ＋ Anchor ＋ Why ＋ Fatal ＋ Repair ＋ Development note；无角色被强行安排「无质疑」或赞扬，Panel Synthesis 未平均掉致命弱点 |
| 11 | fatal risk 与可修复弱点明确区分；含 score-change conditions 与最小可行修复路线 | ✓ | `Serious blockers` A 段 0 条 fatal ＋ B 段 Q1′–Q4′ ＋ C 段 W1–W11 ＋ D 段隔离；`Score-change conditions` 表 C1–C8 含升分与反向降分；`Upgrade / pivot actions` 内含按依赖排序的「最小可行修复路线」5 步 |
| 12 | 推荐值仅为 5 选 1 之一 | ✓ | `pivot-with-rescue-route`（accept-to-develop / revise / pivot-with-rescue-route / abandon / needs-literature-search 五者之一）；`startup-decision` 为 4 选 1 之 `proceed`，属 `f-guidance-builder-v1` 独立体系，已标注 |
| 13 | 禁止编造：文献 / 数值 / 实验结果 / 评审意见 / 录用概率 | ✓ | 全部文献仅来自用户提供的核验清单（venue/year 照录，未附 URL/DOI，未转录协议中已存在的仓库 URL）；所有实验数值均照录 `m0-results.json` / `m0-theory-check.md` / `matched-protocol.md` 或成稿原文，未改动；无录用概率、无真实审稿人 / meta-review 引用；专家意见与 Strict reviewer comments 已声明为「本红队 panel 独立判断」；加权分数与预期变化为按 rubric 计算 / 条件性表述，非实验结果 |
| 14 | novelty 状态标为 searched 并写明边界 | ✓ | `Search basis` 标 `searched`（组件层）＋ **推论层 `not searched`** ＋ 4 条边界，据此封顶 novelty 3 / conf 3；`Novelty delta` 逐条复核并设「特别回答：M0 是否改变 F2 核心质疑」，明确结论「没有改变，且部分证据反而强化原质疑」 |
| 15 | 未发表内部结果全程标注为「用户提供的未公开先验（未发表、不充当公开证据）」 | ✓ | `Target venue/journal and assumptions`、`Normalized idea`、`Closest prior art table`、`Novelty delta`、`Serious blockers`、各专家 notes、`Strict reviewer comments`、`Fixability`、`Upgrade / pivot actions`、`Evidence that would change my score`、`Recommendation`、`Output self-check` 中凡提及成稿数值 / §3.2 / §5.1 / `T≤8` 带内，均带完整标注；H1 设为诚信硬门；明确不进入 evidence / 打分依据、不替代公开视觉实验、不当公开前作 |
| 16 | 文件用中文撰写、保留技能要求的全部字段标题 | ✓ | 21 个英文契约字段标题原样保留（Verdict first: … Output self-check:），正文全部中文 |
| 17 | Verdict first 给结论、回复含 `**Overall:**` 行与 recommendation | ✓ | `Verdict first` 段含完整结论、四问判定表、F1/F2/F3 逐条判定与综合 recommendation；`**Overall:** 3.4` 在 `Verdict first` 与 `Weighted final score` 字段各以独立行给出；聊天回复另给 `**Overall:**` 行、recommendation、F2/F3 逐条判定与 startup-decision 建议值＋硬条件 |
| 18 | 四问逐条明确回答（用户硬要求） | ✓ | 问 1（F2 = **部分解决**，且严格区分「恒等式精确成立」与「ρ_n/T 单调判据在真实训练网络成立」，引 `m0-theory-check.md` 第 35 行）见 `Verdict first` 四问表、关键区分段、`Novelty delta` 特别回答、`Serious blockers` A/B；问 2（F3 = **已解决到 guidance 阶段程度**，「第 0 批必跑 ＋ 同骨干同 θ 同 calibration 是否足够」= 足够消除两难但残留 W2/W3/W4/W5 由 H3/H4/H5 兜住）见四问表、F3 判定、`Strict reviewer comments` 5/6/7、Startup 判据表；问 3（**0 条未解 fatal**）见 `Serious blockers` A 段逐条核对表、Fatal gates 清单、Startup 判据表；问 4（`startup-decision = proceed` ＋ H1–H9）见 `Recommendation` 字段下两个三级小节 |
| 19 | 成稿原文数值逐项核对（用户硬要求） | ✓ | ρ_n Cora 最高 **5.75**（`p7-draft.md` 第 68、189 行）；`var(U)=0.082 vs 0.083`、`mean(U)=0.481 vs 0.5`（第 272–273 行）；Hoeffding 松弛 **3.2–6.7×**（`guidance-v3.md` 第 20、38 行；`p7-draft.md` 第 372 行记 `3.5-6.7x for T>=4, up to 8.4x at T=1`，版本措辞差异已如实记录）；ρ-不变性反直觉发现（`p7-draft.md` §5.1 第 358–365 行「We originally predicted the opposite and were corrected by the experiment」）；`T≤8` 达 `ANN−1.5pp` 带内（第 93–95、445 行；`guidance-v3.md` 第 31 行）。全部标注为「用户提供的未公开先验（未发表、不充当公开证据）」 |
| 20 | 新增证据数值与 SHA 如实核验、差异不隐藏 | ✓ | P1 25 格最大残差 `9.880984919163893e-15`、P2 β\* 与 ρ 无关、P4 0 违反（**1920 对 / 每 T 384 对**，最大比 `0.7766068749112546`）、P5 20,000 激活 × 5 T / Σs=n 100% / 重建误差 `0.49999812148232436` / 条件方差 0、P6 `0.7476370778501276` 与 `1.105089450044243` 均照录；SHA 声明值 `2498875f…` 与磁盘 `aecfa88e…` 的差异已用 `sha256sum` ＋ LF 规范化 ＋ canonical re-dump 三步核实为 Windows CRLF（497 处）＋ 尾随换行所致、内容非篡改；用户「3840 对」与文件「1920 对」的差异以文件为准；M0「不训练 / 不报告分类精度 / 不证明能耗 / 不证明单调判据」的边界全程保留 |
| 21 | 不因前两次已给分而倾向升档 | ✓ | 相对第二次 3.2 仅 +0.24，且只有 Method / Experimental 两个「新增证据直接兑现」的维度各 +1；其余 8 维（含 Novelty、Conceptual、Acceptance 三个压档维度）**零变化**；无 +2 跳升；recommendation 仍 `pivot-with-rescue-route`（3.0–3.6 段由分数段直接得出）；`startup-decision = proceed` 是依 `f-guidance-builder-v1` 的「进 G0 唯一硬标准 = 无未解 fatal」独立得出，并已显式说明与 readiness 低分不矛盾、不等于 novelty 已站稳 |

**最终一致性确认**：本报告为**第三次独立红队评审**，未由前两次会话代写或模拟打分，未修改前两次报告，未抬分；如实承认 M0 实跑与 `matched-protocol.md` 兑现带来的**局部、可追溯**进步（Method / Experimental 各 +1），同时逐条论证 F2 的 novelty 核心质疑**未被 M0 消解**、F2 因此仅「部分解决」、整体仍 `pivot-with-rescue-route`；严格区分「恒等式精确成立」与「ρ_n/T 单调判据在真实训练网络成立」；成稿全程隔离标注为「用户提供的未公开先验（未发表、不充当公开证据）」，不进打分依据、不替代公开视觉实验；未把「视觉侧零正式实验」自动判 fatal（遵循 guidance 阶段硬要求）；未越权执行任何模块切换；未生成任何编造文献 / URL / DOI / 实验结果数值 / 录用概率；所有分数证据基础可追溯至 rev2 文本、前两次报告、用户提供的 prior-art 核验结论、M0 三件实跑工件、`matched-protocol.md` 与成稿原文。
