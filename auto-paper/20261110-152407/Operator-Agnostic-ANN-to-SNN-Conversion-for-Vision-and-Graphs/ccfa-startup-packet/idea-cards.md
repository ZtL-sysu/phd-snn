# idea-cards.md

> 机制级 problem-method 卡 · 按 `ccf-idea-optimizer` 职责生成（standard 模式）
> 生成者：CCFA startup 包撰写员（本 Agent） · 日期：2026-11-10
> 纪律：不编造文献/结果/基线数值/评审分数/URL；机制必须解释而非只命名；创新类型按 `problem-method-blueprint.md` 分类且只取 top 1–2；novelty 视 G4 `pass-with-narrowing` 为已知边界；内部先验仅作内部校准。

## 0. Venue lens 与模式

| 项 | 值 |
| --- | --- |
| Target venue | `CCF-A / AI, ML, CV` family（具体 venue `UNKNOWN / must-know 待确认`，见 `startup-stage-plan.md` §2） |
| 模式 | `standard`（成熟 idea 具象化，输出将 feed 文献检索与实验设计） |
| Development stance | 主卡收窄后的 `pass-with-narrowing`：不做发散扩张，只把 OAC 打磨成可证伪、机制清晰、贡献类型诚实的最小主张集 |
| Raw idea 状态 | 已由用户给出完整拟议方法（OAC）与「已核验事实」，本卡做机制化与边界化，不新增方向 |
| 隐私边界 | OAC 拟议方法细节、未发表内部先验属 `private`；本卡按用户授权写入本地工件，不用于任何公开检索 |

## 1. 主卡：OAC（Operator-Agnostic ANN-to-SNN Conversion）

### 1.1 一句话
把 ANN→SNN 转换的传播算子抽象为**固定、非负、线性矩阵 `A`**，在此算子上建立层类型无关的精确误差恒等式，并用「闭式偏置 + 膜电位累加解码 + 确定性两阶段时间误差扩散」在 T≤4 降低 conversion loss；视觉侧冻结并线性化 ViG 图聚合、图侧用 GCN 消息传递，用**同一算子**做跨骨干统一横评。

### 1.2 bottleneck
既有低时步 ANN→SNN 转换的误差分析深度绑定**具体层类型 / 具体骨干**（CNN 的卷积-池化堆叠、逐层归一化假设），且强基线多针对 CNN 设计。一旦算子不是行随机、或换成图消息传递 / ViG 的图聚合，误差传播公式与偏置校准不再自动成立，导致：① 缺少一个「层类型无关」的精确误差刻画；② 缺一个在同一算子下公平比较视觉骨干与图骨干 conversion loss 的协议；③ 低时步下随机化时间误差补偿引入条件方差，复现与理论一致性受损。

### 1.3 causal / algorithmic mechanism（解释，非命名）

**核心机制（非显然交互）**：只要把层间传播写成固定线性 `A`，第 2 层转换误差就**精确**等于 `A` 作用于「第 1 层量化误差经 `W₂` 传播」的结果 —— `B̂₂−B₂ = A(E₁W₂)`。该恒等式把「误差如何跨层传播」从具体层实现中剥离出来，只剩 `A` 的线性与固定性。于是：
- **为何能降 conversion loss**：误差项 `E₁W₂` 可被 `A` 线性搬运，配合闭式偏置 `β*=θ/(2T)` 把量化误差的期望对齐到零，再用**膜电位累加解码**替代计数解码消除计数截断误差，使低 T 下残差可控；
- **为何要确定性两阶段**：时间维度上把总脉冲数 `n=round(a/θ)` 用 `s[t]=round(t·n/T)−round((t−1)·n/T)` 分配到 T 步，保证 `Σs[t]=n` 且**条件方差 0、无 RNG**，使「时间误差扩散」不再引入随机噪声，理论恒等式与仿真严格对应；
- **为何跨骨干成立**：视觉侧把 ViG 的 KNN 图**冻结**并把 max-relative 聚合**线性化**（去掉 max 非线性与动态图），图侧用 GCN 消息传递 —— 二者都落成「固定、非负、线性 `A`」，因此同一恒等式、同一偏置、同一解码、同一 `s[t]` 协议可统一横评 conversion loss。

