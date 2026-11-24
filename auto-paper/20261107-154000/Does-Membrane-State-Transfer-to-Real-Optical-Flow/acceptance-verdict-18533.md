# P4 全量实验正式结果判定 — C1 / novix task 18533（attempt #7）

判定时间：2026-11-09 01:5x GMT+8（round-013 **收尾复核状态跃迁**时发现）
判定依据：C1 `guidance.md` §Expected Results（预注册 `minimum` / `expected_strong` /
`failure`）与 §Traceability Checklist；证据来自**短路径实拉且 SHA-256 核验通过**的
`project/result.json`（5,393,376 B）、`config.json`、`config_preregistered.json`、
`experiment.py`、`entrypoint.sh`、`MANIFEST.txt`（归档 `evidence/p4-novix-18533/`）。
判定口径：只用实测数值，不推断、不补数、不把负结果改成正结果、不把「实验跑完」写成「结果达标」。

## Verdict: `REJECT_FAILURE`（设计有效、全量实验真实跑完，但预注册 failure 条件命中）

不是 `REJECT_INVALID`：本次 `design_valid=true`、`all_required_stages_complete=true`、
`scientific_results_available=true`、`frozen_before_outcomes=true`、
`hash_lock_verified=true`、`validation.exit_code=0`（pre-final 77/77、final 88/88、
13/13 单测、411 个 per-condition/per-seed raw NPZ、264/264 梯度矩阵 cell、
90 contrasts、33/33 参数量/SynOps 审计、447 项 manifest 缺失 0），
且**三个主文件在可 pull 的 workspace 内真实存在、非空、SHA-256 与 finalReply 声明逐字节一致**。
与 `17682`/`17788`（finish 但零产物）有本质区别。
也不是平台故障（`finish`/536 + 完整 finalReply + 全部产物）、不是机制否证、
不是达标、不是 `ACCEPT_STRONG`。

**因此不进 P5、不写论文、不标任何 stage passed、不 `--before P5`。**
`pipeline-state.json` 仍 26 阶段全 `pending`、`history=[]`。

## 交付物严格核验（本次是第四次「回复声称存在、实拉没有」风险的复核）

短路径 `C:/code/phd-snn/_nv18533`（长 run-root 会触发 Windows `WinError 206`），
逐文件 `novix debug pull task:18533 --sub <path>`（全量 pull 会触发本机 safe-delete
批量确认，故按 round-008/009 先例用定向 `--sub`）：

| 文件 | 实测字节 | 实测 SHA-256（前 16） | finalReply 声明 | 结论 |
|---|---:|---|---|---|
| `project/result.json` | 5,393,376 | `9f24e07f0d703841…` | `9f24e07f0d70384192b24b3224163368e4e642110ae4282c360fb0ff40e3c5f8` | **MATCH** |
| `project/config.json` | 32,759 | `78c84bda1396ff49…` | `78c84bda1396ff492194bd65df79fbf5a571a12bbcbea482336ae2cbe3d1ccf2` | **MATCH** |
| `project/MANIFEST.txt` | 65,614 | `1015e8a78d4e1c68…` | `1015e8a78d4e1c68a4689e14da045efe70ca2cb421f90f8573cf0f5738856268` | **MATCH** |
| `project/experiment.py` | 16,792 | `0d0f234de85bcf6b…` | （未单独声明哈希） | 存在且非空 |
| `project/config_preregistered.json` | 22,352 | `0a7c6d473a110e6a…` | `result.json.config_preregistered.sha256` 同值 | **MATCH** |
| `project/entrypoint.sh` | 4,516 | `79044c4f11819892…` | — | 存在且非空 |

注：`project/result_snapshot.json` 与 `project/config_snapshot.json` 定向拉取返回
HTTP 404（远端路径下不存在；finalReply 声称「双 snapshot 与 result/config 字节完全相同」），
**如实记录，不编造、不把缺失写成存在**。快照存在性不影响主文件判定。
`novix debug ls task:18533 project` 曾挂起 5m52s 被本地终止（本地链路慢，非平台故障；
`--sub` 定向 pull 随后 6/6 rc=0 成功）。

## 预注册门槛逐条实测（全部取自拉回的 `result.json`）

