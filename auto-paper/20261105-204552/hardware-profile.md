# Hardware / Runtime Profile（本机探测）

探测时间：2026-11-05 20:40 GMT+8，方式：`f-guidance-builder-v1/scripts/hardware_probe.py`
在 `base` 环境运行 + `nvidia-smi` + 各 Conda 环境 `importlib.util.find_spec` 逐个核验。
用户长期偏好：**代码一律在本机 Conda 里跑**，远程算力需显式授权。

## 主机

| 项 | 值 |
|---|---|
| OS | Windows 11 (AMD64) |
| CPU 逻辑核 | 12 |
| GPU | NVIDIA GeForce RTX 3060，12,288 MiB（探测时空闲 10,867 MiB） |
| 驱动 | 591.74 |
| CUDA（torch 内置） | 12.8 |
| 工作区磁盘空闲 | 547,572,613,120 B ≈ 510 GiB |
| 物理内存 | probe 的 `memory_bytes` 在 Windows 返回 `null`；未据此推断数值 |

## Conda 环境清单（`conda env list`）

`base`, `dyg-cold`, `dyg-writing`, `jiewu-research`, `siigm`, `spikinggcn36`，
另有两个无名称的本地环境目录。

## 关键依赖矩阵

| 环境 | Python | torch | PyG | torch_scatter | spikingjelly | cv2 | 结论 |
|---|---|---|---|---|---|---|---|
| **dyg-cold** | 3.13.13 | 2.11.0+cu128 | 2.8.0.post1 | 有 | 有 | 有 | **冒烟实验首选**：PyG + SNN + 视觉三方齐备 |
| base | 3.13.13 | 2.11.0+cu128 | 有 | 无 | 有 | 有 | 备选，缺 torch_scatter |
| spikinggcn36 | 3.6.15 | 有 | 无 | 无 | 有 | 无 | 老 SNN 环境，仅备用 |
| siigm | 3.11.15 | 有 | 无 | 无 | 无 | 无 | 不适用 |
| jiewu-research | 3.13.13 | 有 | 无 | 无 | 无 | 有 | 不适用 |

## 对实验规模的约束

- 12 GB 显存：无法对 166k 神经元 / 5450 万突触整图做长序列 BPTT；
  必须取视叶子图（几千至几万节点）、短时间序列（T=8~16）、小 batch。
- `train-your-fly` 论文环境是 torch 2.6.0 + PyG 2.6.1 + torch-scatter 2.1.2 + torch-sparse 0.6.18；
  本机 `dyg-cold` 是 torch 2.11 / PyG 2.8，缺 `torch_sparse`，**直接复现官方代码需兼容性验证**，
  这是冒烟实验必须首先检查的事项。
- 数据下载预算：单份 <= 1.5 GB（MaleCNS 全图 1.1 GB 或 train-your-fly 图包 1.3 GB）。
