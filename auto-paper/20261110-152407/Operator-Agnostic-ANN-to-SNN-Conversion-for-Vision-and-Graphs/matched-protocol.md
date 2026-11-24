# Matched-Protocol · 统一比较协议（冻结版 v1）

> 生成 2026-11-10｜本文件是第二次独立红队指出的 F3 缺口（`matched-protocol.md` 当时不存在）的实物补齐。
> 地位：`f-research-v1` P3/P4 的**唯一比较协议**；任何偏离必须版本化升 v2 并在 `pipeline-state.json` 记 `reopen`，不得静默改。
> 所有结果栏在实验前一律 `TBD`；本文件不含任何实验结果、不含任何编造数值。

## 1. 为什么需要它

OAC-rev2 的横评对象是**同一批被固定的骨干**。若基线跑原始骨干、我们跑冻结/线性化骨干，conversion loss 不可比；若把基线移到同一骨干却不控制 teacher、阈值、校准数据与 T 网格，增益无法归因。本协议把这两点写死。

## 2. 骨干与算子类（所有方法共用，不得各跑各的）

| 臂 | 骨干 | 传播算子 | ρ_n 范围 | 角色 |
|---|---|---|---|---|
| B1 | VGG-16 / ResNet-18（CIFAR-10/100） | 卷积 + 线性投影 | ≈1 | 行随机对照臂；预测我们与最强基线**非劣效** |
| B2 | 线性化 + 冻结 KNN 图的 ViG（ViG-Ti/S 结构，CIFAR-10/100、Tiny-ImageNet） | 冻结 KNN 图 + 线性（mean/sum）聚合 | ≠1，随度数变化 | 主战场；预测 ρ_n/T 单调差距 |
| B3 | 2 层 GCN（Cora / CiteSeer / PubMed） | 对称归一化 / mean / sum | 对称归一化实测可达 5.75（Cora，成稿） | 同一算子的图侧通用性臂 |
| B4 | 原版 ViG（动态 KNN + max-relative） | 动态、非线性 | 不适用 | **失效边界诊断**，不进主结果、不得删 |
| B5 | CIFAR10-DVS（可选） | 事件帧 + 上述骨干 | 视骨干而定 | 稳健性臂，不进主 claim |

构造规则：B2 的 KNN 图在**前处理阶段**按冻结策略一次性确定并随数据落盘（含图文件 SHA-256），推理时不再随样本重算；聚合中的 `max` 一律替换为线性 `mean` 或 `sum`，并在论文中量化此替换相对原版 ViG 的 ANN teacher 精度代价（不得隐瞒）。B4 保留原版实现，仅用于验证 M0-P6 的失效预测。

## 3. Teacher 与转换前置（所有方法同一份）

1. 每个 (骨干, 数据集) 训练**唯一一份** ANN teacher，冻结权重并落 SHA-256；所有转换方法从这一份权重出发。
2. QCFS 类需要重训源 ANN 的方法，使用**同一随机种子、同一增广、同一 epoch/batch/优化器**，并把重训后的 teacher 精度与冻结 teacher 一并报告（避免"teacher 更好所以 SNN 更好"）。
3. 阈值 θ、每层 scale、calibration 数据（固定 512 张 train 子集，种子固定）全局统一；任何方法需要自己的阈值时须记录并作为敏感性分析，不得默认不同。
4. T 网格固定 `T ∈ {1, 2, 4, 8, 16}`；不允许各方法自选最优 T 后进主表。
5. 神经元统一为 soft-reset IF；某方法要求特殊神经元（TPP 概率相、AdaFire burst、DCGS 多阈值）时，该差异本身即为被比较对象，须在表中单列 `neuron_family`。

## 4. 指标定义（唯一口径）

- **主指标**：`conversion loss = ANN teacher top-1(%) − SNN top-1(%)`，单位 pp，**越低越好**。
- 次指标：达到 `ANN − 1.5pp` 带内所需最小 T、`argmax` 一致率、`B2hat − B2 = A(E1 W2)` 浮点残差、`Σ_t s[t]=n` 命中率与第二相条件方差。
- 效率 proxy：SynOps、spike count、峰值显存、wall-clock。**全部标注为 proxy**，不得写成能耗实测或硬件收益。
- 统计：5 个**冻结** seed（0–4）；seed 级配对 bootstrap `R=5000` 给 95% CI；sign-flip 置换 1000 次；跨多比较用 BH 校正 `q<0.05`。主表报告均值±std 与配对差值 CI，不报单 seed 最好值。

## 5. 数据划分（防泄漏）

- CIFAR-10/100 **无官方 val split**：预注册从 50,000 train 中按固定 seed 切 45,000/5,000，test 10,000 **只在最终评测用一次**。
- Tiny-ImageNet：官方 100k train / 10k val / 10k test（test 无标签）→ 用 val 作最终评测，train 内切 val 作选择。
- CIFAR10-DVS：无官方 split → 预注册社区 9,000/1,000，降采样 48×48、T≤20、batch≤32–64。
- Planetoid：`split='public'` 固定划分（每类 20 train / 500 val / 1000 test），不重切。
- 任何用于选择方法/超参的测试集，之后不得再被描述为"unseen"。