| 预注册条目（C1 guidance §Expected Results） | 实测 | 命中 |
|---|---|---|
| `failure`: real-domain ceiling < 0.70 | DAVIS current **0.6172839506** / oracle 0.9691358025 / gap **0.3518518519** → `INPUT_BOTTLENECK`；SINTEL current **0.3125** / oracle 0.6875 / gap **0.375** → `TASK_UNDECIDABLE`。两域 threshold 均为 0.70 | **是（两域都命中）** |
| `failure`: delta ≤ 0 或 CI 下界 ≤ 0 | 主读出 SINTEL exposed_test `delta=0.000000`、CI `[0,0]`、三检验族 p 全 `1.0`、11 个 paired differences 全 0；DAVIS unexposed holdout `−0.011069` CI `[−0.014837,−0.007537]` | **是** |
| `failure`: 缺失 raw evidence | SINTEL `unexposed_holdout` = `unavailable`（冻结的 scene-hash 分区无法组成双类别匹配集；分区未在观察结果后修改） | **部分（主读出缺失，非全缺）** |
| `minimum`: real-domain `delta >= +0.15` 且 CI 下界 > 0 | `c1_guidance.minimum_met = false` | **否（未达）** |
| `expected_strong`: `delta >= +0.25` + 迁移裁决 + 一因子消融指认承载机制 | `c1_guidance.expected_strong_met = false`；`migration_verdict = NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE`；`single_factor_flip_localized = false` | **否（未达）** |
| 迁移主张 | `transfer_claim_made = false`；两域均**非** `DOMAIN_USABLE` | **禁止作迁移主张** |

`c1_guidance.blocking_failures` 原文（4 项）：
`negative_control_calibration_failed` / `sintel_current_ceiling_below_0.70` /
`both_real_domains_not_DOMAIN_USABLE` / `sintel_unexposed_11seed_readout_unavailable`。

## 关键数值（原样保留，含对被阻断的正向数值）

- **训练后主对比 `LIF − stateless_trained_identically`（11 paired seeds）**：
  - SINTEL validation `+0.204545`，95% CI `[0.159091, 0.255682]`，
    exact sign-flip p `0.0009765625`、bootstrap p `0.0`、BH q `0.0017/0.0/0.0024`
    —— 但 `interpretation_allowed = false`，tags 含 `domain_not_usable` / `uncalibrated`
    （SINTEL ceiling 0.3125 < 0.70、阴性对照校准失败、unexposed 主读出缺失）。
    **这不是达标、不是强结果、不得写成 C1 成立**；平台 finalReply 明确写
    「SINTEL validation 的正 delta 不能作为正式主结果」。
  - SINTEL exposed_test `0.000000`（CI `[0,0]`、三检验族 p=1.0）；
    SINTEL unexposed holdout `unavailable`（5/11 seed 槽均为 null）。
  - DAVIS validation `+0.016835` CI `[0.010662,0.022447]`；
    exposed_test `+0.089394` CI `[0.085354,0.093939]`；
    **unexposed holdout `−0.011069` CI `[−0.014837,−0.007537]`（符号翻转）**。
- **测量可辨识性第一硬门（attempt #7 新增）**：`measurement_identifiability_gate_passed = true`，
  两域 `decision_rule_identifiable = true`、`domain_measurement_gate_passed = true`、
  `recover_known_plus_0_25 = true`，`locked_before_main_contrasts = true`。
  `known_signal_injection_ladder` 在 +0.25 档的实测恢复量：
  DAVIS validation `0.0679012346`（斜率 `0.2843829562`）、
  SINTEL validation `0.0625`（斜率 `0.1556420233`）、
  SINTEL exposed_test `0.0`（`recover=False`）。
  即**装置确能检出注入信号，但灵敏度远低于单位增益**；
  `domain_usable = false`（两域）。
  → round-011「测量装置整体不可辨识」假设被**部分否证**（装置非完全退化），
  但「灵敏度不足 + 真实域不可判定」成为新的可归因瓶颈。
- **阴性对照校准（attempt #7 必修①）**：`negative_controls_calibrated_nonsignificant = false`。
  经验 I 类错误率（500 replicates，冻结上限 0.075）：
  exact paired sign-flip `0.044`（通过）、paired bootstrap two-sided **`0.076`（超限，未通过）**、
  paired randomization `0.044`（通过）。**所有后续 contrast 均保留 `uncalibrated` 标签**。
- **DAVIS 输入编码阶梯（必修②）**：`all_variants_reported = true`、
  `any_preregistered_variant_narrows_gap = false`、
  `any_preregistered_variant_domain_usable = false`；baseline gap 与最小预注册 gap
  同为 `0.3518518519`，7 档无一收窄、无一达到 0.70；
  `main_pipeline_changed_after_viewing = false`、`ci_upper_used_for_decision = false`。
- **SINTEL delta≡0 三态（必修③）**：`sintel_zero_delta_state = IMPLEMENTATION_IDENTICAL_BRANCH`；
  forced branch probe validation_accuracy `0.78125` < 冻结阈值 `0.90`（`passed=false`）；
  `historical_18448_branch_state_inferred = false`（不推断历史实现）。
  **按预注册规则，delta=0 不得作任何科学结论**（既非否证、亦非达标）。
