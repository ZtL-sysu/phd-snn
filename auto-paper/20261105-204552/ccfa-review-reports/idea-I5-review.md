---
idea_id: I5
overall: 3.3
confidence: 0.83
verdict: NO-GO
scores: {novelty: 2, mechanism: 2, evidence_plan: 3, baselines: 3, cvpr_fit: 3, executability_11d: 1}
fatal_risks: ["新颖性坍塌：JEPA-on-connectome / P4 已占连接组脉冲 + 自监督表征，相对 arXiv:2610.10023 仅加蒸馏/换训练法，落入去重日志的 incremental 判定", "核心机制未定义：teacher patch 相似度矩阵到生物图邻接的对齐无实现定义，且三条可证伪消融无法干净分离结构与蒸馏贡献", "11 天不可行：卡片自陈极低，触犯执行契约的冒烟预算上限与本机 torch/PyG 兼容性红线"]
go_conditions: ["用实测证明与 JEPA-on-connectome 的主张正交且带来非平凡的 CV 增益，而非换 teacher 来源", "给出 patch 关系矩阵到连接组邻接的可实现映射并把析因补全为 2×2 完整设计", "重定位为能效/时序任务并补齐硬指标、视觉证据与 SNN 蒸馏近期强基线", "放弃 11-16 主会全文窗口，改投后续轮次；当前窗口内以上均不可达，故维持 NO-GO"]
review_execution: independent-agent
---

# Mode

- Review mode: `scientific`（`ccf-paper-reviewer` 标准科学评审，顶会主会级，非 writing/full 模式）。
- Review execution: `independent-agent`——未参考任何其他 agent 的评审结论，独立依据冻结输入判定。
- 输入性质：**idea 卡片，不是论文，没有任何实验结果**。因此 evidence 维度评的是「证据计划的可行性与完整性」，不是已观测结果；本报告不把任何计划、预测或外推写成已观测结论，不编造实验结果、数值或引用。
- 评审对象：I5 — Structure-Aware Spike Distillation（*Distilling Vision Foundation Models into Connectome-Constrained Spiking Graphs*）。
- 隐私边界：冻结输入视为私有用户数据；本报告仅引用输入内已核验的公开来源与任务明确给出的 URL，不做扩展公开检索。

# Venue and assumptions

- 目标：CVPR 2027 **主会**（顶会/CVPR-ICCV-ECCV 家族），按 `venue-review-styles.md` 的 CVPR 权重评审：novelty、technical quality、empirical validation、visual evidence、clarity、fair comparison；要求强近期基线、消融、跨数据集、鲁棒性、公平协议，figures/qualitative/failure cases 作为证据而非装饰。**不用期刊 Q2 标准放水**。
- 时间线（`execution-contract-v1.md` 第 4 节，源 https://cvpr.thecvf.com/Conferences/2027/CallForPapers 访问 2026-11-05）：Paper Registration 2026-11-10 AOE、Submission 2026-11-16 AOE、Supplementary 2026-11-23；当前 2026-11-05，**仅剩 11 天**。
- CFP 主题：Datasets and Benchmarks / Efficient and scalable vision / AI for Science；大方向锁定 GNN + SNN + 果蝇连接组 + 视觉，不得漂到纯神经科学仿真或纯图表示学习。
- Contemporaneous 规则（`prior-art-dedup-log.md` 第 16-21 行、`execution-contract-v1.md` 第 40-41 行）：2026-09-15 之后上线论文须引用讨论，高度相似加审；arXiv:2610.10023（2026-10-08）落入此窗口。
- 硬件/运行信封（`hardware-profile.md`、`execution-contract-v1.md` 第 5 节）：RTX 3060 12 GB、31.9 GB RAM 级、`dyg-cold`（torch 2.11+cu128 / PyG 2.8.0.post1 / spikingjelly）；冒烟预算单次 ≤15 分钟 GPU、显存 ≤10 GB、下载 ≤1.5 GB、不做完整训练/多种子大实验；**禁止伪造实验结果或把预测写成观测**（契约第 2 节）。
- 竞争工作：`train-your-fly` / arXiv:2610.10023（https://arxiv.org/abs/2610.10023，无状态 GNN 视觉分类 + 4 种随机图等布线预算对照，代码数据全公开，含 `benchmark_speed.py` 与 sweep）；arXiv:2609.01330（NeurIPS 2025，连接组+脉冲+朝向图仿真）；Nature 2024 flyvis；BrainTrace / BioReservoir / **JEPA-on-connectome**（连接组脉冲 + 自监督/预测表征）。
- 特别假设（任务强制）：I5 必须严格判断 JEPA-on-connectome 已探索「连接组脉冲 + 自监督/预测表征」之后的新颖性剩余空间。所有 idea 必须回答：相对 arXiv:2610.10023 的增量是否足以撑起 CVPR 主会。

# Paper summary

- 一段概述：I5 主张把视觉基础模型（DINOv2/CLIP）的 patch 相似度矩阵当作 teacher，对「连接组约束的 LIF-GNN 学生」做关系蒸馏，令 teacher 提供语义、生物图提供稀疏结构，二者共同缓解脉冲训练不稳定；学生在 CIFAR-10/100 与 cogstim 三任务上以 accuracy、收敛步数、spike rate 评测。
- Claimed problem（`idea-cards.md` I5 行 139）：「大规模 SNN 难训练（梯度消失、脉冲稀疏）；连接组提供的是**有语义的稀疏骨架**而非随机稀疏」。
- Claimed gap（行 140）：「若把 teacher 的 patch 关系对齐到生物图邻接，就能给 SNN 一个结构监督信号」；G4 定位（行 148）称 P1 无蒸馏、P2 无可训练 CV 任务。
- Method / contribution map（行 141-145）：机制 = DINOv2/CLIP patch 关系蒸馏 + 连接组约束 LIF-GNN；贡献类型 = 「训练方法 + 结构蒸馏」。
- Evidence package（计划，非结果）：3 条可证伪消融（随机图+同蒸馏 / 生物图+无蒸馏 / teacher 换随机矩阵，行 143-144）、强基线清单（行 147）、指标（行 146）、最小冒烟（小图上一次 teacher-student 关系损失前向+反传，确认显存与收敛，行 150）。**无任何已观测实验数据**。
- Stated limitations（行 148-153，卡片自陈）：「JEPA-on-connectome（2026 工作论文）已探索『连接组脉冲 + 自监督表征』，P4 令本 idea 的新颖性变薄」；「强烈『A+B 拼盘』感；引入 teacher 后『结构是否有用』更难干净归因；需要额外大模型推理成本；11 天不可行」；「11 天可投性：极低」。

