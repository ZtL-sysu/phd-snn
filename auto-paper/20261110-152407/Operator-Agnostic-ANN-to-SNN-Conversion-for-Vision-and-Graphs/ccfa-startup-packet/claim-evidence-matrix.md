# claim-evidence-matrix.md

> 主张—证据矩阵 · 按 `ccf-experiment-designer` 职责生成（`design` + `result-template` 模式）
> 生成者：CCFA startup 包撰写员（本 Agent） · 日期：2026-11-10
> **No-fabrication 强声明**：本文件 **只含占位符与决策规则**，**绝不填任何实验结果数值**。所有结果位一律 `<TBD>`；协议参数（T 网格、seed 数、bootstrap 次数）与预注册目标阈值（ANN−1.5pp 带）不是实验结果，按原样登记并标注。

## 0. Mode / Venue / 纪律

| 项 | 值 |
| --- | --- |
| Mode | `design`（主） + `result-template`（§9 的 TBD 表模板） |
| Venue and assumptions | `CCF-A / AI, ML, CV` family；具体 venue `UNKNOWN / must-know 待确认`；按 `evidence-design.md` AI/ML 条：强且近的基线、简单基线、消融、seeds/统计、算力、超参、稳健性、诊断 |
| 中心主张 | C1–C5（见 `idea-cards.md` §1.8、`prior-art-opportunity-map.md` §6） |
| 统计协议（协议参数，非结果） | `T∈{1,2,4,8,16}`；5 冻结 seeds；配对 bootstrap `R=5000` + sign-flip `1000` + BH 校正 |
| 主指标 | `conversion loss (pp) = ANN teacher top-1 − SNN top-1`，**越低越好** |
| 次指标 | 达 ANN−1.5pp 带的最小 T；SynOps / spike count / 峰值显存（**proxy**）；理论-仿真恒等式残差 |
| 诚实边界 | 不声称能耗实测 / 生物保真 / 精度 SOTA；CIFAR 无官方 val split 须预注册从 train 切；test 只在最终评测用一次；内部先验仅内部校准 |

> 数值填充规则（决策规则，非数值）：任何 `<TBD_locked_at_G0>` 由 G0 预注册锁定；任何 `<TBD_locked_after_pilot>` 由 G7 pilot 复现基线后按 `strong-result-feasibility-contract.md` 的 baseline-calibration 规则锁定；任何 `<TBD>` 由 G7 实验后填。**本文件不锁定、不预设任何结果或 headline gain。**

---

## 1. C1 — 固定线性算子上的精确误差恒等式（理论 + 数值残差）

| 字段 | 内容（占位符 / 决策规则） |
| --- | --- |
| 所需实验 | ① 在固定、非负、线性 `A` 上解析推导 `B̂₂−B₂ = A(E₁W₂)`；② 数值残差探针：逐层同时记录 ANN `B₂` 与 SNN `B̂₂`，计算残差 `r = ‖(B̂₂−B₂) − A(E₁W₂)‖`；③ 跨 T、跨层、跨骨干（线性化 ViG / GCN）重复探针 |
| 数据集 / split | CIFAR-10 / CIFAR-100（train 预注册切 val，test 最终一次）、Tiny-ImageNet（官方 val）、Planetoid（public split）；切分比例 `<TBD_locked_at_G0>` |
| 主指标与方向 | 理论-仿真恒等式残差 `r → 0`（辅助）；主指标 conversion loss (pp) ↓ 作为一致性旁证 |
| 简单基线 | 朴素 rate-coding 转换（无 `β*`、计数解码、单相）作为「有误差但可测」的 sanity 对照；实现来源 `<TBD / 自研>` |
| 最强可行域基线 | Dual-Phase TNNLS'24 式精确误差等式在可得数据上同协议复现值（G7 复现，值 `<TBD>`）；不直接引用其官方数值 |
| 匹配内部对照 | 保持 `A`、`θ`、`β*`、seeds、T 完全一致，仅把「固定线性 `A`」替换为「行随机归一化算子」→ 检验残差是否仍闭合 |
| 消融 | (a) 去掉 `A` 线性性；(b) 让 `A` 随输入/时间动态；(c) 去掉膜电位累加解码改回计数解码；(d) 变 `T` 看残差是否系统性漂移 |
| 稳健性 / 效率测量 | 跨 5 seeds、跨 T∈{1,2,4,8,16}、跨视觉/图骨干的残差分布；配对 bootstrap 一致性；峰值显存（proxy） |
| 回答评审的哪个问题 | **Why does the mechanism work?** + **Does the method solve the stated problem?**（理论形式化 / theory 家族期望：formal model、theorem statement、proof roadmap、数值闭合） |

## 2. C2 — 非行随机算子上 `β*` + 膜电位解码相对强基线在 T≤4 降低 conversion loss

