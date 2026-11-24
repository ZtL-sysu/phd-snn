# P4 全量实验结果判定 — C1 / novix task 18156

判定时间：2026-11-08 06:5x GMT+8（人工提前查看，非定时任务轮次）
判定依据：`guidance.md` §「Expected Results」预注册 failure 条件；证据来自 novix exp-4090 任务 `18156` 的实拉工作区。
判定人执行口径：只用实测数值，不推断、不补数、不把负结果改成正结果。

## Verdict: `REJECT_FAILURE`（实验有效执行，但预注册 failure 条件命中）

不是 `REJECT_INVALID`：这次实验**确实跑完并留下完整证据**（`experiment.py`、`entrypoint.sh` 退出码 0、
5 seeds、110 个 raw npz、`main_table.csv`、`experiment-traceability.csv` 123 行、`validation.json` status=passed、
121 个 artifacts 复核、4 项 invariant tests passed）。与 `17682` 的「finish 但零产物」有本质区别。
但它也**不是可接受结果**，更不是强结果，因此不得进入 P5/P6 写作链。

## 三条 failure 条件逐条实测

| 预注册 failure 条件 | 实测 | 命中 |
|---|---|---|
| real-domain ceiling < 0.70 | DAVIS-2017 ceiling mean **0.5214611872**（5 seeds `[0.5388, 0.5068, 0.5114, 0.5388, 0.5114]`） | **是** |
| real-domain `delta(LIF - stateless) <= 0` | REAL_DAVIS2017：stateless **0.5205479452**、lif_homeostasis **0.5205479452**、lif_combo **0.5205479452**，delta = **0.0** | **是** |
| CI lower bound <= 0 | real-domain 所有 LIF 条件 delta CI `[0, 0]`；degree_null_lif delta **+0.000913**, CI `[-0.009132, 0.010046]` 跨 0 | **是** |
| BH-FDR q=0.05 显著 | 全表 `bh_fdr_q` 为 0.25 / 1.0，`bh_reject_q_0_05 = False`（5 paired seeds 下 exact sign-flip 最小双侧 p = 0.0625） | **否（无显著）** |
| 缺失 raw evidence | 110 个 npz + traceability 已在；但**主检查点 `result.json` 在拉回工作区中不存在** | 部分 |

`expected_strong`（real delta ≥ +0.25、CI 下界 > 0、迁移判定、一因子消融指认承载机制）**完全未达成**；
`minimum`（real delta ≥ +0.15）同样未达成。

## 实测主表（SYNTHETIC direction，5 seeds，400 样本，70/30 stratified）

| 条件 | mean acc | Δ vs stateless | 95% bootstrap CI | BH q | KC readout spike rate | feature std |
|---|---:|---:|---|---:|---:|---:|
| stateless | 0.500000 | 0 | [0, 0] | 1.0 | 0 | 0 |
| lif_homeostasis | 0.500000 | 0 | [0, 0] | 1.0 | 0 | 0 |
| lif_combo | 0.500000 | 0 | [0, 0] | 1.0 | 0 | 0 |
| degree_null_lif | 0.703333 | +0.203333 | [0.151667, 0.268333] | 0.25 | 1.971e-05 | 0.001924 |
| A=0 | 0.891667 | +0.391667 | [0.385000, 0.400000] | 0.25 | 0 | 0.056187 |

SYNTHETIC ceiling 0.998333（标签可学）；flash control ceiling 1.0，但 stateless / homeostasis / combo 同样 0.5。
REAL_DAVIS2017 motion_direction：stateless / lif_homeostasis / lif_combo 全部 **0.5205479452**（恒定），
A=0 0.536986，degree_null_lif 0.521461。

## 根因诊断（远程 finalReply 原文，可复核）

1. **KC 拓扑不可达**：从 active eye roots 出发的 exact-hop 可达 KC 数为
   hop1=0, hop2=0, hop3=0, hop4=8, hop5=714, hop6=2231, hop7=2526, hop8=2539。
   基座约定的 **3 步**传播在拓扑上到不了 Kenyon，KC 读出特征恒为常数（std=0、spike rate=0）。
   远程明确写这是「可复核的结构诊断，不是随机训练失败」。
