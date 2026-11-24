# E2 结果与能耗目标的理论边界

> 数据源：`results/e2/val_sweep.json`（96 行/数据集，349 s，val-only，seed 0），脚本 `protocols/run_e2.py`。
> 目标（冻结）：`val_loss ≤ 1.5pp` **且** primary 与 conservative 两套能耗口径都 `≥ 5×`。

## 1. 结果：0 个达标点

| 数据集 | 扫描行数 | qualifying | loss≤1.5pp 下的最佳能耗比 |
|---|---:|---:|---|
| MNIST | 96 | **0** | primary 1.226× / conservative 1.384×（`θ=2, T=8`） |
| CIFAR10 | 96 | **0** | primary 2.270× / conservative 2.718×（`sparsity=1e-3, scale=0.5, θ=2, T=4`） |

**软稀疏化惩罚基本无效**：`sparsity∈{0,1e-4,1e-3,1e-2}` 下 val ANN 几乎不变（MNIST 65.8/65.6/62.4/67.4%，CIFAR10 35.8/36.0/35.2/36.0%），spike 数也几乎不变（~3.9M / ~1.9M 两档，主要由 θ 决定，不是由 sparsity 决定）。惩罚被交叉熵与 weight decay 淹没，量级不够。

## 2. 发现并修掉一个会产生假优势的口径缺陷

`θ=8` 时脉冲为零，`ac_ops→0`，`energy_primary` 算出 **4.99e20× / 9.04e20×** 这种荒谬数值 —— 但精度同时崩到 val loss 53.0pp / 26.4pp（chance 附近）。这正是「带内判定」要防的情形，说明仅靠 `loss≤1.5pp` 过滤还不够，零脉冲也必须显式排除。

已在 `vision_pipeline.energy_accounting` 加保护：`total_spikes<=0` 或 `ac_ops<=1e-9` 时把比值记为 `0.0` 并返回 `zero_spike_degenerate=true`；E7 选点时同时排除该标记。**不允许零脉冲网络被写成能效优势。**

## 3. 为什么 5× 这么难：一个可算的理论边界

45 nm CMOS 口径下 MAC = 4.6 pJ、AC = 0.9 pJ，**单操作能量比只有 4.6/0.9 ≈ 5.11×**。因此

```
ANN/SNN 能量比 >= 5  <=>  ANN_MAC * 4.6 / (SNN_AC * 0.9) >= 5
                     <=>  SNN_AC <= 1.022 * ANN_MAC
```

也就是说，**5× 目标几乎等价于「SNN 的总突触操作次数不超过 ANN 的 MAC 次数」**。当前 T=8 下 SNN 的 `ac_ops ≈ Σ_t nnz(s_t)·(H + deg_mean·C)` 远大于 ANN 的 MAC 数（实测比值 0.6–2.2×，对应 AC/MAC ≈ 2.3–8.5×）。要达标需要把 spike 数再压 **约 2–8 倍**，同时保持 1.5pp 带内精度。

这不是调口径能解决的 —— conservative 口径把 A 传播按 MAC 计，同样未达标（1.384× / 2.718×）。

## 4. 按「不退」政策的下一步

`contracts/strong-result-no-retreat.md` 禁止下调 5× 目标、禁止只挑有利口径、禁止把理论估算写成硬件实测。因此合法路径只剩**真正减少脉冲数**：

- **E7（已启动）**：结构性剪枝（unit mask），直接把隐藏单元连同其 W1 列、b1、W2 行置零，spike 数按保留比例线性下降；扫 `prune∈{0,0.5,0.8,0.9,0.95}` × `θ∈{1,2,4}` × `T∈{4,8}`，val-only 筛选，找 `loss≤1.5pp` 且两套口径 ≥5× 的点。
- **E8（若 E7 精度掉太多）**：剪枝后微调（1028 `unit_mask` 机制），在保持 mask 的前提下恢复 teacher 精度。
- **E3**：margin 正则把 1.5pp 带推进 T≤4（低 T 本身就少脉冲，可同时服务精度与能耗）。
- **E6**：同规模固定工作点配对对照（修正 E1 与 v2 规模不一致的口径问题）。

若 E7/E8/E3 穷尽后仍无达标点，按 `f-research-v1` 修正回路须如实向用户报告「在当前 45 nm 操作计数口径与本机算力下 5× 不可达」并请求方向；**不自动降级故事、不自动下调目标**。

## 5. 状态

- 冻结目标仍为 **2 PASS（横评、恒等式）/ 2 未达（精度 1.5pp 带、带内能耗 5×）**，P5 blocked，P6 写作禁止。
- CVPR 8 页模板与约束已就绪但不动正文。
- 故事五条定位、四项目标一个字未改。
