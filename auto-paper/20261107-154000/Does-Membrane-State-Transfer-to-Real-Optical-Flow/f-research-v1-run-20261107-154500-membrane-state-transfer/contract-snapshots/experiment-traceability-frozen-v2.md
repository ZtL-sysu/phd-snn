# P4 全量实验 traceability（round 001，主攻 C1）

> 本表是 `guidance.md` Experiment Plan 的逐行检查表。P4 未全部 `done` 之前不得进 P5。
> 当前状态：**P4 实验已派发到 novix exp-4090，结果尚未回收**。所有行均为 `pending`，
> 没有任何观测数值。远程任务完成后按 Step 0 拉回 `result.json`，再逐行回填。

| Guidance requirement | Required artifact | Minimum success check | Strong success check | Status |
|---|---|---|---|---|
| 远程硬件与环境报告 | `evidence/hardware.json` | GPU / 显存 / CUDA / torch 记录 | 与 4090 46,068 MiB 一致 | pending |
| 公开数据可达性与列名校验 | `evidence/data_access.json` | 三个 Zenodo 文件 + DAVIS 直链状态 | DAVIS ZIP 解压并列名核对 | pending |
| 真实域天花板与标签派生 | `evidence/real_ceiling.json` | ceiling >= 0.70 + 派生脚本 | ceiling >= 0.85 | pending |
| SYNTHETIC 域天花板 | `evidence/synthetic_ceiling.json` | ceiling >= 0.90 | ceiling >= 0.95 | pending |
| 主比较（2 域 × 5 条件 × 5 seeds） | `evidence/main_table.csv` | 每格 5 seeds，无 NaN | real delta >= +0.25 且 CI 下界 > 0 | pending |
| 一因子机制消融 | `evidence/ablation.json` | 每个新增机制移除一次 | 指名承载机制且 CI 下界 > 0 | pending |
| 保度零模型对照 | `evidence/null.json` | 带符号如实报告 | 真实图胜出仅当 CI 下界 > 0 | pending |
| A=0 与 stateless 控制 | `evidence/main_table.csv` | 两者均记录、无 NaN | 5 seeds 全部复现 | pending |
| 统计检查 | `evidence/stats.json` | bootstrap 95% CI、BH q=0.05 | 预注册方向成立 | pending |
| spike rate / feature std | `evidence/diagnostics.json` | 每条件非空 | 方差变化由机制解释 | pending |
| 鲁棒性（帧率 / 光流幅度分桶 / PCA 维数） | `evidence/robustness.json` | 至少两项完成 | 结论在分桶下稳定 | pending |
| 效率（显存 / 耗时） | `evidence/efficiency.json` | 峰值与 wall time 记录 | 与 guidance 预算一致 | pending |
| 复现元数据 | `evidence/run_manifest.json` | task id / seeds / config / script | 拉回脚本可本机重跑 | pending |

## 派发信息

- 远程池：`exp-4090`，命令不带 `--max-turns` / `--timeout`（用户 14:34 指令）。
- query 位置：本 run root 的 `novix/query.txt`；任务 id 与回收日志由 Step 0 写入
  `fly-connectome-cvpr2027/automation-state.json` 的 `tasks[]`。
- query 加固要点（针对 17682 的 `finish` 但零产物）：任何提前终止前先写
  `experiment.py` 与阶段性 `result.json`；依赖清单显式；数据可达性前置；
  最终回复必须给实际数值。
- 验收：按 `guidance.md` §6 出 `acceptance-verdict.md`，再 `--before P5` 续跑；
  P5 未达强结果不得进 P6；最终成稿需 `ccf-paper-reviewer full` `**Overall:** X >= 8.0` + P21。

---

## round-007 追加（2026-11-08 13:2x，append-only）：task 18273 证据回收