| 字段 | 内容（占位符 / 决策规则） |
| --- | --- |
| 所需实验 | 在**非行随机** `A` 上，对比 OAC（β* + 膜电位累加解码 + 确定性 `s[t]`）与 must-rerun 强基线在 `T≤4` 的 conversion loss；主表 + 配对显著性检验 |
| 数据集 / split | CIFAR-10 / CIFAR-100、Tiny-ImageNet（官方 val）；Planetoid 作辅助；split 同 §1，比例 `<TBD_locked_at_G0>` |
| 主指标与方向 | conversion loss (pp) **↓**；相对最强基线差值 `Δ = CL(method) − CL(anchor)`（负 = 更好），阈值 `<TBD_locked_after_pilot>` |
| 简单基线 | 朴素 rate-coding 转换（同 §1）；另加 QCFS 原始 floor/clamp 作为「简单已发表 sanity」 |
| 最强可行域基线 | must-rerun 六者（QCFS / FTBC / TPP / Parallel Conversion / DCGS / AdaFire）在**本项目 G1 可得数据、同协议**下复现的最佳者，值 `<TBD>`；官方 ImageNet 数值仅文献背景（见 `prior-art-opportunity-map.md` §2.3） |
| 匹配内部对照 | 保持 `A`、`θ`、T、seeds 一致，仅把 OAC 的「β* + 膜电位解码」替换为「无偏置 + 计数解码」→ 隔离降损来源 |
| 消融 | (a) 去掉 `β*`；(b) 膜电位解码→计数解码；(c) 确定性 `s[t]`→随机两阶段；(d) `A` 行随机化（回到强基线假设域） |
| 稳健性 / 效率测量 | 5 seeds 配对 bootstrap `R=5000` + sign-flip `1000` + BH；T∈{1,2,4,8,16} 曲线；SynOps / spike count / 峰值显存（proxy） |
| 回答评审的哪个问题 | **Is the comparison fair and current?**（强且近的基线 + 同协议复现）+ **Does the method solve the stated problem?** |

## 3. C3 — 确定性第二相零条件方差且不劣于 TPP

| 字段 | 内容（占位符 / 决策规则） |
| --- | --- |
| 所需实验 | 对 `s[t]=round(t·n/T)−round((t−1)·n/T)`、`n=round(a/θ)` 验证 `Σs[t]=n` 与条件方差 = 0（无 RNG）；在相同 `n,θ,T` 下与 TPP 原版第二相比 conversion loss |
| 数据集 / split | 同 §2（CIFAR-10/100、Tiny-ImageNet；Planetoid 辅助）；split 比例 `<TBD_locked_at_G0>` |
| 主指标与方向 | 条件方差 `→ 0`、`‖Σs[t]−n‖ → 0`（辅助，硬约束）；conversion loss (pp) **↓ 或不劣于 TPP**（Δ ≤ 0） |
| 简单基线 | 单相均匀脉冲分配（无两阶段） |
| 最强可行域基线 | TPP 官方实现（`github.com/shizukanaskytree/TPP-SNN`）在本项目同协议复现值，值 `<TBD>`；官方 PMLR Fig.1 数值仅背景且图注不一致已标注 |
| 匹配内部对照 | 保持 `n`、`θ`、T、seeds、`A`、`β*` 完全一致，仅把确定性 `s[t]` 替换为 TPP 原版（随机/非零条件方差）第二相 |
| 消融 | (a) 确定性 `s[t]` → 随机化；(b) 两阶段 → 单相；(c) 变 `T` 检查 `Σs[t]=n` 不变性；(d) 变 `θ` 看 `n` 舍入稳健性 |
| 稳健性 / 效率测量 | 5 seeds 下条件方差估计、跨 T 网格、无 RNG 可复现性审计（同 seed 逐位一致）；spike count（proxy） |
| 回答评审的哪个问题 | **Why does the mechanism work?**（零条件方差与恒等式闭合）+ **Can the work be reproduced or audited?**（无 RNG、确定性调度） |

## 4. C4 — 同一算子跨视觉骨干与图消息传递的通用性（图上复现 ≤1.5pp 带）

