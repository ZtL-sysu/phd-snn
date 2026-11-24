# P1A · Strong-Result Feasibility Lock

> 阶段：P1A（**任何环境设置之前**）｜契约 `../guidance-v2.md`｜生成 2026-11-10
> 本锁只证明「强结果有可信实验路径」，**不**授予降低 `expected_strong` 或把计划当结果的权限；P5 仍须用真实证据达标。

## 1. 依据工件

- `../guidance-v2.md` §Experiment Plan / §Expected Results / §Traceability Checklist
- `../ccfa-startup-packet/claim-evidence-matrix.md` 与 `strong-result-feasibility-contract.md`（v1 场景，**因数据集/对比/主张变更不可直接复用**）
- `contracts/claim-evidence-matrix-v2.md`（本运行重做）
- `contracts/guidance-validation.md`（P1）
- `../evidence-snapshots/m0-results.json`（v1 M0：恒等式 25 格最大残差 9.88e-15、Hoeffding 上界 0 违反、ρ-不变干净隔离 0.3056→0.3111、失效边界 0.7058/1.1669）

## 2. 逐条主 claim 锁定

| ID | Claim | Mechanism | 直接基线路径 | 指标与方向 | `minimum` / `expected_strong` / `failure` | 代码与预算 | 证伪消融 | Stop & return | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| C1 | 图级池化后恒等式 `B̂−B=R A(E1W2)` 精确成立 | R 与 A 均固定线性，可从时间求和提出 | 固定线性算子 vs 动态/非线性变体 | 浮点残差（越低越好） | 类内 <1e-5 / <1e-12 且类外显著非零 / 类内超容差 | `vision_pipeline.check_identity`；本机 <1 min | 非线性池化、动态邻接 | S1 残差超容差 → 回 P2 | **pass** |
| C2 | 1028 组合在 T≤8 达 ANN−1.5pp 带内 | β* 消系统项、膜电位解码去 1/T 网格、确定性两阶段零方差 | ANN teacher（上限）+ 朴素 rate + QCFS/FTBC/TPP/Parallel 适配 | conversion loss (pp，越低越好) | ≤3.0pp / ≤1.5pp 且优于最强单点基线 ≥1.0pp@T≤4 / 持续 >5pp | `run_experiments.py`；5 seeds×5 T×2 数据集；3060 12GB | 去 β*、改计数解码、随机第二相 | S4 连续 failure → 修正回路 | **pass** |
| C3 | 全套转换方法在**同一超像素图骨干**上可公平横评 | 同一 teacher、同 θ/calibration/T/split；FTBC β 只在 val 校准 | 6 个转换方法 + 直训 SNN | 配对 conversion loss 差值 + 95% CI + BH | 至少 1 数据集 T≤4 优于全部单点 / 两数据集均显著 / 基线复现失败 | 官方 pkl 已落盘；6 方法同协议 | 逐方法开关组件 | S2 基线无法复现 → `infeasible-with-evidence` | **pass** |
| C4 | 与 ANN 对照且理论算术能耗有优势（用户预判） | 0/1 脉冲把 MAC 换成 AC；45nm 表 MAC 4.6pJ / AC 0.9pJ | 同架构 ANN 的精确 MAC 计数 | ANN/SNN 理论算术能量比（越高越好） | 比值 >1 / ≥5× 且 spike 密度显著低于 ANN 激活密度 / ≤1× 或 <2× 且无稀疏性证据 | `energy_accounting`，按 T 全网格记录 | 低 T 与稀疏化 teacher 条件 | 能耗假设不成立 → 收窄为「稀疏活动与 SynOps 代理」并保留负结果 | **pass（假设可证伪）** |
| C5 | 组合的每个组件都有可归因贡献 | 逐组件开关，方向由恒等式预测 | 主臂 vs A1–A4 消融臂 | 差值方向与配对 CI | 方向一致 ≥3/4 / 4/4 且 CI 不跨 0 / 方向与机制相反 | `ablations` 已实现 | 去 β*、计数解码、随机相、朴素 IF | 方向相反 → 回 P2 查实现，禁改结论 | **pass** |

## 3. 绑定目标的可信度校准

- **C2 的 1.5pp 不是拍脑袋**：来自 1028 成稿在三个引文图、7 seeds 上实测的 T≤8 水平（用户未发表内部先验，只作 baseline-calibrated 锚点，不充当公开证据）。任务结构支持迁移：R 为线性、A 固定非负，恒等式精确成立（M0 已实跑）。
- **C4 的 5× 是预注册假设，不是承诺**：用户预判「一定有优势」，本运行把它写成带 `failure` 的可证伪命题，按 T 全网格与 spike 密度共同裁定；理论估算与硬件实测严格区分。
- **阈值锁定规则**：绝对阈值在 P3 基线复现后依基线方差复核；若复核显示原阈值与证据不符，须走版本化契约变更，**不得**因尝试失败而下调同一目标。

## 4. 资源与隔离

- 5 冻结 seeds（0–4）、T∈{1,2,4,8,16}、每方法超参 ≤12 组；官方 train/val/test 划分冻结并登记 SHA-256。
- 只在 val 上校准（FTBC β）与选择；test 一次最终评测；全部 trial 记 `results/trial-ledger.json`。
- 本机 3060 12GB / CUDA 12.8 / 548 GB 空闲；全量扩展按用户授权转 novix `exp-4090`。
- CUDA 稀疏归约非确定 → 5 seeds 的 std 与 CI 必须报告，不报单 seed 最好值。

## 5. Gate verdict

**P1A pass（5/5 claims）** —— 每条主 claim 均有机制、可证伪消融、直接 simple/strong/matched 基线路径、metric-calibrated 三档、代码路径、prototype 里程碑、算力/显存/时长预算、seed 与搜索预算、以及 stop-and-return 条件。无 claim 被标 `block`。允许进入 P1B，进而 P2。
