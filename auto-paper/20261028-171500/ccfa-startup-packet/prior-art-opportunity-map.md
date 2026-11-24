# Prior-Art & Opportunity Map（CCFA startup）

## 集群 1：吴晓锋的转换/低延迟 SNN（方法基座，必引）
- **FTBC**（Wu et al., ECCV 2024）*: Forward Temporal Bias Correction for ANN-SNN Conversion，CIFAR-10/100、ImageNet，代码已开源。→ D1/D4 的校准基线。
- **Temporal Misalignment + TPP Spiking Neuron**（Wu et al., 主贡献）*: 概率脉冲神经元，超低延迟匹配 ANN 精度（ImageNet）。→ D1/D3/D4 的核心机制来源。
- **Temporal Misinformation and Conversion through Probabilistic Spiking Neurons**（Wu et al.）*。
- **Parallel ANN-SNN Conversion**（Faster and Stronger, ICML 2025）: 并行脉冲计算 + 转换，超低延迟。→ D1/D4 的并行校准基线。
- *注：TPP/时序错位两篇的精确 venue 需在下轮核实（检索显示为 Wu 代表工作，疑似 NeurIPS/ICLR/AAAI 级别）。

## 集群 2：序列/事件流转换（证明"转换在 non-vision 会失效"）
- **Kugele et al., 2020, Front. Neurosci**: 序列处理转换需 delay-matching（N-MNIST/CIFAR10-DVS/DvsGesture）。→ D2/D4 的"转换不直接适用序列"证据。
- **事件相机 SNN 综述/应用**：Spiking-YOLO、事件视觉——D2 的灵感与对比。

## 集群 3：脉冲图神经网络（D1 的差异化来源）
- 现有**脉冲 GNN 多为直训**（替代梯度），如 SpikeGraph / 各类 spiking GCN 变体（需 G4 时精确检索核对）。
- **空白**：预训练 GNN 的 **ANN→SNN 转换**几乎无人做；图的异步脉冲聚合引入的"邻域时序错位"未被校准。→ D1 的差异化路线。

## 集群 4：EEG / 生物信号 SNN（D3 的差异化来源）
- **Li et al., 2024, Computers in Biology and Medicine (vol 183, 109225)**: 实时亚毫瓦癫痫检测 SNN，部署 Xylo 神经形态芯片，93.3%/92.9% acc，87.4µW+287.9µW。→ D3 的强基线/对比。
- **Loihi EEG/ECG 边缘智能**（eccsubmit 2024）: STDP 无监督 + 神经形态。→ D3 的对比（直训 vs 转换）。
- **空白**：用 **ANN→SNN 转换 + 概率神经元**做跨被试低延迟 EEG，区别于上述直训/STDP 路线。→ D3 差异化。

## 公开数据集（G1 候选）
- 图：Cora、CiteSeer、PubMed（节点分类，公开直接下载）；xhf 自有洪涝图（P-SGCN 数据，私有但可用）。
- EEG：SEED、SEED-IV、SEED-VIG（公开/多需简单注册）；BCI Competition；xhf 已用 SADT/MPD-DF/SEED-VIG。
- 事件/动态图：N-MNIST、CIFAR10-DVS、DvsGesture（事件视觉，公开）；动态图见 D2 筛选。

## 差异化总览
| 方向 | 最强相近工作 | 本文差异 |
|------|--------------|----------|
| D1 | 直训脉冲 GNN；图像转换(FTBC) | 首个 GNN 的 ANN→SNN 转换 + 邻域时序错位校准 |
| D3 | Li2024 直训 EEG SNN；Loihi STDP | 转换 + 概率神经元 + 跨被试低延迟边缘 |
| D4 | FTBC/并行转换（视觉） | 统一 non-vision 转换框架与基准 |