# Likely stance and calibrated score

- Expected outcome / Likely stance: **NO-GO**（calibration-and-rank.md 的「clear reject」带：fatal 新颖性 + 机制 + 可行性三重问题，overall 通常 1-3；本例取带内偏高 3.3 以承认其写了可证伪消融与强基线清单）。
- Overall: **3.3 / 10**；Confidence: **0.83**（判断所依赖的去重日志、文献矩阵、卡片自陈风险均可核验，故置信度高；不因「无实验结果」而自动压低，因新颖性/机制判断不依赖实验观测）。
- Main accept signal: 明写了 3 条可证伪消融、`train-your-fly` must-rerun 与 ANN teacher 上界基线（行 143-147），比纯叙事 idea 更可检验；方向落在 CFP「AI for Science」主题内。
- Main reject signal: JEPA-on-connectome / P4 已占据核心主张（行 148-149、`prior-art-dedup-log.md` 行 14），teacher→连接组邻接的核心对齐未定义（行 140-141），卡片自陈 11 天不可行（行 152-153）。
- Calibration band: CSPaper 风格相对解释为「bottom / below average」，为近似判断、非官方 cutoff；升到下一带需先解决新颖性坍塌，而这在冻结输入下无证据支持。不声称任何接收概率。

## 相对 arXiv:2610.10023 的增量判定（明确回答）

**结论：不足以撑起 CVPR 主会。** 依据：
1. `train-your-fly`（https://arxiv.org/abs/2610.10023）已是无状态 GNN 视觉分类 + 4 种随机图等布线预算对照，且代码、图数据、刺激生成器、`benchmark_speed.py` 与 sweep 全公开（`literature-baseline-matrix.md` 行 8、任务说明）。I5 相对它的差分 = 换动力学（LIF-GNN）+ 加关系蒸馏（teacher 语义）+ 换训练目标，属于「同一骨架 + 加监督信号/训练技巧」。`prior-art-dedup-log.md` 行 21 明确警告：「如果只做『同一模型 + 换数据集』，仍会被判 incremental」；此处虽非换数据集，但增量性质更接近「加模块」而非新贡献单元。
2. I5 最像新颖性的部分——「把 teacher/自监督语义注入连接组脉冲网络」——恰好撞上 P4 / JEPA-on-connectome（`literature-baseline-matrix.md` 行 22，工作论文 https://louistier.github.io/projects/3_hack_the_worlds；`prior-art-dedup-log.md` 行 14 把「连接组脉冲自监督」列为被堵死的朴素 idea）。DINOv2/CLIP 与 JEPA 的差异只是监督信号来源不同，不是新的贡献单元；SNN 知识蒸馏本身已是成熟方向，增量更薄。按 contemporaneous 规则（`execution-contract-v1.md` 行 40-41），高度相似会受额外审查。
3. CVPR 主会要求 novelty + strong recent baselines + visual evidence + 公平协议（`venue-review-styles.md` 行 60-69）。I5 的指标仅 accuracy / 收敛步数 / spike rate（行 146），无能效、延迟、参数量的硬收益，无定性/失败案例视觉证据，无法证明「生物结构 + 蒸馏」带来 CV 可度量的工程收益。

## 若只有部分正向结果：诚实可发表的下位结论（明确回答）

- 若只观察到「蒸馏让 LIF-GNN 收敛更快/更稳」但「生物图 + 同蒸馏」与「度匹配随机图 + 同蒸馏」的等预算 accuracy 差异落在 95% CI 内（`dataset-access-log.md` 行 35 以 95% CI 为标准口径）：诚实结论只能是「基础模型 patch-relation 蒸馏可在单一小图设置下稳定连接组约束 SNN 的训练」，并**必须同时写明未观察到生物拓扑的独立贡献**。该结论达不到 CVPR 主会，最多是 SNN 专项 venue / workshop 的简短 empirical note，或作为其他论文的训练附录。
- 若「teacher 换随机矩阵」也达到相近收敛步数：则「teacher 提供语义」被证伪，只剩「任意结构化正则都有效」，结论进一步变弱，只能报负结果。
- 诚实下位结论模板（受限、可发表、但明显低于主会）：「在 cogstim 单一任务 + 视叶子图 + T=8 + 有限种子的单一设置下，patch-relation 蒸馏相对无蒸馏 LIF-GNN 缩短收敛步数；但等预算下生物图与度匹配随机图准确率差异的 95% CI 跨 0，故本轮不支持『生物接线提供特权』」。不得外推到 CIFAR-10/100、多数据集、或声称泛化。

# Quantitative scorecard

