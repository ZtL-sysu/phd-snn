# strong-result-feasibility-contract.md

> **`feasibility-contract.json` 的内容草稿文本**。本 Agent **只写本 Markdown 草稿**；JSON 文件本身由**主会话按哈希最终生成**，本 Agent 不写 JSON、不指定哈希值、不虚构任何文件名之外的产物。
> 按 `ccf-experiment-designer` 职责生成（`design` 模式，evidence-bound，无真实结果）
> 生成者：CCFA startup 包撰写员（本 Agent） · 日期：2026-11-10
>
> **给主会话的转换说明**：下文 §3–§7 每个 claim 块用统一字段，建议 JSON key 依次为
> `claim_id / claim / mechanism / prerequisite_assumptions / falsifying_ablation / exact_dataset_split / primary_metric_direction / simple_baseline / strongest_feasible_domain_baseline / matched_internal_control / minimum / expected_strong / failure / implementation_readiness / reviewer_question / stop_and_return`。
> 所有 `<TBD*>` 为占位符，哈希前**不得**替换为任何数值。

## 0. 硬性纪律（贯穿全文）

1. **零虚构**：不出现任何本项目实验结果数值、虚构评审分数、虚构 URL。文中出现的数字仅为：协议参数（T 网格、seed 数、bootstrap 次数）、用户给定的已核验环境/数据事实、预注册目标阈值（ANN−1.5pp 带）、以及用户给定的公开已发表背景数值（仅作 calibration 参考，不进结果栏）。
2. **所有 `expected_strong` 一律写成「预注册目标 / 非实测」**，并附 **baseline-calibrated 依据** 与 **failure signal**；不凭空设定 headline gain。
3. **baseline-calibrated**：一切 `minimum / expected_strong / failure` 阈值以 **G7 在 G1 可得数据、同协议复现的基线值为锚**（§1）；G2 排除的 ImageNet 官方数值只作文献背景，不作阈值锚、不作 headline 对照。
4. **诚实边界**：不声称发明 `β*=θ/(2T)` / 膜电位解码 / 两阶段；不声称精度 SOTA、能耗实测、生物保真；SynOps / spike count / 峰值显存均为 **proxy**；CIFAR 无官方 val split 须预注册从 train 切；test 只在最终评测用一次。
5. **内部先验**：用户未发表内部先验（图节点分类 T≤8 达 ANN−1.5pp 带内；视觉侧 0 正式实验）**仅作内部校准，绝不当公开证据**。

---

## 1. Baseline-calibration 决策规则（全局，阈值如何锁定）

> 本契约 **不预设任何绝对 headline gain**。所有数值阈值在 G7 pilot 复现基线后按以下规则锁定，锁定值写 `<TBD_locked_after_pilot>`。

- **锚（anchor）**：`strongest_feasible_domain_baseline` 与 `matched_internal_control` 在**相同 dataset / split / T / 5 seeds / 同一统计管线**下的 G7 复现值。官方 ImageNet 数值不参与锚定（G2 排除）。
- **差值定义**：`Δ = CL(method) − CL(anchor)`，单位 pp，负 = 更好；`CL = ANN teacher top-1 − SNN top-1`。
- **MDE（最小可检测效应）**：由 5 冻结 seeds 的配对 bootstrap（`R=5000`）在 pilot 上估计；符号为 `MDE`，具体数值 `<TBD_locked_after_pilot>`。
- **baseline 波动**：`σ_baseline` 为锚基线在 5 seeds 上的 CL 标准差；系数 `k` 由预注册检验功效决定，`k·σ_baseline` 数值 `<TBD_locked_after_pilot>`。
- **三档定义（通用）**：
  - `minimum`（可发表下限）：方向正确、`Δ ≤ 0` 对 simple baseline，且对 matched internal control 经 BH 校正后不显著劣化；pp 阈值 `<TBD_locked_after_pilot>`。
  - `expected_strong`（**预注册目标 / 非实测**）：`Δ ≤ −max(MDE, k·σ_baseline)`。依据 = must-rerun 基线在本项目协议下的复现分布（+ 私有内部先验仅作校准）。failure signal = pilot 基线方差过大导致 `MDE` 超过任何合理效应，或连续两轮 pilot 的 `Δ` 落入 `failure` 区。
  - `failure`：`Δ ≥ 0` 且经 BH 校正后显著（对最强基线），或理论残差超容差，或 C5 边界未按预测失效。
