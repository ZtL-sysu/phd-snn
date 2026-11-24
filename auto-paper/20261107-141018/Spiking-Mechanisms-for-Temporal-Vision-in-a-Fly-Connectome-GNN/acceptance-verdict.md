# Acceptance verdict — novix task 17682

**Verdict: `REJECT_INVALID`**（无效运行；不是负结果，也不是成功）
判定时间：2026-11-07 14:55 GMT+8
判据：`guidance.md` §6 的前置有效性条件与四种 verdict 定义。

## 平台与回收事实（实测）

| 项 | 值 |
|---|---|
| 平台状态 | `finish`（`novix --json task result 17682`，steps 40） |
| 工作区 | `novix debug ls task:17682` 可见；`debug pull` 退出码 4（后端读超时），部分产物落在 `novix/pulled/.novix-pull.*/workspace/` |
| 远程进度 | `progress.md` 仅 `[x] Setup and hardware report`；数据、实现、5-seed 实验、QA 四项均 `[ ]`；Results log 原文 "Pending experiment run. Do not infer or fill numerical results before execution." |
| 远程 `project/` 目录 | **0 个文件** |
| `experiment.py` | **不存在** |
| `result.json` | **不存在**（整个 pull 目录 0 个） |
| 远程硬件（实测） | RTX 4090 46,068 MiB / 驱动 580.126.09 / CUDA 13.0 / torch 2.11.0+cu130 / `cuda.is_available()=True` |
| trajectory | 40 events、20 tool calls、0 error-looking messages；末步在探测 Zenodo 注释表/坐标表列名 |

详见 `novix/failure-diagnostics.md`（命令原始输出与加固建议）。

## 逐条对照 guidance.md §6 前置有效性

| 前置条件 | 实测 | 结论 |
|---|---|---|
| 帧堆叠天花板 ≥ 0.90 | 未测量 | **不满足** |
| stateless 与 A=0 ≤ 0.60 | 未测量 | **不满足** |
| 5 seeds 全部完成 | 0 seeds | **不满足** |
| 无 NaN | 无数据 | **不满足** |
| `experiment.py` + `result.json` 已拉回且可检视 | 均不存在 | **不满足** |

任一不满足即 `REJECT_INVALID`。因此：
- 不计算 `lif_combo − stateless`、不计算 bootstrap CI、不判 `ACCEPT_STRONG` / `ACCEPT_MINIMUM_ITERATE`；
- `REJECT_NEGATIVE` 也不成立——那需要一次有效但为负的实验，本次连实验都没跑；
- **不授权本机 `f-research-v1` 任何写作阶段**，不产出 paper.tex/PDF，不编造任何数值或 Overall。

## 为什么任务 `finish` 却没有结果（实测 / 推断分离）

- **实测**：`status=finish`，但工作区只有硬件报告、依赖安装与 git 初始化；
  agent 在探测数据列名时停止，未进入实现与实验阶段。
- **推断（未证实）**：该任务按 v1 口径提交，带了 `--max-turns 12 --timeout 3600`；
  40 events / 20 tool calls 处终止可能与步数上限或平台侧默认限制有关，
  但现有日志**不能证明因果**，故不写死为结论。
- **无论原因**：按用户 2026-11-07 14:34 指令，后续一律不传任何预算参数，
  任务跑到平台自己的终态，结果由后续轮次跨轮回收。

## 下一步（`next_action = ITERATE_NEW_IDEA`）

1. 保留本次全部证据（trajectory、progress.md、pull 日志、本判定与诊断），
   不删除、不改写成正结果。
2. 下一轮 6 小时定时任务 Step 0 读到 `VERDICT_REJECT_INVALID` 后，
   由 f-guidance 重新细化方案，用**新设计 + 无预算参数**提交，不重复提交同一实验配置。
3. 新 query 需加固：数据获取与列名校验前置、依赖显式安装、
   **在任何提前终止前先落盘 `experiment.py` 与阶段性 `result.json`**、
   最终回复必须给出实际数值而非只汇报进度。
4. 只有新任务拉回有效 `result.json` 且按 §6 判 `ACCEPT_STRONG`，才启动本机 f-research 写作链。
