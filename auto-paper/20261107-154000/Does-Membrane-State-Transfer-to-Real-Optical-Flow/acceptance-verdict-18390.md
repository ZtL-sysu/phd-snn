# P4 全量实验结果判定 — C1 / novix task 18390（grind attempt #4，正式判定）

判定时间：2026-11-08 15:4x GMT+8（定时任务 round-008 Step 2）
判定依据：C1 `guidance.md` §「Expected Results」预注册条件（`minimum` / `expected_strong` / `failure`）
证据来源：novix exp-4090 任务 `18390` 的**平台终态原文** + **实拉并 SHA-256 核验的工作区文件**，
已归档 `f-research-v1-run-20261107-154500-membrane-state-transfer/evidence/p4-novix-18390/`（20 个关键文件 + `ARCHIVE-MANIFEST.json`）。
判定口径：只用实测数值，不推断、不补数、不把负结果改成正结果、不把「实验跑完」写成「结果达标」。

## 本轮 Step 0 / Step 2 的严格核验（**第四次交付缺陷已修复**）

| 核验项 | 结果 |
|---|---|
| `check_inflight.py` 机械轮询 | `18390` 记为 `transport_error_retry`（脚本对 rc≠0 的机械标注）；**不采信**，主会话亲自权威复核 |
| `novix --json task result 18390` | rc=0、`status=finish`、`steps=395`、**完整 finalReply**（`updatedAt 2026-11-08 15:16:33`）、`chatSessionId=a988d1715a9b330ca943067d4275d58e` |
| `novix --json task get 18390` | rc=0，`status=finish`，`createdBy=637`，`createdAt 13:51:02`，`updatedAt 15:16:33`，`version=2` |
| 远端 `novix debug ls <session> project -L 2` | **权威确认**：`project/result.json` 1,971,899 B、`project/config.json` 29,945 B、`project/experiment.py` 64,070 B、`project/MANIFEST.txt` 46,738 B、`project/entrypoint.sh` 4,197 B、`project/config_preregistered.json` 15,913 B **全部真实存在** → 18156/18228/18273 三次「声称存在、实拉没有」的**协议缺陷本次确实修好** |
| 短路径定向 `--sub` 拉取 | 主文件 6 个 + `evidence/`（299 文件，含 280 raw NPZ）+ `logs/`（13 文件）全部 rc=0；长路径 `WinError 206` 与全量 pull 的 safe-delete 批量确认均未触发 |
| **SHA-256 实测核验** | `result.json` 1,971,899 B sha256 `6749655d3601b77361cd02991e0257b823b61a4eb12fe9e7ca7bee9663911213` **MATCH**；`config.json` 29,945 B sha256 `4b921cb3ee34215f2a5fddac59e139828a442ca4f092044071fb406b473255da` **MATCH**；`evidence/result_snapshot.json` 与 `result.json` **byte-identical=True**；`config_snapshot.json` 与 `config.json` **byte-identical=True**；`MANIFEST.txt` sha256 `f4b7ad3585fa9c83…` 与 finalReply 一致 |
| `evidence/validation.json` / `validate_results.log` | 97/97 checks passed、0 error failures、0 warning failures、280/280 raw NPZ、`design_valid=true`、`scientific_expected_signal_met=false` |
| `test_pipeline.log` | 25 tests run、24 passed、1 skipped（`test_25` finalization 前按设计跳过）、0 failures |
| 预注册哈希锁定 | `preregistration.frozen_before_training=true`、`posthoc_protocol_registered=false`、sha256 `f182d79e6810175c7f422ce8279167b9cf19ef72bf3cc7add76b2877a42c14f5` 与实拉 `config_preregistered.json` 一致 |

→ 结论：**本次数据真实、完整、可复现，没有任何数值推断或编造**。交付缺陷已修复，
因此 attempt #5 不再需要把「主文件持久化」列为必改项。

## Verdict: `REJECT_FAILURE`（有效跑完全量、有真实方法数值、命中预注册 failure 条件 / 强信号未整体达标）

**不是** `REJECT_INVALID`（`design_valid=true`、97/97 validator、readout 已拟合、有全部方法数值），
**不是**平台故障（平台 `finish`、脚本/日志/数据齐全）、
**不是**科学负结果或机制否证（平台明示「不作 synthetic→real 迁移主张」，
`migration_verdict=NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE`）、
**不是**方法优越、不是迁移成立、**不是结果达标**。

## 逐条对照 C1 guidance §Expected Results