- **C1 / C5 例外**：主指标为恒等式残差 `r`，三档用数值容差 `ε` 表述（`ε` 由浮点精度 + 量化步长界定，`<TBD_locked_after_pilot>`），不套用 `Δ` 公式。
- **C3 例外**：`Σs[t]=n` 与「条件方差 = 0」为**硬约束**（解析可证 + 数值可验），不是统计目标；只有「不劣于 TPP」部分套用 `Δ` 公式。
- **C4 例外**：用户给定预注册带内目标 `CL ≤ 1.5pp`（ANN−1.5pp 带）。该值是**目标阈值、非实测**，baseline-calibrated 依据 = 内部先验（私有，仅校准）+ G7 同协议复现；`expected_strong` 仍须满足 §0.2 的标注与 failure signal 要求。

---

## 2. 全局实现就绪基线（implementation readiness 共享项）

各 claim 的 `implementation_readiness` 引用本节编号，并附本 claim 特有差异。

| 编号 | 子项 | 内容（已核验事实 / 占位符） |
| --- | --- | --- |
| IR-1 | 代码来源 | must-rerun 官方仓库（用户原样提供）：`github.com/putshua/SNN_conversion_QCFS`、`github.com/shizukanaskytree/FTBC`、`github.com/shizukanaskytree/TPP-SNN`、`github.com/hzc1208/Parallel_Conversion`、`github.com/h-z-h-cell/ANN-to-SNN-DCGS`、`github.com/bic-L/burst-ann2snn`；ViG：`huawei-noah/Efficient-AI-Backbones`（Apache-2.0，8 个预训练权重，GitHub Release 无摩擦）；**GCN 消息传递实现来源 `TBD / 需确认`，不编造库名或 URL** |
| IR-2 | 缺失组件 | `torchvision` 缺失（conda `dyg-cold` 需补装，G6 blocker）；自研：统一 `A` 抽象层、确定性 `s[t]` 调度器、膜电位累加解码、恒等式残差探针、跨骨干统一 conversion loss 横评 harness；adaptation-attempt（PASCAL TMLR'25 / CS-QCFS Neural Networks'25 / ECL arXiv'25）无官方代码，需自行复现且数值标 `NOT VERIFIED` |
| IR-3 | prototype 里程碑 | **M0** 补装 `torchvision` + 跑通 ViG 权重加载 + 冻结 KNN 图 + 线性化聚合（同时保留原版 ViG 对照）；**M1** 统一 `A` 抽象层 + 计数/膜电位解码切换 + `β*` 闭式 + 残差探针；**M2** 确定性两阶段 `s[t]` 调度器 + 零条件方差验证；**M3** GCN 消息传递接入同一 `A` + 跨骨干横评 harness；**M4** 5 seeds × T 网格 + 统计管线（bootstrap/sign-flip/BH）+ pilot 基线复现 → 锁定 §1 阈值 |
| IR-4 | 算力 / 显存 / 时长预算 | 本机 Windows 11 / 12 核 / RTX 3060 **12288 MiB** / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / 548 GB 空闲 / conda `dyg-cold`；显存上限 `≤ 12288 MiB`；**时长预算 `<TBD_estimated_after_prototype>`（不编造小时数）**；大规模实验用户已授权上远端 4090（novix），但 **guidance 阶段不提交**，G7 按需 |
| IR-5 | seed 数 | **5 冻结 seeds**（全 claim 统一） |
| IR-6 | 超参搜索预算 | 预注册固定网格 `T∈{1,2,4,8,16}`；`θ` 按层激活分位预注册（分位 `<TBD_locked_at_G0>`）；`β*=θ/(2T)` 闭式不搜；`n=round(a/θ)` 由 `a,θ` 决定不搜；**不做大规模 NAS / 随机搜索 / 测试集调参** |
| IR-7 | 复现产物 | checkpoint、config、seed list、环境锁（含 `torchvision` 补装记录）、log、conversion loss 表、恒等式残差探针输出、`s[t]` 序列与 `Σs[t]` / 条件方差记录、统计脚本（配对 bootstrap `R=5000` + sign-flip `1000` + BH）、冻结/线性化 ViG 与原版 ViG 的配置对照 |

