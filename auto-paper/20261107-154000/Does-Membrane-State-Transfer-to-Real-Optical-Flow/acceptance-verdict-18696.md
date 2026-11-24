# P4 全量实验正式结果判定 — C1 / novix task 18696（attempt #8）

判定时间：2026-11-09 05:5x GMT+8（round-015 **收尾复核状态跃迁**时发现）
判定依据：C1 `guidance.md` §Expected Results（预注册 `minimum` / `expected_strong` /
`failure`）与 §Traceability Checklist；证据来自**短路径定向 pull 且 SHA-256 核验通过**的
`project/result.json`（3,726,536 B，`ffc4a000b8042b91…`）、`config_preregistered.json`
（11,988 B）、`experiment.py`（64,898 B）、`MANIFEST.txt`（78,873 B）、
`validation_report.json`（23,306 B）、`final_self_check.json`、`entrypoint.sh`、
`execution_lock.json` 及双 snapshot（归档
`f-research-v1-run-20261107-154500-membrane-state-transfer/evidence/p4-novix-18696/`，
见 `ARCHIVE-MANIFEST.json`）。
判定口径：只用实测数值，不推断、不补数、不把负结果改成正结果、不把「实验跑完」写成「结果达标」。

## Verdict: `REJECT_FAILURE`（设计有效、全量实验真实跑完，但预注册 failure 条件命中）

不是 `REJECT_INVALID`：本次 `design_valid=true`、`all_required_stages_complete=true`、
`scientific_results_available=true`、`frozen_before_outcomes=true`、
`hash_lock_verified=true`、`validation.passed=true`（23/23 单测、142/142 pre-final、
148/148 final、165 raw NPZ、614 manifest 文件、614/614 重哈希通过、最终入口 exit code 0），
**主文件 9/9 声明 SHA-256 全部 MATCH**、三主文件真实存在且非空、双 snapshot 逐字节一致。
也不是平台故障（`finish`/507 + 完整 finalReply + 全部产物）、不是机制否证
（两域 `diagnostic_only=true`、`interpretation_allowed=false`、
`scientific_interpretation_allowed=false`、全部 contrast `uncalibrated`）、
不是达标、不是 `ACCEPT_STRONG`、不是 `qualified` 文章。

**因此不进 P5、不写论文、不标任何 stage passed、不 `--before P5`。**
`pipeline-state.json` 仍 26 阶段全 `pending`、`history=[]`。

## 交付物严格核验（第五次「回复声称存在、实拉没有」风险复核）

短路径 `C:/code/phd-snn/_nv18696`，逐文件
`novix debug pull task:18696 --sub <path> _nv18696/`（长 run-root 触发 `WinError 206`）：
远端 `debug ls task:18696 project` rc=0 权威列出全部文件；14 次 `--sub` 定向 pull 全部 rc=0。

| 文件 | 实测字节 | 实测 SHA-256（前 16） | finalReply 声明 | 结论 |
|---|---:|---|---|---|
| `project/result.json` | 3,726,536 | `ffc4a000b8042b91…` | `ffc4a000b8042b91…` | **MATCH** |
| `project/config_preregistered.json` | 11,988 | `5bf618d5c21a8a88…` | 同值 | **MATCH** |
| `project/experiment.py` | 64,898 | `e6f398fa98c1b81e…` | 同值 | **MATCH** |
| `project/MANIFEST.txt` | 78,873 | `b1c0daec70ec963f…` | 同值 | **MATCH** |
| `project/validation_report.json` | 23,306 | `747c33b2cef512d5…` | 同值 | **MATCH** |
| `project/final_self_check.json` | 1,706 | `2be393b3df457f7c…` | 同值 | **MATCH** |
| `project/entrypoint.sh` | 1,253 | `d8b1e42230821f36…` | 同值 | **MATCH** |
| `project/execution_lock.json` | 1,273 | `3308644514fbcc65…` | 同值 | **MATCH** |
| `config.snapshot-a.json` | 16,885 | `0312844449ece822…` | = 声明的 `config.json` 哈希 | **MATCH** |

**第五次交付缺陷（如实记录，不编造）**：`project/config.json` 在远端 `project/` 根
**不存在**（finalReply 声称 16,885 B `0312844449ece822…`）。但
`project/snapshots/config.snapshot-a.json` 与 `-b.json` 均 16,885 B、
SHA-256 **恰好等于**该声明哈希，且两份 config snapshot 逐字节一致；
`result.json` 与两份 result snapshot 亦逐字节一致（均 3,726,536 B `ffc4a000…`）。
→ config **内容**已按声明哈希逐字节核验，但 `config.json` 这个**路径**确实缺失。
与 round-007 的 `evidence/result_snapshot.json` 同类，按等价实测保留、原文不删改。