| Dimension | Score (1-5) | Confidence (1-5) | Evidence basis | Deduction / score-change condition |
|:---|:---:|:---:|:---|:---|
| Novelty | 2 | 5 | I5 行 148-149 自陈「新颖性变薄」；`prior-art-dedup-log.md` 行 14 P4；`literature-baseline-matrix.md` 行 22 | 与 JEPA-on-connectome 高度同构，相对 2610.10023 增量 incremental；详见下方明细 |
| Mechanism | 2 | 5 | I5 行 140-142「把 teacher 的 patch 关系对齐到生物图邻接」；行 151 自陈归因困难 | 核心对齐无实现定义、析因不闭合；详见下方明细 |
| Evidence plan | 3 | 4 | I5 行 143-144 三条消融、行 146-147 指标与基线、行 150 冒烟 | 计划有骨架但暴露核心主张、缺统计与硬指标；详见下方明细 |
| Baselines | 3 | 4 | I5 行 147 强基线清单；`literature-baseline-matrix.md` 行 31 | 缺 SNN 蒸馏近期强基线与等预算协议；详见下方明细 |
| CVPR fit | 3 | 4 | I5 行 145-146 贡献类型与指标；`venue-review-styles.md` 行 60-69 | 训练方法/蒸馏非视觉洞察，无视觉证据与硬效率指标；详见下方明细 |
| Executability (11d) | 1 | 5 | I5 行 152-153「11 天不可行/极低」；`execution-contract-v1.md` 行 51-52；`hardware-profile.md` 行 36-40 | 与 11-16 截止及冒烟预算直接冲突；详见下方明细 |

**Overall:** 3.3 / 10  | **Scholarly Confidence:** 4/5（对应 front matter 0.83）
**Recommendation:** reject  | **Verdict:** NO-GO；多重 fatal，其中新颖性坍塌不可通过修订解决

## 低分维度（≤3）扣分与修复明细（每个含 Deduction / Repair condition / Expected score movement）

```text
Dimension: Novelty
Score: 2
Confidence: 5
Evidence basis: idea-cards.md I5「G4 定位 … JEPA-on-connectome（2026 工作论文）已探索『连接组脉冲 + 自监督表征』，P4 令本 idea 的新颖性变薄」；prior-art-dedup-log.md P4 行 14 把「连接组脉冲自监督」列为被堵死的朴素 idea；literature-baseline-matrix.md 行 22（Wiring the Fly Brain into a World Model）。
Deduction: 核心主张「teacher 语义 + 生物结构共同作用于连接组脉冲网络」与 JEPA-on-connectome 高度同构；相对 https://arxiv.org/abs/2610.10023 只差加蒸馏/换训练法，落入去重日志行 21 的 incremental 判定，且 contemporaneous 相似加审。
Repair condition: 用实测（非计划）证明与 JEPA-on-connectome 的主张正交，并给出非平凡的 CV 增益与新的贡献单元，而非把 teacher 从 JEPA 换成 DINOv2/CLIP。
Expected score movement: 维度 +0.5 to +1（至 3）仅在上述实测成立时可能；overall 最多 +0.3 to +0.6，仍停留 reject 带，不改变 NO-GO。

Dimension: Mechanism
Score: 2
Confidence: 5
Evidence basis: idea-cards.md I5 行 140-141「若把 teacher 的 patch 关系对齐到生物图邻接」「用 DINOv2/CLIP 的 patch 相似度矩阵作为 teacher，对生物图上的消息传递做关系蒸馏」；hardware-profile.md 行 36-37（视叶子图几千至几万节点）；行 151 自陈「引入 teacher 后『结构是否有用』更难干净归因」。
Deduction: DINOv2/CLIP 的 patch token 是稠密图像块关系（约 10^2–10^3 量级），与连接组稀疏有向图节点无天然对应，卡片未给出映射/投影定义——核心步骤不可实现、不可审查；且三条消融缺「随机图 + 无蒸馏」格，无法分离结构 vs 蒸馏贡献（methodology invalid）。
Repair condition: 给出 patch 关系矩阵到连接组邻接的可实现映射定义，并把析因补全为 2×2 完整设计（{生物图, 度匹配随机图} × {有蒸馏, 无蒸馏}）+ 等预算口径。
Expected score movement: 维度 +1 to +1.5（至 3-3.5）若映射可定义且冒烟通过；overall +0.3 to +0.5，仍受新颖性与可行性封顶，不改变 NO-GO。

Dimension: Evidence plan
Score: 3
Confidence: 4
Evidence basis: idea-cards.md I5 行 143-144（三条可证伪消融）、行 146（accuracy/收敛步数/spike rate）、行 150（冒烟仅「确认显存与收敛」）；dataset-access-log.md 行 35（主指标含 95% CI）。
Deduction: 计划列了消融与基线，但 (a) 无多种子/95% CI/统计检验，(b) 无能效/延迟/参数量硬指标，(c) 最小冒烟只验代码能否跑通、完全不触及核心假设（teacher-图对齐、结构贡献），(d) teacher 推理成本未量化；属「计划支撑部分故事但暴露核心主张」。
Repair condition: 补齐多种子 + 95% CI + 显式统计检验；把冒烟改为「对齐可行性探针」；补能效/延迟/参数量硬指标与等预算协议。
Expected score movement: 维度 +0.5 to +1（至 3.5-4）；overall +0.2 to +0.4，不改变 stance。

Dimension: Baselines
Score: 3
Confidence: 4
Evidence basis: idea-cards.md I5 行 147「强基线：train-your-fly、无蒸馏 SNN、随机图蒸馏、ANN teacher 本身（上界）」；literature-baseline-matrix.md 行 31「不可仅与 ANN toy baseline 比较：CVPR 主会评审不会接受」。
Deduction: 在贡献类型为「训练方法 + 结构蒸馏」下，最重要的近期同类基线（SNN knowledge distillation / transformer→SNN 蒸馏）完全未列；ANN teacher 是上界而非同类方法基线；缺等参数量/等预算的公平协议声明。
Repair condition: 补 2-3 个近期 SNN 蒸馏强基线并声明等参数量/等 synaptic-op 预算的公平对比协议。
Expected score movement: 维度 +0.5 to +1（至 3.5-4）；overall +0.2 to +0.3，不改变 stance。

Dimension: CVPR fit
Score: 3
Confidence: 4
Evidence basis: idea-cards.md I5 行 145「贡献类型：训练方法 + 结构蒸馏」、行 146 指标；venue-review-styles.md 行 60-69（CVPR 要求 visual evidence、强近期基线、公平协议、与近期 CV 工作的清晰关系）。
Deduction: 核心贡献是 SNN 训练技巧而非视觉洞察；无定性/失败案例视觉证据，指标无能效/延迟/参数量硬收益；相对 2610.10023（视觉分类 + 等布线预算）的增量不落在 CVPR 主维度上。
Repair condition: 重定位为能效/时序视觉任务，补 accuracy-vs-预算曲线、脉冲/能耗硬指标与定性可视化，并明确与 2610.10023 的差分贡献。
Expected score movement: 维度 +0.5 to +1（至 3.5-4）；overall +0.2 to +0.4，不改变 stance。

Dimension: Executability (11d)
Score: 1
Confidence: 5
Evidence basis: idea-cards.md I5 行 152-153「需要额外大模型推理成本；11 天不可行」「11 天可投性：极低」；execution-contract-v1.md 行 51-52（冒烟单次 ≤15 分钟、不做完整训练/多种子大实验）、行 37-41（11-10 注册 / 11-16 全文）；hardware-profile.md 行 36-37（整图 BPTT 不可能）、行 39-40（官方 pin torch 2.6/PyG 2.6 与本机 2.11/2.8 兼容性未验证、缺 torch_sparse）。
Deduction: 任务面为 CIFAR-10/100 + cogstim 三任务 + 3 消融 + teacher 大模型推理 + must-rerun 基线（行 146-147），与 11 天窗口、冒烟预算封顶、版本兼容性未验证三项同时冲突；卡片自陈极低。
Repair condition: 放弃 11-16 主会全文窗口、改投后续轮次，并先完成官方代码的本机兼容性验证。
Expected score movement: 维度 +1 to +2（至 2-3）仅在时间窗放宽后可能；当前 11 天窗口内 overall 无正向移动，NO-GO 不变。
```

