# prior-art-opportunity-map.md

> 先验 / 机会地图 · 按 `ccf-literature-searcher` 职责组装（standard 模式输出：clusters + opportunity map + benchmark table + handoff summary）
> 生成者：CCFA startup 包撰写员（本 Agent） · 日期：2026-11-10
> 纪律：不编造论文、引用、venue、链接、录用状态、数值结果；已核验事实与推断分离；无官方数值一律 `NOT VERIFIED`；无稳定论文 URL 一律 `NOT VERIFIED (URL)`，不编造；MDPI 等源按共享策略排除。

## 0. Search purpose / Source policy / Provenance

| 项 | 值 |
| --- | --- |
| Search purpose | 为本 startup 包做 novelty grounding、Related-Work 结构、benchmark/数据集发现、experiment-design 输入（非最终 novelty kill gate） |
| 是否执行新检索 | **否**。本 Agent 职责是按用户已提供的「已核验事实」组装 startup 工件；所有检索类事实的 provenance = `known from user-provided verified material`。novelty 判定由用户给定的 **G4 `pass-with-narrowing`** 提供，本报告不重新裁定 |
| 论文标识方式 | 「方法名 + venue + 年份」。用户未提供稳定论文 URL → 全部标 `NOT VERIFIED (URL)`，**不编造链接**；代码仓库 URL 为用户原样提供，照录 |
| paper type | 按 `search-and-scoring.md` taxonomy 标注，均为 `inferred`（用户未给类型，按名称推断） |
| Source policy | 偏好官方 proceedings / PMLR / CVF / OpenReview / arXiv / 项目页 / 数据集页；**排除 MDPI**、predatory、无稳定链接、仅 snippet 可见的来源 |
| Excluded source notes | 本次未执行新检索，无新增排除项；共享排除策略（MDPI 等）仍适用于后续 G3 重搜 |
| Folder written | 用户指定单文件输出，未建 `literature-search-YYYYMMDD-*/` 标准目录；本文件即机会地图载体 |

**Provenance 图例**：`[U]` = known from user-provided verified material（用户已核验）；`[P]` = known from public source（官方仓库/论文，由用户核验后转述）；`[I]` = inferred（本报告推断）；`[?]` = unknown / NOT VERIFIED。

## 1. Closest-work clusters（含 G4 判定与三处真空白）

> 分类标签取自 `search-and-scoring.md` Opportunity Mapping。每个 `covered central claim` 仍给出 rescue route 与 evidence needed。

### Cluster 1 — 偏置校准与零期望误差偏置 `[U]`
| 项 | 内容 |
| --- | --- |
| 成员 | `β*=θ/(2T)` → Deng&Gu ICLR'21；零期望误差偏置 → QCFS ICLR'22 / FTBC ECCV'24 |
| 标签 | `covered central claim`（数学组件已被占） |
| 已覆盖 | 闭式最优偏置、量化误差期望对齐到零、低 T 下的 floor/clamp 校准 |
| 欠测试 | 均绑定具体 CNN 层 / 行随机或归一化假设；未处理「固定线性算子 `A`」的层类型无关表述 |
| Rescue route | **不作为 novelty**，仅作 OAC 的既有组件；差异化走真空白①（把误差刻画统一到 `A`） |
| Evidence needed | 无（定位已定）；若后续 G3 重搜发现 `A`-level 统一版本 → 回 G4 重估 |
| paper type | `theory/proof`（Deng&Gu）、`pure method`（QCFS / FTBC）`[I]` |

### Cluster 2 — 膜电位解码与精确误差等式 `[U]`
| 项 | 内容 |
| --- | --- |
| 成员 | Dual-Phase TNNLS'24：膜电位累加解码 + 精确误差等式 |
| 标签 | `covered central claim` |
| 已覆盖 | 用膜电位累加替代计数解码、给出精确误差等式 |
| 欠测试 | 等式的「层类型无关 / 算子无关」形式；与固定线性 `A` 的绑定；与图消息传递的关系 |
| Rescue route | 真空白①：把等式从特定层推广为**固定线性算子上层类型无关的精确统一**（C1） |
| Evidence needed | 需证明 `B̂₂−B₂ = A(E₁W₂)` 在任意固定线性 `A` 上成立，且数值残差闭合 |
| paper type | `theory/proof` + `pure method` `[I]` |

