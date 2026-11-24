# Idea Cards · rev2（按独立红队 F1/F2/F3 修复后的主卡）

> 生成：2026-11-10｜依据：`idea-red-team-review.md`（独立 `ccf-idea-reviewer standard`，`**Overall:** 2.5`/5 = 5.0/10，`pivot-with-rescue-route`）的「最小可行修复路线」第 1、3 步。
> 本文件是 **CCFA-startup 的 repair 输入**，不是对第一次评审的改写；第一次评审原文完整保留，不修改、不抬分。
> 目录名沿用 `Operator-Agnostic-...` 仅为文件系统稳定；**正式论文标题与全文禁用 "Operator-Agnostic" 这一命名**（红队指出它掩盖"仅适用固定线性算子"的强假设）。

---

## 0. 命名与定位修订（先解决 F1）

| 项 | rev1（被红队判 fatal） | rev2（本卡） |
|---|---|---|
| 工作标题 | Operator-Agnostic ANN-to-SNN Conversion | **When Does ANN-to-SNN Conversion Fail? A Matched-Protocol Study across Grid, Frozen-Graph Vision, and Graph Message-Passing Operators** |
| 中心问题 | 统一"非网格、数据依赖的邻域聚合"的误差 | **当传播算子固定、非负、线性但行和 ρ_n ≠ 1 时，为行随机算子导出的转换校准律是否仍最优？** |
| 算子类 | 声称覆盖数据依赖 / 动态 / 非线性算子 | **明确只覆盖固定、非负、线性传播算子类**；冻结 KNN 图与线性化聚合只是"构造该类成员"的手段，**不是**对原版 ViG 的脉冲化主张 |
| 原版 ViG | 被写成"首次脉冲化"卖点 | **显式的失效边界诊断实验**（动态 KNN + max-relative 非线性 → 恒等式按预测不成立），不进主结果、不得删除 |
| 目标档位 | CVPR/ICCV/NeurIPS 主会 + Q1 | **主投 IEEE TNNLS / Q1–Q2 类脑与神经网络期刊档**（红队 AC 专家指出的自洽落点；Q2+ 满足 f-guidance-builder-v1 门槛）。CVPR/ICCV 需 ImageNet-1K（G2 不可得）→ 本轮不主张 |
| 贡献类型 | 新方法 | **理论判据 + 统一协议横评 + 失效边界**（empirical/diagnostic，允许增量但须充分验证） |
| 数学组件措辞 | "由恒等式推出 β*、膜电位解码、确定性两阶段" | **全部继承前人**：β*→Deng & Gu ICLR'21；零期望偏置→QCFS/FTBC；膜电位解码+精确等式→Dual-Phase TNNLS'24；确定性精确计数→PASCAL TMLR'25；两阶段→TPP ICML'25/SpikeConverter AAAI'22；跨 CNN+GCN→One-Spike SNN。**本文不声称发明其中任何一项** |

---

## 1. 主卡 OAC-rev2（唯一主攻）

**Bottleneck（瓶颈）**
ANN→SNN 转换的误差分析与校准律几乎全部在**行随机、逐元素**的卷积/线性算子上推导（QCFS、FTBC、TPP、并行转换、DCGS、AdaFire 皆然）。但视觉图骨干与图消息传递使用的传播算子行和 ρ_n 可以远大于 1（成稿实测 GCN 对称归一化在 Cora 上 ρ_n 最高 5.75；sum 聚合 ρ_n 可达 169）。为 ρ=1 导出的偏置校准、阈值缩放与量化步长，在 ρ_n≠1 时是否仍是最优，未见系统检验，也缺少统一协议下的横评。

**Causal / algorithmic mechanism（机制）**
对固定、非负、线性传播算子 A，转换误差满足精确恒等式 `B̂₂ − B₂ = A (E₁ W₂)`，`E₁ = count₁/T − ReLU(B₁)`（成稿 §3.2 已证，本文继承并明确归功）。由此得到**两条 row-stochastic 文献给不出的推论**（本次的新理论抓手，均需在本轮重新推导并数值验证）：

- **T1 · ρ 加权系统性误差**：在相位随机化假设下 `E[E₁] = β − 1/(2T)`，闭环偏置 `β* = θ/(2T)` 与 ρ 无关；但把均值误差传播过 A 后，margin 平移量为 `ρ_n/(2T) · Σ_h DW_c[h]`，即**系统项按行和 ρ_n 加权**。所以"校准不足"在非行随机算子上不是幅度噪声，而是有确定方向、随度数/聚合权重变化的 margin 偏置。
- **T2 · 相对误差的 ρ-不变性**：margin `Δ_n` 本身由同一聚合 logits 算出，因此相对转换误差由 `‖a_n‖₂ ‖DW‖₂ / (T Δ_n)` 控制，而非 `ρ_n`。成稿 §5.1 明确记录：作者原本预测 sum 聚合（ρ 达 169）会灾难性退化，实测被推翻，进而给出 ρ-不变的正确解释。**这个反直觉结论是可证伪的、且直接决定"现有方法何时失效"**。

**由 T1/T2 导出的可证伪判据（本文的核心新推论）**
定义算子非行随机度 `κ_n = ρ_n / ‖a_n‖₂`。预测：为 ρ=1 推导的校准律在 `κ_n` 大且 T 小（T≤4）时系统性欠校准，其 conversion loss 相对 ρ 加权闭式偏置的差距随 `ρ_n/T` 单调增大；而在 ρ≈1 的标准 CNN 算子上两者等价（非劣效）。这给出一个**先验可算、逐节点/逐样本可检验**的"何时失效"判据，而不是一句"换了个算子"。

