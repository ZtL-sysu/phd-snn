# P4 全量实验结果判定 — C1 / novix task 18448（attempt #5）

判定时间：2026-11-08 18:2x GMT+8（round-009 收尾复核发现状态跃迁后补做）
判定依据：`guidance.md` §「Expected Results」预注册 `minimum` / `expected_strong` / `failure`；
证据来自 novix exp-4090 任务 `18448` 的**实拉工作区**（不是只信 finalReply）。
判定口径：只用实测数值，不推断、不补数、不把负结果改成正结果、不把「实验跑完」写成「结果达标」。

## Verdict: `REJECT_FAILURE`（实验有效执行，但 C1 预注册 acceptance 条件未达成）

**不是** `REJECT_INVALID`：`design_valid=true`、`validation_summary 146/146 passed / 0 failed`、
32/32 单元契约测试、326 raw NPZ、11 paired seeds、真实公开数据逐字节哈希验证、
`zero_information_termination=false`、全部预注册档位落盘。
**不是**平台故障、**不是**科学负结果 / 机制否证、**不是**方法优越、
**不是**迁移成立、**不是**结果达标、**不是**达标进 P5。

→ **不进 P5、不写论文、不标任何 stage passed**（26 阶段仍全 pending、history 空）。

## 平台状态与实拉核验（严格核验，不退化、不盲信回复）

| 项 | 实测 |
|---|---|
| 平台终态 | `finish` / steps 316 / `updatedAt 17:56:41` / `errorCode=None` / `errorInfo=None` / 完整 finalReply（4862 字符） |
| 收尾复核前状态 | 17:38–17:43 权威读仍 `processing`（steps 282→302），本轮执行期间跃迁终态（round-005/006/008 同类） |
| 远端 `debug ls project -L 2` | `result.json` 575,285 B、`config.json` 20,955 B、`config_preregistered.json` 18,448 B、`experiment.py` 47,594 B、`entrypoint.sh` 2,169 B、`MANIFEST.txt` 44,644 B、`validate_results.py` 15,241 B **全部真实存在** |
| 短路径定向 `--sub` pull | `C:/code/phd-snn/_nv18448`（长 run-root 触发 `WinError 206`）；主文件与 evidence 定向拉取，已核验主文件 rc=0 |
| `result.json` SHA-256 | `74a186458c202f032d94f58383ecd4baad10d47955588e70e044257bdc1f1009` — **MATCH** finalReply |
| `config.json` SHA-256 | `94b5e738de07e13015c4f99fa65c8c37dbaf5fce0c3376ab35762d6b18ec5191` — **MATCH** finalReply |
| `config_preregistered.json` SHA-256 | `9acf32dee230f5b75fc824f92a5bd11de0c004b83a8da336145987b2dc543c50` — **MATCH** finalReply，且与 `config_preregistered.sha256` 自绑定一致 |
| 预注册完整性 | `frozen_before_outcomes=true`、`hash_lock_verified=true`、`post_hoc_ladder_variants_added=false`、`thresholds_lowered=false`、SINTEL 判定 `ci_upper_bound_used_for_state=false` |

## 逐条对照 C1 guidance §Expected Results

| 预注册条件 | 实测 | 达成 |
|---|---|---|
| `minimum`: real-domain `delta(LIF − stateless) >= +0.15` 且 bootstrap CI 下界 > 0 | SINTEL `lif_homeostasis − stateless`：5-seed **0.000000** CI `[0,0]`；11-seed **0.000000** CI `[0,0]`，三检验族 p 全 = 1.0 | **否** |
| `expected_strong`: real delta >= +0.25 + 决定性迁移裁决 + 一因子消融指认承载机制 | 同上；`c1_expected_signal_met=false`、`expected_signal_met=false`、`diagnostic_expected_signal_met=false` | **否** |
| `failure`: real ceiling < 0.70 / delta <= 0 / CI 下界 <= 0 / NaN / 缺原始证据 | DAVIS current 0.613333 (<0.70) 命中；SINTEL delta = 0.000000 (<=0)、CI `[0,0]` 命中 | **是（命中 failure）** |
| 两域都 unavailable 时不得作迁移主张 | 本次 SINTEL 达 `DOMAIN_USABLE`，允许评估；DAVIS `INPUT_BOTTLENECK` 不允许 real delta。`transfer_claim_made=false`、`migration_verdict=REAL_DOMAIN_EVALUATION_PERMITTED_SINTEL_ONLY`、`transfer_outcome_verdict=NO_POSITIVE_TRANSFER_C1_MINIMUM_NOT_MET` | 如实（**不作迁移主张**） |
| SYNTHETIC ceiling >= 0.90（训练前 invariant） | 0.975000 | 是 |
| `c1_guidance` | `{"verdict":"failure","minimum_met":false,"expected_strong_met":false,"per_domain":{"SINTEL":"failure"}}` | **failure** |