> 上方 round-001 原始表保留不动。以下只追加 18273（grind attempt #3）**已回收并哈希核验**的行。
> 正式判定见 `acceptance-verdict-18273.md` = `REJECT_FAILURE`。
> **主表的 `Status` 列不改为 done**：`minimum` / `expected_strong` 均未达成，P4 全量批次
> 尚未满足 `f-research-v1` P4→P5 的强结果锁。26 阶段 pipeline-state.json 仍全部 pending。

| Guidance requirement | 实拉证据（均在 `evidence/p4-novix-18273/`） | 实测结果 | Status |
|---|---|---|---|
| 完整连接组与可达性 | `platform-result-round007.json` / `result_snapshot.json` | 178,853,187 B、138,639 节点、15,091,983 去重边；eye→KC hop3=2,544 → K=3 | 协议 done |
| SYNTHETIC 域天花板 | `result_snapshot.json.ceilings` | 1.0（5 seeds，CI [1.0,1.0]） | 协议 done |
| 真实域天花板与标签派生 | `result_snapshot.json.unavailable` | DAVIS 0.4769 < 0.70、Sintel 下载超时 → **两真实域 unavailable** | **infeasible-with-evidence** |
| 主比较（条件 × 5 seeds） | `main_table.csv` / `result_snapshot.json.conditions` | 12 条件全部有 5-seed 数值；`lif − stateless = −0.375`；`A=0 = 1.0` | 数值 done，强结果 **未达** |
| 预注册强对比 + 统计 | `result_snapshot.json.diagnostic_decisions.expected_strong` | `+0.011667`、CI `[0.00333,0.02000]`、p=0.25、q=0.25、门槛 +0.15 → `expected_strong_met=false` | **未达** |
| 一因子机制消融 | `result_snapshot.json.ablations_and_negative_controls` | 全部差值 0 / p=1 / q=1，未指认承载机制 | **未达** |
| 保度零模型对照 | `structure_dynamics_2x2.csv` | degree-null rewired fraction 0.7100；LIF 0.5067 / std 9.07e-07 | 协议 done |
| A=0 与 stateless 控制 | `main_table.csv` | `A=0` 1.0（仅解释为输入信息上界）、stateless 0.875 | 协议 done |
| λ×K 相图 / 逐跳探针 / 方差轨迹 | `lambda_K_phase.csv` / `probe_vs_hop.csv` / `variance_trajectory.csv` | 20/20 格；biological LIF 全格 KC std=0；`directional_structure_supported=false` | 协议 done |
| 复现元数据 | `config_preregistered.json`（sha 58766f4f…）、`data_manifest_revalidated.json`、`environment.json`、`entrypoint_reproduction.log`、`validate_results.log`、`experiment-traceability.csv` | 预注册哈希锁定成立；18/18 测试、440/440 validator、685 raw NPZ（远端核验） | 协议 done |
| **`project/result.json` / `project/config.json` 主文件** | **远端 `debug ls` 权威确认缺失** | 第三次路径缺陷；等价 `evidence/result_snapshot.json` 1,322,902 B、SHA-256 `2c15f8466687d7ef…` 与声称逐字节一致 | **协议缺陷（attempt #4 必改）** |

- 结论：**不进 P5**。本次是有效性 / 外部效度失败，不是机制否证、不是平台故障、不是达标。
- `result_snapshot.json` 与 claimed `result.json` 哈希一致 → 全部数值可复现，未编造、未推断。

---

## round-008 追加（2026-11-08 15:4x，append-only）：task 18390 证据回收

> 上方所有历史行保留不动。以下只追加 18390（grind attempt #4）**已回收并 SHA-256 核验**的行。
> 正式判定见 `acceptance-verdict-18390.md` = `REJECT_FAILURE`。
> **主表的 `Status` 列不改为 done**：`minimum` / `expected_strong` 均未达成，P4 全量批次
> 尚未满足 `f-research-v1` P4→P5 的强结果锁。26 阶段 pipeline-state.json 仍全部 pending。

