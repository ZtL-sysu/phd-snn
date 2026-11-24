# Path Containment Manifest（P0）

> 生成 2026-11-10｜按 `f-research-v1` 非协商规则：所有本地过程文件与交付物必须在 guidance 目录内的 P0 run root 中。

## 1. 唯一可写根

`C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\`

| 子目录 | 用途 |
|---|---|
| `contracts/` | 契约、输入快照、路径清单、强结果锁、claim-evidence 矩阵 |
| `audits/` | 完整性、数值、引用去重、figure/table、guidance 覆盖等审计 |
| `protocols/` | 数据加载、模型、转换、基线、能耗、统计与运行脚本 |
| `results/` | 每次运行的 JSON/CSV 原始结果、trial ledger、environment 快照 |
| `writing/` | 手稿大纲、草稿、章节包、评审与修订记录 |
| `figures/` | 图源文件与生成脚本 |
| `tex/` | 主 TeX、章节、表格、参考文献与编译产物 |
| `data/` | 公开数据集下载与解析缓存（用于主张的内容已登记哈希） |

## 2. 外部只读引用（不写入，快照已复制进 run root）

| 外部路径 | 角色 | run root 内快照 |
|---|---|---|
| `../guidance-v2.md` | 权威契约 | `contracts/guidance-v2.snapshot.md` |
| `../contract-change-v1-to-v2.md` | 契约变更 | `contracts/contract-change-v1-to-v2.md` |
| `../ccfa-startup-packet/` | v1 CCFA 启动包（decision=proceed） | 仅引用，P1 记录适用性核对 |
| `../literature-baseline-matrix.md` | 文献与基线地图 | 仅引用，P1 记录复用 |
| `../evidence-snapshots/m0-results.json` | v1 M0 恒等式实跑 | 仅引用，P2 复算适用性 |
| `C:\code\phd-snn\auto-paper\20261028-171500\Spiking-GNN-Conversion\f-research-v1-run-20261028-174053-gnn-snn-conv\experiments\core.py` | 1028 核心实现 | `contracts/core-1028.snapshot.py` |
| `C:\code\phd-snn\auto-paper\20261028-171500\Spiking-GNN-Conversion\f-research-v1-run-20261028-174053-gnn-snn-conv\protocols\graph_data.py` | 1028 数据加载参考 | 仅引用 |

## 3. 禁止写入位置

`AutoResearchClaw/artifacts`、`auto-paper/` 根、全局 temp、桌面、下载目录、当前 shell 工作目录、1028 成稿目录、资料库节点、v1 guidance 文件。

## 4. 远程/临时位置

`novix-platform` / `exp-4090` 沙箱若启用，仅作瞬态计算位置；用于主张或交付的结果必须同步进本 run root `results/` 并在 `experiment-traceability.md` 登记。本轮 P0–P5 以本机 3060 为主，未提交远程任务。

## 5. 自检

- P0 时本清单、`pipeline-state.md`、`pipeline-state.json`、`execution-contract-v1.md` 均位于 run root 内。
- 每次新增交付物后复核路径；P21 用 manifest 证明所有本地交付/过程文件均在 `guidance_dir` 下。