---

## 3. C1 — 固定线性算子上的精确误差恒等式（理论 + 数值残差）

- **claim_id**：`C1`
- **claim**：对固定、非负、线性传播算子 `A`，转换误差满足精确恒等式 `B̂₂−B₂ = A(E₁W₂)`，且该刻画层类型无关。
- **mechanism**：把层间传播抽象为 `A` 后，第 2 层 SNN 与 ANN 输出之差精确等于 `A` 作用于「第 1 层量化误差经 `W₂` 传播」；误差传播从具体层实现剥离，只剩 `A` 的线性与固定性。数值残差 `r = ‖(B̂₂−B₂) − A(E₁W₂)‖` 应闭合到数值精度。
- **prerequisite_assumptions**：`A` 固定 / 非负 / 线性（**不要求行随机**）；ANN teacher 权重冻结、training-free；`θ` 由层激活统计预注册；`β*=θ/(2T)` 闭式成立；视觉侧 ViG 图已冻结且聚合已线性化、图侧为 GCN 消息传递；`T∈{1,2,4,8,16}`。
- **falsifying_ablation**：(a) 令 `A` 非线性；(b) 令 `A` 随输入/时间动态；(c) 膜电位累加解码 → 计数解码；(d) `A` 行随机归一化（匹配内部对照）；任一使 `r` 系统性超 `ε` 或随 T 漂移即证伪「线性/固定必要性」。
- **exact_dataset_split**：CIFAR-10 / CIFAR-100（**无官方 val split → G0 预注册从 train 切**，比例 `<TBD_locked_at_G0>`，test 最终一次）；Tiny-ImageNet（官方 100k/10k/10k val，test 无标签不用）；Planetoid（public split 每类 20 train / 500 val / 1000 test）。
- **primary_metric_direction**：主 = 恒等式残差 `r → 0`（辅助硬指标）；旁证 = `CL (pp) ↓`。容差 `ε = <TBD_locked_after_pilot>`。
- **simple_baseline**：朴素 rate-coding 转换（无 `β*`、计数解码、单相），实现来源自研 `<TBD>`。
- **strongest_feasible_domain_baseline**：Dual-Phase TNNLS'24 式精确误差等式在 G1 可得数据、同协议下的 G7 复现值 `<TBD>`；不直接引用其官方数值。
- **matched_internal_control**：保持 `A`/`θ`/`β*`/seeds/T 一致，仅把「固定线性 `A`」替换为「行随机归一化算子」。
- **minimum**：`r ≤ ε` 且对 matched internal control 不显著劣化（BH 后）。
- **expected_strong**：**【预注册目标 / 非实测】** `r ≤ ε` 且在跨 T、跨层、跨视觉/图骨干上一致闭合（CV `<TBD_locked_after_pilot>`）。**baseline-calibrated 依据** = 解析解与仿真一致性 + matched control 的残差分布 + 内部先验（私有，仅校准）。**failure signal** = `r` 随 T 系统性漂移，或行随机对照也闭合（则 `A` 线性非必要，理论定位需重估）。
- **failure**：`r > ε`，或残差随 T 系统性漂移，或 C5 边界未按预测失效（与 C1 定位冲突）。
- **implementation_readiness**：IR-1（统一 `A` 抽象层自研 + ViG 权重）、IR-2（残差探针自研；`torchvision` 补装）、IR-3 → **M1**（+ M0 提供线性化算子）、IR-4（本机 3060，显存 ≤12288 MiB，时长 `<TBD_estimated_after_prototype>`）、IR-5（5 seeds）、IR-6（固定 T 网格、`θ` 分位 `<TBD_locked_at_G0>`）、IR-7（残差探针输出 + config + seed list）。
- **reviewer_question**：**Why does the mechanism work?** / **Does the method solve the stated problem?**（theory 家族：formal model、theorem statement、proof roadmap、数值闭合）。
- **stop_and_return**：冻结线性 `A` 上 `r > ε` → **停**，回 G4/G5 重推导，不进 G7 主实验；行随机对照也闭合 → **停**，回 G4 重定位「线性必要性」。

