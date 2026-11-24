# E13 多 seed 稳健选点 + 恒等式残差定位

## 1. E13：CIFAR10 有稳健点，MNIST 权衡卡死

`results/e13/val_multiseed.json`（108 行/数据集，17m43s，val seeds 0/1/2，**test 未碰**）。按 3-seed 均值执行严格四条。

| 数据集 | qualifying | 说明 |
|---|---:|---|
| MNIST | **0** | 精度最好的点 `keep=0.2,θ=1,T=4` loss 1.133pp 但能耗仅 2.317/2.657×；能耗够的 `keep=0.1,θ=1,T=2` 为 7.080/6.797× 但 loss 2.667pp |
| CIFAR10 | **1** | `keep=0.08, θ=1.5, T=4`：loss **1.5pp**(std 0.497)、primary **8.302×**、conservative **5.185×**，逐 seed 最小 8.194/5.162×，teacher 27.17% |

MNIST 的 3-seed val Teacher 其实不错（keep=0.3 达 54–59.5%），但**精度与能耗在此配置下不能同时达标** —— 这是真实权衡，不是实现 bug。CIFAR10 的点跨 3 个 seed 稳定，可作为版本化新筛选结果，待用未暴露 holdout（seeds 10–14）做 5-seed 确认。

## 2. 恒等式残差：定位为 fp32 前向数值精度，不是理论失效

`protocols/diag_identity.py` 在窄网络（unit_mask）上实测：

```
max|fp32 B1 - fp64 inst1|        = 3.7158e-07
max|fp32 H1 - fp64 H1|          = 3.7158e-07
spike-train L1 diff (fp32 vs fp64 inst1) = 0.0
identity_f64 (current)          = 1.0180e-07
identity using convert's own fp32 trains = 1.0180e-07
```

结论：

- `convert` 的 `inst1 = A@(X@W1)` 是 **fp32 sparse matmul**，累加误差 3.7e-7；`identity_f64` 用 fp64 重算，两者基准不一致 → 残差被锁在 1e-7 量级。
- 两条路径产生的**脉冲序列完全一致**（L1 差 0），说明确定性两阶段调度本身精确；恒等式 `B̂−B = R A(E₁W₂)` 在数学上成立，只是无法在 fp32 实现上验证到 <1e-10。
- 之前「修复后 4.13e-15」只在**未剪枝小网络**上成立（那里 A@X@W1 的 fp32 误差更小），不能推广到目标配置。

**修法（E14，待做）**：让 `convert` 的校验路径与实现走同一套 fp64 前向 —— 把 `A/R/X/W1/W2` 全部转 fp64 后再算 `inst1`、`out_t` 与累加器，消除 fp32 sparse matmul 的误差源。这属于实现修复，不改理论、不改目标。

## 3. 当前冻结目标状态（准确）

| 目标 | 状态 |
|---|---|
| 横评 T≤4 领先 ≥1.0pp | **PASS**（5-seed 全量 43.67 / 19.85pp） |
| 带内能耗 ≥5×（两套口径） | **PASS**（E11 seeds0–4 + E12 seeds5–9，10 个独立 seed 全部 ≥5×） |
| 精度 T≤8 进 1.5pp 带 | **未闭合**（E12 test 4.08 / 1.85pp；E13 3-seed val：MNIST 无稳健点、CIFAR10 1 个待 holdout 确认） |
| 恒等式 <1e-10 | **未闭合**（目标配置 2e-7，已定位为 fp32 数值精度，E14 修） |

**P5 blocked，P6 写作禁止。** 故事五条定位、四项 `expected_strong`、CVPR 8 页硬限未改。

## 4. 已启动 E15：margin 正则冲 MNIST 精度带

`protocols/run_e15_margin.py`（`uve5Bo`）：给 `train_ann` 加 hinge margin 正则 `margin_coef · mean(relu(1−(logit_true − max_rival)))`，依 1028 `T=O(‖a_n‖‖DW‖/Δ)` 增大 Δ 降低低 T 转换误差。扫 `margin_coef∈{0,0.05,0.2,0.5}` × `keep∈{0.1,0.2}`(MNIST)/`{0.08,0.15}`(CIFAR10) × θ × T，2 个 val seeds 聚合、严格四条、val-only、test 不碰。

后续并行路径：E14（fp64 恒等式实现修复）、CIFAR10 新工作点的 seeds 10–14 holdout 确认、E6 同规模配对对照。
