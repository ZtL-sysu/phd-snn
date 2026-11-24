# Guidance Pipeline State（可读台账）

> Canonical 顺序（`assets/pipeline-definition.json`）：`CCFA-startup → G0 → G1 → G2 → G3 → G4 → G5 → G6 → G7 → G8 → validation → handoff`
> 合法状态：`pending / running / passed / blocked / superseded`；**无 `skipped`**。
> 机器权威为 `pipeline-state.json`；本文件是其可读视图。哈希与校验器只证明结构一致性，不证明科学正确性。

## 1. 顺序完整性声明

- 本台账在 **CCFA-startup 商议开始之前**创建（初始 12 门全 `pending`），随后逐门 `--before` 校验、逐门记录 `passed`。
- **场景更换与 repair**：rev1 场景在 CCFA-startup 被第 1 轮独立红队判 `blocked`（3 条 fatal）→ 未进入 G0。rev2 是 **repair**，从 `CCFA-startup` 重新起算，依次重跑三轮独立评审、M0 实跑与协议成文，之后才由 `startup-decision.md`（终版 v3）判 `proceed` 并进 G0。**没有用旧证据把后置门标记通过**。
- 第 1 轮 `blocked` 记录保留在 `ccfa-startup-conflict-resolution.md` 与 `scenario-decision-log.md`；三轮评审原文与分数一字未改。

## 2. 12 门逐门记录

| # | Stage | Status | Gate verdict | 实质证据 | `inputs` | `--before` 结果 |
|---:|---|---|---|---|---|---|
| 1 | `CCFA-startup` | **passed** | pass | `ccfa-startup-packet/` 7 工件 + 3 份独立红队 + `idea-cards-rev2.md`；`startup-decision.md` 终版 `proceed (conditional)` + H1–H9 | `execution-contract-v1.md`、`idea-cards-rev2.md`、`idea-red-team-review.md` | `--before G0` PASS |
| 2 | `G0` | **passed** | pass | `literature-baseline-matrix.md`（6 must-rerun / 3 adaptation / literature-context；纠正 FTBC 全称与 QCFS 年份） | `literature-baseline-matrix.md` | `--before G1` PASS |
| 3 | `G1` | **passed** | pass | `dataset-access-log.md`（5 组直链实测、G2 排除清单、NOT VERIFIED 清单） | `dataset-access-log.md` | `--before G2` PASS |
| 4 | `G2` | **passed** | pass | `matched-protocol.md` §4–§5（主/次/proxy 指标、5 seeds + bootstrap + BH、split 预注册、test 隔离） | `matched-protocol.md` | `--before G3` PASS |
| 5 | `G3` | **passed** | pass | `theoretical-feasibility-audit.md` + `evidence-snapshots/m0-results.json`（恒等式 `9.88e-15`、上界 0 违反、P3 `0.3056→0.3111`、失效边界 `0.7058`/`1.1669`）；**H2 硬前置** | `theoretical-feasibility-audit.md`、`evidence-snapshots/m0-results.json` | `--before G4` PASS |
| 6 | `G4` | **passed** | pass-with-narrowing | `novelty-feasibility-report.md` + `literature-baseline-matrix.md` §4（7 条最近邻、3 处真空白、降档 Q1–Q2） | `novelty-feasibility-report.md` | `--before G5` PASS |
| 7 | `G5` | **passed** | pass | `hardware-profile.md`（3060/CUDA/torch/磁盘实测、M0 smoke、缩放策略、G6 blocker） | `hardware-profile.md` | `--before G6` PASS |
| 8 | `G6` | **passed** | pass | `matched-protocol.md` §6–§7（第 0 批 PASCAL/TPP must-rerun、A1–A7 消融、S2 硬回退） | `matched-protocol.md` | `--before G7` PASS |
| 9 | `G7` | **passed** | pass | `ccfa-startup-packet/strong-result-feasibility-contract.md`（三档预注册目标、M0–M4、5 seeds、S1–S7）；**全部非实测** | `ccfa-startup-packet/strong-result-feasibility-contract.md` | `--before G8` PASS |
| 10 | `G8` | **passed** | pass | `story-strength-audit.md`（挑剔审稿人、最强增量威胁、决定性实验、强论文阈值、诚实低档故事） | `story-strength-audit.md` | `--before validation` PASS |
| 11 | `validation` | **passed** | pass | `guidance.md` 通过 `validate_guidance.py --strict --packet`；`ccfa-startup-packet/feasibility-contract.json` 哈希绑定 7 工件；`guidance-pipeline-state.md` 与 JSON 一致 | `guidance.md`、`ccfa-startup-packet/feasibility-contract.json` | `--before handoff` PASS |
| 12 | `handoff` | **passed** | pass | `auto-paper/generated-research-directions.md` 追加一行；`delivery-readiness.json` 记录 `preparation / submission_ready=false`；交接点明确 | `delivery-readiness.json` | `--workflow-complete` PASS |

## 3. 失败与回退记录（全部保留，未删除）

| 事件 | 阶段 | 处置 |
|---|---|---|
| CCFA 第 1 轮独立红队 `pivot-with-rescue-route`（2.5/5，F1/F2/F3 三条 fatal） | `CCFA-startup` | `blocked` → 不进 G0；按最小可行修复路线做 problem-refinement |
| CCFA 第 2 轮（3.2/5，F1 已解，F2/F3 降级） | `CCFA-startup` | 继续 repair：补 M0 实跑、成文 `matched-protocol.md`、核对成稿原文 |
| CCFA 第 3 轮（3.4/5，0 未解 fatal，建议 conditional proceed） | `CCFA-startup` | 记 `passed`，附 H1–H9 |
| startup 包撰写员初版 `startup-decision.md` 在无红队结论时写 `proceed` | `CCFA-startup` | **整体作废**，由终版 v3 取代；见 `ccfa-startup-conflict-resolution.md` |
| M0 初版 P3 每 ρ 重采样 problem、SHA 用内存字符串 | `G3` | 第三轮红队指出后**实际修正并重跑**；权威哈希改为磁盘字节 `ea4c05a6…`；P3 干净隔离后 `0.3056→0.3111` |
| S1 / S3 场景 | `CCFA-startup` 前的场景筛选 | 拒，降为对照臂；不推进、不删记录 |

## 4. 与 `pipeline-state.json` 的一致性

- 12 个 stage 的 `id` 顺序、`status`、`gate_verdict`、`contract_version` 与上表一致。
- `history` 恰为 12 条 `{"action":"pass","stage":...}`，按 canonical 顺序；无伪造 `reopen`。
- `contract` 绑定 `execution-contract-v1.md`（不可变）；`readiness` 恰好一条，绑定 `delivery-readiness.json`。
- 每个 `passed` stage 的 `inputs` 与 `evidence` 均为非空哈希清单，且所有文件在 run root 内、非空、哈希正确。

## 5. 交付状态

- `workflow_complete`：**true**（所有本地阶段按顺序真实执行或由仍然适用的不可变证据重新接受）
- `submission_ready`：**false**（作者/投稿/发布/venue 官方规则等待决项，见 `delivery-readiness.json`）
- 下游交接：`f-research-v1` 从 `guidance.md` 的契约抽取开始；P4 全量实验按 `novix-platform` 流程派 `exp-4090`（用户已授权但本轮未提交）。`f-guidance-builder-v1` 明确不在此运行实验、不写论文。
