# Execution Contract v1（不可变）

- 版本：`v1`，生成时间：2026-11-05 20:45 (GMT+8)
- 运行根：`C:\code\phd-snn\auto-paper\20261105-204552`
- 主技能：`f-guidance-builder-v1`；评审技能：`ccf-paper-reviewer`

## 1. 用户目标（原话要点）

> 创建一个新文件夹，研究 GNN + 果蝇大脑 + SNN，做视觉方向，目标冲刺 CVPR 2027；
> 参考 Google Research 完整雄性果蝇脑连接组博客与 `cobanov/awesome-fly`；
> 先用技能多想几个 idea，每想出一个就用 CCF 技能打分评审，有搞头的做冒烟实验，
> 实验不理想就换 idea。大方向：GNN、SNN、果蝇连接组、视觉。

## 2. 授权范围（本轮）

允许：本地文件读写、公开网络检索、公开数据下载、在本机 Conda 环境运行轻量冒烟实验、
生成 idea 卡片与评审报告、可视化汇总、写入工作区记忆日志。

不允许：远程/云上训练（未授权）、任何需要账号审批/IRB/NDA 的数据、
代用户提交论文或注册 OpenReview、伪造实验结果或引用、把预测结果写成已观测结论。

## 3. 相对技能默认的显式偏离（用户指令优先）

`f-guidance-builder-v1` 的标准终点是产出 `guidance.md` 并交接 `f-research-v1`，且声明
"Do not run experiments here"。本轮用户明确要求 **idea 生成 → CCF 逐个打分 → 冒烟实验 →
不理想换 idea** 的筛选循环。因此：

- 本轮定位为 **idea-screening round（选题筛选轮）**，不是完整 guidance build。
- 运行根直接是 `auto-paper/<timestamp>/`，**不**创建 paper-title 子文件夹——因为论文题目尚未选定；
  选定后将另起一个带标题的目录重新走完整 canonical gates 并生成 `guidance.md`。
- 冒烟实验作为用户额外授权的证据收集动作，**不冒充 G7/G8 通过**。
- G6-G8、validation、handoff 在本轮保持 `pending`，不伪造 pass。
- 36 篇引用 / 严格近期多数的文献要求属于最终 guidance 阶段，本轮不声称满足。

## 4. 硬约束（必须在评审中生效）

- **CVPR 2027 时间线**：Paper Registration 2026-11-10 AOE；Submission 2026-11-16 AOE
  （北京时间 11/17 19:59）；Supplementary 2026-11-23；会议 2027-06-20~25 西雅图。
  来源：https://cvpr.thecvf.com/Conferences/2027/CallForPapers （访问 2026-11-05）。
  距本轮仅 **11 天**；2026-09-15 之后上线的论文按 CVPR 规则视为 contemporaneous，
  不构成直接拒稿理由但必须引用讨论（arXiv 2610.10023 属此列）。
- 目标 venue 层级：CVPR 主会（Q1/顶会）。评审须用顶会标准，不能用"期刊 Q2"标准放水。
- 大方向锁定：GNN + SNN + 果蝇连接组 + 视觉。不得漂到纯神经科学仿真或纯图表示学习。

## 5. 资源与运行信封

- 本机 Windows 11，12 逻辑核，NVIDIA RTX 3060 12 GB，CUDA 12.8，磁盘空闲 ~547 GB。
- 代码必须在**本机 Conda** 里跑（用户长期偏好）。候选：`dyg-cold`（torch 2.11+cu128 /
  PyG 2.8.0.post1 / spikingjelly / cv2 齐备）、`base`（PyG + spikingjelly + cv2）、
  `spikinggcn36`（Py3.6 + spikingjelly，仅备用）。
- 冒烟实验预算：单次 <= 15 分钟 GPU，显存 <= 10 GB，数据下载 <= 1.5 GB，
  不做完整训练/多种子大实验。远程算力为 opt-in，本轮不用。

## 6. 输入清单（已核验的公开来源）

| 输入 | URL | 访问日 |
|---|---|---|
| Google Research 博客（MaleCNS） | https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain | 2026-11-05 |
| awesome-fly 列表 | https://github.com/cobanov/awesome-fly | 2026-11-05 |
| MaleCNS 官方下载页 | https://male-cns.janelia.org/download/ | 2026-11-05 |
| train-your-fly README | https://github.com/eudald-seeslab/train-your-fly | 2026-11-05 |
| connectome（论文实验仓库）README | https://github.com/eudald-seeslab/connectome | 2026-11-05 |
| cogstim README | https://github.com/eudald-seeslab/cogstim | 2026-11-05 |
| flyvis | https://github.com/TuragaLab/flyvis | 2026-11-05 |
| CVPR 2027 CFP | https://cvpr.thecvf.com/Conferences/2027/CallForPapers | 2026-11-05 |

## 7. 质量要求

- 每个 idea 必须有机制级理由、可证伪消融、公开数据/任务/指标、强基线。
- CCF 评审必须给出：criterion score、overall stance、confidence、证据依据、
  扣分原因与加分条件；<=3 分必须写清扣分与修复条件。
- 冒烟实验必须记录真实 stdout/stderr、指标、失败信号；失败即淘汰并记录，不许事后改写目标。
- 所有数字与链接必须可追溯到本轮检索记录，不得编造。