## Score-change conditions

| Change | Condition | Likely affected dimensions | Expected movement |
| --- | --- | --- | --- |
| Raise score | 用实测证明与 JEPA-on-connectome 正交且有非平凡 CV 增益 + 给出对齐可实现定义 + 2×2 完整析因 + 补硬指标与 SNN 蒸馏强基线 | Novelty, Mechanism, Evidence plan, Baselines, CVPR fit | overall +0.5 to +0.8（上限约 4.1，仍 reject 带，不改 NO-GO） |
| Lower score | 冒烟显示 teacher→图对齐不可实现，或随机图+同蒸馏与生物图+同蒸馏无差异被坐实 | Mechanism, Novelty, Evidence plan | overall -0.3 to -0.6（至 2.7-3.0） |
| No quick change | 新颖性坍塌（P4/JEPA 已占核心主张）与 11 天算力/时间窗 | Novelty, Executability (11d) | 当前窗口内不可能修复，NO-GO 稳定 |

# Top strengths

- 写了明确的可证伪消融与强基线清单：`idea-cards.md` I5 行 143-147 含「随机图 + 同蒸馏 / 生物图 + 无蒸馏 / teacher 换成随机矩阵」与 `train-your-fly` must-rerun、ANN teacher 上界。相较纯叙事 idea，这是可检验的骨架，故未给最低分。
- 卡片诚实自陈风险与限制：行 148-153 主动写明「新颖性变薄」「A+B 拼盘」「归因更难」「11 天不可行 / 极低」，降低了过度承诺风险，便于评审定位（`review-output-standards.md` 对 limitation honesty 的正面信号）。
- 共享证据底座可直下：`dataset-access-log.md` 中 cogstim（MIT/pip）、FlyWire 图包、MaleCNS feather 全部 PASS，`hardware-profile.md` 确认 `dyg-cold` 齐备 PyG + spikingjelly + cv2；方向落在 CFP「AI for Science」主题内。以上为真实但有限的优势，不据此夸大新颖性。

# Major-fatal concerns

- **C1 · Severity: fatal · 新颖性坍塌（相对最强竞争工作增量不成立）**
  - Concern: 「teacher/自监督语义注入连接组脉冲网络」这一核心主张已被 JEPA-on-connectome / P4 占据，相对 arXiv:2610.10023 仅「加蒸馏/换训练法」。
  - Evidence basis: `idea-cards.md` I5 行 148-149「JEPA-on-connectome（2026 工作论文）已探索『连接组脉冲 + 自监督表征』，P4 令本 idea 的新颖性变薄」；`prior-art-dedup-log.md` 行 14 P4 把「连接组脉冲自监督」列为被堵死的朴素 idea、允许差异轴仅为「明确的单一定量贡献 + 严格受控对照 + CVPR 可解释的架构/效率结论」；`literature-baseline-matrix.md` 行 22（Wiring the Fly Brain into a World Model，工作论文 https://louistier.github.io/projects/3_hack_the_worlds）；https://arxiv.org/abs/2610.10023；`execution-contract-v1.md` 行 40-41（contemporaneous 高度相似加审）。
  - Reviewer deduction: 换 teacher（DINOv2/CLIP vs JEPA）不是新贡献单元；SNN 蒸馏成熟，剩余新颖性极薄，触发 `universal-review-rubric.md` 的 fatal-risk triage「novelty claim collapses under close prior work」。
  - Required fix: 用实测证明与 JEPA-on-connectome 主张正交并给出新的贡献单元与硬收益；当前 11 天窗口不可达。
