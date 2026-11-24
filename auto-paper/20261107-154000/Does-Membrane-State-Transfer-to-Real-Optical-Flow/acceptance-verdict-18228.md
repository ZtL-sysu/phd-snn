# P4 全量实验结果判定 — C1 / novix task 18228（grind attempt #2）

判定时间：2026-11-08 09:0x GMT+8（定时任务 round-005 Step 2）
判定依据：`guidance.md` §「Expected Results」预注册条件；
证据来自 novix exp-4090 任务 `18228` 的**平台终态**与**实拉工作区**
（短路径 `C:/code/phd-snn/_nv18228`，`debug pull` rc=0，1305+ 文件 / 1.7 GB），
关键文件已归档进 `f-research-v1-run-20261107-154500-membrane-state-transfer/evidence/p4-novix-18228/`。
判定口径：只用实测数值，不推断、不补数、不把负结果改成正结果、不把「实验跑完」写成「结果达标」。

## Verdict: `REJECT_INVALID`（`design_invalid`，预注册前置不变量失败）

**不是** `REJECT_FAILURE`（18156 那种「跑完全量、有方法数值、命中 failure 条件」），
**不是**科学负结果（readout 根本没运行，没有 `delta`，不能说 LIF 差也不能说好），
**不是**平台故障（平台 `status=finish`、steps 348、脚本齐全、72/72 独立校验通过、完整数据已下载），
**更不是**方法优越或迁移成立的证据。

它是远程**严格按 query-round004.txt 第 2 项 invariant check**
（`kc_feature_std > 0`：任一方法条件在 KC 读出的特征标准差必须 > 0，否则立即落盘并标 `design_invalid`）
**合法 fail-fast 的 invalid run**。远程在 readout 拟合之前停止，
未生成任何方法准确率、bootstrap CI、sign-flip p 值或 BH-FDR 结果；
finalReply 明确区分「实测」与「推断」，未把 `design_invalid` 写成机制否证或方法优越。
`entrypoint.sh` 退出码 2 被 README 定义为「registered pre-training invariant failed」，不是运行时崩溃。

## 逐条对照 C1 guidance §Expected Results

| 预注册条件 | 实测 | 是否达成 |
|---|---|---|
| `minimum`: real-domain `delta(LIF − stateless) ≥ +0.15` 且 CI 下界 > 0 | **无任何方法准确率**（readout 未拟合，`main_table.csv` 明确标为 ceiling-only partial evidence） | **否（无法判定，不是负结果）** |
| `expected_strong`: real delta ≥ +0.25 + CI 下界 > 0 + 迁移裁决 + 一因子消融指认承载机制 | 同上，全部未测 | **否** |
| `failure`: 真实域 ceiling < 0.70 / delta ≤ 0 / CI ≤ 0 / NaN / **missing raw evidence** | `missing raw evidence` **成立**：主检查点 `result.json` 与 `config.json` 均不在拉回工作区；无方法数值 | **是（因此不构成可接受结果）** |
| 真实域 ceiling ≥ 0.70（门槛） | DAVIS-2017 v1 full-frame **0.685 < 0.70** → 标 `unavailable`；Sintel 120 s 仅 423,001,855 B、curl rc=28 → 标 `unavailable`；DAVIS v2 = **0.72** 但远程明确标注为 **post-hoc 注册**，按预注册口径**不得**当作达标证据 | 不达标（v2 不可用于正式判定） |
| SYNTHETIC ceiling ≥ 0.90 | `1.0`（5 seeds 全 1.0） | 是 |
| 完整证据/脚本拉回 | `experiment.py`、`entrypoint.sh`、`validation.json`、`main_table.csv`、`experiment-traceability.csv` 均实拉非空 | 部分（`result.json`/`config.json` 缺） |

`expected_strong` 与 `minimum` **均未达成**，且前置有效性失败 → **不进 P5、不进 P5A、不写论文、
不启动任何写作阶段、不标任何 pipeline stage passed**。`pipeline-state.json` 26 阶段仍全 pending、history 为空。

## 实测主表（全部来自拉回文件，非推断）

**平台终态**：`status=finish`、`steps=348`、`finalReply` 全文已归档
（`platform-finalReply.md`，3514 B，sha256 前 16 位 `d6dc37be219c0af1`）。

**图与可达性（18156 的两个失败点已被修好）**

| 项 | 实测 |
|---|---|
| 连接组边表 | **178,853,187 B 完整下载**，`prefix=false`，sha256 `402fa0e61198e6f26b2ef4fd18e0123cc2edff0bb1edca9dd31b29b8171580bc`（HTTP Range 64+64+44,635,459 B 拼接，gzip 校验通过） |
| 图规模 | 16,847,997 原始行 / 138,639 节点 / **15,091,983** 去重非零边；`A[post,pre]=log1p(syn_count)`、谱半径 0.95（幂迭代 60 步）、无行归一化 |
| 复眼映射 | 32×32 `x_axis/y_axis` Voronoi → 717 唯一 receptor root，704 在图中 |
| eye→KC exact-hop 1..8 | `0, 15, 2559, 2559, 2559, 2559, 2559, 2559`；**自动选 K=5**，KC readout 2559，`readout_fallback=false` |

**训练前 4 项 invariant checks（INV-2 失败导致 fail-fast）**

