# PRELIMINARY — C1 / novix task 18273 平台终态记录（**非正式判定**）

> **本文件不是 `acceptance-verdict.md`**，不是 `f-research-v1` P5 强结果锁的正式判定，
> 也不得被当作 RESULTS_PULLED / 结果达标的证据。
> 依据仅为 **平台终态 `finalReply` 原文**（已归档
> `f-research-v1-run-.../evidence/p4-novix-18273/platform-finalReply.md` 与
> `platform-result.json`）。按 `WORKFLOW-PLAYBOOK.md` Step 2，正式判定必须建立在
> **实拉并核验 `project/result.json` + `config.json` + `experiment.py` 真实存在且非空**
> 之上（18156 / 18228 两次都出现「finalReply 声称存在、拉回工作区却没有」）。
> 本轮 short-path `debug pull` 到 `C:/code/phd-snn/_nv18273` **仍在进行中**，
> 收尾时 `result.json` / `config.json` 尚未落盘 → 正式判定交给 **round-007 Step 0**。
>
> 记录时间：2026-11-08 11:4x GMT+8（round-006 收尾复核时发生状态跃迁）。

## 平台终态（原文口径，非推断）

- `novix --json task result 18273` → `status=finish`、`steps=355`、**完整 `finalReply`**（7247 B）。
- 平台自报终态标签：**`COMPLETED_VALID_DESIGN_EXPECTED_SIGNAL_NOT_MET`**，
  `design_valid=true`、`expected_signal_met=false`。
- 平台明确口径：「实验、机制诊断和验证均已完整完成，但预注册的强恢复信号没有达到固定标准」；
  「**不能表述为方法成功、方法优越或机制已被否证**」。
- 18/18 单元/集成测试、440/440 严格 validator、685 个 raw NPZ、`entrypoint.sh` 端到端成功。
- `finalReply` 声称 `project/result.json` 1,322,902 B（sha256 前 16 `2c15f8466687d7ef`）、
  `project/config.json` 16,314 B，且 `git check-ignore -v project/result.json` stdout 空 / exit=1
  （未被忽略）。**这三点仍需本地实拉核验，本文件不据此确认。**

## 关键实测数值（全部来自平台终态原文，非本机核验）

| 项 | 实测 |
|---|---|
| 完整连接组 | 178,853,187 B、`prefix=false`、138,639 节点 / 15,091,983 去重有向边；biological 谱半径 504.30、degree-null 461.81 |
| eye→KC exact-hop | hop2=15、**hop3=2,544**（按冻结回退规则取 **K=3**，读出 2,544 个 annotated KC，未用随机替代） |
| SYNTHETIC ceiling | 1.0（5 seeds），CI [1.0, 1.0] |
| DAVIS full-frame v1 ceiling | **0.4769**（CI [0.4478, 0.5061]）< 0.70 → `unavailable` |
| Sintel | 受控下载未完成 → `unavailable` |
| 两真实域 | **均 unavailable → 明确不做 SYNTHETIC→REAL 迁移主张**；未注册 post-hoc DAVIS v2，未用 toy 冒充真实域 |
| `stateless` | 0.875000，读出 std 1.4355e-08 |
| `lif_homeostasis` / `lif_combo` / `lif_drive_every_frame` | 0.500000 / 0.500000 / 0.500000，读出 std **0** |
| `degree_null_lif` | 0.473333，std 9.0732e-07 |
| `A=0` | **1.000000**，std 0.20876（仅解释为输入信息上界，非生物接线优势） |
| `stateless_skip` / `lif_homeostasis_skip` | 0.988333 / 1.000000（composite std 0.14462） |
| `lif_homeostasis − stateless` | **−0.375**，exact p=0.0625，BH q≈0.06818 |
| **预注册强对比 `lif_skip − stateless_skip`** | **+0.011667**，CI [0.00333, 0.02000]，exact p=0.25，BH q=0.25；**固定强信号门槛 +0.15 未达** → `expected_strong_met=false` |
| 方差定位 | biological LIF hop0–3 KC std 全 0、hop3 membrane cross-sample std 0、hard-spike rate 0；`drive_every_frame=true` **仍全 0**；skip 只恢复 composite（绕过图传播的输入分支），**graph-KC 分支仍零方差** |
| 2×2 结构×动力学 | biological/identity/A=0/degree-null × stateless/LIF 全格；**identity LIF std 0.2075、A=0 LIF std 0.00156 非零**，但准确率仍 ≈chance |
| λ×K 相图 | 20/20 格完成；biological baseline LIF 与 drive-every-frame LIF **所有格 KC std=0**；drive-reinjection interaction fraction=0；`directional_structure_supported=false` |
| 一因子消融 | 去 adaptive /  refractory / E/I / frozen gain / drive once-every / 打乱帧序 / flash 全部 accuracy=0.5、KC std=0、差值 0、p=1、q=1 |