## 实测主表（全部来自哈希核验的 `result.json` / finalReply）

### 真实域 ceiling / oracle 阶梯（这是 attempt #5 的核心转向）

| 域 | current | w2 | w4 | w8 | multiscale | oracle | difficulty | `decidability_state` |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| DAVIS | 0.613333 | 0.575000 | 0.605000 | 0.591667 | 0.650000 | **1.000000** | 0.613333 | **`INPUT_BOTTLENECK`** |
| SINTEL | **0.700000** | 0.666667 | 0.666667 | 0.733333 | 0.800000 | 0.800000 | 0.700000 | **`DOMAIN_USABLE`** |

- DAVIS current CI `[0.601667, 0.623333]`；`oracle − current = +0.386667`，CI `[0.376667, 0.398333]`。
- SINTEL current **恰为**冻结门槛 0.70，按预注册 **inclusive point-estimate** 规则判可用，
  `ci_upper_bound_used_for_state=false`、未用 CI 上界凑门槛、门槛未下调。
- 这是 5 次远程实验以来**第一次有真实域达到 `DOMAIN_USABLE`、第一次真正算出 real-domain delta**。
  但 delta = 0.000000 → **不是达标**，只是从「无法判定」变成「可判定的不达标」。

### C1 真实域主对比（SINTEL，唯一允许 real delta 的域）

| seeds | lif_homeostasis | stateless | delta | 95% CI | sign-flip p | bootstrap p | permutation p |
|---|---:|---:|---:|---|---:|---:|---:|
| 5 | 0.466667 | 0.466667 | **0.000000** | `[0, 0]` | 1.0 | 1.0 | 1.0 |
| 11 | 0.466667 | 0.466667 | **0.000000** | `[0, 0]` | 1.0 | 1.0 | 1.0 |

### SYNTHETIC 历史可比锚点（5 / 11 seeds）

| 条件 | 5-seed | 11-seed |
|---|---:|---:|
| stateless | 0.475000 | 0.475000 |
| lif_homeostasis | 0.536667 | 0.528788 |
| lif_combo | 0.631667 | 0.634091 |
| degree_null_lif | 0.886667 | 0.884848 |
| A=0 | 0.975000 | 0.973485 |

- `A=0` 明确为**输入信息上界**，不得写成生物接线优势。
- `degree_null_lif` 仍高于全部真实图 LIF 条件 → **「保度零模型从未输给真实生物接线」继续成立**，
  禁止宣称「生物接线带来精度优势」。

### 统计效力、阴性对照与跨实现审计（如实保留失败项）

- 5 paired seeds 最小双侧 exact p = `0.0625` → 11 seeds = `0.0009765625`；
  多个 contrast 在 5→11 seeds 后显著性翻转（`A0_minus_lif_homeostasis` 等），
  平台明确「该显著性变化仅反映检验力增加，**不作为机制成立证据**」。
  零效应注入校准通过（delta 0、三检验 p=1）。
- **阴性对照校准失败（必须原样保留）**：预注册 `label_permutation − lif_combo`
  11-seed delta `−0.115909`、exact/permutation p `0.0009765625`，未满足「恒不显著」预期 →
  `negative_controls_calibrated_nonsignificant = false`、`diagnostic_expected_signal_met = false`、
  `expected_signal_met = false`。平台未事后更换检验族或重定义对照，如实落盘。
  这是本轮的**实验有效性隐患**，下一轮设计必须处理，不得忽略或改写成通过。
- 跨实现审计：7 单因子 + 2 端点全部完成，逐档五阶段指纹齐；
  canonical `kc_feature_std = 0.0673775`、reconstructed-18273 端点 `2.2631e-6`，
  但**没有任何单因子达到冻结的 exact-zero flip 判据** → `single_factor_flip_localized = false`，
  attempt #5 子假设 (d) **未成立**。
  谱半径口径映射（解释矩阵定义差异，**不是生物机制证据**）：
  binary directed `292.415061` / parallel-row log1p `504.356358` / 当前合并 log1p `395.648612`。
