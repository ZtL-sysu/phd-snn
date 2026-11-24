# 7 难点地图

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f81c68e0ac192040b01d3)；由 `export_notion.py` 从只读块数据导出。

> 📌
> **一句话结论**：九个难点里，三个已有成熟解法，四个部分解决、图上还有缺口，两个没找到解法——“动态选邻居会不会因误差翻转”和“图网络与量化网络的公平能耗对比”。

```mermaid
flowchart TB
    subgraph S["已有成熟解法"]
        h1["低时间步误差大 —— QCFS、校准、DCGS"]
        h2["负值 —— 带符号脉冲（DCGS、PMSM）"]
        h3["固定图 + 线性聚合转换 —— One-Spike SNN（Text GCN）"]
    end
    subgraph P["部分解决，图上还有缺口"]
        h4["注意力、归一化 —— Transformer 转换仍靠浮点补偿或长时间步"]
        h5["max 聚合 —— CNN 办法要求非负、长时间步，不适用有符号差值"]
        h6["流式输入的时间冗余 —— 图上已有精确增量，缺逐层阈值化"]
        h7["硬件 —— 事件图芯片已有，跑的是量化网络"]
    end
    subgraph E["没找到解法"]
        h8["动态选邻居：误差使第 k 与第 k+1 近互换"]
        h9["图网络与量化网络的公平能耗对比"]
    end
    style S fill:#e8f5e9,stroke:#4caf50
    style P fill:#fff8e1,stroke:#f0ad4e
    style E fill:#fdecea,stroke:#d9534f
```

*图注：这张图想让你看到的是哪些难点已经有人解决（绿）、哪些部分解决（黄）、哪些还空着（红）。分组依据是 *[*audit 文件*](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/audit-of-claude-v1.md)*的难点树核查结果。*

### 逐个说明

