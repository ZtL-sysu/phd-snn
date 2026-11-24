# Literature & Baseline Matrix（G0 / G6）

> 核验日期 2026-11-10｜由独立文献核验 Agent 用 WebSearch/WebFetch 实际检索；所有 URL 均来自检索结果，未构造。
> 不确定的字段一律写 `NOT VERIFIED`。第三方摘要页的数值与官方摘要严格分开标注。
> 角色定义：`must-rerun` / `adaptation-attempt` / `internal-matched` / `oracle/upper-bound` / `literature-context`。

## 0. 两处题面纠正（已按官方页核实）

- **FTBC 全称是 "Forward Temporal Bias Correction"**（不是 Free Timestep Budget Calibration），arXiv:2403.18388 / ECCV 2024 / Springer LNCS 一致。
- **QCFS 正式 venue 是 ICLR 2022**，但 arXiv:2303.04347 预印本提交于 2023-03-08；引用写 Bu et al., ICLR 2022，预印本年份 2023，勿混。

## 1. 第一梯队 · must-rerun（官方代码已核验 + 权威 venue + 可直接比较）

| 方法 | 年份 / Venue | 官方 URL | 代码 / checkpoint | 数据集与 T | 官方关键数值（仅检索到的） | 3060 12GB 可行性 | 角色 |
|---|---|---|---|---|---|---|---|
| **QCFS** (Bu et al.) | ICLR 2022（arXiv 2023） | `arxiv.org/pdf/2303.04347.pdf`、`arxiv.org/html/2303.04347v1`、DOI `10.48550/arXiv.2303.04347` | `github.com/putshua/SNN_conversion_QCFS`；checkpoint NOT VERIFIED | CIFAR-10/100、ImageNet；VGG-16 / ResNet-18/20/34；T=1…≥1024 | CIFAR-10 VGG-16 **91.18%@T=2、93.96%@T=4**；CIFAR-100 69.62%@T=4；ImageNet ResNet-34 59.35%@T=16（官方 arXiv HTML 结果表） | ✅ 锚点；**先做回归测试锁定统一环境**；torch 2.11 兼容性 NOT VERIFIED | `must-rerun`（锚点 + 源激活） |
| **FTBC** (Wu, Bojković, Gu, Suo, Zou) | ECCV 2024, LNCS Part LXIX pp.155–173, DOI `10.1007/978-3-031-72890-7_10` | `arxiv.org/abs/2403.18388`、`eccv2024.ecva.net//virtual/2024/poster/437` | `github.com/shizukanaskytree/FTBC`（含 QCFS/RTS/SNNC 基线目录，2 commits，2024-09-24）；checkpoint NOT VERIFIED | CIFAR-10/100、ImageNet；VGG-16 / ResNet-34；低 T 改善最显著 | 叠加 QCFS 后 ImageNet VGG-16 **@T=2 由 1.50%→41.10%**、ResNet-34 4.91%→30.10%（官方 arXiv HTML §5.2/Table 5） | ✅ 纯前向校准、零训练开销、最省显存 | `must-rerun` |
| **TPP / Temporal Misalignment** (Bojković, Wu, Gu) | ICML 2025, PMLR 267:4791–4822 | `arxiv.org/abs/2502.14487`、`proceedings.mlr.press/v267/bojkovic25a.html`、`icml.cc/virtual/2025/poster/45627` | `github.com/shizukanaskytree/TPP-SNN`（官方 PMLR PDF 内）；checkpoint NOT VERIFIED | CIFAR-10/100、CIFAR10-DVS、ImageNet；T=4,8,16,32,64 | 官方 PMLR PDF Fig.1：VGG-16/ImageNet **T=4 QCFS 4.67%→TPP 68.39%**、T=8 19.03%→72.98%；**图注 ANN 74.29% 与表内末列 70.00 不一致，已标注** | ✅ ICML 权威 + 官方码；与 FTBC 同作者/代码风格 | `must-rerun`（**第 0 批，最近邻**） |
| **Parallel Spiking Conversion** (Hao et al.) | ICML 2025, PMLR 267 Art.864 pp.22103–22115 | `arxiv.org/abs/2412.13610v2`、`icml.cc/media/icml-2025/Slides/44986.pdf` | `github.com/hzc1208/Parallel_Conversion`（arXiv HTML / ACM DL / PMLR PDF 三处一致）；checkpoint NOT VERIFIED | CIFAR-10/100、ImageNet-1k；VGG/ResNet 系列；T=2…64，仿真步 T̃=4/8/16 | **72.90% top-1 ImageNet / ResNet-34 @T=4**（官方 arXiv HTML 摘要 + Table 3）；VGG-16 73.92%@T=8；19×–38× 加速 | ✅ 并行计算省显存省时 | `must-rerun` |
| **DCGS / Differential Coding** (Huang, Fang, Bu, Hao, Yu, Huang et al.) | ICML 2025, Poster 45408 | `arxiv.org/abs/2503.00301`、`icml.cc/virtual/2025/poster/45408` | `github.com/h-z-h-cell/ANN-to-SNN-DCGS`（arXiv 摘要/ICML poster/mlanthology 三处一致） | ImageNet/COCO/PascalVOC；ViT-S/L、EVA02-L；T=4,8,16 | 官方摘要**未列具体数值 → NOT VERIFIED**；第三方 Lacuna 页数字须回原文核对，不采信 | ✅ 只跑 CNN 子集；ViT-Large 在 12GB 上不保证 | `must-rerun`（CNN 子集） |
| **AdaFire / Adaptive Calibration** (Wang et al.) | AAAI 2025, Art.177 pp.1583–1591, DOI `10.1609/aaai.v39i2.32150` | `arxiv.org/abs/2311.14265`、`dlnext.acm.org/doi/10.1609/aaai.v39i2.32150` | `github.com/bic-L/burst-ann2snn`（ACM DL 参考文献栏）；checkpoint NOT VERIFIED | CIFAR-10/100、ImageNet、CIFAR10-DVS、3D/检测/分割；VGG-16 | 节能 70.1%/60.3%/43.1%（官方 AAAI 摘要）；VGG-16 ImageNet 73.46%@5.72T 等数值来自第三方 Lacuna 且互相冲突，**不采信** | ✅ training-free，只跑分类子集 | `must-rerun`（分类子集） |

