# 9 Claude 的判断哪里对、哪里错

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f81cba505e4f774ccf728)；由 `export_notion.py` 从只读块数据导出。

> 📌
> **一句话结论**：Claude 草稿的 72 处论断里，43 处正确、18 处不准确、4 处错误、7 处无法核实；错的集中在“图网络从没被转换过”“最大值聚合不再是空白”“Spiking PointCNN 是转换”这几处，方向判断（动态选邻居是空白）站得住。

> 💭
> **说明**：Claude 的文献树 v1 是在没有通读论文全文的情况下写的，里面的结论都是“判断”，不是事实。下面的核查结果来自 [audit-of-claude-v1.md](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/audit-of-claude-v1.md)，那里有每一行的证据。

### 判定统计

| 判定 | 数量 | 含义 |
| --- | --- | --- |
| 正确 | 43 | 与原文一致 |
| 不准确 | 18 | 大体对，但有偏差（数字、发表处、说法过头） |
| 错误 | 4 | 与原文相反 |
| 无法核实 | 7 | 依赖项目内部实验或尚未做的测量 |

*表注：草稿八张表共 56 行，加表格外 16 处论断，共 72 处。*

### 四处错误

| 草稿说 | 实际情况 |
| --- | --- |
| 检索中没有找到把现成图网络免训练转成脉冲网络的工作 | One-Spike SNN 免训练转换了预训练的文本图网络，5 个数据集平均掉 0.90% [One-Spike SNN（2025）](https://app.notion.com/p/41b0e3342e6f8142af44e1d41fa091ff) |
| 视觉图任务只有骨架识别有人做 | 点云上有 Spiking PointNet 等多篇 [Spiking PointNet（2023）](https://app.notion.com/p/41b0e3342e6f81da8fd4e977dc2fa215)，SpikingGCN 做了 MNIST 超像素图 [SpikingGCN（2022）](https://app.notion.com/p/41b0e3342e6f8128a8dec0fa53d7ab03) |
| Spiking PointCNN 是点云转换的先例 | 它是从头训练的；真正的先例是 Lan 等（ICCV 2023）[Spiking PointCNN（2024）](https://app.notion.com/p/41b0e3342e6f81f29a81d3fb0e22e2ed) [Lan 等 3D/2D 转换 SNN（2023）](https://app.notion.com/p/41b0e3342e6f81f6ab43c02a81f1e24c) |
| 最大池化已有多种解法（含“改成神经元层”），最大值聚合不再算空白 | Bu 等是把最大池化挪到神经元之前，不是改成神经元层；现有办法都不适用 ViG 的有符号差值 [Inference-Scale Conversion（2025）](https://app.notion.com/p/41b0e3342e6f8189b3dcdf43ac9f4e6e) |

### 值得注意的不准确

- **多跳扩散“未解”**：图上已有很多精确增量方法研究并缓解多跳扩散，缺的是视觉图上逐层阈值化的近似方法 [InkStream（2025）](https://app.notion.com/p/41b0e3342e6f8150b1b1f1356365a7bf) [DAGr（2024）](https://app.notion.com/p/41b0e3342e6f81748ed9d8b84b2d24e2)。
- **AEGNN“最多降 200 倍”**：这是 CVPR 原版的说法，arXiv 更新版改成“比最好的异步方法低 11 倍”，引用时要注明版本 [AEGNN（2022）](https://app.notion.com/p/41b0e3342e6f81d58665c55f7cb453c6)。
- **注意力与归一化“Transformer 上已有解法”**：Transformer 转换仍靠浮点补偿或很长的时间步 [SpikeZIP-TF（2024）](https://app.notion.com/p/41b0e3342e6f81e2a77bf2c3063d849f) [STA（2024）](https://app.notion.com/p/41b0e3342e6f814f9595dcc2bb722d1c)。
- **ETHEREAL“仅见作者消息”**：论文已在 arXiv 公开；草稿写的 ESSERC 2026 在两份 PDF 里都没有出现 [ETHEREAL（2026）](https://app.notion.com/p/41b0e3342e6f81b78866fd3008d1ab55)。
- **同位数均匀量化当对照**：图网络低位宽下朴素量化会崩，应加入 TopGQ [TopGQ（2026）](https://app.notion.com/p/41b0e3342e6f81d59105ce3ec5d943ac)。
### 草稿判断对的地方

> ✅
> **核查确认**：ViG、DGCNN 的转换确实没找到（ViG 的 552 篇被引中也没有）；图网络上的公平能耗对比确实没找到；事件图芯片跑的确实不是脉冲网络；MobileViG 确实是固定图加取最大值（[questions.md Q2、Q3、Q7](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）。

### 审查时又发现的问题

> ✅
> **事实**：Claude 审查任务 01 时，独立核对了 7 篇论文和 3 个代码仓库，全部与记录吻合，并修了三处小问题：MobileViG 的差值方向是“自身减邻居”、实现用切片拼接；PMSM 条目对应的是 arXiv 后续版本；One-Spike SNN 的“唯一”改为“本次检索范围内唯一”（见 [docs/PROGRESS.md](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/docs/PROGRESS.md) 2026-11-17 记录）。

**三句话小结**

1. 草稿大部分正确，但四处错误都落在“别人做没做过”这类关键判断上。
1. 草稿最大的问题是没读全文：把 Spiking PointCNN 当转换、把 Bu 等的方法读错。
1. 草稿“动态选邻居是空白”的核心判断经核查成立。
**读完应该能回答的两个问题**

- 草稿“图网络从没被转换过”错在哪里？
- 为什么草稿说“最大值聚合不再算空白”站不住？