### Cluster 3 — 确定性精确计数 `[U]`
| 项 | 内容 |
| --- | --- |
| 成员 | PASCAL TMLR'25（确定性精确计数；属 adaptation-attempt，无官方代码） |
| 标签 | `covered central claim` |
| 已覆盖 | 确定性、精确脉冲计数思想 |
| 欠测试 | 本项目不采用其计数机制；其与第二相时间误差扩散的确定性化不同 |
| Rescue route | 真空白②：用确定性两阶段 `s[t]` 扩散实现零条件方差、无 RNG，而非计数机制（C3） |
| Evidence needed | `Σs[t]=n`、条件方差 0、且不劣于 TPP |
| paper type | `pure method` `[I]` |

### Cluster 4 — 两阶段时间误差扩散 `[U]`
| 项 | 内容 |
| --- | --- |
| 成员 | TPP ICML'25 / SpikeConverter AAAI'22 |
| 标签 | `crowded but open` |
| 已覆盖 | 两阶段 / 时间误差扩散框架 |
| 欠测试 | **TPP 第二相的特定确定性化**：零条件方差、无 RNG、与精确恒等式严格闭合（真空白②） |
| Rescue route | 不主张发明两阶段框架；只主张第二相的确定性特化（C3），并用 matched internal control 对照 TPP 原版 |
| Evidence needed | 同 `n,θ` 下 `s[t]` 零条件方差、conversion loss 不劣于 TPP |
| paper type | `pure method` `[I]` |

### Cluster 5 — 跨 CNN + GCN 统一 `[U]`
| 项 | 内容 |
| --- | --- |
| 成员 | One-Spike SNN TETC'24/25（跨 CNN+GCN） |
| 标签 | `covered central claim`（跨骨干 idea 已被占） |
| 已覆盖 | CNN 与 GCN 统一的脉冲化思路 |
| 欠测试 | 「**同一固定线性算子 `A`** + 统一 conversion loss 协议」的横评；**ViG 首次脉冲化**；冻结图 + 线性化聚合的算子假设 |
| Rescue route | 真空白③：首次 ViG 脉冲化 + 同一算子跨视觉骨干与图消息传递的统一协议 conversion loss 横评（C4） |
| Evidence needed | 同协议下图侧复现进入 ANN−1.5pp 带（内部校准目标，非公开证据）；视觉侧须先有正式实验 |
| paper type | `pure method` `[I]` |

### Cluster 6 — 基础转换与近期背景 `[U]`
| 项 | 内容 |
| --- | --- |
| 成员 | Diehl'15 / Rueckauer'17 / SpikeNorm'19 / RMP-SNN CVPR'20 / Adaptive Fission NeurIPS'25 / 2026 预印本 RMP-Alignment、GTDL |
| 标签 | `background only`（literature context，不强制 rerun） |
| 作用 | 界定字段边界与时序；2026 预印本提示需 G3 重搜确认是否覆盖真空白① |
| paper type | `pure method` / `theory/proof` / `other` `[I]`；2026 预印本状态 `NOT VERIFIED` |

### Cluster 7 — 三处真空白（差异化簇，`[U]` 给定 / `[I]` 归类）
| # | 真空白 | 机会标签 | 对应 claim |
| --- | --- | --- | --- |
| ① | **固定线性算子的层类型无关精确统一** | `theory/analysis gap` | C1 |
| ② | **TPP 第二相的特定确定性化（零条件方差、无 RNG）** | `mechanism gap` | C3 |
| ③ | **首次 ViG 脉冲化 + 同一算子跨视觉骨干与图消息传递的统一协议 conversion loss 横评** | `benchmark gap` + `negative-result opportunity`（失效边界） | C4 / C5 |

