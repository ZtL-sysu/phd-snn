# 11 文献库

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f814a98b5c85f2ded4083)；由 `export_notion.py` 从只读块数据导出。

> 📌
> **一句话结论**：这里是全部讲解的事实来源——任务 01 核实过的 115 篇论文，一篇一条；其他页面里每条事实后面的链接都指向这里。

### 怎么用

- 每条记录的属性对应任务 01 的固定格式：短名、年份、脉络、标题、作者、发表处、链接、代码、核对深度、是否需要训练或微调、与本方向的关系、一句话、核对人与日期，以及指向仓库原条目的“仓库条目”链接。
- 较长的字段（解决的难点、留下的局限、涉及的算子、关键数字，以及“与本方向的关系”的具体说明）在每条记录的正文里。
- 可以按“脉络”筛选，按“年份”排序，或按“核对深度”找出只核对到摘要的条目。
> ✅
> **事实**：任务 01 共有 120 个条目，其中 5 篇论文在两条脉络里各出现一次（One-Spike SNN、Adaptive Calibration、AEGNN、DAGr、EvGNN），这里合并为一条，正文里分别保留两条脉络的记录，所以共 115 条。110 个条目读过全文，9 个只核对到摘要，1 个只见过引用。

> 💭
> **提醒**：“与本方向的关系”是核查人的判断，不是事实；条目里“首个”“首次”等说法是论文自己的说法，已标为“论文自称”。

> ❓
> **已知的未确认项**：Claude 审查任务 01 时没能独立确认以下几处，引用前要复核——PMSM 的 GCN 实验；Bu 等（arXiv 2409.03368）发表于 CVPR 2025、Yan 等发表于 IEEE TCAD 2026、InkStream 发表于 IPDPS 2025、NI-SGCN 发表于 AAAI 2025 这四个发表处。

### 数据库

数据库在下方，可点开浏览、筛选和排序。

**三句话小结**

1. 文献库收录 115 篇论文，是全篇所有事实的出处。
1. 短字段是属性，长字段在每条正文里。
1. “与本方向的关系”是判断，不是事实。
**读完应该能回答的两个问题**

- 怎样找出只核对到摘要的论文？
- 为什么条目数是 115，而任务 01 写的是 120？
## 文献库

任务 01 核实过的论文，一篇一条。字段对应 tasks/01-literature-collection.md 的固定格式；长字段在每条的正文里。来源：仓库 literature/01–05。

共 115 条记录。

### <a id="41b0e334-2e6f-8102-8b39-c6a709fd1adf"></a>RIPPLE++（2026）

- **发表处：** arXiv（第 1 页脚注说明是 ICDCS 2025 论文 Ripple 的扩展长文版）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Pranjal Naman, Parv Agarwal, Hrishikesh Haritas, Yogesh Simmhan
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#ripple2026
- **代码：** [https://github.com/dream-lab/ripple](https://github.com/dream-lab/ripple) （据正文引用）
- **年份：** 2026
- **一句话：** 图的边或节点特征变化时，只沿受影响的邻域逐层传播“增量消息”，精确更新所有节点的嵌入，比每次在受影响邻域里重算更快。
- **链接：** https://arxiv.org/abs/2601.12347
- **核对人与日期：** Gemini，2026-11-16
- **标题：** RIPPLE++: An Incremental Framework for Efficient GNN Inference on Evolving Graphs
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把 Ripple 从只支持累加型聚合推广到 max 这类单调算子和 GAT 这类注意力算子（第 5 页）；给出逐跳的计算量模型（第 13 页）：重算需约 $a_l\delta d_{l-1}+a_l d_{l-1}d_l$ 次浮点运算，增量需约 $a_{l-1}\delta d_{l-1}+a_l d_{l-1}d_l$ 次，其中 $a_l$ 是第 l 跳受影响顶点数。

**留下的局限**：坚持精确结果，不做近似（第 17 页明确说不采样、不近似）；当 $a_{l-1}$ 接近 $a_l$（深层或高度数图）时节省消失；注意力的系数同时依赖源和目标节点，一跳变化会迫使下一跳所有入边重算。

**是否需要训练或微调**：否

**涉及的算子**：sum / mean / max 聚合、GAT 注意力、线性变换、ReLU

**关键数字**：单机最高约 56K 次更新 / 秒，比 InkStream 快 2.2–24 倍；分布式比重算基线吞吐高约 25 倍、通信低 20 倍（第 1 页摘要、第 5 页）；Products 图上批大小 1→100 时受影响顶点由 0.7% 升到约 37%，Arxiv 图由 0.06% 升到 2.2%（第 3 页 Fig. 4 正文）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（它量化了多跳扩散，并且支持 max 聚合）

### <a id="41b0e334-2e6f-8109-b83a-f599d3973e9a"></a>Ripple（2025）

- **发表处：** 45th IEEE International Conference on Distributed Computing Systems（ICDCS 2025）（第 1 页脚注）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Pranjal Naman, Yogesh Simmhan
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#ripple2025
- **代码：** [https://github.com/dream-lab/ripple](https://github.com/dream-lab/ripple) （据 RIPPLE++ 正文）
- **年份：** 2025
- **一句话：** 流式图上边或特征变化时，用增量消息逐层更新受影响顶点的嵌入，支持单机和分布式。
- **链接：** https://arxiv.org/abs/2505.12112
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Ripple: Scalable Incremental GNN Inferencing on Large Streaming Graphs
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：逐顶点推理会重复计算重叠的邻域，逐层全图推理太慢（Products 图一次更新约 20 秒，第 3 页）；它只对受影响邻域做精确增量。

**留下的局限**：只支持线性（累加型）聚合（第 4 页贡献 1）；精确、无阈值；与视觉图无关。

**是否需要训练或微调**：否

**涉及的算子**：sum / mean 聚合、线性变换、逐元素激活

**关键数字**：单机稀疏图 Arxiv 上约 28000 次更新 / 秒，Products 上约 1200 次 / 秒，延迟 0.1 ms–1 s；分布式比基线吞吐高约 30 倍、通信低 70 倍（第 1 页摘要）。

> 💭
> **与本方向的关系（判断）**：可借用的技术

### <a id="41b0e334-2e6f-8130-854f-e0de535da6b0"></a>PointNet++（2017）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2017，Vol. 30，pp. 5099–5108；预印本 `arXiv:1706.02413`）
- **脉络：** 3 视觉图骨干
- **作者：** Charles R. Qi, Li Yi, Hao Su, Leonidas J. Guibas
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#pointnet2017
- **代码：** [https://github.com/charlesq34/pointnet2](https://github.com/charlesq34/pointnet2) （高星社区 PyTorch 版及预训练权重：[https://github.com/yanx27/Pointnet_Pointnet2_pytorch](https://github.com/yanx27/Pointnet_Pointnet2_pytorch) ）
- **年份：** 2017
- **一句话：** 通过迭代最远点采样（FPS）、度量空间多尺度球邻域分组（MSG/MRG）以及局部微型 PointNet（共享 MLP + 对称 `MAX` 池化）递归提取三维点云的多尺度局部几何结构。
- **链接：** https://arxiv.org/abs/1706.02413
- **核对人与日期：** Gemini，2026-11-16
- **标题：** PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了初代 `PointNet` 只有单次全局最大池化、完全缺失局部邻域几何上下文且对非均匀采样密度脆弱的根本缺陷。

**留下的局限**：每个集合抽象层（`SA`）都完全依赖局部邻域上的**逐通道 **`**MAX**`** 池化**保证点集置换不变性——脉络一、二中已有两篇转换论文（ICCV 2023 `Lan 等` 与 AAAI 2025 `Adaptive Calibration`）试图转换 `PointNet++`，**但它们无一例外都因为处理不了脉冲 **`**MAX**`** 池化，被迫先把源网的 **`**MAX**`** 改成均值池化（**`**AvgPool**`**）并从头重新训练浮点源网络**，真正的原版 `MAX` 池化 `PointNet++` 免训练转换至今仍是空白！

**是否需要训练或微调**：是（Adam 训练；`yanx27` PyTorch 仓库内置 `ModelNet40` 与 `ShapeNetPart` 预训练模型）

**涉及的算子**：最远点采样（FPS）、固定三维坐标球查询（SSG / 多尺度 MSG / 跨层 MRG）、局部相对坐标平移 $x_i - \hat{x}$、共享逐点 MLP（`Conv1x1 + BatchNorm + ReLU`）、**邻域逐通道对称 **`**MAX**`** 池化**、分割解码 $k=3$ 反平方距离加权插值

**关键数字**：`ModelNet40` 分类（Table 2，第 6 页）：1024 点纯坐标达 **90.7%** OA，5000 点加面法向达 **91.9%** OA（邻域消融 Supp. Table 5 第 13 页：球查询 $r=0.2$ **90.7%** 略优于 $k=64$ $k$-NN 的 **90.3%** 与 $k=16$ 的 **89.3%**）；`ShapeNetPart` 部件分割达 **85.1%** mIoU（Supp. Table 4，第 13 页）；`ScanNet` 室内体素标注精度 `MSG+DP` 达 **84.5%**（非均匀扫描下 **80.4%**，Figure 5，第 6 页）；`SHREC15` 非刚体测地距离分类达 **96.09%**（Table 3，第 8 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（检验“不改源网、保留原始对称 `MAX` 集合归约直接免训练转脉冲”能否超越“改 `AvgPool` 重训源网”路线的经典试金石，直接对应定向问题 Q2）

### <a id="41b0e334-2e6f-8136-88e7-e78fc1245efc"></a>NeutronRT（2026）

- **发表处：** arXiv（PDF 中未见会议信息；本地文件名里的 “ICDE26” 无法从 PDF 证实，记为未核实）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Qiange Wang, Haoran Lv, Yanfeng Zhang, Weng-Fai Wong, Bingsheng He
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#neutronrt2026
- **代码：** 未公开
- **年份：** 2026
- **一句话：** 把 GNN 拆成一组细粒度算子并安全地重排顺序，使流式图上的嵌入更新只在受影响子图上做，结果与全邻居计算一致。
- **链接：** https://arxiv.org/abs/2603.20622
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Incremental GNN Embedding Computation on Streaming Graphs
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：L 层 GNN 的一次更新会波及 L 跳，朴素做法连有效的中间结果也重算（第 1 页 Fig. 1）；它区分“传播路径”和“最后一层受影响顶点”，只算必要部分；对 GAT、门控 GCN 这类消息依赖目标节点的模型给出了正确性条件。

**留下的局限**：精确方法，无阈值；更新比例变大时优势迅速缩小（第 11 页：|ΔE|=1K 时比全量快 285.0 倍，|ΔE|=100M、约占原边集 16% 时只快 3.8 倍）。对“每帧几乎所有节点特征都变”的视觉图，这正是最差情况。

**是否需要训练或微调**：否

**涉及的算子**：消息、聚合、更新的细粒度算子，GCN / GraphSAGE / GAT / 门控 GCN

**关键数字**：冗余计算减少 64%–99%，比现有方案快 1.7–145.8 倍，单张 A5000 处理十亿级流式图（第 1–2 页摘要与引言）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（门控 GCN 的增量正确性分析与本项目 GatedGCN 锚点直接相关）

### <a id="41b0e334-2e6f-8147-b449-ee3bd25011a5"></a>ST-GCN（2018）

- **发表处：** Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence（AAAI 2018，pp. 7444–7452；预印本 `arXiv:1801.07455`）
- **脉络：** 3 视觉图骨干
- **作者：** Sijie Yan, Yuanjun Xiong, Dahua Lin
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#st-gcn2018
- **代码：** [https://github.com/yysijie/st-gcn](https://github.com/yysijie/st-gcn)
- **年份：** 2018
- **一句话：** （论文自称）首次把人体动作序列建模为“帧内自然骨骼边 + 帧间同关节轨迹边”的固定时空图，通过按骨骼重心距离划分自身/向心/离心三个固定子集做度归一化图卷积与时间一维卷积，开创了图神经网络骨架动作识别领域。
- **链接：** https://arxiv.org/abs/1801.07455
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：摆脱了早期手工划分身体部位规则或用 RNN/伪图像丢失骨骼拓扑的局限。

**留下的局限**：图拓扑完全静态固定（可学习边掩码 $\mathbf{M}$ 只是对已有物理边乘标量权重，无法在原本不相连的左右手之间生成新边），因此绝对精度明显低于后续自适应动态图（如 `CTR-GCN`、`HD-GCN`）；但**正因其全网仅含固定稀疏矩阵乘、**$1\times 9$** 卷积、**`**BatchNorm**`**、**`**ReLU**`** 与全局 **`**AvgPool**`**（零 **`**MaxPool**`**、零 **`**Softmax**`** 注意力、零动态 **`**topk**`**）**，它是检验基础图转换保真度的理想无干扰基线！

**是否需要训练或微调**：是（SGD 训练；官方仓库及 `MMSkeleton` 公开了 `NTU-RGB+D` 与 `Kinetics` 预训练权重）

**涉及的算子**：固定人体骨骼空间构型三子集划分（自身、向心、离心，$K=3, D=1$）、可学习固定边重要性掩码 $\mathbf{A}_j\otimes\mathbf{M}$、对称度归一化线性矩阵乘加权和、$1\times 9$ 时序卷积（第 4、7 层步幅 2 降采样）、残差跳连、输入层与卷积层 `BatchNorm`、`ReLU`、全局 `AvgPool`

**关键数字**：`Kinetics-Skeleton` 验证集 Top-1 / Top-5 达 **30.7% / 52.8%**（Table 2，第 8 页）；`NTU-RGB+D 60` X-Sub / X-View 达 **81.5% / 88.3%**（Table 3，第 8 页；注：`2s-AGCN` Section 5.3 第 7 页指出仅改进学习率调度与预处理即可将原版 `ST-GCN` 在 X-View 提至 **92.7%**；另注 `InfoGCN` Table 1 误引 `ST-GCN` X-View 为 `88.0%`，以 `ST-GCN` 原文 Table 3 **88.3%** 为准）。

> 💭
> **与本方向的关系（判断）**：直接相关（**最纯净的固定图+线性求和+ReLU 视觉教师基线**：许可证宽松 [`BSD-2-Clause`]、有官方预训练权重，且尚未有任何工作发表过针对 `ST-GCN` 的免训练转换评测，见定向问题 Q2）

### <a id="41b0e334-2e6f-816e-b420-d85703d62a3e"></a>RG-CNNs（2019）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2019，pp. 491–501；预印本 `arXiv:1908.06648`；后续扩展版发表于 IEEE TIP 2020）
- **脉络：** 3 视觉图骨干
- **作者：** Yin Bi, Aaron Chadha, Alhabib Abbas, Eirina Bourtsoulatze, Yiannis Andreopoulos
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#rg-cnns2019
- **代码：** [https://github.com/PIX2NVS/NVS2Graph](https://github.com/PIX2NVS/NVS2Graph)
- **年份：** 2019
- **一句话：** （论文自称）首次将事件相机输出的异步事件流经非均匀网格降采样后直接构建为加权时空半径图，用带残差跳连的 B 样条空间图卷积（`RG-CNNs`）和二维网格簇最大池化完成分类，并发布了 10 万样本的真实手语事件数据集 `ASL-DVS`。
- **链接：** https://arxiv.org/abs/1908.06648
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Graph-Based Object Classification for Neuromorphic Vision Sensing
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：避免了把稀疏事件流强行压成稠密二维图像帧带来的内存与卷积冗余，仅用 `ResNet-50` 五分之一的计算量即在六个事件视觉分类集上超越帧式 CNN。

**留下的局限**：图按整段 30ms 窗口批量重算（尚不支持逐事件异步局部更新，后被 `AEGNN` 解决），每层后接二维网格簇 `MaxPool`，且仓库仅公开 `ASL-DVS` 数据集与建图脚本，未公开模型预训练权重与许可证。

**是否需要训练或微调**：是（Adam 训练 150 轮）

**涉及的算子**：三维时空网格随机单点采样（$k=8$）、加权时空欧氏半径建图（$R=3, D_{\max}=32$）、一阶 B 样条空间卷积 `SplineCNN`（$m=1, k=5$，度归一化均值）、残差图块（`K=5` 主干 + `K=1` 捷径）、二维空间簇 `**MaxPool**`**（**`**MaxP**`**）**、`BatchNorm`、`ReLU`

**关键数字**：六个事件分类基准 Top-1 精度（Table 1，第 7 页）：`N-MNIST` **99.0%**、`MNIST-DVS` **98.6%**、`N-Caltech101` **65.7%**、`CIFAR10-DVS` **54.0%**、`N-CARS` **91.4%**、`ASL-DVS` **90.1%**；在 `N-Caltech101` 上仅需 **0.79 GFLOPs** 与 **19.46 MB** 模型体积，优于帧式 `ResNet-50` 的 63.7% / 3.87 GFLOPs（Tables 2–3，第 8 页）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（事件相机点图表示的奠基之作，全网仅用 `SplineConv + BN + ReLU + MaxPool`，也是脉络二中诸多 DVS 事件分类脉冲网络的重要浮点对照基准）

### <a id="41b0e334-2e6f-8184-b8ce-dc475b0a3aca"></a>Reforge（2026）

- **发表处：** 2026 IEEE International Parallel and Distributed Processing Symposium（IPDPS 2026），pp. 788–803（据 arXiv v2 第 14 页参考文献 [1]）。**名称冲突**：同一 arXiv 编号 2501.08547 的早期版本名为 Omega，Ripple 论文第 8 页即以 “Omega [16]” 引用它。
- **脉络：** 4 事件驱动与增量推理
- **作者：** Geon-Woo Kim, Donghyun Kim, Jeongyoon Moon, Henry Liu, Tarannum Khan, Anand Iyer, Daehyeok Kim, Aditya Akella
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#reforge2026
- **代码：** 未公开（PDF 中未见仓库链接）
- **年份：** 2026
- **一句话：** 在大图上回答“新来一个查询节点，它的嵌入是什么”时，大部分邻居直接用预先算好的嵌入，只挑对精度影响大的少数邻居重新计算。
- **链接：** https://arxiv.org/abs/2501.08547
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Reforge: Low-Latency Distributed GNN Serving with Selective Embedding Recomputation
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：完全复用预计算嵌入会忽略新节点对旧节点的影响，导致掉点（第 4 页 Table I：快 10.7 倍但掉 6.3 个百分点）；完全重算又太慢。它用一个启发式在预算内挑选要重算的节点，并做跨机器的计算图并行以减少通信。

**留下的局限**：针对的是“新增查询节点”的服务场景，不是逐帧的特征变化；挑选依据是统计意义上的误差最小化，没有逐层的变化量阈值；面向社交 / 商品大图，与视觉图无关。

**是否需要训练或微调**：否（复用已训练模型）

**涉及的算子**：GraphSAGE、GCN、GCNII 等的 sum / mean 聚合，嵌入缓存，选择性重算

**关键数字**：Amazon 数据集上 SAGE 模型延迟比 DGL 全量低 159 倍（第 10 页 Fig. 10 附近正文）；GCNII + Yelp 上层数增加时延迟变化见第 13 页 Fig. 17。

> 💭
> **与本方向的关系（判断）**：可借用的技术（“预算式选择性重算”是阈值化之外另一种控制扩散的思路）

### <a id="41b0e334-2e6f-81a0-ace0-e748ae7064c8"></a>ResGatedGCN（2017）

- **发表处：** arXiv preprint `arXiv:1711.07553`（2017 首版，2018 v2 修订）
- **脉络：** 3 视觉图骨干
- **作者：** Xavier Bresson, Thomas Laurent
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#resgatedgcn2017
- **代码：** [https://github.com/graphdeeplearning/benchmarking-gnns](https://github.com/graphdeeplearning/benchmarking-gnns)
- **年份：** 2017
- **一句话：** 将边缘 Sigmoid 软门控机制、批归一化（BN）与跨层恒等残差连接融合成通用深层空间图卷积架构，使消息传递图网络在叠加至 10 层以上时依然单调提点且快于图循环网络。
- **链接：** https://arxiv.org/abs/1711.07553
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Residual Gated Graph ConvNets
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了早期同构图卷积无法自动抑制异类邻居噪声边（社区边界边），以及超过 3–4 层后性能剧烈退化的问题。

**留下的局限**：每一条边 $(i,j)$ 在每一层都需计算 `Sigmoid` 门控值 $\eta_{ij}=\sigma(A^\ell h_i^\ell + B^\ell h_j^\ell)$（在后续 `Benchmarking GNNs` 版中还需做邻域门控归一化 $\frac{\sigma(\hat{e}_{ij})}{\sum_{j'}\sigma(\hat{e}_{ij'})+\varepsilon}$ 并维护边特征），将二值或分级脉冲免训练映射到连续乘法边门控是静态异构边权图转换的典型难点。

**是否需要训练或微调**：是（Adam 端到端训练）

**涉及的算子**：有向/无向边 `Sigmoid` 门控 $\sigma(A^\ell h_i^\ell + B^\ell h_j^\ell)$、Hadamard 逐元素门控邻居加权和、中心节点独立变换 $U^\ell h_i^\ell$、`BatchNorm`、`ReLU`、恒等残差连接

**关键数字**：在变长随机块模型（SBM）子图匹配与 10 簇半监督图聚类任务上（Section 4，第 6–9 页），较图 RNN 精度高 **3%–17%**、速度快 **1.5×–4×**，较非学习变分 Dirichlet 方法精度高 **36%**（达 **82%**），叠加超过 6 层时残差跳连带来 **10%** 精度增益（Abstract & Section 5）。

> 💭
> **与本方向的关系（判断）**：直接相关（作为 `MNIST`/`CIFAR10` 超像素图上表现最佳的各向异性边门控教师架构，代表了除 `Max` 与 `Softmax` 之外第三类关键非线性图聚合——`Sigmoid` 边门控）

### <a id="41b0e334-2e6f-8113-b556-ee0bd878e360"></a>Point Transformer / PTv1（2021）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2021，pp. 16259–16268；预印本 `arXiv:2012.09164`）
- **脉络：** 3 视觉图骨干
- **作者：** Hengshuang Zhao, Li Jiang, Jiaya Jia, Philip H.S. Torr, Vladlen Koltun
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#point-transformer--ptv12021
- **代码：** [https://github.com/POSTECH-CVLab/point-transformer](https://github.com/POSTECH-CVLab/point-transformer) （亦集成于 [https://github.com/Pointcept/Pointcept](https://github.com/Pointcept/Pointcept) ）
- **年份：** 2021
- **一句话：** 在点云局部 $k=16$ 近邻内引入基于特征向量减法与可学习三维相对位置编码的逐通道向量自注意力（Vector Attention），在室内大场景分割 `S3DIS Area 5` 上（论文自称）首次突破 70% mIoU 大关。
- **链接：** https://arxiv.org/abs/2012.09164
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Point Transformer
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：证明了逐通道调制的减法向量注意力比传统标量点积注意力在三维不规则点集上高出 5.8 个百分点 mIoU（Table 7），并验证了双支路相对坐标编码的必要性。

**留下的局限**：同时依赖局部向量 `Softmax` 注意力与降采样层的 $k=16$ 局部 `MaxPool`，且第一作者提供的复现实验仓未附预训练权重与开源许可证（注：参数量存在跨文献口径差异——原论文 Section 4.1 第 5 页报 `4.9M`，而 `PointNeXt` Table 1 第 6 页复测完整分割网报 `7.8M`）。

**是否需要训练或微调**：是（SGD 端到端训练）

**涉及的算子**：最远点采样（FPS）、三维坐标堆排序 $k$-NN（$k=16$）、向量减法自注意力（MLP + `ReLU` + `Softmax` 逐通道权重调制）、可训练相对位置编码 $\delta=\theta(p_i-p_j)$、`Transition Down` 局部 `MaxPool`、三线性插值上采样、`BatchNorm`、`ReLU`

**关键数字**：`S3DIS` 室内语义分割：`Area 5` 达 **70.4%** mIoU / **76.5%** mAcc / **90.8%** OA（Table 1，第 6 页），6 折交叉验证达 **73.5%** mIoU / **90.2%** OA（Table 2，第 6 页）；`ModelNet40` 分类达 **93.7%** OA / **90.6%** mAcc（Table 3，第 6 页）；`ShapeNetPart` 部件分割达 **86.6%** ins. mIoU / **83.7%** cat. mIoU（Table 4，第 7 页）；邻居数消融（Table 5，第 7 页）确认 $k=16$（70.4%）显著优于 $k=4$（59.6%）、$k=8$（67.7%）与 $k=32$（68.3%）。

> 💭
> **与本方向的关系（判断）**：背景（三维点云向量注意力里程碑，也正是脉络二中直接训练脉冲点云工作 `PPT` [CVPR 2024] 所脉冲化的原型架构）

### <a id="41b0e334-2e6f-8116-82d7-dcfddfefb7e0"></a>DGCNN（2019）

- **发表处：** ACM Transactions on Graphics（ACM TOG 2019，Vol. 38，No. 5，Article 146，pp. 1–12；预印本 `arXiv:1801.07829`）
- **脉络：** 3 视觉图骨干
- **作者：** Yue Wang, Yongbin Sun, Ziwei Liu, Sanjay E. Sarma, Michael M. Bronstein, Justin M. Solomon
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#dgcnn2019
- **代码：** [https://github.com/WangYueFt/dgcnn](https://github.com/WangYueFt/dgcnn) （官方推荐 PyTorch 版及预训练权重：[https://github.com/AnTao97/dgcnn.pytorch](https://github.com/AnTao97/dgcnn.pytorch) ）
- **年份：** 2019
- **一句话：** 提出边卷积（`EdgeConv`），在**每一层特征空间实时重算欧氏距离 ****$k$**** 近邻图**，对中心点特征与邻居相对特征差做不对称非线性映射后再取邻域逐通道最大值 `max`，奠定了动态图点云学习的经典范式。
- **链接：** https://arxiv.org/abs/1801.07829
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Dynamic Graph CNN for Learning on Point Clouds
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：克服了 `PointNet++` 只按输入三维物理坐标静态分组、深层无法按语义相似性跨空间聚合远处同类部件（如飞机两侧机翼）的局限。

**留下的局限**：**与 **`**ViG**`** 完全同构的三大免训练脉冲转换难点**——（1）每层特征空间欧氏距离动态 $k$-NN（1024 点 $k=20$，2048 点 $k=40$）；（2）每层对 $k$ 条边特征执行逐通道 `max` 聚合；（3）全网激活函数采用带负斜率 **0.2** 的 `**LeakyReLU**`（标准单向正阈值 IF 神经元会直接抹掉负半轴信息，需双极性带符号脉冲神经元支持）。

**是否需要训练或微调**：是（端到端训练浮点教师；`AnTao97/dgcnn.pytorch` 直接提供分类、部件分割与室内分割全套预训练权重）

**涉及的算子**：每层特征空间欧氏距离动态 $k$-NN（1024 点 $k=20$，2048 点 $k=40$）、不对称边卷积 `EdgeConv`（拼接 $[x_j-x_i \| x_i]$ 接 $1\times 1$ 卷积 + `BatchNorm` + `LeakyReLU(0.2)` + **邻域 **`**max**`** 池化**）、多尺度层间拼接 + 全局 `MaxPool` / `AvgPool`

**关键数字**：`ModelNet40` 分类（Tables 2 & 4，第 7–8 页）：1024 点（$k=20$）达 **92.9%** OA / **90.2%** mAcc，2048 点（$k=40$）达 **93.5%** OA / **90.7%** mAcc；固定首层静态 $k$-NN 消融掉至 **91.7%** OA（证实动态重算图带来 **+1.2%** 净增益，Table 4）；`ShapeNetPart` 部件分割达 **85.2%** mIoU（Table 6，第 10 页）；`S3DIS` 6 折室内分割达 **56.1%** mIoU / **84.1%** OA（Table 7，第 10 页）；在后续 `ScanObjectNN` 复测中改进训练可达 **86.0%** OA（见 `PointNeXt` Table 6）。

> 💭
> **与本方向的关系（判断）**：直接相关（**3D 点云动态图方向最核心的必选教师模型**：架构极其干净（仅 4 层 `EdgeConv`、1.8M 参数）、`MIT` 许可证、全套 PyTorch 预训练权重开箱即用，且脉络二中的 `NI-SGCN` [AAAI 2025] 因无法转换动态 `max` 被迫改成均值重训——免训练攻克原版 `DGCNN` 极具说服力！）

### <a id="41b0e334-2e6f-812b-8cc3-d8cb9aaedac4"></a>InfoGCN（2022）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2022，pp. 20186–20196）
- **脉络：** 3 视觉图骨干
- **作者：** Hyung-gun Chi, Myoung Hoon Ha, Seunggeun Chi, Sang Wan Lee, Qixing Huang, Karthik Ramani
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#infogcn2022
- **代码：** [https://github.com/stnoah1/infogcn](https://github.com/stnoah1/infogcn)
- **年份：** 2022
- **一句话：** 结合最大均值差异（MMD）变分信息瓶颈损失、每帧多头自注意力动态内在拓扑图卷积（SA-GC）与多跳相对骨骼多模态集成，提升人体骨架动作表征的紧凑性与判别力。
- **链接：** https://openaccess.thecvf.com/content/CVPR2022/html/Chi_InfoGCN_Representation_Learning_for_Human_Skeleton-Based_Action_Recognition_CVPR_2022_paper.html
- **核对人与日期：** Gemini，2026-11-16
- **标题：** InfoGCN: Representation Learning for Human Skeleton-based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了仅靠外在物理骨骼连边传递远端关节消息时随最短路径指数衰减的稀释效应，并压缩与动作类别无关的姿态冗余噪声。

**留下的局限**：官方仓库**既无开源许可证也未发布预训练权重**；且每层每帧均需计算多头缩放点积 `Softmax` 注意力矩阵（`SA-GC`）与块尾 `LayerNorm`，不适合作为免训练脉冲转换的首选骨架教师。

**是否需要训练或微调**：是（含变分重参数化噪声采样与 MMD 信息瓶颈损失端到端训练）

**涉及的算子**：多头缩放点积自注意力内在拓扑 `SA-GC`（$M=3$ 头，`Softmax` 乘可学习拓扑 $\tilde{\mathbf{A}}_m$）、多尺度时序卷积 `MS-TC`（含 `3×1 MaxPool`）、变分重参数化、`LayerNorm`、`BatchNorm`、`ReLU`

**关键数字**：6 模态集成精度（Table 1，第 6 页）：`NTU-RGB+D 60` X-Sub / X-View **93.0% / 97.1%**，`NTU-RGB+D 120` X-Sub / X-Set **89.8% / 91.2%**（单流 Joint 为 **85.1% / 86.3%**，4 流集成为 **89.4% / 90.7%**），`NW-UCLA` **97.0%**。

> 💭
> **与本方向的关系（判断）**：背景（代表“自注意力内在拓扑 + 信息瓶颈”骨架图路线，因无公开权重和许可证，转换选型中不作主教师）

### <a id="41b0e334-2e6f-817c-be36-d765126abfee"></a>CTR-GCN（2021）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2021，pp. 13359–13368；预印本 `arXiv:2107.12213`）
- **脉络：** 3 视觉图骨干
- **作者：** Yuxin Chen, Ziqi Zhang, Chunfeng Yuan, Bing Li, Ying Deng, Weiming Hu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#ctr-gcn2021
- **代码：** [https://github.com/Uason-Chen/CTR-GCN](https://github.com/Uason-Chen/CTR-GCN) （预训练权重：[https://drive.google.com/drive/folders/1C9XUAgnwrGelvl4mGGVZQW6akiapgdnd?usp=sharing](https://drive.google.com/drive/folders/1C9XUAgnwrGelvl4mGGVZQW6akiapgdnd?usp=sharing) ）
- **年份：** 2021
- **一句话：** 用“全局可学习共享邻接矩阵 + 按样本关节特征差动态推断的逐通道拓扑修正项”替代所有通道共用一张图的传统做法，成为近五年人体骨架动作识别使用最广的黄金基准（亦是脉冲骨架网络 `MK-SGN` 的蒸馏教师）。
- **链接：** https://arxiv.org/abs/2107.12213
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Channel-wise Topology Refinement Graph Convolution for Skeleton-Based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在不显著增加参数量（仅 1.46M）的前提下，解除不同特征通道必须按同一张拓扑聚合的强约束，大幅提升诸如“剪指甲”“打字”等精细手指交互动作的识别率。

**留下的局限**：（1）逐通道拓扑关联分支使用双极性 `**Tanh**` 激活（Table 3 显示改成非负 `ReLU`/`Sigmoid` 会掉点）并与特征做样本级动态张量乘；（2）多尺度时序模块含 `**3×1 MaxPool**` 分支；（3）官方仓库许可证为非商业 `CC BY-NC 4.0`。

**是否需要训练或微调**：是（SGD 训练 65 轮）

**涉及的算子**：逐通道拓扑精炼图卷积 `CTR-GC`（时序池化 + 关节特征差 $\tanh(\psi(x_i)-\phi(x_j))$ + 逐通道广播修正 $\mathbf{R}=\mathbf{A}+\alpha\mathbf{Q}$ + 通道图矩阵乘）、四分支多尺度时序卷积（含空洞卷积与 `**3×1 MaxPool**`）、`BatchNorm2d`、`ReLU`、`Tanh`

**关键数字**：单流模型（1.46M 参数，1.97G FLOPs）在 `NTU-RGB+D 120` X-Sub 上达 **84.9%**（Joint）/ **85.7%**（Bone，Tables 4–5，第 7–8 页）；4 流集成（Joint + Bone + JointMotion + BoneMotion）：`NTU-RGB+D 60` X-Sub / X-View **92.4% / 96.8%**（Table 6，第 8 页），`NTU-RGB+D 120` X-Sub / X-Set **88.9% / 90.6%**（Table 5，第 8 页），`NW-UCLA` **96.5%**（Table 7，第 8 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（**骨架动作识别方向动态拓扑首选教师模型**：官方公开了 Google Drive 预训练权重，且脉络二中的 `MK-SGN` [2026] 正是用 `CTR-GCN` 当教师从头蒸馏训练脉冲网络——若我们能免训练直接转换 `CTR-GCN`，即可与重训蒸馏路线正面同台比较！）

### <a id="41b0e334-2e6f-8181-86a1-e796fe38d874"></a>PointNeXt（2022）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2022，Vol. 35，pp. 23192–23204；预印本 `arXiv:2206.04670`）
- **脉络：** 3 视觉图骨干
- **作者：** Guocheng Qian, Yuchen Li, Houwen Peng, Jinjie Mai, Hasan Abed Al Kader Hammoud, Mohamed Elhoseiny, Bernard Ghanem
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#pointnext2022
- **代码：** [https://github.com/guochengqian/PointNeXt](https://github.com/guochengqian/PointNeXt) （预训练权重：[https://guochengqian.github.io/PointNeXt/modelzoo/](https://guochengqian.github.io/PointNeXt/modelzoo/) ）
- **年份：** 2022
- **一句话：** 系统证明经典 `PointNet++` 落后于新型点云网络很大程度源于训练配方老旧与缺乏残差缩放；通过引入现代数据增强/优化器、相对坐标半径归一化与分离式倒残差 `InvResMLP` 模块，在不改球查询+`MaxPool` 骨架的前提下重夺分类与分割双料第一且推理快 10 倍。
- **链接：** https://arxiv.org/abs/2206.04670
- **核对人与日期：** Gemini，2026-11-16
- **标题：** PointNeXt: Revisiting PointNet++ with Improved Training and Scaling Strategies
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了原始 `PointNet++` 加深加宽时梯度消失、过拟合以及邻域三层 MLP 计算过重难以扩展的瓶颈。

**留下的局限**：虽然建图完全基于**输入固定的三维物理坐标球查询**（彻底无特征空间动态建图漂移！），但每一块的核心归约算子仍然是 $k=32$** 个球内邻居的通道逐元素 **`**MaxPool**`；若像以往脉冲点云工作那样强行改成 `AvgPool` 就必须重新训练，而免训练直接用二值脉冲过 `MaxPool` 则会产生阶数偏差。

**是否需要训练或微调**：是（浮点教师使用 `AdamW` + 标签平滑 + 点重采样/丢色增强训练）

**涉及的算子**：最远点采样（FPS）、三维坐标静态球查询（$k=32$）、相对坐标除以查询半径归一化 $(\mathbf{p}_j^l-\mathbf{p}_i^l)/r^l$、邻域单层 MLP + **通道 **`**MaxPool**`** 归约** + 两层 $4\times$ 倒残差逐点 MLP（`InvResMLP`）、`BatchNorm`、`ReLU`

**关键数字**：`ScanObjectNN (PB_T50_RS)` 真实扫描分类（Table 2，第 7 页）：仅靠改进训练策略就把原封不动的 `PointNet++` 从 77.9% 提至 **86.1±0.7%**，`PointNeXt-S`（1.4M 参数）进一步达 **87.7±0.4%** OA（快于 `PointMLP` **10×**）；`ModelNet40` `PointNeXt-S` 达 **93.2±0.1%**（C=32）/ **94.0%**（C=64）；`S3DIS` 6-fold 语义分割 `PointNeXt-XL` 达 **74.9%** mIoU（Area 5 **70.5±0.3%**，Table 1，第 6 页）；`ScanNet V2` Test 达 **71.2%** mIoU；`ShapeNetPart` 达 **87.0±0.1%** ins. mIoU（Table 3，第 7 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（**3D 点云静态坐标图方向首选教师模型**：`MIT` 许可证、HuggingFace 官方模型库齐全、纯 `BatchNorm + ReLU` 无复杂超越函数，唯一非线性聚合瓶颈就是纯粹的邻域 `MaxPool`，与 `DGCNN` 的动态特征 $k$-NN 形成绝佳对照）

### <a id="41b0e334-2e6f-819f-8308-ddd5dac0d8f4"></a>Benchmarking GNNs 超像素视觉图基准（2022）

- **发表处：** Journal of Machine Learning Research（JMLR 2022，Vol. 23，No. 329，pp. 1–48；首版预印本 `arXiv:2003.00982`，2020）
- **脉络：** 3 视觉图骨干
- **作者：** Vijay Prakash Dwivedi, Chaitanya K. Joshi, Anh Tuan Luu, Thomas Laurent, Yoshua Bengio, Xavier Bresson
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#benchmarking-gnns-超像素视觉图基准2022
- **代码：** [https://github.com/graphdeeplearning/benchmarking-gnns](https://github.com/graphdeeplearning/benchmarking-gnns)
- **年份：** 2022
- **一句话：** 建立固定 100K / 500K 参数预算的公平图神经网络评测框架，其中将 `MNIST` 与 `CIFAR-10` 制成 SLIC 超像素 $k=8$ 近邻图，系统量化了同构求和/均值聚合与各向异性门控/`Max` 聚合在视觉图分类上的巨大性能鸿沟。
- **链接：** http://jmlr.org/papers/v23/22-0567.html
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Benchmarking Graph Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：终结了早期 GNN 仅在极小引文图（Cora/Citeseer）或高方差 TU 数据集上无法区分架构优劣的混乱局面，给出了固定静态视觉图上五大主流消息传递算子的标准同预算基线。

**留下的局限**：超像素图拓扑由 SLIC 2D 坐标静态预计算（不含特征空间动态建图），且在 `CIFAR10` 超像素（仅 85–150 节点）上绝对精度上限约 67%–70%，需要与 `ImageNet` 级的 `ViG` / `MobileViG` 配合才能覆盖完整视觉规模。

**是否需要训练或微调**：是（提供 4 随机种子统一训练脚本，单卡数小时内精确复现全部教师模型）

**涉及的算子**：SLIC 超像素 2D 坐标 $k=8$ 高斯边权建图、`GatedGCN`（`Sigmoid` 软边门控 + 显式边特征更新）、`GraphSAGE`（邻域 `**Max**`** 池化**聚合 Eq. 8）、`GAT`（多头 `LeakyReLU + Softmax` 注意力 + `ELU`）、`GIN`（$(1+\epsilon)$ 求和）、`GCN`（对称度归一化均值）、`BatchNorm`、`ReLU`、拉普拉斯特征向量位置编码（`LapPE`）

**关键数字**：视觉超像素图分类（$L=4, \approx 104\text{K}$ 参数，Table 7，第 30 页，`MNIST` / `CIFAR10` 测试精度）：各向异性 `GatedGCN` 最高达 **97.340±0.143% / 67.312±0.311%**，带邻域 `Max` 聚合的 `GraphSage` 紧随其后达 **97.312±0.097% / 65.767±0.308%**，`GAT` 达 **95.535±0.205% / 64.223±0.455%**，而纯求和/均值的 `GIN`（**96.485% / 55.255%**）与对称度归一化 `GCN`（**90.120% / 54.142%**）在 `CIFAR10` 上落后 `GatedGCN` 与 `GraphSage-Max` 逾 **11–13 个百分点**！

> 💭
> **与本方向的关系（判断）**：直接相关（这组实验数字是论证本项目核心动机的铁证——在静态视觉图上，只要为了容易转脉冲而退回同构 `GCN`/`GIN` 求和均值，精度就会暴跌 11%–13%；必须攻克 `Max` 聚合与各向异性边门控的免训练脉冲化！且实验仓 `ZtL-sysu/gnn2snn` 与 `DeNA-SGN` 均使用该超像素基准）

### <a id="41b0e334-2e6f-81d5-8665-c55f7cb453c6"></a>AEGNN（2022）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2022，pp. 12371–12381；预印本 `arXiv:2203.17149`）
- **脉络：** 3 视觉图骨干,4 事件驱动与增量推理
- **作者：** Simon Schaefer, Daniel Gehrig, Davide Scaramuzza
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#aegnn2022
- **代码：** [https://github.com/uzh-rpg/aegnn](https://github.com/uzh-rpg/aegnn)
- **年份：** 2022
- **一句话：** 把事件相机输出建模为随时间演化的三维时空半径图，推导出在同步批量图上训练、在测试期只沿新事件的 $k$-hop 局部子图做逐事件异步增量更新的通用规则，把单事件计算量降低最多 11–20 倍、延迟降低 8 倍。
- **链接：** https://arxiv.org/abs/2203.17149
- **核对人与日期：** Gemini，2026-11-16
- **标题：** AEGNN: Asynchronous Event-based Graph Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

##### 来自脉络 3 视觉图骨干 的记录

**解决的难点**：解决了此前事件图网络（如 `RG-CNNs`、`EvS-S`）每来一个新事件都必须整图重算全部节点激活的严重算力浪费，同时支持多层层次化样条图卷积与体素最大池化。

**留下的局限**：（1）**无任何幅度变化门控（**$\Delta$**-threshold）**：每个新事件无条件精确传播至第 $k$ 层的完整 $k$-hop 邻域，7 层深网在稠密事件区子图仍会迅速扩散（后续被 `DAGr` 的有向图与 `max` 池化截断改进）；（2）仍是浮点连续值网络（`SplineConv + ELU + BN + MaxPool`），且官方仓库未公开预训练模型文件（需自行在 `N-Cars` / `N-Caltech101` 上训练）。

**是否需要训练或微调**：是（同步批量训练浮点模型；测试期通过 `make_model_asynchronous()` 免重训转为等价异步局部子图推理）

**涉及的算子**：均匀事件抽样（$K=10$）、时空欧氏半径建图（最大度数 $D_{\max}=32$）、$k$-hop 局部子图增量消息传递、三次 B 样条卷积 `SplineConv`（$m=3$，度归一化求和）、$12\times 16\times 16$ 时空体素网格 `MaxPool`、`ELU`、`BatchNorm`

**关键数字**：事件分类（Table 1，第 6 页）：`N-Cars` 精度 **94.5%**、仅耗 **0.47 MFLOP/ev**（较次优异步图方法 `NVS-S` 省算力 **11×**，较 `EvS-S` 省 **13×**；25k 事件平均仅 `30±4.8 kFLOPs/ev`，第 7 页），`N-Caltech101` 精度 **66.8%**、**7.31 MFLOP/ev**（25k 事件异步更新 **129ms** vs 稠密 GNN **1014ms**，加速 **8×**，第 8 页）；事件检测（Table 3，第 8 页）：`N-Caltech101` **59.5%** mAP（`7.41 MFLOP/ev`），`Gen1` **16.3%** mAP（表格列为 **5.26 MFLOP/ev**，正文第 8 页一处笔误写为 `0.39 MFLOPs/ev`，特此注记冲突）。

> 💭
> **与本方向的关系（判断）**：直接相关（兼具脉络三事件相机图教师与脉络四 $k$-hop 异步图推理奠基工作的双重地位；`MIT` 协议且代码模块化极好，其 `make_model_asynchronous` 可直接作为事件驱动脉冲图推理的工程参照）

##### 来自脉络 4 事件驱动与增量推理 的记录

**标题**：AEGNN: Asynchronous Event-based Graph Neural Networks

**作者**：Simon Schaefer, Daniel Gehrig, Davide Scaramuzza

**发表处**：IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2022）；arXiv v3 是更新版，封面写明“更新了第 5 节的计算量计算”

**链接**：[https://arxiv.org/abs/2203.17149](https://arxiv.org/abs/2203.17149) ；代码：项目页 [https://uzh-rpg.github.io/aegnn/](https://uzh-rpg.github.io/aegnn/)

**核对深度**：全文（arXiv 更新版）

**一句话**：把事件流当作不断生长的时空图，每来一个新事件只重算受影响的局部子图。

**解决的难点**：第 5 页 4.2 节推出：第 1 层只需更新新节点的 1 跳子图，之后每层多扩一跳，第 N 层更新 N 跳子图，结果与全图计算相同；在同步数据上训练，测试时以异步方式部署。

**留下的局限**：扩散是无条件的——只要拓扑上可达就重算，没有变化量阈值；深层的节省迅速变小（第 7 页 Fig. 4(b) 逐层节省）；靠下采样、半径和最大邻居数、图池化压制计算量。

**是否需要训练或微调**：是（训练普通 GNN；异步化本身不需要改权重）

**涉及的算子**：半径建图、样条卷积、max 图池化、ELU、BatchNorm

**关键数字**：**数字冲突**——CVPR 原版摘要称计算量“最多降 200 倍”（据检索到的 CVF 页面摘要，见 SL-65；未打开 CVF PDF）；arXiv 更新版摘要改为“比最好的异步方法低 11 倍”，延迟比普通 GNN 低 8 倍（第 1 页）。N-Cars 上 0.47 MFLOPs/ev、精度 0.945（第 6 页 Table 1）；N-Caltech101 上 25000 事件时普通 GNN 每事件 11.2×10³ MFLOPs，AEGNN 6.11 MFLOPs（第 7 页 Table 2）；Fig. 4(a)：GNN 比稠密 CNN 少 10 倍，异步化再少 30 倍。

> 💭
> **与本方向的关系（判断）**：直接相关

### <a id="41b0e334-2e6f-81df-8f5a-cfd0b48ea602"></a>2s-AGCN（2019）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2019，pp. 12026–12035；预印本 `arXiv:1805.07694`）
- **脉络：** 3 视觉图骨干
- **作者：** Lei Shi, Yifan Zhang, Jian Cheng, Hanqing Lu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#2s-agcn2019
- **代码：** [https://github.com/lshiwjx/2s-AGCN](https://github.com/lshiwjx/2s-AGCN)
- **年份：** 2019
- **一句话：** （论文自称）首次把骨架图邻接矩阵拆成“物理先验图 + 全局可学习参数图 + 按样本特征计算的嵌入高斯 Softmax 注意力图”三项之和，并提出关节坐标与骨骼方向向量双流融合范式。
- **链接：** https://arxiv.org/abs/1805.07694
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Two-Stream Adaptive Graph Convolutional Networks for Skeleton-Based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了 `ST-GCN` 全层全样本共用固定人体物理连边、无法直接建立“拍手”动作中左右手强关联的缺陷，并开创了此后所有骨架 GNN 标配的关节+骨骼多流评测体系。

**留下的局限**：官方仓库未公开预训练权重且采用 `CC BY-NC 4.0` 许可证；样本自适应项 $\mathbf{C}_k$ 在每层引入了全关节时空展平特征矩阵乘法与 `Softmax`。

**是否需要训练或微调**：是（SGD 训练 50–65 轮）

**涉及的算子**：三重自适应邻接矩阵求和（物理归一化图 $\mathbf{A}_k$ + 无约束可学习矩阵 $\mathbf{B}_k$ + 嵌入高斯点积 `Softmax` 相似度图 $\mathbf{C}_k$，$K_v=3$）、$K_t\times 1$ 时序卷积、`BatchNorm2d`、`ReLU`、关节/骨骼双流融合

**关键数字**：`NTU-RGB+D 60` X-Sub / X-View 达 **88.5% / 95.1%**（其中单关节流 `Js-AGCN` 在 X-View 达 **93.7%**、单骨骼流 `Bs-AGCN` 达 **93.2%**，Tables 2–3，第 8 页）；`Kinetics-Skeleton` Top-1 / Top-5 达 **36.1% / 58.7%**（较 `ST-GCN` 提升 +5.4% Top-1，Table 4，第 8 页）。

> 💭
> **与本方向的关系（判断）**：背景（承上启下连接固定骨架图 `ST-GCN` 与逐通道动态图 `CTR-GCN` 的经典里程碑；实际实验选教师时，`CTR-GCN` 与 `ST-GCN` 因公开预训练权重而更优）

### <a id="41b0e334-2e6f-8143-af16-c5ee19448d7f"></a>FTBC（2024）

- **发表处：** European Conference on Computer Vision（ECCV 2024，LNCS Vol. 15105，pp. 155–173；预印本 `arXiv:2403.18388`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Xiaofeng Wu, Velibor Bojkovic, Bin Gu, Kun Suo, Kai Zou
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#ftbc2024
- **代码：** [https://github.com/shizukanaskytree/FTBC](https://github.com/shizukanaskytree/FTBC)
- **年份：** 2024
- **一句话：** 无需反向传播，只用一个校准批次做纯前向统计，在**每一个时间步 ****$t$**** 独立计算逐通道均值残差并注入随时间变化的动态偏置 ****$B^{(\ell)}(t)$**，可即插即用叠加在标准 ReLU 网络或 QCFS 网络之上。
- **链接：** https://arxiv.org/abs/2403.18388
- **核对人与日期：** Gemini，2026-11-16
- **标题：** FTBC: Forward Temporal Bias Correction for Optimizing ANN-SNN Conversion
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：传统偏置校准（如 `SNNC-AP` 的 BC）只在总时间步 $T$ 末端对齐总均值，忽略了早期时间步的瞬态偏差积累；按步校准 $B^{(\ell)}(t)$ 用几秒前向计算即可在低步下显著提分。

**留下的局限**：单独用于未经 QCFS 重训的标准 ReLU `ResNet-34` 时，在 $T\le 8$ 下精度依然很低（$T=16$ 仅 60.68%），若要压到 $T=4$ 仍需搭配重训过的 QCFS 源网络；且按空间高宽求通道均值的公式假定规则二维特征图，未处理 `MaxPool` 或动态图。

**是否需要训练或微调**：否（纯前向逐时间步均值误差统计，支持直接校准预训练 ReLU ANN，也可叠加于 QCFS 模型）

**涉及的算子**：逐层逐时间步通道动态偏置注入 $B^{(\ell)}(t)$（Algorithm 1，第 9 页）、百分位数/MMSE 阈值初始化、IF 软复位神经元

**关键数字**：`ImageNet` 上直接免训练转换标准 ReLU 模型（`Ours*`，Section 4.2 Table 1，第 10 页）：`VGG-16`（源 **75.36%**）在 $T=8 / 16 / 32$ 达 **64.20% / 71.19% / 73.89%**；`ResNet-34`（源 **75.66%**）在 $T=16 / 32 / 64$ 达 **60.68% / 70.88% / 73.79%**；若叠加在 QCFS 重训源模型上，则 `ResNet-34` 在 $T=4 / 8$ 达 **68.76% / 72.73%**，`VGG-16` 在 $T=4 / 8$ 达 **71.22% / 73.32%**（Table 1）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（把二维特征图空间均值改成图节点集 $V$ 上的均值，即可零成本移植为图转换 baseline 的逐时间步节点偏置校准器）

### <a id="41b0e334-2e6f-814f-9595-dcc2bb722d1c"></a>STA（2024）

- **发表处：** The Twelfth International Conference on Learning Representations（ICLR 2024，OpenReview ID: `135eKq323G`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yizhou Jiang, Kunlin Hu, Tianren Zhang, Haichuan Gao, Yuqian Liu, Ying Fang, Feng Chen
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#sta2024
- **代码：** [https://github.com/ViviaHu/STA](https://github.com/ViviaHu/STA)
- **年份：** 2024
- **一句话：** （论文自称）首个**完全不修改源架构、不微调**的预训练 Transformer 全脉冲转换方法：用离线在合成随机数据上预训练的小型脉冲子网（通用群算子 UGO）替代 GELU、LayerNorm、Softmax，并用时间步间布尔“与（AND）”加记忆修正逼近动态脉冲流乘法。
- **链接：** https://openreview.net/forum?id=135eKq323G
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking Transformer: Spatial-Temporal Attention for Converting Any Pretrained Transformers into Spiking Neural Networks（OpenReview 正式收录标题为 *Spatio-Temporal Approximation: A Training-Free SNN Conversion for Transformers*）
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：无需源训练数据、无需把 LN/GELU 改成 BN/ReLU，直接将 CLIP ViT 等现成预训练多模态视觉基座转换为纯二值脉冲网络完成零样本分类。

**留下的局限**：时间步开销极大（ImageNet 上需 $T=64\sim 256$ 步才能接近源精度）；且每个标量 GELU/指数/平方根运算都要展开成 $N=8\sim 32$ 个隐层 IF 神经元组成的 UGO 子网，神经元与突触规模显著膨胀，也未涉及离散选邻居。

**是否需要训练或微调**：否（UGO 仅在合成分布数据上离线拟合一次即可复用，对预训练 Transformer 完全免训练）

**涉及的算子**：通用群算子（UGO，$N\in\{8,16,32\}$ 个隐层 IF 神经元拟合 GELU / 指数 / 倒数 / 平方根）、时空注意力脉冲点积（TCSA，布尔 AND 估计—修正单元）、逐神经元 MMSE 阈值校准、突触噪声调制（SNM）与脉冲簇（$\Gamma=2$）

**关键数字**：零样本转换预训练 `CLIP ViT-B/32`（Section 4.2 Table 1，第 8 页）：`CIFAR-10`（源 **89.74%**）在 $T=32 / 64 / 256$ 达 **87.71% / 88.88% / 89.56%**；微调版 `ViT-B/32` 在 `ImageNet-1K`（源 **83.60%**，Appendix Table 5，第 21 页）在 $T=32 / 64 / 128 / 256$ 分别达 **78.72% / 82.33% / 82.61% / 82.79%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（确立了免训练全脉冲 Transformer 转换的可行性下限，同时也是定向问题 Q3 被引检索的五篇核心种子论文之一）

### <a id="41b0e334-2e6f-8155-9fec-de2b6e6cd907"></a>Fast-SNN（2023）

- **发表处：** IEEE Transactions on Pattern Analysis and Machine Intelligence（IEEE TPAMI 2023，Vol. 45, No. 12，pp. 14546–14562，DOI: `10.1109/TPAMI.2023.3275769`；预印本 `arXiv:2305.19868`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yangfan Hu, Qian Zheng, Xudong Jiang, Gang Pan
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#fast-snn2023
- **代码：** [https://github.com/yangfan-hu/Fast-SNN](https://github.com/yangfan-hu/Fast-SNN)
- **年份：** 2023
- **一句话：** 严格证明 $b$-bit 无符号均匀量化激活等价于 $T=2^b-1$ 步脉冲率编码，通过引入带正负符号的积分发放神经元（SIF）消除发放顺序错位引起的负残余误差，并用逐层代理网络微调将分类、检测与分割统一压至 $T=3, 7, 15$ 步。
- **链接：** https://arxiv.org/abs/2305.19868
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Fast-SNN: Fast Spiking Neural Network by Converting Quantized ANN
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：从数学上打通了“$b$-bit 量化网络”与“$2^b-1$ 步带符号脉冲网络”的等价性，解释了单极性 IF 神经元因先正后负脉冲到达顺序引起多发错脉冲（spurious spikes）的机理并用负向纠错脉冲抵消。

**留下的局限**：**重度依赖重训与改结构**——不仅要求对源网络做量化感知训练（QAT）和逐层最小二乘微调，而且明确要求**删掉源网络中的 **`**MaxPool**`** 层并改用步幅为 2 的卷积下采样重训**（Section 4.1）。

**是否需要训练或微调**：是（需先移除 `MaxPool` 做 $b$-bit QAT 训练，转换时再对每层做代理 ANN 梯度微调）

**涉及的算子**：带符号积分发放神经元（Signed IF / SIF，带负纠错脉冲抑制伪发放）、$b$-bit 均匀激活量化（对应 $T=2^b-1$）、移除 `MaxPool` 改步幅卷积、逐层时空误差代理微调

**关键数字**：`ImageNet` 上（Section 4.2 Table 5，第 9 页），`VGG-16` 在 $T=3 / 7$ 达 **71.31% / 72.95%**，`ResNet-34` 在 $T=3 / 7$ 达 **66.22% / 71.31%**；`PASCAL VOC 2007` 目标检测 `YOLOv2 (ResNet-34)`（源 76.08% mAP，Section 4.4 Table 9，第 12 页）在 $T=3 / 7 / 15$ 达 **62.51% / 73.43% / 75.77% mAP**；`PASCAL VOC 2012` 语义分割 `ResNet-34+ASPP`（源 72.1% mIoU，Table 10，第 14 页）在 $T=7 / 15$ 达 **66.7% / 69.7% mIoU**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（SIF 用负脉冲撤回早期误发正脉冲的机制，与脉冲图 `max` 池化抑制相位高估同源；其 $T=2^b-1 \leftrightarrow b\text{-bit}$ 精确对应关系直接支撑 M4 同比特量化公平对照设计）

### <a id="41b0e334-2e6f-8161-8d98-c2887aac0334"></a>SpiCalib 与 MLIPooling（2022）

- **发表处：** arXiv（2022 年 7 月预印本，`arXiv:2207.02702`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yang Li, Xiang He, Yiting Dong, Qingqun Kong, Yi Zeng
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spicalib-与-mlipooling2022
- **代码：** 未公开
- **年份：** 2022
- **一句话：** 用发放间隔（ISI）驱动的双突触校正首脉冲延迟误差，并提出支持重叠窗口（$k\neq s$）和 `ceil_mode` 补零边界的修正侧抑制最大池化 `MLIPooling`，免重训转换了原封不动的 YOLO 检测器与 FCN 分割网。
- **链接：** https://arxiv.org/abs/2207.02702
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spike Calibration: Fast and Accurate Conversion of Spiking Neural Network for Object Detection and Segmentation（PDF 第 1 页与 arXiv API；本条早先误写成另一篇论文的标题，复查时已更正；方法简称 SpiCalib）
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：补齐了 `LIPooling`（IJCAI 2022）在处理重叠步幅最大池化（如 ResNet 首层与目标检测主干中的 $3\times 3, s=2$ 或 $s=1$ `MaxPool`）时的边界与跨窗干扰缺陷，不改源模型一行结构即可做检测与分割转换。

**留下的局限**：属于纯单极性率编码路线，在目标检测与分割任务上仍需 $T=64\sim 512$ 个时间步才能收敛，远未达到个位数时间步；且 `MLIPooling` 同样假定非负脉冲计数，不支持负特征差取最大。

**是否需要训练或微调**：否（利用贝叶斯优化搜索 $p$-范数归一化因子，完全免重训、不修改源模型 `MaxPool` 层）

**涉及的算子**：基于脉冲发放间隔（ISI）的双突触在线偏差监测与校正（`SpiCalib`）、支持重叠核与 `ceil_mode` 的修正侧抑制最大池化（`MLIPooling`）、贝叶斯优化 $p$-Norm 权重归一化

**关键数字**：目标检测（Section 4.3 Table 2 & Table 3，第 8 页）：`PASCAL VOC` `YOLO (ResNet-50)`（源 **75.28% mAP**）在 $T=64 / 128 / 512$ 免训练转换达 **62.13% / 73.78% / 75.21% mAP**；`MS COCO`（源 **45.28%**）在 $T=128 / 512$ 达 **43.61% / 45.32%**；语义分割 `PASCAL VOC 2012` `FCN`（源 **60.20% mIoU**，Table 4 & Section 4.4，第 9 页）在 $T=64 / 256$ 达 **55.66% / 59.56% mIoU**（$T=64$ 时估算能耗为 ANN 的 **0.492×**）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（目前少有的在真实重叠窗口 `MaxPool` 检测/分割主干上做纯脉冲免重训转换的完整对照方案）

### <a id="41b0e334-2e6f-81aa-9ccc-f5ca27331479"></a>COS（2023）

- **发表处：** The Eleventh International Conference on Learning Representations（ICLR 2023；预印本 `arXiv:2302.10685`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Zecheng Hao, Jianhao Ding, Tong Bu, Tiejun Huang, Zhaofei Yu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#cos2023
- **代码：** [https://github.com/hzc1208/ANN2SNN_COS](https://github.com/hzc1208/ANN2SNN_COS)
- **年份：** 2023
- **一句话：** 通过观察神经元在结束时刻的残余膜电位 $v^l(T)$ 是否落在异常区间（$<0$ 或 $>\theta^l$）来识别脉冲到达不均匀导致的“多发/少发偏移脉冲”，在推理期对每个测试样本先跑 $\rho$ 步预探测调整初始膜电位，再正式跑 $T$ 步。
- **链接：** https://arxiv.org/abs/2302.10685
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Bridging the Gap Between ANNs and SNNs by Calibrating Offset Spikes
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：（论文自称）首次专门针对 `QCFS` 遗留的第三类误差——“不均匀性误差（unevenness error）”给出逐神经元修正法则，使正式推理步 $T=1\sim 4$ 的精度显著跃升。

**留下的局限**：（1）源网络仍须经过 `QCFS`（含 `MaxPool → AvgPool` 替换）重训；（2）**推理总延迟容易被表观 **$T$** 误导**——Appendix Algorithm 1（第 19 页）显示对每一张新测试图都必须串行执行两趟仿真（先跑 $\rho$ 步算残余电位偏移，重置后再跑 $T$ 步），故标称 $T=2, \rho=4$ 实际消耗 **6 个时间步**，$T=8, \rho=8$ 实际消耗 **16 个时间步**！

**是否需要训练或微调**：部分（偏移校准在推理期完成无需微调，但**源 ANN 必须先按 QCFS 替换为 **`**AvgPool**`** + 阶梯激活从头重训**）

**涉及的算子**：QCFS 阶梯激活、残余膜电位越界判据（$v^l(\rho)<0$ 或 $v^l(\rho)>\theta^l$）、每个测试样本两阶段推理（$\rho$ 步探测 + $T$ 步正式仿真）

**关键数字**：`ImageNet` `ResNet-34`（QCFS 源 **74.22%**，Section 4.2 Table 1 & Table 2，第 7–8 页）：在 $\rho=4$ 下名义 $T=1 / 2 / 4$（实际总步数 $5 / 6 / 8$）达 **61.84% / 67.12% / 71.86%**；在 $\rho=8, T=8$（实际总步数 16）达 **74.17%**；`VGG-16`（源 **74.19%**）在 $\rho=4, T=2$ 达 **70.59%**、$\rho=8, T=8$ 达 **74.19%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（提醒我们在做公平能耗与延迟对比时，必须把预探测/预热步数计入真实计算量；其利用越界膜电位诊断相位错位多发脉冲的判据可辅助误差归因）

### <a id="41b0e334-2e6f-81e2-a77b-f2c3063d849f"></a>SpikeZIP-TF（2024）

- **发表处：** Proceedings of the 41st International Conference on Machine Learning（ICML 2024，PMLR Vol. 235；预印本 `arXiv:2406.03470`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Kang You, Zekai Xu, Chen Nie, Zhijie Deng, Xiang Wang, Qinghai Guo, Zhezhi He
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spikezip-tf2024
- **代码：** [https://github.com/Intelligent-Computing-Research-Group/SpikeZIP-TF](https://github.com/Intelligent-Computing-Research-Group/SpikeZIP-TF)
- **年份：** 2024
- **一句话：** 先将预训练 Transformer 的 GELU 换成 ReLU 微调并做 LSQ 量化感知蒸馏训练（QAT），再通过三值正负脉冲神经元 `ST-BIF+`、三项分解脉冲自注意力 `SESA` 与累积差分包装器等效转换为脉冲 Transformer。
- **链接：** https://arxiv.org/abs/2406.03470
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SpikeZIP-TF: Conversion is All You Need for Transformer-based SNN
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：证明了在相同时间步或更低功耗下，基于 QAT 转换得到的脉冲 ViT 在 ImageNet 精度上显著优于从头直接训练的 `Spikformer` / `Spike-driven Transformer` 系列。

**留下的局限**：（1）**绝非免训练转换**——Appendix A.4（第 15–17 页）明确记载需先做 50–100 轮 `GELU → ReLU` 替换微调，再做 50–300 轮带知识蒸馏的 LSQ 量化感知训练；（2）所谓 `Spike-Softmax` 与 `Spike-LayerNorm`（公式 5）实际上仍是对累积输入 $X_t$ 直接调用数字浮点 $\sigma(X_t)$ 后输出相邻步差值 $O_t-O_{t-1}$（Claude v1 草稿笼统称其“设计了脉冲化的 Softmax 和 LayerNorm”并不准确）；（3）推理仍需 $T=32\sim 128$ 步。

**是否需要训练或微调**：是（需两阶段重训微调：50–100 轮 GELU→ReLU 微调 + 50–300 轮 LSQ QAT 蒸馏训练）

**涉及的算子**：对称三值双向积分发放神经元（`ST-BIF+`，脉冲取值 $\{-1,0,+1\}$）、三项增量更新脉冲等效自注意力（`SESA`）、数字累积差分包装算子 `Spike-Softmax` / `Spike-LayerNorm`、LSQ 激活量化与 ReLU

**关键数字**：`ImageNet-1K` 上（Section 4.2 Table 5，第 7 页），`SViT-S-32Level` / `SViT-B-32Level` / `SViT-L-32Level` 在 $T=64$（对应 32 量化级×2）分别达 **81.45% / 82.71% / 83.82%**（源量化 ViT 为 81.59% / 82.85% / 83.86%）；NLP `RoBERTa` 在 `SST-2`（$T=128$，Table 6，第 8 页）达 **93.79%**、`MNLI` 达 **85.03%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（`ST-BIF+` 正负三值脉冲神经元解决负向过发放引起的残差偏置，对含负特征的图聚合有启发；同时也是定向问题 Q3 被引追踪的五篇种子论文之一）

### <a id="41b0e334-2e6f-81ef-88e5-e7e615bec312"></a>MST（2023）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2023，pp. 1761–1771；预印本 `arXiv:2210.01208`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Ziqing Wang, Yuetong Fang, Jiahang Cao, Qiang Zhang, Zhongrui Wang, Renjing Xu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#mst2023
- **代码：** 未公开
- **年份：** 2023
- **一句话：** 早期将 Swin Transformer 转换为脉冲网络的尝试——把源模型的 `LayerNorm` 改成 `BatchNorm`、激活改成 `QCFS` 从头重训，再引入随机脉冲掩码（RSM）配合自蒸馏微调削减脉冲数量。
- **链接：** https://arxiv.org/abs/2210.01208
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Masked Spiking Transformer
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：作为首批跑通层次化窗口视觉 Transformer（Swin-T）转换的工作，验证了随机掩蔽冗余脉冲在保持精度的同时可额外省电约四分之一。

**留下的局限**：（1）必须大改源架构并从头重训 + 蒸馏微调；（2）注意力里的 `Softmax` 依然保留原始模拟浮点运算未做脉冲化；（3）即便用了 QCFS，在 ImageNet 上仍需 $T=128\sim 512$ 步才能达到 77.88%–78.51%。

**是否需要训练或微调**：是（需把 `Swin-T` 的 LN 换 BN、GELU/ReLU 换 QCFS 从头训练，再为随机脉冲掩码做知识蒸馏微调）

**涉及的算子**：QCFS 量化阶梯激活、BatchNorm 替代 LayerNorm、随机脉冲掩码（RSM）、模拟浮点 Softmax 窗口注意力

**关键数字**：`ImageNet-1K` 上改装版 `Swin-T`（Section 4.2 Table 1，第 5 页）在 $T=128 / 256 / 512$ 分别达 **77.88% / 78.37% / 78.51%**（注：0% 掩码下 `Swin-T` 在 $T=128$ 为 78.51% 的接近值，开启 RSM 后在 `CIFAR-10` 上 75% 掩码率取得 **97.29%** 并降低 **26.8%** 功耗，Section 4.3 Table 3，第 8 页）。

> 💭
> **与本方向的关系（判断）**：背景（展示了早期视觉 Transformer 转换不得不“改结构重训 + 保留浮点 Softmax + 数百时间步”的历史局限）

### <a id="41b0e334-2e6f-81fb-8512-ef5304537699"></a>ECMT（2024）

- **发表处：** Proceedings of the 32nd ACM International Conference on Multimedia（ACM MM 2024，pp. 10688–10697，DOI: `10.1145/3664647.3680852`；预印本 `arXiv:2502.21193`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Zihan Huang, Xinyu Shi, Zecheng Hao, Tong Bu, Jianhao Ding, Zhaofei Yu, Tiejun Huang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#ecmt2024
- **代码：** [https://github.com/h-z-h-cell/Transformer-to-SNN-ECMT](https://github.com/h-z-h-cell/Transformer-to-SNN-ECMT)
- **年份：** 2024
- **一句话：** `DCGS` 的直接前身——用正负 $2n$ 级二次幂多阈值神经元（MT）降低单步量化误差，并为非线性算子（GELU/LN/Softmax）与双脉冲流矩阵乘设计按前 $t$ 步累积均值计算期望增量的补偿模块（ECM），（论文自称）首次在 $T=4$ 下免训练转换十亿参数级视觉大模型 EVA。
- **链接：** https://arxiv.org/abs/2502.21193
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Towards High-performance Spiking Transformers from ANN to SNN Conversion
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打破了此前免训练 Transformer 转换（如 `STA`）动辄需要 $T=32\sim 256$ 步的延迟瓶颈，在不修改源 ViT / EVA 任何结构与权重的条件下把步数压到 $T=2\sim 8$。

**留下的局限**：ECM 模块本质是在每个时间步保留浮点状态并重算 $T\cdot F(S(T)/T)-(T-1)\cdot F(S(T-1)/(T-1))$（公式 15），属于数模/浮整混合执行而非纯脉冲神经元动力学；且未做激活中心化与差分增量稀疏化（该缺点随后在 `DCGS` 中改进），亦未探讨 `MaxPool` 或图邻域算子。

**是否需要训练或微调**：否（仅需少量校准样本前向统计阈值，零重训、零微调）

**涉及的算子**：$2n$ 级正负二次幂多阈值神经元（MT，$\pm 2^{p-1}\theta_{1,2}$）、非线性期望补偿模块（ECM，覆盖 LayerNorm / Softmax / GELU）、矩阵乘期望补偿模块（Matrix-Product-EC）

**关键数字**：`ImageNet-1K` 免训练转换结果（Section 4.2 Table 1，第 7 页）：`EVA`（源 **89.62%**）在 $T=2 / 4$ 达 **87.38% / 88.60%**（能耗比 ER=**0.19 / 0.35**）；`ViT-L/16`（源 **84.88%**）在 $T=4 / 8$ 达 **83.20% / 84.48%**（ER=**0.27 / 0.56**）；`ViT-B/16`（源 **80.77%**）在 $T=4 / 8$ 达 **76.27% / 79.40%**（ER=0.33 / 0.66）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（其“节点侧维护前缀均值重构 $S(t)/t$、算完非线性后再输出本步差分增量 $O(t)-O(t-1)$”的数学骨架，可直接迁移到视觉图的 `MRConv` 有符号相对 `max` 聚合中）

### <a id="41b0e334-2e6f-8105-91f7-f303160e35ff"></a>QCFS（2022）

- **发表处：** The Tenth International Conference on Learning Representations（ICLR 2022；预印本 `arXiv:2303.04347`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Tong Bu, Wei Fang, Jianhao Ding, PengLin Dai, Zhaofei Yu, Tiejun Huang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#qcfs2022
- **代码：** [https://github.com/putshua/SNN_conversion_QCFS](https://github.com/putshua/SNN_conversion_QCFS)
- **年份：** 2022
- **一句话：** 系统将转换误差拆分为“截断误差、量化（向下取整）误差、脉冲到达不均匀误差”三类，提出带 $1/2$ 平移项的量化剪裁取整激活函数（QCFS）替换源 ANN 的 ReLU 从头训练，（论文自称）首次将转换 SNN 的有效工作步数从数十步拉进 $T=4$。
- **链接：** https://arxiv.org/abs/2303.04347
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Optimal ANN-SNN Conversion for High-Accuracy and Ultra-Low-Latency Spiking Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：严格证明当源网络采用步数为 $L$、平移 $\varphi=1/2$ 的 QCFS 激活且转换后初始膜电位设为 $\theta^l/2$ 时，对**任意**目标时间步 $T$（无需 $T=L$）转换误差的数学期望恒为零（Theorem 2，公式 16）。

**留下的局限**：（1）**必须修改并从头训练源 ANN 300 轮**——Appendix A.1 与 Algorithm 1（第 14、20 页）明确要求训练前先把所有 `MaxPooling` 替换为 `AvgPooling`、把 `ReLU` 替换为 `QCFS`；（2）在 `ImageNet` 大模型上单靠 QCFS 在 $T=4\sim 8$ 仍因不均匀误差明显掉点（`ResNet-34` 在 $T=16$ 仅 59.35%）。

**是否需要训练或微调**：是（需用 STE 直通估计器从头训练改用 `AvgPool + QCFS` 的源网络 300 轮）

**涉及的算子**：量化剪裁向下取整平移激活函数（QCFS，$\lambda^l\text{clip}(\frac{1}{L}\lfloor\frac{z^l L}{\lambda^l}+\frac{1}{2}\rfloor, 0, 1)$）、可学习阈值 $\lambda^l$、初始膜电位偏置 $v^l(0)=\theta^l/2$、软复位 IF 神经元、`AvgPool` 替代 `MaxPool`

**关键数字**：`CIFAR-10` 上（Section 6.2 Table 2，第 8 页），`VGG-16`（源 **95.52%**）在 $T=2 / 4 / 8$ 达 **91.18% / 93.96% / 94.95%**，`ResNet-18`（源 **96.04%**）在 $T=4 / 8$ 达 **90.43% / 94.82%**；`CIFAR-100` `VGG-16`（源 **76.28%**，Appendix Table S4，第 19 页）在 $T=4 / 8$ 达 **69.62% / 73.96%**；`ImageNet`（Table 3，第 9 页）`ResNet-34`（源 **74.32%**）在 $T=16 / 32 / 64$ 达 **59.35% / 69.37% / 72.35%**，`VGG-16`（源 **74.29%**）在 $T=16 / 32 / 64$ 达 **50.97% / 68.47% / 72.85%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（超低时间步转换理论的分水岭里程碑；其“初始膜电位预充 $\theta/2$ 消除向下取整半格系统偏置”的结论在免训练转换中也完全通用）

### <a id="41b0e334-2e6f-8144-9ff6-c194ab8d964a"></a>SNNC-AP / SNN Calibration（2021）

- **发表处：** Proceedings of the 38th International Conference on Machine Learning（ICML 2021，PMLR Vol. 139，pp. 6316–6325；预印本 `arXiv:2106.06984`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yuhang Li, Shikuang Deng, Xin Dong, Ruihao Gong, Shi Gu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#snnc-ap--snn-calibration2021
- **代码：** 未公开（论文摘要写将发布于 GitHub，正文未附具体 URL）
- **年份：** 2021
- **一句话：** 将训练后量化（PTQ）中的逐层校准范式引入 ANN→SNN 转换，用网格搜索最小均方误差（MMSE）定阈值，并提供仅调偏置的轻量流水线（Light Pipeline）与联合调初始膜电位及权重的进阶流水线（Advanced Pipeline），（论文自称）首次成功转换带 BN 的 `MobileNet` 与 `RegNetX-4GF`。
- **链接：** https://arxiv.org/abs/2106.06984
- **核对人与日期：** Gemini，2026-11-16
- **标题：** A Free Lunch From ANN: Towards Efficient, Accurate Spiking Neural Networks Calibration
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：攻克了早期转换方法面对带 `BatchNorm` 轻量化深度可分离卷积网络（如 MobileNet）在 $T\le 256$ 时精度近乎归零（0.11%）的崩溃问题，只需 128–1024 张无标签校准图即可恢复精度。

**留下的局限**：（1）**遇到 **`**MaxPool**`** 仍需改源网**——Appendix C.1（第 11 页）明确写明实验测试的 VGG/ResNet 均预先将 `MaxPool` 替换为 `AvgPool`（再转成固定权重深度可分离卷积）；（2）对不同目标时间步 $T$ 需分别校准并存储独立参数；（3）在 $T<16$ 下尚未可用（实验最低从 $T=32$ 起测）。

**是否需要训练或微调**：部分（若源模型本身仅含 `AvgPool`/步幅卷积如开源 `MobileNet`，则 Light Pipeline 完全免梯度训练，Advanced Pipeline 仅用 1024 张图逐层 SGD 校准权重数分钟；但含 `MaxPool` 的源网仍被预先改成 `AvgPool` 训练）

**涉及的算子**：逐通道 MMSE 网格搜索阈值、轻量偏置校准（BC，$b_c\leftarrow b_c+\mu_c(e)$）、初始膜电位校准（PC，$v(0)\leftarrow T\cdot e$）、基于 STE 的逐层权重校准（WC）、BatchNorm 折叠、`AvgPool` 转深度可分离卷积

**关键数字**：`ImageNet` 上（Section 5.3 Table 4，第 7 页），`ResNet-34`（带 BN，源 **75.66%**）在 $T=32 / 64$ 下 Light Pipeline 达 **50.21% / 63.66%**，Advanced Pipeline 达 **64.54% / 71.12%**（对比未校准基线在 $T=32$ 仅 **0.09%**）；`MobileNet`（源 **73.40%**）在 $T=64 / 128 / 256$ 下 Advanced Pipeline 达 **56.26% / 65.40% / 69.02%**（基线在 $T=256$ 仅 **0.964%**，提升超 68 个百分点）；`RegNetX-4GF`（源 **80.02%**）在 $T=32 / 64 / 128$ 达 **55.70% / 70.96% / 75.78%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（确立了“用百余张无标签样本逐层对齐 ANN 激活与 SNN 平均脉冲输出”的训练后校准范式，可直接作为视觉图转换的基础校准层）

### <a id="41b0e334-2e6f-8149-8d48-f9ad639042f8"></a>Spiking-YOLO（2020）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2020，Vol. 34, No. 07，pp. 11270–11277，DOI: `10.1609/aaai.v34i07.6787`；预印本 `arXiv:1903.06530`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Seijoon Kim, Seongsik Park, Byunggook Na, Sungroh Yoon
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spiking-yolo2020
- **代码：** 未公开
- **年份：** 2020
- **一句话：** （论文自称）首个将深层目标检测器免重训转换为 SNN 的里程碑工作，提出逐通道权重归一化（Channel-Norm）消除通道尺度悬殊导致的欠发放，并用带正负非对称阈值的双极脉冲神经元（IBT）精确转换 `LeakyReLU` 的负半轴斜率。
- **链接：** https://arxiv.org/abs/1903.06530
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking-YOLO: Spiking Neural Network for Energy-Efficient Object Detection
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：攻克了坐标边界框连续回归对细粒度数值极其敏感、传统整层归一化（Layer-Norm）压死小幅值特征通道，以及单极性 IF 无法表达 `LeakyReLU` 负斜率（如 $-0.1x$）的两大障碍。

**留下的局限**：为逼近连续检测框回归所需的精细分辨率，推理需要高达 $T=3500\sim 8000$** 个时间步**，无法用于实时低延迟场景；且源模型 `Tiny YOLO` 中的步幅为 1 最大池化仍被替换为近似层处理。

**是否需要训练或微调**：否（直接对预训练 `Tiny YOLO` 执行逐通道最大激活归一化与双阈值映射，无需重训）

**涉及的算子**：逐通道激活归一化（Channel-Norm）、非对称正负双阈值带符号神经元（Imbalanced-Threshold / `IBT`，$V_{th}^+ = 1, V_{th}^- = -1/\alpha$ 映射 `LeakyReLU`）、软复位 IF 神经元

**关键数字**：在 `PASCAL VOC` 上转换 `Tiny YOLO`（源 **53.01% mAP**，Section 4 Table 1 & Table 2，第 6–7 页），传统整层归一化 + 标准 IF 仅得 **7.52% mAP**，引入 `Channel-Norm + IBT` 后在 $T=8000$ 达 **51.83% mAP**（$T=3500$ 收敛至约 51.4%）；在 `MS COCO`（源 **26.24% mAP**）上达 **25.66% mAP**；基于 TrueNorth 芯片功耗建模估算较 V100 GPU 节能约 **280×**（Section 4，第 7 页）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（`Channel-Norm` 是此后几乎所有逐通道阈值校准的鼻祖；`IBT` 用非对称正负双阈值免训练表达 `LeakyReLU` / `GELU` 负半轴小斜率的做法可直接用于采用 `GELU` 或 `LeakyReLU` 的视觉图骨干如 ViG / DGCNN！）

### <a id="41b0e334-2e6f-815c-9d73-d7b48bccc386"></a>RMP-SNN（2020）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2020，pp. 13558–13567；预印本 `arXiv:2003.01811`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Bing Han, Gopalakrishnan Srinivasan, Kaushik Roy
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#rmp-snn2020
- **代码：** 未公开（论文第 6 页仅引用其派生自 Facebook `fb.resnet.torch` 基线仓库）
- **年份：** 2020
- **一句话：** 系统阐明硬复位（reset-to-zero）在发放瞬间抹掉超阈值电位的非线性台阶失真，结合软复位残余膜电位（RMP）神经元、无 BN/无偏置约束训练与阈值比例缩放（$\alpha \le 0.8$），在深层 VGG-16 与 ResNet-34 上实现近无损转换并提速 2–8 倍。
- **链接：** https://arxiv.org/abs/2003.01811
- **核对人与日期：** Gemini，2026-11-16
- **标题：** RMP-SNN: Residual Membrane Potential Neuron for Enabling Deeper High-Accuracy and Low-Latency Spiking Neural Network
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了 `Rueckauer 2017` 虽提出软复位但在带 BN/偏置的 ImageNet VGG-16 上仍掉点 14.28% 的遗留问题，确立了深层残差网络软复位转换的标准基线。

**留下的局限**：（1）**要求源网络训练时严禁使用偏置项和 **`**BatchNorm**`** 层**（Section 2，第 2 页），无法复用现成带 BN 的现代视觉预训练权重；（2）采用随机泊松率编码，在 ImageNet 上仍需 $T=512\sim 4096$ 个时间步。

**是否需要训练或微调**：部分（转换阶段本身只统计最大加权输入定阈值，但**源 ANN 必须在去掉全部 BN 层与偏置项、改用 Dropout 的严格约束下从头训练**）

**涉及的算子**：残余膜电位软复位神经元（RMP，$V_m(t)=V_m(t)-V_{th}$）、基于 SNN 脉冲统计的逐层最大输入阈值与比例缩放（$\alpha V_{\text{in}}^{\max}$）、泊松正负率编码、去 BN 无偏置 ReLU 卷积与残差块

**关键数字**：近无损高步精度（Section 5 Tables 1–3，第 7 页）：`CIFAR-10`（$T=2048$）`VGG-16` **93.63%**（源 93.63%，掉点 <0.01%）、`ResNet-20` **91.36%**（源 91.47%）；`CIFAR-100`（$T=2048$）`VGG-16` **70.93%**（源 71.22%）、`ResNet-20` **67.82%**（源 68.72%）；`ImageNet`（$T=4096$）`VGG-16` **73.09%**（源 73.49%，掉 0.4%）、`ResNet-34` **69.89%**（源 70.64%，掉 0.75%）；缩放阈值快速模式下 `ImageNet` `VGG-16` 在 $T=512$ 达 **68.93%**（Section 5，第 7–8 页）。

> 💭
> **与本方向的关系（判断）**：背景（软复位残余膜电位机制的经典代表作，解释了为何现代所有转换法一律采用减法软复位而非归零硬复位）

### <a id="41b0e334-2e6f-815d-96d5-cd4423a54b93"></a>Spike-Norm（2019）

- **发表处：** Frontiers in Neuroscience（2019 年，Vol. 13，Article 95，DOI: `10.3389/fnins.2019.00095`；预印本 `arXiv:1802.02627`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Abhronil Sengupta, Yuting Ye, Robert Wang, Chiao Liu, Kaushik Roy
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spike-norm2019
- **代码：** 未公开
- **年份：** 2019
- **一句话：** 提出在实际脉冲网络前向传播中逐层记录真实脉冲累积输入最大值来设定阈值的 `Spike-Norm` 算法，并定制无 BN、无偏置、全平均池化的残差块，（论文自称）首次把 ANN→SNN 转换成功推上 `ImageNet` 全集的深层 `VGG-16` 与 `ResNet-34`。
- **链接：** https://arxiv.org/abs/1802.02627
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Going Deeper in Spiking Neural Networks: VGG and Residual Architectures
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：发现此前单纯基于 ANN 静态激活最大值定阈值会低估多步随机泊松脉冲叠加的瞬时峰值，通过“在环脉冲统计定阈值”把转换规模从 CIFAR 小网络扩展到深层 ImageNet 架构。

**留下的局限**：使用硬复位（hard-reset）IF 神经元且要求源网络去偏置、去 BN、把所有 `MaxPool` 换成 `AvgPool` 从头训练；在 `ImageNet` 上需要 $T=2500$** 步**，且 `ResNet-34` 仍掉点逾 5 个百分点。

**是否需要训练或微调**：部分（阈值标定无需梯度训练，但必须预先按无偏置、无 BN、`AvgPool` 约束重训源 VGG/ResNet）

**涉及的算子**：SNN 在环逐层最大突触输入阈值平衡（`Spike-Norm`）、硬复位 IF 神经元、泊松率编码、无 BN 定制残差连接与 `AvgPool`

**关键数字**：在 $T=2500$ 下（Section 4 Tables 1–3，第 11–14 页），`CIFAR-10` `VGG-16` 达 **91.55%**（源 91.70%）；`ImageNet` 全集上 `VGG-16` 达 **69.96%**（源 **70.52%**，仅掉 0.56%），`ResNet-34` 达 **65.47%**（源 **70.69%**，掉 5.22%）。

> 💭
> **与本方向的关系（判断）**：背景（深层视觉主干转换的早期里程碑，直观展示了硬复位与朴素率编码在深层残差结构上的延迟代价）

### <a id="41b0e334-2e6f-8165-9b92-e95317f25094"></a>Spiking MaxPooling 电路（2022）

- **发表处：** 2022 International Joint Conference on Neural Networks（IJCNN 2022，DOI: `10.1109/IJCNN55064.2022.9892074`；预印本 `arXiv:2205.07076`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Ramashish Gaurav, Bryan Tripp, Apurva Narayan
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spiking-maxpooling-电路2022
- **代码：** 未公开
- **年份：** 2022
- **一句话：** 面向 Intel Loihi 芯片设计并对比了两种完全由脉冲神经元构成的 `MaxPooling` 硬件近似电路：基于恒等式 $\max(a,b)=\frac{a+b}{2}+\frac{|a-b|}{2}$ 的绝对值群体电路 `AVAM` 与最大跳跃门控电路 `MJOP`。
- **链接：** https://arxiv.org/abs/2205.07076
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking Approximations of the MaxPooling Operation in Deep SNNs
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在不支持硬件浮点比较器、只有标准 LIF 神经元核的第一代神经形态芯片（Loihi 1）上给出了纯脉冲电路实现 `MaxPool` 的构造性方案。

**留下的局限**：代价高且延迟长——`MJOP` 精度损失高达十余个百分点；较准的 `AVAM` 需要成群辅助神经元两两配对构建二叉树（邻域 $k=20$ 时树深与辅助神经元激增），且论文第 7 页 Section IV-B 明确承认**必须依赖突触低通滤波平滑电流，完全不支持未滤波直接脉冲或超低时间步编码**（实测需 $T=50\sim 120$ 步）。

**是否需要训练或微调**：否（基于 NengoDL / NengoLoihi 转换预训练 CNN，将 `MaxPool` 替换为预构建脉冲微电路）

**涉及的算子**：两两配对绝对值拟合脉冲最大池化（`AVAM`）、最大跳变输出池化（`MJOP`）、指数突触电流滤波、LIF 神经元

**关键数字**：在 `CIFAR-10` 转换实验中（$T=50\sim 120$ 步，Section III Table I，第 6 页），源 CNN 精度为 **65.3%**，`AVAM` 转换精度为 **64.68%**（Loihi 仿真掉点 <1%），而 `MJOP` 大幅掉点至 **51.80%**；`MNIST` 上 `AVAM` 达 **98.55%**（源 98.71%）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（与 `LIPooling`、`Pre-Neuron MaxPool` 一起证明了“脉冲域做 `MaxPool` 绝非平凡无损”，在低时间步与大邻域 $k$ 下纯脉冲拟合电路并不划算）

### <a id="41b0e334-2e6f-817b-a806-f0c2e0b5306c"></a>RTS / Optimal Conversion（2021）

- **发表处：** The Ninth International Conference on Learning Representations（ICLR 2021；预印本 `arXiv:2103.00476`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Shikuang Deng, Shi Gu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#rts--optimal-conversion2021
- **代码：** [https://github.com/Jackn0/snn_optimal_conversion_pipeline](https://github.com/Jackn0/snn_optimal_conversion_pipeline)
- **年份：** 2021
- **一句话：** 通过二阶泰勒展开把全网转换损失分解为逐层激活均方误差之和，从理论上推导出在 SNN 每层偏置上加 $\frac{V_{th}}{2T}$ 最优平移项以抵消向下取整的系统性低估，并配合截断阈值 ReLU 将步数从上千步压至数十步。
- **链接：** https://arxiv.org/abs/2103.00476
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Optimal Conversion of Conventional Artificial Neural Networks to Spiking Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：（论文自称）首次严格指出 IF 软复位神经元的脉冲计数是输入电流的“向下取整（floor）”而非“四舍五入”，推导出 $\delta = \frac{V_{th}}{2T}$ 的半格偏置补偿公式与总误差 $\Delta\mathcal{L}_{\min}\approx \frac{L V_{th}^2}{4T}$（公式 15–16），把转换从经验调参推进到解析误差最小化。

**留下的局限**：未兼容 `BatchNorm` 与 `MaxPool`（论文第 9 页 Section 8 讨论明确将支持 BN 和正负双极激活列为未来工作，实验中全部去 BN 并使用 `AvgPool`，一旦直接套在带 BN 的 ImageNet ResNet-34 上在 $T=32$ 即崩至 0.09%）；且最优效果需用截断 `Threshold ReLU` 重训源 ANN。

**是否需要训练或微调**：部分（仅加偏置平移 `Work-S` 可免重训用于普通 ReLU 网络但需 $T\ge 256$；要在 $T=16\sim 32$ 收敛则须用 `Threshold ReLU` 重训源 ANN，且源网不含 BN 与 `MaxPool`）

**涉及的算子**：截断激活 `Threshold ReLU`（上限 $y_{th}$）、逐层偏置平移 $b_{\text{SNN}} = b_{\text{ANN}} + \frac{V_{th}}{2T}$、软复位 IF 神经元、`AvgPool`

**关键数字**：无 BN 架构下（Section 7.3 Table 1，第 8 页），`CIFAR-10` `VGG-16` 在 $T=16 / 32$ 达 **92.29% / 92.29%**（较 `RMP-SNN` 的 1536 步缩短近百倍），`ResNet-20` 在 $T=16 / 32$ 达 **92.41% / 93.30%**；`CIFAR-100` `VGG-16` 在 $T=16 / 32$ 达 **65.94% / 69.80%**；`ImageNet` `VGG-16` 在 $T=16 / 32 / 64$ 达 **55.80% / 67.73% / 70.97%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（半格偏置补偿 $\frac{V_{th}}{2T}$ 与二阶泰勒逐层误差分解是理解此后所有低步转换方法的理论基石）

### <a id="41b0e334-2e6f-81ee-8cf8-c39f24740761"></a>Burst + LIPooling（2022）

- **发表处：** Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence（IJCAI 2022，pp. 2485–2491；预印本 `arXiv:2204.13271`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yuhang Li, Yi Zeng
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#burst--lipooling2022
- **代码：** [https://github.com/BrainCog-X/Brain-Cog](https://github.com/BrainCog-X/Brain-Cog)
- **年份：** 2022
- **一句话：** 允许单个时间步内连续发放一簇最多 $\Gamma$ 个二值脉冲（Burst Spikes）以释放高激活截断误差，同时**从理论上证明朴素脉冲 **`**MaxPool**`** 输出必被高估至 ****$[\max, \text{sum}]$**** 之间，并设计侧抑制池化 **`**LIPooling**`** 精确收敛于真最大值**。
- **链接：** https://arxiv.org/abs/2204.13271
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Efficient and Accurate Conversion of Spiking Neural Network with Burst Spikes
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：（1）用仿生脉冲簇在 $T=32\sim 64$ 步免训练转换下压低截断误差；（2）论文第 4–5 页公式 (11)–(12) 给出了脉冲域逐时刻取 `max` 因胜者来回切换导致前期脉冲不可撤回、从而产生严重正向偏置的严格数学证明与互抑制消除机制。

**留下的局限**：`LIPooling` 的互抑制矩阵构造依赖非负脉冲计数（单极性率编码），且为了等各通道脉冲相位对齐仍需 $T=16\sim 32$ 步；在图网络中每个节点邻域大小 $k$ 可变且 `MRConv` 输入差值 $x_j-x_i$ 带负号，无法原样照搬。

**是否需要训练或微调**：否（直接转换带 BN 和原版 `MaxPool` 的预训练 CNN，无需重训或改为 `AvgPool`）

**涉及的算子**：脉冲簇神经元（Burst Spikes，单步最大发放数 $\Gamma=5$）、侧抑制最大池化神经元层（`LIPooling`）、BatchNorm 折叠

**关键数字**：在保留原版 `MaxPool` 的 `VGG-16` 上（Section 4.2 Table 1 & Table 2，第 5–6 页），`CIFAR-100`（$T=32$）单纯将 p-Norm 池化换成 `LIPooling` 即从 58.51% 跃升至 **65.63%**，再叠加 Burst（$\Gamma=5$）达 **71.41%**（$T=64$ 达 **74.98%**，源 ANN 76.31%）；`ImageNet` `VGG-16`（源 **74.49%**，Table 3，第 6 页）在 $T=32 / 64$ 达 **70.61% / 73.00%**，`ResNet-34`（源 **73.45%**）在 $T=32 / 64$ 达 **65.06% / 70.95%**。

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q10“取最大值对输入/脉冲误差敏感度”的核心文献：公式 (11) $\max(\mathbb{O})\le r_i^{(\ell)}\le\text{sum}(\mathbb{O})$ 精确刻画了脉冲流直接取 `max` 的单向高估定律）

### <a id="41b0e334-2e6f-814d-9c5c-d7dbcc3e1841"></a>Weight & Threshold Balancing（2015）

- **发表处：** 2015 International Joint Conference on Neural Networks（IJCNN 2015，pp. 1–8，DOI: `10.1109/IJCNN.2015.7280696`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Peter U. Diehl, Daniel Neil, Jonathan Binas, Matthew Cook, Shih-Chii Liu, Michael Pfeiffer
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#weight--threshold-balancing2015
- **代码：** [https://github.com/dannyneil/spiking_relu_conversion](https://github.com/dannyneil/spiking_relu_conversion)
- **年份：** 2015
- **一句话：** 提出“基于模型权重范数”和“基于训练数据最大激活值”的逐层权重/阈值平衡（Data-based Normalization）法则，消除了早期手工设阈值导致的深层过饱和与脉冲熄灭问题，把 MNIST 转换脉冲 CNN 推至 99.1% 以上高精度。
- **链接：** https://doi.org/10.1109/IJCNN.2015.7280696
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Fast-Classifying, High-Accuracy Spiking Deep Networks Through Weight and Threshold Balancing
- **核对深度：** 仅见引用
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：证明将每层权重按该层最大激活比例缩放 $\mathbf{W}^\ell \leftarrow \mathbf{W}^\ell \frac{\lambda^{\ell-1}}{\lambda^\ell}$ 可保证任意神经元期望发放率不超过上限 1，奠定了此后所有阈值/权重缩放转换法的数学原型。

**留下的局限**：强制要求源网络**无偏置项、无 BatchNorm、使用平均池化替代最大池化**，且对单个极端离群激活极其敏感（导致阈值偏大、需数百时间步），采用硬复位神经元无法扩展到深层复杂数据集。

**是否需要训练或微调**：部分（归一化本身在训练后执行，但源 CNN 须在无偏置、平均池化约束下训练）

**涉及的算子**：基于数据的逐层最大激活权重归一化（Data-based Normalization）与基于模型的权重行和归一化（Model-based Normalization）、硬复位 IF 神经元、无偏置 ReLU 卷积与平均池化

**关键数字**：据 `Rueckauer 2017`（Section 1 & Table 1）与开源仓库记录核实，在 `MNIST` 上转换无偏置 3 层卷积网取得 **99.14%** 精度（当时脉冲网络最高纪录，但在更深 CIFAR/ImageNet 网络上因无 BN 与硬复位受限）。

> 💭
> **与本方向的关系（判断）**：背景（确立“激活尺度归一化 $\Leftrightarrow$ 发放阈值平衡”等价性的奠基文献）

### <a id="41b0e334-2e6f-817b-b31f-c077803fd854"></a>Spiking Deep CNN 奠基（2015）

- **发表处：** International Journal of Computer Vision（IJCV 2015，Vol. 113, Issue 1，pp. 54–66，DOI: `10.1007/s11263-014-0788-3`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yongqiang Cao, Yang Chen, Deepak Khosla
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spiking-deep-cnn-奠基2015
- **代码：** 未公开
- **年份：** 2015
- **一句话：** 现代深度学习时代 ANN→SNN 转换路线的开创性工作——指出 ReLU 的非负分段线性响应与无漏电积分发放（IF）神经元的脉冲发放率天然同构，（论文自称）首次通过裁剪 CNN 结构（去偏置、平均池化）训练后直接把浮点权重复制给脉冲网络识别物体。
- **链接：** https://doi.org/10.1007/s11263-014-0788-3
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking Deep Convolutional Neural Networks for Energy-Efficient Object Recognition
- **核对深度：** 仅摘要
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：绕开了脉冲神经元不可微难以直接反向传播训练深层网络的死结，（论文自称）首次指明“先用成熟反向传播训练定制 ReLU CNN，再复制权重映射为事件驱动 SNN 上类脑芯片”的工程捷径。

**留下的局限**：缺少系统的层间权重/阈值归一化公式，必须手工定制无负输出、无偏置、无 `MaxPool` 的浅层 CNN，仅在 `CIFAR-10` 与 `Neovision2 Tower` 等中小规模目标识别上验证，且需要数百个时间步。

**是否需要训练或微调**：部分（转换只是直接复制权重，但必须先将源 CNN 裁剪为去偏置、非负平均池化的 SNN 兼容结构后训练）

**涉及的算子**：ReLU 到 IF 神经元发放率直接权重映射、零偏置卷积与全连接、空间平均池化替代最大池化

**关键数字**：据 Springer 官方摘要披露，在 `DARPA Neovision2 Tower` 与 `CIFAR-10` 数据集上取得与裁剪后源 CNN 相近的识别精度，且面向 DARPA SyNAPSE 类脑硬件的映射分析表明其能效比商用现成 FPGA 上的原 CNN 高出**两个数量级（约 100×）**（Abstract；具体逐表分类百分比因未获取付费正文记为未核实）。

> 💭
> **与本方向的关系（判断）**：背景（整条 ANN→SNN 转换研究脉络的起点）

### <a id="41b0e334-2e6f-8193-a5f6-f469a42d2475"></a>AMP2（2026）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2026，Vol. 40, Issue 3，DOI: `10.1609/aaai.v40i3.37187`；预印本 `arXiv:2502.12791`）
- **脉络：** 2 脉冲图网络
- **作者：** Jian Song, Xiangfei Yang, Shangke Lyu, Donglin Wang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#amp22026
- **代码：** [https://github.com/LockFaiz/AMP2](https://github.com/LockFaiz/AMP2)
- **年份：** 2026
- **一句话：** 提出单时间步（$T=1$）逐激活混合传播策略，在训练与推理中通过神经元子群耦合消除多时间步循环展开，并在 2D 图像与 **3D 点云脉冲版 PointNet++** 上验证了单步推理精度。
- **链接：** https://doi.org/10.1609/aaai.v40i3.37187
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Activation-wise Propagation: A One-Timestep Strategy for Spiking Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把直接训练脉冲网络在 3D 点云分层架构（PointNet++）上的推理时间步压缩到 $T=1$，大幅降低多步展开的显存与延迟成本。

**留下的局限**：完全依赖从头替代梯度训练（非 ANN→SNN 转换），无法直接复用已训练好的浮点 PointNet++ 权重。

**是否需要训练或微调**：是（从头直接训练）

**涉及的算子**：单时间步逐激活混合传播脉冲单元、PointNet++ 最远点采样（FPS）、球查询（Ball Query）局部邻域分组、逐点 MLP 与局部对称池化

**关键数字**：在 `Spiking PointNet++` 骨干、单时间步 $T=1$ 下，`ModelNet40` 总体精度（OA）达 **91.63%**、类别平均精度（mAcc）达 **89.02%**；真实扫描点云 `ScanObjectNN` 达 **78.81% OA / 76.23% mAcc**，显著超过同表引用的转换基线 `KPConv-SNN`（$T=40$ 时仅 70.50% / 43.90%）及多步直接训练基线（Section 4 Table 5）。

> 💭
> **与本方向的关系（判断）**：直接相关（提供了 `PointNet++` 在 $T=1$ 直接训练路线下的强脉冲基线，可与 Lan et al. ICCV 2023 的改池化转换版 `PointNet++` 形成鲜明对照）

### <a id="41b0e334-2e6f-8194-9629-ff404a6cb59a"></a>SpikeGraphormer（2026）

- **发表处：** Information Sciences（2026 年第 123828 号论文，DOI: `10.1016/j.ins.2026.123828`；预印本于 2024 年 3 月发布于 `arXiv:2403.15480`，常简称 `SpikeGT`）
- **脉络：** 2 脉冲图网络
- **作者：** Yundong Sun, Dongjie Zhu, Yansong Wang, Zhaoshuo Tian, Ning Cao, Gregory O'Hare
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spikegraphormer2026
- **代码：** [https://github.com/PHD-lanyu/SpikeGraphormer](https://github.com/PHD-lanyu/SpikeGraphormer)
- **年份：** 2026
- **一句话：** 将稀疏全精度 GCN 局部分支与去除 Softmax 的线性复杂度脉冲图注意力（SGA）全局分支并联，用于大规模图节点分类及基于 $k$-NN 构图的图像与文本分类。
- **链接：** https://doi.org/10.1016/j.ins.2026.123828
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SpikeGraphormer: A High-Performance Graph Transformer with Spiking Graph Attention
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：用二值脉冲 $Q, K, V$ 的按列掩码与稀疏加法替代 $O(N^2)$ 点积 Softmax 注意力，把全局节点交互复杂度降为 $O(ND)$，显著降低显存开销（较标准自注意力省 10–20 倍）。

**留下的局限**：需要从头端到端训练；并联的局部图分支仍是常规浮点稀疏 GCN（公式 6），并非纯事件驱动网络；在图像任务上只是对 CNN 提取好的样本级特征建样本间 $k$-NN 图，而非图像块级视觉图骨干转换。

**是否需要训练或微调**：是（从头端到端梯度训练）

**涉及的算子**：LIF 脉冲神经元、无 Softmax 的脉冲图注意力（SGA，$Q^i((K^i)^\top \odot V^i)$）、稀疏浮点 GCN 聚合、样本特征 $k$-NN 建图（$k \in \{5,10,15,20\}$）

**关键数字**：`Cora` **84.8±0.7%**、`Chameleon` **44.8±4.2%**、`Squirrel` **42.6±2.4%**（Section 5.2 Table 2）；大规模图 `OGB-Proteins` ROC-AUC **79.62±0.90%**（显存 3.7 GB，Table 3），`Amazon2M` **88.12±0.06%**（显存 4.8 GB，Table 4）；在 `Mini-ImageNet` 图像样本 $k$-NN 图分类上达 **86.90±0.39%**（$k=15$，无图退化版亦达 86.84%，Section 5.5 Table 6）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（SGA 去掉 Softmax 的线性脉冲图注意力设计，以及在 `Mini-ImageNet` 上建 $k$-NN 图但发现模型几乎不依赖显式图边的现象值得对照）

### <a id="41b0e334-2e6f-819a-b80a-fd3295903996"></a>DeNA-SGN（2026）

- **发表处：** arXiv（2026 年 11 月预印本，`arXiv:2611.14775`）
- **脉络：** 2 脉冲图网络
- **作者：** Sanjay Das, Xi Zhang, Emily Herron, Prasanna Date
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#dena-sgn2026
- **代码：** 未公开
- **年份：** 2026
- **一句话：** 先在二值化节点特征上用布尔“或（OR）”与“多数表决（Majority）”确定性邻域聚合配合直通估计器（STE）训练硬阈值分类器，再零决策失配地编译为 7 个时间拍的 SuperNeuroMAT 脉冲神经形态电路。
- **链接：** https://arxiv.org/abs/2611.14775
- **核对人与日期：** Gemini，2026-11-16
- **标题：** DeNA-SGN: Deterministic Neighborhood Aggregation for Verified Spiking Graph Inference
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：消除了脉冲图推理中的随机采样编码噪声与软硬模型转换失配，并用共享抑制控制神经元精确实现与节点度数相关的多数表决聚合。

**留下的局限**：并非对现成浮点 ReLU/GELU 视觉图骨干做免训练转换——节点特征必须预先二值化，且分类器在训练期就使用硬阈值；同时在 `ogbn-arxiv` 上揭示出若硬件为空闲脉冲神经元持续供能，脉冲电路总能耗反而高于浮点基线。

**是否需要训练或微调**：是（需用直通估计器 STE 从头训练带符号权重的硬阈值分类器，随后确定性编译为脉冲电路）

**涉及的算子**：离线特征二值化投影、无参数闭邻域 1 跳 OR 聚合（$c_{if}\ge 1$）、由至多 $\lfloor\log_2 \Delta\rfloor$ 个共享二进制抑制控制神经元（权重 $-2^b$）实现的度数自适应 tie-inclusive Majority 聚合（$c_{if}\ge \lceil k_i/2\rceil$）、无偏置硬阈值阶跃激活与验证集输出阈值校准

**关键数字**：在 7 个图数据集共 41 个映射分类器、累计 **296,577** 次原生测试查询上，SuperNeuroMAT 脉冲仿真（7 ticks，第 4 tick 输出）与导出硬阈值 ANN 实现 **0 决策与脉冲模式失配**（Abstract 及 Section VI-A Table VI，第 8 页）；`Amazon Photo` 达 **83.93±0.93%**（电流读出）/ **71.61±2.22%**（严格单脉冲读出），`Wiki-CS` 达 **75.99±0.54%**（电流）/ **67.36±1.66%**（严格脉冲），`Cora` 达 **74.90±2.67%**（电流）/ **68.57±2.94%**（严格脉冲，同划分 GAT 参考为 `81.47±0.90%`，Section VI-A/C Table V & VIII，第 8–9 页）；按解析能耗模型 $E_{\text{ANN}}=4.6M+0.9G$ 对照 $E_{\text{SNN}}=0.9\varepsilon+0.1s+0.7N_{\text{dep}}$（Section IV-J 公式 14），`Cora` 与 `CiteSeer` 的建模 ANN/SNN 能耗比为 **102.35×** 与 **171.03×**，`Amazon Photo` 与 `Wiki-CS` 为 **5.41×** 与 **4.24×**，但在 `ogbn-arxiv`（电流 **58.36±0.69%** / 严格脉冲 **46.20±0.99%**，部署神经元 `339,135` 个）上因空闲神经元每拍时钟更新开销主导，能耗比跌至 **0.53×**（ANN `136.9 nJ` vs SNN `257.71 nJ`，即 SNN 反而更耗电，Section VI-E Table X，第 10–11 页）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（其度数自适应抑制阈值构造以及“空闲神经元时钟功耗会吞噬脉冲收益”的定量反例对 M4 能耗盈亏分析极具参考价值）

### <a id="41b0e334-2e6f-81a3-b2f0-dca38f8f241d"></a>SNN Toolbox（2017）

- **发表处：** Frontiers in Neuroscience（2017 年，Vol. 11，Article 682，DOI: `10.3389/fnins.2017.00682`；早期理论与工具版见 NIPS 2016 Workshop 预印本 `arXiv:1612.04052`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Bodo Rueckauer, Iulia-Alexandra Lungu, Yuhuang Hu, Michael Pfeiffer, Shih-Chii Liu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#snn-toolbox2017
- **代码：** [https://github.com/NeuromorphicProcessorProject/snn_toolbox](https://github.com/NeuromorphicProcessorProject/snn_toolbox)
- **年份：** 2017
- **一句话：** 现代无约束 CNN 转换的奠基之作——一次性提出了**减法软复位（reset-by-subtraction）、BatchNorm 参数折叠、99.9% 分位数鲁棒归一化、直接恒定电流首层输入、脉冲滑动滤波门控 **`**MaxPool**`** 以及脉冲对数比近似 **`**Softmax**`，让任意带偏置与 BN 的现成 CNN（含 Inception-V3）可直接免重训转换。
- **链接：** https://doi.org/10.3389/fnins.2017.00682
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Conversion of Continuous-Valued Deep Networks to Efficient Event-Driven Networks for Image Classification
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：彻底解除了 `Cao 2015` 与 `Diehl 2015`“源网络不准加偏置、不准用 BN、不准用 MaxPool”的三大紧箍咒，（论文自称）首次给出转换误差随层传播的理论推导与开源通用转换工具箱。

**留下的局限**：受限于单步二值脉冲率编码与 `MaxPool` 门控所需的指数滑动滤波稳定时间，推理需要 $T=300\sim 550$** 个时间步**；且在更深的 `ImageNet` `VGG-16` 子集上仍出现 **14.28%** 的较大精度损失（Table 2，第 8 页）。

**是否需要训练或微调**：否（直接转换带 BN、偏置、`MaxPool` 和 `Softmax` 的标准预训练网络）

**涉及的算子**：减法软复位 IF 神经元、BatchNorm 权重偏置折叠、99.9% 激活分位数鲁棒权重归一化（Robust Normalization）、基于 FIR/指数移动平均发放率估计门控的脉冲 `MaxPool`（Section 2.2.6，第 6 页）、深度可分离卷积与 `Inception-V3` 分支拼接、脉冲 `Softmax`

**关键数字**：`CIFAR-10` 上（Section 3.1 Table 1，第 8 页）带 BN 与脉冲 `MaxPool` 的 CNN 转换达 **90.85%**（源 **91.91%**，约 $T=400$ 步）；`ImageNet` 子集评测（Table 2，第 8 页）`Inception-V3`（1,382 张图，$T=550$）转换误差率 **25.04%**（即 Top-1 精度 **74.96%**，源精度 **76.12%**，仅掉 1.16%），但 `VGG-16`（2,570 张图，$T=400$）精度从 **76.11%** 掉至 **61.83%**（掉 14.28%）。

> 💭
> **与本方向的关系（判断）**：直接相关（现代免训练 ANN→SNN 转换算子工具箱的总源头，其中的 BN 折叠、软复位与分位数定阈值至今仍是所有转换算法的标准前置步骤）

### <a id="41b0e334-2e6f-81d5-a3cc-c05895e3389c"></a>MK-SGN（2026）

- **发表处：** Neurocomputing（2026 年 1 月正式发表，DOI: `10.1016/j.neucom.2025.131796`；预印本于 2024 年 4 月发布于 `arXiv:2404.10210`）
- **脉络：** 2 脉冲图网络
- **作者：** Naichuan Zheng, Hailun Xia, Zeyu Liang, Yuchen Du
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#mk-sgn2026
- **代码：** [https://github.com/zhengnaichuan2022/MK-SGN](https://github.com/zhengnaichuan2022/MK-SGN)
- **年份：** 2026
- **一句话：** （论文自称）首个面向人体骨架动作识别的脉冲图卷积网络，融合关节/骨骼/关节运动/骨骼运动四模态脉冲编码、空间—时间脉冲图自注意力，并用预训练 4 流 CTR-GCN 教师对 6 层脉冲学生网络实施软标签与中间层特征知识蒸馏。
- **链接：** https://doi.org/10.1016/j.neucom.2025.131796
- **核对人与日期：** Gemini，2026-11-16
- **标题：** MK-SGN: A Spiking Graph Convolutional Network with Multimodal Fusion and Knowledge Distillation for Skeleton-based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了二值脉冲在三维骨架序列上的表征退化，通过跨架构知识蒸馏将 10 层浮点 CTR-GCN 的高阶时空语义迁移到轻量级 6 层脉冲图卷积网络中。

**留下的局限**：属于**从头直接训练 + 跨架构知识蒸馏**（需训练 60 轮），完全不是免训练权重转换；且与教师 CTR-GCN 相比在 `NTU-RGB+D 120` 等大类别集上仍有逾 20 个百分点的精度差距。

**是否需要训练或微调**：是（使用 SGD 与 SpikingJelly 替代梯度从头训练 60 轮，并依赖预训练好的 4 流 CTR-GCN 教师模型提供蒸馏监督）

**涉及的算子**：脉冲多模态融合（SMF，Conv2D+BN+LIF）、脉冲自适应图卷积（SA-GC，固定骨架邻接 + 可学习邻接矩阵）、脉冲时空图自注意力（STGA，无 Softmax 脉冲矩阵乘）、特征变换模块（FTM）与余弦相似度内层特征蒸馏（IFD）

**关键数字**：脉冲步 $S=4$ 下，`NTU-RGB+D`（60 类）XSub / XView 精度达 **78.5% / 85.6%**，单样本理论能耗仅 **0.596 mJ**（较教师 CTR-GCN 的 36.25 mJ 降低 **98.36%**，Section 4.2 Table 6）；`NTU-RGB+D 120` XSub / XSet 为 **67.8% / 69.5%**，`NW-UCLA` 为 **92.3%**；知识蒸馏消融（Section 4.2.2 Table 6 & Table 9）显示，加入软标签蒸馏（SKD）与内层特征蒸馏（IFD，对齐教师第 5、8 层与学生第 3、5 层）使 6 层多模态模型在 NTU-60 XSub/XView 上从 **76.1% / 82.6%** 提升至 **78.5% / 85.6%**（+2.4 / +3.0 个百分点）。

> 💭
> **与本方向的关系（判断）**：直接相关（视觉骨架图上的代表性脉冲工作；回答定向问题 Q2 与 Q8 的核心证据：并非转换，但明确使用了 CTR-GCN→SGN 知识蒸馏）

### <a id="41b0e334-2e6f-81e4-b7bd-f88852236884"></a>GT-SNT（2026）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2026；预印本 `arXiv:2504.11840`）
- **脉络：** 2 脉冲图网络
- **作者：** Huizhe Zhang, Jintang Li, Yuchang Zhu, Huazhen Zhong, Liang Chen
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#gt-snt2026
- **代码：** [https://github.com/Zhhuizhe/GT-SNT](https://github.com/Zhhuizhe/GT-SNT)
- **年份：** 2026
- **一句话：** 不把脉冲神经元当作省电激活替代品，而是用作“序列到离散词元”的无码本节点分词器（SNT），将多跳随机特征传播序列压缩为脉冲计数码本，从而驱动线性时间复杂度的图 Transformer。
- **链接：** https://arxiv.org/abs/2504.11840
- **核对人与日期：** Gemini，2026-11-16
- **标题：** GT-SNT: A Linear-Time Transformer for Large-Scale Graphs via Spiking Node Tokenization
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了传统矢量量化（VQ）图模型中的“码本坍缩（codebook collapse）”与最近邻查表开销，实现 100% 有效码字利用率与 $O(NBd_v)$（$B \ll N$）线性全局注意力。

**留下的局限**：仅脉冲分词支路采用脉冲神经元，主干辅助 MPNN 与 `softmax` 注意力仍包含浮点线性层与指数运算；且必须从头训练。

**是否需要训练或微调**：是（采用替代梯度从头端到端训练）

**涉及的算子**：$T$ 步图传播算子、IF/LIF/PLIF 脉冲计数累加（$\hat{\mathbf{S}} = \sum_{t=0}^T \mathbf{S}^t$）、动态去重码本重构、节点—码字 Softmax 注意力（CGSA）、单层无归一化 GCN

**关键数字**：9 个数据集上平均超越已有脉冲图基线 **3.9%**（Section 5.1）：`Cora` **84.7±0.8%**、`CiteSeer` **74.0±0.5%**、`PubMed` **80.6±0.4%**、异配图 `Actor` **39.1±0.2%**、`ogbn-arxiv` **72.4±0.3%**、`ogbn-products` **74.8±0.4%**（Table 2）；在 `Coauthor-Physics` 上推理延迟仅 **0.02 s**（比图 Transformer 平均速度快 **130×**，理论能耗 **0.37 J**，Table 3）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（利用多步脉冲计数构造局部拓扑感知离散桶的思想，对视觉图动态选邻居的粗粒度分桶有启发）

### <a id="41b0e334-2e6f-8128-a8de-c0fa53d7ab03"></a>SpikingGCN（2022）

- **发表处：** Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence（IJCAI 2022，pp. 2434–2440；预印本 `arXiv:2205.02767`）
- **脉络：** 2 脉冲图网络
- **作者：** Zulun Zhu, Jiaying Peng, Jintang Li, Liang Chen, Qiang Yu, Siqiang Luo
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spikinggcn2022
- **代码：** [https://github.com/ZulunZhu/SpikingGCN](https://github.com/ZulunZhu/SpikingGCN)
- **年份：** 2022
- **一句话：** 将归一化图卷积预传播（$S=\tilde{A}^K X$）与伯努利脉冲编码、全连接线性层及 LIF 神经元结合进行端到端直接训练，**明确否定自动转换路线，并在 MNIST 网格图与 75 节点超像素图分类上验证了视觉图像图扩展性**。
- **链接：** https://arxiv.org/abs/2205.02767
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking Graph Convolutional Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：给出了（论文自称）首个端到端简明脉冲图卷积范式，避免在每一层重复做稠密图矩阵乘，并（论文自称）首次把脉冲图卷积拓展到超像素图像图分类（B 样条几何核）。

**留下的局限**：① 引言与附录 A 以“预训练 ANN 的多种算子与 SNN 不兼容（引 Rueckauer et al., 2017）”为由直接放弃转换路线，每次换任务都需从头训练；② 在普通引文图上把图传播退化为输入前的无参预处理 $S=\tilde{A}^K X$，脉冲层本身只是单层线性分类器；③ 在规模稍大的 `ogbn-arxiv` 上精度跌至 55.8%（见 `SpikeGCL` Table 1）。

**是否需要训练或微调**：是（使用替代梯度从头直接训练）

**涉及的算子**：无参归一化邻接矩阵幂预聚合 $S=\tilde{A}^K X$、伯努利率编码器、全连接线性层、LIF 神经元；在图像超像素图任务上额外包含**可训练 B 样条图卷积核（SplineCNN 式伪坐标核）与 IF 脉冲编码器**

**关键数字**：`Cora` / `CiteSeer` / `PubMed` 节点分类精度达 **80.9±0.6% / 72.5±0.7% / 77.6±0.6%**，理论能耗极低（Section 3.2 Table 2 & Table 3）；**视觉图像图实验（Section 3.3 Table 4 & Table 5 及 Appendix C.4，直接反驳 Claude 草稿“视觉图只有骨架有人做”的说法）**：① `MNIST` 28×28 像素网格图（784 节点，4 层深度）达 **99.35%**（Table 4）；② `**MNIST**`** 75 超像素图分类**（沿用 MoNet / SplineCNN 超像素图设置，$T=20$，10 次运行均值）取得 **94.50%** 准确率，逼近全精度 `SplineCNN` 的 95.22% 并超越 `MoNet` 的 91.11%（Table 5）！

> 💭
> **与本方向的关系（判断）**：**直接相关（一方面它是本项目现有 M0 超像素图任务在“直接训练阵营”里的直接前辈——早在 2022 年就跑了 MNIST 75 超像素图；另一方面它在附录 A 断言“自动转换算子不兼容、精度比不上直接训练”，正好构成本项目免训练低步保真转换要正面回应的靶子）**

### <a id="41b0e334-2e6f-8160-8d57-c71ce84f4816"></a>TactileSGNet（2020）

- **发表处：** IEEE/RSJ International Conference on Intelligent Robots and Systems（IROS 2020，pp. 9908–9914，DOI: `10.1109/IROS45743.2020.9341421`；预印本 `arXiv:2008.08046`）
- **脉络：** 2 脉冲图网络
- **作者：** Fuqiang Gu, Weicong Sng, Tasbolat Taunyazov, Harold Soh
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#tactilesgnet2020
- **代码：** [https://github.com/clear-nus/TactileSGNet](https://github.com/clear-nus/TactileSGNet)
- **年份：** 2020
- **一句话：** 最早将脉冲神经网络与图卷积结合处理异步传感器事件流的工作之一——把机器手指尖 NeuTouch 事件触觉传感器的 39 个不规则触觉单元建成空间图（手工图、$k$-NN 图或最小生成树图），用拓扑自适应图卷积（TAGConv）+ LIF 神经元直接识别抓取物体。
- **链接：** https://doi.org/10.1109/IROS45743.2020.9341421
- **核对人与日期：** Gemini，2026-11-16
- **标题：** TactileSGNet: A Spiking Graph Neural Network for Event-based Tactile Object Recognition
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：无需把非欧排布的异步触觉脉冲强行插值填零成二维像素网格，直接利用传感器几何邻接消费原生事件流。

**留下的局限**：从头使用矩形窗替代梯度训练 100 轮，且需要将 5–6.5 秒触觉序列按 0.02 s 分箱为多达 $T=250\sim 325$ 个时间步（对比后来 `PMSM` 用转换法在同数据集实现 $T=1$ 达 90.97%）。

**是否需要训练或微调**：是（使用 Adam + 矩形替代梯度 + MSE 投票损失从头训练 100 轮）

**涉及的算子**：传感器三维物理坐标手工连边 / $k$-NN（$k=1\sim 8$）/ 最小生成树（MST+$\sigma_d$）静态建图、多跳多项式拓扑自适应图卷积（TAGConv，$\sum_{k=0}^K g_k \mathbf{A}^k$）、LIF 脉冲神经元、时间均值投票解码

**关键数字**：在 36 类抓取物体数据集 `EvTouch-Objects` 与 20 类容器盛水量数据集 `EvTouch-Containers` 上（10 轮平均，Section IV-D Table II & Section IV-E Table III），手工连边图达 **89.44±0.55% / 64.17±2.75%**（超越网格脉冲 CNN 的 88.40% / 60.17% 与标准脉冲 GCN 的 85.14% / 58.83%）；改用自动 $k$-NN 建图后进一步提升至 **89.65±0.83%**（$k=7$，`EvTouch-Objects`）与 **67.00±1.39%**（$k=4$，`EvTouch-Containers`）。

> 💭
> **与本方向的关系（判断）**：背景（异步物理事件传感器 + 脉冲图网络的先驱工作，也是 2025 年 `PMSM` 做 GCN→SNN $T=1$ 转换实验所采用的标准基准来源）

### <a id="41b0e334-2e6f-8187-8ae9-df9c5d515aff"></a>SpikeNet（2023）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2023，Vol. 37, No. 7, pp. 8588–8596；预印本于 2022 年 8 月发布于 `arXiv:2208.10364`）
- **脉络：** 2 脉冲图网络
- **作者：** Jintang Li, Zulun Zhu, Zeang Liu, Ruofan Wu, Liang Chen, Zibin Zheng, Sheng-hua Zhong
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spikenet2023
- **代码：** [https://github.com/EdisonLeeeee/SpikeNet](https://github.com/EdisonLeeeee/SpikeNet)
- **年份：** 2023
- **一句话：** 用可学习阈值的 LIF 脉冲神经元取代传统时序图网络里的重量级 RNN（LSTM/GRU），结合时间邻域采样在百万节点级离散快照时序图上直接训练可扩展节点分类模型。
- **链接：** https://arxiv.org/abs/2208.10364
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Scaling Up Dynamic Graph Representation Learning via Spiking Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把动态图时序状态记忆从浮点循环网络替换为稀疏二值脉冲动力学，（论文自称）首次让脉冲图网络扩展到 273 万节点、1,396 万边的 `Patent` 时序图。

**留下的局限**：从头使用动态替代梯度训练；在每个时间步的邻域采样与特征线性聚合阶段仍包含浮点线性投影与采样开销。

**是否需要训练或微调**：是（基于动态自适应替代梯度从头端到端训练）

**涉及的算子**：时序随机游走/邻域采样（Temporal neighbor sampling）、GraphSAGE 式特征拼接与均值/求和线性聚合、带自适应阈值更新的 LIF 脉冲神经元

**关键数字**：在 `DBLP` / `Tmall` / `Patent` 三个大规模时序图（80% 训练集，Section 5.2 Table 2）上，Macro-F1 分别达 **74.86% / 62.40% / 83.90%**（注：`Dy-SIGN` 引用复现值在 DBLP 上记为 74.64% Macro-F1 / 74.86% Micro-F1，原论文 `aaai23.tex` Table 2 报告 DBLP 80% 划分为 Macro-F1 **74.34%**、Micro-F1 **75.58%**，`Tmall` Macro-F1 **62.40%** / Micro-F1 **66.10%**，`Patent` Macro-F1 **83.90%** / Micro-F1 **83.88%**，以原论文表 2 为准），训练参数量与推理速度显著优于 EvolveGCN 与 TGAT。

> 💭
> **与本方向的关系（判断）**：背景（时序动态图直接训练奠基工作，其把外部流式时间步与内部脉冲膜电位时间步对齐的思路与 `Signal-SGN` 及 M3 流式推理同源）

### <a id="41b0e334-2e6f-818d-bcaa-d3c3fe95bc01"></a>GC-SNN 与 GA-SNN（2021）

- **发表处：** Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence（IJCAI 2021，pp. 3171–3177；预印本 `arXiv:2107.06865`）
- **脉络：** 2 脉冲图网络
- **作者：** Mingkun Xu, Yujie Wu, Lei Deng, Faqiang Liu, Guoqi Li, Jing Pei
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#gc-snn-与-ga-snn2021
- **代码：** 未公开
- **年份：** 2021
- **一句话：** 静态引文图上最早一批直接训练脉冲图网络的工作，构建脉冲图卷积（GC-SNN）与脉冲图注意力（GA-SNN），并提出按节点邻域空间维度与时间步同步归一化的时空特征归一化（STFN）。
- **链接：** https://arxiv.org/abs/2107.06865
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Exploiting Spiking Dynamics with Spatial-temporal Feature Normalization in Graph Learning
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了深层/多步脉冲图传递中的发放率失衡与梯度难以收敛问题，把基于 BPTT 的直接训练引入 GCN 与 GAT。

**留下的局限**：从头 BPTT 训练开销大（无法扩展到 `ogbn-arxiv` 等大图，在 `SpikeGCL` 表 1 中因显存溢出 OOM 缺失）；且 `GA-SNN` 中的注意力系数 $\alpha_{ij}$ 仍由浮点 LeakyReLU + Softmax 算出后再乘二值脉冲（并非完全事件化的注意力）。

**是否需要训练或微调**：是（使用空间—时间反向传播 STBP 从头直接训练，$T=10\sim 20$）

**涉及的算子**：度归一化邻接聚合（GC-SNN）、浮点 Softmax 图注意力系数加权二值脉冲（GA-SNN）、时空特征归一化（STFN）、LIF 脉冲神经元

**关键数字**：在 `Cora` / `CiteSeer` / `PubMed` 标准划分下（$T=20$，Section 4.2 Table 1），`GC-SNN` 分别达 **80.7±0.5% / 70.3±0.6% / 78.2±0.5%**，`GA-SNN` 分别达 **81.0±0.6% / 70.1±0.6% / 78.6±0.4%**；消融显示去掉 STFN 后 `Cora` 精度下降约 2–4 个百分点（Section 4.3）。

> 💭
> **与本方向的关系（判断）**：背景（通用图脉冲网络早期奠基工作；`GA-SNN` 中注意力权重仍用模拟浮点计算的遗留问题恰对应路线图中的 M2）

### <a id="41b0e334-2e6f-81c7-8a6c-fce0adbeb1d9"></a>DVHGNN（2025）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2025；预印本 `arXiv:2503.14867`）
- **脉络：** 3 视觉图骨干
- **作者：** Caoshuo Li, Tanzhe Li, Xiaobin Hu, Donghao Luo, Taisong Jin
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#dvhgnn2025
- **代码：** [https://github.com/lcs0215/DVHGNN](https://github.com/lcs0215/DVHGNN) （注：截至核查日仓库仅有 `Apache-2.0` 许可证与标题占位符 `Coming soon...`，模型源码与权重均未上传）
- **年份：** 2025
- **一句话：** 先按余弦相似度将图像特征粗聚为 4 个语义簇，再以多尺度空洞步幅从各簇中心采样构建动态空洞超图，并用 Sigmoid 门控超图卷积提升高阶多尺度视觉表征能力。
- **链接：** https://arxiv.org/abs/2503.14867
- **核对人与日期：** Gemini，2026-11-16
- **标题：** DVHGNN: Multi-Scale Dilated Vision HGNN for Efficient Vision Recognition
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了原版 `ViHGNN` 全局模糊 C 均值聚类在大特征图上计算重且超边感受野尺度单一的问题。

**留下的局限**：**作为本项目教师模型目前不可用**——官方代码与预训练权重均未发布；且其每层余弦相似度聚类、多尺度排序采样与 Sigmoid 门控均高度非脉冲友好。

**是否需要训练或微调**：是（从头在 ImageNet-1K 等数据集上端到端训练浮点骨干）

**涉及的算子**：余弦相似度动态分簇（$C=4$）、多尺度空洞超图构建（`DHGC`，$r=1,2,3$）、超边均值聚合、`Sigmoid` 门控逐元素乘法、深度可分离卷积、`BatchNorm`、`GELU`

**关键数字**：`ImageNet-1K` Top-1 分类精度（Table 1，第 6 页）：`DVHGNN-T/S/M/B` 分别达 **79.8% / 83.1% / 83.8% / 84.2%**；`MS COCO` 目标检测与实例分割（Table 2，第 7 页）：`DVHGNN-S` 配 RetinaNet 达 **43.3** AP，配 Mask R-CNN 达 **44.8** $\text{AP}^b$ / **40.2** $\text{AP}^m$；`ADE20K` 语义分割（Table 3，第 7 页）：`DVHGNN-S` 配 Semantic FPN 达 **43.8%** mIoU，配 UperNet 达 **46.8%** mIoU。

> 💭
> **与本方向的关系（判断）**：背景（代表 2D 视觉超图骨干的最新精度上限，但因无公开代码和预训练权重，不宜选作免训练转换实验教师）

### <a id="41b0e334-2e6f-81d8-b9ee-e155c807626e"></a>GreedyViG（2024）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2024，pp. 6118–6127；预印本 `arXiv:2405.06849`）
- **脉络：** 3 视觉图骨干
- **作者：** Mustafa Munir, William Avery, Md Mostafijur Rahman, Radu Marculescu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#greedyvig2024
- **代码：** [https://github.com/SLDGroup/GreedyViG](https://github.com/SLDGroup/GreedyViG) （预训练权重：[https://huggingface.co/SLDGroup/GreedyViG/tree/main](https://huggingface.co/SLDGroup/GreedyViG/tree/main) ）
- **年份：** 2024
- **一句话：** 把 `MobileViG` 的固定轴向图推进到全网四个阶段，用对角象限翻转快速估算特征距离均值与标准差，动态筛除距离大于 $\mu-\sigma$ 的轴向移位候选邻居后再做 `max` 相对差聚合。
- **链接：** https://arxiv.org/abs/2405.06849
- **核对人与日期：** Gemini，2026-11-16
- **标题：** GreedyViG: Dynamic Axial Graph Construction for Efficient Vision GNNs
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：消除了 `ViG` 全图 $O(N^2)$ 两两距离矩阵与 `topk` 排序瓶颈，同时避免 `MobileViG` 纯静态轴向连边把背景异类像素强行连入同一邻域。

**留下的局限**：（1）**核查发现两处关键冲突与合规风险**：一是论文 Section 3.1 声称用欧氏距离（$\ell_2$），但官方源码 `greedyvig.py` 第 122、130、141 行实际调用 `torch.norm(..., p=1)` 计算 $\ell_1$** 曼哈顿距离**；二是不同于 `MobileViG` 的 `Apache-2.0`，`GreedyViG` 仓库采用 **UT Austin Research License（UTRL）**，严禁再分发衍生代码且要求将衍生修改回交许可方；（2）每层动态阈值硬掩码 $\mathbb{I}(\text{dist}<\mu-\sigma)$ 对脉冲量化噪声存在跳变风险。

**是否需要训练或微调**：是（浮点教师使用 `RegNetY-16GF` 知识蒸馏训练 300 轮）

**涉及的算子**：动态轴向图构建（`DAGC`，步幅 $K=[8,4,2,1]$，`torch.roll` 移位 + 翻转距离均值/标准差二值掩码）、相对差最大值聚合 $\max(0, \text{mask}\cdot(X_{\text{rolled}}-X))$、条件位置编码 `CPE`（$7\times 7$ 深度卷积）、倒残差 `MBConv`、`BatchNorm2d`、`GELU`

**关键数字**：`ImageNet-1K` Top-1 精度（Table 1，第 6 页）：`GreedyViG-S`（12.0M 参数，1.6 GMACs）达 **81.1%**，`GreedyViG-M`（21.9M，3.2 GMACs）达 **82.9%**，`GreedyViG-B`（30.9M，5.2 GMACs）达 **83.9%**；`MS COCO` Mask R-CNN（Table 2，第 7 页）：`GreedyViG-S/B` 达 **43.2 / 46.3** $\text{AP}^{box}$、**39.8 / 42.1** $\text{AP}^{mask}$；`ADE20K` Semantic FPN 达 **43.2% / 47.4%** mIoU。

> 💭
> **与本方向的关系（判断）**：直接相关（非常适合作为“半动态轴向掩码图 vs 全动态 $k$-NN 图 vs 纯静态轴向图”转换误差对比的教师模型，但引用其代码时须遵守 UTRL 限制、切勿直接拷贝源码分发）

### <a id="41b0e334-2e6f-81da-8fd4-e977dc2fa215"></a>Spiking PointNet（2023）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2023，Vol. 36；预印本 `arXiv:2310.06232`）
- **脉络：** 2 脉冲图网络
- **作者：** Dayong Ren, Zhe Ma, Yuanpei Chen, Weihang Peng, Xiaode Liu, Yuhan Zhang, Yufei Guo
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spiking-pointnet2023
- **代码：** [https://github.com/DayongRen/Spiking-PointNet](https://github.com/DayongRen/Spiking-PointNet)
- **年份：** 2023
- **一句话：** （论文自称）首个面向三维点云分类的直接训练脉冲神经网络——将 PointNet 的 ReLU 替换为 LIF 脉冲神经元，提出“单时间步训练、多时间步推理（Trained-less but Learning-more）”范式与膜电位微扰增广（MPP）。
- **链接：** https://arxiv.org/abs/2310.06232
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking PointNet: Spiking Neural Networks for Point Clouds
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了点云脉冲网络在多时间步反向传播（BPTT）下的梯度消失/爆炸及高显存开销，仅需 $T=1$ 训练即可在 $T=4$ 推理时获得类似集成投票的精度提升。

**留下的局限**：**完全属于替代梯度从头直接训练（非 ANN→SNN 转换）**；骨干为无局部邻域图结构的逐点 MLP + 全局对称池化（PointNet），未涉及动态 $k$-NN 建图或局部图消息传递算子的免训练转换。

**是否需要训练或微调**：是（使用 `tanh` 型替代梯度 $k=5$ 在 $T=1$ 下从头直接训练，配合训练期初始膜电位随机扰动 MPP）

**涉及的算子**：逐点共享 MLP、T-Net 空间变换对齐、硬复位 LIF 脉冲神经元、训练期膜电位微扰（MPP，$\delta \in [0, 0.5]$）、全局对称最大池化、多时间步输出均值集成

**关键数字**：单步训练（$T_{\text{train}}=1$）配合膜电位微扰（MPP）后，在 `ModelNet10` 上 $T_{\text{test}}=1 / 4$ 精度达 **91.66% / 93.31%**（超越同结构浮点 PointNet 的 92.98%，Section 5.1 Table 4 / `tab:ab4` & Table 5 / `Comparison`）；在 `ModelNet40` 上 $T_{\text{test}}=1 / 2 / 4$ 精度达 **87.72% / 88.46% / 88.61%**（浮点 PointNet 为 89.20%，常规 $T=4$ BPTT 训练仅为 86.70%，Section 5.1 Table 5）；按 45nm Horowitz 模型（4.6 pJ MAC vs 0.9 pJ AC，平均发放率 18.7%）估算，`ModelNet10` 单次前向能耗在 $T=1$ 为 $9.2 \times 10^6$** pJ**（比 PointNet 省电 **15.2×**），$T=4$ 为 $3.7 \times 10^7$** pJ**（省电 **3.8×**，Section 5.2 Table 6）。

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q2 与核查 Claude 草稿二轮补充的核心文献：三维点云脉冲网络早期里程碑，但走的是从头直接训练路线且无图邻域拓扑）

### <a id="41b0e334-2e6f-81f6-ab43-c02a81f1e24c"></a>Lan 等 3D/2D 转换 SNN（2023）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2023，pp. 9211–9220，DOI: `10.1109/ICCV51070.2023.00845`）
- **脉络：** 2 脉冲图网络
- **作者：** Yuxiang Lan, Yachao Zhang, Xu Ma, Yanyun Qu, Yun Fu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#lan-等-3d2d-转换-snn2023
- **代码：** 未公开
- **年份：** 2023
- **一句话：** **（论文自称）首个系统性将 3D 点云网络（**`**PointNet**`** 与 **`**PointNet++**`**）通过 ANN→SNN 转换变为低延迟脉冲网络的工作**——先将源网络中的 `MaxPooling` 替换为 `AvgPooling` 训练源模型，再用 5–10 批样本做 KL 散度阈值校准、偏置修正，并在推理时引入动态指数衰减阈值与 2 比特自适应多脉冲发放。
- **链接：** https://doi.org/10.1109/ICCV51070.2023.00845
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Efficient Converted Spiking Neural Network for 3D and 2D Classification
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：将 3D 点云转换 SNN 的有效推理时间步从数十步压缩至 $T=4\sim 16$，在转换后 SNN 与“改用平均池化的源 ANN”之间实现了几乎零掉点（$<0.36\%$）。

**留下的局限**：**对本项目极富启发的致命局限**：作者在 **Section 4.1（第 9216 页左栏）** 明确承认*“In the ANN-SNN conversion method, using Maxpooling will not work.”*——为此**被迫修改源 **`**PointNet**`** / **`**PointNet++**`** 架构并重新训练源 ANN**，导致源 `PointNet++` 教师本身在真实扫描集 `ScanObjectNN` 上的精度从原版 `MaxPool` 的 ~77.9%–84.3% 暴跌至 **69.22%**！它回避而非解决了 `max` 聚合与现成预训练权重的免训练转换。

**是否需要训练或微调**：**部分**（转换阶段仅需 5–10 个 batch 训练数据做免训练校准；但**必须先把源 PointNet/PointNet++ 的 **`**MaxPooling**`** 全部改成 **`**AvgPooling**`** 并从头重训源 ANN**，不能直接转官方公开的 `MaxPool` 预训练权重！）

**涉及的算子**：`**MaxPooling**`** 强制替换为 **`**AvgPooling**`、BatchNorm 折叠（Eq. 4）、KL 散度 95 点网格搜索阈值初始化（Eq. 8）、输出均值误差偏置校准（Eq. 7）、按激活神经元比例调节的自适应动态阈值 $\tilde{V}_{th}^{(l)}(t) = (1 - \alpha e^{-(t-1)}\tau^{(l)}(t))V_{th}^{(l)}$（$\alpha=0.5$，Eq. 9–11）、2 比特自适应分级脉冲发放 $s^{(l)}(t)=\text{clip}(\lfloor \tilde{v}_{mem}(t)/\tilde{V}_{th}(t)\rfloor, 0, 2^n-1)$（$n=2$，最大脉冲值 3，软复位，Eq. 13–14）、PointNet++ 的 FPS 与多尺度球邻域分组

**关键数字**：全部出自 Section 4.2 **Table 1–3（pp. 9216–9217）**：① `ModelNet-10`（Table 1）：`PointNet`（AvgPool 源 ANN 92.81%）在 $T=4/8/16$ 达 **92.38% / 92.59% / 92.75%**；`PointNet++`（AvgPool 源 ANN 93.54%）在 $T=4/8/16$ 达 **93.18% / 93.54% / 93.54%**；② `ModelNet-40`（Table 2）：`PointNet`（源 ANN 88.17%）在 $T=4/8/16$ 达 **87.95% / 87.99% / 88.17%**；`PointNet++`（源 ANN 89.45%）在 $T=4/8/16$ 达 **89.37% / 89.43% / 89.45%**；③ `ScanObjectNN`（Table 3）：`PointNet`（源 ANN 66.56%）在 $T=4/8/16$ 达 **65.16% / 65.94% / 66.56%**；`PointNet++`（源 ANN 69.22%，常规转换 Baseline 在 $T=16$ 仅 58.02%）在 $T=4/8/16$ 达 **68.91% / 69.06% / 69.22%**。

> 💭
> **与本方向的关系（判断）**：**直接相关（Claude v1 完全漏掉的 3D 点云与 **`**PointNet++**`** 转换头号先例！其“因无法转换 MaxPool 而把 PointNet++ 改成 AvgPool 重训、致使教师在 ScanObjectNN 上狂掉约 9–15 个百分点”的事实，为本项目坚持“不改教师架构、免重训直接转换含 **`**max**`** 聚合的视觉图模型”提供了最强立项依据！）**

### <a id="41b0e334-2e6f-8112-9ffd-e23c92169d05"></a>SpikeGCL（2024）

- **发表处：** International Conference on Learning Representations（ICLR 2024；预印本于 2023 年 5 月发布于 `arXiv:2305.19306`）
- **脉络：** 2 脉冲图网络
- **作者：** Jintang Li, Huizhe Zhang, Ruofan Wu, Zulun Zhu, Baokun Wang, Changhua Meng, Zibin Zheng, Liang Chen
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spikegcl2024
- **代码：** [https://github.com/EdisonLeeeee/SpikeGCL](https://github.com/EdisonLeeeee/SpikeGCL)
- **年份：** 2024
- **一句话：** 将节点全维特征按通道均分为 $T$ 个子块依次送入脉冲图编码器，采用时间块间截断梯度（blockwise stop-gradient）局部对比损失学习紧凑的 1 比特节点表征，并在理论上证明了减法复位 IF 脉冲图网络对全精度 ReLU GCN 的率编码逼近误差界。
- **链接：** https://arxiv.org/abs/2305.19306
- **核对人与日期：** Gemini，2026-11-16
- **标题：** A Graph is Worth 1-bit Spikes: When Graph Contrastive Learning Meets Spiking Neural Networks（arXiv API 返回的标题；简称 SpikeGCL。本条早先标题字段有乱码，复查时已更正）
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：避免了对整张大图静态重复输入 $T$ 次的算力浪费，并通过分块局部对比训练消除了长序列替代梯度反向传播中的梯度消失。

**留下的局限**：本身属于自监督从头训练而非免训练转换；但**极具理论价值的是其附录 A 定理 1 证明了若用减法复位 IF 神经元按率编码逼近 **$L$** 层最大度为 **$D$** 的预训练 ReLU GCN，最坏误差上界随 **$(\nu\sqrt{1+D})^L / (T\sqrt{T})$** 指数放大**！

**是否需要训练或微调**：是（分块自监督图对比学习从头训练 + 线性分类头微调）

**涉及的算子**：节点特征通道分块（Feature partitioning）、随机边丢弃与特征置换图增强、GCN/SAGE 邻域聚合、IF/LIF 神经元、时间块间 `detach` 梯度隔离对比损失

**关键数字**：1 比特脉冲表征在 `Computers` / `Photo` / `CS` / `Physics` / `ogbn-arxiv` / `ogbn-MAG` 上分别达 **88.9±0.3% / 93.0±0.1% / 92.8±0.1% / 95.2±0.6% / 70.9±0.1% / 32.0±0.3%**，达到全精度图对比学习基线 95%–99% 的精度（Section 5 Table 1）；在百万级异构图 `ogbn-MAG` 上参数量仅 **6.6 KB**（约为全精度平均值的 **1/37**，原文正文泛称为 ~1/60），理论能耗 **0.18 mJ**（Table 2）；**理论逼近界（Appendix A Theorem 1 Eq. 6）**：$\sup_{v} \|\widehat{z}_v - z^*_v\|_2 \le \frac{\sqrt{d}\kappa(\sqrt{1+D}\nu)^L}{T\sqrt{T}}$。

> 💭
> **与本方向的关系（判断）**：可借用的技术（附录 A 定理 1 直接给出了固定图 ReLU GCN 做减法复位 IF 转换时的度数—层数误差放大上界，可直接引入本项目理论分析章节！）

### <a id="41b0e334-2e6f-811b-90c5-ea5d98e07372"></a>P2SResLNet（2024）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2024，Vol. 38, No. 6, pp. 6092–6099，DOI: `10.1609/aaai.v38i6.28425`）
- **脉络：** 2 脉冲图网络
- **作者：** Qiaoyun Wu, Quanxiao Zhang, Chunyu Tan, Yun Zhou, Changyin Sun
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#p2sreslnet2024
- **代码：** 未公开
- **年份：** 2024
- **一句话：** 结合核点卷积（KPConv）几何思想设计空间感知核点脉冲神经元与 3D 脉冲残差块，直接训练低时间步 3D 点云分类脉冲网络，并在文中构建了早期点云卷积 ANN→SNN 转换对照基线 `KPConv-SNN`。
- **链接：** https://doi.org/10.1609/aaai.v38i6.28425
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Point-to-Spike Residual Learning for Energy-Efficient 3D Point Cloud Classification
- **核对深度：** 仅摘要
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了常规脉冲神经元在三维核点卷积深层残差传递中的空间几何退化，实现了 $T=1$ 至 $T=4$ 下在真实扫描集 ScanObjectNN 上的有效收敛。

**留下的局限**：主模型采用从头直接训练且参数量偏大（14.3M）；而文中对比的常规转换基线 `**KPConv-SNN**`** 即便拉长到 **$T=40$** 时间步，在真实点云 ScanObjectNN 上精度仍崩溃至 43.9%**，直观暴露了未经专门校准的朴素转换在三维局部几何卷积上的严重失效。

**是否需要训练或微调**：是（主模型 `P2SResLNet` 从头直接训练；文中对照基线 `KPConv-SNN` 为转换基线）

**涉及的算子**：三维欧氏球邻域查询、空间感知核点卷积（KPConv）脉冲神经元、3D 脉冲残差连接

**关键数字**：据 `Spiking Point Mamba` Table 1、`Spiking Point Transformer` Table 2 与 `E-3DSNN` Table 1 一致引用，`P2SResLNet-B`（14.3M 参数）在 `ModelNet40` 上达 **88.7% OA**，在 `ScanObjectNN`（`PB-T50-RS`，$T=1$）上达 **74.5% OA**；而其报告的转换对照基线 `**KPConv-SNN**`**（**$T=40$**）** 在 `ModelNet40` 上仅为 **70.5% OA / 67.6% mAcc**，在 `ScanObjectNN` 上跌至 **43.9% OA / 38.7% mAcc**（亦见 `AMP2` Table 5 与 `Spiking PointCNN` Table 4；注：`Spiking Point Mamba` Table 1 第 23 行误将 `KPConv-SNN` 的 70.5 与 43.9 两列颠倒排印，对照 `SPT`/`AMP2`/`Spiking PointCNN` 三篇表格可确认 ModelNet40 为 70.5%、ScanObjectNN 为 43.9%）。

> 💭
> **与本方向的关系（判断）**：直接相关（提供了点云核点卷积朴素 ANN→SNN 转换在大时间步 $T=40$ 下仍然严重掉点的基准反例）

### <a id="41b0e334-2e6f-8143-942e-cb0fcbfc0b02"></a>SpikePoint（2024）

- **发表处：** International Conference on Learning Representations（ICLR 2024 Spotlight；预印本于 2023 年 10 月发布于 `arXiv:2310.07189`）
- **脉络：** 2 脉冲图网络
- **作者：** Hongwei Ren, Yue Zhou, Yulong Huang, Haotian Fu, Xiaopeng Lin, Jie Song, Bojun Cheng
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spikepoint2024
- **代码：** 未公开（论文内未附代码仓链接）
- **年份：** 2024
- **一句话：** 把事件相机输出的异步事件流切窗映射为三维时空伪点云 $(x, y, t)$，用单阶段 FPS + $k$-NN 局部球分组、折叠高斯绝对距离补偿编码与恒等脉冲残差块直接训练超低功耗事件动作识别网络。
- **链接：** https://arxiv.org/abs/2310.07189
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SpikePoint: An Efficient Point-based Spiking Neural Network for Event Cameras Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：避免把稀疏异步事件压成稠密二维帧造成的时空细节丢失，解决了局部相对坐标含负值无法直接做无符号率编码导致的不对称失真。

**留下的局限**：明确采用替代梯度反向传播从头训练 300 轮（第 5 节结论写明“not converting ANNs to SNNs”）；局部特征与全局特征提取均使用 `MaxPool` 在二值脉冲或脉冲计数上池化。

**是否需要训练或微调**：是（使用 Adam + ATan 替代梯度 + MSE 投票损失从头训练 300 轮）

**涉及的算子**：滑动时间窗三维时空点云映射、最远点采样（FPS）、三维时空坐标 $k$-NN 分组、相对坐标标准差归一化与绝对值 + 组内最小坐标补偿编码 $[\Delta|x|,\Delta|y|,\Delta|z|,x_{\min},y_{\min},z_{\min}]$、无符号泊松率编码、脉冲后恒等残差连接（$\text{LIF}(I)+S^{l-1}$）、局部与全局 `MaxPool`、Parametric LIF 神经元

**关键数字**：$T=16$、1024 采样点下，`DVS128 Gesture` 达 **98.74%**（0.58M 参数，动态能耗 **0.82 mJ**、静态能耗 **0.756 mJ**，Section 4.4 Table 2 & Section 4.5 Table 7）；`Daily DVS` 达 **97.92%**（0.16M 参数，仅为重型 ANN 参数量的约 **0.3%**，Table 3）；`DVS Action` 达 **90.6%**（Table 4）；`HMDB51-DVS` 达 **55.6%**（超越图卷积基线 RG-CNN 的 51.5%，Table 5）；`UCF101-DVS` 达 **68.46%**（Table 6）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（事件流三维点云分组中对局部负相对坐标做分布对称补偿的设计，对点云/事件图输入编码有参考价值）

### <a id="41b0e334-2e6f-8154-92b2-e92f673bf465"></a>DRSGNN（2024）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2024，Vol. 38, No. 15，DOI: `10.1609/aaai.v38i15.29640`）
- **脉络：** 2 脉冲图网络
- **作者：** Han Zhao, Xu Yang, Cheng Deng, Junchi Yan
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#drsgnn2024
- **代码：** [https://github.com/hzhao98/DRSGNN](https://github.com/hzhao98/DRSGNN)
- **年份：** 2024
- **一句话：** 为脉冲图网络引入每个神经元可独立优化的动态反应阈值（Dynamic Reactive Spiking Neurons），并自适应融合图位置脉冲特征以增强长程邻域交互建模。
- **链接：** https://doi.org/10.1609/aaai.v38i15.29640
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Dynamic Reactive Spiking Graph Neural Network
- **核对深度：** 仅摘要
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打破了全图共用单一固定发放阈值的同质性限制，提升了小规模与中等规模静态图节点分类上的表达能力。

**留下的局限**：必须从头训练可学习动态阈值与图位置脉冲模块，无法用于现成预训练视觉图模型的免训练转换。

**是否需要训练或微调**：是（从头端到端直接训练）

**涉及的算子**：可学习动态阈值脉冲神经元、图位置编码脉冲融合、消息传递图卷积聚合

**关键数字**：据 `SGNNBench` 全文统一复现评测（Table 2 & Table 3），`DRSGNN` 在静态同配图 `Cora` / `CiteSeer` / `PubMed` / `Photo` 上达 **80.76% / 71.12% / 78.03% / 92.66%**，在浅层局部异配图 `Chameleon` / `Squirrel` 上达 **63.60% / 47.74%**（居 9 种 SGNN 前列），但在长程异配图 `Roman-Empire` 上仅为 **45.28%**（全精度 GraphGPS 为 82.59%）。

> 💭
> **与本方向的关系（判断）**：背景（通用静态图直接训练代表作，其节点/通道异质可调阈值的思想可与转换校准中的分层/分通道阈值设定对照）

### <a id="41b0e334-2e6f-81bd-a961-eddab27c8006"></a>Dy-SIGN（2024）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2024，Vol. 38, No. 15；预印本 `arXiv:2401.05373`）
- **脉络：** 2 脉冲图网络
- **作者：** Nan Yin, Mengzhu Wang, Zhenghan Chen, Giulia De Masi, Huan Xiong, Bin Gu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#dy-sign2024
- **代码：** 未公开（附录匿名链接已注释）
- **年份：** 2024
- **一句话：** 面向离散时间快照动态图节点分类，设计跨层拓扑与初始特征信息补偿机制，并将多层反馈脉冲图网络的平均发放率视作不动点平衡态，用隐式微分变分训练替代高显存的 BPTT。
- **链接：** https://mlanthology.org/aaai/2024/yin2024aaai-dynamic
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Dynamic Spiking Framework for Graph Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把动态图脉冲训练的显存占用砍到 `SpikeNet` 的一半左右，缓解了多层二值脉冲传递造成的原始图结构细节丢失。

**留下的局限**：处理的是社交/电商/专利等非视觉离散快照动态图，且需要从头训练 100 轮；平衡态推导依赖线性连续图卷积假设（Section 4 公式推导末行明确要求聚合函数 $g_A(\cdot)$ 线性）。

**是否需要训练或微调**：是（采用隐式微分变分法从头训练 100 轮）

**涉及的算子**：快照内 GCN 邻域聚合、首尾跨层特征/结构补偿反馈连接、LIF 脉冲神经元、不动点平衡方程隐式梯度反传、跨时间片状态传递与拼接分类

**关键数字**：在 80% 训练比例下，`DBLP`（28K 节点，27 时间步）Macro-F1 / Micro-F1 达 **74.67±0.5% / 74.96±0.2%**，`Tmall`（577K 节点，186 时间步）达 **61.89±0.1% / 65.82±0.2%**，`Patent`（2.73M 节点，25 时间步）达 **83.91±0.2% / 83.90±0.2%**（Section 4 Table 1 & Table 2），且在 `DBLP` 上训练显存约为 `SpikeNet` 的 **50%**（Section 5.2 Figure 2a）。

> 💭
> **与本方向的关系（判断）**：背景（通用动态图直接训练代表作，其“平衡态等价于缩放 ReLU 图卷积不动点”的推导仅在线性聚合下成立）

### <a id="41b0e334-2e6f-81d8-bf4a-eccf30cbd6ed"></a>Loihi Transductive SGNN（2024）

- **发表处：** arXiv（2024 年 4 月预印本，`arXiv:2404.17048`）
- **脉络：** 2 脉冲图网络
- **作者：** Shay Snyder, Victoria Clerico, Guojing Cong, Shruti Kulkarni, Catherine Schuman, Sumedh R. Risbud, Maryam Parsa
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#loihi-transductive-sgnn2024
- **代码：** 未公开
- **年份：** 2024
- **一句话：** 在面向 Intel Loihi 2 的开源异步框架 Lava 中用定点整数权重与脉冲时间依赖可塑性（STDP）实现直推式引文图分类，并用贝叶斯优化（Lava BO）自动搜索神经形态超参数。
- **链接：** https://arxiv.org/abs/2404.17048
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Transductive Spiking Graph Neural Networks for Loihi
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：摆脱了传统冯·诺依曼浮点仿真器（NEST）无法直接部署到异步定点类脑芯片的限制，验证了纯脉冲局部可塑性规则在图拓扑上的硬件兼容原型。

**留下的局限**：仅利用引文边连接而不处理高维连续视觉特征，且直推式 STDP 在 `Cora` 上的分类精度明显低于现代 GNN。

**是否需要训练或微调**：是（基于在线 STDP 突触可塑性学习与 Lava BO 超参数搜索）

**涉及的算子**：无漏电定点积分发放神经元、不应期门控（Refractory gating）、STDP 突触权重更新、异步通道事件通信

**关键数字**：在 `Cora` 验证集上，Lava 定点实现于 $t=14$ 时间步、零突触延迟下取得 **63.57%** 分类精度（对比 NEST 浮点延迟 1 配置的 68.57%，Section 4 Table 2），经 15 轮 Lava BO 搜索 2,450 组参数后测试精度为 **62.86%**，单篇论文网络重置开销从 NEST 的 9.73 s 降至 **123.6 ms**（Section 4）。

> 💭
> **与本方向的关系（判断）**：背景（类脑芯片 Loihi 2 软件栈 Lava 上的纯事件图推理早期探索，与脉络五硬件实测呼应）

### <a id="41b0e334-2e6f-81dd-9e3d-c837dcf75f09"></a>MSG（2024）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2024，Vol. 37，DOI: `10.52202/079017-1071`；预印本 `arXiv:2410.17941`）
- **脉络：** 2 脉冲图网络
- **作者：** Li Sun, Zhenhao Huang, Qiqi Wan, Hao Peng, Philip S. Yu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#msg2024
- **代码：** 论文内仅提供匿名评审仓 `https://anonymous.4open.science/r/MSG-16E9`（未见正式实名公开仓）
- **年份：** 2024
- **一句话：** 将脉冲图神经网络推广到双曲/球面等常曲率黎曼流形空间（MSG），利用指数映射与对数映射桥接切空间脉冲序列与流形点，并推导无需替代梯度、无需按时间步反向展开（BPTT-free）的流形微分（DvM）训练算法。
- **链接：** https://arxiv.org/abs/2410.17941
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking Graph Neural Network on Riemannian Manifolds
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：克服了欧氏空间脉冲图网络表达层次/环状图结构的几何失真，同时在反向传播时绕开了不可导阶跃函数和随 $T$ 线性增长的 BPTT 训练延迟。

**留下的局限**：面向同配无向静态图的节点分类与链路预测从头训练（作者在 Section 8 局限性中自述尚未解决有向图与异配图，且 `SGNNBench` 实测其在深层异配图上掉点严重）；流形指数/对数映射涉及大量超越函数浮点运算。

**是否需要训练或微调**：是（使用流形微分 DvM 从头训练）

**涉及的算子**：黎曼流形对数映射（$\operatorname{Log}_{\mathbf{z}}$）与指数映射（$\operatorname{Exp}_{\mathbf{z}}$）、切空间图卷积聚合、IF/LIF 脉冲神经元、推前/拉回（Pushforward / Pullback）雅可比矩阵反向梯度

**关键数字**：$T \in \{5, 15\}$、32 维双曲洛伦兹流形 $\mathbb{H}^{32}$ 下，节点分类精度在 `Computers` / `Photo` / `CS` / `Physics` 上分别达 **89.27±0.19% / 93.11±0.11% / 92.65±0.04% / 95.93±0.07%**，链路预测 AUC 分别达 **94.65% / 96.75% / 95.19% / 93.43%**（Section 6.2 Table 1）；理论推理能耗分别为 **0.047 / 0.043 / 0.026 / 0.029 mJ**，不到全精度黎曼 GNN 基线的 **1/20**（Table 3）。

> 💭
> **与本方向的关系（判断）**：背景（通用静态图直接训练里程碑；Claude 草稿二轮补充曾引用其相关工作综述判断）

### <a id="41b0e334-2e6f-81f2-9a81-d3fb0e22e2ed"></a>Spiking PointCNN（2024）

- **发表处：** Electronics（MDPI，2024 年 9 月，Vol. 13, Issue 18, Article 3626，DOI: `10.3390/electronics13183626`）
- **脉络：** 2 脉冲图网络
- **作者：** Yingzhi Tao, Qiaoyun Wu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spiking-pointcnn2024
- **代码：** [https://github.com/DeadlyAbyss/Spiking-PointCNN](https://github.com/DeadlyAbyss/Spiking-PointCNN)
- **年份：** 2024
- **一句话：** 将 PointCNN 的局部坐标 $\mathcal{X}$-变换卷积模块在架构层面替换为嵌入 LIF 脉冲神经元的 `Spiking X-Conv`，并用**可调陡度参数的替代梯度函数从头反向传播训练** 3D 点云分类网络。
- **链接：** https://www.mdpi.com/2079-9292/13/18/3626
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking PointCNN: An Efficient Converted Spiking Neural Network under a Flexible Framework
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在保留 PointCNN 对无序局部点集做学习置换（$\mathcal{X}$-transformation）能力的同时引入脉冲激活，提升了合成点云与含噪真实扫描点云上的直接训练收敛性。

**留下的局限**：**极其关键的文献纠偏**：尽管论文标题和摘要使用了“Converted SNN”一词，但原文第 3.2–3.3.3 节及官方代码（`main_ModelNet.py` 从头训练 600 轮、`main_ScanObjectNN.py` 从头训练 1000 轮）证实，**它根本不是把预训练 ANN 权重转成 SNN 的转换方法**，而是“把网络模块替换成脉冲层后用替代梯度从头训练”；此外，官方代码 `SpikingLayers.py` 在每个脉冲层内部重复输入 $T$ 次后立刻执行 `out = out.mean(dim=0)` 折叠回连续浮点数，导致层间传递与矩阵乘（`torch.matmul(x_star, transform_matrix)`）实为浮点运算，且全文未报告任何能耗或发放率数据。

**是否需要训练或微调**：**是**（完全从头直接训练，无任何预训练 ANN 权重复制、阈值平衡或训练后校准）

**涉及的算子**：**三维空间坐标膨胀 **$k$**-NN 建图**（4 层 `Spiking X-Conv` 的 $(K, D)$ 依次为 $(8,1), (12,2), (16,2), (16,2)$，非按深层特征动态选邻居）、最远点采样（FPS，下采样率 0.375 与 0.334）、局部相对坐标中心化 $p_{i,k}-p_i$、坐标特征脉冲 MLP（$MLP'_\delta$）与 $\mathcal{X}$ 置换矩阵脉冲 MLP（$MLP'_{trans}$）、深度可分离一维卷积、全局均值池化（`global_mean_pool`）、硬复位 LIF 神经元与可调替代梯度（正文 Eq. 13 写为参数化 Sigmoid，开源代码 `SpikingLayers.py` 实现为温度缩放 `tanh`）

**关键数字**：时间步消融 $T \in \{1,2,3,4\}$（默认 $T=1$）：在 `ModelNet40` 上，$T=1,2,3,4$ 的 OA 分别为 **84.28% / 85.78% / 85.94% / 84.97%**，mACC 分别为 **81.85% / 84.48% / 83.14% / 80.71%**（Section 4.2.3 Table 3）；替代梯度陡度 $k=1$ 时 `ModelNet40` 取得主对比表最佳 OA **86.71% / 82.21% mACC**（Table 2 & Table 4，主表四舍五入记为 **86.7% / 82.2%**）；在真实扫描集 `ScanObjectNN`（代码加载 `PB_T50_RS` 旋转缩放扰动集）上主表报告 **74.1% OA / 73.3% mACC**（Section 4.3 Table 4；注：正文第 40 段文字另称最高达 76.10% OA，与表 4 的 74.1% 存在文内不一致，两处均予记录）；相比作者自建同结构无脉冲基线（84.68% OA，Table 1）高 1.26%，但相比原版全精度 PointCNN（ModelNet40 92.2%、ScanObjectNN 78.5%）分别低约 **5.5%** 与 **4.4%**。

> 💭
> **与本方向的关系（判断）**：直接相关（定向问题 Q4 的目标论文；纠正 Claude v1 将其误判为“点云 ANN→SNN 转换先例”的关键证据——真正的点云转换先例是该文表 4 引用的 `[20]` Lan et al., ICCV 2023）

### <a id="41b0e334-2e6f-8106-ad5f-cb47f46d290c"></a>MotionDeltaCNN（2023）

- **发表处：** IEEE/CVF International Conference on Computer Vision（ICCV 2023）（据 CVF 检索；PDF 为 arXiv 版）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Mathias Parger, Chengcheng Tang, Thomas Neff, Christopher D. Twigg, Cem Keskin, Robert Wang, Markus Steinberger
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#motiondeltacnn2023
- **代码：** 未核实
- **年份：** 2023
- **一句话：** 把 DeltaCNN 推广到移动相机：用环形缓冲对齐前后帧，只处理新露出的区域和真正变化的像素。
- **链接：** https://arxiv.org/abs/2210.09887
- **核对人与日期：** Gemini，2026-11-16
- **标题：** MotionDeltaCNN: Sparse CNN Inference of Frame Differences in Moving Camera Videos with Spherical Buffers and Padded Convolutions
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：相机移动时几乎所有像素都变，DeltaCNN 退化为稠密计算；球形缓冲和带填充的卷积让新区域无缝接入已有缓冲。

**留下的局限**：仍是 CNN；依赖前后帧可对齐。

**是否需要训练或微调**：否（使用作者提供的预训练权重，第 6 页）

**涉及的算子**：卷积、激活、截断阈值、环形缓冲

**关键数字**：移动相机视频上帧率比 DeltaCNN 最多高 90%（第 1 页摘要、第 2 页）。

> 💭
> **与本方向的关系（判断）**：背景

### <a id="41b0e334-2e6f-8130-8b78-fdecb6648d37"></a>EvNets（2022）

- **发表处：** European Conference on Computer Vision（ECCV 2022）（据检索结果；PDF 为 arXiv 版）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Matthew Dutson, Yin Li, Mohit Gupta
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#evnets2022
- **代码：** 未核实
- **年份：** 2022
- **一句话：** 给每个神经元加上长期记忆的状态变量，只有累计变化超过阈值才向下游发送，可把现成网络直接改造成事件驱动推理。
- **链接：** https://arxiv.org/abs/2112.00891
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Event Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：Skip-Conv 一类“只看帧间差”的做法会漏掉缓慢累积的变化（第 7 页举例：从 0 每步增加 0.1δ 到 2δ）；EvNets 用累积量和阈值 $m_i=H(|d_i|-h_i)$ 解决（第 9 页式 6）。

**留下的局限**：针对 CNN；没有处理图结构和邻居选择。

**是否需要训练或微调**：否（第 1 页摘要“without re-training”；附录中的 HRNet 基线本身是在 JHMDB 上微调的）

**涉及的算子**：卷积、线性层、逐神经元阈值、累积器

**关键数字**：计算量约降一个数量级（第 1 页摘要、第 3 页）；每个模型选“PCK 或 mAP 下降不到 0.5%”的最高阈值，结果见第 12 页 Table 1，开销见 Table 2。

> 💭
> **与本方向的关系（判断）**：可借用的技术（逐神经元阈值 + 累积状态与脉冲神经元的“积分—发放”同构）

### <a id="41b0e334-2e6f-8150-b1b1-f1356365a7bf"></a>InkStream（2025）

- **发表处：** 2025 IEEE International Parallel and Distributed Processing Symposium（IPDPS 2025），pp. 1273–1285（据检索结果；arXiv 版 2023 年发布）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Dan Wu, Zhaoying Li, Tulika Mitra
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#inkstream2025
- **代码：** [https://github.com/WuDan0399/InkStream](https://github.com/WuDan0399/InkStream) （据 RIPPLE++ 正文引用）
- **年份：** 2025
- **一句话：** 利用 max / min 聚合“只有被选中的邻居才有贡献”这一性质，在流式图里只更新真正受影响的节点，并保证结果与重新推理完全相同。
- **链接：** https://arxiv.org/abs/2309.11071
- **核对人与日期：** Gemini，2026-11-16
- **标题：** arXiv 版：InkStream: Real-time GNN Inference on Streaming Graphs via Incremental Update；**会议版标题不同**：InkStream: Instantaneous GNN Inference on Dynamic Graphs via Incremental Update（据检索到的 IPDPS 2025 目录，未打开会议版 PDF）
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：k 层 GNN 的一次更新理论上要访问整个 k 跳邻域，GPU 放不下；它发现 max / min 聚合下理论受影响区域里大多数节点其实没受影响（第 2 页 Fig. 3(b)：100 次更新时平均只有 3%），用事件机制控制层间传播。

**留下的局限**：节省来自 max / min 的选择性，对 sum / mean 收益小；精确方法无阈值；在视觉图上每帧所有节点特征都可能变，选择性带来的节省未经验证。

**是否需要训练或微调**：否

**涉及的算子**：max / min / sum 聚合，GCN、GraphSAGE、GIN

**关键数字**：三个模型、四张大图上，CPU 集群加速 2.5–427 倍，两种 GPU 集群加速 2.4–343 倍，输出与最新快照上的推理完全相同（第 1 页摘要）。

> 💭
> **与本方向的关系（判断）**：直接相关（ViG、DGCNN 都用 max 聚合，它说明 max 的选择性能大幅压低多跳扩散）

### <a id="41b0e334-2e6f-8152-bc9a-fe36594e3e25"></a>EvGNN（2025）

- **发表处：** IEEE Transactions on Circuits and Systems for Artificial Intelligence（TCASAI），2025（DOI 10.1109/TCASAI.2024.3520905，第 1 页页眉）
- **脉络：** 4 事件驱动与增量推理,5 能耗与硬件
- **作者：** Yufeng Yang, Adrian Kneip, Charlotte Frenkel
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#evgnn2025
- **代码：** [https://github.com/cogsys-tudelft/evgnn](https://github.com/cogsys-tudelft/evgnn)
- **年份：** 2025
- **一句话：** 事件相机 GNN 的 FPGA 加速器，用“只指向新事件”的有向图把每次更新限制在一跳，从而让多层网络能逐层并行处理。
- **链接：** https://arxiv.org/abs/2404.19489
- **核对人与日期：** Gemini，2026-11-16
- **标题：** EvGNN: An Event-driven Graph Neural Network Accelerator for Edge Vision
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

##### 来自脉络 4 事件驱动与增量推理 的记录

**解决的难点**：无向事件图的更新会逐层扩散到 n 跳（第 2 页定义）；改成有向动态图后每个新事件只影响自身，存储也不必保存边。

**留下的局限**：跑的是 INT8 量化 GNN，不是脉冲网络；有向单跳的简化只适用于“每个事件是一个新节点”的事件图，不适用于节点固定、特征逐帧变化的超像素图或 ViG 图。

**是否需要训练或微调**：是（需按其有向图结构训练并量化）

**涉及的算子**：PointNetConv 风格的消息传递、max 聚合、INT8 量化

**关键数字**：Xilinx KV260 上 N-CARS 精度 87.8%，平均每事件延迟 16 µs（第 1 页摘要）；Table VI（第 10 页）中软件版 0.07 MFLOPs/ev、88.0%。同表把 AEGNN 记为 0.6 MFLOPs/ev、86.7%（注明来自开源代码复现），与 AEGNN 论文 Table 1 的 0.47 MFLOPs/ev、0.945 不一致，两者都记录。

> 💭
> **与本方向的关系（判断）**：可借用的技术（硬件端如何规避多跳扩散）

##### 来自脉络 5 能耗与硬件 的记录

**标题**：EvGNN: An Event-Driven Graph Neural Network Accelerator for Edge Vision

**作者**：Yufeng Yang, Adrian Kneip, Charlotte Frenkel

**发表处**：IEEE Transactions on Circuits and Systems for Artificial Intelligence（IEEE TCASAI），vol. 2, no. 1, pp. 37–50, 2025（DOI: `10.1109/TCASAI.2024.3520905`；预印本 `arXiv:2404.19489v2` 首版提交于 2024 年 4 月）

**链接**：[https://arxiv.org/abs/2404.19489](https://arxiv.org/abs/2404.19489) ；代码：[https://github.com/cogsys-tudelft/evgnn](https://github.com/cogsys-tudelft/evgnn)

**核对深度**：全文

**一句话**：提出面向事件相机的算法—硬件协同优化框架，用有向单跳棱柱队列建图和**免重训 INT8 训练后量化（PTQ）**的简化 PointNetConv，在边缘 FPGA 和 28nm ASIC 模型上实现 16 微秒级逐事件推理。

**解决的难点**：（1）把 AEGNN 中昂贵的双向多跳无向图与 SplineConv 简化为有向单跳图 + 轻量 PointNetConv，避免了历史节点级联重算；（2）用 L1 距离棱柱邻域 + 片上事件队列取代耗时的球面欧氏建图；（3）设计层间并行硬件流水，将多跳延迟压缩到微秒量级。

**留下的局限**：（1）**同样不是脉冲网络**：节点激活是 8-bit 整数量化特征，不是脉冲序列；（2）未设计图池化层，深层图规模不收缩，特征维度被迫限制在 32 维以内，且大容量场景仍需访问片外 DRAM（DRAM 占总延迟 50% 以上、占总能耗约 73%，见 Section V-D 及 EFGCN 对照分析）；（3）只适用于事件相机时空坐标建图，不涉及按高维语义特征重算动态 $k$NN 的视觉图骨干。

**是否需要训练或微调**：部分（浮点简化模型本身需从头训练；但**从 FP32 转为硬件 8-bit 定点部署采用的是免重训的训练后量化 PTQ + BN 折叠**，仅掉点 0.1%，见 Section III-C & Table IV, p. 6！）

**涉及的算子**：有向单跳棱柱 L1 邻域事件队列建图、简化版 PointNetConv（线性层 + BN 折叠 + ReLU + `max` 邻域聚合）、INT8 训练后量化（PTQ）

**关键数字**：（1）量化消融（Table IV, p. 6）：在 N-CARS（`120×100`）上，FP32 精度 `87.9%`，**直接 INT8 PTQ 精度达 **`**87.8%**`（仅降 `0.1%`），单事件计算量仅 `0.07 MFLOPs/ev`（参数量 `4.8k`）；（2）**Xilinx KV260 Ultrascale+ MPSoC 实测**（Tables V–VI, p. 10）：占用 `30,908` LUTs、`24,083` FFs、`228` DSPs、`1.76 MB` 片上存储（15 BRAM + 48 URAM），单事件端到端延迟 `**16 µs/event**`，精度 `**87.8%**`；（3）**28nm CMOS ASIC 综合与仿真评估**（`0.8V, 200MHz, 2.5 mm²`，Section V-D, p. 11 & Fig. 14, p. 12）：单事件延迟 `**10.7 µs/event**`，单事件能耗仅 `**305 nJ/event**`。

> 💭
> **与本方向的关系（判断）**：直接相关（既是事件图硬件的核心参照，又给出了一个极重要的事实：**在 PointNetConv + **`**max**`** 聚合上，标准 INT8 PTQ 几乎无损（掉点仅 0.1%）**，这意味着脉冲转换在 8-bit 等效预算下将面临极强的 PTQ 对手！）

### <a id="41b0e334-2e6f-8169-b6b3-ff85004ce8f0"></a>InstantGNN（2022）

- **发表处：** Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining（KDD 2022）（第 1 页）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Yanping Zheng, Hanzhi Wang, Zhewei Wei, Jiajun Liu, Sibo Wang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#instantgnn2022
- **代码：** 未核实
- **年份：** 2022
- **一句话：** 动态图上边陆续到来时，增量更新解耦式 GNN 的传播矩阵，用残差阈值控制近似误差，不必每个快照都重算。
- **链接：** https://arxiv.org/abs/2206.01379
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Instant Graph Neural Networks for Dynamic Graphs
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：快照式动态 GNN 反映变化有延迟、重复计算量大；它借用近似 PPR 的“估计值 + 残差”推送算法，只推送残差超过阈值 ε 的节点（第 4–5 页 Algorithm 1、2），并给出更新复杂度上界。

**留下的局限**：阈值作用在**线性特征传播**（解耦 GNN 的预处理）上，不是多层非线性消息传递的逐层激活；附带“何时重训”的自适应策略。这是图上唯一找到的“小于阈值不传”的做法，但机制与 DeltaCNN 式逐层截断不同。

**是否需要训练或微调**：部分（传播增量更新，分类器按自适应策略在必要时重训）

**涉及的算子**：线性特征传播（类 PPR）、残差推送、MLP 分类器

**关键数字**：大图上效率提高一到数个数量级，精度相当（第 2 页贡献、第 8 页 Fig. 1–3）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（图上“残差 + 阈值”推送的误差分析可借）

### <a id="41b0e334-2e6f-816c-8a89-dca8703814da"></a>Eventful Transformers（2023）

- **发表处：** IEEE/CVF International Conference on Computer Vision（ICCV 2023）（PDF 为 arXiv 版，会议归属据 CVF 检索，见 SL-65）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Matthew Dutson, Yin Li, Mohit Gupta
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#eventful-transformers2023
- **代码：** 未核实
- **年份：** 2023
- **一句话：** 视频逐帧跑 ViT 时，每个块里只重新处理变化大的 token，其余沿用上一帧的结果。
- **链接：** https://arxiv.org/abs/2308.13494
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Eventful Transformers: Leveraging Temporal Redundancy in Vision Transformers
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 多数情况否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：用“参考缓冲 + 误差累积”的 token 门避免缓慢漂移被一直忽略；注意力里的 $QK^\top$ 和 $AV$ 用差分形式增量更新（第 4–6 页）；选择策略有 top-r（固定预算）和阈值 h（输入自适应）两种（第 6 页）。

**留下的局限**：自注意力相当于全连接图，一跳就扩散到所有 token，它靠门在每个块后截断；没有处理稀疏图上的多跳扩散，也没有处理按特征选邻居（kNN）这种离散决策。

**是否需要训练或微调**：多数情况否（第 1 页摘要：“often without any re-training”）；第 3 页称同类自适应 ViT 方法一般需要重训。

**涉及的算子**：token 门、自注意力、Softmax、LayerNorm、MLP

**关键数字**：ImageNet VID 上 ViTDet，分辨率 1024、r=768 时由 467.4 降到 122.3 GFlops（3.8 倍），mAP50 由 82.93 降到 81.25；分辨率 672 时省 3.7 倍、mAP50 降 0.85（第 8 页）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（“全连接图 + 门截断”是最接近 ViG 的增量推理先例）

### <a id="41b0e334-2e6f-8177-a5ae-ef1f224aafb6"></a>CoST-GCN（2023）

- **发表处：** Pattern Recognition，Vol. 140，109528，2023（据检索结果；PDF 为 arXiv 版）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Lukas Hedegaard, Negar Heidari, Alexandros Iosifidis
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#cost-gcn2023
- **代码：** [https://github.com/lukashedegaard/continual-skeletons](https://github.com/lukashedegaard/continual-skeletons) （第 6 页）
- **年份：** 2023
- **一句话：** 把 ST-GCN 改写成“来一帧算一帧”的连续推理网络，时间卷积缓存历史结果，不再每次重算整段序列。
- **链接：** https://arxiv.org/abs/2203.11009
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Continual Spatio-Temporal Graph Convolutional Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：骨架动作识别的在线推理中，滑窗输入造成大量重复计算。

**留下的局限**：节省来自时间维的缓存复用，空间图上每帧所有关节仍全部重算，没有阈值；直接搬权重会因去掉补零掉 0.3 个点，最好再微调（第 7 页 Table I）。

**是否需要训练或微调**：部分（可直接转换，微调后精度更好）

**涉及的算子**：空间图卷积（固定骨架图）、时间卷积、BatchNorm、ReLU、自注意力（CoAGCN、CoS-TR 变体）

**关键数字**：每次预测 FLOPs 最多降 109 倍，硬件上加速 26 倍，峰值显存降 52%（第 1 页摘要）；NTU RGB+D 60 X-View 上直接转换精度 −0.3（第 7 页 Table I）。

> 💭
> **与本方向的关系（判断）**：直接相关（ST-GCN 是失效普查的流式教师，这是它的增量推理先例，但不是差分推理）

### <a id="41b0e334-2e6f-8188-86f2-fd847900b43e"></a>DeltaCNN（2022）

- **发表处：** IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2022）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Mathias Parger, Chengcheng Tang, Christopher D. Twigg, Cem Keskin, Robert Wang, Markus Steinberger
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#deltacnn2022
- **代码：** [https://github.com/facebookresearch/DeltaCNN](https://github.com/facebookresearch/DeltaCNN)
- **年份：** 2022
- **一句话：** 视频逐帧推理时，各层只传帧间差分，差分太小就截断并存入缓冲，第一个在 GPU 上真正跑赢 cuDNN 的稀疏 CNN 框架。
- **链接：** https://arxiv.org/abs/2203.03996
- **核对人与日期：** Gemini，2026-11-16
- **标题：** DeltaCNN: End-to-End CNN Inference of Sparse Frame Differences in Videos
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：线性层传差分、非线性层保存累积输入；截断误差放进缓冲，超过阈值才一次性发出，避免误差长期累积（第 4 页 Fig. 3）；每层阈值在小训练子集上从前往后自动调（第 5 页 3.3 节）。

**留下的局限**：针对规则网格卷积；“更新掩码随卷积逐层膨胀”在图上对应多跳扩散，但它没有处理按特征选邻居。

**是否需要训练或微调**：否（第 1 页摘要“without retraining”；阈值需在小子集上自动调）

**涉及的算子**：卷积、ReLU 等激活、池化、截断阈值 ε、累积缓冲

**关键数字**：最高 7 倍加速（第 1 页摘要）；单像素更新经三层 3×3 卷积扩散到 49 像素（第 5 页 3.3 节）；Human3.6M 姿态估计的速度与精度对比见第 8 页 Table 1。

> 💭
> **与本方向的关系（判断）**：直接相关（差分推理在 CNN 上的对应物，阈值 + 截断缓冲是可直接借到图上的机制）

### <a id="41b0e334-2e6f-8100-b692-c685fc1e7650"></a>BlockGCN（2024）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2024，pp. 2049–2058）
- **脉络：** 3 视觉图骨干
- **作者：** Yuxuan Zhou, Xudong Yan, Zhi-Qi Cheng, Yan Yan, Qi Dai, Xian-Sheng Hua
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#blockgcn2024
- **代码：** [https://github.com/ZhouYuxuanYX/BlockGCN](https://github.com/ZhouYuxuanYX/BlockGCN)
- **年份：** 2024
- **一句话：** 指出可学习骨架邻接矩阵在训练中会发生“物理骨骼拓扑灾难性遗忘”，通过最短路径跳数静态编码 + 持续同调条形码动态编码保住拓扑先验，并用块对角分组权重矩阵砍掉 40% 以上冗余参数。
- **链接：** https://openaccess.thecvf.com/content/CVPR2024/html/Zhou_BlockGCN_Redefine_Topology_Awareness_for_Skeleton-Based_Action_Recognition_CVPR_2024_paper.html
- **核对人与日期：** Gemini，2026-11-16
- **标题：** BlockGCN: Redefine Topology Awareness for Skeleton-Based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在不依赖多头自注意力的前提下，以更少参数同时保留静态物理骨骼约束与样本级全局几何动态。

**留下的局限**：官方仓库未公开预训练模型权重；且其动态拓扑分支需要对每个输入序列构建 Vietoris-Rips 单纯复形滤子并计算 0 维持续同调生灭条形码，无法直接用脉冲神经元实现（只能作为首层离线输入特征预处理）。

**是否需要训练或微调**：是（端到端浮点训练 140 轮）

**涉及的算子**：最短路径距离查表嵌入（`Static Topological Encoding`）、关节欧氏距离 Vietoris-Rips 持续同调条形码向量化（`Dynamic Topological Encoding`）、块对角分组图卷积 `BlockGC`（$K=8$ 组）、多尺度时序卷积（含 `3×1 MaxPool` 分支）、`BatchNorm`、`ReLU`

**关键数字**：单关节流 `BlockGCN`（1.3M 参数，1.63G FLOPs，较基线减参 **43%**，Table 2 & 4，第 7–8 页）：`NTU-RGB+D 60` X-Sub / X-View 达 **90.9% / 95.4%**，`NTU-RGB+D 120` X-Sub / X-Set 达 **86.9% / 88.2%**；4 流集成（Table 2，第 7 页）：`NTU-60` 达 **93.1% / 97.0%**，`NTU-120` 达 **90.3% / 91.5%**，`NW-UCLA` 达 **96.9%**。

> 💭
> **与本方向的关系（判断）**：背景（骨架图近两年的代表性强基线；因无公开预训练权重且含持续同调拓扑预处理，转换实验优先选公开权重的 `ST-GCN`、`CTR-GCN` 或 `HD-GCN`）

### <a id="41b0e334-2e6f-8147-baf6-c94fa0b0bf57"></a>MobileViG（2023）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops（CVPRW 2023，Mobile AI Workshop，pp. 2211–2219；预印本 `arXiv:2307.00395`）
- **脉络：** 3 视觉图骨干
- **作者：** Mustafa Munir, William Avery, Radu Marculescu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#mobilevig2023
- **代码：** [https://github.com/SLDGroup/MobileViG](https://github.com/SLDGroup/MobileViG) （预训练权重：[https://huggingface.co/SLDGroup/MobileViG/tree/main](https://huggingface.co/SLDGroup/MobileViG/tree/main) ）
- **年份：** 2023
- **一句话：** 在前三阶段使用移动端倒残差卷积，仅在第四阶段（$7\times 7$ 特征图）用**完全固定的稀疏轴向网格连边（SVGA）**替代动态 $k$-NN 搜索，直接通过张量循环移位和逐元素 `max` 完成图聚合，（论文自称）首次让视觉图骨干在手机 NPU 上跑进 1 毫秒级。
- **链接：** https://arxiv.org/abs/2307.00395
- **核对人与日期：** Gemini，2026-11-16
- **标题：** MobileViG: Graph-Based Sparse Attention for Mobile Vision Applications
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：彻底消除了原版 `ViG` 中移动端 NPU 极不擅长的两两特征距离矩阵计算、动态 `topk` 排序以及频繁的 4D↔3D 张量重排开销。

**留下的局限**：（1）只在最末 $7\times 7$ 低分辨率阶段包含图层，前三阶段本质仍是纯 CNN（`MBConv`）；（2）**其 **`**MRConv4d**`** 依然保留了逐元素取最大值 **`**max**`** 聚合与 **`**GELU**`** 激活**——源码初始化 `x_j = x - x = 0`，将负相对差全部截断为 0 后对 6 个轴向移位差值取 `max`，在低时间步二值脉冲下仍会遭遇转换偏差。

**是否需要训练或微调**：是（浮点教师在 ImageNet-1K 上配合 `RegNetY-16GF` 蒸馏训练）

**涉及的算子**：静态稀疏轴向图构建 `SVGA`（步幅 $K=2$，`torch.roll` 同行同列移位 $\{2,4,6\}$ 共 6 个固定轴向邻居）、轴向相对差**逐元素 **`**max**`** 聚合 **`**MRConv4d**`（$\max_{mK\in\{2,4,6\}}(0, x - \text{roll}(x, mK))$ 后拼接做 $1\times 1$ 卷积）、`MBConv`、`BatchNorm2d`、`GELU`

**关键数字**：`ImageNet-1K` Top-1 精度与 iPhone 13 Mini NPU 实测延迟（Tables 2–3，第 5–6 页）：`MobileViG-Ti`（5.2M 参数）**75.7%** / **0.78 ms**，`MobileViG-S`（7.2M）**78.2%** / **0.99 ms**，`MobileViG-M`（14.0M）**80.6%** / **1.38 ms**，`MobileViG-B`（26.7M）**82.6%** / **2.30 ms**；`MS COCO` Mask R-CNN（Table 4，第 7 页）：`MobileViG-M / B` 达 **41.3 / 42.0** $\text{AP}^b$、**38.1 / 38.9** $\text{AP}^m$。

> 💭
> **与本方向的关系（判断）**：直接相关（**本项目极佳的首批免训练转换教师模型之一**：`Apache-2.0` 协议、HuggingFace 权重齐全，且天然固定了图拓扑而保留了 `MRConv` 的 `max` 聚合与 `GELU`，能与动态建图的 `ViG` 形成完美的单变量对照！）

### <a id="41b0e334-2e6f-8167-be5f-c852220398d0"></a>ViG 与 Pyramid ViG（2022）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2022，Vol. 35，pp. 8291–8303；预印本 `arXiv:2206.00272`）
- **脉络：** 3 视觉图骨干
- **作者：** Kai Han, Yunhe Wang, Jianyuan Guo, Yehui Tang, Enhua Wu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#vig-与-pyramid-vig2022
- **代码：** [https://github.com/huawei-noah/Efficient-AI-Backbones/tree/master/vig_pytorch](https://github.com/huawei-noah/Efficient-AI-Backbones/tree/master/vig_pytorch) （预训练权重：[https://github.com/huawei-noah/Efficient-AI-Backbones/releases/tag/vig](https://github.com/huawei-noah/Efficient-AI-Backbones/releases/tag/vig) 与 [https://github.com/huawei-noah/Efficient-AI-Backbones/releases/tag/pyramid-vig](https://github.com/huawei-noah/Efficient-AI-Backbones/releases/tag/pyramid-vig) ）
- **年份：** 2022
- **一句话：** 开创性地不再把图像看作规则像素网格或全连接序列，而是把图像块当作图节点，在**每一层动态按特征重算空洞 ****$k$**** 近邻图**并用相对差最大值 `MRConv` 传递消息，证明纯视觉图神经网络在 ImageNet 与 COCO 上可匹敌主流 CNN 与 ViT。
- **链接：** https://arxiv.org/abs/2206.00272
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Vision GNN: An Image is Worth Graph of Nodes
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打破了 CNN 固定局部方形卷积核与 ViT 稠密全局自注意力的二元对立，能够灵活连接不规则物体轮廓与语义同源区域，并通过 `Grapher` 双线性投影 + `FFN` 抑制了深层 GNN 的过平滑崩溃。

**留下的局限**：**集中暴露了视觉图免训练转脉冲的全部三大核心障碍**：（1）每一层 `Grapher` 都对 $\ell_2$ 归一化后的特征重算两两距离并用 `topk` 选邻居，低时间步脉冲量化噪声会直接扰动边集合（拓扑漂移）；（2）默认聚合算子 `MRConv2d` 对带符号特征差 $\tilde{x}_j-\tilde{x}_i$ 取逐元素 `max`，在脉冲流上存在系统性高估与正负号错位；（3）全网采用 `GELU` 激活（虽全用 `BatchNorm2d` 可折叠进 $1\times 1$ 卷积，但 `GELU` 负半轴非单调）。此外核查发现**论文与官方仓库两处数字冲突**：论文 Table 5 报 `Pyramid ViG-Ti` 为 **78.2%**、`Pyramid ViG-B` 参数量为 **92.6M**，而官方 `vig_pytorch/readme.md` 发布的 `pvig_ti` 实测权重精度为 **78.5%**、`pvig_b` 参数量为 **82.6M**。

**是否需要训练或微调**：是（ImageNet-1K 上用 DeiT 配方端到端训练 300 轮）

**涉及的算子**：通道 $\ell_2$ 归一化特征成对欧氏距离平方（等价余弦距离）+ 二维相对位置偏置（金字塔版）、动态空洞 $k$-NN 搜索（各向同性 $k=9\to 18$，金字塔恒定 $k=9$，空洞率 $\lceil l/4\rceil$）、源节点空间 `AvgPool` 降采样（金字塔版前两阶段 $r=[4,2,1,1]$）、相对差最大值图卷积 `MRConv2d`（拼接 $[\tilde{x}_i\|\max_{j\in\mathcal{N}(i)}(\tilde{x}_j-\tilde{x}_i)]$ 接 4 组分组 $1\times 1$ 卷积）、`BatchNorm2d`、`GELU`、`FFN`

**关键数字**：`ImageNet-1K` Top-1 精度：各向同性 `ViG-Ti/S/B` 达 **73.9% / 80.4% / 82.3%**（Table 4，第 6 页）；金字塔 `Pyramid ViG-Ti/S/M/B` 论文 Table 5（第 7 页）报 **78.2% / 82.1% / 83.1% / 83.7%**（仓库发布权重 `Ti` 为 **78.5%**）；算子消融（Tables 1–3，第 5–6 页，`ViG-Ti`）：`Max-Relative` **73.9%** 优于 `EdgeConv`（72.3%）、`GIN`（72.8%）、`GraphSAGE`（73.3%），`GELU` **73.9%** 显著优于 `ReLU`（**71.4%**，低 2.5%）与 `LeakyReLU`（72.5%）；`MS COCO` `Pyramid ViG-S` 配 RetinaNet 达 **41.8** mAP，配 Mask R-CNN 达 **42.6** $\text{AP}^b$ / **39.4** $\text{AP}^m$（Table 10，第 9 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（**本项目最核心的首要教师模型**；`Apache-2.0` 许可证、官方 PyTorch 代码精炼、GitHub Release 全系列预训练权重可直接下载）

### <a id="41b0e334-2e6f-816c-806c-f18b477110bb"></a>HD-GCN（2023）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2023，pp. 10444–10453；预印本 `arXiv:2208.10741`）
- **脉络：** 3 视觉图骨干
- **作者：** Jungho Lee, Minhyeok Lee, Dogyoon Lee, Sangyoun Lee
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#hd-gcn2023
- **代码：** [https://github.com/Jho-Yonsei/HD-GCN](https://github.com/Jho-Yonsei/HD-GCN) （预训练权重：[https://drive.google.com/drive/folders/1FB_IQdTMWE8cRvwE2KiyxC0P6LyqZku4?usp=sharing](https://drive.google.com/drive/folders/1FB_IQdTMWE8cRvwE2KiyxC0P6LyqZku4?usp=sharing) ）
- **年份：** 2023
- **一句话：** 以身体质心为根将人体骨架分解为多层有根树，把相邻层级间的远距语义对称关节（如左右手、左右脚）显式全连接，并融合特征空间动态 $k$-NN `EdgeConv` 与层次注意力聚合。
- **链接：** https://openaccess.thecvf.com/content/ICCV2023/html/Lee_Hierarchically_Decomposed_Graph_Convolutional_Networks_for_Skeleton-Based_Action_Recognition_ICCV_2023_paper.html
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Hierarchically Decomposed Graph Convolutional Networks for Skeleton-Based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了传统骨架图无法直接沟通身体两侧对称末端关节、而纯注意力全连接图又丢失物理层次结构的矛盾，且无需使用噪声较大的关节/骨骼运动差分流即可登顶四大基准。

**留下的局限**：单块内同时包含固定/可学习子集图卷积、特征欧氏距离动态 $k$-NN（`S-EdgeConv` 与 `H-EdgeConv`）、时序 `MaxPool`、`Sigmoid` 门控以及多尺度时序 `3×1 MaxPool`，算子异构度高，直接全网免训练转换需同时解决动态 $k$-NN、`MaxPool` 与 `Sigmoid` 三道关卡。

**是否需要训练或微调**：是（浮点教师端到端训练 90 轮）

**涉及的算子**：有根树层次分解全连接图（`HD-Graph`）、特征欧氏距离动态 $k$-NN 边卷积（`S-EdgeConv` / `H-EdgeConv`）、注意力引导层次聚合 `A-HA`（含时序 `MaxPool_T`、代表节点均值池化 `RSAP` 与 `Sigmoid` 门控）、多尺度时序卷积（含 `3×1 MaxPool`）、`BatchNorm2d`、`ReLU`

**关键数字**：单流 Joint 模型在 `NTU-RGB+D 120` X-Sub / X-Set 达 **85.7% / 87.3%**（仅 1.60 GFLOPs、1.68M 参数，Table 4，第 8 页）；6 路集成（3 种质心树 × 关节/骨骼双流，Table 1，第 7 页）：`NTU-RGB+D 60` X-Sub / X-View **93.4% / 97.2%**，`NTU-RGB+D 120` X-Sub / X-Set **90.1% / 91.6%**，`Kinetics-Skeleton` Top-1 / Top-5 **40.9% / 63.5%**，`NW-UCLA` **97.2%**。

> 💭
> **与本方向的关系（判断）**：直接相关（拥有 `MIT` 协议与官方公开预训练权重的强骨架教师；非常适合用来测试含动态 `EdgeConv` 的现代混合骨架 GNN 在免训练转换下的行为）

### <a id="41b0e334-2e6f-8171-8777-d5415a273e78"></a>ViHGNN 与 Pyramid ViHGNN（2023）

- **发表处：** Proceedings of the IEEE/CVF International Conference on Computer Vision（ICCV 2023，pp. 19878–19888）
- **脉络：** 3 视觉图骨干
- **作者：** Yan Han, Peihao Wang, Souvik Kundu, Ying Ding, Zhangyang Wang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#vihgnn-与-pyramid-vihgnn2023
- **代码：** [https://github.com/VITA-Group/ViHGNN](https://github.com/VITA-Group/ViHGNN)
- **年份：** 2023
- **一句话：** 把 `ViG` 的成对边图推广为允许一条超边同时连接多个图像块的视觉超图网络（ViHGNN），用模糊 C 均值聚类动态生成超边并执行“节点→超边→节点”两步高阶消息传递。
- **链接：** https://openaccess.thecvf.com/content/ICCV2023/html/Han_Vision_HGNN_An_Image_is_More_than_a_Graph_of_ICCV_2023_paper.html
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Vision HGNN: An Image is More than a Graph of Nodes
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：突破了普通图每条边只能刻画两个图像块二元关系的限制，用高阶超边建模多区域语义共现并缓解深层过平滑。

**留下的局限**：（1）**官方仓库未发布任何预训练权重**；（2）**核查发现论文与官方代码存在显著不一致**：论文 Tables 1–2（第 5 页）写明超边数 $E=50$ 且 Eq. 1 采用度矩阵归一化与可学习超边对角权重 $\mathbf{W}$，但官方仓库 `pyramid_vihg.py:215` 实际设置聚类簇数 `k=25`，且 `torch_vertex.py:88-133` 用的是无权 `torch.mean` 聚合加 $(1+\epsilon)x$ 残差；（3）每层在线迭代模糊 C 均值（FCM）聚类对免训练脉冲转换极不友好。

**是否需要训练或微调**：是（ImageNet-1K 上训练 300 轮）

**涉及的算子**：动态模糊 C 均值（FCM）超图构建、节点到超边与超边到节点两步均值/加权聚合、`ConvFFN`、`BatchNorm2d`、`GELU`

**关键数字**：`ImageNet-1K` Top-1 精度：各向同性 `ViHGNN-Ti/S/B` 达 **74.3% / 81.5% / 82.9%**（Table 4，第 6 页）；金字塔 `Pyramid ViHGNN-Ti/S/M/B` 达 **78.9% / 82.5% / 83.4% / 83.9%**（较同规模 `Pyramid ViG` 分别高 +0.7% / +0.4% / +0.3% / +0.2%，Table 5，第 6 页）；`MS COCO` Mask R-CNN `PViHGNN-S` 达 **43.1** $\text{AP}^b$ / **39.8** $\text{AP}^m$（Table 11，第 8 页）。

> 💭
> **与本方向的关系（判断）**：背景（ViG 家族超图分支代表作；由于无官方预训练权重且代码与论文超参数冲突，不宜选作免训练转换的首发教师）

### <a id="41b0e334-2e6f-8174-8ed9-d8b84b2d24e2"></a>DAGr（2024）

- **发表处：** Nature（2024，Vol. 629，pp. 1034–1040，DOI: `10.1038/s41586-024-07409-w`）
- **脉络：** 3 视觉图骨干,4 事件驱动与增量推理
- **作者：** Daniel Gehrig, Davide Scaramuzza
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#dagr2024
- **代码：** [https://github.com/uzh-rpg/dagr](https://github.com/uzh-rpg/dagr) （预训练权重：[https://download.ifi.uzh.ch/rpg/dagr/data/dagr_s_50.pth](https://download.ifi.uzh.ch/rpg/dagr/data/dagr_s_50.pth) ）
- **年份：** 2024
- **一句话：** 将事件相机微秒级异步事件流构建为有向时空半径图，结合查表样条图卷积、有向体素最大池化剪枝与低频 RGB 特征融合，在车载场景实现亚毫秒级超低延迟目标检测。
- **链接：** https://www.nature.com/articles/s41586-024-07409-w
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Low-latency automotive vision with event cameras
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

##### 来自脉络 3 视觉图骨干 的记录

**解决的难点**：攻克了初代 `AEGNN` 无向图消息向过去事件回传导致 $k$-hop 子图随层数急剧膨胀的问题——通过只让旧事件指向新事件（$t_i<t_j$）并在体素 `max` 池化处截断未改变最大值的更新，削减了 **91%** 的异步图更新计算量。

**留下的局限**：整个网络仍是运行在 GPU 上的**连续浮点激活图网络**而非脉冲神经元网络；官方仓库采用传染性较强的 `**GPL-3.0**` 许可证，且公开预训练权重 `dagr_s_50.pth` 绑定了双流 `ResNet-50` RGB 分支与 `YOLOX` 检测头。

**是否需要训练或微调**：是（在批量同步事件图上端到端训练浮点权重，测试时等价部署为逐事件异步流式更新）

**涉及的算子**：有向时空半径建图（$\|n_p^i-n_p^j\|_\infty < 0.01, t_i<t_j$，上限 16 邻居）、查表一阶 B 样条卷积 `LUT-SplineConv`（邻居 `add` 求和）、有向时空体素簇 `max` 池化（前 3 级 `max`、第 4 级 `mean`）及更新截断、`ELU`、`SiLU`、`BatchNorm`

**关键数字**：`DSEC-Detection` 车载事件+图像检测（Table 1）：`DAGr-S + ResNet-50` 达 **41.9** mAP（单事件能耗 **5.42 µJ/event**），`DAGr-S + ResNet-18` 达 **37.6** mAP；纯事件 `Gen1` 检测（Table 2）：`DAGr-L` 达 **32.1** mAP，`DAGr-N` 仅需 **1.36 MFLOPs/event** 与 **1.93 µJ/event**；`N-Caltech101` 检测 `DAGr-S / L` 达 **70.2 / 73.2** mAP；早期体素 `max` 池化自然拦截了 **73%** 的冗余下游传播，有向建图+有向池化合计减少 **91%** 算力（Main Text & Fig. 4）。

> 💭
> **与本方向的关系（判断）**：直接相关（既是事件相机图检测标杆教师，又在硬件实测层面证明了“`max` 池化天然抑制小幅更新扩散”这一核心现象，同时可作为脉络四增量推理的重要先驱）

##### 来自脉络 4 事件驱动与增量推理 的记录

**标题**：Low-latency automotive vision with event cameras

**作者**：Daniel Gehrig, Davide Scaramuzza

**发表处**：Nature（2024，Vol. 629，pp. 1034–1040）

**链接**：[https://doi.org/10.1038/s41586-024-07409-w](https://doi.org/10.1038/s41586-024-07409-w) ；代码：[https://github.com/uzh-rpg/dagr](https://github.com/uzh-rpg/dagr)

**核对深度**：全文（PMC 开放全文 PMC11136662）

**一句话**：事件建成有向时空图、配合低帧率图像 CNN 做检测；新事件到来时只更新必要节点，并在 max 池化处截断“最大值没变”的更新。

**解决的难点**：AEGNN 的无向图让更新向过去事件回传、逐层膨胀；DAGr 只让旧事件指向新事件，再利用 max 池化的选择性截断，把异步更新计算量削减 91%（详见脉络三 DAGr 条目）。

**留下的局限**：截断是“max 结果没变”这种精确条件，不是阈值；浮点激活，不是脉冲网络；双向时空依赖的固定节点图不能直接套用。

**是否需要训练或微调**：是

**涉及的算子**：有向半径建图、样条卷积、体素 max 池化、ELU、BatchNorm

**关键数字**：体素 max 池化拦截约 73% 的下游更新，有向建图加池化合计减少 91% 计算（正文与 Fig. 4，数字与脉络三一致）。

> 💭
> **与本方向的关系（判断）**：直接相关

### <a id="41b0e334-2e6f-819b-9adf-fe7b06407196"></a>Point Transformer V3 / PTv3（2024）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2024，pp. 4840–4851；预印本 `arXiv:2312.10035`）
- **脉络：** 3 视觉图骨干
- **作者：** Xiaoyang Wu, Li Jiang, Peng-Shuai Wang, Zhijian Liu, Xihui Liu, Yu Qiao, Wanli Ouyang, Tong He, Hengshuang Zhao
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#point-transformer-v3--ptv32024
- **代码：** [https://github.com/Pointcept/PointTransformerV3](https://github.com/Pointcept/PointTransformerV3) （预训练权重：[https://huggingface.co/Pointcept/PointTransformerV3](https://huggingface.co/Pointcept/PointTransformerV3) ）
- **年份：** 2024
- **一句话：** 彻底抛弃占点云 Transformer 前向耗时 28% 的精确 $k$-NN 搜索与 26% 的相对位置编码，改用 Z 序与希尔伯特空间填充曲线把无序三维点云序列化为一维定长块做点积自注意力，换取 3.3 倍提速、10.2 倍省显存及 20 余项三维任务全面刷榜。
- **链接：** https://arxiv.org/abs/2312.10035
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Point Transformer V3: Simpler, Faster, Stronger
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打破了点云骨干因执着于严格置换不变性与精确 $k$-NN 检索而无法扩大感受野（从 16 点扩至 1024 点）和模型规模的效率瓶颈。

**留下的局限**：实质上已从“图消息传递网络”转向“空间填充曲线分块窗口 Transformer + 3D 稀疏卷积 `xCPE` + 网格 `MaxPool`”，因此若对其做脉冲转换，主要检验的是脉冲 `Softmax` 点积注意力与 `LayerNorm`（而非动态图转换）；且源码许可证为非商业 `CC BY-NC 4.0`。

**是否需要训练或微调**：是（单数据集从头训练或多数据集 `PPT` 协同预训练）

**涉及的算子**：Z-order / Hilbert 空间填充曲线位编码排序与轮换打乱（`Shift/Shuffle Order`）、1024 点非重叠块多头点积注意力（`Softmax`）、前置 3D 稀疏卷积 `xCPE`、`LayerNorm`、`GELU`、`Grid Pooling`（含 `BatchNorm` 与 `MaxPool`）

**关键数字**：效率（Table 1，第 3 页，`nuScenes` 单卡 RTX 4090）：46.2M 参数下推理延迟 **44ms**、显存 **1.2G**（较 `PTv2` 提速 **3.3×**、显存降 **10.2×**）；室内语义分割（Table 5，第 7 页，从头训 / PPT 联训）：`ScanNet v2` Test **77.9% / 79.4%** mIoU，`ScanNet200` Test **37.8% / 39.3%** mIoU，`S3DIS` Area5 **73.4% / 74.7%**、6-fold **77.7% / 80.8%** mIoU；室外分割（Table 7）：`nuScenes` Test **82.7% / 83.0%** mIoU，`SemanticKITTI` Test **74.2% / 75.5%** mIoU。

> 💭
> **与本方向的关系（判断）**：可借用的技术（其“用空间填充曲线一维定长分块彻底消除动态 $k$-NN 搜索”的设计，为规避脉冲网络在线排序选邻居提供了极有启发性的结构替代思路）

### <a id="41b0e334-2e6f-81a1-b1af-ef104349bc8c"></a>MobileViGv2（2024）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops（CVPRW 2024，Mobile AI Workshop；预印本 `arXiv:2406.05850`）
- **脉络：** 3 视觉图骨干
- **作者：** William Avery, Mustafa Munir, Radu Marculescu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/03-vision-graph-backbones.md#mobilevigv22024
- **代码：** [https://github.com/SLDGroup/MobileViGv2](https://github.com/SLDGroup/MobileViGv2) （预训练权重：[https://huggingface.co/SLDGroup/MobileViGv2/tree/main](https://huggingface.co/SLDGroup/MobileViGv2/tree/main) ）
- **年份：** 2024
- **一句话：** 设计极简的移动端图卷积 `MGC`，在第 2–4 阶段只让每个像素固定连接自身与上下左右固定步幅的 4 个十字邻居，并用通道拼接加分组投影取代逐元素 `max` 聚合。
- **链接：** https://arxiv.org/abs/2406.05850
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Scaling Graph Convolutions for Mobile Vision
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了初代 `MobileViG` 在高分辨率阶段轴向连接过多导致延迟飙升、只能在第 4 阶段用图层的缺陷。

**留下的局限**：图结构退化为固定空洞十字模板卷积，已不含动态建图或 `max` 聚合，因此在方法论上只能充当“无动态建图、无 `max` 聚合”的消融下界对照，不能单独代表一般视觉图转换的难点。

**是否需要训练或微调**：是（浮点教师使用 `RegNetY-16GF` 蒸馏训练）

**涉及的算子**：静态五点十字图卷积 `MGC`（步幅 $K=[0,8,4,2]$，上下左右 4 邻居相对差 $x_j-x_i$ 拼接线性映射）、重参数化条件位置编码 `RepCPE`、`MBConv`、`BatchNorm2d`、`GELU`

**关键数字**：`ImageNet-1K` Top-1 精度（Table 1，第 5 页）：`MobileViGv2-Ti/S/M/B` 分别达 **77.7% / 79.8% / 81.7% / 83.4%**（iPhone 13 Mini NPU 延迟 **0.79 / 1.00 / 1.49 / 2.38 ms**）；`MS COCO` Mask R-CNN `M/B` 达 **42.5 / 43.0** $\text{AP}^{box}$，`ADE20K` Semantic FPN 达 **42.9% / 44.3%** mIoU（Table 2，第 6 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（`Apache-2.0` 协议宽松且 HuggingFace 权重齐全，是剥离“动态 $k$-NN 误差”与“`max` 聚合误差”的理想干净对照组教师）

### <a id="41b0e334-2e6f-811f-bf69-f7b9c5c48dda"></a>Davidson & Furber（2021）

- **发表处：** Frontiers in Neuroscience，vol. 15, Article 651141, April 2021（DOI: `10.3389/fnins.2021.651141`）
- **脉络：** 5 能耗与硬件
- **作者：** Simon Davidson, Steve B. Furber
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#davidson--furber2021
- **代码：** 未公开
- **年份：** 2021
- **一句话：** 用 TSMC 22FDX（SpiNNaker 2 同款工艺）版图后实测电路能耗对率编码转换 SNN 与数字 ANN 做逐神经元对比，推导出**转换后的 SNN 只有在每个神经元每次推理平均发放脉冲数少于 **`**1.72**`** 个时才能比同结构数字 ANN 省电**。
- **链接：** https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2021.651141/full
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Comparison of Artificial and Spiking Neural Networks on Digital Hardware
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：最早用 22nm 真实版图后 SRAM 与乘加器焦耳数刺破了“率编码 ANN→SNN 转换天然省电”的泡沫——指出在 22nm 数字电路里，读一次 32 位本地 SRAM（`296 fJ`）与做一次 32+8×8 乘加（`293 fJ`）能耗几乎相等，SNN 每来一个脉冲都要读/改/写状态 SRAM，多次发放会迅速亏本。

**留下的局限**：分析局限于单神经元率编码脉冲计数（未考虑多位分级脉冲一次传完信息），且假设权重读取在多神经元间完全分摊或对等。

**是否需要训练或微调**：否（基于转换型率编码 SNN 的数字电路能耗理论分析）

**涉及的算子**：率编码 IF 脉冲神经元、8-bit×8-bit+32-bit 整数 MAC、32-bit 加法器、2K-word 本地 SRAM 读写

**关键数字**：基于 **TSMC 22FDX 版图后实测数据**（Section 4, p. 5）：从 2K×32b SRAM 读一个 32 位字耗能 `**296 fJ**`（记为 `5E`），一次 32 位累加 + 8×8 位乘加耗能 `**293 fJ**`（亦约为 `5E`），纯 32 位加法约 `**60 fJ**`（记为 `E`），SRAM 写回约 `E`。据此算得每连接每神经元更新成本：ANN 为 $5E + 5E + E + E = 12E$，SNN 每处理一个脉冲为 $5E + E + E = 7E$（Eqs. 1–2, p. 5）。因此 SNN 比 ANN 省电的临界条件是**每神经元平均发放脉冲数 **$N_{\text{meanSpikes}} < 12E / 7E \approx 1.72$（Section 4, p. 5）！文中实测 MNIST 转换 CNN 首层在全 0 输入背景外很容易超过该阈值，改用信息更紧凑的编码可将脉冲数压低 `75%` 以上。

> 💭
> **与本方向的关系（判断）**：直接相关（`1.72` 脉冲/神经元的硬门槛直接解释了为什么传统几百步率编码转换在硬件上必败，而本方向采用的 $T=2,4$ 差分多阈值转换恰好能把平均事件数压进 `< 1.72` 的盈利区间！）

### <a id="41b0e334-2e6f-8133-95c7-e1fa23bb12ef"></a>Degree-Quant（2021）

- **发表处：** 9th International Conference on Learning Representations（ICLR 2021）（预印本 `arXiv:2008.05000v3`）
- **脉络：** 5 能耗与硬件
- **作者：** Shyam A. Tailor, Javier Fernandez-Marques, Nicholas D. Lane
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#degree-quant2021
- **代码：** [https://github.com/camlsys/degree-quant](https://github.com/camlsys/degree-quant)
- **年份：** 2021
- **一句话：** 图神经网络低比特量化领域的奠基论文，揭示了 GNN 直接做 INT8/INT4 量化崩溃的病根在于**邻域聚合阶段高度数（high in-degree）节点的幅值离群扩张**，并提出按节点入度随机保护全精度前向/梯度的量化感知训练（QAT）方案。
- **链接：** https://arxiv.org/abs/2008.05000
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Degree-Quant: Quantization-Aware Training for Graph Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：精准定位了为什么 CNN 上管用的标准量化搬到 GCN / GIN / GAT 上会严重掉点——图聚合把多达上百个邻居的特征相加，高度数节点的聚合值远大于低度节点，拉宽全局量化步长，导致占绝大多数的低度节点丧失分辨率（Section 3, pp. 3–4）。

**留下的局限**：**必须从头做量化感知训练（QAT），完全不是免训练 PTQ**！文中配套测了朴素训练后量化基线，在 INT4 下几乎彻底失效；且在大图上训练极慢（据 TopGQ 实测在 Reddit 上慢 330 倍，在 2.4 亿节点 MAG240M 上需 37.5 天）。

**是否需要训练或微调**：是（完整量化感知训练 QAT，训练中按节点度数伯努利采样保护掩码并用 0.1% 分位数截断跟踪量化范围，Section 4, pp. 4–6）

**涉及的算子**：`sum` / 加权邻域聚合（GCN、GIN、GAT）、INT8 / INT4 均匀伪量化、百分位激活截断（Percentile Tracking）

**关键数字**：（1）精度表现（Tables 1–2, pp. 7–8）：在 Cora、CiteSeer、ZINC、CIFAR10 超像素图、MNIST 超像素图及 Reddit 上，INT8-DQ 基本追平 FP32（例如 CIFAR10 超像素图 **GAT FP32 **`**65.4%**`** → INT8-DQ **`**66.6%**`**、INT4-DQ **`**56.2%**`；**GCN FP32 **`**56.3%**`** → INT8-DQ **`**56.6%**`**、INT4-DQ **`**51.8%**`；ZINC 分子图 GIN MAE：FP32 `0.356` → INT8-DQ `0.357`、INT4-DQ `0.431`，而普通 QAT-STE INT4 崩至 `1.388`）；（2）推理加速：CPU 上 INT8 获得最高 `**4.7×**` 加速（Reddit GraphSAGE 为 `4.2×`，Section 5.3, p. 8）。

> 💭
> **与本方向的关系（判断）**：直接相关（其发现的“节点入度差异导致聚合输出动态范围失衡”与 ANN→SNN 转换中高度数节点膜电位饱和/低度节点欠发放完全同构！同时说明不能把需要重训的 Degree-Quant 当免训练对照，免训练对照应选均匀 PTQ 与 TopGQ）

### <a id="41b0e334-2e6f-8159-b316-d791d77137e8"></a>Ottati 等：To Spike or Not To Spike（2023）

- **发表处：** IEEE Journal on Emerging and Selected Topics in Circuits and Systems（IEEE JETCAS），vol. 13, no. 4, pp. 1015–1025, Dec. 2023（预印本 `arXiv:2306.15749v5`）
- **脉络：** 5 能耗与硬件
- **作者：** Fabrizio Ottati, Chang Gao, Qinyu Chen, Giovanni Brignone, Mario R. Casu, Jason K. Eshraghian, Luciano Lavagno
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#ottati-等to-spike-or-not-to-spike2023
- **代码：** [https://github.com/fabrizio-ottati/awesome-neuromorphic-hw](https://github.com/fabrizio-ottati/awesome-neuromorphic-hw)
- **年份：** 2023
- **一句话：** 从数字芯片设计视角对比了最先进的 ANN 与 SNN 加速器流片实测数据，明确得出**在静态图像分类上现有数字 ANN 芯片在精度—能耗—吞吐上全面帕累托占优（Pareto-dominate）SNN 芯片**，脉冲优势只可能出现在时序流或事件传感器任务及混合架构中。
- **链接：** https://arxiv.org/abs/2306.15749
- **核对人与日期：** Gemini，2026-11-16
- **标题：** To Spike or Not To Spike: A Digital Hardware Perspective on Deep Learning Acceleration
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：摒弃了模糊且忽略膜电位读写的 `SynOP/W` 指标，统一改用“每次完整推理的焦耳数（Energy/inference）”加 45nm SRAM/INT8 解析模型和 ImageNet / 语音流片芯片实测数据做横向硬核对比。

**留下的局限**：分析聚焦于卷积与循环网络（CNN / ViT / RNN），未覆盖图神经网络加速器；其解析模型未考虑寄存器级空间复用优化。

**是否需要训练或微调**：否（硬件综述与解析能耗对比研究）

**涉及的算子**：INT8 2D 卷积、LIF 脉冲卷积、RNN / GRU / LSTM 时序单元

**关键数字**：（1）**45nm 解析卷积对比**（Section IV-A, pp. 3–4）：对 `(512, 3, 3)` 卷积窗口（8-bit 权重与状态，8KB SRAM 读 64b 耗能 `10 pJ`），单步 SNN 耗能 `13.1 nJ · γ_SNN`，单通 INT8 ANN 耗能 `24.1 nJ · γ_ANN`（单步仅省 `1.84×`），但静态图像 SNN 需乘时间步 $T$（$E_{\text{SNN}} = 13.1\text{ nJ} \cdot T \cdot \gamma_{\text{SNN}}$），只要同稀疏度下 $T \ge 2$ 即输给 INT8 ANN；（2）**ImageNet 流片芯片实测**（Table II & Fig. 1, pp. 5–6）：同在 **28nm CMOS** 下，最佳数字 SNN 芯片 SNPU'23（ResNet18，$T=16$）精度仅 `**66.8%**`、单帧能耗高达 `**2.0 mJ**`（正文精确值 `1.95 mJ/inf`），而 28nm INT8 CNN 芯片 Mo'21（ResNet50）精度 `**76.9%**`、能耗 `**1.1 mJ**`（最佳点 `0.46 mJ/inf`），5nm INT4 Transformer 芯片 Keller'23（DeiT-Base）精度 `**80.5%**`、能耗 `**1.0 mJ**`，**28nm ANN+SNN 混合芯片 C-DNN'23**（ResNet50）精度 `**77.1%**`、能耗仅 `**0.3 mJ**`**（**`**281 µJ**`**）**。

> 💭
> **与本方向的关系（判断）**：直接相关（强力支撑 Claude 草稿中的假设 H3——在静态单帧图像图上脉冲网络极难在真实数字硬件能耗上击败 INT8/INT4 量化网络，真正的突破口在流式图时间差分与混合事件架构）

### <a id="41b0e334-2e6f-81a9-8c33-f6cec4dcf4cd"></a>SENECA（2023）

- **发表处：** Frontiers in Neuroscience，vol. 17, Article 1187252, June 2023（DOI: `10.3389/fnins.2023.1187252`）
- **脉络：** 5 能耗与硬件
- **作者：** Guangzhi Tang, Kanishkan Vadivel, Yingfu Xu, Refik Bilgic, Kevin Shidqi, Paul Detterer, Stefano Traferro, Mario Konijnenburg, Manolis Sifalakis, Gert-Jan van Schaik, Amirreza Yousefzadeh
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#seneca2023
- **代码：** 学术申请获取（未公开仓库）
- **年份：** 2023
- **一句话：** Imec 研制的 GF-22nm 全数字可编程类脑处理器（RISC-V + 微码循环缓冲器 + 8 个 SIMD 神经处理单元），**原生支持 4/8/16-bit 分级脉冲与 **`**MAX/MIN**`** 比较指令**，并用实测数据证明：**把 16-bit 分级脉冲换成二值脉冲仅省电 6.1%，而通过脉冲分组复用膜电位能省电 47.0%**！
- **链接：** https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1187252/full
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SENECA: building a fully digital neuromorphic processor, design trade-offs and challenges
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了传统类脑芯片“专用硬连线太死板、纯嵌入式核控制开销又大十倍”的两难——用轻量 RISC-V 做每脉冲级（`<1%` 算量）地址计算与压缩，用比 RISC-V 省电 100 倍的 Loop Buffer 驱动 8 个 NPE 执行每突触级运算，并系统对比了 11 款主流类脑芯片的架构参数。

**留下的局限**：片上多播路由表较小，遇到百万级完全随机无结构连接时需退回单播模式（Section 2.4 & 3.5, pp. 7, 10–11）；目前仅给出单核 RTL 级（Cadence JOULES，距签核功率误差 15% 内）算子与单层基准测试，未跑完整视觉图网络。

**是否需要训练或微调**：否（通用可编程数字类脑硬件，支持事件驱动全连接、卷积与在线学习 e-prop）

**涉及的算子**：**分级脉冲（Graded Spikes，带可选数值载荷）**、二值脉冲、4/8/16-bit 线性与浮点（FP16/BF16）算术指令（`ADD/SUB/MUL`）、**硬件比较与极值指令（**`**GTH/MAX/MIN**`**）**、脉冲分组（Spike-grouping）

**关键数字**：（1）**芯片规格**（GF-22nm FDX，`0.8V, 500MHz`，Table 1, 6, 7, pp. 5, 10, 12）：单核面积 `**0.47 mm²**`（其中 `2 Mb` 数据 SRAM 占 **70%** 面积，8 个 NPE 仅占 `1.3%`，RISC-V 占 `2.3%`），静态漏电 `30 µW`；NPE 寄存器访问（`8–12 fJ/b`）比片上 SRAM（`180–220 fJ/b`）省电约 **20 倍**（Table 2 & Sec. 3.2, pp. 5, 9）；（2）**单指令能耗拆解**（Table 8, p. 13）：FP16 `ADD/SUB/MUL` 总能耗 `**1.4 pJ**`（纯 ALU 仅 `0.5 pJ`），2×INT8 算术 `**1.2 pJ**`，FP16 `GTH/MAX/MIN` `**1.2 pJ**`，而单次 16b 数据 SRAM 读/写高达 `**3.7 pJ**`** / **`**3.9 pJ**`；（3）**分级脉冲 vs 二值脉冲关键实测**（4000 神经元全连接层处理 16 输入脉冲、64k SOPs，Table 9, p. 15）：16-bit 分级脉冲基线总能耗 `908.8 nJ`（`**14.2 pJ/SOp**`）；改成二值脉冲（省去乘法但仍读写 16b 权重状态）总能耗 `853.1 nJ`（`**13.3 pJ/SOp**`**，仅省电 **`**6.1%**`！）；而保留分级脉冲、仅将 4 个脉冲分组复用寄存器内膜电位（Spike-grouping）即降至 `481.9 nJ`（`**7.5 pJ/SOp**`**，省电 **`**47.0%**`）；结合二值脉冲 + 4b 权重/8b 状态量化 + 脉冲分组可降至 `**2.7 pJ/SOp**`（省电 `80.7%`）。

> 💭
> **与本方向的关系（判断）**：直接相关（为本项目使用**多阈值/分级脉冲（如 DCGS）和硬件 **`**MAX**`** 指令**提供了极其硬核的电路级依据：在真实 22nm 类脑核上，分级脉冲带来的乘法器额外功耗不到 7%，真正决定能耗的是事件稀疏度、低位宽权重以及状态访存复用！）

### <a id="41b0e334-2e6f-81b3-843f-e11ec01ca648"></a>Lemaire 等：SNN 与 FNN 解析能耗模型（2022）

- **发表处：** 29th International Conference on Neural Information Processing（ICONIP 2022），Part I, LNCS vol. 13623, pp. 577–587（预印本 `arXiv:2210.13107v1`）
- **脉络：** 5 能耗与硬件
- **作者：** Edgar Lemaire, Loïc Cordone, Andrea Castagnetti, Evgeny Novakovsky, Jean-François Rousseau, Benoît Miramond
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#lemaire-等snn-与-fnn-解析能耗模型2022
- **代码：** 未公开
- **年份：** 2022
- **一句话：** 基于 Horowitz 45nm INT32 与 SRAM 插值参数建立与具体芯片解耦的解析模型，指出 **SNN 总能耗中超过 98% 来自存储器访问**，且 SNN 只有在层间用微型脉冲 FIFO 替代完整特征图缓存时才比前馈网络省电 6–8 倍。
- **链接：** https://arxiv.org/abs/2210.13107
- **核对人与日期：** Gemini，2026-11-16
- **标题：** An Analytical Estimation of Spiking Neural Networks Energy Efficiency
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把神经元参数存储、状态读写、层间特征图/FIFO 缓冲与寻址计算全部纳入解析公式（Eqs. 1–20, pp. 3–5），纠正了忽略片上存储容量差异的纯算术对比。

**留下的局限**：（1）模型设定偏袒 SNN 的层间存储假设——假设前馈 ANN 必须把整张高精度特征图存在大容量 SRAM 中，而 SNN 只需 1000 深度的微型脉冲 FIFO（若 ANN 采用深度优先或分块缓存、或 SNN 需跨步缓存膜电位，比值会大幅改写）；（2）算术采用 INT32（乘法 `3.1 pJ`、加法 `0.1 pJ`）而非现代加速器常用的 INT8/INT4；（3）在静态图像 CIFAR-10 上为压低时间步（$T=4$），SNN 精度比 FNN 暴跌 6.7 个百分点（`95.1% → 88.4%`），并非等精度比较！

**是否需要训练或微调**：否（解析能耗评估模型，评测用 SNN 采用替代梯度直接训练）

**涉及的算子**：卷积层、全连接层、LIF 脉冲神经元、SRAM 容量对数线性插值访存模型

**关键数字**：采用 Horowitz 45nm INT32 参数与 SRAM 对数插值（Eq. 1, p. 3）：（1）CIFAR-10 VGG-16（$T=4$，平均每神经元发放 `0.10` 脉冲，Table I–II, pp. 6–7）：FNN 能耗 `1.30e7 nJ`（精度 `95.1%`），SNN 能耗 `1.58e6 nJ`（精度仅 `**88.4%**`），名义比值 `8.19×`，其中 **SNN 访存能耗占比高达 **`**99.9%**`** 以上**（`1.58e6 nJ` 访存 vs `4.34e2 nJ` 计算，Table II, p. 7）；（2）Google Speech Commands 语音（$T=2$）：FNN `93.6%` vs SNN `91.8%`，能耗比 `6.22×`；（3）**Prophesee NCARS 事件相机分类**（$T=5$，发放率 `0.08`）：SNN 精度反超（`**93.5%**`** vs **`**93.4%**`）且能耗比达 `**8.17×**`（Table I–II, pp. 6–7）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（一方面再次证实静态图低 $T$ 易掉点、事件相机数据最契合 SNN；另一方面其“访存占 >98% 能耗”的结论提醒我们图邻接访存建模不可省略）

### <a id="41b0e334-2e6f-81c7-b38a-f78861cdd8ac"></a>Loihi 2（2021）

- **发表处：** 2021 IEEE Workshop on Signal Processing Systems（SiPS 2021），pp. 254–259（DOI: `10.1109/SiPS52927.2021.00053`；预印本 `arXiv:2111.03746v1`）
- **脉络：** 5 能耗与硬件
- **作者：** Garrick Orchard, E. Paxon Frady, Daniel Ben Day Rubin, Sophia Sanborn, Sumit Bam Shrestha, Friedrich T. Sommer, Mike Davies
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#loihi-22021
- **代码：** [https://github.com/lava-nc/lava（Intel](https://github.com/lava-nc/lava（Intel) Lava 软件栈）
- **年份：** 2021
- **一句话：** Intel 第二代异步类脑芯片 Loihi 2（Intel 4 工艺）的官方信号处理论文，明确引入了**可编程神经元微码与最高 32-bit 分级脉冲（graded spikes）**，大幅压缩了高动态范围信号处理所需的脉冲数和时间步。
- **链接：** https://arxiv.org/abs/2111.03746
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Efficient Neuromorphic Signal Processing with Loihi 2
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了第一代 Loihi 只能传二值脉冲且神经元固定为 CUBA LIF 导致逼近连续值需要几百步、延迟高的问题——允许神经元通过汇编微码自定义内部状态方程，并在触发时发出携带最多 32 位整数载荷的分级脉冲直接参与突触乘加。

**留下的局限**：芯片硬件不对外零售（仅对 Intel INRC 研究社区开放）；动态重连图边（如逐层动态 $k$NN）不符合其预设静态突触路由表范式。

**是否需要训练或微调**：否（硬件架构与算法映射，支持免训练转换或直接编程的脉冲算法）

**涉及的算子**：**最高 32-bit 分级脉冲（Graded Spikes）**、可编程微码神经元（如谐振发放 Resonate-and-Fire、Sigma-Delta 神经元）、卷积连接权值共享、三维网格异步路由

**关键数字**：采用 Intel 4 工艺（据 SENECA Table 1, p. 5 核实单核面积 `0.21 mm²`、每核 `1.5 Mb` 存储，单芯片 128 核），**原生支持最高 32-bit 分级脉冲载荷**（Section II, p. 2 右栏）；在短时傅里叶变换（STFT）近似语音谱特征任务上，相比 CPU 实现能耗降低超过 `**100×**`，带宽压缩 `**27×**`（Section IV, pp. 4–5）。

> 💭
> **与本方向的关系（判断）**：直接相关（分级脉冲与差分神经元（Sigma-Delta / 多阈值）在工业界标杆类脑芯片上具备原生硬件指令支持的头号证据）

### <a id="41b0e334-2e6f-81ca-aa3d-c333eeeecf4b"></a>SpiNNaker 2（2024）

- **发表处：** 37th NeurIPS Workshop on Machine Learning with New Compute Paradigms（MLNPCP @ NeurIPS 2023），预印本发布于 2024 年 1 月（`arXiv:2401.04491v1`）
- **脉络：** 5 能耗与硬件
- **作者：** Hector A. Gonzalez, Jiaxin Huang, Florian Kelber, Khaleelulla Khan Nazeer, Tim Langer, Chen Liu, Matthias Lohrmann, Amirhossein Rostami, Mark Schöne, Bernhard Vogginger, Timo C. Wunderlich, Yexin Yan, Mahmoud Akl, Christian Mayr
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#spinnaker-22024
- **代码：** [https://doi.org/10.5281/zenodo.10202110（](https://doi.org/10.5281/zenodo.10202110（)`py-spinnaker2`）
- **年份：** 2024
- **一句话：** 介绍了采用 22nm FDX 工艺量产的数字异步类脑芯片 SpiNNaker 2（单芯片 152 个 ARM 核 + 硬件 MAC 阵列），原生支持最高 **128-bit 载荷的事件数据包**和分级事件神经网络（如 EGRU）。
- **链接：** https://arxiv.org/abs/2401.04491
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SpiNNaker2: A Large-Scale Neuromorphic System for Event-Based and Asynchronous Machine Learning
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打破了传统类脑芯片只能传 1-bit 二值脉冲且不支持矩阵乘加速的限制——每个处理单元（PE）既能通过中断驱动异步处理稀疏脉冲，又内置 8-bit/16-bit 整数矩阵乘与卷积加速器，路由包可携带多位分级激活值或反向误差梯度。

**留下的局限**：单 PE 本地 SRAM 仅 `128 kB`（需靠片上 DMA 与 `2 GB` 片外 LPDDR4 协同调度大模型），若图拓扑动态变化，预编译静态路由表（Section 3.2, p. 5）难以在运行期低开销重配。

**是否需要训练或微调**：否（硬件平台，可直接部署转换后的 SNN、EGRU 或普通量化 DNN，Section 3.2–3.3, p. 5）

**涉及的算子**：任意可编程脉冲/事件神经元（IF / LIF / EGRU）、最高 128-bit 载荷多播事件包、8-bit/16-bit 整数矩阵乘（MAC Array）与 2D 卷积、硬件指数/对数与随机数加速

**关键数字**：GlobalFoundries 22nm FDX 工艺（已量产超 3.5 万颗芯片组成 500 万核系统，Section 1–2, p. 2；据 SENECA Table 1 & 3, pp. 5–6 交叉核实单核面积 `1.09 mm²`、约 `10 pJ/SOp`）；单芯片含 **152 个 ARM Cortex-M4F PE**，每 PE 配 `**128 kB**`** SRAM**，芯片配 `**2 GB**`** LPDDR4 DRAM** 和 6 条芯片间链路；片上/片间路由支持最高 **128-bit payload** 数据包（32-bit 神经元 ID + 多位数值载荷，Section 2, p. 2 & Section 3.3.2, p. 6）；在 DVS Gesture 手势识别（128 PEs 部署 2 层分级事件网络 EGRU）上，batch=1 实时推理单步能耗约 `**~190 µJ/step**`，显著低于 Nvidia A100（`~950 µJ/step`）与 GTX 1070Ti（`~360 µJ/step`）（Section 3.3.1 & Fig. 3, pp. 5–6）。

> 💭
> **与本方向的关系（判断）**：直接相关（证明主流新一代数字类脑芯片已原生支持多位分级事件包与局部整数 MAC，本方向若采用多阈值/分级脉冲或局部混合算子，在硬件上完全可落地上板）

### <a id="41b0e334-2e6f-81cf-a51c-e1c5f1595304"></a>Dampfhoffer 等：硬件感知 SNN vs ANN 研究（2023）

- **发表处：** IEEE Transactions on Emerging Topics in Computational Intelligence（IEEE TETCI），vol. 7, no. 3, pp. 731–741, June 2023（DOI: `10.1109/TETCI.2022.3214509`；CEA-HAL 编号 `cea-03852141`）
- **脉络：** 5 能耗与硬件
- **作者：** Manon Dampfhoffer, Thomas Mesquida, Alexandre Valentian, Lorena Anghel
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#dampfhoffer-等硬件感知-snn-vs-ann-研究2023
- **代码：** 未公开
- **年份：** 2023
- **一句话：** 以经典数字加速器 Eyeriss 的数据复用与稀疏上限为参照，证明简单 IF 神经元远比 LIF 省电，且 SNN 只有在**每个突触每次推理平均仅发放 0.15 到 1.38 个脉冲**的极高稀疏区间内才能与高效数字 ANN 抗衡。
- **链接：** https://cea.hal.science/cea-03852141
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Are SNNs Really More Energy-Efficient Than ANNs? An In-Depth Hardware-Aware Study
- **核对深度：** 仅摘要
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：量化了 ANN 侧空间/时间数据复用（如行驻留/权重驻留）以及 SNN 侧不同神经元动力学（IF vs LIF vs 连续突触模型）的状态维护开销，打破了“只要把乘加换成累加就省电”的迷思。

**留下的局限**：未获取全文 PDF 核对其具体 CMOS 工艺节点参数表；研究范围限于前馈/卷积网络，未分析图消息传递的邻域访存特征。

**是否需要训练或微调**：否（硬件感知能耗建模分析）

**涉及的算子**：IF 神经元、LIF 神经元、连续突触电流模型、Eyeriss 风格空间数据复用卷积

**关键数字**：据 HAL 官方摘要（`halId: cea-03852141`）：IF 脉冲网络要与充分利用数据复用和稀疏性的数字 ANN 实现竞争，**每次推理每突触平均脉冲数必须落在 **`**0.15–1.38 spikes/synapse/inference**`** 的稀疏窗口内**（具体取决于所对比的 ANN 硬件数据流实现）；作者据此主张在高稀疏层用事件驱动 SNN、在低稀疏层用并行 ANN 的混合架构。

> 💭
> **与本方向的关系（判断）**：直接相关（给出了极直观的“每突触每推理脉冲数 `0.15–1.38`”经验警戒线，可直接用于核验转换后视觉图模型的每标量累计事件数是否越过盈亏线）

### <a id="41b0e334-2e6f-8100-8f8e-e1e46358f201"></a>Yan 等：QNN-SNN Twin 能耗分析（2026）

- **发表处：** IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems（IEEE TCAD），2026（录用版对应 `arXiv:2409.08290v6`，首版提交于 2024 年 8 月）
- **脉络：** 5 能耗与硬件
- **作者：** Zhanglu Yan, Zhenyu Bai, Kaiwen Tang, Weng-Fai Wong
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#yan-等qnn-snn-twin-能耗分析2026
- **代码：** 未公开
- **年份：** 2026
- **一句话：** 构造了与 $T$ 步脉冲网络表达能力严格等价的 $\lceil\log_2(T+1)\rceil$ 比特量化网络（QNN-SNN Twin），从算术、膜电位读写、权重复用和片上网络路由四个维度推导出 SNN 胜过等价 QNN 的精确稀疏度盈亏线。
- **链接：** https://arxiv.org/abs/2409.08290
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Reconsidering the Energy Efficiency of Spiking Neural Networks Inference from Analytical Perspectives
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：纠正了以往 SNN 论文拿“多步二值脉冲网络”去对比“32 位全精度浮点网络”且忽略膜电位访存与稀疏路由地址开销的不公平做法，给出了闭合解析不等式和跨视觉/语言模型的轨迹级硬件实测对照。

**留下的局限**：全文只分析了全连接层、卷积层与 Transformer（VGG、RepVGG、BERT/GLUE、Spiking Llama-2），**完全未涉及图神经网络**——既没有考虑图邻接表的不规则散列访存（图上节点度呈幂律分布、权重与激活复用率与规则网格截然不同），也未讨论分级/多阈值差分脉冲（如 DCGS）与动态 $k$NN 建图开销。

**是否需要训练或微调**：否（本文为解析能耗建模与硬件轨迹评估框架）

**涉及的算子**：IF 减法复位脉冲神经元、均匀量化 ReLU（QNN Twin）、稀疏事件路由（AER NoC）与稠密广播数据流

**关键数字**：（1）**等价性定理**（Theorem 1 & Proposition 1, pp. 2–3）：带减法复位的 $T$ 步率编码 IF 网络与激活位宽 $b = \lceil\log_2(T+1)\rceil$ 的 QNN 表达能力等价，且平均发放率满足 $(1-\gamma)/T \le s_r \le 1-\gamma$（$\gamma$ 为 QNN 激活零值比例，Theorem 2, p. 3）；（2）**22nm 典型类脑工艺下的盈亏阈值**（Fig. 5, p. 6）：在 $T=5$、4-bit 权重、扇入 $N_{\text{src}}=4096$、QNN 稀疏度 $\gamma=0.8$ 时，SNN 平均发放率必须满足 $s_r < 5.7\%$（8-bit 权重时 $< 6.4\%$）才能比等价 QNN 省电；当 $s_r > 12\%\sim 17\%$ 时，稀疏事件路由（Loihi 级 `3.0 pJ/bit/hop`）甚至比稠密广播（`0.25 pJ/bit/hop`）更费电（Section II-C, p. 6）；（3）**真实模型轨迹比值 **$E_{\text{SNN}}/E_{\text{QNN}}$（Tables II–V, p. 9）：CIFAR-10 VGG16 在 $T=3$（$s_r=5.49\%$）时为 `**0.987**`（勉强持平），$T=4,5,7$ 时升至 `**1.026 / 1.406 / 2.243**`；CIFAR-100 VGG16 在 $T=3\sim 7$ 全线落败（`**1.262–2.270**`）；ImageNet RepVGG（$T=10$）为 `**2.232**`；GLUE 7 任务平均（$T=3$）为 `**1.500**`；Spiking Llama-2 7B（$T=15$）高达 `**3.793**`（逼近理论退化比 $T/\lceil\log_2(T+1)\rceil = 15/4 = 3.75$）。

> 💭
> **与本方向的关系（判断）**：直接相关（本项目“M4 图网络公平能耗盈亏分析”最核心的方法论底座）

### <a id="41b0e334-2e6f-8115-aad1-fc6e5053aad1"></a>GraphPTQ（2026）

- **发表处：** ICML 2026 Workshop on Graph Foundation Models（GFM @ ICML 2026，Oral）
- **脉络：** 5 能耗与硬件
- **作者：** Itay Niv, Neta Rabin
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#graphptq2026
- **代码：** 未核实
- **年份：** 2026
- **一句话：** 研究图模型上的训练后量化（PTQ）在显存压缩与泛化性能上的表现，是 2026 年与 TopGQ 同期出现的另一项免训练图量化探索。
- **链接：** https://icml.cc/（OpenReview
- **核对人与日期：** Gemini，2026-11-16
- **标题：** GraphPTQ: Post-Training Quantization for Graph Models, Memory Savings and Generalization
- **核对深度：** 仅摘要
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在不重新训练图模型的前提下压缩图表示与模型参数存储，考察量化对图模型泛化的影响。

**留下的局限**：因 OpenReview 受反爬限制未能读取全文 PDF，其是否覆盖动态 $k$NN 视觉图与超低比特（2–4 bit）设置尚未核实；属于静态图量化范畴而非事件驱动推理。

**是否需要训练或微调**：否（训练后量化 PTQ）

**涉及的算子**：图神经网络消息传递与训练后量化（具体算子细节未核实）

**关键数字**：ICML 2026 GFM Workshop Oral 报告；具体数据集精度与压缩比因未打开 OpenReview 正文标为“未核实”。

> 💭
> **与本方向的关系（判断）**：背景（补充证明图网络免训练 PTQ 在 2026 年正快速成为活跃子方向，做公平对照时应关注最新进展）

### <a id="41b0e334-2e6f-8118-aea0-e47aa4068b25"></a>EDA-GNN / Liu 等（2026）

- **发表处：** IEEE Transactions on Circuits and Systems I: Regular Papers（IEEE TCAS-I），vol. 73, no. 8, pp. 5542–5555, Aug. 2026
- **脉络：** 5 能耗与硬件
- **作者：** Tianhang Liu, Shen Zhang, Guangyao Yan, Runhua Wang, Rui Li, Shijie Meng, Hao Sun, Yajun Ha
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#eda-gnn--liu-等2026
- **代码：** [https://github.com/ShanghaiTechRicLab/EDA-GNN（仓库主页显示源码待正式开放）](https://github.com/ShanghaiTechRicLab/EDA-GNN（仓库主页显示源码待正式开放）)
- **年份：** 2026
- **一句话：** 针对事件相机边缘视觉设计了免显式边存储（edge-free storage）的事件队列异步图神经网络 FPGA 加速器，通过层间并行流水实现微秒级单事件实时推理。
- **链接：** https://github.com/ShanghaiTechRicLab/EDA-GNN（IEEE
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Event-Driven Asynchronous Graph Neural Network FPGA Accelerator for Real-Time Edge Vision
- **核对深度：** 仅摘要
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 未核实

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：消除了动态事件图在 FPGA 上维护显式边表带来的庞大存储开销与指针跳转延迟，用时空解耦搜索窗口内的事件队列直接完成有向单跳邻居查找与层并行更新。

**留下的局限**：与 EvGNN、ETHEREAL 相同，加速的是定点量化的事件相机 GNN 而非脉冲神经元网络；未获取闭源全文 PDF，具体 LUT/DSP 资源数与单事件能耗待获取 IEEE Xplore 原文后补全。

**是否需要训练或微调**：未核实（仅读摘要与官方仓库说明，通常需训练事件图模型并做定点量化）

**涉及的算子**：时空事件队列有向建图、无边存储图卷积、层并行流水推理

**关键数字**：发表于 IEEE TCAS-I 2026 年第 73 卷第 8 期第 5542–5555 页；在边缘 FPGA（Xilinx Zynq UltraScale+ MPSoC）与事件相机基准（如 N-CARS）上实现微秒级逐事件低延迟推理（具体精度与功耗数字因未读闭源正文标为“未核实”）。

> 💭
> **与本方向的关系（判断）**：背景（再次印证 2025–2026 年硬件界围绕事件驱动视觉图加速器的活跃投入）

### <a id="41b0e334-2e6f-8119-9cdb-ce7b2bf68c98"></a>Bhattacharjee 等：SATA 与 SpikeSim 硬件评测（2024）

- **发表处：** 2024 IEEE International Conference on Acoustics, Speech and Signal Processing（ICASSP 2024），pp. 13311–13315（DOI: `10.1109/ICASSP48485.2024.10448269`；预印本 `arXiv:2309.03388v1`）
- **脉络：** 5 能耗与硬件
- **作者：** Abhiroop Bhattacharjee, Ruokai Yin, Abhishek Moitra, Priyadarshini Panda
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#bhattacharjee-等sata-与-spikesim-硬件评测2024
- **代码：** [https://github.com/Intelligent-Computing-Lab-Yale/SATA](https://github.com/Intelligent-Computing-Lab-Yale/SATA) 及 [https://github.com/Intelligent-Computing-Lab-Yale/SpikeSim](https://github.com/Intelligent-Computing-Lab-Yale/SpikeSim)
- **年份：** 2024
- **一句话：** 用数字脉动阵列（SATA，28nm）和模拟阻变存算一体（SpikeSim，65nm RRAM）两套硬件评测工具实测主流 SNN 算法，证明论文里按 `FLOPs × T × 稀疏度` 算出的理论省电倍数比真实硬件高估了一个数量级以上。
- **链接：** https://arxiv.org/abs/2309.03388
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Are SNNs Truly Energy-efficient? — A Hardware Perspective
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：定量拆解了 SNN 落到真实芯片上的三大隐性开销：（1）跨时间步重复从片上缓存搬运权重与膜电位（稀疏性只能在 PE 内部跳过累加，片上 Buffer 读取无法跳过）；（2）LIF 神经元模块自身功耗与膜电位 SRAM 面积占比极高；（3）模拟 RRAM 交叉阵列寄生电阻与器件噪声会在多时间步上累积导致精度雪崩。

**留下的局限**：评测对象全部为 BPTT 直接训练的静态图像 CNN（VGG9、VGG16、ResNet18），未涉及免训练转换模型、多比特/分级脉冲或图神经网络的不规则访存。

**是否需要训练或微调**：部分（评测对象为预训练 BPTT SNN；文中缓解非理想性的 BN 自适应方法仅更新 BN 均值方差而无需重训权重，Section IV, p. 4）

**涉及的算子**：2D 卷积、LIF 神经元膜电位更新与复位、动态时间步早退（熵阈值 DT-SNN）、通道间共享 LIF 单元

**关键数字**：（1）**理论估算 vs 真实硬件能耗鸿沟**（CIFAR-10, 28nm CMOS，Table II, p. 2）：例如 TSSL（$T=5$，稀疏度 `90.1%`）按公式估算出 `5.8e4 nJ`（声称省电 `80×`），但在数字加速器 SATA 上实测耗能 `**3.1e7 nJ**`**（仅省电 **`**4.9×**`**）**，在 SpikeSim 上为 `1.3e5 nJ`（`16×`）；TDBN（$T=4$）公式估算省电 `83×`，SATA 实测仅 `**6.8×**`（`5.4e7 nJ`）；LTH（$T=5$）公式估算 `15×`，SATA 实测仅 `**1.3×**`；（2）**硬件瓶颈占比**（Section IV, p. 4）：在 128-PE SATA 上，LIF 神经元单元最高占计算部件总功耗的 `**61.6%**`（共享 4 通道 LIF 可降 `75.1%` LIF 功耗）；采用权重驻留的 tick-batch 数据流在 $T=4$（Tiny ImageNet VGG9）下可节省 `**62.5%**` 数据搬运能耗；动态时间步早退（平均 $T=2.14$）在 CIFAR-10 VGG9 上降低 `**46.5%**` 总能耗（Fig. 4–5, p. 4）。

> 💭
> **与本方向的关系（判断）**：直接相关（警示我们在写能耗分析时绝不能只算突触加法次数，必须把膜电位缓存与跨时间步数据搬运写进成本模型）

### <a id="41b0e334-2e6f-8198-aeea-e63b0f70abae"></a>EFGCN（2026）

- **发表处：** arXiv（`arXiv:2406.07318v3`，2026 年 6 月更新版；首版提交于 2024 年 6 月，硬件原型曾于 CVPR 2025 现场演示，pp. 5103–5104）
- **脉络：** 5 能耗与硬件
- **作者：** Kamil Jeziorek, Piotr Wzorek, Krzysztof Blachut, Andrea Pinna, Tomasz Kryjak
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#efgcn2026
- **代码：** [https://github.com/vision-agh/gcnn-dvs-fpga](https://github.com/vision-agh/gcnn-dvs-fpga)
- **年份：** 2026
- **一句话：** 在 Xilinx ZCU104 SoC FPGA 上实现了完全无需片外 DDR 的事件图卷积加速器，（论文自称）首次在硬件中引入事件流 3D MaxPool 图池化，兼顾高吞吐与低片上存储。
- **链接：** https://arxiv.org/abs/2406.07318
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Embedded Graph Convolutional Networks for Real-Time Event Data Processing on SoC FPGAs
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：指出了 EvGNN 不做图池化导致深层图节点与边数不减、计算量放大最高 50 倍且依赖片外 DDR 的缺陷（Section 2.2 & Fig. 6, pp. 5, 16）；通过“邻域矩阵有向建图 + 首层异步卷积 + `4×4×4` 3D MaxPool 降采样 + 后继层时间通道同步卷积”，把片上存储需求比 EvGNN 降低 70%，完全驻留 BRAM/URAM。

**留下的局限**：（1）依然是 **8-bit（及 6-bit）QAT 整数量化 GNN**（带 ReLU 与逐位 `max`），不是脉冲网络；（2）3D MaxPool 在时间轴分窗聚合会打断严格逐事件异步流，导致第 2–5 层退回按时间片（$\Delta T$）同步批处理（Section 4.3, p. 12）；（3）需要 100 轮浮点训练加 50 轮 QAT 微调（Section 5.1.3, p. 15）。

**是否需要训练或微调**：是（100 epochs FP32 训练 + 50 epochs QAT 量化感知训练，Section 5.1.3, p. 15）

**涉及的算子**：离散化邻域矩阵有向时空建图（半径 $R=3$，最多 29 条边）、简化版 PointNetConv（线性变换 + BN 融合 + ReLU + `max` 邻域聚合）、硬件 `4×4×4` 3D Graph MaxPool

**关键数字**：部署于 Zynq UltraScale+ ZCU104（`200 MHz`），建图瓶颈仅 15 周期/事件，峰值吞吐率达 `**13.3 MEPS**`（百万事件/秒，Section 4.1, p. 9）；8-bit 下在 N-Cars 上精度为 `**91.0%**`**（EFGCN-S）/ **`**91.9%**`**（EFGCN-B）/ **`**92.5%**`**（EFGCN-L）**，明显高于 EvGNN 的 `87.8%`，且片上存储减少 `**70%**`（Table 7 & Sec. 5.4.4, pp. 18, 20）；N-Caltech101 精度 `62.8%–64.1%`，CIFAR10-DVS `57.4%–61.5%`，MNIST-DVS `97.9%–98.7%`，端到端（PL+PS）延迟 `4.39–9.31 ms`（单事件模块级延迟 `4.02–13.76 µs`，Table 7, p. 18）；Vivado 翻转率标定功耗为 PL `1.23–1.86 W` + ARM PS `2.64 W`（合计 `3.87–4.5 W`），相比 Jetson Orin NX（10W/25W）提速 `**7.6–8.4×**`（Section 5.4.3 & Fig. 8, pp. 20, 22）。

> 💭
> **与本方向的关系（判断）**：直接相关（展示了 `max` 邻域聚合与 3D `max` 图池化在整数硬件上的高效比较器实现，同时凸显 QAT 重训成本与后层退回同步处理的局限）

### <a id="41b0e334-2e6f-81a7-af98-d25598d3a123"></a>AMPLE（2025）

- **发表处：** Proceedings of the 5th Workshop on Machine Learning and Systems（EuroMLSys '25），pp. 107–113, ACM, 2025（DOI: `10.1145/3721146.3721963`）
- **脉络：** 5 能耗与硬件
- **作者：** Pedro Gimenes, Aaron Zhao, George Constantinides
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#ample2025
- **代码：** 未公开
- **年份：** 2025
- **一句话：** 针对静态大图节点度数极度不均导致的双缓冲流水线空泡，设计了“按节点槽位异步完成事件触发调度”的混合精度（FP32 / INT8 / INT4）GNN FPGA 加速器。
- **链接：** https://doi.org/10.1145/3721146.3721963（全文
- **核对人与日期：** Gemini，2026-11-16
- **标题：** AMPLE: Event-Driven Accelerator for Mixed-Precision Inference of Graph Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：（1）传统 GNN 加速器（如 HyGCN）按批次同步双缓冲，低度节点必须干等高度数 hub 节点聚完，AMPLE 用 64 槽位节点记分牌（Node Scoreboard）实现节点完成即释放重分配的事件驱动控制流；（2）用硬件 NoC 划分子网原生支持按节点度数分配精度（高度数节点走 Float 核，其余 >97% 低度节点走 INT8/INT4 核）；（3）用多通道 HBM 预取标签（Fetch Tags）隐藏大图片外访存延迟。

**留下的局限**：（1）此处的“Event-Driven”指**硬件任务调度上的节点完成事件驱动**，而非神经元脉冲事件驱动，内部算术仍是常规浮点/定点乘加；（2）节点混合精度掩码直接照搬 Degree-Quant（需 QAT 训练）；（3）仅在 Modelsim + Vivado（Alveo U280 @ 200MHz）做延迟仿真，未报告实测板级功耗数字，也未支持 `max` 聚合或动态 $k$NN 建图。

**是否需要训练或微调**：是（依赖 Degree-Quant 的量化感知训练策略确定高精度保护节点比例，Section 2.3.1 & 4.1, pp. 3, 5）

**涉及的算子**：`sum` / `mean` 邻域聚合（GCN、GIN、GraphSAGE）、节点级混合精度（Float / INT8 / INT4）矩阵乘法、HBM 异步预取

**关键数字**：在 Xilinx Alveo U280（`200 MHz`）仿真下，跨 Cora、CiteSeer、PubMed、Flickr、Reddit、Yelp 六个图数据集（2.7K 至 71.7 万节点，高精度保护节点占比均 `< 3%`，Table 5, p. 5）及 GCN / GIN / GraphSAGE 三种模型，相比 Intel Xeon CPU 平均提速 `**243×**`，相比 NVIDIA RTX A6000 GPU 平均提速 `**7.2×**`（单层 GCN 上平均延迟 `15.2 ms`，比 CPU 快 `361.1×`、比 GPU 快 `12.9×`，Fig. 4 & Table 6, p. 6）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（揭示了图结构特有的**幂律度数长尾效应**：既导致低比特量化误差集中在 <3% 的高度数节点，又导致同步硬件出现严重等待空泡，这对分析脉冲图网络的发放率分布与硬件映射极有启发）

### <a id="41b0e334-2e6f-81d5-9105-ce3ec5d943ac"></a>TopGQ（2026）

- **发表处：** Proceedings of the 63rd ACM/IEEE Design Automation Conference（DAC '26），July 26–29, 2026, Long Beach, CA, USA, 7 pages（DOI: `10.1145/3770743.3804433`；预印本 `arXiv:2608.30394v1`）
- **脉络：** 5 能耗与硬件
- **作者：** Dain Kwon, Kanghyun Choi, Hyeyoon Lee, Sunjong Park, Seoyong Lee, Sukjin Kim, Jinho Lee
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#topgq2026
- **代码：** [https://github.com/meowrowan/TopGQ](https://github.com/meowrowan/TopGQ)
- **年份：** 2026
- **一句话：** 提出目前最强的**纯免训练图神经网络训练后量化（PTQ）**方法，把节点级量化缩放因子吸收进归一化邻接矩阵，并用一度/二度拓扑统计量零开销预测归纳式新节点的量化步长。
- **链接：** https://arxiv.org/abs/2608.30394
- **核对人与日期：** Gemini，2026-11-16
- **标题：** TopGQ: Fast GNN Post-Training Quantization Leveraging Topology Information
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了 GNN 训练后量化（W8A8 / W4A4）的两大痛点：（1）不同度数节点的激活幅值差异巨大，若逐节点设量化因子会破坏整数矩阵乘法（GEMM），TopGQ 提出*选择性双轴缩放吸收*（将节点激活缩放对角阵 $\text{diag}(S_N)$ 吸收进稀疏邻接矩阵 $\tilde{A}$，Section 4.1 Eqs. 6–8, p. 3）；（2）归纳式图任务测试时出现未见节点无法预先校准，TopGQ 提出拓扑感知对偶索引 *TopPIN*（$\text{TopPIN}(v) = (d(v), \frac{1}{d(v)}\sum_{v_k \in \mathcal{N}(v)} \frac{1}{d(v_k)})$，Section 4.2 Eq. 9, p. 4）按局部拓扑查表插值赋参。

**留下的局限**：（1）该方法面向固定图拓扑（Cora、CiteSeer、Reddit、ogbn-products、MAG240M、IMDB-BINARY、COLLAB）上的 GCN / GAT / GraphSAGE / GIN，**未评测每层按特征动态重算 **$k$**NN 图的视觉图骨干（如 ViG、DGCNN）**——在动态图中邻接矩阵每层随特征改变，无法离线预吸收进固定稀疏矩阵；（2）属于稠密单步整数推理，不利用流式图帧间时间冗余。

**是否需要训练或微调**：否（纯训练后量化 PTQ，仅需无梯度校准统计，亚秒级至分钟级完成）

**涉及的算子**：图稀疏邻接聚合（SpMM）、线性投影（INT8 / INT4 GEMM）、注意力（GAT / R-GAT）、节点度拓扑索引（TopPIN）

**关键数字**：（1）在 Reddit 数据集 GCN 上（Table 1, p. 5），TopGQ 仅耗时 **`1.88 秒`**即达到 INT8 `**94.41%**`、INT4 `**93.05%**`（FP32 基线 `94.40%`；而 QAT 方法 Degree-Quant 耗时 `10.59 分钟`仅得 `87.01%` / `64.18%`，朴素 INT4 PTQ 仅 `3.79%`，见 Table 6, p. 6）；（2）在 2.4 亿节点的超大图 MAG240M（R-GAT）上（Table 2, p. 5），TopGQ 耗时 **`58.8 分钟`**达到 INT8 `**69.14%**`（FP32 `69.66%`），而梯度校准 PTQ 方法 DRA 需 `2.06 天`（`66.13%`）、SGQuant 需 `5.50 天`（`46.76%`）、Degree-Quant 预计需 `37.5 天`；（3）部署实测（ogbn-products GCN，Table 4, p. 6）：在 RTX 4090 上获得 `**1.68×**` 端到端推理加速（`34.51s → 20.53s`），在边缘端 Jetson AGX Orin 上获得 `**1.59×**` 加速（`754.09s → 473.25s`）。

> 💭
> **与本方向的关系（判断）**：直接相关（未来做免训练 GNN→SNN 转换与非脉冲量化对照时，除朴素均匀量化外最具代表性的现代免训练 GNN PTQ 强基线）

### <a id="41b0e334-2e6f-81f4-bb32-eb27fbe69fc9"></a>DRA（2024）

- **发表处：** 2024 IEEE Nordic Circuits and Systems Conference（NorCAS 2024），DOI: `10.1109/NorCAS64408.2024.10752486`
- **脉络：** 5 能耗与硬件
- **作者：** Hadi Mousanejad Jeddi, Mahdieh Grailoo, Jose Nunez-Yanez
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#dra2024
- **代码：** 未公开
- **年份：** 2024
- **一句话：** 早期针对图卷积网络（GCN）的训练后量化（PTQ）方法，通过动态范围分析与基于梯度的迭代校准拟合 FP32 分布，无需重训主干权重。
- **链接：** https://doi.org/10.1109/NorCAS64408.2024.10752486（核实自作者官方机构页
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Leveraging Dynamic Range Analysis for Efficient Post-Training Quantization in Graph Convolutional Networks
- **核对深度：** 仅摘要
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在 TopGQ 之前尝试摆脱 Degree-Quant 的完整 QAT 重训流程，在小图（如 Cora、CiteSeer、IMDB-BINARY、COLLAB）INT8 上取得接近浮点精度。

**留下的局限**：据 TopGQ（Section 1, 6 & Table 1–2, pp. 1, 5, 6）核实，DRA 仍依赖反向梯度校准迭代且未解决跨节点度数尺度的矩阵乘吸收问题：（1）在大图上校准极慢（2.4 亿节点 MAG240M 上需 `2.06 天`，比 TopGQ 慢 50 倍以上）；（2）在大图与 INT4 低比特上严重崩溃（Reddit GCN INT4 暴跌至 `1.75%`，ogbn-products GCN INT8 跌至 `36.22%`、INT4 跌至 `3.12%`）。

**是否需要训练或微调**：部分（属 PTQ，不更新网络主干权重，但校准阶段需用梯度迭代优化量化参数）

**涉及的算子**：GCN / GraphSAGE / GIN / GAT 图消息传递、基于梯度的动态范围校准量化

**关键数字**：据 TopGQ 复现表（`topgq_2608.30394.pdf` Table 1–3, p. 5）：Cora GCN INT8 `**79.76%**` / INT4 `**77.02%**`（耗时 `1.7s`）；Reddit GCN INT8 `**93.15%**`（`42.99s`）、但 INT4 崩至 `**1.75%**`；ogbn-products GCN INT8 `**36.22%**` / INT4 `**3.12%**`（FP32 `71.25%`）；MAG240M R-GAT INT8 `**66.13%**`（耗时 `**2.06 天**`）。

> 💭
> **与本方向的关系（判断）**：背景（标志 GNN 量化从 QAT 走向免训练 PTQ 的中间过渡节点，同时展示忽略节点拓扑差异时 INT4 PTQ 在大图上会彻底崩溃）

### <a id="41b0e334-2e6f-8100-87ea-e7f7baecf402"></a>Spiking Point Transformer（2025）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2025；预印本 `arXiv:2502.15811`）
- **脉络：** 2 脉冲图网络
- **作者：** Peixi Wu, Bosong Chai, Hebei Li, Menghua Zheng, Yansong Peng, Zeyu Wang, Xuan Nie, Yueyi Zhang, Xiaoyan Sun
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spiking-point-transformer2025
- **代码：** [https://github.com/PeppaWu/SPT](https://github.com/PeppaWu/SPT)
- **年份：** 2025
- **一句话：** 提出面向 3D 点云分类的脉冲点云 Transformer（SPT），用队列偏移动态点编码（Q-SDE）激发时间步间差异，并设计基于局部 $k$-NN 邻域向量减法注意力的双分支脉冲点注意力模块。
- **链接：** https://arxiv.org/abs/2502.15811
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Spiking Point Transformer for Point Cloud Classification
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了静态点云直接重复输入导致的脉冲序列完全雷同问题，并将 Point Transformer 的局部邻域向量自注意力改造为全脉冲驱动版本。

**留下的局限**：从头直接训练（300 轮），不支持预训练浮点 Point Transformer 的免训练转换；局部 $k$-NN 是在三维空间坐标上构建的固定几何邻域。

**是否需要训练或微调**：是（使用替代梯度从头直接训练）

**涉及的算子**：最远点采样（FPS）、三维坐标 $k$-NN 局部邻域建图、队列偏移动态编码（Q-SDE）、局部向量减法脉冲自注意力与全局分支脉冲点注意力（DB-SPA）、LIF 神经元

**关键数字**：$T=4$ 下，`ModelNet40` 达 **91.37% OA / 88.97% mAcc**（推理能耗 **5.19 mJ**，比浮点 Point Transformer 的 19.65 mJ 低 **3.79×**），`ModelNet10` 达 **94.50% OA**，`ScanObjectNN`（`PB-T50-RS`）达 **78.02% OA / 75.15% mAcc**（Section 4.2 Table 1 & Table 2）。

> 💭
> **与本方向的关系（判断）**：直接相关（Claude 草稿二轮补充点名的点云直接训练代表作，其局部 $k$-NN 向量减法脉冲注意力可作为 M2 图注意力事件化的对照）

### <a id="41b0e334-2e6f-8144-b4ba-d0b7761af88b"></a>Signal-SGN（2025）

- **发表处：** Proceedings of the 33rd ACM International Conference on Multimedia（ACM MM 2025，DOI: `10.1145/3746027.3755246`；预印本于 2024 年 8 月发布于 `arXiv:2408.01701`）
- **脉络：** 2 脉冲图网络
- **作者：** Naichuan Zheng, Yuchen Du, Hailun Xia, Zeyu Liang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#signal-sgn2025
- **代码：** [https://github.com/zhengnaichuan2022/Signal-SGN](https://github.com/zhengnaichuan2022/Signal-SGN)
- **年份：** 2025
- **一句话：** 把人体骨架动作序列的自然帧时间轴直接映射为脉冲神经网络的时间步（$T=16$），将脉冲特征视为多维离散信号，结合一维脉冲图卷积、FFT 频域脉冲卷积与离散小波多尺度融合直接训练骨架识别模型。
- **链接：** https://doi.org/10.1145/3746027.3755246
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Signal-SGN: A Spiking Graph Convolutional Network for Skeleton Action Recognition via Learning Temporal-Frequency Dynamics
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：避免了在静态化骨架张量外额外堆叠脉冲时间步维度造成的冗余，利用频域与多尺度小波特征显著拉高了无蒸馏脉冲骨架网络的识别精度。

**留下的局限**：完全依赖从头直接训练（150 轮），无免训练转换机制；频域 FFT 与小波变换引入非纯脉冲算子开销。

**是否需要训练或微调**：是（使用 SGD + 交叉熵损失从头训练 150 轮，**未使用知识蒸馏**）

**涉及的算子**：骨架坐标归一化脉冲编码、1D 脉冲图卷积（1D-SGC）、脉冲自注意力（SSA）、快速傅里叶变换频域脉冲卷积（FSC）、离散小波变换多尺度融合（MWTF）

**关键数字**：$T=16$（对应 16 帧骨架输入）下，`NTU-RGB+D` Xs/Xv 单流（Joint）精度为 **80.5% / 87.7%**（理论能耗 **0.372 mJ**），双流（Bone+Joint）为 **82.5% / 89.2%**（0.744 mJ），四流集成为 **86.1% / 93.1%**（**1.488 mJ**，比 ST-GCN 的 16.01 mJ 低一个数量级以上）；`NTU-RGB+D 120` Xs/Xt 四流集成为 **75.3% / 77.9%**，`NW-UCLA` 达 **95.9%**（Section 4.2 Table 1）。

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q2 与 Q8 的核心文献：直接训练、无蒸馏；其“把流式序列帧直接对齐脉冲步 $T$”的做法与 M3 流式图处理思路相通）

### <a id="41b0e334-2e6f-8152-9613-dcac49d0c0b4"></a>E-3DSNN（2025）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2025；预印本 `arXiv:2412.07360`）
- **脉络：** 2 脉冲图网络
- **作者：** Xuerui Qiu, Man Yao, Jieyuan Zhang, Yuhong Chou, Ning Qiao, Shibo Zhou, Bo Xu, Guoqi Li
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#e-3dsnn2025
- **代码：** [https://github.com/bollossom/E-3DSNN](https://github.com/bollossom/E-3DSNN)
- **年份：** 2025
- **一句话：** 放弃直接在无序点集上做脉冲采样，提出脉冲体素编码（SVC）与仅在中心位置有脉冲时触发计算的脉冲稀疏卷积（SSC），配合整数多脉冲神经元（I-LIF）构建覆盖 3D 分类、自动驾驶检测与语义分割的通用 3D 脉冲骨干。
- **链接：** https://arxiv.org/abs/2412.07360
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Efficient 3D Recognition with Event-driven Spike Sparse Convolution
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了三维稠密脉冲卷积立方级膨胀及背景空体素冗余计算问题，（论文自称）首次把直接训练 3D SNN 推向大规模室外雷达检测与分割基准（KITTI、SemanticKITTI、nuScenes）。

**留下的局限**：走规则体素化稀疏 3D 卷积 + 从头直接训练路线，并非图网络转换；且训练时依赖整数发放神经元 I-LIF（$T=1, D=4$），推理时需展开为虚拟时间步。

**是否需要训练或微调**：是（在 4 张 A100 上从头直接训练 80–200 轮）

**涉及的算子**：3D 点云体素化、整数 LIF 神经元（I-LIF，$\lfloor\text{clip}\{U,0,D\}\rceil$）、子流形脉冲稀疏卷积（SSC，Rulebook 地址映射）、膜电位残差连接

**关键数字**：$T \times D = 1 \times 4$ 下，`ModelNet40` 达 **91.7%**（3.27M 参数，能耗 **0.04 mJ**；轻量版 1.87M 达 **91.5%**、**0.02 mJ**，Section 4.2 Table 1）；`KITTI` 验证集 Car 3D AP（Easy/Mod./Hard）达 **89.6% / 84.0% / 78.7%**（能耗 **3.4 mJ**，Table 2）；`SemanticKITTI` 验证集达 **69.2% mIoU**（能耗 **6.1 mJ**，较同架构 ANN 省电 **8.8×**，Table 3 & Table 4）；`nuScenes` 验证集达 **64.1 NDS**（能耗 **3.1 mJ**，Appendix Table 6）。

> 💭
> **与本方向的关系（判断）**：背景（3D 视觉脉冲网络的强性能标杆；其 I-LIF 整数多级发放与分级脉冲硬件映射同脉络一/五中的多阈值脉冲高度相通）

### <a id="41b0e334-2e6f-8177-8ccb-c1f98b9a1e3d"></a>Spiking Point Mamba（2025）

- **发表处：** IEEE/CVF International Conference on Computer Vision（ICCV 2025，DOI: `10.1109/ICCV51701.2025.02449`；预印本 `arXiv:2504.14371`）
- **脉络：** 2 脉冲图网络
- **作者：** Peixi Wu, Bosong Chai, Menghua Zheng, Wei Li, Zhangchi Hu, Jie Chen, Zheyu Zhang, Hebei Li, Xiaoyan Sun
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#spiking-point-mamba2025
- **代码：** [https://github.com/PeppaWu/SPM](https://github.com/PeppaWu/SPM)
- **年份：** 2025
- **一句话：** 提出（论文自称）首个面向 3D 点云分析的脉冲 Mamba 框架（SPM），结合分阶段动态最远点采样编码（HDE）、基于 $k$-NN 邻域与逐元素最大池化的脉冲嵌入层、沿时间步双向翻转的脉冲状态空间块，以及非对称 SNN 编码器—ANN 解码器掩码预训练。
- **链接：** https://doi.org/10.1109/ICCV51701.2025.02449
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Efficient Spiking Point Mamba for Point Cloud Analysis
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：突破了此前点云脉冲网络难以建模长程点序列依赖的瓶颈，并把点云脉冲网络拓展到部件分割（ShapeNetPart）与自监督掩码预训练。

**留下的局限**：需在双卡 RTX 4090 上从头迭代训练 300 轮；状态空间模块内部仍保留部分浮点矩阵乘法（公式 14 中 $E_{\text{MAC}} \cdot FL_1^n$），且 $k$-NN 仅在输入三维坐标层做一次静态分组，未涉及深层特征动态建图的转换。

**是否需要训练或微调**：是（从头直接训练 300 轮，或先做掩码自监督预训练再微调 150 轮）

**涉及的算子**：分层动态 FPS 采样编码（HDE）、三维坐标 $k$-NN 邻域分组、逐元素最大池化（EMP）与逐元素平均池化（EAP，用于门控支路防脉冲相乘信息丢失）、时间维翻转双向状态空间模型（SSM）、LIF 神经元

**关键数字**：$T=4$ 从头训练下，`ScanObjectNN` 三种变体 `OBJ-BG` / `OBJ-ONLY` / `PB-T50-RS` 总体精度分别达 **90.2% / 89.5% / 84.2%**（较 `Spiking Point Transformer` 分别提升 **+7.4 / +6.1 / +6.2** 个百分点），`ModelNet40` 无投票/有投票达 **92.3% / 92.7%**（Section 5.2 Table 1）；叠加掩码预训练后 `PB-T50-RS` 达 **86.5%**、`ModelNet40` 达 **93.1%**（Section 5.2.1）；`ShapeNetPart` 部件分割达 **82.29% Cls. mIoU / 84.8% Ins. mIoU**（Table 3）；$T=4$ 能耗 **5.4 mJ**（比 PointMamba 的 18.9 mJ 低 **3.5×**，$T=1$ 时 1.5 mJ 低 **12.6×**，Table 6）。

> 💭
> **与本方向的关系（判断）**：背景（代表 2025 年直接训练 3D 点云脉冲网络的精度上限参照；其发现“脉冲门控逐元素相乘会破坏词元关系、改用均值池化门控可挽回精度”的消融结论可资参考）

### <a id="41b0e334-2e6f-8179-813a-f26151210c36"></a>PMSM（2025）

- **发表处：** arXiv（2025 年 8 月预印本，`arXiv:2508.14520`）
- **脉络：** 2 脉冲图网络
- **作者：** Hangming Zhang, Zheng Li, Chenxiang Ma, Huajin Tang, Long Cheng, Kay Chen Tan, Qiang Yu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#pmsm2025
- **代码：** 未公开
- **年份：** 2025
- **一句话：** 通过极性量化激活函数（PQA）训练源网络，建立量化整数激活与带正负极性多脉冲增广积分发放神经元（AIF）之间的精确双射映射，实现**第一个时间步（****$T=1$****）零精度损失转换**，并在 **3 层图卷积网络（GCN）事件触觉图分类**上完成实验验证。
- **链接：** https://arxiv.org/abs/2508.14520
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Quantization Meets Spikes: Nearly Lossless Conversion at the First Timestep via Polarity Multi-Spike Mapping
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了传统 ANN→SNN 转换无法处理负激活值、以及常规量化转换在极低时间步（尤其 $T=1$）下因残余膜电位导致精度崩溃的难题。

**留下的局限**：**不是免训练转换**——必须用自定义 PQA 激活函数（可学习正负缩放因子 $\alpha^*, \beta^*$）重新训练源 GCN 200 轮；且硬件端需要支持正负多级整数脉冲（分级脉冲）的神经形态芯片。

**是否需要训练或微调**：部分（转换映射本身无需微调，但**必须先用 PQA 极性量化激活函数从头训练或重训源 ANN/GCN**）

**涉及的算子**：极性量化激活（PQA，含正负双分支阶梯量化）、增广积分发放神经元（AIF，初始膜电位偏置 $\frac{1}{2}\vartheta^l_{\text{SNN}}+\epsilon$，软复位，支持正负多脉冲发放）、3 层标准图卷积（GCN，39 节点触觉图邻接聚合）

**关键数字**：在 36 类事件触觉图数据集 `EvTouch-Objects`（沿用 TactileSGNet 的 39 触觉单元空间图，构建 3 层 PQA-GCN，$L=8, \vartheta_0=8$，Appendix Table VII）上，源 PQA-GCN 精度为 **90.97%**，转换后 SNN 在 $T=1$ 即取得 **90.97%**（**转换损失 0.00%**，突触操作数 0.41M SOPs，理论能耗仅 **0.37 **$\mu$**J**，Section 4.2 Table IV & Table V）；作为对比，常规单极性量化转换（QA）在 $T=1$ 崩溃至 **2.78%**（$T=64$ 才恢复至 86.11%），直接训练基线 `TactileSGNet` 在 $T=250$ 为 **89.44%**（Table IV & V）。

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q1 的关键证据之一：明确对 3 层 GCN 做了 ANN→SNN 权重转换并在 $T=1$ 无损保真，但前提是重训量化源网络且图结构固定、聚合线性）

### <a id="41b0e334-2e6f-81ab-85c7-dd44a710974a"></a>NI-SGCN（2025）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2025；预印本 `arXiv:2502.19660`）
- **脉络：** 2 脉冲图网络
- **作者：** Zikuan Li, Qiaoyun Wu, Jialin Zhang, Kaijun Zhang, Jun Wang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#ni-sgcn2025
- **代码：** [https://github.com/Miraclelzk/NI-SGCN](https://github.com/Miraclelzk/NI-SGCN)
- **年份：** 2025
- **一句话：** 将 DGCNN 的动态边卷积（EdgeConv）改造为面向 3D 点云去噪回归任务的噪声注入脉冲图卷积网络，**直接在二值脉冲特征空间上动态计算 ****$k$****-NN 建图，并将 EdgeConv 的 **`**max**`** 池化替换为 **`**mean**`** 池化**。
- **链接：** https://arxiv.org/abs/2502.19660
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Noise-Injected Spiking Graph Convolution for Energy-Efficient 3D Point Cloud Denoising
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：填补了脉冲图卷积在连续三维坐标回归（点云去噪）任务上的空白，并通过向膜电位注入自适应高斯噪声缓解二值脉冲量化对精细几何位移估计的损失。

**留下的局限**：属于从头直接训练，并非对预训练 DGCNN 做免训练转换；但它的消融实验极其直观地暴露了**二值脉冲特征下 **`**max**`** 邻域聚合严重丢失几何细节**的现象。

**是否需要训练或微调**：是（使用三角窗替代梯度从头端到端训练）

**涉及的算子**：**脉冲特征空间动态 **$k$**-NN 建图**、脉冲相对边特征构造 $[s_i, s_j - s_i]$、噪声注入 LIF 神经元（NI-LIF）、**邻域 **`**mean**`** 聚合（替代原版 EdgeConv 的 **`**max**`** 聚合）**

**关键数字**：$T=4$ 下，在 `PU-Net` 测试集（10K 点，2% 噪声）上 Chamfer Distance（CD，$\times 10^{-4}$，越小越好）达 **1.798**、Point2Mesh（P2M）达 **0.659**（优于浮点 DGCNN/DMRDenoise 等基线，理论能耗仅 **6.12 mJ**，较浮点基线节省约 **86%**，Section 4.2 Table 1 & Section 4.3）；**关键聚合算子消融（Section 4.2 Table 2）**：在完全相同的脉冲动态 EdgeConv 下，使用原版 `MAX` 聚合时 CD 恶化至 **2.199**，改为 `MEAN` 聚合后 CD 显著改善至 **1.798**（降低 18.2% 误差）！

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q2 中 DGCNN 现状的关键文献；其“脉冲特征上算动态 $k$-NN + `max` 聚合显著劣于 `mean` 聚合”的实验结果是对本项目 M1 核心假设的极佳侧面印证）

### <a id="41b0e334-2e6f-81d2-88d9-fd252aa2f68f"></a>SGNNBench（2025）

- **发表处：** Advances in Neural Information Processing Systems Datasets and Benchmarks Track（NeurIPS 2025；预印本 `arXiv:2509.21342`）
- **脉络：** 2 脉冲图网络
- **作者：** Huizhe Zhang, Jintang Li, Yuchang Zhu, Huazhen Zhong / Li Kuang, Liang Chen（注：arXiv 元数据末位作者列为 Li Kuang，NeurIPS 检索页含 Huazhen Zhong，同属中山大学陈亮团队）
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#sgnnbench2025
- **代码：** [https://github.com/Zhhuizhe/SGNNBench](https://github.com/Zhhuizhe/SGNNBench)
- **年份：** 2025
- **一句话：** （论文自称）首个面向大规模图的脉冲图神经网络统一评测基准，在 18 个同配、异配与大规模动态图数据集上系统对比了 9 种直接训练 SGNN 与 7 种全精度 GNN 的精度、显存、延迟和理论能耗。
- **链接：** https://arxiv.org/abs/2509.21342
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SGNNBench: A Holistic Evaluation of Spiking Graph Neural Network on Large-scale Graph
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：统一了此前各篇 SGNN 各自为政的数据划分与能耗估算口径，（论文自称）首次定量揭示了现有 SGNN 在深层异配图上的严重退化以及部分 SGNN 能耗反超全精度 GNN 的隐患。

**留下的局限**：**9 种被测模型全部为从头直接训练的通用图节点分类模型**，既未收录任何 ANN→SNN 图转换方法，也未包含任何视觉图（点云、骨架、超像素/图像块图）任务。

**是否需要训练或微调**：是（基准内所有被测脉冲图模型均为从头训练）

**涉及的算子**：涵盖伯努利/泊松/直接线性脉冲编码，IF/LIF/PLIF 神经元，GCN/GAT/SAGE/SGC/图 Transformer/流形图卷积等消息传递算子

**关键数字**：评测 **9 种 SGNN**（`GC-SNN`, `GA-SNN`, `SpikingGCN`, `SpikeNet`, `SpikeGCL`, `SpikeGT`, `MSG`, `DRSGNN`, `SiGNN`）与 **7 种全精度 GNN**，横跨 **18 个数据集**（9 个静态同配图、6 个静态异配图、3 个百万边级动态图 `DBLP`/`Tmall`/`Patent`，Section 3.1 Table 1；注：正文 3.1 节文字曾顺带提及 Actor/Deezer，实际评测以 Table 1 的 18 个数据集为准）；在异配长程依赖图 `Roman-Empire` 上 9 种 SGNN 相对全精度 GNN 平均暴跌 **-31.27%**（最佳 SGNN 仅 51.32% vs GraphGPS 82.59%，Table 3）；能耗表（Table 6）揭示 `SiGNN` 在多个静态图上理论能耗甚至**高于**全精度 GCN/SGC。

> 💭
> **与本方向的关系（判断）**：直接相关（一方面印证主流图脉冲社区完全忽视了“免训练转换”与“视觉图”，另一方面其揭示的“编码方式与未脉冲化层会导致 SGNN 能耗反超 ANN”直接支撑本项目的公平能耗盈亏分析）

### <a id="41b0e334-2e6f-81dd-a3f8-c2e08f143bdf"></a>Signal-SGN++（2025）

- **发表处：** arXiv（2025 年 12 月预印本，`arXiv:2512.22214`，投稿 *IEEE Transactions on Neural Networks and Learning Systems*）
- **脉络：** 2 脉冲图网络
- **作者：** Naichuan Zheng, Hailun Xia, Weiyi Li, Yuchen Du
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/02-spiking-gnn.md#signal-sgn2025
- **代码：** 未公开
- **年份：** 2025
- **一句话：** 在 `Signal-SGN` 基础上引入融合自适应骨架拓扑先验与 QK 特征相似度的 **Top-****$k$**** 选邻居 + 通道循环移位注意力（TSSA）**，以及基于勒让德多项式小波的低频拓扑感知时频融合模块（TATF）。
- **链接：** https://arxiv.org/abs/2512.22214
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Signal-SGN++: Topology-Enhanced Time–Frequency Spiking Graph Network for Skeleton-Based Action Recognition
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把骨架关节脉冲自注意力和跨频段融合的复杂度从 $O(V^2 d)$ 降为 $O(k V d)$，并用无乘法的左右循环通道移位增强局部动态关节交互表达。

**留下的局限**：仍需从头训练 150 轮；内部包含关节维度的复数快速傅里叶变换（FFT）与小波分解插值，不兼容纯加法脉冲硬件直接免训练迁移。

**是否需要训练或微调**：是（使用 SGD 与替代梯度从头直接训练 150 轮，无知识蒸馏）

**涉及的算子**：骨架脉冲编码（每通道 min-max 归一化 + Conv1D + BN + LIF）、1D 脉冲图卷积（1D-SGC）、Top-$k$ 拓扑—相似度融合选邻居 + 通道循环移位（TSSA，$k=8$）、FFT 频域脉冲复卷积（FSC）、勒让德多小波分解与低频 Top-$k_{\text{topo}}$ 均值聚合（TATF，$k_{\text{topo}}=6$）

**关键数字**：16 帧输入（$T=16$）下，单流（Joint）在 `NTU-RGB+D` Xs/Xv 达 **81.3% / 88.4%**（能耗 **0.369 mJ**，注：消融表 Table II 中 D3 配置报告 Xs 为 82.5%，与主表 Table I 单流 81.3% 存在文内表间微小出入，两处均予记录）；四流集成（4-ensemble）在 `NTU-RGB+D` Xs/Xv 达 **87.2% / 94.5%**（能耗 **1.476 mJ**），`NTU-RGB+D 120` Xs/Xt 达 **76.5% / 78.9%**，`NW-UCLA` 达 **96.3%**（Section V-C Table I）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（TSSA 将静态拓扑先验矩阵与动态脉冲特征相似度加权后再取 Top-$k$ 邻居的设计，对缓解动态选邻居翻转有直接借鉴意义）

### <a id="41b0e334-2e6f-8100-8e7b-c183fa3d01fe"></a>CBinfer 期刊版（2020）

- **发表处：** IEEE Transactions on Circuits and Systems for Video Technology，Vol. 30，No. 5，pp. 1451–1465，2020（据检索结果；PDF 为 arXiv 1808.05488）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Lukas Cavigelli, Luca Benini
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#cbinfer-期刊版2020
- **代码：** [https://github.com/lukasc-ch/CBinfer](https://github.com/lukasc-ch/CBinfer)
- **年份：** 2020
- **一句话：** 静态相机视频上，只对变化超过阈值的像素及其受影响区域重算卷积。
- **链接：** https://arxiv.org/abs/1808.05488
- **核对人与日期：** Gemini，2026-11-16
- **标题：** CBinfer: Exploiting Frame-to-Frame Locality for Faster Convolutional Network Inference on Video Streams
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：把会议版推广到语义分割、姿态检测和目标检测。

**留下的局限**：静态相机；变化区域随层扩散，靠阈值和池化压制。

**是否需要训练或微调**：否

**涉及的算子**：卷积、ReLU、池化、像素变化阈值

**关键数字**：Tegra X2 上语义分割平均加速 9.1 倍、精度损失 <0.1%；姿态检测加速 7.0 倍；目标检测运算量降 5 倍；能效 511 GOp/s/W（基线 70）（第 1 页摘要）。

> 💭
> **与本方向的关系（判断）**：背景

### <a id="41b0e334-2e6f-810e-ac17-f92453cd9b67"></a>Ingress（2021）

- **发表处：** Proceedings of the VLDB Endowment（PVLDB），Vol. 14，No. 9，pp. 1613–1625，2021
- **脉络：** 4 事件驱动与增量推理
- **作者：** Shufeng Gong, Chao Tian, Qiang Yin, Wenyuan Yu, Yanfeng Zhang, Liang Geng, Song Yu, Ge Yu, Jingren Zhou
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#ingress2021
- **代码：** [https://github.com/alibaba/libgrape-lite](https://github.com/alibaba/libgrape-lite) （ingress 分支）
- **年份：** 2021
- **一句话：** 把用户写好的批处理顶点中心图算法自动改写成增量版本，图变化时只修正受影响的结果。
- **链接：** https://vldb.org/pvldb/vol14/p1613-gong.pdf
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Automating Incremental Graph Processing with Flexible Memoization
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 不适用

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：增量图算法难写；它给出四种记忆化策略及各自的适用条件，并自动检查条件来选用（第 1–2 页）。

**留下的局限**：精确增量，无阈值；面向 PageRank、SSSP 等迭代图计算和 GCN 前向这类顶点中心程序，不涉及脉冲、视觉图或逐帧特征变化。

**是否需要训练或微调**：不适用

**涉及的算子**：顶点中心消息传递、min / sum 聚合、GCN 前向、mean 聚合 GraphSAGE

**关键数字**：比现有增量图系统平均快 15.93 倍，最高 147.14 倍（第 1 页摘要）。

> 💭
> **与本方向的关系（判断）**：背景（通用增量图计算的先例）

### <a id="41b0e334-2e6f-8124-a575-dbd7f0fa5227"></a>DynaGraph（2022）

- **发表处：** GRADES & NDA '22（ACM SIGMOD 附属研讨会），2022 年 6 月 12 日，费城（第 1 页页脚，DOI 10.1145/3534540.3534691）。**更正**：上一轮笔记写作 “SoCC 2022”，PDF 页脚显示不是。
- **脉络：** 4 事件驱动与增量推理
- **作者：** Mingyu Guan, Anand Padmanabha Iyer, Taesoo Kim
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#dynagraph2022
- **代码：** 未公开
- **年份：** 2022
- **一句话：** 加速“图卷积 + 循环网络”式动态 GNN 训练的系统，靠缓存同一份图消息、合并多个时间步的图卷积、分布式数据并行来提速。
- **链接：** https://taesoo.kim/pubs/2022/guan:dynagraph.pdf
- **核对人与日期：** Gemini，2026-11-16
- **标题：** DynaGraph: Dynamic Graph Neural Networks at Scale
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 不适用

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：GraphRNN 的多个门各自重复做同一次图聚合；小图上逐时间步卷积 GPU 利用率低。

**留下的局限**：针对训练，不是推理；精确，无阈值，不丢小变化（第 7 页 5.4 节：精度与 DGL / PyG Temporal 相同）；不涉及脉冲或视觉图。

**是否需要训练或微调**：不适用（本身就是训练系统）

**涉及的算子**：图卷积、GRU / LSTM 门、消息缓存

**关键数字**：比 DGL 最多快 2.5 倍、比 PyG Temporal 最多快 2.7 倍（第 5 页）；GCRN-LSTM 两机加速 2.54 倍、八机 2.23 倍（第 7 页）。

> 💭
> **与本方向的关系（判断）**：背景（共享消息缓存的先例）

### <a id="41b0e334-2e6f-8129-8669-caf55d93d3d5"></a>Sigma-Delta（2017）

- **发表处：** International Conference on Learning Representations（ICLR 2017，Poster）（OpenReview 决定，见 SL-65；PDF 页眉仍是“Under review”）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Peter O'Connor, Max Welling
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#sigma-delta2017
- **代码：** [https://github.com/petered/sigma-delta](https://github.com/petered/sigma-delta)
- **年份：** 2017
- **一句话：** 层与层之间只传激活变化量的取整脉冲，计算量随输入变化多少而不是网络大小而定，可把预训练网络直接改造过来。
- **链接：** https://openreview.net/forum?id=Hy1b8W9eg
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Sigma-Delta Quantized Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：时间差分和积分与线性运算可交换；用 herding 做离散化，使任一时刻的输出与“取整网络”相同，不随历史路径漂移；只优化层间尺度系数，在精度和计算量之间折中（第 5 页第 4 节）。

**留下的局限**：MLP / CNN；层间尺度需在小数据上优化；未涉及图结构。

**是否需要训练或微调**：否（不改权重，只调层间尺度）

**涉及的算子**：线性层、卷积、ReLU、取整、herding、时间差分 / 积分

**关键数字**：MNIST / Temporal-MNIST 结果见第 13 页 Table 1；预训练 VGG 在 ILSVRC2015 两段拼接视频上，第一段（静态背景）计算量约为原网络的 1/11，第二段（运动较多）约为 1/4（第 8 页 Fig. 5 图注）；正文另称视频上约可省 10 倍计算、精度有一定损失（第 8 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（差分推理的思想源头，且明确面向预训练网络）

### <a id="41b0e334-2e6f-815c-9186-c7c0c03ea480"></a>CBinfer 会议版（2017）

- **发表处：** International Conference on Distributed Smart Cameras（ICDSC 2017）（据 DeltaCNN、Eventful Transformers 参考文献及检索；PDF 为 arXiv 1704.04313）。**更正**：上一轮下载的 `arXiv:1608.08404` 实际是一篇类星体天文论文，已排除。
- **脉络：** 4 事件驱动与增量推理
- **作者：** Lukas Cavigelli, Philippe Degen, Luca Benini
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#cbinfer-会议版2017
- **代码：** [https://github.com/lukasc-ch/CBinfer](https://github.com/lukasc-ch/CBinfer)
- **年份：** 2017
- **一句话：** 检测帧间变化的像素，只更新受它们影响的卷积输出。
- **链接：** https://arxiv.org/abs/1704.04313
- **核对人与日期：** Gemini，2026-11-16
- **标题：** CBinfer: Change-Based Inference for Convolutional Neural Networks on Video Data
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：第 3 页指出像素级更新会随卷积层逐层扩散，但变化在输出端同样局部，噪声样的变化对深层影响小。

**留下的局限**：静态相机；阈值手调。

**是否需要训练或微调**：否

**涉及的算子**：卷积、像素变化阈值

**关键数字**：比 cuDNN 平均快 8.6 倍、精度损失 <0.1%、能效约为逐帧推理的 10 倍（第 1 页摘要）。

> 💭
> **与本方向的关系（判断）**：背景

### <a id="41b0e334-2e6f-81aa-9266-d88fe02476bb"></a>Delta 网络（2017）

- **发表处：** Proceedings of the 34th International Conference on Machine Learning（ICML 2017），PMLR 70:2584–2593（据 PMLR 检索）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Daniel Neil, Jun Haeng Lee, Tobi Delbruck, Shih-Chii Liu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#delta-网络2017
- **代码：** 未公开
- **年份：** 2017
- **一句话：** RNN 里每个神经元只有在激活变化超过阈值时才发送新值。
- **链接：** https://arxiv.org/abs/1612.05571
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Delta Networks for Optimized Recurrent Network Computation
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：RNN 每步都要读写状态，内存访问是瓶颈；阈值化减少计算和访存，并保存“上次发送值”以防漂移。

**留下的局限**：RNN；阈值大时需要专门训练才能保持精度。

**是否需要训练或微调**：部分（现成网络可直接用，训练后效果更好）

**涉及的算子**：GRU、线性层、阈值 Θ

**关键数字**：WSJ 语音识别上现成网络 Θ=0.2 时约 5.5 倍加速、WER 10.8%（Θ=0 时 10.2%），训练后 5.7 倍同 WER（第 6 页）；TIDIGITS 上成本降 9 倍；驾驶转向网络中 RNN 部分约 100 倍（第 1 页摘要、第 6 页）。

> 💭
> **与本方向的关系（判断）**：背景

### <a id="41b0e334-2e6f-81b7-8866-fd3008d1ab55"></a>ETHEREAL（2026）

- **发表处：** arXiv（两份预印本：`2608.17787v1`，2026-08-18，14 页；`2609.15241v1`，2026-09-14，5 页）。**冲突说明**：Claude 草稿写作 “ESSERC 2026”，但两份 PDF 全文都没有出现 ESSERC 或其他录用信息（长文版参考文献里的 ESSERC 2026 指的是另一篇 HeMAiA 论文），因此会议归属记为“未核实”。（核对人 2026-11-16 复查时更正了本条早先写错的标题与发表处）
- **脉络：** 5 能耗与硬件
- **作者：** Adrian Kneip, Martin Lefebvre, Daniel Gehrig, Victoria Catalán Pastor, Davide Scaramuzza, Marian Verhelst, Charlotte Frenkel
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#ethereal2026
- **代码：** 未公开
- **年份：** 2026
- **一句话：** 流片实现了（论文自称）首颗面向事件相机视觉的专用图神经网络 ASIC 芯片（28nm CMOS），用纯片上混合 3D/2D SRAM 和 4b/8b 量化图卷积实现每事件约 25.6 微秒的实时目标检测与分类。
- **链接：** https://arxiv.org/abs/2608.17787
- **核对人与日期：** Gemini，2026-11-16
- **标题：** ETHEREAL: A 25.6-µs/inf. Low-latency Event-driven Graph-neural-network Processor for High-resolution Vision at the Edge（长文版 `arXiv:2608.17787v1` 第 1 页标题）；另有 5 页短文版 `arXiv:2609.15241v1`，标题为 “A 25-µs/inf Event-driven Graph Neural Network Processor with Spatiotemporal Caching and Spline Convolution for Ultra-low-latency AI at the Edge”
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：解决了事件相机动态时空图在边缘芯片上建图指针访存不规则、片外 DRAM 功耗高、深层图卷积特征存储爆炸三大硬件瓶颈——通过“前浅层 3D 时空缓存异步逐事件更新 + 后深层体素池化转 2D 暂存器同步复用”的混合架构，将全部 1.25 MB 存储塞进 3.7 mm² 芯片内。

**留下的局限**：（1）**芯片运行的不是脉冲神经网络（SNN）**，而是带 4-bit/8-bit 整数量化激活（QReLU）与 B 样条边权（SplineConv）的量化事件图网络，节点间传递的是多位量化特征向量而非脉冲；（2）部署前必须做量化感知训练（QAT），不能免训练直接部署预训练浮点模型；（3）为了硬件确定性，将原版 DAGr 的双向多跳更新简化为有向单跳或受限双向图，纯 GNN 模式在复杂检测上精度偏低，仍需搭配帧图像 CNN 分支。

**是否需要训练或微调**：是（需对 4b/8b 混合精度 DAGr-GNN 进行量化感知训练 QAT，见 Section VI-A）

**涉及的算子**：半径邻域时空建图（Directed / Bidirectional FIFO 3D Grid）、SplineConv（一阶 B-spline 边特征加权卷积）、`max` 邻域聚合、体素网格 `max` 池化（VoxelPool）、量化 ReLU（QReLU）、层融合批归一化

**关键数字**：TSMC 28nm CMOS 流片，芯片面积 `3.7 mm²`，片上总 SRAM `1.25 MB`（`512 kB` 权重 + `144 kB` 3D 时空缓存 + `584 kB` 2D 暂存器，Section IV-V, pp. 5–9）；含 8 个邻居并行消息传递核，支持 4b/8b 权重与激活；在 VGA 分辨率（`640×480`）DSEC 目标检测基准上（8b/8b 首层 + 4b/4b 主干），流水线推理延迟 `**25.6 µs/event**`（顺序执行 `46.1 µs`；不同位宽配置下 `20.1–40.1 µs`），`0.95V / 220MHz` 下平均功耗 `65.2 mW`、单事件能耗 `**1.6 µJ/event**`（跨配置 `1.2–2.5 µJ`；低压 `0.6V` 模式下最低 `**0.54 µJ/event**`、功耗 `10.6 mW`），检测精度 `30.3 mAP50`（GNN+CNN 融合）/ `7.6 mAP50`（纯有向 GNN）；在 N-CARS 分类上精度 `**86.7%**`（Section VI, Fig. 18–21 & Table I, pp. 10–13）。**版本间数字冲突**：长文版摘要写单事件能耗 `1.6 µJ`，5 页短文版摘要写 `25.6 µs` 与 `1.7 µJ`、并称“比已有工作改善 10–1000 倍”（`arXiv:2609.15241` 第 1 页摘要），两者都记录，不作取舍。

> 💭
> **与本方向的关系（判断）**：直接相关（证明事件驱动视觉图网络已有真实流片需求，同时坐实当前专用芯片跑的是 4b/8b 量化 GNN 而非脉冲 GNN）

### <a id="41b0e334-2e6f-81df-8dda-f72a143b3488"></a>Skip-Conv（2021）

- **发表处：** IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2021）（据检索结果）
- **脉络：** 4 事件驱动与增量推理
- **作者：** Amirhossein Habibian, Davide Abati, Taco S. Cohen, Babak Ehteshami Bejnordi
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/04-event-driven-inference.md#skip-conv2021
- **代码：** 未核实
- **年份：** 2021
- **一句话：** 卷积改为在帧间残差上计算，每层配一个门决定哪些位置的残差值得算。
- **链接：** https://arxiv.org/abs/2104.11487
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Skip-Convolutions for Efficient Video Processing
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：背景区域的重复计算；门可以按残差幅值直接判断，也可以与卷积一起训练（第 1 页）。

**留下的局限**：只看帧间差，缓慢累积的变化会被持续忽略（EvNets 第 7 页指出此问题）；针对 CNN。

**是否需要训练或微调**：部分（幅值门不需要，学习门需要）

**涉及的算子**：卷积、门函数、残差

**关键数字**：EfficientDet 和 HRNet 上计算量降 3–4 倍且不掉点（第 1 页摘要）；HRNet-w32 上 MAC 降 2.51 / 4.33 / 7.92 倍时实际耗时降 1.48 / 1.91 / 4.09 倍（第 7 页 Table 2）。

> 💭
> **与本方向的关系（判断）**：背景

### <a id="41b0e334-2e6f-815d-a926-fff7869d3f03"></a>Horowitz（2014）

- **发表处：** 2014 IEEE International Solid-State Circuits Conference Digest of Technical Papers（ISSCC 2014），pp. 10–14（DOI: `10.1109/ISSCC.2014.6757323`）
- **脉络：** 5 能耗与硬件
- **作者：** Mark Horowitz
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#horowitz2014
- **代码：** 无（硬件综述与大会主题报告论文）
- **年份：** 2014
- **一句话：** 现代计算机体系结构与神经网络硬件能耗估算的奠基参照文献，给出了 45nm 0.9V CMOS 工艺下整数/浮点加乘运算、片上 SRAM 缓存、片外 DRAM 访问及处理器指令管线的精确数量级能耗表。
- **链接：** https://doi.org/10.1109/ISSCC.2014.6757323（全文
- **核对人与日期：** Gemini，2026-11-16
- **标题：** 1.1 Computing's Energy Problem (and what we can do about it)
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：系统阐明了 Dennard 缩放终结后的“暗硅（Dark Silicon）”与能耗墙根源——指出算术单元本身极省电，真正的能耗大头是指令控制开销（高出加法几百倍）和远距离存储器数据搬运（高出加法成百上千倍）。

**留下的局限**：数据测算于 45nm 0.9V 平面 CMOS 时代（距今十余年，在 22nm/7nm/5nm 下算术与连线电容缩放比例已发生变化，SRAM 读写与 NoC 搬运占比相对算术进一步攀升）；且常被脉冲网络论文断章取义地只抽取 `FP32 Add (0.9 pJ)` 与 `FP32 Mult (3.7 pJ)` 而无视同表中的 `INT8` 与 `Cache/DRAM` 行。

**是否需要训练或微调**：否（集成电路基础能耗基准文献）

**涉及的算子**：8-bit/32-bit 整数加乘、16-bit/32-bit 浮点加乘、8KB/32KB/1MB SRAM 缓存访问、DRAM 访问

**关键数字**：45nm CMOS, 0.9V（完整数字见本文开头专表，出自 p. 14, Figure 1.1.9 及 p. 11, Section 5–6）：`8b Int Add = 0.03 pJ`、`32b Int Add = 0.1 pJ`、`16b FP Add = 0.4 pJ`、`32b FP Add = 0.9 pJ`、`8b Int Mult = 0.2 pJ`、`32b Int Mult = 3.1 pJ`、`16b FP Mult = 1.1 pJ`、`32b FP Mult = 3.7 pJ`；64-bit 读取 `8KB / 32KB / 1MB Cache = 10 / 20 / 100 pJ`，`DRAM = 1.3–2.6 nJ`；简单顺序处理器控制管线 `**70 pJ/instruction**`。

> 💭
> **与本方向的关系（判断）**：直接相关（所有能耗讨论的原点；必须在我们的论文里完整引用其访存与低比特整数行，彻底告别不严谨的纯 FP32 `4.6 vs 0.9 pJ` 口径）

### <a id="41b0e334-2e6f-8196-b0a4-e2fc4c682737"></a>Tianjic（2019）

- **发表处：** Nature，vol. 572, no. 7767, pp. 106–111, August 2019（DOI: `10.1038/s41586-019-1424-8`；配套电路实现详述于 Deng 等，IEEE JSSC 2020, vol. 55, no. 8, pp. 2228–2246）
- **脉络：** 5 能耗与硬件
- **作者：** Jing Pei, Lei Deng, Sen Song, Mingguo Zhao, Youhui Zhang, Shuang Wu, Guanrui Wang, Zhe Zou, Zhenzhi Wu, Wei He 等（Luping Shi 团队）
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#tianjic2019
- **代码：** 未公开
- **年份：** 2019
- **一句话：** 清华大学研制的 28nm 异构融合类脑芯片“天机”，通过可独立重构的轴突与胞体模块，在同一套片上路由网络上同时支持 1-bit 脉冲网络（SNN）与 8-bit 连续值深度网络（ANN）及二者混合模型。
- **链接：** https://doi.org/10.1038/s41586-019-1424-8
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Towards artificial general intelligence with hybrid Tianjic chip architecture
- **核对深度：** 仅摘要
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打通了脉冲范式与传统 8-bit 定点神经网络范式的硬件隔阂——复用树突与突触乘加阵列，仅在输入轴突和输出胞体切换脉冲序列解析或 8-bit 激活截断打包，从而支持无人自行车上的多模态混合网络协同推理。

**留下的局限**：需注意**概念区分**——据 SENECA（Table 3, p. 6）核实，天机的单一模式数据类型为固定精度（`Fixed`：SNN 模式传 1-bit 二值脉冲，ANN 模式传 8-bit 整数激活，或由胞体把膜电位截断为 8-bit 混合信号转发），不同于 Loihi 2 / SENECA 在纯事件驱动脉冲指令流中原生支持任意可编程分级脉冲载荷。

**是否需要训练或微调**：否（双模推理芯片平台）

**涉及的算子**：LIF 脉冲神经元（1-bit 脉冲）、ANN 8-bit 整数乘加与 ReLU/非线性查表、异构混合信号转换（ANN↔SNN 胞体直转）

**关键数字**：UMC 28nm 工艺，156 个功能核（FCores），单核面积 `**0.092 mm²**`、每核 `0.17 Mb` SRAM，等效突触能效约 `**1.54 pJ/SOp**`（核实自 SENECA 全文 Table 1 & Table 3, pp. 5–6，引用 Deng et al., IEEE JSSC 2020）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（如果视觉图模型中“动态 $k$NN 建图模块”保留低比特整数计算、而“图消息传递主干”转为事件驱动脉冲推理，天机与 C-DNN 这类 ANN-SNN 异构融合芯片正是现成的硬件载体！）

### <a id="41b0e334-2e6f-81ae-8be3-f7518c8e02f6"></a>SGQuant（2020）

- **发表处：** 2020 IEEE 32nd International Conference on Tools with Artificial Intelligence（ICTAI 2020），pp. 1044–1052（DOI: `10.1109/ICTAI50040.2020.00161`；预印本 `arXiv:2007.05100v2`）
- **脉络：** 5 能耗与硬件
- **作者：** Boyuan Feng, Yuke Wang, Xu Li, Shu Yang, Xueqiao Peng, Yufei Ding
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/05-energy-and-hardware.md#sgquant2020
- **代码：** 未公开
- **年份：** 2020
- **一句话：** 针对图嵌入显存占用远大于权重矩阵的特点，设计了按层、按拓扑分量（节点特征 vs 注意力系数）和按节点度分组的多粒度 GNN 特征量化框架，并用机器学习回归器自动搜索各组位宽。
- **链接：** https://arxiv.org/abs/2007.05100
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SGQuant: Squeezing the Last Bit on Graph Neural Networks with Specialized Quantization
- **核对深度：** 全文
- **与本方向的关系：** 背景
- **是否需要训练或微调：** 是

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：缓解了大图训练/推理中节点特征矩阵撑爆 GPU 显存的问题，利用高入度节点分配更高比特、低入度节点分配更低比特（1–4 bit）实现高压缩比。

**留下的局限**：（1）**只量化节点嵌入与注意力系数，权重矩阵 **$W$** 全程保留 FP32，且在矩阵相乘前先反量化回 FP32**（Section III-A, Eq. 5, p. 3），因此**只能省显存/带宽，不能省浮点乘加算术能耗**，不适合作为整数算术能耗基线；（2）**并非纯免训练**：原文明确指出直接训练后量化会掉点高达 `**10%**`，必须依赖基于直通估计器（STE）的微调才能把掉点拉回 `0.5%` 以内（Section III-B, p. 3），且自动位宽选择需采样跑 200 组量化评估训练回归模型。

**是否需要训练或微调**：是（需 STE 微调恢复直接量化最高 10% 的精度损失，且自动位宽搜索需 200 次探针评估，Section III-B & III-C, pp. 3–4）

**涉及的算子**：GCN / GAT / AGNN 邻域聚合与注意力得分、组件级/拓扑度感知均匀量化、FP32 反量化重匹配（Rematching）

**关键数字**：在 Cora、CiteSeer、PubMed、Reddit、Amazon-Computers、Amazon-Photo 六个数据集上（Tables I–III, pp. 5–7），将特征表示压缩至平均约 `1.6–4 bits`，实现 `**4.25×–31.9×**` 特征比特压缩比和 `**1.11×–2.53×**` GPU 时间加速（主要来自访存带宽减少），微调后精度损失控制在 `**< 0.5%**` 以内（Reddit GCN FP32 `93.9%` vs SGQuant `93.7%`，Table II, p. 6）。

> 💭
> **与本方向的关系（判断）**：背景（厘清了 GNN 量化早期代表作的真实边界：SGQuant 保留 FP32 权重且需微调，不能误当作免训练全整数 W4A4/W8A8 对照基线）

### <a id="41b0e334-2e6f-8102-8bb3-f66e4680f8f4"></a>Parallel Conversion（2025）

- **发表处：** Proceedings of the 42nd International Conference on Machine Learning（ICML 2025，PMLR Vol. 267；预印本 `arXiv:2412.13610`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Zecheng Hao, Qichao Ma, Kang Chen, Yi Zhang, Zhaofei Yu, Tiejun Huang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#parallel-conversion2025
- **代码：** [https://github.com/hzc1208/Parallel_Conversion](https://github.com/hzc1208/Parallel_Conversion)
- **年份：** 2025
- **一句话：** 利用转换任务中输入恒定的性质推导累积发放数闭式跳变边界，将串行时间步展开的 IF 神经元改写为可一步并行计算的并行脉冲神经元（PSN），并提供免重训的 `ReLU → ClipReLU → DA-QCFS` 贪心通道校准流水线。
- **链接：** https://arxiv.org/abs/2412.13610
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Faster and Stronger: When ANN-SNN Conversion Meets Parallel Spiking Calculation（PDF 第 1 页与 arXiv API；本条早先误写为另一标题，复查时已更正）
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：打破了传统转换 SNN 必须在 GPU 上串行循环 $T$ 个时间步的仿真墙，用 $O(T)$ 前缀充电加 $O(\log T)$ 二分搜索在 $T\ge 32$ 时获得 19–38 倍 GPU 推理加速，同时兼容 QAT（QCFS）与免训练转换。

**留下的局限**：闭式并行跳变条件依赖“输入在全部 $T$ 个时间步内保持恒定或严格阶梯单调”的静态假设，无法直接迁移到动态重算拓扑或流式异步变化的视觉图输入；且免训练分支仍需 $T=16\sim 32$ 步才能逼近原精度。

**是否需要训练或微调**：部分（支持两种模式：一是直接对接需重训的 QCFS 模型；二是完全免训练的 `ReLU → ClipReLU → DA-QCFS` 训练后逐通道贪心误差校准）

**涉及的算子**：并行脉冲神经元（PSN，预计算累积权重矩阵 $\Lambda_{\text{PC}}^l$ 与二分搜索脉冲计数）、免训练剪裁阈值与通道残差贪心校准（`DA-QCFS`）、BatchNorm 折叠、`AvgPool`

**关键数字**：在 GPU 实测中（Section 5.3 Figure 2，第 8 页），当 $T\ge 32$ 时较串行 IF 仿真提速 **19×–38×**；对接 QCFS 源模型时，`ImageNet` `ResNet-34`（源 **74.30%**）在 $T=4 / 8$ 达 **72.90% / 74.32%**（Section 5.1 Table 3，第 7 页）；**纯免训练转换标准 TorchVision ReLU 模型**时（Section 5.2 Table 4，第 8 页），`ResNet-34`（源 **73.31%**）在 $T=16 / 32$ 达 **68.04% / 72.46%**，`ResNet-50`（源 **76.12%**）达 **73.59% / 75.71%**，`ResNet-101`（源 **77.38%**）达 **73.86% / 76.42%**。

> 💭
> **与本方向的关系（判断）**：可借用的技术（在大规模静态视觉图失效普查实验中，可借用其闭式并行仿真思想大幅加速多时间步率编码基线的 GPU 评测）

### <a id="41b0e334-2e6f-8142-af44-e1d41fa091ff"></a>One-Spike SNN（2025）

- **发表处：** IEEE Transactions on Emerging Topics in Computing（IEEE TETC 2025，Vol. 13, Issue 3，pp. 1020–1032，DOI: `10.1109/TETC.2025.3558454`；预印本 `arXiv:2403.08786`）
- **脉络：** 1 ANN→SNN 转换,2 脉冲图网络
- **作者：** Sangwoo Hwang, Jaeha Kung
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#one-spike-snn2025
- **代码：** 未公开
- **年份：** 2025
- **一句话：** 把整数二次幂相位编码推广为非整数底数 $B \in (1,2)$（如 $B=1.5$）并加两遍扫描抑制冗余脉冲，使每个激活神经元在整个推理窗口内尽量只发 1 个脉冲，且**在 5 个文本图数据集上免训练转换了预训练 2 层 ReLU Text GCN**。
- **链接：** https://doi.org/10.1109/TETC.2025.3558454
- **核对人与日期：** Gemini，2026-11-16
- **标题：** One-Spike SNN: Single-Spike Phase Coding With Base Manipulation for ANN-to-SNN Conversion Loss Minimization
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

##### 来自脉络 1 ANN→SNN 转换 的记录

**解决的难点**：攻克了传统 $B=2$ 相位编码在连续实数上因表达空隙导致的严重转换掉点，无需修改或重训源模型即可兼顾高稀疏度与精度，并给出了面向固定静态线性 GCN 的（论文自称）首个免训练转换实测。

**留下的局限**：（1）每个神经元虽平均仅发约 1 个脉冲，但为了扫过分数底数相位阶梯仍需 $T=16\sim 22$ 个串行时钟拍；（2）每个时钟拍需将发放阈值乘以分数底数 $B^{-t}$，带来额外硬件控制复杂度；（3）仅适用于 `ReLU` + 线性加权求和（静态 Text GCN 邻接乘），不支持 `MaxPool`、GELU 或动态 $k$-NN 建图。

**是否需要训练或微调**：否（纯训练后校准每层 99.9% 分位数缩放并套用分数底数两阶段相位编码）

**涉及的算子**：分数底数（$B=1.5$）两遍单脉冲相位编码（Phase Coding）、99.9% 激活分位数阈值校准、ReLU、卷积与全连接、静态归一化邻接矩阵乘法（Text GCN）

**关键数字**：在 5 个文本词—文档图基准（`20NG`, `R8`, `R52`, `Ohsumed`, `MR`）上免训练转换预训练 2 层 ReLU Text GCN（$B=1.5, T=16$，Section 4.3 Table 2，第 8 页），平均精度仅从 **81.98%** 微降至 **81.08%**（掉点 **0.90%**，其中 `R8` 从 97.07% 转为 **96.98%**），较传统 $B=2$ 相位编码减损 **89%** 并节能 **66%**；`ImageNet` `ResNet-34`（$B=1.5, T=22$）达 **71.50%**（源 73.30%），45nm ASIC 综合较浮点基线节能 **5.9×**（Section 4.2 & 4.4）。

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q1“有没有人把普通图网络免训练转成脉冲网络”的核心阳性证据：在静态固定图线性 ReLU Text GCN 上做过，但视觉图与非线性聚合仍属空白）

##### 来自脉络 2 脉冲图网络 的记录

**标题**：One-Spike SNN: Single-Spike Phase Coding With Base Manipulation for ANN-to-SNN Conversion Loss Minimization

**作者**：Sangwoo Hwang, Jaeha Kung

**发表处**：IEEE Transactions on Emerging Topics in Computing（IEEE TETC，2025 年 1–3 月刊，Vol. 13, No. 1, pp. 162–172，DOI: `10.1109/TETC.2024.3386893`；预印本 `arXiv:2403.08786`）

**链接**：[https://doi.org/10.1109/TETC.2024.3386893](https://doi.org/10.1109/TETC.2024.3386893) （预印本：[https://arxiv.org/abs/2403.08786](https://arxiv.org/abs/2403.08786) ）；代码：未公开

**核对深度**：全文

**一句话**：**本次检索范围内找到的唯一一篇对预训练 ReLU 图卷积网络（Text GCN）做免训练 ANN→SNN 权重转换的工作**——将每层 GCN 拆解为“特征线性变换”与“邻接矩阵乘”两个级联脉冲层，并用基数可调（$Q=1.3$）的单脉冲相位编码将 5 个文本图数据集的平均转换精度损失压至 0.90%。

**解决的难点**：证明了在固定邻接矩阵、线性求和聚合的 ReLU GCN 上，无需重训源模型即可通过“双矩阵乘法拆层 + 阈值中点平移 + 小基数单脉冲相位编码”在 $T=16$ 内完成高精度低功耗转换。

**留下的局限**：① 仅适用于**静态固定拓扑 + 线性矩阵乘聚合（**$\tilde{A}XW$**）+ 纯 ReLU 激活**的浅层（2 层拆为 4 层）非视觉文本图（Text GCN），完全未涉及视觉图骨干中的动态 $k$-NN 选邻居、`max` 聚合、GELU/SiLU 或归一化算子；② 层间存在因残余电位引发的伪脉冲（noise spikes），需在层与层之间插入等待步 $w$ 抑制误差传播（Section V-C2）。

**是否需要训练或微调**：**否**（真正免训练转换：仅在训练集上统计最大激活值做通道/层归一化，直接复制预训练 Text GCN 权重）

**涉及的算子**：通道级/层级最大激活权重归一化（Eq. 2）、单脉冲相位编码（每个隐藏神经元最多发放 1 次脉冲，输入层采用多脉冲二进制相位编码，Section III-A）、发放阈值中点平移 $V_\theta \to \frac{1+1/Q}{2}$（Eq. 4）、相位基数调节（Base Manipulation，$Q=1.3$，膜电位衰减系数 $\lambda_j = Q$）、**GCN 双步拆层（2 层 Text GCN 拆为 4 层 SNN：奇数层算消息传递 **$XW$**，偶数层乘固定归一化邻接矩阵 **$A$**，Section IV-C）**

**关键数字**：在 Section IV-C（*GCN-to-SNN Conversion*）及 **Table V（**`**\label{tab:GCN}**`**，**$T=16, Q=1.3$**）** 中，对预训练 2 层 Text GCN 免训练转换的精确结果为：`20NG`（ANN 86.27% → SNN **85.90%**，掉点 0.37%，能效提升 $\alpha=\mathbf{5.91\times}$）、`R52`（ANN 93.49% → SNN **92.24%**，掉点 1.25%，$\alpha=\mathbf{11.11\times}$）、`R8`（ANN 97.06% → SNN **96.44%**，掉点 0.62%，$\alpha=\mathbf{6.59\times}$）、`Ohsumed`（ANN 68.42% → SNN **66.95%**，掉点 1.47%，$\alpha=\mathbf{6.24\times}$）、`MR`（ANN 75.93% → SNN **75.09%**，掉点 0.84%，$\alpha=\mathbf{4.53\times}$）；5 个图数据集**平均转换精度损失仅 0.90%**，按 45nm Horowitz 模型（4.6 pJ MAC vs 0.9 pJ AC，Eq. 6）估算能效提升 **4.53×–11.11×**。

> 💭
> **与本方向的关系（判断）**：**直接相关（核心必引先例！它直接推翻了 Claude v1 草稿中“未见任何图网络免训练转换”的全称判断，同时其“仅支持固定图 + 线性矩阵乘 + ReLU Text GCN”的清晰边界恰恰凸显了本项目聚焦“视觉图动态拓扑与非线性聚合免训练转换”的不可替代性）**

### <a id="41b0e334-2e6f-8189-b3dc-df43ac9f4e6e"></a>Inference-Scale Conversion（2025）

- **发表处：** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition（CVPR 2025；预印本 `arXiv:2409.03368`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Tong Bu, Maohua Li, Zhaofei Yu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#inference-scale-conversion2025
- **代码：** [https://github.com/putshua/Inference-scale-ANN-SNN](https://github.com/putshua/Inference-scale-ANN-SNN)
- **年份：** 2025
- **一句话：** 提出仅需单次 ANN 推理级开销（RTX 4090 上 93 秒）的免训练转换框架：用局部学习率更新逐通道阈值，**利用交换律把 **`**MaxPool**`** 移到脉冲神经元之前由硬件比较器处理膜前连续值**，并估计首脉冲传播延迟做延迟区间统计，统一打通分类、分割、检测与视频分类。
- **链接：** https://arxiv.org/abs/2409.03368
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Inference-Scale Complexity in ANN-SNN Conversion for High-Performance and Low-Power Applications
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：无需像 `SNNC-AP` 那样对每个目标 $T$ 反复跑脉冲前向和权重微调，更巧妙绕开了二值脉冲流上做 `MaxPool` 的相位错位高估难题（注：论文第 5 页英文写 "replace all max-pooling layers with neuron layers"，结合紧随其后的 Theorem 2 实指**互换 **`**MaxPool**`** 层与神经元层的先后顺序**，即前置比较器池化而非用脉冲神经元拟合 `max`）。

**留下的局限**：**Theorem 2 的层序交换恒等式 **$\max_i\text{ReLU}(z_i)=\text{ReLU}(\max_i z_i)$** 严格依赖先线性卷积、紧接 ReLU 再接 **`**MaxPool**`** 且 **$\max z > 0$** 的 CNN 拓扑**；而在 ViG 的 `MRConv` 中，$\max_{j\in\mathcal{N}(i)}(x_j-x_i)$ 位于上一层激活之后、当前层线性映射之前且相对差值 $x_j-x_i$ 可正可负，不能直接套用层序对调，且该文仅支持 CNN，仍需 $T=32\sim 64$ 步。

**是否需要训练或微调**：否（直接加载 TorchVision 等开源预训练权重，仅需少量样本做推理级复杂度局部阈值搜索，一次校准通用于任意时间步 $T$）

**涉及的算子**：逐层/逐通道局部阈值平衡（CLTB）、**神经元前最大池化（Pre-Neuron Max Pooling，硬件比较器处理膜前连续值）**、首脉冲传播延迟估计与延迟求均值评估（Delayed Evaluation）、初始膜电位 $\theta^l/2$ 预充

**关键数字**：`ImageNet` 标准 TorchVision `ResNet-34`（源 **73.31%**）免训练转换仅耗时 **92.73 秒**（Appendix G Table S5，第 15 页），在 $T=32 / 64 / 128$ 达 **64.88% / 71.17% / 72.30%**（Table 2，第 7 页；若从无前置池化交换退化到基础局部平衡则在低步明显掉点）；密集预测与视频任务（Section 5.6 Table 3，第 8 页）：`Pascal VOC` `DeepLab-34`（源 58.95% mIoU）在 $T=64 / 128$ 达 **55.74% / 58.36%**，`MS COCO` 分割 `DeepLab-50`（源 63.01%）在 $T=128$ 达 **61.52%**，`MS COCO` 检测 `RetinaNet-50`（源 36.4% mAP）在 $T=64 / 128$ 达 **27.3% / 32.2%**，`S-Kinetics-400` 视频分类 `MC3-18`（源 63.52%）在 $T=64$ 达 **61.60%**。

> 💭
> **与本方向的关系（判断）**：直接相关（回答定向问题 Q10 及核查 Claude 草稿“改成神经元层”误读的关键文献；其“对连续累积量用硬件比较器取 `max` 再进脉冲编码”的思想可直接改造为图 `MRConv` 的节点前缀重构比较器规程）

### <a id="41b0e334-2e6f-81a6-ac26-fc23b4a2700b"></a>Adaptive Calibration（2025）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2025 Oral；预印本 `arXiv:2412.16219`）
- **脉络：** 1 ANN→SNN 转换,2 脉冲图网络
- **作者：** Ziqing Wang, Yuetong Fang, Jiahang Cao, Hongwei Ren, Renjing Xu
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#adaptive-calibration2025
- **代码：** [https://github.com/bic-L/burst-ann2snn](https://github.com/bic-L/burst-ann2snn)
- **年份：** 2025
- **一句话：** 用输出 KL 散度灵敏度分析为不同层自动分配最优脉冲簇发放上限（Burst-firing）并结合运行期自适应降阈值发放（AdaFire）与偏置校准，在约 5 分钟免训练校准内同时覆盖 2D 分类/检测/分割与改进版 PointNet 3D 点云任务。
- **链接：** https://arxiv.org/abs/2412.16219
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Adaptive Calibration: A Unified Conversion Framework of Spiking Neural Networks
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

##### 来自脉络 1 ANN→SNN 转换 的记录

**解决的难点**：同时解决了前期高激活截断（靠多层差异化脉冲簇上限释放）与初期沉默神经元欠发放（靠 AdaFire 动态微调阈值），并给出匹配商用芯片（Loihi 2、Xylo）脉冲簇指令的低开销部署路径。

**留下的局限**：核查其官方仓库 `3dtasks/models/model.py` 证实，为了转换 PointNet 分类与分割模型，作者**预先把原版 PointNet 中的全局 **`**torch.max**`** 对称池化全部硬改成了 **`**torch.mean**`** 平均池化并重新训练源模型**，仍未正面解决点集/图邻域 `max` 聚合算子的免重训转换。

**是否需要训练或微调**：部分（对本身不含 `MaxPool` 瓶颈的预训练 2D 网络完全免重训，校准仅约 0.09 小时；但对 3D PointNet 需先将 `max` 池化改为 `mean` 池化重训源 ANN）

**涉及的算子**：KL 灵敏度引导的分层脉冲簇（Burst-firing，`maxspike` 搜索）、自适应阈值衰减（AdaFire）、偏置校准、BatchNorm 折叠、改用 `mean` 池化的 PointNet

**关键数字**：校准耗时约 **0.09 小时**（Section 4）；在 `CIFAR-10` / `CIFAR-100` / `ImageNet` 上较基线降低 **70.1% / 60.3% / 43.1%** 能耗；多任务结果（Figure 1 及官方配置）：改进型 PointNet 3D 分类（$T=16, \text{maxspike}=4$）达约 **94.0%**（源约 96.0%），ShapeNet Part 3D 分割（$T=8$）达约 **74.75% mIoU**（源约 75.5%）。

> 💭
> **与本方向的关系（判断）**：直接相关（连接脉络一与脉络二的桥梁文献：既提供分层灵敏度分配脉冲位宽的工具，又从源码层面证实了现有转换法遇到几何 `max` 聚合时的回避做法）

##### 来自脉络 2 脉冲图网络 的记录

**标题**：Adaptive Calibration: A Unified Conversion Framework of Spiking Neural Networks

**作者**：Ziqing Wang, Yuetong Fang, Jiahang Cao, Hongwei Ren, Renjing Xu

**发表处**：Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2025 Oral；预印本 `arXiv:2412.16219`）

**链接**：[https://arxiv.org/abs/2412.16219](https://arxiv.org/abs/2412.16219) ；代码：[https://github.com/bic-L/burst-ann2snn](https://github.com/bic-L/burst-ann2snn)

**核对深度**：全文（含主文 PDF 全文与官方 GitHub 仓库 `3dtasks/` 全部模型及转换源码核验）

**一句话**：提出免训练的统一 ANN→SNN 校准转换框架，利用灵敏度分析为各层自动搜索最优脉冲簇（burst-firing）上限与自适应发放阈值（AdaFire），并将评测拓展到改进型 **PointNet 3D 点云分类与部件分割**。

**解决的难点**：无须重训即可在低时间步下利用商业类脑芯片（如 Loihi 2、Xylo）已支持的脉冲簇机制快速释放残余膜电位，兼顾 2D 分类/检测/分割与 3D 点云转换。

**留下的局限**：经核查官方开源仓库 `3dtasks/models/model.py`（文件头注释写明 `# Improved PointNet for ANN2SNN 3d Tasks`），其 3D 点云转换**同样被迫将原版 PointNet（含 STN3d、STNkd 与主干特征层）中的全局 **`**torch.max**`** 池化全部替换为 **`**torch.mean**`** 平均池化后再训练源 ANN**，并未解决原版 `max` 聚合或动态 $k$-NN 图网络的免重训直接转换。

**是否需要训练或微调**：部分（转换阶段本身完全免训练，仅需少量校准样本做 KL 散度灵敏度搜索与偏置校准；但对于 3D 点云任务，源 PointNet 须先改为 `mean` 池化架构再预训练）

**涉及的算子**：BatchNorm 折叠、分层灵敏度引导的脉冲簇上限搜索（Burst-firing，`maxspike`）、自适应阈值发放（AdaFire）、偏置校准、**改用 **`**torch.mean**`** 全局池化的 PointNet（**`**PointNetCls**`** 与 **`**PointNetDenseCls**`**）**

**关键数字**：转换校准仅需约 **0.09 小时**（README 与 Section 4）；在 `CIFAR-10` / `CIFAR-100` / `ImageNet` 上分别降低 **70.1% / 60.3% / 43.1%** 能耗；主文 Figure 1 多任务雷达图报告在改进型 PointNet 3D 点云分类（`3D-Cls`，默认 $T=16, \text{maxspike}=4$）上转换 SNN 达约 **94.0%**（源 ANN 约 96.0%），3D 部件分割（`3D-Seg`，ShapeNet Part，默认 $T=8, \text{maxspike}=4$）达约 **74.75% mIoU**（源 ANN 约 75.5%）。

> 💭
> **与本方向的关系（判断）**：直接相关（继 Lan et al. ICCV 2023 之后又一篇把免训练校准转换推广到 3D 点云网络的工作，且源码实锤了现有转换框架遇到点集 `max` 池化时仍依赖“改源网络为 `mean` 池化”）

### <a id="41b0e334-2e6f-81c0-a6bf-c95183e45597"></a>SpikedAttention（2024）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2024，Vol. 37，pp. 67422–67445，DOI: `10.52202/079017-2152`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Sangwoo Hwang, Seunghyun Lee, Dahoon Park, Donghun Lee, Jaeha Kung
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#spikedattention2024
- **代码：** [https://github.com/sangwoohwang/SpikedAttention](https://github.com/sangwoohwang/SpikedAttention)
- **年份：** 2024
- **一句话：** 通过维护 $Q, K$ 历史脉冲迹在脉冲域增量计算注意力点积，并用赢家导向脉冲移位（WOSS）电路在无需浮点指数单元的条件下全脉冲逼近 Softmax，还给出 45nm 硬件综合面积与功耗数据。
- **链接：** https://proceedings.neurips.cc/paper_files/paper/2024/hash/7c9341ad0263428b5057d92f4d88dfa0-Abstract-Conference.html
- **核对人与日期：** Gemini，2026-11-16
- **标题：** SpikedAttention: Training-Free and Fully Spike-Driven Transformer-to-SNN Conversion with Winner-Oriented Spike Shift for Softmax Operation
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 部分

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：实现了自注意力 $Q K^\top$ 点积、Softmax 与加权 $V$ 的纯脉冲硬件流水线，证明专用 WOSS Softmax 单元仅占加速器总面积的 9.88%。

**留下的局限**：**标题虽写 Training-Free，但全文不支持标准 Transformer 的 **`**LayerNorm**`** 和 **`**GELU**`——论文第 8–10 页（Section 5.1–5.2 与 Section 6 Limitations）明确交代，被转源模型必须是**预先把 **`**LayerNorm**`** 全换成 **`**BatchNorm**`**、把 **`**GELU**`** 全换成 **`**ReLU**`** 重新训练好的定制变体**（如 `Swin-T (BN)` 与 `MA-BERT`），无法直接转换现成开源的 GELU/LN 视觉骨干！同时推理仍需 $T=16\sim 40$ 步。

**是否需要训练或微调**：部分（转换过程本身免训练，但**要求源 Transformer 预先以 **`**BatchNorm + ReLU**`** 替代 **`**LayerNorm + GELU**`** 完成训练**）

**涉及的算子**：分数底数（$B=1.15$）相位编码、基于脉冲迹（Spike Trace）的双脉冲流点积乘法、赢家导向脉冲移位 Softmax（`WOSS`）、BatchNorm 折叠、ReLU

**关键数字**：`ImageNet-1K` 上转换定制 `Swin-T (BN)`（源 **80.6%**，$T=40, B=1.15$，Section 5.1 Table 1，第 8 页）达 **80.0%**（掉 0.6%），估算能耗从 45.4 mJ 降至 **25.6 mJ**（节省 **42%**）；`GLUE` 基准转换定制 `MA-BERT`（$T=16\sim 24$，Table 3，第 9 页）平均仅掉 **0.3%**、节能 **58%**；45nm CMOS 综合显示 `WOSS` 模块仅增加 **9.88%** 芯片面积与 **12.35%** 功耗（Appendix Table 4，第 15 页）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（一方面其 `WOSS` 赢家移位电路对图注意力 GAT（M2）的边 Softmax 脉冲化极具参考价值；另一方面提醒我们核查“免训练转换”论文时必须紧盯源模型是否偷偷把 LN/GELU 改成了 BN/ReLU——好在主流卷积式 ViG 教师恰好原生采用 `BatchNorm`！）

### <a id="41b0e334-2e6f-81d8-b1d1-ccbe05acdde2"></a>DCGS（2025）

- **发表处：** Proceedings of the 42nd International Conference on Machine Learning（ICML 2025，PMLR Vol. 267，pp. 25235–25264；预印本 `arXiv:2503.00301`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Zihan Huang, Wei Fang, Tong Bu, Peng Xue, Zecheng Hao, Wenxuan Liu, Yuanhong Tang, Zhaofei Yu, Tiejun Huang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#dcgs2025
- **代码：** [https://github.com/h-z-h-cell/ANN-to-SNN-DCGS](https://github.com/h-z-h-cell/ANN-to-SNN-DCGS)
- **年份：** 2025
- **一句话：** 将首步密集激活锚定（AC）、每步对输出变化量做正负 $2n$ 级二次幂阈值编码的差分编码分级脉冲（DCGS），以及逐通道异步网格搜索阈值校准（CAT）相结合，把大型 CNN 与视觉 Transformer 的免训练转换推至 $T=2\sim 4$ 步近无损精度。
- **链接：** https://arxiv.org/abs/2503.00301
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Differential Coding for Training-Free ANN-to-SNN Conversion（`arXiv:2503.00301v3` 与 PDF 第 1 页；本条早先误写为另一标题，复查时已更正）
- **核对深度：** 全文
- **与本方向的关系：** 直接相关
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：消除了传统率编码在 $T=2\sim 4$ 超低步下的严重量化截断误差与层间延迟失配，用“只对相邻时间步的增量差发放带符号分级脉冲”换取高稀疏度。

**留下的局限**：（1）**源码实查不支持通用 **`**MaxPool**`** 与图算子**：`neurons/nonlinear_neuron.py` 第 22–114 行写明只要 `kernel_size != stride`（如 ResNet 首层 $3\times 3, s=2$），就绕过脉冲化直接对累积激活调浮点 `self.maxpool(x)`，仅对规则无重叠网格 $k=s$ 实现 `UniformUnpooling`；（2）GELU、LayerNorm、Softmax 依赖 `exp_comp_neuron` 在每步用浮点重算前缀期望差（非纯脉冲电路）；（3）能耗估算把任意多阈值分级脉冲按单次 `0.9 pJ` 累加计费且漏计模拟非线性层与多比较器开销；（4）官方仓库**未设置任何开源许可证**（默认保留全部权利），且缺失论文汇报的分割代码。

**是否需要训练或微调**：否（完全免训练，仅用少量校准集前向搜索阈值缩放因子，支持 $\times 1$ 与 $\times 2$ 网格搜索预算）

**涉及的算子**：激活中心化首步稠密锚定（`AtNeuron`）、正负对称 $2n$ 级二次幂阈值差分分级脉冲神经元（$\pm\theta/2^{i-1}, i=1,\dots,n$）、逐通道异步阈值搜索（CAT）、浮点期望补偿模块（`exp_comp_neuron` 处理 GELU / LayerNorm / Softmax）、脉冲矩阵乘补偿（`ProductNeuron`）、规则网格 `MaxPool2d`（$k=s$ 时 `UniformUnpooling`，$k\neq s$ 时退回浮点 `MaxPool2d`）

**关键数字**：`ImageNet-1K` 上（$n=8$ 即正负共 16 级阈值，Appendix K Table 6 & Appendix L Table 7），`EVA02-Large`（源 **90.05%**）在 $T=2 / 4 / 8$ 达 **88.25% / 89.72% / 89.90%**（能耗比 ER 为 **0.31 / 0.64 / 1.15**）；`ViT-Large`（源 **85.84%**）在 $T=4$ 达 **85.45%**（ER=0.46）；`ViT-Base`（源 **84.54%**）在 $T=4$ 达 **83.98%**（ER=0.54）；`ViT-Small`（源 **81.38%**）在 $T=4 / 8$ 达 **81.11% / 81.43%**（ER=0.62 / 1.05）；`ResNet-34`（源 **76.42%**，$\times 2$ 搜索）在 $T=4 / 8$ 达 **76.24% / 76.39%**（ER=0.32 / 0.50）；`MS COCO` 检测 `Mask R-CNN`（源 45.7% mAP）在 $T=4$ 达 **44.1%**（Table 3，第 7 页）；`ADE20K` 分割 `EVA-02+UperNet`（源 53.1% mIoU）在 $T=4$ 达 **52.18%**（Table 4，第 8 页）。

> 💭
> **与本方向的关系（判断）**：直接相关（本项目最重要的免训练超低步转换参照基线；对其论文与源码差异的核查见定向问题 Q5）

### <a id="41b0e334-2e6f-81e5-b9ea-f84dbb01a5cf"></a>MBE 脉冲浮点转换（2026）

- **发表处：** Proceedings of the AAAI Conference on Artificial Intelligence（AAAI 2026；预印本 `arXiv:2508.07710`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Jingya Wang, Xin Deng, Wenjie Wei, Dehao Zhang, Shuai Wang, Qian Sun, Jieyuan Zhang, Hanwen Liu, Ning Xie, Malu Zhang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#mbe-脉冲浮点转换2026
- **代码：** 未公开
- **年份：** 2026
- **一句话：** 用离线在合成实数点上预拟合的多基指数衰减（MBE）脉冲神经元传输精确浮点值，配合外积脉冲乘法及 IEEE-754 指数/尾数位拆分，（论文自称）首次在不重训源模型且不回退主机模拟浮点的前提下将 ViT、RoBERTa 与 GPT-2 中的 GELU、LayerNorm、Softmax 全部脉冲化。
- **链接：** https://arxiv.org/abs/2508.07710
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Training-Free ANN-to-SNN Conversion for High-Performance Spiking Transformers（PDF 第 1 页与 arXiv API；本条早先误写为另一标题，复查时已更正）
- **核对深度：** 全文
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：攻克了免训练转换中二值脉冲无法精确执行动态两激活乘法（$Q\cdot K^\top$）以及指数、平方根倒数等超越非线性运算的瓶颈，无需接触任何源任务训练数据。

**留下的局限**：时间步压到极低时精度雪崩——在 `ViT-M/16` 上 $T=16$ 虽达 85.31%，但 $T=10$ 即暴跌至 21.99%、$T=8$ 崩至 1.17%（Table 4）；且全文仅处理连续算术非线性，完全未涉及离散 `MaxPool` 或动态 $k$-NN 排序选邻居。

**是否需要训练或微调**：否（仅在 $M=10{,}000$ 个合成标量点上离线拟合一次 $N=4$ 个基神经元的通用系数，对下游预训练模型完全零训练、零数据校准）

**涉及的算子**：多基指数衰减神经元（MBE）、Hadamard 外积脉冲浮点乘法、基于 $e^x=2^{x\log_2 e}$ 与 IEEE-754 阶码/尾数拆分的脉冲 Softmax 与脉冲 LayerNorm、GELU / SiLU / ReLU

**关键数字**：`ImageNet-1K` 上（Section 5.2 Table 1，第 6 页），$T=16$ 时 `ViT-B/16` 从源 ANN **83.44%** 转为 **83.00%**（掉 0.44%），`ViT-M/16` 从 **85.95%** 转为 **85.31%**（掉 0.64%；但 $T=10$ 为 **21.99%**、$T=8$ 为 **1.17%**，Section 5.4 Table 4，第 7 页）；CNN 在 $T=10$ 时 `ResNet-34` 达 **75.57%**（源 76.31%）、`VGG-16` 达 **72.61%**（源 73.37%）；NLP 上 $T=16$ 时 `RoBERTa-Large` 在 `SST-2` 达 **95.98%**（源 96.22%，Table 2），`GPT-2` 在 `WikiText-2` 困惑度为 **22.69**（源 22.34，Table 3）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（为视觉图骨干或混合图—注意力模型中的 GELU、LayerNorm 与边注意力 Softmax 提供了纯脉冲免训练逼近方案，但需警惕其在 $T\le 8$ 下的精度崩溃）

### <a id="41b0e334-2e6f-81f1-bee9-ee39e6a7cb31"></a>Adaptive Fission（2025）

- **发表处：** Advances in Neural Information Processing Systems（NeurIPS 2025 Poster，OpenReview ID: `2zZzdAMyYi`）
- **脉络：** 1 ANN→SNN 转换
- **作者：** Yizhou Jiang, Feng Chen, Yihan Li, Yuqian Liu, Haichuan Gao, Tianren Zhang, Ying Fang
- **仓库条目：** https://github.com/Casey-sketch-cyber/gnn2gsnn/blob/main/literature/01-ann2snn-conversion.md#adaptive-fission2025
- **代码：** 未公开
- **年份：** 2025
- **一句话：** 提出一种广义群体编码式的训练后神经元“自适应裂变”技术，按误差敏感度只把少数高敏感神经元拆分为具有不同尺度与权重的二值脉冲子神经元群，在不重训的前提下用极小空间冗余换取大幅延迟与功耗下降。
- **链接：** https://openreview.net/forum?id=2zZzdAMyYi
- **核对人与日期：** Gemini，2026-11-16
- **标题：** Adaptive Fission: Post-training Encoding for Low-latency Spike Neural Networks
- **核对深度：** 仅摘要
- **与本方向的关系：** 可借用的技术
- **是否需要训练或微调：** 否

> ℹ️
> 下面内容照搬任务 01 的核查记录（仓库 literature/ 目录）。“与本方向的关系”一栏是核查人的判断，不是事实；文中“首个”“首次”等说法是论文自称。

**解决的难点**：在不依赖硬件原生多位分级脉冲的前提下，仅靠纯二值脉冲神经元按需分配等效量化分辨率，缓解传统率编码对高时间步的依赖。

**留下的局限**：会改变高敏感通道的神经元扇出拓扑结构；未涉及图神经网络中消息传递算子、不规则邻接或动态 $k$-NN 建图的转换。

**是否需要训练或微调**：否（纯训练后编码与神经元拆分，无需重训或微调）

**涉及的算子**：敏感度引导的神经元自适应裂变（群体多尺度二值脉冲编码）、按需阈值与权重分配

**关键数字**：据 OpenReview 官方摘要披露，在类脑硬件实测中可在不降低精度的前提下实现最高 **80%** 的推理延迟与功耗缩减（Abstract；具体各数据集逐表数值因未获取全文记为未核实）。

> 💭
> **与本方向的关系（判断）**：可借用的技术（若目标硬件不支持 DCGS 式的分级/多阈值脉冲，可用“高敏感通道神经元裂变”在纯二值脉冲芯片上模拟等效多级精度）
