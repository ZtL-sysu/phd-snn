# E7 结果：结构性剪枝暴露「退化 teacher 假达标」陷阱

> 数据源：`results/e7/val_sweep.json`（30 行/数据集，93.7 s，val-only，seed 0）、`results/e7/refiltered.json`。

## 1. 表面结果与真实结果

| 数据集 | naive qualifying | **strict qualifying** | 说明 |
|---|---:|---:|---|
| MNIST | 3 | **0** | naive 点全在 `prune≥0.9`，teacher val 8.6–10.4% |
| CIFAR10 | 5 | **0** | naive 点全在 `prune≥0.5`，teacher val 8.2–10.6% |

10 类任务的 chance 是 10%。**剪掉 50% 以上单元后 teacher 立刻塌到 chance 附近**：MNIST 66.2% → 13.0% → 12.8% → 10.4% → 8.6%；CIFAR10 35.4% → 9.6% → 10.0% → 10.6% → 8.2%。

于是出现一个极具误导性的组合：`val_loss_pp ≈ 0`（ANN 和 SNN 一起崩到随机，相对差自然为 0）+ `energy_primary 20.63× / 24.99×`（几乎不发放脉冲）。若不检查 teacher 绝对精度，就会被当成「1.5pp 带内 + 5× 能耗」双达标。

## 2. 判定规则的第二个漏洞（已修补）

继 E2 的「零脉冲 → 1e20× 假优势」之后，E7 暴露了第二个：**conversion loss 是相对量，分母（ANN teacher）失效时它照样能达标**。

修正后的严格选点规则，四条必须同时成立：

1. **teacher val accuracy ≥ 2 × chance**（10 类 → ≥ 20%）—— 绝对精度门槛
2. `val_loss ≤ 1.5pp`
3. `total_spikes > 0` 且 `zero_spike_degenerate = false`
4. primary 与 conservative **两套**能耗口径都 ≥ 5×

`results/e7/refiltered.json` 用此规则重筛：两数据集 **strict Q = 0**。保留有效 teacher 的行只有未剪枝（`prune=0`）的 6 行，其最佳能耗仅 MNIST 0.61/0.85×、CIFAR10 1.12/1.35×（在 loss≤1.5pp 处），或 loss 15.8/17.8pp 处也不过 2.05/4.13×。

**结论：直接剪枝训练好的宽网络不可行，它摧毁 teacher 而不是压缩它。**

## 3. E8：换一条真正可能有效的路

E7 的错误在于「先训宽网络、再截肢」。1028 `core.py` 的 `unit_mask` 机制本意是 **prune-and-finetune**：保持 mask 不变，让存活单元继续学习。E8 进一步做成**从头训练窄网络**：

- 给 `vision_pipeline.train_ann` 加 `unit_mask` 参数，每步 `opt.step()` 后把 `W1[:, ~mask]`、`b1[~mask]`、`W2[~mask, :]` 精确置零；
- 扫 `keep∈{1.0, 0.5, 0.2, 0.1, 0.05}` × `θ∈{1,2,4}` × `T∈{4,8}`；
- 严格四条判定，val-only，**test 不碰**。

如果窄网络能重新学到显著高于 chance 的精度，就有可能在真实有效的前提下把 spike 数降一个数量级，从而同时满足 1.5pp 带与 5× 能耗。这是当前唯一还有物理希望的改进路径。

## 4. 状态

- 冻结目标仍为 **2 PASS（横评、恒等式）/ 2 未达（精度带、带内能耗 5×）**；P5 blocked，P6 写作禁止。
- 所有假达标点已识别、标记并从候选中剔除，**没有**把它们写进任何结论。
- 故事五条定位、四项目标、CVPR 8 页硬限未改。
