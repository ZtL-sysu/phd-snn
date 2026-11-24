# Experiment Traceability Matrix（P4 前置，随每批更新）

> 契约：`../guidance-v2.md` §Traceability Checklist。状态取值：`done`（本机 smoke，非正式结果）/ `in-flight`（novix 20049 全量）/ `pending` / `infeasible-with-evidence`。

| Guidance requirement | 数据集 | 基线/方法/消融 | 主指标 | 本机 smoke | 全量 4090 | 证据路径 | 状态 |
|---|---|---|---|---|---|---|---|
| 恒等式在图级管线上精确成立 | MNIST/CIFAR10 | 固定线性 A+R vs 动态/非线性 | 浮点残差 | MNIST 3.24e-05→6.41e-06 | H3 float64 重算 | `gpu_MNIST_seed0.json` | in-flight |
| ANN 精度上限 | 两数据集 | ANN teacher | top-1 | MNIST 68.8% | 5 seeds × 2 数据集 | 同上 | in-flight |
| 全套转换方法横评 | 两数据集 | naive/qcfs/ftbc/tpp/parallel/ours | conversion loss | MNIST 六方法 ×5 T 完成 | 5 seeds 全量 | `gpu_MNIST_seed0.json` | in-flight |
| 1028 组合主臂 | 两数据集 | ours + Variant A/B | top-1 / conversion loss | MNIST T=16 66.8% | 同上 | 同上 | in-flight |
| 闭式偏置贡献 | 两数据集 | 消融 去 β* | conversion loss / margin | MNIST T=8 去 β* 66.2% > ours 60.2% | 配对差值 + CI | 同上 | in-flight（负结果保留） |
| 膜电位解码贡献 | 两数据集 | 消融 计数解码 | conversion loss | MNIST T=8 计数 14.8% | 配对差值 + CI | 同上 | in-flight |
| 确定性第二相 | 两数据集 | 消融 TPP 随机相 | Σs=n / 方差 / loss | MNIST T=8 46.4% | 5 seeds | 同上 | in-flight |
| ANN vs SNN 能耗对照 | 两数据集 | ANN teacher vs ours | MAC/AC/能量比 | MNIST T=1 1.605× → T=16 0.277× | primary + conservative 两套口径 | 同上 | in-flight（优势仅 T≤2） |
| 统计稳健性 | 两数据集 | 全部方法 | 配对 CI / BH q | 单 seed，无 CI | 5 seeds + bootstrap | 远端 `result.json` | pending |
| 算子与阈值鲁棒性 | 两数据集 | 三种归一化、两种池化、θ∈{0.5,1,2} | conversion loss | 仅对称归一化 + sum pooling | H2 加 `sym_norm=False` | 远端 `result.json` | pending |
| 复现 1028 回归锚点 | Cora/CiteSeer/PubMed | 1028 原管线 | 节点分类 top-1 | 未跑 | 待排期 | `contracts/core-1028.snapshot.py` | pending |
| 数据划分与 test 隔离 | 两数据集 | 全部 | split SHA-256 / trial ledger | 官方 split 子集、seed 0 | 冻结 seeds 0–4 | 远端 `config.json` | in-flight |

## 批次记录

| 批次 | 时间 | 位置 | 内容 | 结果 |
|---|---|---|---|---|
| smoke（CPU） | 17:2x | 本机 | mean pooling、未 gauge | ANN 24%，暴露梯度稀释与激活尺度问题，保留为失败证据 |
| smoke2（CPU） | 17:3x | 本机 | 加入 pos 特征 | ANN 21.67%，能耗比 0.34× |
| smoke3（CPU） | 17:4x | 本机 | gauge 变换 | ANN 24.33%，能耗比 0.42× |
| 诊断 | 17:5x | 本机 | loss 曲线定位 | mean pooling 1/n 稀释梯度约 70× |
| 诊断 | 17:5x | 本机 | sum pooling | 500 epoch 到 48.2% |
| CUDA sweep | 18:0x | 3060 | hidden/lr/epoch 扫描 | hidden=128/lr=0.01/800ep → train 67.5%, val 68.2%；GPU 13–28 s vs CPU 50–216 s |
| gpu smoke | 18:0x | 3060 | 完整六方法矩阵 | `results/gpu_MNIST_seed0.json`（66.87 s） |
| **全量** | 18:0x | **novix 20049 / exp-4090** | 2 数据集 × 5 seeds × 6 方法 × 5 T + 消融 + 两套能耗 + H1–H3 | **在途，长时间 `queued / NO_ALLOCATION`，未回收** |
| **本机全量 v1（旧配置）** | 21:06–21:59 | 3060 CUDA | 10/10 runs，5 seeds × 2 数据集，`ours_beta=star` | **done**，`results/local_full/result.json` |
| **本机全量 v2（去 β\*）** | 21:14–22:09 | 3060 CUDA | 10/10 runs，同规格，`ours_beta=zero` | **done**，`results/local_full_v2/result.json` |
| 配对强目标审计 | 22:1x | 本机 | `protocols/analyze_paired.py`，5-seed 均值/配对差值/CI/冻结目标判定 | **done**，`audits/paired-strong-result-audit.md` |
| gauge/θ 尺度扫描 | 22:1x | 本机 | `protocols/scale_sweep.py`，单 seed，验证 logit 漂移 0.0 与 1.4pp 候选工作点 | **done（候选，待 5-seed 验证）** |

## 纪律

- 所有失败与负结果保留并在 `audits/baseline-reproducibility.md` 解释其排除了什么。
- test 只在最终评测用一次；FTBC β 只在 val 校准；用于选择的切分之后不得称 unseen。
- 远端结果回收后由 P3A 数值审计与 P5 强结果锁复核；未达 `expected_strong` 不得进 P6 写作。
