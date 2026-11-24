# E10 突破：找到严格达标工作点（val / 单 seed）

> 数据源：`results/e10/val_sweep.json`（75 组/数据集，421.2 s，val-only，seed 0），脚本 `protocols/run_e10.py`。
> 严格四条：teacher val ≥ 20%（2× chance）、loss ≤ 1.5pp、非零脉冲、primary 与 conservative 都 ≥ 5×。

## 1. STRICT QUALIFYING 点

| 数据集 | keep | 单元数 | θ | T | teacher | loss | primary | conservative | spikes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MNIST | 0.1 | 13 | 1.5 | 3 | 31.0% | **1.2pp** | **5.8007×** | **5.0439×** | 420,385 |
| CIFAR10 | 0.08 | 10 | 1.0 | 3 | 27.6% | **−0.8pp** | **7.5251×** | **5.9554×** | 584,516 |
| CIFAR10 | 0.08 | 10 | 1.0 | 2 | 27.6% | **1.0pp** | **11.4032×** | **8.9725×** | 383,936 |

两个数据集**都**有工作点同时满足精度带与两套能耗口径。MNIST 有 1 个 Q、CIFAR10 有 2 个 Q；另有 MNIST 40 行、CIFAR10 55 行通过「有效 teacher + 非零脉冲 + 双 5×」三条（只差 loss）。

**这是 E9 转折的落地**：低 T（T=2/3）把 conservative 口径的 `T·E·C·4.6pJ` 项压下来，窄网络（10–13 个存活单元）把 spike 数压到 38–58 万，两者叠加后 45 nm 理论算术能耗比稳定站上 5×，同时 teacher 保持 27.6–31.0%（远高于 20% 门槛）。

## 2. 必须说清的边界（不夸大）

1. **这是 validation-only、单 seed=0 的筛选结果，不是正式 P4/P5 结果。** 工作点是在 val 上从 75 组里选出来的，存在选择偏差；按 `f-research-v1` 的 test 隔离规则，必须在**冻结工作点**后做 5-seed 确认、test 只评一次。
2. **teacher 绝对精度偏低**：MNIST 31.0%、CIFAR10 27.6%（10 类 chance 10%）。虽通过 2× chance 门槛且 conversion loss 很小，但绝对精度不是 SOTA 水平；论文里不得包装成精度优势，主张仍是「组合方法在图结构视觉上的转换保真 + 能效」。
3. MNIST 的 conservative 余量很小（5.0439×，仅高出 0.044），5-seed 均值可能掉到 5× 以下；CIFAR10 选 T=3 的点（5.9554×、loss −0.8pp）余量更足。
4. 能耗仍是 **45 nm 理论算术能耗估算，非硬件实测**；两套口径始终同时报告。

## 3. E11：冻结工作点的 5-seed 确认（已启动）

`protocols/run_e11.py`，**工作点写死、不再调参**：

| 数据集 | 冻结 (keep, θ, T) |
|---|---|
| MNIST | `(0.1, 1.5, 3)` |
| CIFAR10 | `(0.08, 1.0, 3)` |

2 数据集 × 5 冻结 seeds，每 seed 重新训练窄网络并在**各自 test 上评一次**；报告 5-seed loss 均值±std/CI、两套能耗均值与最小值、float64 恒等式残差、teacher 均值。判定：两数据集 `loss_mean ≤ 1.5pp` 且 `energy_primary_mean ≥ 5` 且 `energy_conservative_mean ≥ 5` 且 `ann_mean ≥ 20%`。

## 4. 若 E11 通过

四项冻结目标将全部有证据：横评领先（5-seed 全量 43.67/19.85pp）、恒等式（float64 ~1e-14）、精度带、带内能耗 5×。届时可回填 P3A/P4/P5 → P5A → **P6–P21 写作与 CVPR 排版链**（正文 ≤8 页、官方模板、双盲）。

若 E11 未通过（尤其 MNIST conservative 余量小），按 `strong-result-no-retreat.md` 继续 E3 margin 正则（依 1028 `T=O(‖a_n‖‖DW‖/Δ)` 增大 Δ 降低所需 T），不改故事、不降目标。

## 5. 状态

- 当前 P5 仍 **blocked**（尚缺 5-seed 确认），P6 写作禁止。
- 故事五条定位、四项 `expected_strong`、CVPR 8 页硬限未改。
- 所有历史假达标（零脉冲 1e20×、退化 teacher 假 0pp）已识别剔除，未写入结论。