- **C2 · Severity: fatal · 核心机制（teacher→图对齐）未定义，方法不可审查**
  - Concern: patch 相似度矩阵到生物图邻接的「对齐」没有任何实现定义，且节点空间无天然对应。
  - Evidence basis: `idea-cards.md` I5 行 140-141「若把 teacher 的 patch 关系对齐到生物图邻接」「用 DINOv2/CLIP 的 patch 相似度矩阵作为 teacher，对生物图上的消息传递做关系蒸馏」；`hardware-profile.md` 行 36-37（视叶子图几千至几万节点、T=8~16、小 batch）。
  - Reviewer deduction: 稠密 patch-pair 关系（约 10^2–10^3 patch）与稀疏有向连接组图之间缺映射/投影/聚合定义，中心机制不可实现、无法复现，属 methodology invalid（rubric 第 3 维 2/5 及以下）。
  - Required fix: 给出可实现、可复现的映射定义，并在冒烟中验证其非平凡性。
- **C3 · Severity: fatal · 归因混淆，可证伪消融不闭合**
  - Concern: 三条消融无法干净分离「结构」与「蒸馏」贡献，且「随机图 + 同蒸馏」因 C2 不可执行。
  - Evidence basis: `idea-cards.md` I5 行 143-144「随机图 + 同蒸馏 / 生物图 + 无蒸馏 / teacher 换成随机矩阵」、行 151 自陈「引入 teacher 后『结构是否有用』更难干净归因」。
  - Reviewer deduction: 缺「随机图 + 无蒸馏」格，无法构成 2×2 析因；随机图无生物语义邻接则 teacher 关系无对齐目标，C1/C2/C3 互相锁死，中心机制主张不可证。
  - Required fix: 重设计为 2×2 完整析因 + 度分布匹配随机图 + 等预算口径 + 多种子与 95% CI。
- **C4 · Severity: fatal · 11 天与本机算力不可行**
  - Concern: 任务面与大模型推理成本、冒烟预算封顶、版本兼容性红线同时冲突。
  - Evidence basis: `idea-cards.md` I5 行 146-147（CIFAR-10/100 + cogstim 三任务 + 3 消融 + must-rerun）、行 152-153「需要额外大模型推理成本；11 天不可行 / 极低」；`execution-contract-v1.md` 行 51-52（单次 ≤15 分钟、不做完整训练/多种子大实验）、行 37-41（11-10 注册 / 11-16 全文）；`hardware-profile.md` 行 39-40（官方 pin torch 2.6/PyG 2.6 与本机 2.11/2.8 需兼容性验证、缺 torch_sparse）；`literature-baseline-matrix.md` 行 8。
  - Reviewer deduction: 与 deadline 及本机可复现性直接冲突，证据计划在窗口内无法兑现（evidence 维度评可行性）。
  - Required fix: 改投后续轮次；先完成官方代码本机兼容性验证。
- **C5 · Severity: major · CVPR 主会 fit 与指标/视觉证据缺口**
  - Concern: 贡献是训练方法/蒸馏而非视觉洞察，指标无能效/延迟/参数量硬收益，无定性/失败案例视觉证据。
  - Evidence basis: `idea-cards.md` I5 行 145-146（贡献类型、指标仅 accuracy/收敛步数/spike rate）；`venue-review-styles.md` 行 60-69（CVPR 把 figures/qualitative/failure cases 作为证据、要求强近期基线与公平协议）。
  - Reviewer deduction: 「生物结构 + 蒸馏」无法转化为 CV 可度量的工程收益，主会相关度弱。
  - Required fix: 重定位能效/时序任务并补硬指标与可视化。
- **C6 · Severity: major · 强基线定位缺口**
  - Concern: 贡献类型为「训练方法 + 结构蒸馏」，却未列近期 SNN 蒸馏同类强基线。
  - Evidence basis: `idea-cards.md` I5 行 147（基线清单）；`literature-baseline-matrix.md` 行 31「不可仅与 ANN toy baseline 比较：CVPR 主会评审不会接受」。
  - Reviewer deduction: 公平对比不足以支撑「训练方法」类主张；ANN teacher 是上界而非同类基线。
  - Required fix: 补 2-3 个近期 SNN 蒸馏强基线与等预算/等参数量协议。

# Writing and presentation concerns

- 「有语义的稀疏骨架」（`idea-cards.md` I5 行 139）中「语义」未定义——指细胞类型/递质符号，还是 teacher patch 关系？术语不稳定，转成论文后必被追问（`review-output-standards.md` 输出质量门第 6 点）。
- 「teacher 提供语义，生物图提供稀疏结构，二者共同缓解脉冲训练不稳定」（行 142）把两因子写成并列协同，但无交互项检验设计（呼应 C3），claim-evidence 呈现强于证据计划；`universal-review-rubric.md` 的 hard rule 要求 unsupported claims 弱化或补证据，不得靠修辞强化。
- 标题 *Distilling Vision Foundation Models into Connectome-Constrained Spiking Graphs* 堆叠三个名词，读者无法判断差分贡献是蒸馏、结构还是 SNN，contribution display 不清。
- 行 148-149 出现非中文混入（「P4 ทำให้本 idea…」），属轻微语言一致性瑕疵，提示未来论文需统一术语与语言。
- 边界说明：以上是 **idea 卡片** 表述，不是已存在论文的章节；本节评的是「若照此写成论文会暴露的呈现风险」，未把卡片当论文文本评审，也未生成任何论文文本。

# Format-venue concerns

