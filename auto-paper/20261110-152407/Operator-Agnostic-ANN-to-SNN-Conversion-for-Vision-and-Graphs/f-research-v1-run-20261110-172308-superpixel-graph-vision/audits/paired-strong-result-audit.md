# Paired Strong-Result Audit

> 生成 2026-11-10T22:10:24.541180｜v1 runs 10，v2 runs 10
> 来源：本机 3060 CUDA 两份真实 `result.json`；**不是** novix `20049` 的产物。
> 政策：`contracts/strong-result-no-retreat.md`，故事与目标冻结，只按改进路径冲。

## 5-seed conversion loss（越低越好）

| 数据集 | T | v1 带 β* | v2 去 β* | 配对改善 | v2 95% CI |
|---|---|---:|---:|---:|---:|
| MNIST | 1 | 52.32 | 43.57 | 8.75 | ±6.835 |
| MNIST | 2 | 45.23 | 21.77 | 23.46 | ±6.568 |
| MNIST | 4 | 32.44 | 6.29 | 26.15 | ±1.261 |
| MNIST | 8 | 14.64 | 3.1 | 11.54 | ±1.364 |
| MNIST | 16 | 5.75 | 2.0 | 3.75 | ±1.266 |
| CIFAR10 | 1 | 26.22 | 20.74 | 5.48 | ±1.846 |
| CIFAR10 | 2 | 25.13 | 9.65 | 15.48 | ±1.191 |
| CIFAR10 | 4 | 20.47 | 3.47 | 17.0 | ±1.848 |
| CIFAR10 | 8 | 13.31 | 2.13 | 11.18 | ±1.431 |
| CIFAR10 | 16 | 7.08 | 1.95 | 5.13 | ±1.501 |

## 相对最强单点转换基线的领先（v2）

| 数据集 | T | 领先 (pp) | 95% CI |
|---|---|---:|---:|
| MNIST | 4 | 43.67 | ±2.002 |
| MNIST | 8 | 46.48 | ±1.921 |
| CIFAR10 | 4 | 19.85 | ±2.316 |
| CIFAR10 | 8 | 21.85 | ±2.023 |

## 理论算术能耗比 ANN/SNN（45 nm 估算，非硬件实测）

| 数据集 | T | v1 | v2 |
|---|---|---:|---:|
| MNIST | 1 | 1.89 | 8.558 |
| MNIST | 2 | 1.538 | 3.204 |
| MNIST | 4 | 1.039 | 1.511 |
| MNIST | 8 | 0.615 | 0.743 |
| MNIST | 16 | 0.336 | 0.371 |
| CIFAR10 | 1 | 3.058 | 16.471 |
| CIFAR10 | 2 | 2.569 | 5.717 |
| CIFAR10 | 4 | 1.776 | 2.651 |
| CIFAR10 | 8 | 1.066 | 1.301 |
| CIFAR10 | 16 | 0.588 | 0.647 |

## 冻结强目标判定

### MNIST
- `accuracy_1_5pp_at_Tle8`：目标 <=1.5pp at any T<=8，实测 3.1，未达/待核
- `baseline_margin_1pp_at_T4`：目标 >=1.0pp，实测 43.67，PASS
- `energy_5x_within_band`：目标 >=5x at a T inside the 1.5pp band，实测 None，未达/待核
- `energy_max_any_T_reference_only`：目标 reference only; NOT an acceptance criterion，实测 8.558，未达/待核
- `identity_residual`：目标 <1e-10，实测 —，未达/待核

### CIFAR10
- `accuracy_1_5pp_at_Tle8`：目标 <=1.5pp at any T<=8，实测 2.13，未达/待核
- `baseline_margin_1pp_at_T4`：目标 >=1.0pp，实测 19.85，PASS
- `energy_5x_within_band`：目标 >=5x at a T inside the 1.5pp band，实测 None，未达/待核
- `energy_max_any_T_reference_only`：目标 reference only; NOT an acceptance criterion，实测 16.471，未达/待核
- `identity_residual`：目标 <1e-10，实测 —，未达/待核

## 读法

- v2 未完成全部 seeds 时，其数值按已完成 seeds 计算，并在 `paired_analysis.json` 记录 `n_v2`。
- 未达项按 `strong-result-no-retreat.md` 只走改进重跑，不改定位、不降阈值、不挑 seed。
- CUDA 稀疏归约非确定，v1/v2 的 ANN 有约 0.5pp 差异；配对比较一律用各自运行内的 conversion loss。
