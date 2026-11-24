# Hardware Profile

> 生成 2026-11-10｜由 `f-guidance-builder-v1/scripts/hardware_probe.py` 在目标 conda 环境实跑，辅以 OS/GPU 原生查询。
> 隐私：序列号、UUID、用户名、主机名、网络标识一律不记录。

## Local Experiment Machine

- Role: 默认执行实验、训练、评估、预处理、写作与产物准备；本机承担 smoke / 基线回归 / 小数据集全量，大规模全量实验按用户授权转远端 4090
- OS: Windows 11 (10.0.26200), AMD64
- CPU: 12 逻辑核
- RAM: 技能探针未返回（`null`）；未由本轮核验，**NOT VERIFIED**
- GPU: NVIDIA GeForce RTX 3060
- GPU memory: 12288 MiB
- Disk free (工作区): 548,335,472,640 B ≈ 510.7 GiB
- CUDA: driver 591.74 / torch 报 `12.8`
- Apple MPS available: false
- Conda/Python: Miniconda；`dyg-cold` = Python 3.13.13
- Selected Conda environment: **`C:\Users\xhf\miniconda3\envs\dyg-cold`**
- Key probes: `torch 2.11.0+cu128`、`torch.cuda.is_available()=True`、device count 1、recommended device `cuda`
- 已安装：`spikingjelly`（无 `__version__` 属性，版本 NOT VERIFIED）、`numpy`
- **缺失且必须在 G6 前补装**：`torchvision`（实查 `ModuleNotFoundError: No module named 'torchvision'`）→ 否则 CIFAR-10/100 无法用 torchvision 载入，G6 blocker
- 其它可用但不适用环境：`spikinggcn36` = Python 3.6.15 / torch 1.10.2+cpu / CUDA False；`base`、`dyg-writing`、`jiewu-research`、`siigm` 本轮未核验
- 关键提示：资料库参考报告里写的「本机 conda MPS」属于**另一台机器/另一会话**，与本机不符；本文件只采信本机实测

## Optional Remote Compute

- Enabled only when: 用户在本轮明确授权「大规模实验上 novix-platform 跑」；guidance 阶段**不提交**
- Role: 全套基线 × 5 seeds × T 网格 × 多数据集的全量实验（P4）
- OS / CPU / RAM: 远端未在本轮探测，**NOT VERIFIED**（历史项目记录远端为 RTX 4090 / 46,068 MiB / CUDA 13.0 / torch 2.11.0+cu130，仅作参考，不构成本轮核验）
- GPU: 资源池 `exp-4090`（用户指定）
- Endpoint reference: 仅记非密别名 `novix / exp-4090`；**不写入任何端点、账号、令牌或凭据**
- Artifact synchronization plan: 按 `novix-platform` 技能的结果回收流程；只有解析到 JSON `status` + `finalReply` + 可 pull 的落盘产物 + SHA-256 校验一致才判终态（历史教训：平台 `status` 不可单独作权威）
- 历史风险（来自本项目日志）：控制面曾出现 `processing` 与 `failed` 同时存在、HTTP 503、静默零产物；长任务需带外通道与阶段性探测

## Experiment Budget

- Maximum runtime per run (本机 smoke): ≤ 10 min；M0 理论核验实跑 < 5 s
- Maximum runtime per run (全量单臂): ≤ 6 h（远端 4090）
- Maximum total runtime: 本机 ≤ 24 h；远端按任务实际，不设 `--max-turns`/`--timeout` 预算参数
- Maximum number of runs: 5 seeds × 5 T × (8 基线 + 7 消融 + 1 主臂) × 4 数据集分组，按 `matched-protocol.md` §6 分批，先第 0 批 PASCAL/TPP
- Maximum dataset size: CIFAR-10 170,498,071 B；CIFAR-100 169,001,437 B；Tiny-ImageNet 248,100,043 B；CIFAR10-DVS 8,384,752,624 B（须降采样）；Planetoid 逐文件公开直链
- Maximum model size: ViG-Ti 7.1M / ViG-S 22.7M 参数；ViG-B 86.8M 在本机只做推理评估
- Memory: 单卡 ≤ 12288 MiB；CIFAR10-DVS 降采样 48×48、T≤20、batch≤32–64

## Feasibility Notes

- Expected bottleneck: ① `torchvision` 缺失（G6 blocker）；② 6 个官方基线仓库建于 2022–2025，torch 2.11 兼容性 **NOT VERIFIED**，须先以 QCFS 回归测试（91.18%@T=2 / 93.96%@T=4）锁定统一环境；③ PASCAL / CS-QCFS / ECL 无官方代码，自行复现是最大工作量；④ ViG KNN 图冻结与脉冲域实现需自写；⑤ ImageNet-1K 为 G2 不可得，不做全量训练
- Scaling strategy: 本机 3060 只跑 smoke、基线回归与 CIFAR-10/100 单 seed；全量 5 seeds + Tiny-ImageNet + 事件视觉转远端 4090；ViG 用官方公开预训练权重做推理评估，避免全量 ImageNet 训练
- Risks: 远端控制面状态与产物不同步；基线复现失败必须如实登记而非用文献数值顶替；冻结 KNN 图改变 ViG 表征力，须量化精度代价
- Assumptions: `torchvision` 可补装且与 torch 2.11 匹配；6 个官方仓库在统一环境下可跑通（未验证）；远端 4090 资源池可用（未在本轮探测）

## M0 本机 smoke 实跑记录

`protocols/m0_operator_theory_check.py` 在 `dyg-cold` **修正后重跑**通过：恒等式最大残差 `9.880984919163893e-15`、Hoeffding 上界 0 违反、P3 干净隔离后相对误差 `0.3056→0.3111`（ρ=0.5→10，argmax 一致率全 1.0）、动态 A 残差 `0.7058297672203355`、max 非线性 gap `1.1668779395601996`；结果 JSON 的**磁盘字节 SHA-256（权威）** `ea4c05a67300766ed9141bb0f1e99b2407760321f32ab95dcdb6c25e5ec7575f`。详见 `evidence-snapshots/m0-theory-check.md`。