**非显然交互（不是工程拼装）**：`A` 的线性/固定性 ←→ 精确误差恒等式 ←→ 确定性零方差时间扩散，三者互相约束：若 `A` 非线性或动态，恒等式失效；若时间扩散有随机性，恒等式的数值残差不再闭合。这正是「算子无关性」与「确定性化」必须绑定、且原版 ViG 必须作为失效边界的原因。

**机制字段（`problem-method-blueprint.md` 模板）**：
- Input / output：ANN teacher（冻结权重、含 `A`）→ 同结构 SNN，在 T 步内输出分类 logits。
- Key representation：层间传播 = 固定非负线性矩阵 `A`；脉冲序列由 `s[t]` 确定性调度；解码为膜电位累加。
- Main operation：`β*=θ/(2T)` 偏置校准 → `s[t]` 两阶段脉冲分配 → `A` 线性聚合 → 膜电位累加解码。
- Inference objective：最小化 `conversion loss = ANN teacher top-1 − SNN top-1`（pp，越低越好），保持 `Σs[t]=n`、条件方差 0、理论-仿真恒等式残差 → 0。
- Assumptions / Failure modes / Rejected alternatives：见 §1.4 / §1.5。

### 1.4 assumptions（前置假设，逐条可被 G6/G7 检验）
1. `A` **固定**（不随输入 / 时间步变化）、**非负**、**线性**；行随机性**不要求**（这是与既有逐层归一化路线的差异点）。
2. ANN teacher 权重冻结，转换是 training-free 的推理时过程（不引入大规模微调）。
3. 阈值 `θ` 可由层激活统计预注册确定，`β*=θ/(2T)` 闭式成立。
4. ViG 的 KNN 图在转换前冻结、max-relative 聚合被线性聚合替代；原版动态图 + max 非线性仅作**失效边界对照**。
5. 图侧为 GCN 式消息传递，可写成同一个 `A`。
6. 低时步区间 `T∈{1,2,4,8,16}`，主结论聚焦 `T≤4`。

### 1.5 falsification condition（可证伪）
- **C1 崩塌**：在冻结线性 `A` 上，理论-仿真恒等式残差超数值容差，或残差随 T 系统性漂移 → 精确恒等式不成立。
- **C5 反向崩塌（最关键）**：原版 ViG（max 非线性 + 动态 KNN）**竟然也**满足恒等式 → 说明「线性/固定」不是必要条件，`A` 抽象的理论定位失去意义。
- **C3 崩塌**：`s[t]` 在相同 `n,θ` 下出现 `Σs[t]≠n` 或条件方差 >0 → 确定性零方差主张失效。
- **C4 崩塌**：同一 `A` 协议下图侧无法复现进入 ANN−1.5pp 带（内部校准目标，非公开证据）→ 跨骨干通用性不成立。
- **C2 崩塌**：相对最强可行域基线，T≤4 的 conversion loss 未降低（配对检验后方向为正）→ 降损主张失效。

### 1.6 contribution type（诚实分类，只取 top 2）
| 排序 | 类型（`problem-method-blueprint.md`） | 对应 | 说明 |
| --- | --- | --- | --- |
| 主 | **New synthesis that resolves a known tension / New theoretical result** | 真空白① | 固定线性算子上「层类型无关」的精确统一（C1）。把被逐层绑定的误差分析统一到 `A` |
| 次 | **New evaluation / protocol（新协议 / 横评）** | 真空白③ | ViG 首次脉冲化 + 同一算子跨视觉骨干与图消息传递统一 conversion loss 横评（C4） |
| 补充 | **New mechanism specialization（机制特化，非新框架）** | 真空白② | TPP 第二相的特定确定性化（零条件方差、无 RNG），明确**不主张发明两阶段框架本身** |