| 预注册条件 | 实测（哈希核验的 `result.json` / `validation.json`） | 是否达成 |
|---|---|---|
| `minimum`: real-domain `delta(LIF − stateless) ≥ +0.15` 且 CI 下界 > 0 | **无 real-domain delta**：`real_domain_contrasts=[]`；DAVIS ceiling `0.691667 < 0.70` → `unavailable`；Sintel `0.435714 < 0.70` → `unavailable` | **否（不是负结果，是无法判定）** |
| `expected_strong`: real delta ≥ +0.25 + 迁移裁决 + 一因子消融指认承载机制 | 同上；`acceptance.expected_signal_met=false`，7 项预注册检查 **5 true / 2 false**：`at_least_one_real_ceiling_ge_0_70=false`、`yoked_2x2_pairwise_delta_ci_crosses_zero=false`；`thresholds_lowered=false`（门槛未下调）、`fixed_minimum_real_delta=0.15`、`fixed_expected_strong_real_delta=0.25` | **否** |
| `failure`: real ceiling < 0.70 / delta ≤ 0 / CI ≤ 0 / NaN / missing raw evidence | `real ceiling < 0.70` **命中**（DAVIS 0.691667、Sintel 0.435714）；`real_domain_methods` 两域均 `status=unavailable, reason=ceiling_mean_below_0.70` | **是（因此不构成可接受结果）** |
| SYNTHETIC ceiling ≥ 0.90 | `0.976667`（CI [0.961667, 0.990000]，400 样本） | 是 |
| 决定性对照 / 消融 / 阴性对照 | A=0 0.848333（明确为输入信息上界）、保度零模型（15,091,983 边精确保度审计通过）、identity、15 格 θ×gain 网格、等发放率 2×2、方差—信息分离、五种读出状态变量、一因子消融、打乱帧序/flash/标签置换全部落盘 | 是（协议层面） |

`expected_strong` 与 `minimum` **均未达成**，且命中预注册 failure 条件 →
**不进 P5、不进 P5A、不写论文、不标任何 pipeline stage passed**。
`pipeline-state.json` 26 阶段仍全 pending、history 为空（本轮未改动）。

## 实测主表（全部来自哈希核验文件，非推断）

| 条件 | probe accuracy | feature std | hard-spike rate |
|---|---:|---:|---:|
| Stateless biological | 0.903333 | 0.021345 | 0.082674 |
| Biological LIF homeostasis（θ=0.15, gain=8） | 0.705000 | **0.049855** | **0.576893** |
| Biological LIF combo | 0.791667 | 0.010898 | 0.003149 |
| Degree-null LIF（固定阈值） | 0.500000 | 0（饱和常量，非 no-spike collapse） | 1.000000 |
| A=0（输入信息上界） | 0.848333 | 0.145290 | 0.080394 |

- 门控网格 15 格：probe accuracy `0.488333–0.821667`，**所有 15 格 feature std > 0**，
  hard-spike rate `0.000004–0.999823`；三态分类 `VARIANCE_AND_INFORMATION_RESTORED`。
  代表格 θ=0.01/gain=1 → 0.821667；θ=0.30/gain=1 → 0.630000。
- 等发放率 LIF r*=0.02：biological 0.823333 / degree-null 0.850000 / identity 0.620000 / A=0 0.755000；
  r*=0.10：biological 0.843333 / degree-null 0.850000（**yoke 0/5 未达成**）/ identity 0.910000 / A=0 0.898333。
  `yoked_2x2_pairwise_delta_ci_crosses_zero=false` → **不能宣称结构效应已被等发放率控制解释或消除**。
- 方差—信息分离：observed biological LIF std 0.049855 → 0.705000；
  方差匹配噪声（target 0.2075）实测 std **0.207497** 但 probe **0.495000**；
  方差不匹配噪声 std 0.103748 → 0.495000；标签置换 0.473333；A=0 上界 0.848333。
  → 「恢复总方差 ≠ 恢复标签信息」得到支持，但**不是**最终因果证明。
- 读出状态变量：`v_raw` **0.793333** > `hard_spike`/`spike_count` 0.696667 >
  `soft_sigmoid` 0.673333 > random projection 0.676667 > `threshold_crossing_time` 0.650000。
  `v_raw − soft_sigmoid = +0.120000`，bootstrap 95% CI `[0.085, 0.160]`（CI 下界 > 0），
  **但** exact paired two-sided p=`0.0625`、BH q=`0.3125` → 5 paired seeds 下最小可及双侧 p 就是 0.0625，
  **不能表述为 p<0.05 或 FDR 显著**，只能作为预注册 CI 信号如实报告。
- 一因子消融：去 adaptive threshold `−0.070000`（CI `[-0.096667, -0.044958]`、p=0.0625、q=0.1875）；
  去 refractory `−0.006667`（CI 跨 0）；去 E/I `+0.006667`（CI 跨 0）；
  固定 θ 重标 gain vs 固定 gain 重标 θ `−0.003333`（p=0.9375、q=0.9375）。