2. **输入映射差异**：32×32 的 1024 个像素只映射到 **717 个** active eye root IDs（总 5,354）；
   每帧 drive 按最大值归一化。与本机挖掘时的 4,097 个复眼光感受器、2,335,888 行完整可读边不同
   —— 远程只取了 8 MB HTTP Range 前缀（791,218 行真实边 → 130,391 节点 / CSR nnz 782,761）。
3. **因此这不能当作对本地结论的否证**：本机实测的 `LIF − stateless = +0.2817`（CI [0.2033, 0.3617]）
   建立在另一套图构建与复眼映射上。两次实验的输入/图/读出不一致，必须先对齐协议再谈复现。
   同时 `A=0` 高达 0.8917 说明标签在输入层已可线性分离，图传播反而把信息抹平 —— 这是设计缺陷信号。

## 平台状态异常（如实记录）

- `novix --json task result 18156` 返回 `status: "processing"`、`steps: 317`，但 `finalReply` 首行即
  「# P4 全量实验最终结果」「总状态 completed」「Stage A/B/C completed」「当前无运行中的进程」。
  **平台 status 字段与内容不一致**，本判定以已落盘证据为准，并保留原始 `platform-finalReply.md` 全文。
- 远程 finalReply 声称主检查点 `/home/novix/workspace/project/result.json`，但 `debug pull` 拉回的
  session workspace 中**没有 result.json**（`ARCHIVE-MANIFEST.json` 已标注）。等价实测数据在
  `main_table.csv` + `experiment-traceability.csv` + `validation.json`，不影响数值判定，但严格按
  guidance 前置有效性属于「交付物不齐」，下一轮必须要求远程把 result.json 写进被 pull 的 workspace。
- `debug pull` 第一次失败是 Windows `WinError 206 文件名或扩展名太长`（目标 run root 路径过长 +
  远程 `.claude/skills/...` 深层目录）；改用短路径 `C:/code/phd-snn/_nv18156` 后成功（13,951 文件 / 1.7 GB）。
  全量原始证据保留在该短路径目录，关键文件已复制进 `evidence/p4-novix-18156/`。

## 后续动作（写死，交给定定时任务下一轮 Step 0 或人工 correction loop）

1. **不进 P5、不写论文、不伪造 passed**。`pipeline-state.json` 仍 26 阶段全 pending、history 为空，
   保持原样，不因本次回收而标任何阶段通过。
2. **先修当前方案（correction loop 第 1 优先级）**：
   - 把传播步数从 3 提到 ≥5（或把读出层移到 hop-2/3 信息实际到达的中间神经元），使 KC 可达；
   - 统一图构建与复眼映射到本机协议（完整可读边、相同 active eye roots），否则两域结果不可比；
   - 修 DAVIS-2017 ceiling（当前 0.52）：换更强特征/标签构造/预处理，或换一个真实域任务使 ceiling ≥0.70；
   - 要求远程在任何提前终止前把 `result.json` 写入被 pull 的 workspace，并在 query 中显式指定路径。
3. **仍不行** → 从 `candidate_pool` 取次优（D3 6.3 / E5 6.3）生成 versioned guidance
   （换 scenario 必须从 CCFA-startup 重跑）。
4. **备选耗尽** → 发散新的 5 个候选。
5. 唯一合格线不变：成稿 `ccf-paper-reviewer full` `**Overall:** X >= 8.0` 且 P21 完成。

## 诚实性声明

本判定中的每一个数值都来自 `evidence/p4-novix-18156/main_table.csv`、
`platform-finalReply.md` 或 `validation.json`，没有推断、没有补数、没有把 0.5 改成 0.6、
没有把「实验跑完」写成「结果达标」、没有把平台 `processing` 写成 `completed` 终态。
`C1` 的主命题「膜状态增益可迁移到真实光流」在本次实验中**未获支持**，且实验存在可复核的设计缺陷。
失败证据全部保留，供 correction loop 使用。
