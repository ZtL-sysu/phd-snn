# P3 · Baseline-First Reproducibility Record

> **性质声明**：以下全部是**本机 3060 CUDA、单 seed=0、MNIST 超像素图子集（train 2000 / val 500 / test 500）的预实验 smoke 数值**，不是正式 P4 结果，不得写进论文主表。正式全量在 novix task `20049` 的 4090 上执行。

## 环境与数据

| 项 | 值 |
|---|---|
| 设备 | NVIDIA GeForce RTX 3060 12288 MiB, CUDA 12.8, torch 2.11.0+cu128 |
| 环境 | `dyg-cold`, Python 3.13.13, numpy 2.4.4, scipy 1.18.0, PyG 2.8.0.post1 |
| 数据 | 官方 SuperPixel MNIST (`MNIST_v2.zip`, 192,378,381 B)，PyG `GNNBenchmarkDataset` |
| 图结构 | test 系统 N=35,219 节点 / G=500 图 / F=3 / C=10 / E=376,695；`rho_mean=0.9987, rho_max=1.1057` |
| 配置 | hidden=128, lr=0.01, epochs=800, sum pooling, gauge scale 0.5435, device=cuda |
| 运行时间 | 66.87 s（单 seed 全套六方法 × 5 T + 消融 + 恒等式） |
| 结果文件 | `results/gpu_MNIST_seed0.json` |

## Baseline-first 结果（真实实跑）

| 方法 | T=1 | T=2 | T=4 | T=8 | T=16 |
|---|---:|---:|---:|---:|---:|
| ANN teacher（上限） | 68.80 | 68.80 | 68.80 | 68.80 | 68.80 |
| naive rate | 9.0 | 10.8 | 10.8 | 10.8 | 10.8 |
| qcfs | 9.0 | 15.0 | 11.2 | 11.2 | 11.2 |
| ftbc | 20.8 | 21.0 | 20.0 | 16.8 | 11.4 |
| tpp | 11.2 | 11.2 | 11.2 | 11.4 | 11.4 |
| parallel | 14.8 | 20.0 | 21.6 | 20.2 | 17.8 |
| **ours（1028 组合）** | 10.8 | 22.0 | 41.8 | 60.2 | **66.8** |

teacher train/val/test = 68.9 / 66.8 / 68.8%。**ours 的 conversion loss 随 T 单调下降**：T=16 为 2.0pp（未达 1.5pp strong，落在 3.0pp minimum 内）。

## 恒等式与消融

| T | `max_abs_identity_residual` | `argmax_agreement` |
|---|---:|---:|
| 1 | 3.24e-05 | 0.126 |
| 2 | 1.47e-05 | 0.254 |
| 4 | 9.54e-06 | 0.486 |
| 8 | 7.51e-06 | 0.744 |
| 16 | 6.41e-06 | 0.878 |

残差为 float32 累加量级，**未达 <1e-10 目标** → 已作为 H3 交给远端用 float64 重算，不宣称「已精确验证」。

T=8 消融：`ours_no_beta` 66.2%、`ours_naive_if` 66.2%、`ours_tpp_phase` 46.4%、`ours_count_readout` 14.8%。
- 膜电位解码贡献巨大（计数读出仅 14.8%）→ 1028 的核心组件在本场景被验证。
- **去 β* 与朴素 IF 反而优于完整 ours** → β* 与确定性两阶段可能冗余，已作为 C1 负结果交给远端全量复核，不删除、不美化。

## 理论算术能耗（45 nm，非硬件实测）

| T | ANN/SNN 能量比 | ours 总脉冲数 |
|---|---:|---:|
| 1 | **1.605×** | 1,472,976 |
| 2 | **1.296×** | 1,827,689 |
| 4 | 0.863× | 2,749,354 |
| 8 | 0.508× | 4,679,417 |
| 16 | 0.277× | 8,588,651 |

**真实结论：能耗优势只在 T≤2 出现且仅 1.3–1.6×，T≥4 反转为劣势，远未达预注册的 5×**。用户预判「一定有优势」在这个口径下不成立；已作为 B1/C2 写入 concern ledger，并要求远端同时报保守口径两套管比值后裁定。这不是口径调整的空间，而是必须如实报告的负结果信号。

## P3 gate

Baseline-first 顺序已满足（ANN teacher → 朴素 rate → QCFS/FTBC/TPP/Parallel → ours），六方法在同一 teacher、同一 T/θ/split 下跑通，复现产物（JSON、脚本、配置）齐备。**P3 pass（限于本机 smoke 层）**；全量基线证据待 novix `20049` 回收后由 P3A 复核。
