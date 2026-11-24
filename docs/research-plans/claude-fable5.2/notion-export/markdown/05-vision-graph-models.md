# 4 时间线：视觉图模型

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f81d3b941f53e1b53937f)；由 `export_notion.py` 从只读块数据导出。

> 📌
> **一句话结论**：现成的强视觉图模型分四类——图片、点云、骨架、事件相机；对转换来说，最关键的区别是“图固定还是每层按特征重算”和“聚合是求和还是取最大值”。

### 两个看点

**打个比方**：同样是开会，有的会座位固定、每次只和邻座讨论（固定图）；有的会每轮都按“谁的观点和我最像”重新换座位（每层按特征重算）。讨论结果的汇总，有人取平均意见，有人只听最激进的那一个（取最大值）。

**准确地说**：**建图方式**决定邻居是事先定好的，还是每一层根据当前特征用 kNN 重新挑；**聚合算子**决定邻居的消息怎么合成。比方不成立的地方：开会换座位是整人换，而 ViG 的“取最大值”是对每一个数位分别取，不同数位的最大值可能来自不同邻居。

> 💭
> **判断**：对转换而言，“固定图 + 求和”最容易，“每层重算 kNN + 取最大值”最难，因为后者里有“挑谁”和“取谁”两个离散决定，误差可能让决定翻转。这是本项目的核心假设，尚待实验验证。

### 代表模型

| 类别 | 模型 | 建图方式 | 聚合 | 公开精度（论文表格） | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 图片 | ViG / Pyramid ViG [ViG 与 Pyramid ViG（2022）](https://app.notion.com/p/41b0e3342e6f8167be5fc852220398d0) | 每层按特征重算 kNN（k 为 9–18） | 邻居差值取最大 | ImageNet：ViG-Ti/S/B 为 73.9% / 80.4% / 82.3% | Apache-2.0 |
| 图片 | MobileViG [MobileViG（2023）](https://app.notion.com/p/41b0e3342e6f8147baf6c94fa0b0bf57) | 固定：同行同列每隔一个取邻居 | 差值取最大 | ImageNet：Ti/S/M/B 为 75.7% / 78.2% / 80.6% / 82.6% | Apache-2.0 |
| 图片 | GreedyViG [GreedyViG（2024）](https://app.notion.com/p/41b0e3342e6f81d8b9eee155c807626e) | 动态轴向建图 | 取最大 | ImageNet：S/M/B 为 81.1% / 82.9% / 83.9% | 仅限非商业研究 |
| 点云 | PointNet++ [PointNet++（2017）](https://app.notion.com/p/41b0e3342e6f8130854fe0de535da6b0) | 按三维坐标固定分组 | 最大池化 | ModelNet40：90.7%（1024 点） | MIT |
| 点云 | DGCNN [DGCNN（2019）](https://app.notion.com/p/41b0e3342e6f811682d7dcfddfefb7e0) | 每层按特征重算 kNN（k = 20） | 取最大 | ModelNet40：92.9% | MIT（PyTorch 实现仓库） |
| 骨架 | ST-GCN [ST-GCN（2018）](https://app.notion.com/p/41b0e3342e6f8147b449ee3bd25011a5) | 固定骨架图 | 加权求和 | NTU-60：81.5% / 88.3% | BSD-2-Clause |
| 骨架 | CTR-GCN [CTR-GCN（2021）](https://app.notion.com/p/41b0e3342e6f817cbe36d765126abfee) | 每层按样本特征调整 | 加权求和（含动态拓扑） | NTU-60 四流（关节、骨头及其运动合算）：92.4% / 96.8% | CC BY-NC 4.0 |
| 事件相机 | AEGNN [AEGNN（2022）](https://app.notion.com/p/41b0e3342e6f81d58665c55f7cb453c6) | 按时空距离建图，增量更新 | 样条卷积（按点间相对位置连续调权重的图运算） + 最大图池化 | N-Cars：94.5% | MIT |
| 事件相机 | DAGr [DAGr（2024）](https://app.notion.com/p/41b0e3342e6f81748ed9d8b84b2d24e2) | 有向时空半径图 | 样条卷积 + 三维小格子（体素）最大池化 | Gen1：32.1 mAP（DAGr-L） | GPL-3.0 |
| 超像素基准 | GatedGCN 等 [Benchmarking GNNs 超像素视觉图基准（2022）](https://app.notion.com/p/41b0e3342e6f819f8308ddd5dac0d8f4) | 固定 kNN 图 | 门控加权求和（每条边带一个 0 到 1 的开关系数） | CIFAR10 超像素：67.31% | MIT |

> ✅
> **事实**：MobileViG 的图是完全固定的，不随输入变化，但聚合仍是逐元素取最大值（[questions.md Q7](https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/questions.md)）[MobileViG（2023）](https://app.notion.com/p/41b0e3342e6f8147baf6c94fa0b0bf57)。所以它可以当作“有取最大值、没有动态选邻居”的对照。

> ✅
> **事实**：同样的超像素图、同样的参数预算下，GatedGCN 在 CIFAR10 上 67.31%，换成只做求和或平均的简单图网络明显更低（见文献库条目的表 7）[Benchmarking GNNs 超像素视觉图基准（2022）](https://app.notion.com/p/41b0e3342e6f819f8308ddd5dac0d8f4)。

> 💭
> **判断（来自许可证核查）**：选老师模型时要注意许可证：GreedyViG 仅限非商业研究，CTR-GCN 是 CC BY-NC 4.0，DAGr 是 GPL-3.0；DCGS 官方代码没有任何许可证（第 2 页）。做研究可以用，但发布代码时需要留意。

**三句话小结**

1. 视觉图模型有图片、点云、骨架、事件相机四类，都有公开的预训练权重。
1. 关键差别是图固定还是每层重算、聚合是求和还是取最大值。
1. ViG、DGCNN 是“动态选邻居 + 取最大值”的代表，MobileViG、ST-GCN 是固定图的对照。
**读完应该能回答的两个问题**

- 为什么 MobileViG 适合用来和 ViG 做对照？
- 选老师模型时，除了精度还要看哪两件事？
