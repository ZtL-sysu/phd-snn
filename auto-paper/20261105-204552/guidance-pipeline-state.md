# Guidance Pipeline State（可读账本）

canonical 顺序：`CCFA-startup -> G0 -> G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 -> validation -> handoff`
合法状态：`pending | running | passed | blocked | superseded`（无 `skipped`）。
机器可读版本见 `pipeline-state.json`。本轮为 **idea-screening round**，不声称 workflow complete。

| 阶段 | 状态 | 本轮实际动作 | 证据 |
|---|---|---|---|
| CCFA-startup | running | 目标层级/约束/契约已固化为 `execution-contract-v1.md`；idea 卡片、机会图、红队、claim-evidence 正在生成 | `execution-contract-v1.md`, `ccfa-startup-packet/` |
| G0 近期文献与基线图 | passed | 已检索并核验 2024-2026 权威工作与代码/数据状态 | `literature-baseline-matrix.md` |
| G1 公开数据可得性 | passed | MaleCNS 全图 1.1 GB feather 与 train-your-fly/Zenodo 1.3 GB 图数据均为公开直连、CC-BY；cogstim 公开生成刺激 | `dataset-access-log.md` |
| G2 任务与评测有效性 | passed | 颜色/形状/数量辨别与朝向条纹任务有明确标签、可复现 split、准确率主指标 | `dataset-access-log.md`, `literature-baseline-matrix.md` |
| G3 理论契合 | pending（逐 idea 判定） | 每个 idea 卡片内含机制与可证伪消融 | `ideas/idea-cards.md` |
| G4 新颖性/非重复 | running | 已定位 4 个高度相关工作并写出差异化定位 | `prior-art-dedup-log.md` |
| G5 硬件与运行可行性 | passed（本机信封） | RTX 3060 12GB / CUDA 12.8 / `dyg-cold` 环境依赖齐备 | `hardware-profile.md` |
| G6 强基线与消融 | pending | 待选定 idea 后冻结 | — |
| G7 强结果可行性 | pending | 冒烟实验仅作为证据收集，不等价于 G7 pass | `smoke-tests/` |
| G8 顶会故事强度 | pending | 待 CCF 评审与冒烟结果 | `ccfa-review-reports/` |
| validation | pending | 本轮不生成 `guidance.md`，故不运行 `validate_guidance.py` | — |
| handoff | pending | 本轮不交接 `f-research-v1` | — |

## 回溯记录

- 2026-11-05：初始化 v1 契约；确认 CVPR 2027 仅剩 11 天，评审标准按顶会主会执行。
- 2026-11-05：发现直接撞车工作 arXiv 2610.10023（2026-10-08）与 arXiv 2609.01330（NeurIPS 2025），
  全部 idea 必须在 G4 中给出明确定位，否则淘汰。
- 2026-11-05：CCFA-startup 完成 6 份独立 CCF 评审，0 GO / 3 REVISE / 3 淘汰，
  `startup-decision.md` 判 `pivot-with-rescue-route`（非 proceed）。
- 2026-11-05：S0 验证官方 `train-your-fly` 在 `dyg-cold` 可导入可构图，I1 兼容性致命风险解除。
- 2026-11-05：冒烟 I3 两轮真实数据后淘汰；冒烟 I1 首轮失败（NaN / 脉冲稀疏 / 结构无信号，
  主因为前缀子图读出未激活）；I6 成本外推判 mini-benchmark 可行。
  详见 `smoke-tests/results/` 与 `scenario-decision-log.md`。
- 2026-11-05：G3 逐 idea 判定：I1 有条件成立（机制级理由 + 可证伪消融），
  I2/I4/I5 淘汰；G4 对 I1 仍为最高风险项，保持 `running`，未判 passed。
- 本轮结论：不生成 `guidance.md`、不运行 `validate_guidance.py`、不交接 `f-research-v1`；
  G6-G8 / validation / handoff 保持 `pending`，pipeline 未 complete。