- CVPR 主维度含 visual evidence 与 fair comparison（`venue-review-styles.md` 行 60-69）：I5 指标包无定性示例、失败案例、跨数据集可视化，且强基线缺同类近期方法（C6）。
- Contemporaneous 引用义务：arXiv:2610.10023（2026-10-08，https://arxiv.org/abs/2610.10023）与 JEPA-on-connectome（2026 工作论文）均须诚实引用讨论，不能当作不存在（`execution-contract-v1.md` 行 40-41）。
- 时间线：注册 11-10、全文 11-16 AOE、supp 11-23（`execution-contract-v1.md` 行 37-38）；11 天内补实验/补基线/补兼容性验证均不现实。
- Desk-reject 风险：中。主题未偏出 CV，但若把「训练技巧 + 连接组」处理成纯 SNN 方法论文，易被判与 CV 主会相关度弱或 incremental；`desk-checks.md` 的 topic compatibility / minimum quality 项为 uncertain（无实验、无完整方法定义）。
- 不写 rebuttal、不修改 idea、不生成论文文本（任务硬性约束与 `ccf-paper-reviewer` Core Rule）。

# Multi-reviewer panel

```text
Reviewer: SNN 训练专家
Lens: LIF/ALIF BPTT、surrogate gradient、脉冲训练稳定性、12GB 显存与版本兼容性
Score tendency: reject（约 3/10）
Confidence: 0.75
Main positive signal: 明确把「大规模 SNN 难训练（梯度消失、脉冲稀疏）」作为痛点，并列了「无蒸馏 SNN」对照（idea-cards.md I5 行 139、147）。
Main negative signal: teacher→连接组邻接对齐未定义（行 140-141），ALIF/LIF BPTT 显存与官方/本机 torch-PyG 兼容性未经实测（hardware-profile.md 行 36-40），行 152-153 自陈 11 天不可行。
Evidence basis: idea-cards.md I5 行 139-142、150-153；hardware-profile.md 行 36-40；execution-contract-v1.md 行 51-52。
Score-change condition: 若给出对齐可实现定义且小图冒烟在 ≤10GB / ≤15 分钟内跑通，training-feasibility 维度小幅上调；但新颖性与窗口约束仍封顶，overall 不改变 NO-GO。

Reviewer: benchmark / 评测专家
Lens: 消融闭合性、归因、多种子/95% CI、公平协议
Score tendency: reject（约 3/10）
Confidence: 0.80
Main positive signal: 写了 3 条可证伪消融与「teacher 换成随机矩阵」对照（idea-cards.md I5 行 143-144），比无消融的 idea 可检验。
Main negative signal: 缺「随机图 + 无蒸馏」格、因子混淆、行 151 自陈归因困难、无多种子/95% CI（dataset-access-log.md 行 35 以 95% CI 为标准口径）；最小冒烟（行 150）只验显存与收敛，不验核心假设。
Evidence basis: idea-cards.md I5 行 143-144、146、150-151；dataset-access-log.md 行 35。
Score-change condition: 重设计为 2×2 完整析因 + 等预算 + 多种子/95% CI，并把冒烟改为对齐可行性探针 → 证据计划维度上调至 3.5-4；不改变新颖性判定。

Reviewer: CV 顶会架构 / venue-fit 专家
Lens: CVPR 主会 bar、Datasets/Efficient/AI-for-Science 主题、视觉证据、强近期基线
Score tendency: reject（约 3/10）
Confidence: 0.80
Main positive signal: 任务落在视觉分类且共享底座数据可直下（dataset-access-log.md 全 PASS），方向属 CFP「AI for Science」范畴。
Main negative signal: 核心贡献是训练方法/蒸馏而非视觉洞察；指标（行 146）无能效/延迟/参数量硬收益、无定性/失败案例；相对 https://arxiv.org/abs/2610.10023 增量落在 prior-art-dedup-log.md 行 21 的 incremental 判定；缺 SNN 蒸馏近期强基线（literature-baseline-matrix.md 行 31）。
Evidence basis: idea-cards.md I5 行 145-147；venue-review-styles.md 行 60-69；prior-art-dedup-log.md 行 21；literature-baseline-matrix.md 行 31。
Score-change condition: 重定位能效/时序任务、补硬指标与视觉证据、补同类强基线 → fit 维度上调至 3.5-4；仍受新颖性封顶。

Reviewer: novelty / positioning 专家
Lens: 相对 arXiv:2610.10023 与 contemporaneous 工作的增量、是否 incremental
Score tendency: strong reject（约 2/10）
Confidence: 0.85
Main positive signal: 卡片诚实自陈「新颖性变薄」（行 148-149）并列 must-rerun 基线（行 147），定位诚实。
Main negative signal: JEPA-on-connectome / P4 已占「连接组脉冲 + 自监督/预测表征」（prior-art-dedup-log.md 行 14；literature-baseline-matrix.md 行 22），SNN 蒸馏成熟，contemporaneous 高度相似加审（execution-contract-v1.md 行 40-41），相对 https://arxiv.org/abs/2610.10023 仅加蒸馏/换训练法。
Evidence basis: idea-cards.md I5 行 148-149；prior-art-dedup-log.md 行 14、18-21；literature-baseline-matrix.md 行 22；https://arxiv.org/abs/2610.10023。
Score-change condition: 需实测证明与 JEPA-on-connectome 主张正交且有非平凡 CV 增益——当前 11 天窗口与冻结输入下不可达。

Panel synthesis:
Agreement: 四位评审一致认为「新颖性剩余空间极薄 + 核心机制 teacher→图对齐未定义 + 11 天不可行」，且一致判定相对 arXiv:2610.10023 的增量属 incremental；无人给出 accept 信号。一致结论由同一组证据（行 140-153、去重日志行 14/21、文献矩阵行 22）独立得出，非强行统一。
Disagreement: 无实质立场分歧；唯一差异是 SNN 训练专家认为「若对齐定义清楚、冒烟跑通，训练方法本身有工程价值」（给 3 而非 2），novelty 专家认为即便如此新颖性仍坍塌（给 2）——这是 lens 权重差异，不是人为制造的分歧。评测与 venue 专家都指向「归因混淆 / 指标缺口」同一处证据（行 143-151）。
Decisive accept axis: 理论上需「证明与 JEPA-on-connectome 正交 + 对齐可实现定义 + 非平凡 CV 增益 + 补齐硬指标与强基线」；在 11 天窗口与冻结输入下不可达，不构成现实 accept 路径。
Decisive reject axis: JEPA-on-connectome / P4 占据核心主张（prior-art-dedup-log.md 行 14）+ teacher→图对齐未定义（行 140-141）+ 11 天不可行（行 152-153）——任一即足以 reject，三者叠加为 clear reject。
Unresolved evidence: 无任何实验结果；JEPA-on-connectome 为未同行评审工作论文、直链细节未核验；teacher patch→连接组邻接映射无实现；DINOv2/CLIP 推理成本未量化；官方 torch 2.6/PyG 2.6 与本机 2.11/2.8 兼容性未验证。
Final calibrated stance: NO-GO（overall 3.3, confidence 0.83）；多重 fatal，其中新颖性坍塌不可通过修订解决；合成遵循「最强未解决关注点决定最终立场」，未把致命缺陷平均掉。
```