| 条件 | KC feature std | 非常数维 | KC hard-spike rate | INV-2 |
|---|---:|---:|---:|---|
| stateless | 3.2336e-08 | 2559 | — | pass |
| lif_homeostasis | **0.0** | **0** | **0.0** | **fail** |
| lif_combo | **0.0** | **0** | **0.0** | **fail** |
| degree_null_lif | 1.0941e-06 | 19 | 0.0 | pass |
| A=0（上界探针） | 0.10334 | 654 | — | 不适用 |
| lif_combo_no_adaptive | **0.0** | **0** | **0.0** | **fail** |
| lif_combo_no_refractory | **0.0** | **0** | **0.0** | **fail** |
| lif_combo_no_ei | **0.0** | **0** | **0.0** | **fail** |

失败的 biological-graph LIF 条件：KC soft feature 全部恒等于 **0.04742586985230446**
（`feature_min == feature_max`），跨样本方差严格 0。

**其他实测**：SYNTHETIC ceiling 5 seeds `[1,1,1,1,1]` mean 1.0；
DAVIS v2 5 seeds `[0.6417,0.7583,0.7667,0.7167,0.7167]` mean 0.72（**post-hoc**）；
degree-null 的 exact in/out degree、nnz、weight multiset、duplicate、reciprocal 约束全部验证通过；
单元/协议测试 10/10、独立结果验证 **72/72**；
raw ceiling NPZ 10 个、pre-readout feature NPZ 8 个、**bootstrap NPZ 0 个**（未进入 readout）。

## 新出现的可复核机制诊断（本轮最有价值的资产，不是结论）

`18156` 的根因是「8 MB 前缀 + 3 步传播拓扑上到不了 KC」；`18228` 已把这两个都修好
（完整边表、K=5、KC 可达 2559）。**但 biological-graph 上的 LIF 条件 KC 特征仍全部塌成同一常数**，
而 `stateless`（3.23e-08）、`degree_null_lif`（1.09e-06）、`A=0`（0.103）均保持非零方差。

即：**塌缩是「LIF 脉冲动力学 × 真实生物图拓扑」的组合特有现象，不是单纯传播深度问题，
也不是保度零模型会复现的现象**。这与 8 轮本机实测「保度零模型从未输给真实生物接线」方向一致，
并提供了一个此前没有的机制级诊断信号。同时 `A=0` 特征方差 0.103、SYNTHETIC ceiling = 1.0
再次说明**输入层本已线性可分，图传播 + LIF 反而把信息抹平/吸到固定点**。

严格边界：这是 `design_invalid` 下的**诊断观察**，不是对膜状态机制的否证、
不是 stateless 优于 LIF 的证据、不是生物学接线优势的主张（禁止），
也不能当作本机 `+0.2817`（CI [0.2033,0.3617]）的复现或否证 —— 两次协议仍不一致。

## 交付物不齐（第二次同类问题，如实记录）

- finalReply 与 `validation.json` 均声称主检查点 `result.json` 为 **63,003 B**、
  sha256 `feecf369ae3ce9c2ddbdf62207e59736ecffe879b3f61eb6cab36b5fb45173ca`（前 16 位 `feecf369ae3ce9c2`）；
  `experiment-traceability.csv` 也以 `result.json#/...` 形式嵌入了大量实测数值。
- 但 `find` 全盘确认：拉回工作区 `_nv18228/` 中**不存在** `result.json`，也不存在 `config.json`
  （`project/` 下有 `validation.json` 20653 B、`main_table.csv` 853 B、`experiment-traceability.csv` 20526 B）。
  与 `18156` 同类的坑再次出现，具体成因未证实（可能被远程 ignore 规则或 pull 快照机制排除），**不猜测、不编造**。
- 等价实测数值已完整保留在归档文件中，因此 `design_invalid` 判定**不受影响**；
  但严格按 guidance 前置有效性属于「交付物不齐」，且构成下一版 query 必须加固的实现点。

## 后续动作（写死，交 correction loop）

1. **不进 P5、不写论文、不伪造 passed**。`pipeline-state.json` 保持 26 阶段全 pending、history 空。
2. **继续死磕同一 C1**（v3 §3.6，`abandon_allowed=False`）：本轮按账本四要素给出一次实质优化，
   按 `research-recovery.md` 记录 trigger / 证据 / 替代契约 / 重跑结果，换新设计重提 P4 全量实验，
   **不带任何预算参数**，`expected_strong` 不下调。
3. **本轮不换题**：`18228` 触发的是预注册**前置不变量**（实验无效），不是对主命题的 kill criteria 命中；
   累计实质尝试 3/5、kill 命中 0/2、连续不可修复评审 0/2，放弃门槛 (a)–(e) 全部未满足。
4. 备选 F3(6.5) / F1(6.4) / F4(6.4) / F2(5.8) / F5(5.4) 只补进 `candidate_pool`，不启用。
5. 唯一合格线不变：成稿 `ccf-paper-reviewer full` `**Overall:** X >= 8.0` 且 P21 完成。

## 诚实性声明

本判定每个数值都来自 `evidence/p4-novix-18228/` 下的实拉文件、
`platform-finalReply.md` 或 `platform-task-result.json`。
没有把 `design_invalid` 写成结果达标，没有把「实验跑完」写成「结果达标」，
没有把平台 `finish` 写成科学成功，没有把 post-hoc 的 DAVIS v2 0.72 当作预注册 ceiling 达标，
没有补造任何方法准确率/CI/p 值，没有因一次 invalid run 换主攻。
失败证据全部保留，供 correction loop 使用。