| 字段 | 内容（占位符 / 决策规则） |
| --- | --- |
| 所需实验 | 用**同一 `A` / 同一 `β*` / 同一 `s[t]` / 同一 conversion loss 协议**，分别在「冻结+线性化 ViG 视觉骨干」与「GCN 图消息传递」上横评；报告两侧 conversion loss 与进入 ANN−1.5pp 带的最小 T |
| 数据集 / split | 视觉侧：CIFAR-10/100、Tiny-ImageNet；图侧：Planetoid Cora / CiteSeer / PubMed（public split 每类 20 train / 500 val / 1000 test）；CIFAR10-DVS 仅作外部效度补充（社区 9000/1000，无官方 split） |
| 主指标与方向 | conversion loss (pp) **↓**；预注册目标阈值「进入 ANN−1.5pp 带」= `CL ≤ 1.5pp`（**目标阈值，非实测**）；达带最小 T `T*`（值 `<TBD>`） |
| 简单基线 | 各骨干上朴素 rate-coding 转换（不共享 `A` 协议） |
| 最强可行域基线 | 各域内 must-rerun / One-Spike SNN 背景方法在**同协议**复现值，值 `<TBD>`；内部先验（图节点分类 T≤8 达 ANN−1.5pp 带内）**仅内部校准，绝不当公开证据** |
| 匹配内部对照 | 同一骨干上，把「统一 `A` 协议」替换为「各骨干独立调参/独立算子」→ 检验统一协议是否牺牲精度 |
| 消融 | (a) 视觉侧不冻结 KNN 图；(b) 视觉侧保留 max-relative 非线性；(c) 图侧换非 GCN 聚合；(d) 去掉跨骨干统一协议 |
| 稳健性 / 效率测量 | 5 seeds、跨骨干、跨数据集；配对 bootstrap + BH；SynOps / 峰值显存（proxy）；视觉侧 0 正式实验 → 全部 `<TBD>` |
| 回答评审的哪个问题 | **Does the result generalize across settings?**（跨视觉骨干与图消息传递）+ **Is the comparison fair and current?**（同一协议） |

## 5. C5 — 动态 / 非线性算子上恒等式按预测失效（边界诊断）

| 字段 | 内容（占位符 / 决策规则） |
| --- | --- |
| 所需实验 | **失效边界诊断**：对原版 ViG（max-relative 含 max 非线性 + KNN 动态图）运行与 C1 相同的残差探针，预测残差显著 > 冻结线性化版本；与 C1 结果配对比较 |
| 数据集 / split | 视觉侧 CIFAR-10/100、Tiny-ImageNet；原版 ViG 与其冻结线性化版本用**同一 split / 同一 seeds / 同一 T** |
| 主指标与方向 | 恒等式残差 `r`：原版 ViG **显著 >** 冻结线性化版本（方向 = 失效）；conversion loss 仅作旁证 |
| 简单基线 | 冻结 + 线性化 ViG（即 C1 主协议下的算子） |
| 最强可行域基线 | 原版 ViG 自身在可得数据上的转换结果（值 `<TBD>`）；不引入新基线 |
| 匹配内部对照 | 保持权重、split、seeds、T 一致，仅切换「冻结+线性化」↔「原版动态+非线性」这一处 |
| 消融 | (a) 只引入 max 非线性（图仍冻结）；(b) 只引入动态 KNN（聚合仍线性）；(c) 两者同时 → 定位是哪一项破坏恒等式 |
| 稳健性 / 效率测量 | 5 seeds 残差分布、跨 T；配对 bootstrap 检验「原版 > 线性化」方向；峰值显存（proxy） |
| 回答评审的哪个问题 | **What fails, when, and why?**（失效边界 / negative-result）+ **Does the evidence match the venue's expectations?**（诊断与 limitation study） |

---

## 6. 汇总矩阵（一览，全部为占位符 / 决策规则）

| Claim | 主指标方向 | 简单基线 | 最强可行域基线（G7 复现） | 匹配内部对照 | 关键消融 | 评审问题 |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 恒等式残差 → 0 | 朴素 rate-coding | Dual-Phase 式等式复现值 `<TBD>` | 线性 `A` → 行随机算子 | 去线性 / 动态 `A` / 换解码 | Why mechanism works / solves problem |
| C2 | CL (pp) ↓ | 朴素 + QCFS floor | must-rerun 六者最佳 `<TBD>` | 去 β* + 计数解码 | 去 β* / 换解码 / 行随机化 | Fair & current / solves problem |
| C3 | 方差→0、Σs=n、CL 不劣于 TPP | 单相均匀 | TPP 官方实现复现值 `<TBD>` | 确定性 s[t] → TPP 第二相 | 随机化 / 单相 / 变 θ | Why mechanism works / reproducible |
| C4 | CL (pp) ↓，≤1.5pp 带（目标） | 各骨干朴素 | 各域同协议复现值 `<TBD>` | 统一 A → 各骨干独立 | 不冻结图 / 留 max / 换聚合 | Generalize across settings / fair |
| C5 | 残差：原版 > 线性化 | 冻结线性化 ViG | 原版 ViG 自身 `<TBD>` | 冻结线性化 ↔ 原版动态 | 只 max / 只动态 KNN | What fails when why / venue fit |