## 对照 C1 `guidance.md` §Expected Results（预览，非正式判定）

| 预注册条件 | 平台终态数值 | 是否达成 |
|---|---|---|
| `minimum`: real-domain `delta(LIF−stateless) ≥ +0.15` 且 CI 下界 > 0 | 两真实域 `unavailable`，无 real-domain delta | **无法判定（不是负结果）** |
| `expected_strong`: real delta ≥ +0.25 + 迁移裁决 + 一因子消融指认承载机制 | 同上；且 SYNTHETIC 侧预注册强恢复信号 +0.0117 << +0.15 | **否** |
| `failure`: real ceiling < 0.70 / delta ≤ 0 / CI ≤ 0 / NaN / missing raw evidence | DAVIS 0.4769 < 0.70 命中；`lif−stateless = −0.375` | **是（因此不构成可接受结果）** |
| 一因子消融 | 全部差值 0、p=1、q=1，未指认承载机制 | 否 |

→ 待本地实拉核验后，按 §6 的预期正式判定为 **`REJECT_FAILURE`**
（**有效跑完全量、有方法数值、命中预注册 failure 条件 / 强信号未达**），
**不是** `REJECT_INVALID`（这次 `design_valid=true`，readout 已拟合），
**不是**平台故障，**不是**科学负结果，**不是**方法优越，**不是**结果达标。
**不进 P5、不写论文、不标任何 pipeline stage passed。**

## 【必须如实记录】本轮 attempt #4 预案假设被终态实测**部分否证**

round-006 Step 6/7 曾基于 18228 的恒值 `0.04742586985230446 ≈ sigmoid(-3)`
推导假设「LIF 分支 **v≡0**，即输入注入/突触电流/膜状态递推被**整体旁路或恒零**」
（见 `query-round006-attempt4-DESIGN-DRAFT-NOT-SUBMITTED.txt`）。

**18273 的 2×2 实测否证了这个「整体旁路」解释**：

- `identity` 图 LIF：std **0.2075**（非零）、accuracy 0.5067；
- `A=0` LIF：std **0.00156**（非零）、accuracy 0.5067；
- 只有 **biological graph + hard-spike → resolved KC readout** 这条路径严格零方差。

即 LIF 代码在 identity / A=0 图上是**在跑的**，不是被整体旁路；
严格零方差是 **biological-graph × hard-spike 门控 → KC 读出** 的特异现象。
平台终态「有限推断」亦明确：
- #4：「严格零方差」与「标签信息丢失」**不是同一现象**（identity/A=0 LIF 方差非零但准确率仍 ≈chance）；
- #5：当前测量**不能证明**所有隐藏节点收敛到唯一数学固定点，也**不能**简单归因于「只有图结构」或「只有膜动力学」；
- #2：每帧重注入输入**没有恢复** biological KC 或 membrane 的跨样本方差；
- #3：residual skip 保留的是**绕过图传播**的输入信息，没有修复 graph-KC 分支。

→ 结论：round-006 的 attempt #4 预案**不得原样启用**；
下一轮必须基于这批实测**修订假设**（把「整体旁路」收窄为
「biological-graph × hard-spike 门控 → KC 读出的特异塌缩」，
并把「方差塌缩」与「标签信息丢失」分开测量），
再按 `research-recovery.md` 走 correction loop。
**`expected_strong` 不下调、失败证据不删、不把负结果改写成正结果。**

## 交接 round-007 Step 0

1. 先检查短路径 `C:/code/phd-snn/_nv18273` 的 pull 是否已完成；
   未完成则 `RETRY_PULL`（仍用短路径，长 run-root 会触发 Windows `WinError 206`）。
2. **严格核验** `project/result.json`（声称 1,322,902 B）+ `project/config.json`（16,314 B）
   + `experiment.py` 是否真实存在且非空、哈希是否与 finalReply 一致；
   前两次都出现「声称存在、实拉没有」，这次不可只信回复。
3. 把关键证据归档进 `evidence/p4-novix-18273/`、写 `experiment-traceability.md`。
4. 核验通过后按 C1 `guidance.md` §6 写**正式** `acceptance-verdict-18273.md`，
   回填 `status` / `verdict` / `next_action`；**达标才 `--before P5`**。
5. 不达标（预期 `REJECT_FAILURE`）→ 继续死磕同一 C1，
   按上节修订 attempt #4 假设、账本四要素、无预算参数重提。
   `abandon_allowed=False`（3/5 尝试、0/2 kill、0/2 不可修复评审），**不换题、不放弃**。