## 4. C2 — 非行随机算子上 `β*` + 膜电位解码相对强基线在 T≤4 降低 conversion loss

- **claim_id**：`C2`
- **claim**：在**非行随机** `A` 上，OAC（`β*=θ/(2T)` + 膜电位累加解码 + 确定性 `s[t]`）在 `T≤4` 相对最强可行域基线降低 conversion loss。
- **mechanism**：`A` 线性搬运量化误差 `E₁W₂`；`β*` 把误差期望对齐到零；膜电位累加解码消除计数截断误差；确定性 `s[t]` 不引入随机噪声 → 低 T 下 `CL` 可控下降。
- **prerequisite_assumptions**：同 C1，且 `A` **非行随机**（这是与既有归一化路线的差异点）；must-rerun 基线可在 G1 可得数据上同协议复现且偏差在容差内；官方 ImageNet 数值不参与对照。
- **falsifying_ablation**：(a) 去 `β*`；(b) 膜电位解码 → 计数解码；(c) 确定性 `s[t]` → 随机两阶段；(d) `A` 行随机化（回到强基线假设域）。若去掉组件后 `Δ` 不消失则降损归因失败。
- **exact_dataset_split**：CIFAR-10 / CIFAR-100（train 预注册切 val，test 最终一次）、Tiny-ImageNet（官方 val）；Planetoid 辅助；比例 `<TBD_locked_at_G0>`。
- **primary_metric_direction**：`CL (pp) ↓`；`Δ = CL(OAC) − CL(anchor)`（负 = 更好），阈值 `<TBD_locked_after_pilot>`。
- **simple_baseline**：朴素 rate-coding 转换；另加 QCFS 原始 floor/clamp 作简单已发表 sanity。
- **strongest_feasible_domain_baseline**：must-rerun 六者（QCFS / FTBC / TPP / Parallel Conversion / DCGS / AdaFire）在 G1 可得数据、同协议下 G7 复现的**最佳者**，值 `<TBD>`；DCGS / AdaFire 数值 `NOT VERIFIED`，以复现值为准。
- **matched_internal_control**：保持 `A`/`θ`/T/seeds 一致，仅把「`β*` + 膜电位解码」替换为「无偏置 + 计数解码」。
- **minimum**：按 §1 —— `Δ ≤ 0` 对 simple baseline、对 matched control 经 BH 后不显著劣化；pp 阈值 `<TBD_locked_after_pilot>`。
- **expected_strong**：**【预注册目标 / 非实测】** `Δ ≤ −max(MDE, k·σ_baseline)`（§1）。**baseline-calibrated 依据** = must-rerun 基线在本项目协议下 5 seeds 的复现分布（+ 私有内部先验仅校准）；**不预设绝对 pp gain**。**failure signal** = pilot 基线方差过大导致 `MDE` 超合理效应，或连续两轮 pilot `Δ` 落 `failure` 区。
- **failure**：`Δ ≥ 0` 且 BH 校正后显著（对最强基线），或 must-rerun 复现偏差超容差（触发 S2）。
- **implementation_readiness**：IR-1（6 个 must-rerun 仓库）、IR-2（`torchvision` + 解码/偏置组件）、IR-3 → **M1 + M4**（基线复现 + 统计管线）、IR-4（本机 3060；大规模上 4090 仅 G7 按需）、IR-5（5 seeds）、IR-6（固定 T 网格、`β*` 闭式不搜）、IR-7（CL 表 + 统计脚本 + 环境锁）。
- **reviewer_question**：**Is the comparison fair and current?** / **Does the method solve the stated problem?**
- **stop_and_return**：must-rerun 基线复现与官方数值偏差超容差（在可得数据同协议）→ **S2 停**，回 G6 修实现；`Δ` 连续两轮落 failure 区 → **S4** `pivot-with-rescue-route`（收窄到 C1+C5 或换 venue family，且须先确认 venue）。

