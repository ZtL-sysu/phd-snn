# E12 新 holdout 确认：精度带改善但未闭合，恒等式项需更正

> 数据源：`results/e12/confirmation.json`（10/10 runs，669.8 s），脚本 `protocols/run_e12.py`。
> 与 E11 相同**冻结工作点**（MNIST `(0.1,1.5,3)` / CIFAR10 `(0.08,1.0,3)`），但换全新 holdout **seeds 5–9**、`n_test` 500→**2000**、使用修复版 `identity_f64`。E11 的 seeds 0–4 test 已用于诊断，按 test 隔离规则视为 exposed，未复用。

## 1. 5-seed 结果

| 数据集 | teacher 均值±std | loss 均值±std (CI95) | primary 均值 (最小) | conservative 均值 (最小) |
|---|---:|---:|---:|---:|
| MNIST | 35.94±1.83% | **4.08±2.18pp** (±1.910) | **7.773×** (6.698) | **5.725×** (5.385) |
| CIFAR10 | 27.56±2.03% | **1.85±0.86pp** (±0.749) | **7.889×** (6.482) | **6.024×** (5.568) |

逐 seed loss：MNIST 6.00/0.40/2.95/4.80/6.25，CIFAR10 2.85/0.35/2.40/2.05/1.60。

**扩大 test 集 + 新 holdout 有效**：相对 E11（MNIST 6.20±2.75、CIFAR10 3.20±1.04）两组都下降，std 也收窄。CIFAR10 均值 1.85pp、CI 下界 1.10pp，距 1.5pp 只差 0.35；MNIST 仍差 2.58pp。

**能耗 5× 在两组独立 holdout 上都稳定 PASS**：E11(seeds 0–4) 与 E12(seeds 5–9) 的 5-seed 均值与逐 seed 最小值全部 ≥5×。这是目前最扎实、可写进论文的结果。

## 2. 更正：恒等式项在目标配置下未闭合

上一轮曾说「修复后恒等式 PASS」，那只基于**未剪枝小网络**的冒烟测试（4.13e-15）。E12 在真实目标配置（窄网络 + unit_mask）上实测 `identity_f64_residual` 为 **1.56e-07 ~ 4.67e-07**，仍远大于冻结目标 `<1e-10`。

因此当前准确状态是：

| 目标 | 状态 |
|---|---|
| 横评 T≤4 领先 ≥1.0pp | **PASS**（5-seed 全量 43.67 / 19.85pp） |
| 带内能耗 ≥5×（两套口径） | **PASS**（E11 + E12 两组独立 holdout） |
| 精度 T≤8 进 1.5pp 带 | **未达**（4.08 / 1.85pp） |
| 恒等式残差 <1e-10 | **未闭合**（目标配置 2e-07；未剪枝 4e-15） |

**P5 blocked，P6 写作禁止。** 不把 4e-15 的未剪枝冒烟值冒充目标配置的结果。残差来源待定位（疑为 `convert` 的 fp32 `inst1` 与 fp64 校验路径不一致），列为 E14。

## 3. E13：消除单 seed 选择偏差（已启动）

E10 的工作点是按 **seed 0 单 seed val** 从 75 组里选出的，E11/E12 的 val→test 落差与此直接相关。`protocols/run_e13.py` 做**多 seed val 稳健选点**：

- `VAL_SEEDS=(0,1,2)`，每个 (数据集, seed, keep) 重新训练窄网络；
- 网格：MNIST `keep∈{0.1,0.15,0.2,0.3}`、CIFAR10 `keep∈{0.08,0.1,0.15,0.2}`，`θ∈{1,1.5,2}`、`T∈{2,3,4}`；
- 在各自 val 上评估，按 **3-seed 平均** 聚合；选 `avg_loss ≤1.5pp` 且 `avg_primary ≥5` 且 `avg_conservative ≥5` 且 teacher ≥20% 的点，取余量最大；
- **全部 val-only，test 不碰**。

选出的新工作点将作为版本化新筛选结果冻结，再用**另一组未暴露 holdout**（seeds 10–14）做 5-seed 确认，避免自适应评估污染。

若多 seed val 仍无稳健点，按 `strong-result-no-retreat.md` 继续 **E3 margin 正则**（依 1028 `T=O(‖a_n‖‖DW‖/Δ)` 增大 Δ 降低所需 T），不改故事、不降目标。

## 4. 状态

- 故事五条定位、四项 `expected_strong`、CVPR 8 页硬限未改；`submission_ready=false`。
- 所有负结果与实现缺陷（零脉冲、退化 teacher、fp32/fp64 混算）均保留在证据链中。