**另一项部分失败（如实记录）**：`idempotent_reference.status=unavailable`、
`all_archive_hashes_verified=false` —— 18533 归档未挂载到远端 workspace，
attempt #8 第 8 条 diff「幂等引用 + SHA-256 核验归档」**未按原协议完成**；
历史数值以 `declared_historical_results_preserved` 原样声明保留、
`do_not_rerun_or_recompute=true`，平台明确**未重算、未重验**，不作等价性断言。

## 预注册门槛逐条实测（全部取自拉回的 `result.json`）

| 预注册条目（C1 guidance §Expected Results） | 实测 | 命中 |
|---|---|---|
| `failure`: real-domain ceiling < 0.70 | 主门 DAVIS `0.424242` CI `[0.340909,0.515152]`、SINTEL `0.400000` CI `[0.2,0.6]`，两域 `decidability_state=INPUT_BOTTLENECK`、`interpretation_allowed=false`；其余冻结标签族亦全部 < 0.70。本次新协议 `gt_oracle_upper_bound=1.0`（平台明确「**不是**对历史 SINTEL oracle `0.6875` 的重新计算」） | **是（两域都命中）** |
| `failure`: `delta <= 0` 或 CI 下界 ≤ 0 | 11-seed unexposed：DAVIS `−0.128099` CI `[−0.137544,−0.118064]`、SINTEL `−0.015152` CI `[−0.056818,0.030303]`；exposed 虽为正（DAVIS `+0.022727`、SINTEL `+0.081818`）但远低于门槛且 `scientific_interpretation_allowed=false` | **是** |
| `minimum`: real-domain `delta >= +0.15` 且 CI 下界 > 0 | `c1_guidance.minimum_met=false`；`domain_deltas` 全部远低于 +0.15 | **否（未达）** |
| `expected_strong`: `delta >= +0.25` + 迁移裁决 + 一因子消融指认承载机制 | `expected_strong_met=false`；`migration_verdict=NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE` | **否（未达）** |
| 迁移主张 | `transfer_claim_made=false`；`usable_real_domains=[]`、`both_real_domains_DOMAIN_USABLE=false` | **禁止作迁移主张** |
| 阴性对照校准（attempt #8 必修①） | 三族全报告、无 post-hoc 选择：stratified paired bootstrap `0.149`（Wilson `[0.128274,0.172412]`）**失败**；studentized `0.051` 通过；redefined exact/permutation `0.058` 通过 → `all_families_passed=false`、全部 contrast `uncalibrated` | **失败**（冻结上限 0.075） |
| unexposed holdout 符号一致性（必修③） | DAVIS exposed `+0.022727` vs unexposed `−0.128099`；SINTEL `+0.081818` vs unexposed `−0.015152` → `unexposed_holdout_same_positive_sign=false`、`sign_consistent=false` 两域 | **否（符号翻转）** |

`c1_guidance` 其余实测字段：`verdict=failure`、`paper_qualified=false`、
`condition_arms_symmetric=true`、`localized_unit_available=true`、
`one_factor_ablation_localized=true`、`continue_same_C1=true`、`abandon_allowed=false`。
192 个冻结检验纳入 BH-FDR `q=0.05`；即便个别 p/q 显著，因两个输入上界门失败且
校准总体失败，上表全部 `scientific_interpretation_allowed=false`。

## attempt #8 三项必修与核心诊断的实测结果（诊断型进展，不是达标）

- **必修② `localized_unit=syn`**：forced-probe 阈值 0.9，逐单元
  `drive 0.500` / `syn 0.902778` / `v 1.0` / `spike 1.0` / `KC 0.986111` /
  `logit 0.708333`，首个越阈单元 = `syn`；干预经完整 forward re-propagation 重传播，
  非只改缓存数组。18533 的 `IMPLEMENTATION_IDENTICAL_BRANCH` **首次被定位到具体单元**，
  但 `zero_delta_scientific_interpretation_allowed=false`，`delta=0` 仍不得作科学结论。
- **必修③ holdout 可构造性：两域均 `CONSTRUCTIBLE`**（18533 的 SINTEL
  `unavailable` 已解决）：DAVIS fold 4 / 22 scenes / candidate n=181 `[104,77]` →
  matched n=154 `[77,77]`；SINTEL fold 4 / 5 scenes / n=28 `[16,12]` → n=24 `[12,12]`；
  `partition_modified_after_results=false` 两域，分区未在看到结果后修改。
- **两臂对称性审计 `SYMMETRIC`**：`condition_arms_symmetric=true`、
  `confounded_contrasts=[]`、逐 seed 的 scaler/PCA/ridge/图张量/归一化统计量
  `same_identity=false` `shares_memory=false`、交换条件标签反事实精确成立
  → 18448/round-014 假设 C「条件相关偏置」被**否证**。