| 难点 | 谁解决了 | 在图上还缺什么 |
| --- | --- | --- |
| 时间步少时误差大 | QCFS [QCFS（2022）](https://app.notion.com/p/41b0e3342e6f810591f7f303160e35ff)、校准 [SNNC-AP / SNN Calibration（2021）](https://app.notion.com/p/41b0e3342e6f81449ff6c194ab8d964a)、DCGS [DCGS（2025）](https://app.notion.com/p/41b0e3342e6f81d8b1d1ccbe05acdde2) | QCFS 要重训；DCGS 遇到重叠的最大池化退回浮点 |
| 负值 | DCGS 的正负阈值 [DCGS（2025）](https://app.notion.com/p/41b0e3342e6f81d8b1d1ccbe05acdde2)、PMSM 的正负脉冲 [PMSM（2025）](https://app.notion.com/p/41b0e3342e6f8179813af26151210c36) | 和“取最大值”叠加时要一起处理 |
| 固定图 + 线性聚合 | One-Spike SNN（文本图）[One-Spike SNN（2025）](https://app.notion.com/p/41b0e3342e6f8142af44e1d41fa091ff) | 视觉固定图上未测 |
| 注意力、归一化 | SpikeZIP-TF [SpikeZIP-TF（2024）](https://app.notion.com/p/41b0e3342e6f81e2a77bf2c3063d849f)、STA [STA（2024）](https://app.notion.com/p/41b0e3342e6f814f9595dcc2bb722d1c)、ECMT [ECMT（2024）](https://app.notion.com/p/41b0e3342e6f81fb8512ef5304537699) | 仍靠浮点补偿或很长的时间步；图上的门控和可变邻域注意力没有方案 |
| 取最大值聚合 | 侧抑制池化 [Burst + LIPooling（2022）](https://app.notion.com/p/41b0e3342e6f81ee8cf8c39f24740761)、Bu 等 [Inference-Scale Conversion（2025）](https://app.notion.com/p/41b0e3342e6f8189b3dcdf43ac9f4e6e) | 都要求非负或后接 ReLU；ViG 取的是有正有负的差值 |
| 流式输入的重复计算 | DeltaCNN [DeltaCNN（2022）](https://app.notion.com/p/41b0e3342e6f818886f2fd847900b43e)、AEGNN [AEGNN（2022）](https://app.notion.com/p/41b0e3342e6f81d58665c55f7cb453c6)、InkStream [InkStream（2025）](https://app.notion.com/p/41b0e3342e6f8150b1b1f1356365a7bf) | 图上已有精确增量，缺逐层阈值截断 |
| 硬件 | EvGNN [EvGNN（2025）](https://app.notion.com/p/41b0e3342e6f8152bc9afe36594e3e25)、ETHEREAL [ETHEREAL（2026）](https://app.notion.com/p/41b0e3342e6f81b78866fd3008d1ab55) | 芯片跑的是量化网络，不是脉冲网络 |
| 动态选邻居 | 没找到 | 误差可能让第 k 近和第 k+1 近的邻居互换 |
| 公平能耗对比 | 卷积网络上有 Yan 等 [Yan 等：QNN-SNN Twin 能耗分析（2026）](https://app.notion.com/p/41b0e3342e6f81008f8ee1e46358f201) | 图网络上没找到 |

### 动态选邻居为什么可能出错

**打个比方**：班里按身高挑前三名，第三名和第四名只差半厘米；如果尺子有一点误差，两人的名次就可能对调。

**准确地说**：ViG、DGCNN 每层按特征距离挑最近的 k 个邻居。转换成脉冲网络后特征会带一点误差，距离也随之有误差。如果第 k 近和第 k+1 近本来就挨得很近，误差可能让两者互换，这一层聚合的对象就变了。比方不成立的地方：身高只有一个数，而特征有几十到几百个数，误差在不同方向上的影响不一样。

[打开本地附件：f6-knn-flip.html](../assets/41b0e334-f6-knn-flip.html)

*交互动画（可暂停）*

*上面是可以暂停、拖动的交互版；下面是同一内容的静态图，导出成文件后也能看。*

![这张图想让你看到的是：第 k 近和第 k+1 近本来就挨得很近时，一点误差就能让两者互换，选出的邻居就变了。示意，非真实数据。](../assets/41b0e334-f6-knn-flip.svg)

*这张图想让你看到的是：第 k 近和第 k+1 近本来就挨得很近时，一点误差就能让两者互换，选出的邻居就变了。示意，非真实数据。*

> ✅
> **事实（初等推导与已有研究）**：如果每个点的特征误差不超过 ε，任意两点距离的变化不超过 2ε；所以只要第 k 近和第 k+1 近的距离差大于 4ε，邻居集合一定不变。近似最近邻检索（在大批向量里快速找最相近几个的算法）的研究（RaBitQ，SIGMOD 2024）发现，查询向量量化到约 4 位时召回率（真正的前 k 名被找对的比例）已接近原值，1 位时大幅下降。出处见 [questions.md 的 Q9](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)；这几篇理论文献在文献库里还没有单独的条目（已记入 仓库 `notion/gaps.md`）。

> ✅
> **事实（取最大值的误差）**：取最大值本身不会放大误差——输出误差不超过输入的最大误差。但如果每个候选都带零均值的随机误差，取最大值会系统性偏高；k 个候选各带均匀分布误差时，期望偏高 (k−1)/(k+1)·ε，k = 9 时约 0.8ε（出处见 [questions.md 的 Q10](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）。

> ❓
> **未知**：真实的 ViG、DGCNN 每层“第 k 近与第 k+1 近的距离差”有多大、转换后多少比例的邻居会变、精度会掉多少，都没有实验数据。这正是第 8 页“失效普查”要回答的。

**三句话小结**

1. 低时间步、负值、固定图线性聚合已有解法；注意力、取最大值、流式、硬件部分解决。
1. 动态选邻居和图上的公平能耗对比没找到解法。
1. 邻居会不会翻转，取决于误差大小和第 k、k+1 近邻的距离差，真实模型上还没测过。
**读完应该能回答的两个问题**

- 什么情况下转换误差一定不会让邻居集合改变？
- 为什么说现有处理最大池化的办法不能直接用在 ViG 上？
