# Novix 4090 全量实验任务（f-research-v1 P3/P4）

你在本任务的 4090 GPU 沙箱中执行一次**可复现的全量 ANN→SNN 转换对比实验**。这是一个科研流水线的实验阶段，不是写作任务。所有数值必须由真实运行产生，**严禁编造、估算、插值或引用文献数值冒充实验结果**。

## 0. 输出契约（最高优先级，历史踩坑）

在工作区**根目录**下建立 `project/`，最终必须存在以下文件且可被 `novix debug pull` 拉回：

```
project/config.json          实验配置与环境快照
project/result.json          全部真实数值（下节结构）
project/experiment.py        你实际执行的自包含脚本副本
project/README.md            运行方法、数据 SHA/字节数、口径说明
project/protocols/vision_pipeline.py   原样保存的库脚本
project/protocols/run_experiments.py   原样保存的运行脚本
project/logs/run.log         完整 stdout/stderr
```

**关键**：`result.json` 与 `config.json` 必须直接位于 `project/`，不要写到 `/tmp`、隐藏目录、或只有 `config.json` 骨架的空目录。**在任务提前终止、超时或任何失败之前，也必须先把脚本与阶段性结果落盘到 `project/`**。每个 seed 完成后立即追加写 `project/result.json`（不要只在最后一次性写）。最终回复里给出实际数值摘要与 `project/` 文件清单。

## 1. 环境

检查 `python -c "import torch, torch_geometric, scipy, numpy; print(torch.__version__, torch.cuda.is_available())"`。缺失则 `pip install` 对应包（torch 保持 CUDA 版）。记录 torch / CUDA / GPU 型号 / 显存到 `config.json`。

## 2. 数据（官方、公开、无需审批）

```
https://data.pyg.org/datasets/benchmarking-gnns/MNIST_v2.zip     -> data/pyg_bench/MNIST/raw/MNIST_v2.zip     期望 192378381 字节
https://data.pyg.org/datasets/benchmarking-gnns/CIFAR10_v2.zip   -> data/pyg_bench/CIFAR10/raw/CIFAR10_v2.zip 期望 316368127 字节
```
用 `curl -L -k --retry 3` 下载，校验字节数并写入 `README.md`。用 `torch_geometric.datasets.GNNBenchmarkDataset(root="data/pyg_bench", name="MNIST"/"CIFAR10", split="train"/"val"/"test")`，这是官方 SuperPixel 图视觉数据集（SLIC 超像素为节点、8-NN 带权邻接、10 类图分类、官方 split 55k/5k/10k 与 45k/5k/10k）。**不要重新造图、不要改 split**。

## 3. 原样落盘两个已本机验证的脚本

下面两个 Python 文件是本机 3060 上已实跑通过的完整实现，**逐字保存**到 `protocols/vision_pipeline.py` 与 `protocols/run_experiments.py`，禁止改写其核心逻辑（恒等式、β*、膜电位解码、两阶段、基线口径）。若必须调整，只能在 `project/README.md` 记录差异与理由。

`vision_pipeline.py` 提供：`load_vision`、`batch_graphs`（块对角邻接 A + 线性池化 R）、`train_ann`、`ann_logits`、`convert`（naive/qcfs/ftbc/tpp/parallel/ours 六种转换）、`check_identity`、`energy_accounting`、`summarize`。
`run_experiments.py` 提供：`run_one(dataset, seed, n_train, n_val, n_test, epochs, device, hidden, lr, pool)`，返回含 ANN、六方法×T 网格、消融、能耗、恒等式、环境信息的 dict。

## 4. 全量实验矩阵

写 `protocols/run_full.py` 循环调用 `run_one`：

- 数据集 `MNIST`、`CIFAR10`
- 冻结 seeds `0,1,2,3,4`
- `n_train=5000, n_val=1000, n_test=2000`
- `epochs=1000, hidden=128, lr=0.01, device="cuda", pool="sum"`
- T 网格保持 `{1,2,4,8,16}`；六种转换方法 + 4 项消融全部跑完
- 每个 seed 结束立即把该 seed 的完整 dict 追加进 `project/result.json` 的 `runs` 列表，并写 `project/logs/run.log`