### G4 判定（用户给定，照录）
`pass-with-narrowing`。数学组件已被占：`β*=θ/(2T)`→Deng&Gu ICLR'21；零期望误差偏置→QCFS ICLR'22 / FTBC ECCV'24；膜电位解码+精确误差等式→Dual-Phase TNNLS'24；确定性精确计数→PASCAL TMLR'25；两阶段→TPP ICML'25 / SpikeConverter AAAI'22；跨 CNN+GCN→One-Spike SNN TETC'24/25。**真空白只有** ①②③ 三条。

**硬风险（用户给定）**：原版 ViG 的 max-relative 聚合含 max 非线性 + KNN 动态图，破坏线性/固定算子假设 → **必须冻结图 + 线性化**，并把原版 ViG 作为 **失效边界诊断实验**（C5）。

## 2. 公开数据集（G1 直接公开 / G2 排除）

### 2.1 G1 直接公开（已核验）
| 数据集 | 规模 / 实测 | split | license / 条款 | 可得性核验 | 备注 |
| --- | --- | --- | --- | --- | --- |
| CIFAR-10 / CIFAR-100 | 官方 162.6 / 161.2 MiB | 50k train / 10k test；**无官方 val split** | license `NOT VERIFIED` | 实测 HTTP 200 | 须 G0 预注册从 train 切 val；test 只在最终评测用一次 |
| Tiny-ImageNet | 248,100,043 B（实测） | 200 类；100k train / 10k val / 10k test；**test 无标签** | 非商业条款 | 实测可得 | val 可用于调参，test 无标签不作最终评测 |
| CIFAR10-DVS | figshare；8,384,752,624 B | 10k 流 / 10 类；**无官方 split**，社区 9000/1000 | CC BY 4.0 | 实测可得 | 社区 split 须预注册；不引入官方 split 假设 |
| Planetoid Cora / CiteSeer / PubMed | GitHub raw 直链 | public split：每类 20 train / 500 val / 1000 test | `NOT VERIFIED` | 直链实测 200 | 图侧主数据集；用官方 public split |
| ViG 代码 + 8 个预训练权重 | `huawei-noah/Efficient-AI-Backbones` | — | Apache-2.0 | GitHub Release 无摩擦 | 视觉侧骨干与 teacher 权重来源 |

### 2.2 G2 必须排除
| 数据集 | 排除原因 | 状态 |
| --- | --- | --- |
| ImageNet-1K / ILSVRC | 需申请 + 人工审批 | 排除，不得作为本项目自跑数据 |
| ImageNet-100 | 无统一直链 / split | 排除 |
| DVS128 Gesture | 需登录手动下载 | 排除 |
| N-MNIST | 条件性待补证 | `NOT VERIFIED`，不作为启动依赖 |

### 2.3 由此产生的关键证据边界（诚实声明）
G2 排除了 ImageNet，因此 §4 中所有 **ImageNet 官方数值只能作文献背景与 baseline-calibration 参考**，**不能**作为本项目自跑对照或 headline 直接比较对象。本项目一切 baseline-calibrated 阈值必须以 **G7 在 G1 可得数据集上、同协议复现的基线值为锚**（见 `strong-result-feasibility-contract.md`）。

## 3. 当前强基线 / 代码可得性

### 3.1 must-rerun（官方代码已核验 `[U/P]`）
| 方法 | venue / year | 代码仓库（用户原样提供） | paper type `[I]` | 官方数值状态 |
| --- | --- | --- | --- | --- |
| QCFS | ICLR'22 | `github.com/putshua/SNN_conversion_QCFS` | `pure method` | 见 §4 |
| FTBC | ECCV'24 | `github.com/shizukanaskytree/FTBC` | `pure method` | 见 §4 |
| TPP | ICML'25 | `github.com/shizukanaskytree/TPP-SNN` | `pure method` | 见 §4（含不一致标注） |
| Parallel Conversion | ICML'25 | `github.com/hzc1208/Parallel_Conversion` | `pure method` | 见 §4 |
| DCGS | ICML'25 | `github.com/h-z-h-cell/ANN-to-SNN-DCGS` | `pure method` | `NOT VERIFIED` |
| AdaFire | AAAI'25 | `github.com/bic-L/burst-ann2snn` | `pure method` | `NOT VERIFIED` |