**Assumptions（假设，逐条列明）**
A1 传播算子 A 在推理时**固定**（KNN 图在前处理冻结、attention 不随样本重算）；A2 A **非负、线性**（max-relative、softmax 动态权重不在适用类）；A3 亚阈值残差 `U ~ Uniform[0,θ)` 且跨 (m,h) 近似独立（成稿实测 `var(U)=0.082` vs 均匀 0.083、`mean(U)=0.481` vs 0.5）；A4 激活落在 `[0,θ]` 的单元占比足够高（成稿 θ=1 无全局缩放时越界质量 ≤1.01%，超出部分以显式饱和项 σ_n 单列）；A5 所有比较方法在同一 teacher、同一被固定骨干、同一 T/θ/calibration 数据下重跑。

**Falsification condition（可证伪条件）**
- 若 T1/T2 的浮点残差在固定线性算子上不趋于 0 → 恒等式或其适用条件错，主卡作废。
- 若 conversion loss 与 `ρ_n/T` 无单调关系，或 ρ≈1 的 CNN 上出现"我们显著更好" → 核心判据被推翻，pivot 为纯 benchmark 故事。
- 若原版动态/非线性 ViG 上恒等式**仍然成立** → 适用边界写错，必须扩展算子类或放弃 T1/T2。
- 若与 PASCAL / TPP 在统一协议下等价（无可归因增益）→ 按红队 `[pivot]` 路线，把贡献完全收敛为"首次统一协议横评 + 失效边界"，降级定位，不硬撑新方法。

**Contribution type**
理论判据（T1/T2 的跨算子类推广与"何时失效"判据）+ 评估/实证发现（首个固定线性算子类上、含全部最近邻基线的 matched-protocol conversion loss 横评）+ 失效边界诊断。**不是新神经元模型，不是新数学组件。**

**Known feasibility risks**
R1 一般 A（ρ≠1）下 β* 的严格推导与 `‖A‖` 误差上界尚未在本文重做（红队 W3）→ 列为 **M0 纸面里程碑，实验前必须完成**，未过不得进 P4；R2 `‖A‖>1` 时 E₁ 的跨层累积界缺失 → 同上，须给 Bernstein/Hoeffding 型界并数值验证；R3 膜电位累加解码与确定性计数 s[t] 可能冗余 → 用消融 A5 判定，冗余则删；R4 冻结 KNN 图会削弱 ViG 表征力，须量化相对原版的性能代价，不得隐瞒；R5 PASCAL / CS-QCFS / ECL 无官方代码，须自行复现，且 PASCAL / TPP 是**最决定性**的两个基线，必须排在第一批；R6 ImageNet-1K 为 G2 不可得 → 主投 TNNLS 档，不声称 CVPR 档规模。

---

## 2. 对照卡 B：纯标准 CNN 视觉横评（不取主攻）

- Bottleneck：低 T 下各转换方法数值口径不一致。
- Mechanism：统一 T/θ/seed/SynOps 口径重跑 QCFS/FTBC/TPP/Parallel/DCGS/AdaFire。
- Assumptions：全部算子 ρ≈1。
- Falsification：若我们与最强基线无差异 → 纯 benchmark 表。
- Contribution type：评估。
- **为何不取主攻**：红队 F2 已判"缺横评"是工程缺口而非科学瓶颈；在 ρ≈1 上 T1/T2 退化为已知结论，novelty 更低，且用户成稿的 ρ 加权资产完全用不上。本卡作为**主卡内的对照组**（CNN 臂）保留，不独立成篇。

## 3. 对照卡 C：纯事件视觉时序转换（不取主攻）

- Bottleneck：异步事件流的时序错位。
- Mechanism：CIFAR10-DVS 上比 T 与相位策略。
- Assumptions：无官方 split（社区 9000/1000）、8.38 GB 事件流、需降采样。
- Falsification：若增益可由静态帧复现 → 时序机制不成立。
- Contribution type：实证。
- **为何不取主攻**：与"图/算子"资产无关；数据无官方 split、许可与分辨率需额外处理；R91 历史在果蝇/事件线已证伪 degree 轴。仅作为主卡的**稳健性臂**（可选，不进主 claim）。

---

## 4. 本卡相对红队三条 fatal 的逐条处理

| Fatal | 处理 | 是否"已解决" |
|---|---|---|
| F1 主张—适用条件错位 | 中心问题改为"固定线性但非行随机算子上校准律是否最优"；冻结/线性化明写为**构造算子类成员**，原版动态/非线性 ViG 明写为**失效边界**；不再声称覆盖数据依赖算子 | **表述层已解决**；是否真正自洽须由 M0 推导 + C5 边界实验确认 |
| F2 novelty 重述/组合 | 引入 T1/T2 两条 row-stochastic 文献得不到的推论与 `κ_n` 可算判据；全文删除"发明数学组件"措辞；接受 Q1–Q2 期刊增量定位 | **部分解决**，最终判定须由统一协议横评（含 PASCAL/TPP）确认；若等价则按 `[pivot]` 降级 |
| F3 横评可比性两难 | 成文 `matched-protocol.md`：所有基线（含自行复现的 PASCAL/TPP/CS-QCFS/ECL）在**同一批固定骨干**上、同 T/θ/calibration/conversion-loss 定义重跑；PASCAL 与 TPP 列第一批 must-rerun | **设计层已解决**；执行层属 G7/P4 证据，guidance 阶段只需计划完备 |

> 诚实声明：本卡**没有**"补实验"，因为 guidance 阶段按定义就是实验前。红队把"视觉侧零正式实验"计入 fatal 是评当前就绪度；`f-guidance-builder-v1` 的 startup 规则只要求 evidence plan 可行、机制有可跑路径、最近邻基线可复现。上述条件已写入 `strong-result-feasibility-contract.md` 的 M0–M4 与 S1–S7。
