# 3 时间线：脉冲图网络

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f812caa0ec9ae9c741522)；由 `export_notion.py` 从只读块数据导出。

> 📌
> **一句话结论**：脉冲图网络这条线几乎全是“从头设计并训练一个新网络”，视觉上的点云、骨架都有人做；把现成图网络转换过来的只有零星几次，而且都停在“固定图、线性聚合”或“先改结构再重训”。

### 两条路线

**打个比方**：要一辆电动车，可以从零设计一辆（直接训练），也可以把现成的油车改装成电动（转换）。

**准确地说**：**直接训练**是用“替代梯度”（训练时临时用平滑曲线代替阶梯，算完导数再换回脉冲）等技巧，从零直接训练一个脉冲网络；**转换**是拿训练好的普通网络换神经元。比方不成立的地方：改装油车通常比新造便宜得多，而转换是否省事取决于方法——很多转换方法也要先重训原网络。

### 时间线

| 阶段 | 代表工作 | 做了什么 |
| --- | --- | --- |
| 2020–2022：起步 | TactileSGNet [TactileSGNet（2020）](https://app.notion.com/p/41b0e3342e6f81608d57c71ce84f4816)、GC-SNN / GA-SNN [GC-SNN 与 GA-SNN（2021）](https://app.notion.com/p/41b0e3342e6f818dbcaad3c3fe95bc01)、SpikingGCN [SpikingGCN（2022）](https://app.notion.com/p/41b0e3342e6f8128a8dec0fa53d7ab03) | 在触觉传感器图、论文引用图上直接训练；SpikingGCN 还做了 MNIST 手写数字超像素图（把颜色相近的相邻像素合成小块当节点）分类，并明确不走转换路线 |
| 2023–2024：大图与动态图 | SpikeNet [SpikeNet（2023）](https://app.notion.com/p/41b0e3342e6f81878ae9df9c5d515aff)、SpikeGCL [SpikeGCL（2024）](https://app.notion.com/p/41b0e3342e6f81129ffde23c92169d05)、Dy-SIGN [Dy-SIGN（2024）](https://app.notion.com/p/41b0e3342e6f81bda961eddab27c8006)、MSG [MSG（2024）](https://app.notion.com/p/41b0e3342e6f81dd9e3dc837dcf75f09) | 解决直接训练太占显存（显卡内存）、太慢的问题，任务主要是给节点分类 |
| 2025：统一评测 | SGNNBench [SGNNBench（2025）](https://app.notion.com/p/41b0e3342e6f81d288d9fd252aa2f68f) | 在 18 个数据集上比较 9 种直接训练的脉冲图网络 |
| 2023–2026：点云与骨架 | Spiking PointNet [Spiking PointNet（2023）](https://app.notion.com/p/41b0e3342e6f81da8fd4e977dc2fa215)、Spiking Point Transformer [Spiking Point Transformer（2025）](https://app.notion.com/p/41b0e3342e6f810087eae7f7baecf402)、NI-SGCN [NI-SGCN（2025）](https://app.notion.com/p/41b0e3342e6f81ab85c7dd44a710974a)、MK-SGN [MK-SGN（2026）](https://app.notion.com/p/41b0e3342e6f81d5a3ccc05895e3389c)、Signal-SGN [Signal-SGN（2025）](https://app.notion.com/p/41b0e3342e6f8144b4bad0b7761af88b) 等 | 视觉图上的脉冲网络，全部直接训练 |

> ✅
> **事实**：NI-SGCN 是本次检索找到的唯一一篇把 DGCNN 的核心模块 EdgeConv 脉冲化的工作，它是直接训练的，并且把“取最大值”聚合换成了“取平均” [NI-SGCN（2025）](https://app.notion.com/p/41b0e3342e6f81ab85c7dd44a710974a)。MK-SGN 用训练好的 CTR-GCN 做“老师”进行知识蒸馏（让新网络模仿现成老师模型的输出）；Signal-SGN 没有用知识蒸馏，两者都是直接训练（[questions.md Q8](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）[MK-SGN（2026）](https://app.notion.com/p/41b0e3342e6f81d5a3ccc05895e3389c) [Signal-SGN（2025）](https://app.notion.com/p/41b0e3342e6f8144b4bad0b7761af88b)。

> ✅
> **事实（纠正 Claude 草稿）**：Spiking PointCNN 标题里有“Converted”，但它其实是把模块换成脉冲层后从头训练的，邻居按三维坐标固定，不是转换（[questions.md Q4](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）[Spiking PointCNN（2024）](https://app.notion.com/p/41b0e3342e6f81f29a81d3fb0e22e2ed)。

### 已有的几次转换尝试

| 工作 | 转换了什么 | 关键限制 |
| --- | --- | --- |
| One-Spike SNN [One-Spike SNN（2025）](https://app.notion.com/p/41b0e3342e6f8142af44e1d41fa091ff) | 2 层文本分类图网络（Text GCN），不重训，5 个数据集平均掉 0.90% | 只适用于固定的图、线性求和、ReLU |
| PMSM [PMSM（2025）](https://app.notion.com/p/41b0e3342e6f8179813af26151210c36) | 3 层触觉图网络，1 个时间步就不掉点（90.97%） | 必须先用特殊的量化激活函数重训原网络 |
| Lan 等 [Lan 等 3D/2D 转换 SNN（2023）](https://app.notion.com/p/41b0e3342e6f81f6ab43c02a81f1e24c) | 点云网络 PointNet、PointNet++ | 必须先把最大池化换成平均池化再重训；ScanObjectNN 上改过的 PointNet++ 原网络只有 69.22% |
| Adaptive Calibration [Adaptive Calibration（2025）](https://app.notion.com/p/41b0e3342e6f81a6ac26fc23b4a2700b) | 改进版 PointNet | 转换本身免训练，但原网络已把最大值换成平均值再训练 |

> ❓
> **未完全确认**：PMSM 的 arXiv 首版标题和作者与条目记录的不同，条目对应后续版本；Claude 审查时因 arXiv 限流没能独立打开后续版本确认 GCN 实验 [PMSM（2025）](https://app.notion.com/p/41b0e3342e6f8179813af26151210c36)。引用前要复核。

> 💭
> **判断（来自文献核查）**：几次尝试都卡在同一个地方——要么图是固定的、聚合是线性的，要么为了能转换先把“取最大值”改掉并重训。所以真正的空白不是笼统的“图网络转换”，而是“不改结构、不重训，转换带动态选邻居和最大值聚合的视觉图网络”。

**三句话小结**

1. 脉冲图网络绝大多数是直接训练的，点云和骨架上已有不少工作。
1. 转换只有零星几次：文本图、触觉图、点云，且都有“固定图”或“先改结构重训”的限制。
1. 带动态选邻居和最大值聚合的视觉图网络，还没有被转换过。
**读完应该能回答的两个问题**

- 为什么 Lan 等的点云转换不算“免训练转换现成模型”？
- Spiking PointCNN 为什么不能当作转换的先例？