# Concern-to-action table

| ID | Severity | Concern | Evidence basis | Affected criterion | Fix class | Required action | Owner skill | Score-change condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | fatal | 新颖性坍塌，与 JEPA-on-connectome / P4 高度同构，相对 2610.10023 增量 incremental | idea-cards.md I5 行 148-149；prior-art-dedup-log.md 行 14、21；literature-baseline-matrix.md 行 22；https://arxiv.org/abs/2610.10023 | Novelty / Positioning | related-work | 用实测证明主张正交并给出新贡献单元与硬收益；当前窗口不可达 | ccf-paper-writer | 仅在该实测成立时 novelty +0.5~+1、overall +0.3~+0.6，仍不改 NO-GO |
| C2 | fatal | teacher patch 相似度矩阵到生物图邻接的对齐无实现定义 | idea-cards.md I5 行 140-141；hardware-profile.md 行 36-37 | Mechanism / Soundness | method/soundness | 给出可实现、可复现的映射定义并在冒烟验证非平凡性 | ccf-paper-writer | 映射可定义且冒烟通过时 mechanism +1~+1.5、overall +0.3~+0.5 |
| C3 | fatal | 三条消融不闭合，无法分离结构与蒸馏贡献 | idea-cards.md I5 行 143-144、151 | Evidence plan / Soundness | experiment | 重设计 2×2 完整析因 + 度匹配随机图 + 等预算 + 多种子与 95% CI | f-research-v1 | 析因闭合时 evidence_plan +0.5~+1 |
| C4 | fatal | 11 天与本机算力/兼容性不可行 | idea-cards.md I5 行 146-147、152-153；execution-contract-v1.md 行 37-41、51-52；hardware-profile.md 行 39-40 | Executability (11d) | reproducibility | 改投后续轮次；先做官方代码本机兼容性验证 | f-research-v1 | 仅时间窗放宽后 executability +1~+2，当前窗口 overall 无正向移动 |
| C5 | major | CVPR fit 弱：训练技巧而非视觉洞察，无能效/延迟硬指标与视觉证据 | idea-cards.md I5 行 145-146；venue-review-styles.md 行 60-69 | CVPR fit / Evidence | venue-mismatch | 重定位能效/时序任务并补硬指标与定性可视化 | ccf-paper-writer | 补齐后 cvpr_fit +0.5~+1 |
| C6 | major | 缺近期 SNN 蒸馏同类强基线与等预算协议 | idea-cards.md I5 行 147；literature-baseline-matrix.md 行 31 | Baselines | experiment | 补 2-3 个近期 SNN 蒸馏强基线并声明等参数量/等 synaptic-op 协议 | f-research-v1 | 补齐后 baselines +0.5~+1 |

# Recommended next CCFA owner

- 下一责任方：`ccf-paper-writer`（仅在未来轮次对「重定位后的新 idea」做贡献定位与 claim-evidence 收紧）与 `f-research-v1`（兼容性验证、2×2 析因与等预算协议设计）。**本轮不交接为可写论文状态**：C1/C2/C3/C4 均为 fatal 且新颖性不可修。
- 不写 rebuttal（交 `ccf-rebuttal-writer` 的前提不成立）；不修改 idea 卡片；不生成论文文本。
- Handoff: PARTIAL（`ccf-paper-reviewer` SKILL.md 默认），结论为淘汰该 idea，返回 idea-screening 循环另选候选（任务说明的原流程：不理想就换 idea）。

## Minimum smoke-test decision（GO / NO-GO + 可证伪失败信号）

- 该 idea 的最小冒烟实验（「小图上做一次 teacher-student 关系损失前向 + 反传，确认显存与收敛」，idea-cards.md I5 行 150）：**NO-GO，不值得为「冲 CVPR 主会」跑**。
- 理由：该冒烟只验证「代码能跑通 / 显存够 / loss 下降」，完全不触及三个致命风险（C1 新颖性坍塌、C2 teacher→图对齐的语义鸿沟、C3 归因混淆）；即使跑通也不会改变 NO-GO 判定，属于决策无关动作。且 DINOv2/CLIP teacher 推理 + 关系损失在 `execution-contract-v1.md` 行 51-52 的「单次 ≤15 分钟 / ≤10GB」预算内能否跑通本身未经核验。
- 一个可证伪的失败信号（若日后重定位后真要跑）：在「teacher patch 相似度矩阵 → 生物图邻接」对齐下，把生物图替换为度分布匹配随机图、保持同一蒸馏目标与等预算，若两者 test accuracy 差异的 95% CI 跨 0（即无显著结构贡献），则「有语义的稀疏骨架」假设被证伪——这正是卡片行 143-144 第一条可证伪消融的具体化，且是可测判定而非泛泛「需要更多实验」。