| Guidance requirement | 实拉证据（均在 `evidence/p4-novix-18390/`） | 实测结果 | Status |
|---|---|---|---|
| 完整连接组与可达性 | `result.json.graph` / `MANIFEST.txt` | 178,853,187 B（sha `402fa0e61198e6f…`）、138,639 节点、15,091,983 去重边、谱半径 292.415；eye→KC hop1–8 `[0,15,2544,0,0,0,0,0]` → K=3 / 2,544 KC | 协议 done |
| SYNTHETIC 域天花板 | `result.json.ceilings` | 0.976667（CI [0.961667,0.990000]，400 样本，5 seeds） | 协议 done |
| 真实域天花板与标签派生 | `result.json.real_domain_methods` / `ceilings` | DAVIS 官方 GT mask 质心 0.691667（CI [0.661667,0.721667]）< 0.70、Sintel 官方 `.flo` 0.435714 < 0.70 → **两真实域 unavailable**，`migration_verdict=NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE` | **infeasible-with-evidence** |
| 主比较（条件 × 5 seeds） | `main_table.csv` / `result.json.base_conditions` | stateless 0.903333 / LIF 0.705000 / combo 0.791667 / degree-null 0.500000 / A=0 0.848333；**real_domain_contrasts=[]** | 数值 done，强结果 **未达** |
| 预注册强信号 + 统计 | `result.json.acceptance` / `validation.json` | 7 项检查 5 true / 2 false；`expected_signal_met=false`；`thresholds_lowered=false`；97/97 validator、280/280 raw NPZ、25 tests（24 passed / 1 skipped / 0 failed） | **未达** |
| 门控工作点网格 | `gate_operating_point.csv` | 15 格全落盘；probe 0.488333–0.821667；**全部 15 格 feature std > 0**；三态 `VARIANCE_AND_INFORMATION_RESTORED` | 协议 done |
| 等发放率 yoked 2×2 | `yoked_firing_rate_2x2.csv` | r*=0.02 四图 yoke 5/5；r*=0.10 degree-null **0/5 未达**；`yoked_2x2_pairwise_delta_ci_crosses_zero=false` | 协议 done，结论受限 |
| 方差—信息分离 | `variance_vs_information.csv` | 方差匹配噪声 std 0.207497 但 probe 0.495000；A=0 上界 0.848333；标签置换 0.473333 | 协议 done |
| 读出状态变量 | `readout_state_variables.csv` | `v_raw` 0.793333 > `soft_sigmoid` 0.673333，delta +0.120000 CI [0.085,0.160]，但 exact p=0.0625 / BH q=0.3125 → **不能称统计显著** | 协议 done，效力受限 |
| 一因子机制消融 | `result.json.one_factor_ablation_contrasts_vs_combo` | 去 adaptive −0.070000（q=0.1875）；去 refractory −0.006667、去 E/I +0.006667（CI 跨 0） | 协议 done，未指认显著承载机制 |
| 阴性对照 | `result.json.negative_controls` | 打乱帧序 0.708333 / flash 0.440000 / frozen gain 0.775000 / 标签置换 0.473333 / identity 0.910000 | 协议 done |
| 预注册哈希锁定 | `config_preregistered.json`（sha `f182d79e6810175c…`） | `frozen_before_training=true`、`posthoc_protocol_registered=false` | 协议 done |
| **`project/result.json` / `project/config.json` 主文件** | **远端 `debug ls` + 实拉 SHA-256 双重确认存在** | 1,971,899 B / 29,945 B 哈希 MATCH、双 snapshot byte-identical → **前三次交付缺陷本次修复** | **协议 done** |

- 结论：**不进 P5**。有效性 / 外部效度失败（真实域 ceiling < 0.70 + 预注册强信号 2 项未达），
  不是机制否证、不是平台故障、不是 `design_invalid`、不是达标。
- **新的关键事实**：18273 的「KC 方差严格 0」在 18390 规范实现中**未复现**
  （biological LIF std 0.049855、hard-spike rate 0.576893）→ round-007「门控工作点失配」假设的
  观测前提被否证；attempt #5 不得继续沿「修塌缩」路线。