- **输入级 `H(ω)` 传递函数（`attempt #8` 核心）**：注入已验证在
  `raw_32x32_luminance_before_4x4_compound_eye_sampling`；两域第五态均
  `INPUT_SIGNAL_PATH_MEASURABLE`（**不是** `NO_INPUT_SIGNAL_PATH`，
  即「链路整体不通」假设被否证）。11-seed `H_slope(LIF − stateless)` 逐环节全为负：
  DAVIS `drive −1.224299` / `syn −0.141906` / `v −0.210777` / `KC −0.208067`；
  SINTEL `drive −1.204475` / `syn −0.143227` / `v −0.226601` / `KC −0.176757`；
  两域最大首段衰减都定位到 `drive→syn`。**LIF 分支在整条链路上系统性低于
  stateless**，这是新的诊断型实测，不是达标、不是机制否证、不是把负结果改写成正结果。
- **`flow_coherence` × 读出作用域全格**：`n=2/4/6/8` 的小格不得承担迁移结论；
  DAVIS high（n=116）`global −0.022727` / `ommatidial +0.024295` / `hybrid +0.022727`
  方向不一致且全部 `uncalibrated` → 假设 B「全局空间池化抵消方向信息」**未获干净支持**。
- **SYNTHETIC 锚点（11-seed，全部 `uncalibrated`）**：`stateless 0.762121` 最高，
  `lif_combo 0.647727`（Δ `−0.114394` CI `[−0.119697,−0.109091]`）、
  `degree_null_lif −0.106061`、`A=0 0.515152`（Δ `−0.246970`）、
  `identity_graph 0.489394`、`frozen_gain 0.686364`、flash `0.539394`、
  label permutation `0.510606`。**注意**：本 run 的 SYNTHETIC 锚点上 LIF 低于
  stateless，与继承实测 `+0.2817` 方向相反 → 记为**跨实现不一致的待查事实**，
  原样保留、不改写、不推断、不作为机制证据；`A=0` 仍为输入信息上界，
  禁止宣称「生物接线带来精度优势」；「保度零模型从未输给真实接线」的既有禁令继续适用。
- 官方数据完整性：FlyWire 边表 178,853,187 B `402fa0e6…`、DAVIS
  832,766,765 B、MPI-Sintel 5,627,783,629 B 均校验通过；
  `real_data_substitution_used=false`；DAVIS 737 窗口/90 scenes、
  Sintel 127 窗口/23 scenes（官方 GT `.flo`）、SYNTHETIC 400 样本明确标注；
  完整图 138,784 节点 / 16,847,997 边行 / 15,091,983 nnz，边级 `index_add_`、
  未物化稠密邻接；保度零模型 2,000,000 次交换 / 733,649 接受 /
  1,368,018 改变边行（0.081198），`all_required_invariants_exact=true`、
  `nonidentity=true`、`identity_fallback_used=false`。

## 结论与后续

`18696` 是**历轮完成度最高的一次有效全量运行**：attempt #8 的三项必修
（校准修复、分支定位、holdout 可构造性）全部真实执行并落盘，其中两项取得
可定位的诊断进展（`localized_unit=syn`、两域 `CONSTRUCTIBLE`），
两臂对称性审计通过、输入信号通路被证实可测。但**唯一验收线未达成**：
两真实域 ceiling 仍 < 0.70、`minimum` / `expected_strong` 未达、
校准总体失败、unexposed 符号翻转、`transfer_claim_made=false`、
`c1_guidance.verdict=failure`、`paper_qualified=false`。

- **不进 P5、不写论文、不标任何 stage passed**；`pipeline-state.json`
  26/26 pending、history 空、`workflow_complete` / `submission_ready` 未置位。
- **继续死磕同一 C1**。`abandon_allowed=False`：(a) 有实验证据的机制不同尝试
  **7/7**（含本次 18696，已超过 5 次门槛）；(b) **0/2** 干净独立 kill
  （本次仍非干净 kill：校准一族 `0.149` 失败、两域 `INPUT_BOTTLENECK` 非
  `DOMAIN_USABLE`、主读出 `diagnostic_only`、`scientific_interpretation_allowed=false`、
  unexposed 符号翻转，平台明确不作机制结论）；(c) **0/2** 不可修复评审
  （round-015 的 P1–P5 独立 standard 评审 0 个不可修复致命风险、0 个 abandon）。
  (a)(b)(c) **未全满足**，且 (c) 单独即阻断换题 → C1 继续锁定、不得换备选。
- round-015 的 `query-round015-attempt9-DESIGN-DRAFT-NOT-SUBMITTED.txt`
  已按本终态**追加更正**：其 H9 的「SINTEL oracle `0.6875 < 0.70`」前提被
  本次新协议 `gt_oracle_upper_bound=1.0`（明确非历史重算）削弱，
  「标签噪声地基」假设须改写为「输入侧 `INPUT_BOTTLENECK` + `syn` 单元级衰减」；
  该预案**不得原样启用**，round-016 必须按本文件实测修订后再提交。
- 唯一合格线仍是成稿经 `ccf-paper-reviewer full` 落盘
  `**Overall:** X >= 8.0` 且 P21 完成；`final_paper_overall=null`、`qualified=false`。
