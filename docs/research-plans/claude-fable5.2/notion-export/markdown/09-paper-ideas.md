# 8 可以做的论文

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f815cb595c1c6c712b79c)；由 `export_notion.py` 从只读块数据导出。

> 📌
> **一句话结论**：草稿列出的候选选题中，四个有明确空白（失效普查、动态选邻居与最大值聚合的转换、视觉流式图的阈值化差分推理、图网络公平能耗对比），两个被草稿判为“换题”；这一页只列每个选题的理由和风险，不替你做选择。

### 草稿用的“四种情况”分法

> 💭
> **判断（Claude 草稿）**：草稿引用彭思达的 learning_research 文档，把选题分成四种情况，并说“前两种换题，第三种适合新手，第四种适合高手”。本次核查没有打开原文档逐句核对，这个分法的准确含义以原文档为准。

### 候选选题

#### 1. 失效普查：现有转换方法在各类视觉图模型上哪里会坏

- **要解决什么**：把现成的免训练转换方法（如 DCGS）用到 ViG、MobileViG、DGCNN、ST-GCN 上，测精度掉多少、邻居变了多少、取最大值的“胜者”变了多少，并用“把邻居换回老师的”这类干预定位原因。
- **为什么是空白**：没有找到在这些模型上做转换的工作（[questions.md Q2](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）。
> ✅
> **事实**：已有的点云转换都是先把“取最大值”换掉再重训，例如 Lan 等把 PointNet++ 的最大池化换成平均池化后，ScanObjectNN 上原网络只有 69.22% [Lan 等 3D/2D 转换 SNN（2023）](https://app.notion.com/p/41b0e3342e6f81f6ab43c02a81f1e24c)。这说明“取最大值转换不了”在别人那里真实发生过。

- **风险**：DCGS 官方代码没有任何图运算、遇到重叠最大池化退回浮点、仓库没有许可证，接到各个老师模型上的工程量不确定（[questions.md Q5](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）[DCGS（2025）](https://app.notion.com/p/41b0e3342e6f81d8b1d1ccbe05acdde2)。普查结果也可能是“没坏”。
- **草稿的归类**：“发现问题本身”，建议最先做，理由是“成本最低，并且决定其余几项的失效案例是否存在”。核查结论：无法核实（见 [audit 第六节](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/audit-of-claude-v1.md)）。
#### 2. 动态选邻居与最大值聚合的转换

- **要解决什么**：不改结构、不重训，让 ViG、DGCNN 这类模型转换后挑出的邻居和取最大值的结果尽量和原网络一致。
- **为什么是空白**：动态选邻居的转换没找到；最大值的现有办法要求非负或后接 ReLU，而 ViG 取的是有正有负的差值 [Inference-Scale Conversion（2025）](https://app.notion.com/p/41b0e3342e6f8189b3dcdf43ac9f4e6e) [ViG 与 Pyramid ViG（2022）](https://app.notion.com/p/41b0e3342e6f8167be5fc852220398d0)。
> ❓
> **未知**：邻居翻转在真实模型上是否严重，没有实验证据。如果误差远小于“第 k 与第 k+1 近的距离差”，问题可能自然不存在。

- **风险**：如果普查发现结构决定天然稳健，这篇就要改写成解释性分析或放弃（草稿的判据 H1）。
- **草稿的归类**：第三或第四种。核查结论：不准确——归类合理，但草稿说“取最大值部分可借池化的解法”不成立（[audit 第六节](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/audit-of-claude-v1.md)）。
#### 3. 视觉流式图上的阈值化差分推理

- **要解决什么**：在骨架序列、视频上的视觉图里，每帧只传变化，并逐层把太小的变化截断，同时控制截断对选邻居和取最大值的影响。
- **为什么是空白**：视频卷积网络上有 DeltaCNN 等逐层截断 [DeltaCNN（2022）](https://app.notion.com/p/41b0e3342e6f818886f2fd847900b43e)；图上有很多精确增量方法 [InkStream（2025）](https://app.notion.com/p/41b0e3342e6f8150b1b1f1356365a7bf) [RIPPLE++（2026）](https://app.notion.com/p/41b0e3342e6f81028b39c6a709fd1adf)，近似做法只见于线性传播和按预算重算 [InstantGNN（2022）](https://app.notion.com/p/41b0e3342e6f8169b6b3ff85004ce8f0) [Reforge（2026）](https://app.notion.com/p/41b0e3342e6f8184b8cedc475b0a3aca)。视觉图上逐层阈值化没找到。
> ❓
> **未知**：ST-GCN 这类模型相邻帧之间各层的变化到底多稀疏，没有找到测量数据（草稿判据 H2 要测的就是这个）。

- **风险**：如果帧间变化不稀疏，省不下计算；精确增量方法已经很强，近似方法需要证明比它们更好。
- **草稿的归类**：第三种。核查结论：不准确——归类可以接受，但草稿说“图上的多跳扩散未解”说过头了，多跳扩散已有不少研究（[audit 第六节](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/audit-of-claude-v1.md)）。
#### 4. 图网络的公平能耗对比

- **要解决什么**：把脉冲图网络和同位数的量化图网络成对比较，把邻居数量不均、内存读取不规则、每层建图的开销都算进去，画出“什么条件下脉冲更省电”的边界。
- **为什么是空白**：卷积网络和 Transformer 上有 Yan 等的框架 [Yan 等：QNN-SNN Twin 能耗分析（2026）](https://app.notion.com/p/41b0e3342e6f81008f8ee1e46358f201)，图网络上没找到。
> 💭
> **判断**：现有硬件研究倾向于认为静态图片上脉冲网络不占优（第 6 页），所以这篇的结论可能是“静态图上不省电”。草稿认为结论正反都可以写（判据 H3）。

- **风险**：对照组必须包含 TopGQ 这类强量化方法，否则会被质疑选了弱对照 [TopGQ（2026）](https://app.notion.com/p/41b0e3342e6f81d59105ce3ec5d943ac)。
- **草稿的归类**：第三种。核查结论：正确。
#### 5. 固定图、线性聚合的低时间步转换（草稿判为“换题”）

- **情况**：图上已有先例——One-Spike SNN 免训练转换了文本图网络 [One-Spike SNN（2025）](https://app.notion.com/p/41b0e3342e6f8142af44e1d41fa091ff)，PMSM 转换了触觉图网络 [PMSM（2025）](https://app.notion.com/p/41b0e3342e6f8179813af26151210c36)。
- **草稿的归类**：第二种，换题。核查结论：正确，而且理由比草稿写的更充分。
#### 6. 门控、注意力聚合的完全事件化（草稿判为“换题”）

- **情况**：Transformer 转换仍要靠浮点补偿或很长的时间步 [SpikeZIP-TF（2024）](https://app.notion.com/p/41b0e3342e6f81e2a77bf2c3063d849f) [STA（2024）](https://app.notion.com/p/41b0e3342e6f814f9595dcc2bb722d1c)；图上的边门控、可变邻域注意力没有现成方案。
- **草稿的归类**：第二种，换题。核查结论：不准确——“同样的问题已有好解法”根据不足（[audit 第六节](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/audit-of-claude-v1.md)）。
**三句话小结**

1. 四个有空白的选题：失效普查、动态选邻居与最大值转换、视觉流式图阈值化差分、图上公平能耗对比。
1. 每个选题都有“实验可能不支持”的风险，前三个都依赖还没做的测量。
1. 草稿对第 3、5、6 个选题的理由有偏差，具体见第 9 页。
**读完应该能回答的两个问题**

- 为什么“失效普查”的结果会影响其他几个选题？
- 第 4 个选题的对照组为什么一定要包括 TopGQ？
