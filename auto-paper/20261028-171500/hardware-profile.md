# Hardware Profile — 本机条件（f-guidance-builder-v1）

探测时间：2026-10-28｜环境：base conda（C:/Users/xhf/miniconda3/python.exe）

## 本机规格（来自 hardware_probe.py）
- OS：Windows 11（AMD64）
- CPU：12 核
- 内存：未上报（probe 未读到；按 16–32GB 典型 Windows 桌面估算，需后续确认）
- 磁盘空闲：568 GB（充足）
- Python：3.13.13
- PyTorch：2.11.0+cu128（已装）
- **GPU：NVIDIA GeForce RTX 3060，12 GB VRAM，CUDA 13.1，cuda_available=True，device 数=1**
- 推荐设备：cuda（MPS 不可用，符合 Windows 预期）
- 隐私：序列号/UUID/用户名/主机名/网络标识已省略

## 对方案的意义（G5 硬件可行性）
- RTX 3060 12GB 足以本地运行**中小规模 SNN 实验**：Cora/CiteSeer/PubMed 等小图节点分类、SEED 系列 EEG、小规模时序/动态图，单卡分钟–小时级。
- **无需上云**（除非 D2/D4 扩展到超大图或 ImageNet 级视觉，那时再申请远程/集群，且需用户显式授权）。
- 工具链：SpikingJelly（开源，PKU/中科院）支持 ANN2SNN 转换、替代梯度训练、权重量化、神经形态部署；吴老师的 FTBC/TPP/并行转换方法可在其上实现/集成。

## 待确认
- 精确内存容量（影响 batch/图规模上限）。
- 是否已有 conda 环境装了 spikingjelly / torch（base 有 torch；spikingjelly 需 `pip install spikingjelly`）。
- D1/D3 是否要建独立项目 conda env（建议：phd-snn 专属 env，如 `snn-convert`）。
