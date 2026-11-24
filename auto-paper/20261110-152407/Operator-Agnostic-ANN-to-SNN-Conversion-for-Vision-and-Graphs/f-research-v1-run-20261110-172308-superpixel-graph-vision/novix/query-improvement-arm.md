# 预置：改进臂任务规格（待 `20049` 终态后按修正回路提交）

> **不要现在提交**。`20049` 仍在 `queued / NO_ALLOCATION`，带外明确「不要重复提交」；同一 idea 在途不并行提交。本文件是等它终态后立即派发的改进臂规格，用于冲 `expected_strong`，**不改故事、不降目标**。
> 依据：`contracts/strong-result-no-retreat.md`、`audits/strengthen-candidate-report.md`（3-seed 本机预验证）。

## 为什么需要改进臂

本机 3 个冻结 seed 的预验证（非全量）证明：`β*=θ/(2T)` 在确定性两阶段下**冗余且有害** —— `no_beta` 组合 conversion loss 2–3pp，对应 `beta_star` 为 10–25pp。`20049` 携带的是带 β* 的旧脚本，其全量结果大概率达不到 1.5pp 强目标。按 `f-research-v1` 修正回路，正确处置是**改实现并重跑**，不是收窄主张。

## 改进臂相对 `20049` 的变更（只改方法，不改定位）

| 轴 | `20049` 旧脚本 | 改进臂 |
|---|---|---|
| 主臂偏置 | `β*=θ/(2T)`（默认） | **主臂 `beta=0`**；`beta_star` 保留为显式消融臂，用于报告机制冲突 |
| θ | 固定 1.0 | 扫描 θ∈{0.5, 1.0, 2.0}，在 **val** 上选择，test 只在最终评测用一次 |
| teacher 稳定性 | 固定 800 epoch、无验证集选择 | 加 val 早停 / 权重 EMA，训练图提到 5000+，目标 seed 间 teacher 方差 <1pp |
| 稀疏化 | 无 | 加 1028 的 sparsity penalty（降低 `relu(B1)` 质量）并扫系数，目标在 loss≤1.5pp 下把 spike 密度压下来 |
| 能耗 | 单一 primary 口径 | 同时报 primary 与 conservative 两套，禁止只挑有利口径；仍标注「45nm 理论算术能耗估算，非硬件实测」 |
| ρ 算子类 | 仅对称归一化（ρ≈1） | 加 `sym_norm=False` 原始带权臂，报告 ρ 分布 |
| 恒等式 | float32 | `B`/`B̂`/膜电位累加统一 float64，目标残差 <1e-10 |

## 不变的项（故事冻结，逐条核对）

1. 方法核心仍是 1028 成稿组合（精确误差恒等式、膜电位解码、邻域时序错位/ρ_n 加权分析、确定性两阶段）；只是**去掉与新机制冲突的冗余 β***，属于组合内部重认定，不是换方法族。
2. 数据集仍是官方 SuperPixel MNIST / CIFAR10（自带图的视觉数据集），图级 10 类分类。
3. 对比对象仍是全套 ANN→SNN 转换方法（naive/QCFS/FTBC/TPP/Parallel/ours）+ ANN teacher 上限 + 直训 SNN。
4. 三重证据仍是精度（conversion loss）、时延（T 网格）、ANN 理论算术能耗对照。
5. 目标仍是 Q1–Q2 期刊档；`expected_strong` 不变：两数据集 T≤8 达 ANN−1.5pp、T≤4 优于最强单点基线 ≥1.0pp、能耗比 ≥5×、恒等式残差 <1e-10、消融方向一致。

## 执行矩阵

- 2 数据集 × 5 冻结 seeds × T∈{1,2,4,8,16} × 六方法 + 4 消融
- 主臂与 `beta_star` 消融臂都跑，配对差值 + 95% CI + BH
- 稀疏化系数与 θ 在 val 上选择，全部 trial 记 ledger
- 全部负结果保留（尤其 β* 与两阶段的机制冲突、能耗反转）

## 输出契约（与 `20049` 相同，历史踩坑）

工作区根 `project/` 下：`config.json`、`result.json`、`experiment.py`、`README.md`、`protocols/*.py`、`logs/run.log`。每个 seed 完成即追加写 `result.json`；提前终止前先落盘脚本与阶段性结果。`result.json` 不得落在不可 pull 路径。

## 提交命令（仅在 `20049` 终态后）

```
novix --json task create "<本规格>" --provider novixlet --resource-pool exp-4090 --gpu --gpu-count 1
```
不带 `--max-turns` / `--timeout` / `--agent auto`（无预算约定）。提交前确认 `20049` 已终态并已回收产物，避免同 idea 并行。