- **历史证据重分析**：18390 / 18448 均标 `INSUFFICIENT_RAW`
  （远端归档 `archive_roots_present=[]`、`raw_npz_count=0`、
  `same_pipeline_positive_control_present=false`），
  平台明确 `original_evidence_mutated=false`，**不编造历史等价性**。
- **真实域 ceiling 跨实现不一致**：18448 的 SINTEL `0.700000` 在本实现下为 `0.3125`
  （oracle 0.6875）；`single_factor_flip_localized = false`。
  `exact_historical_replication_claimed = false`，平台写明这是「独立执行的
  round-012 冻结重建，不是伪造的等价性断言」。
- **效力限制**：5 paired seeds 下最小双侧 exact p `0.0625`；11 paired seeds 下
  `0.0009765625`；`result.json` 明确「增加 seed 数只提高检验分辨率，不是机制证据」。
- `warnings` 原文含 `No scientific result exists at phase 0.`、
  `18489 remains platform FAILED with steps=0 and zero artifacts; its hypothesis was not tested.`、
  `18448 remains REJECT_FAILURE; its measured failures are preserved verbatim in grind_block.`

## 判定与后续（写死，交 round-014）

1. **不进 P5、不写论文、不伪造 passed、不 `--before P5`**。
   `pipeline-state.json` 仍 26 阶段全 pending / history 空，
   `workflow_complete` / `submission_ready` 均未置位。
2. **继续死磕同一 `C1`**（`abandon_allowed=False`）：本次是**第二次** `REJECT_FAILURE`，
   但**不是干净独立 kill hit**——阴性对照校准再次失败（bootstrap 0.076 > 0.075）、
   两域都非 `DOMAIN_USABLE`、SINTEL 主读出 unavailable、
   `IMPLEMENTATION_IDENTICAL_BRANCH` 明确禁止把 delta=0 作机制结论。
   按 round-009 先例，(b) kill criteria **仍 0/2**，(c) 不可修复评审 **0/2**，
   (a) 机制不同尝试**保守 6/6** 达标；`(a)(b)(c)` 未全满足 → **不得换备选/换题**。
   平台故障 / 跑得久 / 分数低 / 一次负结果明文不构成放弃理由。
3. **round-014 必须按本次真实实测修订 `NOT SUBMITTED` 的 attempt #8 预案**
   （`query-round013-attempt8-DESIGN-DRAFT-NOT-SUBMITTED.txt` 标注「不得原样启用」）：
   - 该预案的「测量装置不可辨识」前提**已被本结果部分否证**（主门通过），
     须改写为「装置可辨识但灵敏度远低于单位增益（0.284 / 0.156 斜率、
     +0.25 注入只恢复 0.068 / 0.063）」；
   - 真正的连续瓶颈是**真实域 ceiling / 标签可判定性**
     （DAVIS `INPUT_BOTTLENECK` gap 0.3519 且 7 档输入编码全不收窄；
     SINTEL `TASK_UNDECIDABLE` current 0.3125 / oracle 0.6875 甚至低于 0.70 门槛）
     与**阴性对照校准**（bootstrap I 类错误 0.076 超限）；
   - 必修：校准修复（预注册检验族/置换构造，未通过则全部 contrast 标 `uncalibrated`）、
     unexposed holdout 可构造性（冻结 scene-hash 分区须保证双类别匹配集）、
     `IMPLEMENTATION_IDENTICAL_BRANCH` 的分支实现层定位、
     SINTEL exposed/unexposed 符号一致性；
   - 保留并幂等 attempt #7 已真跑完的主门 / 注入阶梯 / 梯度路径 2×2 /
     DAVIS 阶梯 / 三态诊断（`result.json` 已哈希核验归档，不重跑、不重算、不改数值）；
   - `expected_strong(+0.25)` / `minimum(+0.15)` / ceiling 0.70 **不下调**，
     失败证据不删、负结果不改写、不编造数值、不给 4090 任何预算参数。
4. 唯一合格线不变：成稿 `ccf-paper-reviewer full` `**Overall:** X >= 8.0` 且 P21 完成。

## 诚实性声明

本判定每一个数值都来自短路径实拉、SHA-256 核验通过的
`evidence/p4-novix-18533/result.json` 与 `platform-finalReply.json`，
没有推断、没有补数、没有把 `validation +0.204545` 写成达标、没有把
`IMPLEMENTATION_IDENTICAL_BRANCH` 下的 `delta=0` 写成机制否证、
没有把「实验跑完 / design_valid / 主门通过」写成「结果达标」、
没有把 `18489` 平台故障写成科学负结果、没有删除任何失败证据。
`C1` 主命题「膜状态增益可迁移到真实光流」在本次实验中**仍未获支持**，
且两真实域在本实现下均不可判定；失败证据全部保留，供 correction loop 使用。