## 2. 第二梯队 · adaptation-attempt（权威但无官方代码，须自行复现）

| 方法 | 年份 / Venue | 官方 URL | 代码状态 | 关键数值 | 复现要点 | 角色 |
|---|---|---|---|---|---|---|
| **PASCAL** (Ramesh, Srinivasan) | TMLR 2025 | `arxiv.org/abs/2505.01730`、`openreview.net/forum?id=kIdB7Xp1Iv` | **NOT VERIFIED（无官方码）** | ResNet-34 ≈74% ImageNet；timesteps 减少 64×（arXiv 摘要）/ 56×（TMLR 周刊版，**两版冲突**）；官方 PDF 指出 QCFS 在 CIFAR-100/ImageNet 需 ~1024 T 才匹配 ANN | 抑制性（负）脉冲 + 逐层量化步 L 敏感度搜索；需重训 QCFS-ANN | `adaptation-attempt`（**第 0 批，确定性精确计数最近邻**） |
| **CS-QCFS** (Yang et al.) | Neural Networks 184:107076, 2025, DOI `10.1016/j.neunet.2024.107076` | `sciencedirect.com/science/article/pii/S0893608024010050`、`ai.nju.edu.cn/rinc/publish/download/2025/csqcfs.pdf` | **NOT VERIFIED（无公开仓库）** | **95.86% CIFAR-10 / 74.83% CIFAR-100 @T=1**（PubMed/ScienceDirect 官方摘要）；实验在 RTX 2080Ti、111.81 s/epoch（南大官方 PDF） | 逐通道可训练阈值 + Softplus 保证恒正；需重训源 ANN | `adaptation-attempt` |
| **ECL / Error Compensation Learning** | arXiv 2025（**正式 venue NOT VERIFIED**；ScholarFeed 打 ICML 标签无官方确认，不采信） | `arxiv.org/abs/2506.01968v1` | **NOT VERIFIED** | **94.75% CIFAR-10 / ResNet-18 @T=2**（官方 arXiv 摘要） | 可学习裁剪 + 双阈值神经元 + 膜电位初始化优化；需重实现并训练 | `adaptation-attempt` |

## 3. 文献对照 · literature-context（只进 related work，不进主比较表）