- 全部数值来自哈希核验文件与平台终态原文，未编造、未推断、未把「实验跑完」写成「结果达标」。

## round-009 补充段（2026-11-08 18:2x GMT+8，append-only）— 18448 终态回收

> 上文所有历史行的 `Status` 列一律**不改动**。本段只追加新事实。
> 收尾复核发现 `18448` 在本轮执行期间由 `processing`（17:43、steps 302）跃迁为
> 平台终态 `finish`（`updatedAt 17:56:41`、steps 316、无 error）。

| Guidance requirement | Required artifact | Status | Evidence path | Notes |
|---|---|---|---|---|
| 全量实验脚本与配置 | `experiment.py` / `config.json` / `config_preregistered.json` | 已回收并哈希核验（**非 done / 不改历史 Status**） | `evidence/p4-novix-18448/` | 47,594 / 20,955 / 18,448 B，三 SHA-256 均 MATCH finalReply；prereg 自绑定一致 |
| 结构化结果 | `result.json` | 已回收并哈希核验 | `evidence/p4-novix-18448/result.json` | 575,285 B，SHA `74a186458c202f03…` MATCH；146/146 validation、design_valid=true |
| 平台终态原文 | `platform-result-18448.json` | 已归档 | 同上 | `finish`/316/完整 finalReply |
| 归档清单 | `ARCHIVE-MANIFEST.json` | 已归档 | 同上 | 9 文件，逐文件 bytes + SHA-256 |
| 正式判定 | `acceptance-verdict-18448.md` | 已出 | guidance 目录根 | **`REJECT_FAILURE`**，逐条对照 §Expected Results |

**实测（来自哈希核验文件，非推断）**：DAVIS `INPUT_BOTTLENECK`
（current 0.613333、oracle 1.000000、gap +0.386667）；SINTEL `DOMAIN_USABLE`
（current 0.700000 恰达冻结门槛）；SINTEL `lif_homeostasis − stateless`
5/11 seeds 均 **0.000000** CI `[0,0]`、三检验族 p=1 → `c1_guidance=failure`、
`transfer_claim_made=false`、`expected_signal_met=false`。
阴性对照校准**失败**（`label_permutation − lif_combo` 11-seed `−0.115909`、p=0.0009765625）、
跨实现 `single_factor_flip_localized=false`，两项如实保留。
`A=0` 为输入信息上界；`degree_null_lif` 仍高于真实图 LIF →
「保度零模型从未输给真实生物接线」继续成立。

**不进 P5、不写论文、不标任何 stage passed**：`pipeline-state.json` 26 阶段仍全
`pending`、`history=[]`。这是 C1 同一篇的 correction loop 证据，不是新篇、不是达标。


---


---

## round-013 收尾追加 · P4 全量实验批次 novix `18533`（attempt #7）· 2026-11-09