**明确不主张**：不声称发明 `β*=θ/(2T)`（Deng&Gu ICLR'21）、零期望误差偏置（QCFS ICLR'22 / FTBC ECCV'24）、膜电位解码 + 精确误差等式（Dual-Phase TNNLS'24）、确定性精确计数（PASCAL TMLR'25）、两阶段（TPP ICML'25 / SpikeConverter AAAI'22）、跨 CNN+GCN（One-Spike SNN TETC'24/25）；不声称精度 SOTA、能耗实测、生物保真。

### 1.7 known feasibility risks
| 风险 | 标签 | 依据 / 处置 |
| --- | --- | --- |
| **硬风险**：原版 ViG max-relative 含 max 非线性 + KNN 动态图，破坏线性/固定算子假设 | `design-fixable`（已内建对策） | 必须冻结图 + 线性化；把原版 ViG 作为 **C5 失效边界诊断实验**，而非主结果 |
| 数学组件几乎被占满，novelty 仅剩三处真空白 | `writing-fixable` | G4 `pass-with-narrowing`；主张不得越界 |
| 视觉侧 0 正式实验 | `requires-new-result` | G6 prototype → G7 执行前不得填任何结果数值 |
| 官方强基线数值多在 ImageNet，而 G2 排除 ImageNet 自跑 | `evidence-fixable` | 阈值以 G7 在可得数据上同协议复现值为锚 |
| `torchvision` 缺失、GCN 实现来源待确认 | `design-fixable` | G6 blocker |
| CIFAR 无官方 val split、CIFAR10-DVS 无官方 split | `design-fixable` | G0 预注册切分，test 最终一次 |

### 1.8 与三处真空白 / C1–C5 的对应
- 真空白①「固定线性算子的层类型无关精确统一」→ C1（理论 + 数值残差）。
- 真空白②「TPP 第二相的特定确定性化（零条件方差、无 RNG）」→ C3。
- 真空白③「首次 ViG 脉冲化 + 同一算子跨视觉骨干与图消息传递统一协议横评」→ C4。
- 相对强基线降损 → C2；原版 ViG 失效边界 → C5。

## 2. 对照卡 A：纯标准 CNN 横评

| 字段 | 内容 |
| --- | --- |
| bottleneck | 标准 CNN（VGG / ResNet）低时步 conversion loss 已有大量结果，但缺统一算子视角与公平的低 T 对齐协议 |
| causal / algorithmic mechanism | 在固定 CNN 骨干上，按同一 T 网格复现 QCFS / FTBC / TPP / Parallel Conversion / DCGS / AdaFire，横向列表对比 conversion loss；不改变算子、不引入图侧 |
| assumptions | 标准 CNN 层可视为固定算子；各基线官方实现可复现；同一 seed / split / 统计协议 |
| falsification condition | 横评不产生任何新的机制洞察，或各方法在统一协议下差异不显著、无法支撑「统一算子」主张 |
| contribution type | **New empirical finding / benchmark**（偏 `empirical finding`，且属 crowded） |
| known feasibility risks | One-Spike SNN TETC'24/25 已覆盖「跨 CNN+GCN」；纯 CNN 横评与 must-rerun 基线复现劳动高度重叠；不产生层类型无关理论；CIFAR 无官方 val split 须预注册 |
| **为何不取为主攻** | 属 `covered central claim`（`search-and-scoring.md`）：问题、证据路径已被强基线覆盖，且不触及三处真空白中的任何一处。纯工程横评无法支撑 C1 的「层类型无关精确统一」，也不能作为论文的中心贡献。**保留价值**：作为 C2 的简单基线来源、must-rerun 复现校验与 sanity check，但降为支撑实验，不设独立主 claim |

## 3. 对照卡 B：纯事件视觉时序

