# Claim–Evidence Matrix · v2（P1A 重做，替换 v1 场景的旧矩阵）

> v1 的 `../ccfa-startup-packet/claim-evidence-matrix.md` 基于 ViG/CIFAR 场景，因用户 17:19 改向（自带图的视觉数据集 + ANN/能耗对照 + 组合创新）**不适用**，本文件为本次 `f-research-v1` 运行重做。
> **结果栏全部为待 P4 全量实验填充**；本文件在 P1A 阶段只定义所需证据与决策规则，不含任何实验结果数值。

| Claim | 所需实验 | 数据集/split | 主指标与方向 | 简单基线 | 最强可行域基线 | 匹配内部对照 | 消融 | 稳健性/效率 | 回答评审的哪个问题 | 结果 |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 图级池化后恒等式精确成立 | `check_identity` 逐 T 浮点残差；固定线性 vs 动态/非线性变体 | MNIST/CIFAR10 官方 test | 残差（越低越好） | 朴素 rate 转换 | 全套转换方法 | 关闭池化线性性 | 非线性池化、动态邻接 | 算子范数、float64 重算 | 池化是否破坏 1028 的误差恒等式 | 待 P4 |
| C2 组合方法 T≤8 达 ANN−1.5pp 带内 | accuracy–T 曲线、conversion loss 主表 | 两数据集 ×5 seeds | conversion loss (pp，越低越好) | 朴素 rate | QCFS/FTBC/TPP/Parallel 适配 | 同一 teacher 的 ANN 上限 | 去 β*、计数解码、随机相、朴素 IF | 5-seed CI、BH、阈值敏感性 | 组合方法能否保住 ANN 精度 | 待 P4 |
| C3 同一超像素图骨干上的公平横评 | 六方法 × T 网格同协议对比 | 两数据集 ×5 seeds | 配对 conversion loss 差值 | 朴素 rate | FTBC/QCFS/TPP（第 0 批必跑） | 逐组件开关臂 | A1–A4 | θ∈{0.5,1,2}、三种归一化、两种池化 | 相对单点转换方法是否有可归因优势 | 待 P4 |
| C4 与 ANN 对照 + 理论算术能耗 | 精确 MAC/AC 计数、两套能耗口径、spike 密度 | 两数据集 ×5 seeds ×全 T | ANN/SNN 能量比（越高越好） | ANN teacher 精确 MAC | 直训 SNN 脉冲活动 | 同架构 ANN 前向 | 低 T 与稀疏化条件 | 峰值显存、wall-clock、SynOps | 事件驱动是否带来算术能耗优势、在哪个 T 区间 | 待 P4 |
| C5 组合各组件可归因 | 四项消融的配对差值与 CI | 两数据集 ×5 seeds | 差值方向 + CI | 完整主臂 | 单点方法 | 主臂 | 去 β*、计数解码、随机第二相、朴素 IF | 逐 seed 一致性 | 组合是新适配还是冗余堆叠 | 待 P4 |

## 决策规则（写死，不随结果改）

- 只有 C1–C5 全部有实跑证据、且 C2/C3/C4 达到 `guidance-v2.md` §Expected Results 的 `expected_strong`，P5 才判 passed；任一未达 → 进入授权修正回路，**不得**下调阈值或把计划写成结果。
- C4 若两套口径下都不存在优势，如实报告负结果并按契约收窄为「稀疏活动与 SynOps 代理指标」，不得调口径凑 5×。
- C5 若显示 β* 与确定性两阶段冗余，保留负结果并给出机制解释假设，不删除该组件以美化主表。
- 所有 test 只在最终评测用一次；FTBC 的 β 只在 val 校准；用于选择的切分之后不得称 unseen。
