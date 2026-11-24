# CCFA Startup Stage Plan（筛选轮）

目标 venue：CVPR 2027 主会（IEEE/CVF，顶会）。会议 2027-06-20~25，西雅图。
硬日期：注册 2026-11-10 AOE，全文 2026-11-16 AOE，补充材料 2026-11-23 AOE。
当前 2026-11-05，剩余 11 天。来源：https://cvpr.thecvf.com/Conferences/2027/CallForPapers

## 约束

- 方向锁定：GNN + SNN + 果蝇连接组 + 视觉；不得漂到纯神经科学仿真或纯图表示学习。
- 算力：本机单卡 RTX 3060 12 GB / 31.9 GB RAM / Conda `dyg-cold`。无远程算力授权。
- 单次冒烟预算：<= 15 分钟 GPU、<= 10 GB 显存、单份数据 <= 1.5 GB。
- 数据：只允许公开直连（MaleCNS feather / train-your-fly release / cogstim）。

## 阶段与产物负责人

| 阶段 | 决策 | 产物 | 负责人 |
|---|---|---|---|
| CCFA-startup | 是否进入 gate | 本 packet + `execution-contract-v1.md` | 主 agent |
| G0 文献基线 | 硬门槛 | `literature-baseline-matrix.md` | 主 agent（已完成） |
| G1 公开数据 | 硬门槛 | `dataset-access-log.md` | 主 agent（已完成） |
| G2 任务/评测 | 硬门槛 | `dataset-access-log.md` | 主 agent（已完成） |
| G3 理论契合 | 硬门槛 | `ideas/idea-cards.md` 逐 idea 机制段 | 主 agent |
| G4 非重复 | 硬门槛 | `prior-art-dedup-log.md` | 主 agent |
| G5 硬件 | 可修复门槛 | `hardware-profile.md` | 主 agent（已完成） |
| G6 基线/消融 | 可修复门槛 | 待选定 idea 后冻结 | 未开始 |
| G7 强结果可行性 | 可修复门槛 | `strong-result-feasibility-contract.md` + 冒烟日志 | 未开始（本轮仅冒烟，不判 pass） |
| G8 顶会故事 | 终值门槛 | `../ccfa-review-reports/` | CCF 独立评审（部分完成） |
| validation / handoff | — | 本轮不产出 guidance.md | 未开始 |

## 本轮需要的决策

CCF 评审对 6 个 idea 给出 0 个 GO / 3 个 REVISE / 3 个淘汰。需要决定：
1. 是否把 3 个 REVISE 收窄为一条可冒烟的主线；
2. 冒烟实验按什么顺序跑、什么信号触发"换 idea"；
3. 是否诚实告知用户 11 天不足以完成 CVPR 主会全量实验。

## 执行中记录的偏离

标准 `f-guidance-builder-v1` 的 CCFA-startup 应调用 5 个具名 CCFA 子技能
（orchestrator / idea-optimizer / literature-searcher / idea-reviewer / experiment-designer）。
本会话可用技能中只有 `ccf-paper-reviewer` 与 `ccf-integrity-auditor` 实际安装，
其余具名技能不可用；因此按用户"让 CCF 技能打分评审"的指令，
用 3 个独立子代理执行 `ccf-paper-reviewer` standard scientific 评审覆盖
idea-reviewer 与 reviewer-panel 职责，其余职责由本 packet 的文档显式承担，
不冒充未安装的技能输出。