### 3.2 adaptation-attempt（无代码，需自行复现 `[U]`）
| 方法 | venue / year | 代码可得性 | 官方数值状态 |
| --- | --- | --- | --- |
| PASCAL | TMLR'25 | 无官方代码 → 自行复现 | `NOT VERIFIED` |
| CS-QCFS | Neural Networks'25 | 无官方代码 → 自行复现 | `NOT VERIFIED` |
| ECL | arXiv'25 | 无官方代码 → 自行复现 | `NOT VERIFIED` |

### 3.3 literature-context（背景，不强制 rerun `[U]`）
Diehl'15 / Rueckauer'17 / SpikeNorm'19 / RMP-SNN CVPR'20 / SpikeConverter AAAI'22 / One-Spike SNN / Adaptive Fission NeurIPS'25 / 2026 预印本 RMP-Alignment、GTDL。
（SpikeConverter AAAI'22、One-Spike SNN 同时出现在 §1 的「数学组件被占」聚类中，此处仅作背景登记，不重复计分。）

### 3.4 代码 / checkpoint 可得性小结
- 6 个 must-rerun 基线：官方仓库已核验，可直接拉取。
- ViG：`huawei-noah/Efficient-AI-Backbones`，Apache-2.0，8 个预训练权重经 GitHub Release 无摩擦获取。
- 3 个 adaptation-attempt：无代码，G6 需自行复现并标 `NOT VERIFIED`。
- GCN 消息传递具体实现来源：`TBD / 需确认`，**不编造库名或 URL**。
- 本机缺失：`torchvision`（conda `dyg-cold` 需补装，G6 blocker）。
- 自研缺失组件：统一 `A` 抽象层、确定性 `s[t]` 调度器、膜电位累加解码、恒等式残差探针、跨骨干统一 conversion loss 横评 harness。

## 4. 已核验官方数值（可引用，注明来源；无官方数值一律 NOT VERIFIED）

| 方法 | 数值 | 来源 | 标注 |
| --- | --- | --- | --- |
| QCFS | CIFAR-10 VGG-16 **91.18%@T=2**、**93.96%@T=4** | QCFS 官方（用户已核验 `[U/P]`） | 公开已发表数值，非本项目实测；CIFAR-10 属 G1 可得数据 |
| FTBC（叠加 QCFS） | ImageNet VGG-16 @T=2 由 **1.50% → 41.10%** | FTBC 官方（用户已核验 `[U/P]`） | 公开已发表数值；ImageNet 受 G2 排除 → 仅文献背景 |
| Parallel Conversion | ImageNet ResNet-34 **72.90% top-1 @T=4** | Parallel Conversion 官方（用户已核验 `[U/P]`） | 公开已发表数值；ImageNet 受 G2 排除 → 仅文献背景 |
| TPP | 官方 **PMLR PDF Fig.1** VGG-16 / ImageNet T=4：QCFS **4.67% → TPP 68.39%** | TPP 官方 PMLR PDF Fig.1（用户已核验 `[U/P]`） | **该图注与表内末列不一致，须标注**；仅文献背景 |
| DCGS / AdaFire / PASCAL / CS-QCFS / ECL / One-Spike SNN / SpikeConverter / 2026 预印本等 | `NOT VERIFIED` | — | 无官方数值一律 `NOT VERIFIED` |

> 引用纪律：以上数值均为**公开已发表数值**，不是本项目实验结果；不得写入 `claim-evidence-matrix.md` 或 `strong-result-feasibility-contract.md` 的「结果」栏；不得据此凭空设定 headline gain。

## 5. 指标与统计协议（用户给定，照录）

| 项 | 值 |
| --- | --- |
| 主指标 | `conversion loss (pp) = ANN teacher top-1 − SNN top-1`，**越低越好** |
| 次指标 | 达 ANN−1.5pp 带的最小 T；SynOps / spike count / 峰值显存（**均为 proxy**）；理论-仿真恒等式残差 |
| 时步 | `T∈{1,2,4,8,16}`，主结论聚焦 `T≤4` |
| seeds | 5 冻结 seeds |
| 统计 | 配对 bootstrap `R=5000` + sign-flip `1000` + BH 校正 |
| 诚实边界 | 不声称能耗实测（SynOps/spike 为 proxy）、不声称生物保真、不声称精度 SOTA |