| Guidance 要求 | 必需产物 | 实测 | 状态 | 证据路径 |
|---|---|---|---|---|
| 全量实验可复现脚本 | `experiment.py` / `entrypoint.sh` | 16,792 B / 4,516 B，短路径实拉非空 | `done` | `evidence/p4-novix-18533/experiment.py`, `entrypoint.sh` |
| 主结果文件 | `project/result.json` | 5,393,376 B，SHA-256 `9f24e07f0d703841…` **MATCH** | `done` | `evidence/p4-novix-18533/result.json` |
| 预注册配置 | `config_preregistered.json` | 22,352 B，SHA-256 `0a7c6d473a110e6a…`，`frozen_before_outcomes=true`、`hash_lock_verified=true` | `done` | `evidence/p4-novix-18533/config_preregistered.json` |
| 配置 / 清单 | `config.json` / `MANIFEST.txt` | 32,759 B / 65,614 B，两哈希均 **MATCH** | `done` | `evidence/p4-novix-18533/config.json`, `MANIFEST.txt` |
| 平台终态与回复 | finalReply / task get | `finish`/536，finalReply 2,734 字符；`errorCode=None` | `done` | `evidence/p4-novix-18533/platform-finalReply.json`, `platform-task-get.json` |
| 真实域 ceiling 阶梯 | 两域 current / oracle / decidability | DAVIS 0.617284 / 0.969136 `INPUT_BOTTLENECK`；SINTEL 0.3125 / 0.6875 `TASK_UNDECIDABLE`；门槛 0.70 均**未达** | `done`（failure） | `result.json.real_domain_ceilings` |
| 测量可辨识性第一硬门 | 混淆矩阵 / 注入阶梯 | `measurement_identifiability_gate_passed=true`；+0.25 注入恢复 DAVIS 0.067901（斜率 0.284383）、SINTEL 0.0625（斜率 0.155642） | `done`（灵敏度远低于单位增益） | `result.json.measurement_identifiability_gate`, `known_signal_injection_ladder` |
| 梯度路径 2×2 | 264/264 cells、33/33 参数审计 | 真跑完；SINTEL validation `+0.204545` CI `[0.159091,0.255682]` 但 `interpretation_allowed=false` | `done`（不可解释） | `result.json.gradient_path_2x2`, `trained_real_domain_main_readout` |
| 三项必修诊断 | ①校准 ②DAVIS 阶梯 ③SINTEL 三态 | ①bootstrap I 类错误 `0.076 > 0.075` **失败**；②7 档无一收窄 gap `0.351852`；③`IMPLEMENTATION_IDENTICAL_BRANCH`（forced probe 0.78125 < 0.90） | `done`（全部不通过/不可解释） | `result.json.negative_control_calibration`, `davis_input_encoding_ladder`, `sintel_zero_delta_diagnostics` |
| 主读出（训练后 real delta） | unexposed holdout | SINTEL `unavailable`（冻结分区无双类别匹配集）；exposed `0.000000` CI `[0,0]` p=1；DAVIS unexposed `−0.011069` CI `[−0.014837,−0.007537]` | `infeasible-with-evidence` / 未达 | `result.json.trained_real_domain_main_readout` |
| 一因子消融 / 阴性对照 | 消融矩阵 / 校准表 | `single_factor_flip_localized=false`；`negative_controls_calibrated_nonsignificant=false`；全部 contrast 标 `uncalibrated` | `done`（不通过） | `result.json.ablations_and_controls`, `negative_control_calibration` |
| 统计效力 | 5 / 11 paired seeds | 最小双侧 exact p `0.0625` / `0.0009765625`；原文「增加 seed 只提高检验分辨率，不是机制证据」 | `done` | `result.json.power_limitations` |
| 原始日志 / 硬件 / seeds | raw NPZ / 环境 | 411 per-condition/per-seed raw NPZ、90 contrasts、13/13 单测、77/77 pre-final、88/88 final、447 manifest 缺失 0 | `done` | `result.json.stages`, `validation`, `hardware`, `environment` |
| 历史证据重分析 | 18390 / 18448 归档 | 均 `INSUFFICIENT_RAW`（远端归档缺失、`raw_npz_count=0`），`original_evidence_mutated=false`，不编造等价性 | `infeasible-with-evidence` | `result.json.historical_delta_interpretability` |

**判定**：`acceptance-verdict-18533.md` = **`REJECT_FAILURE`**
（`design_valid=true`、`all_required_stages_complete=true`，但
`c1_guidance.verdict=failure`、`minimum_met=false`、`expected_strong_met=false`、
`transfer_claim_made=false`、
`migration_verdict=NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE`）。
**不是** design_invalid / 平台故障 / 机制否证 / 达标。
`A=0` 为输入信息上界；「保度零模型从未输给真实生物接线」的既有禁令继续适用。

**不进 P5、不写论文、不标任何 stage passed**：`pipeline-state.json` 26 阶段仍全
`pending`、`history=[]`、`workflow_complete` / `submission_ready` 未置位。
这是同一 C1 的 correction loop 证据，不是新篇、不是达标。
`abandon_allowed=False`（保守 6/6 机制不同尝试、0/2 干净 kill、0/2 不可修复评审）。