## 5. C3 — 确定性第二相零条件方差且不劣于 TPP

- **claim_id**：`C3`
- **claim**：确定性两阶段时间误差扩散 `s[t]=round(t·n/T)−round((t−1)·n/T)`、`n=round(a/θ)` 满足 `Σs[t]=n`、条件方差 0、无 RNG，且 conversion loss 不劣于 TPP。
- **mechanism**：把总脉冲数 `n` 用取整差分确定性分配到 T 步，累计恰好 `n`；因无随机采样，条件方差为 0，理论恒等式与仿真严格闭合、同 seed 逐位可复现。明确**不主张发明两阶段框架本身**（TPP ICML'25 / SpikeConverter AAAI'22 已占），只主张第二相的特定确定性化（真空白②）。
- **prerequisite_assumptions**：`n=round(a/θ)` 由 `a,θ` 决定；`T∈{1,2,4,8,16}`；`Σs[t]=n` 对任意 T 成立；TPP 官方实现可在同 `n,θ,T` 下复现；无 RNG 泄漏。
- **falsifying_ablation**：(a) 确定性 `s[t]` → 随机化第二相；(b) 两阶段 → 单相均匀；(c) 变 `T` 检查 `Σs[t]=n` 不变性；(d) 变 `θ` 看 `n` 舍入稳健性。
- **exact_dataset_split**：同 C2（CIFAR-10/100 train 预注册切 val、Tiny-ImageNet 官方 val、Planetoid 辅助）。
- **primary_metric_direction**：硬约束 `Σs[t]=n`、`条件方差 → 0`、`无 RNG`；`Δ_CL = CL(OAC) − CL(TPP) ≤ 0`（不劣于）。
- **simple_baseline**：单相均匀脉冲分配（无两阶段）。
- **strongest_feasible_domain_baseline**：TPP 官方实现（`github.com/shizukanaskytree/TPP-SNN`）在本项目同协议 G7 复现值 `<TBD>`；官方 PMLR PDF Fig.1 数值仅文献背景且**图注与表内末列不一致须保留标注**。
- **matched_internal_control**：保持 `n`/`θ`/T/seeds/`A`/`β*` 一致，仅把确定性 `s[t]` 替换为 TPP 原版第二相。
- **minimum**：`Σs[t]=n` 且条件方差 = 0（解析 + 数值），`Δ_CL ≤ 0` 对 TPP（BH 后）。
- **expected_strong**：**【预注册目标 / 非实测】** 零方差逐位可复现（同 seed 完全一致）且 `Δ_CL ≤ −max(MDE, k·σ_baseline)`（§1）。**baseline-calibrated 依据** = TPP 同协议复现分布 + matched control 方差估计。**failure signal** = 同 seed 结果不一致（RNG 泄漏），或 `Δ_CL` 落 `failure` 区。
- **failure**：条件方差 > 0、`Σs[t]≠n`、或 `Δ_CL > 0` 且 BH 后显著。
- **implementation_readiness**：IR-1（TPP 仓库）、IR-2（确定性 `s[t]` 调度器自研）、IR-3 → **M2**（+ M4 统计）、IR-4（本机 3060，时长 `<TBD_estimated_after_prototype>`）、IR-5（5 seeds）、IR-6（`n` 由 `a,θ` 决定不搜）、IR-7（`s[t]` 序列 + `Σs[t]` / 条件方差记录 + 逐位可复现日志）。
- **reviewer_question**：**Why does the mechanism work?** / **Can the work be reproduced or audited?**（无 RNG、确定性调度）。
- **stop_and_return**：同 seed 复现不一致（RNG 泄漏）→ **停**，回 G6 修调度器；TPP 复现偏差超容差 → **S2**；`Δ_CL` 连续两轮显著为正 → **S4**。