## 6. 差异化路线（汇总 → 五条主 claim）

| 路线 | 依托真空白 | 主张 | 关键对照 |
| --- | --- | --- | --- |
| R1 | ① | C1 固定线性算子上的精确误差恒等式（理论 + 数值残差） | 解析解 vs 仿真残差；非线性/动态算子作边界 |
| R2 | ② | C3 确定性第二相零条件方差且不劣于 TPP | TPP 原版第二相（matched internal control） |
| R3 | ③ | C4 同一算子跨视觉骨干与图消息传递的通用性（图上复现 ≤1.5pp 带） | 同 `A` 协议下视觉骨干 vs GCN；One-Spike SNN 背景 |
| R4 | ③ + 硬风险 | C5 动态/非线性算子上恒等式按预测失效（边界诊断） | 原版 ViG（max-relative + 动态 KNN）vs 冻结线性化版本 |
| R5 | 整合 | C2 非行随机算子上 `β*` + 膜电位解码相对强基线在 T≤4 降低 conversion loss | must-rerun 强基线（G7 同协议复现值） |

**不走的路线**：不声称发明已占数学组件；不做纯标准 CNN 横评作为中心贡献（对照卡 A）；不做纯事件视觉时序作为中心贡献（对照卡 B）；不依赖 G2 排除数据自跑。

## 7. Novelty and positioning risks
- 三处真空白是 G4 判定后的**窄**空间；若 G3 重搜（尤其 2026 预印本 RMP-Alignment、GTDL）发现 `A`-level 层类型无关统一已被覆盖 → 真空白①崩塌，须回 G4 重定位（已写入 stop-and-return）。
- 「跨 CNN+GCN」idea 已被 One-Spike SNN 占，差异化必须严格落在「同一固定线性 `A` + 统一 conversion loss 协议 + ViG 首次脉冲化」这一具体协议上，不得泛化为「跨骨干统一」大主张。
- 官方强基线数值多来自 ImageNet（G2 排除），评审可能质疑对比公平性 → 必须在 G7 用 G1 可得数据同协议复现基线，并以复现值为阈值锚。

## 8. Handoff summary（→ `ccf-experiment-designer`）
- Closest-work groups：§1 七簇；novelty gaps：三处真空白。
- Citation cautions：无稳定论文 URL（`NOT VERIFIED (URL)`）；TPP 图注与表内末列不一致须保留标注；无官方数值一律 `NOT VERIFIED`。
- Datasets / baselines / metrics / benchmark protocols：§2 / §3.1 / §5。
- 对 experiment design 的输入：must-rerun 6 个、adaptation-attempt 3 个、G2 排除清单、官方数值仅作背景、阈值须 G7 pilot 后锁定。

## 9. Checklist status（`ccf-literature-searcher` standard，诚实标注执行边界）
```
[U] 用户已提供已核验事实 → 本包直接采用，未执行新网页检索
[done] 主题转为 public-safe 标识（方法名+venue+年份）；未使用私有原文做查询
[done] 共享源质量排除策略声明（MDPI 等）；本次无新增排除项
[done] 来源优先官方仓库/论文/数据集页；稳定论文 URL 缺失一律标 NOT VERIFIED (URL)
[done] 候选按「方法名+venue」去重；代码 URL 为用户原样提供
[done] 每条含 venue/year/source status、paper type(inferred)、relevance rationale
[skipped] 质量打分（insight/completeness/numeric evidence）：非本包职责，且会引入主观数值，改为标签+rescue route
[done] 每条 claim 可追溯至 [U] 材料或标 [I]/[?]
[done] 每个 closest-work cluster 含已覆盖/欠测试/差异化或 rescue route
[done] 数据集候选表、基线表、指标、机会地图、novelty 风险、next module 均已给
[skipped] 标准 literature-search folder（用户指定单文件输出）
Unresolved: 具体 venue、GCN 实现来源、2026 预印本是否覆盖真空白①（需 G3 重搜）、全部论文稳定 URL
No-fabrication: 无新增论文/引用/URL/数值；所有数值均来自用户已核验清单
```