# Checks run

- 已读：`ccf-paper-reviewer/SKILL.md`（经 Skill 加载）、`ccf-common/references/review-output-standards.md`、`references/universal-review-rubric.md`、`calibration-and-rank.md`、`reviewer-panel.md`、`venue-review-styles.md`、`review-workflow.md`、`fixed-output-format.md`、`desk-checks.md`；以及 6 个冻结输入（idea-cards.md、prior-art-dedup-log.md、literature-baseline-matrix.md、dataset-access-log.md、hardware-profile.md、execution-contract-v1.md）。
- 已做的审计：desk checks（topic compatibility / minimum quality / policy / prompt-injection 目视 / ethics）、contribution-novelty、claim-evidence（行 139-153 各主张）、evidence-plan 完整性与可行性、related-work positioning、reproducibility、calibration 一致性、panel 独立性、score-change 条件、输出质量门（章节顺序 / 表格列数 / 分数一致 / 无 placeholder）。
- 三遍阅读 + 对抗性 pass：novelty collapse、missing closest work、unsupported central claims、invalid assumptions、missing decisive comparisons。
- 未做新的公开网络检索：新颖性判断的主体证据已由冻结的 `prior-art-dedup-log.md` 与 `literature-baseline-matrix.md`（访问 2026-11-05，已核验）提供；扩展检索会引入不可追溯到本轮检索记录的链接，违反 `execution-contract-v1.md` 第 7 节「所有数字与链接必须可追溯到本轮检索记录，不得编造」。仅引用输入内已核验 URL 与任务明确给出的 https://arxiv.org/abs/2610.10023。
- 未修改任何已有项目文件；仅新建本报告文件。

# Unresolved or unverified

- **无任何实验结果、数值或曲线**：输入是 idea 卡片；本报告所有分数评的是「证据计划」，未把计划写成观测，未编造任何结果。
- JEPA-on-connectome 为 2026 **工作论文、非同行评审**（`literature-baseline-matrix.md` 行 22），其主张细节与直链内容本轮未逐字核验；本报告据去重日志与卡片自陈判定相似，标注为 unverified。
- `literature-baseline-matrix.md` 中标注「本轮未核验」的条目：arXiv:2609.01330 Has Code 直链（行 9）、Reiser Cell 2026 用 163.com 中文解读且未核验出版页（行 14）、BrainTrace 用 inews.qq.com 报道且未核验期刊页（行 15）、flyvis 神经活动响应数据需单独获取（`dataset-access-log.md` 行 25）。
- 「arXiv:2610.10023 含 `benchmark_speed.py` 与 sweep」来自任务说明与卡片共享底座描述，本轮未逐文件核验其仓库内容。
- teacher patch→连接组邻接映射、DINOv2/CLIP 推理成本、单格训练耗时/显存：均无实测，属未验证。
- 官方 pin torch 2.6/PyG 2.6/torch-sparse 与本机 `dyg-cold` torch 2.11/PyG 2.8（缺 torch_sparse）的兼容性未验证（`hardware-profile.md` 行 39-40）。
- CVPR 2027 注册/截止/contemporaneous 规则据 `execution-contract-v1.md`（访问 CFP 2026-11-05），本评审未重新访问 CFP 页面核验。
- 算力/时间冲突为定性判定，未做单格计时实测（本轮无权且无数据）。

# Output self-check

- 章节顺序：Mode / Venue and assumptions / Paper summary / Likely stance and calibrated score / Quantitative scorecard / Top strengths / Major-fatal concerns / Writing and presentation concerns / Format-venue concerns / Multi-reviewer panel / Concern-to-action table / Recommended next CCFA owner / Checks run / Unresolved or unverified / Output self-check —— 与契约一致，无缺无增。
- YAML front matter：字段严格为 idea_id / overall（一位小数 3.3）/ confidence（两位小数 0.83）/ verdict（NO-GO）/ scores 六维 / fatal_risks / go_conditions / review_execution，位于文件开头。
- 每个 ≤3 分数（本例 6 个维度全部）均写明 Deduction / Repair condition / Expected score movement（保守区间），并注明不改变 NO-GO stance。
- 每个维度有可核验 evidence basis（卡片行号 / 去重日志 / 文献矩阵 / URL），未写「需要更多实验」式泛泛表述。
- Multi-reviewer panel：4 个角色（SNN 训练 / benchmark 评测 / CV 顶会架构 / novelty positioning），每人含 Lens / Score tendency / Confidence / Main positive signal / Main negative signal / Evidence basis / Score-change condition；Panel synthesis 含 Agreement / Disagreement / Decisive accept axis / Decisive reject axis / Unresolved evidence / Final calibrated stance；未强行制造分歧或夸奖。
- Concern-to-action table：9 列，每行 9 个单元格，分隔符一致；每条 concern 绑定具体卡片句子或已核验 URL。
- 明确回答了「相对 arXiv:2610.10023 增量是否足以撑起 CVPR 主会」（否 + 三点依据）与「若只有部分正向结果的诚实下位结论」（受限 empirical note 模板）。
- 明确给出最小冒烟实验 GO/NO-GO（NO-GO + 理由）与一个可证伪失败信号（95% CI 跨 0）。
- 不写 rebuttal、不修改 idea、不生成论文文本；未把计划写成观测；未编造结果/数值/引用。
- Overall 3.3 < 6.5 且存在未解决 fatal → verdict NO-GO，与判定规则一致；confidence 0.83 与 stance 内部一致。
- 表格列数一致、无 TBD/TODO/空标题、中文标点统一、无占位符残留。