## 6. 基线清单与执行顺序（重叠 level 决定优先级）

| 批次 | 方法 | 角色 | 代码状态 | 备注 |
|---|---|---|---|---|
| **第 0 批** | PASCAL (TMLR'25) | 确定性精确计数最近邻 | **无官方码，自行复现** | 与 TPP 同为最决定性对照，必须最先跑通 |
| **第 0 批** | TPP (ICML'25) | 两阶段框架最近邻 | 官方 `github.com/shizukanaskytree/TPP-SNN` | 与 PASCAL 同批；二者任一未跑通不得进主表 |
| 第 1 批 | QCFS (ICLR'22) | 锚点 / 源激活 | `github.com/putshua/SNN_conversion_QCFS` | 先做回归测试：复现 91.18%@T=2 / 93.96%@T=4（官方数值） |
| 第 1 批 | FTBC (ECCV'24) | 零期望偏置 | `github.com/shizukanaskytree/FTBC` | 仓库自带 QCFS/RTS/SNNC 基线目录 |
| 第 1 批 | Parallel Conversion (ICML'25) | T=4 低时延 | `github.com/hzc1208/Parallel_Conversion` | 官方 72.90% top-1 ImageNet ResNet-34 @T=4 仅作文献背景（ImageNet 为 G2） |
| 第 1 批 | DCGS (ICML'25) | 差分编码 | `github.com/h-z-h-cell/ANN-to-SNN-DCGS` | 只跑 CNN 子集 |
| 第 1 批 | AdaFire (AAAI'25) | 自适应 burst | `github.com/bic-L/burst-ann2snn` | 只跑分类子集 |
| 第 2 批 | CS-QCFS (Neural Networks'25) / ECL (arXiv'25) | adaptation-attempt | **无官方码，自行复现** | 复现失败须如实记录，不得用文献数值顶替主表 |
| 文献对照 | Diehl'15 / Rueckauer'17 / SpikeNorm'19 / RMP-SNN'20 / SpikeConverter'22 / One-Spike SNN / Adaptive Fission'25 / 2026 预印本 | literature-context | 不适用 | **只进 related work，不进主比较表** |

## 7. 我们的臂（OAC-rev2）与必须做的消融

主臂 = 固定线性算子类上的 ρ 加权闭式偏置 `β*=θ/(2T)` + 膜电位累加解码 + 确定性两阶段第二相。**全部组件明确归功前人**，不声称发明。

| ID | 消融 | 回答的评审问题 |
|---|---|---|
| A1 | 去 β*（β=0） | 系统项是否真按 ρ_n 加权、β* 是否在 ρ≠1 上仍最优 |
| A2 | 计数解码 vs 膜电位累加解码 | 两解码是否冗余；冗余则删除该组件 |
| A3 | Bernoulli 第二相（TPP 式）vs 确定性 s[t] | 确定性化是否只带来"零方差"这一同义反复，还是有可测系统增益 |
| A4 | 去两阶段累积相 | 两阶段结构本身的贡献 |
| A5 | 固定 KNN 图 vs 动态 KNN 图 | 适用边界；动态图应使恒等式残差显著非零 |
| A6 | 线性聚合 vs 原版 max-relative | 非线性边界；并量化冻结/线性化相对原版 ViG 的 ANN 精度代价 |
| A7 | ρ≈1 的 CNN 臂 vs ρ≠1 的 B2/B3 臂 | 判据是否只在非行随机算子上生效（若 CNN 上我们也"显著更好"，判据被推翻） |

## 8. 停止与回退（与 `strong-result-feasibility-contract.md` S1–S7 对齐）

- S1：M0 恒等式残差超出浮点容差 → 回 G3，禁止进 P4。
- S2：第 0 批 PASCAL / TPP 任一无法复现 → 停止主表，转为 `needs-evidence`。
- S3：B4（原版动态/非线性 ViG）上恒等式**仍成立** → 适用边界写错，回 G3 重定算子类。
- S4：主判据（conversion loss 差距随 ρ_n/T 单调）连续落 failure → `pivot-with-rescue-route`，收敛为纯 benchmark + 失效边界。
- S5：`torchvision` 补装失败或 3060/4090 上全套基线跑不通 → `needs-evidence`。
- S6：任何诚信违规（挑 seed、调参到显著、删除负结果、把未公开先验当公开证据）→ 停止，回 `validation` 审计。
- S7：数据划分/许可违反 §5 或 G2 数据被私自使用 → `revise`。

## 9. 复现产物

每次运行落盘：`config.json`、teacher 权重 SHA-256、冻结图文件 SHA-256、seed 列表、`conversion_loss.csv`、脉冲轨迹摘要、环境快照（conda env export + `nvidia-smi`）、完整 log。所有数值由脚本从结果文件生成，禁止手抄进表。

## 10. 明确不做

不做 ImageNet-1K 全量训练（G2 需审批）；不声称精度 SOTA；不声称能耗实测或生物保真；不把用户未发表的图节点 1.5pp 先验写入任何证据表；不把文献里的 ImageNet 官方数值当作本协议下的对照阈值。