## 6. C4 — 同一算子跨视觉骨干与图消息传递的通用性（图上复现 ≤1.5pp 带）

- **claim_id**：`C4`
- **claim**：用**同一 `A` / 同一 `β*` / 同一 `s[t]` / 同一 conversion loss 协议**，在「冻结+线性化 ViG 视觉骨干」与「GCN 图消息传递」上统一横评，图侧复现进入 ANN−1.5pp 带。
- **mechanism**：视觉侧冻结 ViG 的 KNN 图并把 max-relative 聚合线性化、图侧用 GCN 消息传递，二者都落成同一个固定非负线性 `A` → 同一恒等式 / 偏置 / 解码 / `s[t]` 协议可跨骨干复用，conversion loss 可直接横比。明确**不主张发明「跨 CNN+GCN」idea**（One-Spike SNN TETC'24/25 已占），只主张「同一固定线性 `A` + 统一协议 + ViG 首次脉冲化」这一具体协议（真空白③）。
- **prerequisite_assumptions**：ViG 图可冻结且聚合可线性化（否则触发 C5 边界）；GCN 聚合可写成同一 `A`；两侧共享 `θ` 预注册规则与统计管线；视觉侧须先有正式实验（当前 **0 正式实验**）。
- **falsifying_ablation**：(a) 视觉侧不冻结 KNN 图；(b) 视觉侧保留 max-relative 非线性；(c) 图侧换非 GCN 聚合；(d) 去掉跨骨干统一协议、各骨干独立调参。(a)/(b) 应使统一协议失效并与 C5 一致。
- **exact_dataset_split**：视觉侧 CIFAR-10 / CIFAR-100（train 预注册切 val，test 最终一次）、Tiny-ImageNet（官方 val）；图侧 Planetoid Cora / CiteSeer / PubMed（public split 每类 20 train / 500 val / 1000 test）；CIFAR10-DVS 仅外部效度补充（社区 9000/1000，无官方 split，须预注册）。
- **primary_metric_direction**：`CL (pp) ↓`；预注册目标阈值 `CL ≤ 1.5pp`（**目标阈值，非实测**）；达带最小 `T* = <TBD>`。
- **simple_baseline**：各骨干上朴素 rate-coding 转换（不共享 `A` 协议）。
- **strongest_feasible_domain_baseline**：各域内 must-rerun / One-Spike SNN 背景方法在**同协议** G7 复现值 `<TBD>`；内部先验（图节点分类 T≤8 达 ANN−1.5pp 带内）**仅内部校准，绝不当公开证据**。
- **matched_internal_control**：同一骨干上把「统一 `A` 协议」替换为「各骨干独立算子 / 独立调参」。
- **minimum**：图侧 `CL ≤ 1.5pp` 在 5 seeds 下方向成立，且对 matched control 不显著劣化（BH 后）。
- **expected_strong**：**【预注册目标 / 非实测】** 图侧进入 ANN−1.5pp 带且视觉侧同协议下 `Δ ≤ −max(MDE, k·σ_baseline)`（§1）。**baseline-calibrated 依据** = 用户未发表内部先验（**私有，仅内部校准，绝不当公开证据**）+ G7 同协议复现分布；**1.5pp 是带内目标阈值而非 headline gain，不是实测值**；视觉侧 0 正式实验 → 视觉侧全部 `<TBD>`。**failure signal** = 5 seeds 下图侧 `CL` 持续 > 1.5pp，或统一协议相对独立调参显著劣化。
- **failure**：5 seeds 下图侧 `CL > 1.5pp` 持续，或统一协议显著劣于各骨干独立调参，或 ViG 冻结/线性化实现失败（回 G4）。
- **implementation_readiness**：IR-1（ViG 8 权重 + must-rerun + GCN 来源 `TBD/需确认`）、IR-2（跨骨干横评 harness 自研 + `torchvision`）、IR-3 → **M0 + M3**（ViG 冻结线性化 + GCN 接入 + 横评）、IR-4（本机 3060；大规模 4090 仅 G7 按需）、IR-5（5 seeds）、IR-6（固定 T 网格、跨骨干共享 `θ` 规则）、IR-7（跨骨干 CL 表 + 冻结/线性化配置对照）。
- **reviewer_question**：**Does the result generalize across settings?** / **Is the comparison fair and current?**（同一协议）。
- **stop_and_return**：ViG 冻结图 + 线性化实现失败 → **停**，回 G4 重估硬风险；图侧连续两轮未入 1.5pp 带 → **S4**；内部先验被当作公开证据使用 → **S6** 停，回 validation。

