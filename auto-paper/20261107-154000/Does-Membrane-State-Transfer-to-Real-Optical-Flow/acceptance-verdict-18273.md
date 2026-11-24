# P4 全量实验结果判定 — C1 / novix task 18273（grind attempt #3，正式判定）

判定时间：2026-11-08 13:2x GMT+8（定时任务 round-007 Step 2，接 round-006 PRELIMINARY）
判定依据：C1 `guidance.md` §「Expected Results」预注册条件（`minimum` / `expected_strong` / `failure`）
证据来源：novix exp-4090 任务 `18273` 的**平台终态原文** + **实拉并哈希核验的工作区文件**，
已归档 `f-research-v1-run-20261107-154500-membrane-state-transfer/evidence/p4-novix-18273/`（16 个文件）。
判定口径：只用实测数值，不推断、不补数、不把负结果改成正结果、不把「实验跑完」写成「结果达标」。

## 本轮 Step 0 / Step 2 的严格核验（第三次「声称存在、实拉没有」）

| 核验项 | 结果 |
|---|---|
| `novix --json task result 18273` | rc=0，`status=finish`、`steps=355`、**完整 finalReply**（5650 B），平台标签 `COMPLETED_VALID_DESIGN_EXPECTED_SIGNAL_NOT_MET`，`design_valid=true`、`expected_signal_met=false` |
| 短路径全量 pull `task:18273 → C:/code/phd-snn/_nv18273r7` | 传输 32 min 后 rc=1，原因是**本机 safe-delete 批量确认保护**（1469 个 staged 文件 > 阈值 50），**不是平台故障、不是任务失败、不是 rc=4 传输错误**；staged 工作区完整（71 MB / 1292 文件） |
| 远端 `novix debug ls <session> project -L 2` | **权威确认**：`project/` 下**没有** `result.json`、**没有** `config.json`；有 `experiment.py`（83,526 B）、`evidence/`、`logs/`、`data/` |
| 定向 `--sub` 逐个拉取（rc=0） | 成功归档 15 个证据文件 + 本轮平台 result JSON |
| **`evidence/result_snapshot.json`** | **1,322,902 B，SHA-256 `2c15f8466687d7ef4c572b12748d1bef0b1d7263e9b8437b06be3de1ff691aed`** —— 与 finalReply 声称的 `project/result.json` 字节数与哈希**完全一致**；即数据真实、完整、可复现，只是主文件路径缺失 |
| `evidence/config_preregistered.json` | 14,233 B，SHA-256 `58766f4f…`，与 `result_snapshot.json` 内 `preregistration.config_preregistered_sha256` **一致**（预注册哈希锁定成立）；finalReply 声称的 `project/config.json`（16,314 B）远端不存在 |
| 远端 `evidence/raw` | 685 个 raw NPZ（与 finalReply 一致） |

→ 结论：**`project/result.json` / `project/config.json` 第三次未落在可 pull 工作区**（18156 / 18228 / 18273）。
但**等价的完整结果数据已通过 SHA-256 核验拉回**（`result_snapshot.json` 与声称的 `result.json` 逐字节相同），
因此本轮具备写**正式 verdict** 的证据条件；不因路径缺陷编造或推断任何数值。
该协议缺陷作为 attempt #4 的必改项写入本轮新 query（见 `GRIND-LEDGER.md` 四要素）。

## Verdict: `REJECT_FAILURE`（有效跑完全量、有真实方法数值、命中预注册 failure 条件 / 强信号未达）

**不是** `REJECT_INVALID`（18228 那种 `design_invalid`；本次 `design_valid=true`、readout 已拟合、有全部方法数值），
**不是**平台故障（平台 `finish`、脚本齐全、18/18 测试、440/440 validator、685 raw NPZ、数据已下载），
**不是**科学负结果或机制否证（平台明确「不能表述为方法成功、方法优越或机制已被否证」），
**不是**方法优越、不是迁移成立、**不是结果达标**。

## 逐条对照 C1 guidance §Expected Results