- 图与数据：16,847,997 原始边行、15,091,983 合并有向对、1,756,014 重复行合并、
  138,639 节点、eye→KC `[0,15,2544,0,0,0,0,0]` → K=3 / 2,544 KC；
  精确保度零模型 100,000 次成功 double-edge swaps（101,789 attempts）、六项统计量精确保持；
  五个公开文件全部逐字节 SHA-256 复核（connectome 178,853,187 B 等）。
- 运行：`entrypoint.sh` 退出码 0、wall 282.611 s、peak GPU 322 MiB、326 raw NPZ、
  14 真实域阶梯行、154 SYNTHETIC condition-seed 行、28 统计效力矩阵行、9 跨实现审计行、
  MANIFEST 355 entries 零失败、32/32 测试、146/146 语义检查。

## 判定分类（不得混淆）

- **是**：有效跑完全量、设计有效、主文件交付完整且哈希一致、
  首次拿到可判定的 real-domain delta、C1 `minimum` / `expected_strong` **均未达成**、
  `c1_guidance = failure`、不作迁移主张、**诊断型负结果**。
- **不是**：`design_invalid`（146/146、design_valid=true、有全部方法数值）、
  平台故障、机制已被否证（平台 `interpretation_guardrails` 明确
  `diagnostic_negative_result_is_not_mechanism_falsification=true`）、
  方法优越、迁移成立、结果达标、方差恢复等于标签信息恢复、
  `A=0` 高于图条件等于生物接线优势。

## 后续动作（写死）

1. **不进 P5、不写论文、不伪造 passed**。`pipeline-state.json` 26 阶段仍全 pending、history 空，
   保持原样，不因本次回收标任何阶段通过。
2. **继续死磕同一 C1**（`abandon_allowed=False`）；唯一合格线仍是成稿
   `ccf-paper-reviewer full` `**Overall:** X >= 8.0` + P21。
3. round-010 Step 0 依 `decidability_state`（DAVIS `INPUT_BOTTLENECK` /
   SINTEL `DOMAIN_USABLE`）与本次实测**改写** round-009 的 `NOT SUBMITTED`
   attempt #6 预案，不得原样启用：优先 I2 端到端可训练膜状态（本次
   `failure_next_steps` 亦指向 I2 / I4）、I4 逐跳信息预算/残差修复，
   并必须处理本次**阴性对照校准失败**这一有效性隐患。
4. `expected_strong`（+0.25）与真实域 ceiling 门槛 0.70 **不下调**；
   失败证据（含校准失败、跨实现未定位、delta=0）全部保留；
   不把负结果改写成正结果、不编造数值、不删除任何失败档位。
5. **kill criteria 记账（如实、不自评放宽）**：本次是首次在 `DOMAIN_USABLE` 域上
   命中 guidance `failure` 条件（delta<=0、CI 下界<=0），是迄今最强的不达标信号；
   但因 (i) 阴性对照校准失败使该实验存在未解决的有效性隐患、(ii) SINTEL ceiling
   恰在 0.70 边界、(iii) 平台明确不作机制否证、(iv) 与 18273/18390 用的是不同真实域构造协议，
   **本轮不把它计为一次干净的独立 kill hit**，`kill_criteria_independent_hits` 仍记 `0/2`；
   即使计入也只有 1 次，仍 < 2 → 不改变 `abandon_allowed=False`。
   如实标注：这是迄今最接近 kill 的一次，若后续独立实验再次出现干净失败，
   下一轮必须重新评估 (b) 是否达标。

## 诚实性声明

本判定每个数值都来自 `C:/code/phd-snn/_nv18448/result.json`（SHA-256 已核验 MATCH）、
`config.json`、`config_preregistered.json`、平台 finalReply 与远端 `debug ls`。
没有推断、没有补数、没有把 0 写成正数、没有把「实验跑完 / design_valid / 方差恢复 /
首次 DOMAIN_USABLE」写成「结果达标」、没有把平台 `processing` 写成终态或反之、
没有把阴性对照校准失败隐藏、没有删改任何失败档位。
C1 主命题「膜状态增益可迁移到真实光流」在本次实验中**未获支持**；
失败证据全部保留，供 correction loop 使用。
