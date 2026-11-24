# CONFIG_AUDIT · 从代码里提取的全部超参（唯一事实来源）

来源：`protocols/vision_pipeline.py`、`protocols/run_e17.py`、`protocols/run_experiments.py`、`protocols/gen_paper_artifacts.py`。论文 §4.3 未写全的参数在此补齐。凡与提示词 T0「k=16」表述的差异见 §4。

## 1. 数据管道

| 项 | 值 | 代码位置 |
|---|---|---|
| 数据集 | PyG `GNNBenchmarkDataset`，`name="MNIST"` / `"CIFAR10"`，SuperPixel（Dwivedi 版） | `vision_pipeline.load_vision` |
| 官方 zip | `https://data.pyg.org/datasets/benchmarking-gnns/MNIST_v2.zip`（192,378,381 B）、`CIFAR10_v2.zip`（316,368,127 B） | `data/pyg_bench/*/raw/` |
| 图结构 | SLIC 超像素为节点、8-NN 高斯加权边；MNIST 40–75 节点、CIFAR10 85–150 节点 | 官方数据集自带 |
| 官方 split | 55,000/5,000/10,000（MNIST）、45,000/5,000/10,000（CIFAR10） | 同上 |
| 节点特征 X | `[intensity, pos_x, pos_y]` → F=3（论文此前未写明维数，此处钉死） | `load_vision` |
| 邻接 A | 固定、非负、对称归一化 `D^{-1/2} A D^{-1/2}`；`setdiag(0)` 去自环后 `eliminate_zeros()`；block-diagonal 拼接 | `_sym_norm`、`batch_graphs` |
| 读出 R | 固定**线性 sum pooling**（`R.sum(axis=1)==1` 断言） | `batch_graphs` |
| 抽样 | `n_train/n_val/n_test` 在官方 split 内按 seed 均匀抽样；seed ∈ {0..4, 5..9, 10..14, 15..19} 四组互不相交 holdout | `load_vision` |

## 2. ANN teacher 训练

| 项 | 值 | 代码位置 |
|---|---|---|
| 结构 | 两层 GCN：`B1 = A(XW1)+b1`，`B = R(A(relu(B1)W2))+b2` | `train_ann` |
| hidden H | **128**（width 主效应由 `unit_mask` 控制，不是改 H） | `run_e17.POINTS`、`CFG.hidden` |
| 优化器 | Adam，`lr=0.01`，`weight_decay=5e-4` | `train_ann` |
| batch | **full-batch**（整批训练图一次性前向，无 mini-batch） | `train_ann` |
| epochs | 800（E1–E17 主配置）/ 1000（E18 规模探针） | 各 run 脚本 `CFG.epochs` |
| dropout | 0.0 | `train_ann` 默认 |
| 提前停止 | 无（固定 epoch 数；不用 test 做选择） | `train_ann` 注释 |
| 特征缩放 / gauge | 正齐次变换：用训练集 `relu(B1)` 的 **99.5 分位** 归一激活尺度到 `[0, θ]`，且保持 ANN logits 精确不变 | `train_ann` 尾部 |
| 量化激活 | `quantize_L=None`（主臂不用 QCFS 量化；基线里单独实现） | 默认参数 |
| margin 正则 | `λ·E[relu(1−Δ)]`，`Δ=B_y−max_{c≠y}B_c`；MNIST **λ=0.4**、CIFAR10 **λ=0.2** | `run_e17.POINTS` |
| unit mask | 按训练集 `mean(relu(B1))` 排序保留 top-k；MNIST/CIFAR10 均 `keep_frac=0.08`（≈10 个存活单元） | `run_e17.make_mask` |
| sparsity penalty | 默认 0（E2 曾扫 {0,1e-4,1e-3,1e-2}，对 spike 数几乎无效，已记录） | `train_ann(sparsity=...)` |
| 设备 | `cuda`（RTX 3060 12288 MiB，CUDA 12.8，torch 2.11.0+cu128） | 环境 |

## 3. SNN 转换与读出

| 项 | 值 |
|---|---|
| 确定性两阶段 | `n = clip(round(clip(inst1+β,0,None)·T/θ), 0, T)`；`s[t]=round(t·n/T)−round((t−1)·n/T)`，故 `Σ_t s[t]=n` 精确成立、条件方差 0、每步至多一发 |
| 主臂 β | **0** |
| 消融臂 β⋆ | `θ/(2T)` |
| 读出 | 膜电位解码 `argmax B̂`，`B̂=(1/T)Σ_t inst_t`，`inst_t = R(A(s_t W2))+b2`；对照为计数读出 `argmax Σ_t s_t` |
| θ / T（E17 冻结工作点） | MNIST θ=1.5, T=3；CIFAR10 θ=1.0, T=3 |
| 掩码时机 | **转换前固定**：先训全宽 base teacher，用**训练集**激活幅度排序生成 mask，再以 `unit_mask` 从头训练窄网络；不用 val/test |
| 数值精度 | `convert_f64`（`run_e17.py`）全程 float64；`identity_f64` 检查 max\|B̂−B − R A(E1W2)\|，实测 4.88e-15 ~ 1.38e-14；fp32 前向与 fp64 重算差 3.7e-7 |

## 4. 与提示词 T0「k=16」的口径差异（必须在 REPRO.md 里说明）

提示词把宽度因子写作 `k ∈ {16, 128}`。代码里真正的因子是 **`unit_mask` 的 `keep_frac`**：ANN 的 hidden 宽度恒为 128，**转换时的有效宽度由 mask 决定**。

- 论文现值（E17）不是 `hidden=16`，而是 **`hidden=128 + unit_mask(keep_frac=0.08)`**（≈10 个存活单元）+ margin 正则 + θ/T 工作点。
- 因此本任务的 T0 复现采用**代码现值配置**（hidden 128 + keep_frac=0.08 + margin=0.4/0.2 + θ=1.5/1.0 + T=3），而非字面 `hidden=16`。若按字面 `hidden=16` 复现，teacher 会显著不同，属于**配置差异**而非管道错误。
- 因子解释：`k=16` ≈ 「窄网（mask 后少量存活单元）」，`k=128` ≈ 「全宽（无 mask）」。T1–T5 的宽度主效应即为「有无 mask」。

## 5. 能量口径（45 nm 理论操作计数，非硬件实测）

- ANN MACs = `E·F + N·F·H + E·H + N·H·C + N·C`
- 主口径 `R_prim = MAC·4.6 / (AC·0.9)`，`AC = S·(H + d̄·C)`，`d̄=E/N`
- 保守口径 `R_cons = MAC·4.6 / (0.9·S·H + 4.6·T·E·C)`（把实值传播按 MAC 计价）
- 退化保护：`S=0` 或 `AC≈0` 时记为 0 并打 `zero_spike_degenerate` 标记，**不得作为能效优势**
- 可采用条件：teacher ≥ 2× chance（10 类 → ≥20%）；低于该阈值的点即使 loss≈0 也不算达标

## 6. 环境与复现

- Conda 环境 `dyg-cold`：Python 3.13.13、torch 2.11.0+cu128、torch_geometric 2.8.0.post1、numpy 2.4.4、scipy 1.18.0、matplotlib 3.10.1、pandas 2.3.3
- 固定 `torch.manual_seed`、`numpy.random.seed`、`random.seed`；CUDA 稀疏归约非确定 → 每点 5 seeds 并报 mean±std/95% CI
- 原始结果：`results/local_full*`、`results/e1`…`e18`；论文现值取 `results/e17/confirmation.json`（holdout seeds 10–14）
