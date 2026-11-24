# P1 · Guidance Validation Report

> 契约：`../guidance-v2.md`｜校验时间 2026-11-10｜运行根：`f-research-v1-run-20261110-172308-superpixel-graph-vision/`

## 1. 结构校验（实跑）

| 检查 | 命令 | 结果 |
|---|---|---|
| v2 契约结构 | `validate_guidance.py guidance-v2.md --strict` | **rc=0, "Guidance structure is valid."** |
| 一级标题 | 8 个必需节 + `Figure/Table Decision Rules` | 齐备 |
| 论文大纲 | 六个规范主节 `1 Introduction` … `6 Conclusion` | 齐备，无禁止的顶级节 |
| 必需元素 | Dataset / Baseline / Primary metric / Secondary metrics / Failure signal / Runtime / Hardware Budget / Must appear in paper? | 齐备 |
| strict 占位符 | 无行尾冒号、`TBD`/`TODO`、空表格行 | 通过 |

## 2. 契约要素显式性核对

| 要素 | v2 中的位置 | 判定 |
|---|---|---|
| Paper story（问题/缺口/洞见/证据链） | `## Paper Story` | 明确 |
| 预期贡献 | `## Core Idea` 与 `## Paper Story`（组合与适配创新） | 明确 |
| 论文大纲 | `## Paper Outline` | 明确 |
| 预期结果（minimum / strong / failure） | `## Expected Results` | 明确，全部标注「预注册 / 非实测」 |
| 数据集 | `## Experiment Plan` → Datasets（官方 SuperPixel MNIST/CIFAR10 + 备选自构图 + Planetoid 回归锚点） | 明确 |
| 基线 | 同节 Baselines（ANN teacher、朴素 rate、QCFS/FTBC/TPP/Parallel 适配、直训 SNN、文献对照） | 明确 |
| 指标 | 同节 Metrics（top-1、conversion loss、MAC/AC/SynOps、理论算术能耗） | 明确 |
| 实验计划与统计 | 同节 Metrics + Required Ablations + Traceability Checklist | 明确，5 seeds + bootstrap + BH |
| 运行时与硬件预算 | 同节 Runtime / Hardware Budget | 明确 |
| 停止条件 | 同节 + `## Expected Results` failure signal | 明确 |
| Citation scope | `## Citation Scope`（≥36 条候选、2022–2026 冻结窗口、待 P12 核验项） | 明确 |

## 3. CCFA startup packet 加载与适用性核对

v1 的 `../ccfa-startup-packet/` 存在且 `startup-decision.md`（终版 v3）为 **`proceed` (conditional)**，因此 P1 不被阻断。

| 维度 | v1 packet | v2 契约 | 是否仍适用 |
|---|---|---|---|
| 方法族 | 固定线性算子上的转换误差刻画（源自 1028 成稿） | 完全相同，且明确「直接用 1028 成稿实现」 | ✅ 适用 |
| 目标档位 | Q1–Q2 类脑与神经网络期刊 | 相同 | ✅ 适用 |
| 公开数据规则 | 仅直接公开、无审批 | 相同（官方 `data.pyg.org` 直链） | ✅ 适用 |
| 硬件/资源包络 | 3060 12GB 本机 + 已授权 4090 | 相同 | ✅ 适用 |
| 三轮独立红队 | 2.5 / 3.2 / 3.4（1–5 尺度） | 原文保留，未抬分、未删除 | ✅ 作历史评审证据 |
| 数据集 | CIFAR-10/100、Tiny-ImageNet、ViG | **改为官方 SuperPixel MNIST/CIFAR10 图数据** | ❌ 不适用，须重做 |
| 对比对象 | 6 个视觉转换基线（未含 ANN 能耗对照） | 同一批方法适配到图消息传递 + **ANN/理论能耗对照** | ❌ 不适用，须重做 |
| 主张定位 | 收窄为诊断型横评 | 组合与适配创新 + 三重收益 | ❌ 不适用，须重做 |
| claim-evidence / 强结果契约 | C1–C5（ViG 场景） | 必须按 v2 重做 | ❌ 不适用 |

**结论**：packet 的 startup decision 与红线约束仍适用；其 `claim-evidence-matrix.md` 与 `strong-result-feasibility-contract.md` 因数据集/对比/主张变更**不可直接复用**，在 P1A 用 `contracts/claim-evidence-matrix-v2.md` 与 `contracts/strong-result-feasibility-lock.md` 替换并记录原因。

## 4. 用户新指令的契约落地核对

| 用户要求 | v2 落地 |
|---|---|
| 「组合起来也是创新」 | `## Core Idea` 与 `## Paper Story` 明确「组合与适配创新」，逐条写明继承出处 |
| 「核心用 1028 那套方法」 | `## Experiment Plan` → Implementation notes 指向 `experiments/core.py`，快照 `contracts/core-1028.snapshot.py` |
| 「放到视觉上」 | 10 类超像素图视觉分类 |
| 「带图的视觉数据集」 | 官方 SuperPixel MNIST/CIFAR10（图像本身即图，SLIC + 8-NN 带权） |
| 「和别人的 ann 转换 snn 算法对比」 | QCFS/FTBC/TPP/Parallel 适配 + 朴素 rate + 直训 SNN |
| 「和 ann 做对比 + 比能耗」 | ANN teacher 上限 + MAC/AC/SynOps + 45 nm 理论算术能耗，能耗优势为**预注册可证伪假设** |

## 5. Gate verdict

**P1 pass** — 契约结构有效、故事/大纲/预期结果/数据集/基线/指标/计划/启动 decision 全部显式；packet 适用性逐项核对，不适用部分已在 P1A 重做。未发现与证据、可行性或科研诚信冲突的条款。