- 阴性对照：打乱帧序 0.708333、flash 0.440000、frozen gain=1 0.775000、
  标签置换 0.473333、identity fixed-threshold 0.910000。
- 图审计：完整边表 178,853,187 B、SHA-256 `402fa0e61198e6f26b…`、16,847,997 源 CSV 行、
  1,756,014 合并重复对、15,091,983 唯一有向连接、138,639 节点、`syn_count` 总和 54,492,922；
  hop1–8 first-reached annotated-KC `[0,15,2544,0,0,0,0,0]` → 冻结 K=3 / 2,544 KC；
  **实测谱半径 292.41506239264993**（平台如实说明此前 `504.30` 仅是 prior reference、
  本实现未复现该值，未伪造一致性）；精确保度零模型 in/out 度、权重多重集、2,007,259 互反边对、0 自环均精确相等。
- 运行：94 condition groups、280 raw NPZ、2,000 次 bootstrap、paired-seed exact two-sided sign-flip、
  BH-FDR、全部 PCA/scaler/ridge/MI 分位数 train-only、正式批次 wall time 171.079 s。

## 对 round-007 attempt #4 假设的实测裁定（如实记录，**本轮最重要的新事实**）

round-007 假设「严格零方差塌缩 = biological-graph × hard-spike **门控工作点失配**」，
可证伪推论 (i) θ=0 / 等发放率标定后 KC std 应恢复 >0。

**该假设的前提被本次规范实现否证**：冻结 biological LIF 工作点 θ=0.15、gain=8 下，
`feature_std = 0.049855 > 0`、`hard-spike rate = 0.576893 > 0`、probe accuracy `0.705`——
**18273 所报告的「KC 方差严格 0、hard-spike rate 0」在 18390 的规范实现中根本没有复现**。
平台「有限推断」#1 原文：「严格塌缩前提被本次实现的正式测量否证……不能继续把 C1 解释成
『已复现严格塌缩后找到修复』」。

即：前三轮围绕「修复零方差塌缩」的机制假说链（round-006 整体旁路 → round-007 门控失配）
其**观测基础不稳定**，前两版的严格零方差更可能是各自实现/协议特异的产物，而非可复现的机制现象。
→ 账本四要素必须把这条记为本轮失败点，attempt #5 **不得继续沿「修塌缩」路线**，
须转向「真实域任务构造的可学性」这一连续 4 轮都未解决、且是唯一卡住 `minimum`/`expected_strong` 的瓶颈。
**不下调 `expected_strong`、不删失败证据、不把「方差恢复」写成「结果达标」。**

## 对放弃门槛的裁定（自动判定，不得自评放宽）

- 本次仍属**有效性 / 外部效度失败**（两真实域 ceiling < 0.70 + 预注册强信号 2 项未达），
  平台明确不作迁移主张、亦不构成对主命题「膜状态增益可迁移」的独立否证；
  且 18273 与 18390 用的是**不同的真实域构造协议**（full-frame v1 vs 官方 GT mask 质心 / `.flo`），
  不是同一实验的独立重复 → **不计入 kill criteria 独立触发**（维持 **0/2**），如实记录这是连续第二次命中同一 failure signal。
- (c) 连续 2 次独立 `ccf-idea-reviewer standard` 判「不可修复致命风险」：**0/2**（本轮 5 个候选评审见 `ideas/round-008/`）。
- (d)(e) 未触发、不适用。
- 本轮提交 attempt #5 后 (a) 将达 **5/5**，但 (b)(c) 仍未满足 → **`abandon_allowed = False` 不变，
  主攻 C1 继续锁定，不得换备选、不得另起新篇**。

## 交接

- `primary_focus = C1` 锁定不变；按 §3.6(2) 继续同一 idea 的 correction loop。
- 归档清单：`evidence/p4-novix-18390/`（`result.json`、`config.json`、`experiment.py`、
  `entrypoint.sh`、`MANIFEST.txt`、`config_preregistered.json`、`result_snapshot.json`、
  `config_snapshot.json`、`validation.json`、`main_table.csv`、`gate_operating_point.csv`、
  `yoked_firing_rate_2x2.csv`、`readout_state_variables.csv`、`variance_vs_information.csv`、
  `variance_trajectory.csv`、`probe_vs_hop.csv`、`experiment-traceability.csv`、
  `command_history.log`、`test_pipeline.log`、`validate_results.log`、
  `platform-result-18390.json`、`ARCHIVE-MANIFEST.json`）。
- 不进 P5、不写论文、不标任何 stage passed；`final_paper_overall=null`、`qualified=false`。