`result.json` 顶层结构：`{"meta": {...}, "runs": [ run_one 返回的 dict, ... ], "summary": {...}}`。`summary` 由脚本从 `runs` 计算：每个 (dataset, method, T) 的 5-seed 均值±std 与 95% CI、相对 ANN 的 conversion loss、以及每个 T 的 ANN/SNN 理论能耗比均值。**summary 只能从 runs 实算，不得手填**。

## 5. 进入 P2/P3 前必须闭合的三项条件（本机 P1B 独立评审的准 fatal 条件）

本机 smoke（单 seed、MNIST 子集 2000 图）已给出真实信号：ANN 68.8%，ours T=16 达 66.8%（conversion loss 2.0pp），T=8 为 60.2%；理论能耗比 ANN/SNN 随 T 单调下降：T=1 为 1.605×、T=2 为 1.296×、T=4 为 0.863×、T=8 为 0.508×、T=16 为 0.277×；恒等式残差 3.24e-05；对称归一化下 `rho_mean≈0.9987`。这些是**预实验 smoke 数值，不是正式结果**，不得写进 `result.json` 冒充全量结果。

**H1 · 能耗口径统一**：`energy_accounting` 当前主口径把脉冲触发的突触操作按 AC 计（45nm：MAC 4.6 pJ、AC 0.9 pJ）。请在结果中**同时**报告两套口径并明确标注，禁止只挑有利的一套：
  - `primary`（事件驱动）：SNN AC = Σ_t nnz(s_t)×(H + deg_mean×C)；ANN MAC = E×F + N×F×H + E×H + N×H×C + N×C
  - `conservative`（把 A 传播的实值累加也按 MAC 计）：SNN 能量 = (Σ_t nnz(s_t)×H)×0.9 pJ + (T×E×C)×4.6 pJ
  两套都报 `energy_ratio_ann_over_snn` 与 `spike_density`。**若任一口径下都不存在优势，如实报告负结果，不得调口径凑 5×**。所有能耗明确标注「45nm 理论算术能耗估算，非硬件实测」。

**H2 · ρ_n 算子类对应**：对称归一化下 ρ≈1，与「非行随机聚合」的机制叙述不匹配。除主实验（sym_norm=True）外，对两个数据集各跑一个 `sym_norm=False`（原始带权邻接）臂，记录 `rho_mean/rho_max/rho_std` 与六方法 conversion loss，用于检验 ρ_n 加权系统项。**不要**把 ρ≈1 的结果包装成 ρ≠1 的证据。

**H3 · 恒等式精度与 teacher 门槛**：把 `convert` 的膜电位累加与 `B`/`B̂` 重算统一到 float64，报告每个 T 的 `max_abs_identity_residual`，目标是浮点精度内（<1e-10）；若仍为 1e-5 量级，如实记录并分析来源，不要改成「已精确验证」。teacher 若 test acc <70%，把 epochs 提到 1200 或 n_train 提到 8000（记录到 config），并在 README 说明。

## 6. 额外诊断（本机 smoke 发现的真实现象，必须在全量中复核）

- 消融显示 `ours_no_beta` 与 `ours_naive_if` 在 T=8 达 66.2%，高于完整 ours 的 60.2%：`β*=θ/(2T)` 与确定性两阶段可能存在冗余或相互作用。请在全量中按 seed 报告四项消融的配对差值与 CI，**不得删除这些负结果**，并在 README 给出机制层面的解释假设（不要求定论）。
- 膜电位解码贡献巨大（计数读出仅 14.8%），请保留该对照。
- 报告 `argmax_agreement` 随 T 的曲线与 `sum_n_hit_rate`。

## 7. 纪律

- 5 个冻结 seed；FTBC 的 β 只在 val 上校准；test 只在最终评测用一次；用于选择的切分之后不得称 unseen。
- 所有 trial 记 config / 环境 / 时间；CUDA 稀疏归约非确定，必须报 5-seed std 与 CI，不报单 seed 最好值。
- 保留全部失败与负结果；不挑 seed、不调参到显著、不改写负结果。
- 不提交、不发布、不写入任何凭据；`config.json` 中不得出现 token/密码。
- 最终回复给出：两个数据集的 ANN test acc、ours 在 T=1/2/4/8/16 的 5-seed 均值、最强单点基线对比、两套能耗口径在 T=1 与 T=8 的比值、恒等式残差量级、以及 `project/` 文件清单。

## 8. 脚本全文（逐字保存）