| 预注册条件 | 实测（来自哈希核验的 `result_snapshot.json`） | 是否达成 |
|---|---|---|
| `minimum`: real-domain `delta(LIF − stateless) ≥ +0.15` 且 CI 下界 > 0 | **无 real-domain delta**：DAVIS full-frame v1 ceiling `0.4769 < 0.70` → `unavailable`；Sintel 下载 119342 ms 后仅 350,551,807 / 5,627,783,629 B → `unavailable`。平台 `synthetic_to_real_claim.allowed=false` | **否（不是负结果，是无法判定）** |
| `expected_strong`: real delta ≥ +0.25 + 迁移裁决 + 一因子消融指认承载机制 | 同上；且 SYNTHETIC 侧预注册强对比 `lif_homeostasis_skip − stateless_skip = +0.011667`（CI `[0.00333, 0.02000]`、exact p=0.25、BH q=0.25）**远低于固定门槛 +0.15**，`expected_strong_met=false`；一因子消融全部差值 0 / p=1 / q=1，未指认承载机制 | **否** |
| `failure`: real ceiling < 0.70 / `delta ≤ 0` / CI ≤ 0 / NaN / missing raw evidence | `real ceiling < 0.70` **命中**（0.4769）；`lif_homeostasis − stateless = −0.375 ≤ 0` **命中**；`project/result.json`/`config.json` 主文件缺失（等价 snapshot 已核验存在） | **是（因此不构成可接受结果）** |
| SYNTHETIC ceiling ≥ 0.90 | `1.0`（5 seeds 全 1.0，CI [1.0,1.0]） | 是 |
| 决定性对照 / 消融 / 阴性对照 | A=0 1.0（输入信息上界，非生物接线优势）、保度零模型、identity、skip、drive_every_frame、打乱帧序、flash 全部落盘 | 是（协议层面） |

`expected_strong` 与 `minimum` **均未达成**，且命中预注册 failure 条件 →
**不进 P5、不进 P5A、不写论文、不标任何 pipeline stage passed**。
`pipeline-state.json` 26 阶段仍全 pending、history 为空（本轮未改动）。

## 实测主表（全部来自哈希核验文件 / 平台终态原文，非推断）

| 条件 | Accuracy mean | 读出跨样本 std |
|---|---:|---:|
| `stateless` | 0.875000 | 1.4355e-08 |
| `lif_homeostasis` / `lif_combo` / `lif_drive_every_frame` | 0.500000 | **0** |
| `degree_null_lif` | 0.473333 | 9.0732e-07 |
| `A=0` | 1.000000 | 0.20876 |
| `stateless_skip` / `lif_homeostasis_skip` | 0.988333 / 1.000000 | 非零（composite 0.14462） |
| 结构×动力学 2×2 | biological LIF 0.500000 / std **0**；degree-null LIF 0.506667 / std 9.07e-07；identity LIF 0.506667 / std **0.2075**；A=0 LIF 0.506667 / std **0.00156** | 全格落盘 |
| λ×K 相图 | 20/20 格完成；biological LIF 与 drive-every-frame LIF **所有格 KC std=0**；`directional_structure_supported=false` | 落盘 |
| 一因子消融 | 去 adaptive / refractory / E/I / frozen gain / drive once-every / 打乱帧序 / flash 全部 acc=0.5、KC std=0、差值 0、p=1、q=1 | 落盘 |

**平台「有限推断」要点（原文口径）**：严格零方差 collapse 最迟发生在
biological graph + hard-spike → resolved KC readout 路径；每帧重注入输入未恢复方差；
residual skip 只保留绕过图传播的输入信息、未修复 graph-KC 分支；
**identity / A=0 LIF 方差非零但准确率仍 ≈chance → 「严格零方差」与「标签信息丢失」不是同一现象**；
当前测量不能证明所有隐藏节点收敛到唯一数学固定点，也不能简单归因于「只有图结构」或「只有膜动力学」。

## 对 round-006 attempt #4 预案假设的实测裁定（如实记录）

round-006 由 18228 恒值 `0.04742586985230446 ≈ sigmoid(-3)` 推导的假设
「LIF 分支 `v ≡ 0`，输入注入 / 突触电流 / 膜状态递推被**整体旁路**」——
**被 18273 的 2×2 实测部分否证**：identity LIF std 0.2075、A=0 LIF std 0.00156 非零，
说明 LIF 代码在那些图上是运行的，不是整体旁路；严格零方差是
**biological-graph × hard-spike 门控 → resolved KC readout** 的特异现象。
→ 该预案**不得原样启用**，round-007 必须基于实测修订假设（见 `GRIND-LEDGER.md` 四要素与本轮新 query）。
**不下调 `expected_strong`、不删失败证据、不把部分否证写成假设成立。**

## 交接

- `primary_focus = C1` 锁定不变；`abandon_allowed = False`；本轮按 §3.6(2) 继续同一 idea 的 correction loop。
- 本次失败是**有效性 / 外部效度失败**（两真实域 unavailable + 预注册强信号未达门槛），
  平台明确不能表述为机制已被否证 → **不计入 kill criteria 独立触发**（维持 0/2）。
- 归档清单：`evidence/p4-novix-18273/`（`result_snapshot.json`、`main_table.csv`、
  `probe_vs_hop.csv`、`variance_trajectory.csv`、`lambda_K_phase.csv`、
  `structure_dynamics_2x2.csv`、`config_preregistered.json`、`experiment-traceability.csv`、
  `protocol_correction_before_training.json`、`data_manifest*.json`、`environment.json`、
  日志、`platform-finalReply.md`、`platform-result.json`、`platform-result-round007.json`）。