## 7. C5 — 动态 / 非线性算子上恒等式按预测失效（边界诊断）

- **claim_id**：`C5`
- **claim**：原版 ViG（max-relative 含 max 非线性 + KNN 动态图）破坏线性/固定算子假设，恒等式按预测失效，残差显著大于冻结线性化版本。
- **mechanism**：原版 ViG 的 max 非线性使 `A` 不再线性、动态 KNN 使 `A` 不再固定 → 精确误差恒等式前提被破坏，`r` 应显著增大。这是**硬风险的诊断性 negative-result**，用于界定 OAC 的适用边界，不是主结果主张。
- **prerequisite_assumptions**：原版 ViG 与其冻结线性化版本权重一致；两者用同一 split / seeds / T / 残差探针；原版动态图与 max 聚合保持不改。
- **falsifying_ablation**：(a) 只引入 max 非线性（图仍冻结）；(b) 只引入动态 KNN（聚合仍线性）；(c) 两者同时 → 定位是哪一项破坏恒等式。若三者残差无差异则证伪。
- **exact_dataset_split**：视觉侧 CIFAR-10 / CIFAR-100（train 预注册切 val，test 最终一次）、Tiny-ImageNet（官方 val）；与 C1 用**同一 split / seeds / T**。
- **primary_metric_direction**：恒等式残差 `r`：**原版 ViG 显著 > 冻结线性化版本**（方向 = 失效）；`CL` 仅作旁证。分离度阈值 `<TBD_locked_after_pilot>`。
- **simple_baseline**：冻结 + 线性化 ViG（即 C1 主协议下的算子）。
- **strongest_feasible_domain_baseline**：原版 ViG 自身在可得数据上的转换结果 `<TBD>`；不引入新基线。
- **matched_internal_control**：保持权重 / split / seeds / T 一致，仅切换「冻结+线性化」↔「原版动态+非线性」。
- **minimum**：原版残差 > 线性化版本（方向正确，BH 后），分离度 `<TBD_locked_after_pilot>`。
- **expected_strong**：**【预注册目标 / 非实测】** 分离度显著且消融 (a)/(b) 能定位到 max 非线性或动态 KNN 之一。**baseline-calibrated 依据** = C1 冻结线性化版本在 5 seeds 上的残差分布（同一探针、同一协议）。**failure signal** = 两者残差在 BH 后不可区分。
- **failure**：原版 ViG **也满足恒等式**（残差 ≈ 线性化版本）→ 说明「线性/固定」非必要条件，OAC 理论定位崩塌（触发 **S3**）。
- **implementation_readiness**：IR-1（ViG 权重 + 保留原版聚合）、IR-2（残差探针 + `torchvision`）、IR-3 → **M0（保留原版对照）+ M1（残差探针）**、IR-4（本机 3060，时长 `<TBD_estimated_after_prototype>`）、IR-5（5 seeds）、IR-6（固定 T 网格）、IR-7（原版 vs 冻结线性化残差对照 + 配置对照）。
- **reviewer_question**：**What fails, when, and why?** / **Does the evidence match the venue's expectations?**（诊断与 limitation study）。
- **stop_and_return**：原版 ViG 残差 ≈ 线性化版本（边界未按预测失效）→ **S3 停**，回 G4 重定位理论前提；探针本身未通过 C1 校验 → **S1 停**。