## 7. Dataset / benchmark needs
- 主：CIFAR-10 / CIFAR-100（**无官方 val split → G0 预注册从 train 切**，test 最终一次）、Tiny-ImageNet（官方 val，test 无标签）、Planetoid（public split）。
- 辅助 / 外部效度：CIFAR10-DVS（社区 9000/1000，无官方 split，须预注册）。
- 排除（G2）：ImageNet-1K / ILSVRC、ImageNet-100、DVS128 Gesture；N-MNIST 待补证。
- 全部数据集事实见 `prior-art-opportunity-map.md` §2。

## 8. Baseline matrix（`evidence-design.md` 模板，简化）

| Baseline | Why included | Source / implementation | Fairness constraints | Expected metric | Can run? | If missing |
| --- | --- | --- | --- | --- | --- | --- |
| 朴素 rate-coding 转换 | simple sanity | 自研 `<TBD>` | 同 split / seeds / T | CL (pp) | yes（G6 后） | 自研组件待 M1 |
| QCFS / FTBC / TPP / Parallel Conversion / DCGS / AdaFire | close + current strong | 官方仓库（见 `prior-art-opportunity-map.md` §3.1） | 同协议、同数据、同统计 | CL (pp) | yes（G7 复现） | 与官方数值偏差超容差 → stop-and-return G6 |
| OAC 内部消融版 | ablated version of method | 自研（统一 `A` 抽象层） | 只改被检验组件 | CL / 残差 / 方差 | yes（G6 后） | 组件里程碑 M1–M3 |
| 原版 ViG（动态 + max） | failure / boundary | ViG 官方权重 + 不改聚合 | 与冻结线性化版仅差算子 | 残差 r | yes（G6 后） | 冻结图线性化失败 → 回 G4 |

## 9. Result tables / figure specs（`result-template`，**全部 `<TBD>`**）

**表 R1 — conversion loss (pp) vs T**（越低越好）
| 方法 \ T | 1 | 2 | 4 | 8 | 16 |
| --- | --- | --- | --- | --- | --- |
| 朴素 rate-coding | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| 最强可行域基线（G7 复现） | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| matched internal control | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| OAC | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| ANN teacher（参考行，CL=0 定义） | `0` | `0` | `0` | `0` | `0` |

**表 R2 — 理论-仿真恒等式残差 `r`**（→ 0 为通过）
| 算子类型 \ T | 1 | 2 | 4 | 8 | 16 |
| --- | --- | --- | --- | --- | --- |
| 固定线性 `A`（C1） | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| 行随机算子（C1 对照） | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| 原版 ViG 动态+max（C5，预测大） | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |

**表 R3 — `s[t]` 诊断（C3）**
| 量 | 目标（预注册） | 实测 |
| --- | --- | --- |
| `Σs[t]` | `= n` | `<TBD>` |
| 条件方差 | `= 0`（无 RNG） | `<TBD>` |
| 与 TPP 第二相的 ΔCL | `≤ 0` | `<TBD>` |

> 图 spec 仅登记：CL-vs-T 曲线（含 BH 校正后置信带）、残差-vs-T 曲线、跨骨干 CL 对比。**无真实数值，不出图**；真实结果出图属 `ccf-visual-composer`（`result-presentation` 模式），不在本包范围。

## 10. Missing values（全部显式登记）
- 一切实验数值：CL(pp)、残差 `r`、`T*`、条件方差、Σs[t]、SynOps / spike count / 峰值显存 → `<TBD>`。
- 阈值锚：`<TBD_locked_at_G0>`（split 比例、`θ` 分位）、`<TBD_locked_after_pilot>`（MDE、Δ 阈值、容差）。
- 具体 venue / tier、`ccfa.yaml`、`torchvision` 补装、GCN 实现来源、novix 提交时机 → 未决。

## 11. Execution priority（依赖顺序）
1. **C1 + C5**（共用残差探针）：最先。若固定线性 `A` 上残差不闭合 → 理论崩塌，stop-and-return，不进主实验；若原版 ViG 也闭合 → 理论定位崩塌，stop-and-return。
2. **C3**（`s[t]` 零方差）：M2 里程碑，独立于视觉精度，可早期验证。
3. **C2**（强基线对比）：需 G7 先复现 must-rerun 基线并锁定阈值锚。
4. **C4**（跨骨干横评）：最后，依赖视觉侧正式实验 + 图侧统一协议就绪。

## 12. No-fabrication status / Next CCFA owner
```
Mode: design + result-template
No-fabrication: 通过 — 本文件零实验结果数值、零评审分数、零虚构 URL；所有结果位 <TBD>
Checks run: C1–C5 九字段逐条映射、基线矩阵、消融逻辑、稳健性/效率、TBD 表模板、执行优先级
Checks skipped: 真实结果出图/出表（ccf-visual-composer）、论文散文（ccf-paper-writer）、诚信审计（validation）
Next CCFA owner: ccf-experiment-designer（承接 G6 实现就绪 → G7 执行）；再交 ccf-integrity-auditor（validation）
```
