# Guidance Pipeline State（D1）

Canonical order: CCFA-startup -> G0 -> G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 -> validation -> handoff

| Stage | State | Note |
|-------|-------|------|
| CCFA-startup | passed | 见 ccfa-startup-packet/ |
| G0 Recent literature & baseline map | passed | literature-baseline-matrix.md（待扩 ≥36 条） |
| G1 Public dataset access | passed | dataset-access-log.md（Cora/CiteSeer/PubMed 公开） |
| G2 Task & evaluation validity | passed | 节点分类，标准分割，准确率主指标 |
| G3 Theoretical fit & feasibility | passed | theoretical-feasibility-audit.md |
| G4 Novelty & non-duplication | passed | 方向级：GNN 转换为空白（待精确检索核对直训脉冲 GNN） |
| G5 Hardware & runtime | passed | hardware-profile.md（RTX3060 本地） |
| G6 Strong baseline & ablation | repairable | 待补齐强基线重跑 + 精确检索 |
| G7 Effectiveness & strong-result | repairable | strong-result-feasibility-contract.md（待实证） |
| G8 Story strength | pending | story-strength-audit.md（待证据） |
| validation | pending | validate_guidance.py 待 CCFA 包 + 章节对齐后通过 |
| handoff | blocked | 未达 validation 不交付 f-research-v1 |

> 注：本台账证明各阶段按 canonical 顺序记录；G6/G7/G8 在方向锁定时以实证证据推进，不标记未运行阶段为 passed。