---

## 8. 全局显式 stop-and-return 条件

| 编号 | 触发条件 | 返回目标 | decision 影响 |
| --- | --- | --- | --- |
| **S1** 数学 | 冻结线性 `A` 上恒等式残差超容差 `ε` | 回 G4 / G5 重推导，不进 G7 主实验 | 转 `revise` |
| **S2** 复现 | must-rerun 基线复现与官方数值偏差超容差（在 G1 可得数据、同协议） | 回 G6 修实现 | 转 `needs-evidence` |
| **S3** 边界 | C5 原版动态/非线性 ViG 也满足恒等式 | 回 G4 重定位「线性/固定必要性」 | 转 `pivot-with-rescue-route` |
| **S4** 阈值 | pilot 后 `MDE` 过大，或 `expected_strong` 连续两轮落 `failure` 区 | 收窄到 C1（理论）+ C5（诊断），或确认 venue 后换 venue family | 转 `pivot-with-rescue-route` |
| **S5** 资源 | `torchvision` 补装失败且无替代 / 远端 4090 未获调度 | 回 G0 | 转 `needs-evidence` |
| **S6** 诚信 | 任何环节出现虚构数值 / URL / 评审分数，或把内部先验当公开证据，或声称发明已占组件 / 能耗实测 / 生物保真 | 回 validation 审计 | 停，不可 handoff |
| **S7** 数据 | 误用 G2 排除数据自跑 / CIFAR val 未预注册 / test 被多次使用 | 回 G0 重预注册 | 转 `revise` |

> 上述条件均为**显式 stop-and-return**：命中即停止当前门并回退，不得带病推进、不得用「补一个实验」绕过。

## 9. 复现产物清单（IR-7 展开）
1. 环境锁：Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / conda `dyg-cold` + `torchvision` 补装记录。
2. `config` / `seed list`（5 冻结 seeds）/ `checkpoint` / 运行 `log`。
3. conversion loss 主表（§`claim-evidence-matrix.md` 表 R1 模板，值由 G7 填）。
4. 恒等式残差探针输出（表 R2 模板）。
5. `s[t]` 序列、`Σs[t]`、条件方差、同 seed 逐位可复现日志（表 R3 模板）。
6. 统计脚本：配对 bootstrap `R=5000` + sign-flip `1000` + BH。
7. 冻结/线性化 ViG 与原版 ViG 的配置对照（C5）。
8. baseline-calibration 记录：pilot 复现分布、`MDE`、`σ_baseline`、`k`、`ε`、各 `<TBD_locked_after_pilot>` 的锁定依据。

## 10. No-fabrication / 转换就绪状态
```
本文件 = feasibility-contract.json 的内容草稿；JSON 与哈希由主会话生成
零实验结果数值、零评审分数、零虚构 URL（代码/权重 URL 均为用户原样提供）
所有 expected_strong = 【预注册目标 / 非实测】+ baseline-calibrated 依据 + failure signal
所有阈值 = <TBD_locked_at_G0> / <TBD_locked_after_pilot> / <TBD>，未预设 headline gain
官方 ImageNet 数值仅文献背景（G2 排除），不进结果栏、不作阈值锚
内部先验仅内部校准，绝不当公开证据；视觉侧 0 正式实验
诚实边界：不声称发明 β*/膜电位解码/两阶段，不声称 SOTA/能耗实测/生物保真
stop-and-return S1–S7 已显式，命中即回退
待主会话：按本草稿生成 feasibility-contract.json 并计算哈希
```