| 方法 | 年份 / Venue | 官方 URL | 为什么不重跑 |
|---|---|---|---|
| Diehl et al. weight/threshold balancing | IJCNN 2015, DOI `10.1109/IJCNN.2015.7280696` | 官方 IEEE Xplore 页 NOT VERIFIED；仅聚合页 | 无代码、无现代框架实现；仅作归一化思想引文 |
| Rueckauer et al. | Front. Neurosci. 11:682, 2017, DOI `10.3389/fnins.2017.00682` | `frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2017.00682/full` | 概念基石；soft reset 已被后续方法内置 |
| Sengupta et al. SpikeNorm | Front. Neurosci. 13:95, 2019 | `arxiv.org/abs/1802.02627` | T=2500 级，与低时延议题不对齐 |
| RMP-SNN / soft reset (Han et al.) | CVPR 2020 | `arxiv.org/abs/2003.01811`、`openaccess.thecvf.com/content_CVPR_2020/papers/Han_RMP-SNN_...pdf` | soft reset 已是所有现代转换默认组件 |
| SpikeConverter | AAAI 2022 | `aaai.org/AAAI22Papers/AAAI-364.LiuF.pdf` | 8–16 T 已被 2024–25 的 1–4 T 超越；无代码 |
| One-Spike SNN (Hwang, Kung) | IEEE TETC 13(1):162–172, 2025；预印本 arXiv:2403.08786 (2024) | `arxiv.org/abs/2403.08786`、DOI `10.1109/TETC.2024.3386893` | **重要 novelty 锚点**：已跨 CNN+GCN（GCN 文本分类平均 loss 0.90%、能效 4.6–17.3×，T=16/24）；相位编码路线，无官方码 |
| Adaptive Fission | NeurIPS 2025 | `openreview.net/forum?id=2zZzdAMyYi` | 硬件导向、无代码；作"空间换时间"对照引文 |
| RMP-Alignment (Chen et al.) | arXiv 2026 预印本（venue NOT VERIFIED） | `arxiv.org/abs/2608.13952` | 2026 新预印本、无代码、无官方数值、需重训 |
| GTDL + Codebook State Alignment | IEEE DLCV 2026, DOI `10.1109/DLCV69906.2026.11635228` | `xplorestaging.ieee.org/document/11635228/figures` | 新会议论文、无代码无数值；关注项 |
| 中文 RMPE + 两阶段微调 | 《控制理论与应用》2025, 42(3), DOI `10.7641/CTA.2024.30012` | 中文期刊页 | 数值来自第三方转述；思路可引，不重跑 |
| **Deng & Gu** | ICLR 2021 | 本轮独立核验结论（URL 未在本矩阵核验，标 NOT VERIFIED） | **novelty 锚点**：`β*=θ/(2T)` 与逐层误差递归已被占 |
| **Dual-Phase** | IEEE TNNLS 2024 | 同上 | **novelty 锚点**：膜电位解码 + 精确误差等式已被占 |

## 4. 最近邻 novelty 重叠表（G4，来自独立核验）

| 前作 | 年 / Venue | 已占据什么 | 重叠 | 对我们的约束 |
|---|---|---|---|---|
| Deng & Gu | ICLR 2021 | `β*=θ/(2T)`、逐层误差递归 | `duplicate`（该组件） | 不得声称发明 β* |
| QCFS / FTBC | ICLR 2022 / ECCV 2024 | 零期望误差偏置 | `high` | 必比基线；不得声称发明零期望偏置 |
| Dual-Phase | TNNLS 2024 | 膜电位替代计数读出 + 精确误差等式 | `duplicate`（该组件） | 不得声称发明解码或精确等式 |
| PASCAL | TMLR 2025 | 确定性精确计数 | `high` | 第 0 批必跑；确定性化须显示可测增益 |
| TPP / SpikeConverter | ICML 2025 / AAAI 2022 | 两阶段框架 | `high` | 第 0 批必跑；不得声称发明两阶段 |
| One-Spike SNN | IEEE TETC 2024/25 | 跨 CNN + GCN 转换 | `high` | "跨骨干"不新；差异化必须落在算子级误差刻画与统一协议 |
| Parallel / DCGS / AdaFire | ICML'25 / ICML'25 / AAAI'25 | 2025 主流转换 | `medium`（横评对手） | 构成统一协议必须对齐的基线集合 |

**G4 结论：`pass-with-narrowing`**。剩余可辩护贡献 = ① 固定线性算子类上的层类型无关精确统一（须由 G3 证明其非平凡性）；② 特定确定性化相对 PASCAL/TPP 的可测增益；③ 首次冻结图视觉骨干与图消息传递的统一协议横评 + 失效边界。**不得声称发明上述任何数学组件**，且目标档位按 IEEE TNNLS / Q1–Q2 期刊档。

## 5. 直接重跑可行性结论

- **必须直接重跑（第一批之前先锁环境）**：QCFS（回归测试 91.18%@T=2 / 93.96%@T=4）→ FTBC → Parallel → DCGS(CNN 子集) → AdaFire(分类子集)。
- **第 0 批最决定性**：PASCAL（自行复现）+ TPP（官方码）。二者任一未跑通，按 `matched-protocol.md` §8 S2 转 `needs-evidence`，不得进主表。
- **环境风险**：6 个官方仓库建于 2022–2025，torch 2.11 兼容性全部 `NOT VERIFIED`；checkpoint 可得性全部 `NOT VERIFIED`。先统一 env 并以 QCFS 回归测试为准。
- **ImageNet 处理**：本轮不做全量（G2）。文献中的 ImageNet 官方数值仅作背景，不作本协议下的对照阈值。

> 本矩阵所有 URL、年份、数值来自 2026-11-10 独立检索；未找到的字段一律 `NOT VERIFIED`，无编造。