| 字段 | 内容 |
| --- | --- |
| bottleneck | 事件相机（DVS）流式输入下的低延迟 SNN 推理，时序编码与脉冲稀疏性耦合 |
| causal / algorithmic mechanism | 在 CIFAR10-DVS 上做帧/事件聚合与时序脉冲编码，评估不同时间窗下的精度-延迟权衡 |
| assumptions | 事件流可分帧且分帧方式不引入不可控混杂；时序编码增益可与算子效应解耦 |
| falsification condition | 时序编码引入的增益无法与「固定线性算子 `A`」的作用分离，导致 C1 精确恒等式不可辨识 |
| contribution type | **New setting / empirical finding**（不同 setting） |
| known feasibility risks | CIFAR10-DVS **无官方 split**（社区 9000/1000）、体积 8,384,752,624 B；时序变量混淆 `A` 的作用；偏离「固定线性算子」核心；与 ViG 冻结图线性化失效边界无关；G2 中 DVS128 Gesture 需登录、N-MNIST 条件性待补证 |
| **为何不取为主攻** | 引入时序编码这一额外自由度，会把 `A` 的线性/固定效应与时序分帧效应混杂，使 C1 的精确恒等式**不可辨识**；核心主张被稀释到另一个 setting，且与三处真空白、ViG 失效边界均无对应。**保留价值**：可作 C4 的外部效度 / 稳健性补充，但须在 C1–C5 主证据锁定之后，且不设独立主 claim |

## 4. 汇总对比

| 维度 | 主卡 OAC | 对照 A 纯 CNN 横评 | 对照 B 纯事件时序 |
| --- | --- | --- | --- |
| 中心问题 | 层类型无关的精确统一 + 统一横评协议 | 已知方法横向对比 | 不同输入模态的时序编码 |
| 触及三处真空白 | ① + ② + ③ 全部 | 无 | 无 |
| 中心贡献类型 | theory/synthesis + protocol | empirical finding（crowded） | setting / empirical finding |
| 可证伪性 | 强（恒等式残差、失效边界、零方差） | 弱（差异不显著即无结论） | 弱（混杂不可解耦） |
| 与硬风险（ViG）关系 | 直接处理并诊断 | 无关 | 无关 |
| 定位 | **主攻** | 支撑 / sanity | 外部效度补充 |

## 5. Coherence filter（`problem-method-blueprint.md`）
- 问题设定与假设兼容：主卡要求 `A` 固定线性 → 与「冻结 ViG 图 + 线性化聚合」「GCN 消息传递」一致；原版 ViG 的不兼容被显式隔离到 C5 边界，**不进入主协议**。
- 证据可检验中心主张：C1 用残差、C3 用方差/计数、C4 用跨骨干 conversion loss、C5 用失效边界，均可测。
- 贡献类型与证据类型匹配：理论主张配理论+数值残差，协议主张配统一横评，机制特化配零方差消融。
- 无互斥假设：未同时声称「training-free」与「大规模微调」；未同时声称「固定算子」与「动态图主结果」。
- 内部先验（图节点分类 T≤8 达 ANN−1.5pp 带内）仅作 C4 的内部校准锚，**绝不当公开证据**；视觉侧 0 正式实验。

## 6. Checkist status（standard）
```
Target venue / stage: 标为 family + must-know 待确认，未假定具体会议
Raw idea normalized: bottleneck / gap / insight / method / evidence / limitation 已写
Missing inputs named: venue、ccfa.yaml、torchvision、GCN 实现来源、视觉侧实测
Novelty: 按 G4 pass-with-narrowing 处理，未把未检索 novelty 当 novelty
Mechanism explained: 是（§1.3 含非显然交互）
Innovation type: 已分类并只取 top 2，附「明确不主张」清单
Experiment plan: 见 claim-evidence-matrix.md / strong-result-feasibility-contract.md（本卡不重复）
Reviewer risks: 已按 writing/design/evidence/requires-new-result/venue-mismatch 分级
Variants coherence: 3 卡无互斥假设、无主题漂移
Weakness vs potential: 对照卡标为「支撑/补充」而非「否定」
Handoff: 本卡只到 idea plan，未越界写论文散文
```
