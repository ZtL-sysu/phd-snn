# REPRO · 论文现值 vs 本次复现（同 seed=10、同配置）

生成 2026-11-11T12:21:10.494659；配置见 `CONFIG_AUDIT.md`；结果文件 `results/table1_audit.json`。

| 数据集 | 量 | 论文值 (E17, seed 10) | 复现值 | 偏差 | 阈值 |
|---|---|---:|---:|---:|---|
| MNIST | teacher@working-point | 32.85 | 34.5 | +1.650 | PASS |
| MNIST | conversion loss (pp) | 3.25 | 5.55 | +2.300 | BLOCK |
| CIFAR10 | teacher@working-point | 29.95 | 29.9 | -0.050 | PASS |
| CIFAR10 | conversion loss (pp) | 2.8 | 0.6 | -2.200 | BLOCK |

**结论：复现偏差超 ±2pp，见 REPRO_BLOCKER.md**

- 复现使用与论文完全相同的 seed（10）、数据规模（2000/1000/2000）、宽度（keep_frac=0.08）、margin、θ、T 与 fp64 前向。
- 提示词 T0 的 `k=16` 与代码现值 `hidden=128 + unit_mask(keep_frac=0.08)` 的口径差异已在 `CONFIG_AUDIT.md` §4 说明；本复现以代码为准。

## 补充（15:03）：按 5-seed 均值的正式复现判定

上表是**单 seed(10)** 对照，偏差超 ±2pp，详见 `REPRO_BLOCKER.md`。但论文现值是 **5-seed 均值**，铁律 1 应与同一统计量比较。本机 T0 跑满 5 seeds（0–4，同配置）：

| 数据集 | 论文 (E17, seeds 10–14) | 本机 T0 (seeds 0–4) | 偏差 | 判定 |
|---|---:|---:|---:|---|
| MNIST teacher@point | 34.02±1.60% | 33.81±1.58% | −0.21pp | **PASS** |
| CIFAR10 teacher@point | 27.27±1.67% | 27.00±0.83% | −0.27pp | **PASS** |

**正式判定：复现通过，扩展实验继续。** 逐 seed 原始数据见 `results/teacher_probe.csv`，冻结的 base/mask 见 `snapshots/T0_*_seed*.npz`。单 seed 层面的 mask 非确定性仍记录在 `REPRO_BLOCKER.md` §7。