---

## round-015 追加 · P4 全量实验 novix task 18696（attempt #8）

> 正式判定见 `../acceptance-verdict-18696.md` = **`REJECT_FAILURE`**。
> 证据归档 `evidence/p4-novix-18696/`（15 文件 + `ARCHIVE-MANIFEST.json`），
> 短路径 `C:/code/phd-snn/_nv18696`，9/9 声明 SHA-256 **MATCH**、双 snapshot 逐字节一致。
> `project/config.json` 路径**不存在**（第五次交付缺陷），但 config 内容经
> `snapshots/config.snapshot-a/b.json`（16,885 B `03128444…`）按声明哈希核验，如实记录。

| Guidance requirement | Required artifact | Success check | 实测 | Status | Evidence |
|---|---|---|---|---|---|
| 完整边表 + 保度零模型 | connectome / topology invariants | 完整文件、不变量精确相等 | 178,853,187 B `402fa0e6…`；138,784 节点 / 16,847,997 边行 / 15,091,983 nnz；2,000,000 交换 / 733,649 接受 / 1,368,018 改变边行；`all_required_invariants_exact=true`、`nonidentity=true`、`identity_fallback_used=false` | `done` | `result.json.results.connectome` |
| 公开真实域数据 | DAVIS / Sintel / Zenodo | 逐文件字节数 + 哈希 | DAVIS 832,766,765 B、Sintel 5,627,783,629 B、FlyWire annotations/eye positions、SHA256SUMS 全校验；`real_data_substitution_used=false`；DAVIS 737 窗/90 scenes、Sintel 127 窗/23 scenes（官方 GT `.flo`） | `done` | `result.json.results.data_integrity` |
| SYNTHETIC 标注 | 400 样本 T=8 方向二分类 | 明确 SYNTHETIC | 400 样本，flash / label permutation 阴性对照 `0.539394` / `0.510606` | `done` | `result.json.results.historical_synthetic_anchor_and_controls` |
| 预注册冻结 | `config_preregistered.json` + `execution_lock.json` | 训练前锁定、哈希一致 | 11,988 B `5bf618d5…` / 1,273 B `33086445…`；`frozen_before_outcomes=true`、`hash_lock_verified=true`、`observed_main_contrasts_before_lock=false` | `done` | `config_preregistered.json`, `execution_lock.json` |
| 主门：ceiling + 标签可判定性 | `real_domain_ceiling_and_label_decidability_gate` | `DOMAIN_USABLE` 才允许 real delta | DAVIS `0.424242` CI `[0.340909,0.515152]`、SINTEL `0.400000` CI `[0.2,0.6]`，两域 `INPUT_BOTTLENECK`、`interpretation_allowed=false`；本次 `gt_oracle_upper_bound=1.0`（明确非历史 `0.6875` 重算） | `done`（failure 命中） | `result.json.results.preflight.real_domain_ceiling_and_label_decidability_gate` |
| 输入级 `H(ω)` 传递函数 | drive/syn/v/KC 四级 + 逐级增益 | 两条件可分辨 | 注入 `raw_32x32_luminance_before_4x4_compound_eye_sampling`；两域 `INPUT_SIGNAL_PATH_MEASURABLE`；LIF−stateless 逐环节全负（DAVIS drive `−1.224299` / syn `−0.141906` / v `−0.210777` / KC `−0.208067`）；最大首段衰减 `drive→syn` | `done`（诊断型负结果） | `result.json.results.retinal_drive_H_omega` |
| 三族校准修复全报告 | 1000 次零效应 MC、499 inner bootstrap | 三族全通过 | stratified paired bootstrap `0.149` **失败**；studentized `0.051` 通过；redefined exact/permutation `0.058` 通过 → `all_families_passed=false`、全部 contrast `uncalibrated` | `done`（失败） | `result.json.results.preflight.negative_control_calibration` |
| `localized_unit` 分支定位 | 逐计算单元 forced probe | 越过 0.9 阈值的首单元 | `localized_unit=syn`（drive 0.5 / syn 0.902778 / v 1.0 / spike 1.0 / KC 0.986111 / logit 0.708333）；完整 forward re-propagation；`zero_delta_scientific_interpretation_allowed=false` | `done` | `result.json.results.branch_localization` |
| holdout 可构造性 | scene-hash 分层 × 双类别匹配集 | 可构造 + 未在结果后改分区 | 两域 `CONSTRUCTIBLE`：DAVIS n=154 `[77,77]`、SINTEL n=24 `[12,12]`；`partition_modified_after_results=false` | `done` | `result.json.results.preflight.holdout_constructibility` |
| 两臂对称性审计 | RNG / 共享对象 / 交换条件标签反事实 | 无共享 label-dependent 对象 | `SYMMETRIC`、`confounded_contrasts=[]`、逐 seed 五类对象 `same_identity=false` `shares_memory=false`、swap counterfactual exact | `done` | `result.json.results.preflight.condition_arm_symmetry` |
| `flow_coherence` × 读出作用域 | 全格 ceiling/delta/CI | 指认空间池化 | 小格 n=2/4/6/8 不可承担结论；DAVIS high n=116 三档方向不一致；假设 B 未获干净支持 | `done`（诊断 only） | `result.json.results.real_domains.*.flow_coherence_x_readout_scope` |
| 主读出 real-domain delta | exposed / unexposed，5 与 11 seeds | `delta>=+0.15` CI 下界 > 0 | DAVIS exposed `+0.022727` / unexposed `−0.128099`；SINTEL exposed `+0.081818` / unexposed `−0.015152`；`unexposed_holdout_same_positive_sign=false`；192 检验 BH `q=0.05`；`scientific_interpretation_allowed=false` | `infeasible-with-evidence` / 未达 | `result.json.results.real_domains.*.main_delta`, `c1_guidance.domain_deltas` |
| 一因子消融 / 决定性对照 | A=0 / 保度零 / identity / 冻结 gain | 独立消融齐备 | `A=0` `0.515152`、`degree_null_lif` `0.656061`、`identity_graph` `0.489394` 等全部落盘；`one_factor_ablation_localized=true`；SYNTHETIC 上 LIF 低于 stateless（Δ `−0.114394`）记为**跨实现不一致待查事实**，不改写 | `done` | `result.json.results.historical_synthetic_anchor_and_controls` |
| 原始日志 / 校验 / 硬件 | raw NPZ / manifest / 验证报告 | 非 smoke、可审计 | 23/23 单测、142/142 pre-final、148/148 final、165 raw NPZ、614 manifest 文件、614/614 重哈希、`validation.passed=true`、最终入口 exit 0 | `done` | `validation_report.json`, `final_self_check.json`, `MANIFEST.txt` |
| 幂等引用 SHA-256 归档 | `evidence/p4-novix-18533/` | 逐项核验 | `idempotent_reference.status=unavailable`、`all_archive_hashes_verified=false`；历史数值仅声明保留、`do_not_rerun_or_recompute=true`，**未重算未重验** | `infeasible-with-evidence` | `result.json.idempotent_reference`, `config_diff.idempotent_items` |

**判定**：`REJECT_FAILURE`。`design_valid=true`、全阶段真跑完、9/9 主文件哈希 MATCH，
但 `c1_guidance.verdict=failure`、`minimum_met=false`、`expected_strong_met=false`、
`transfer_claim_made=false`、`migration_verdict=NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE`。
**不是** design_invalid / 平台故障 / 机制否证 / 达标。
不进 P5、不写论文、不标任何 stage passed（26/26 pending、history 空）。
`abandon_allowed=False`（(a) 7/7、(b) 0/2、(c) 0/2，(c) 单独即阻断换题）→ C1 继续锁定。
