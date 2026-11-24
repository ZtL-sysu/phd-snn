# 10 个 GNN→SNN idea 的全量实验报告

## 一、任务与执行口径

本报告按 `f-research-v1` 的基线先行、冻结门槛、原始结果留痕和失败不改口径原则，在本机 NVIDIA RTX 3060 12GB 上顺序执行了 10 个 idea。数据包括 DAVIS-2017 真实动作片段、MaleCNS 真实细胞坐标、FlyWire 真实生物边权，以及 Cora/Citeseer/PubMed/Chameleon/Squirrel/OGBN-Arxiv 图与冻结 GCN checkpoint。所有新选择均使用固定 train/validation/test 划分，不用官方测试集调参。

结果不是“10 个 idea 全部成功”。9 个达到各自的强门槛；SIGN-C04 的“异配图上至少 +2pp”假设被否证。事件数、槽位数和比特数均不当作硬件能耗。

## 二、结果总览

| Idea | 核心故事 | 最终实验结果 | 强门槛 |
|---|---|---|---|
| DYN-C01 | 用首帧+因果状态残差替代重复绝对状态 | 5 seeds 解码后精度与 raw 完全相同；重复状态非零事件减少 20.52% | 通过 |
| EQ-C02 | 径向幅值事件保留坐标方向与旋转等变性 | 旋转误差 2.91e-11；量化误差 3.78%；balanced accuracy 25.99% vs raw 24.35% | 通过 |
| PERM-C03 | 图事件池化必须具有置换证书 | 3 图×5 permutations 最大误差 1.11e-16；naive 控制误差 0.50–0.95 | 通过 |
| SIGN-C04 | 兴奋/抑制双库保留负消息 | 精确重构，但 Chameleon/Squirrel 仅 +0.46/+0.48pp，未达 +2pp | **失败** |
| LR-C05 | 算子对齐的低秩图消息事件 | rank128 压缩 7.32/8.99/11.64×；SVD logit error 比 random 低 3.79–6.20× | 通过 |
| EDGE-C06 | 生物边权的非均匀低比特事件字母表 | 6-bit log error 2.82%，存储 5.33×，比 uniform 低 83.2% error | 通过 |
| CERT-C11 | 仿射图聚合误差证书 | 100% coverage；width/RMS 3.06–6.72；比 global bound 紧 79.7–85.1% | 通过 |
| POS-C13 | hop-position 的混合事件编码 | 8-level Lloyd + 0.5% escapes：error 2.46/3.06%，存储 10.17×，accuracy +2.13/+2.20pp | 通过 |
| DLY-C14 | 按传播延迟调度因果残差 | 正确 delay 精确重构；wrong-delay error 4.33%；事件减少 20.52% | 通过 |
| READ-C18 | top-two margin-pair 图读出 | 6 图×3 seeds 预测保持 100%；输出槽中位减少 63.33% | 通过 |

## 三、逐项故事与实验结论

### 1. DYN-C01：因果残差事件

**问题与故事。** 时序图状态在多个 tick 重复传输会造成事件浪费；但普通差分编码若丢失首帧就不是无损表示。这里把“首帧状态 + 后续状态差分”作为因果码，并用未来帧扰动检验前缀不泄漏。

**实验。** DAVIS-2017 728 个 8 帧动作片段，5 个固定 stratified splits；RTX3060 linear probes 比较 raw、首帧+残差、直接残差几何和错误 delay。

**结果。** 解码后 5/5 seeds 精度差均为 0，说明编码无损；重复状态的非零事件减少 20.52%。但直接在残差坐标上训练 probe 的结果波动为 −7.53 到 +10.96pp，说明该码保持信息但不保持线性分类器的优化几何。

**结论。** 支持“无损、更省重复事件”的窄结论；不支持“残差表示本身提升分类”，也未覆盖真正 dynamic-edge GNN。

### 2. EQ-C02：旋转等变径向事件

**问题与故事。** 坐标 GNN 的 spike 量化若逐分量进行会破坏旋转关系。径向编码把幅值离散、方向连续保留，目标是让旋转与事件重构交换。

**实验。** 8,000 个有类型 MaleCNS soma 坐标，8 类任务，5 splits；比较 raw、component-uniform、radial，5 个 z 轴旋转。

**结果。** radial error 3.78%，旋转最大误差 2.91e-11；balanced accuracy 25.99%，比 raw 24.35% 高 1.64pp，比 component-uniform 24.49% 高 1.50pp。

**结论。** 坐标事件层的等变性和精度通过；仍不能替代完整 E(3)/SE(3) equivariant GNN conversion 实验。

### 3. PERM-C03：图置换证书

**问题与故事。** 图转换中的 scatter/reduction 若依赖节点顺序，会把软件调度误差混进神经编码误差。该 idea 将 permutation equivariance 作为转换正确性证书。

**实验。** Cora、Chameleon、Squirrel，各 5 个固定 permutations；deterministic pooling 对比故意保留旧顺序的 naive 控制。

**结果。** deterministic 最大误差 1.11e-16；naive 在三类图上分别错误 0.50、0.90、0.95。

**结论。** 证书强且可复现，但独立论文价值偏系统/正确性；最好与更完整转换框架合并。

### 4. SIGN-C04：兴奋/抑制消息双库

**问题与故事。** 异配图含负向/抑制消息，直接 ReLU/rate coding 可能抹掉证据。正负双库在数学上可精确重构 signed preactivation。

**实验。** Chameleon、Squirrel、Cora 的 frozen GCN signed messages；signed、absolute、positive-only 三种表示，同一 splits 和 GPU probe。

**结果。** Chameleon 58.86% vs 58.40% abs / 57.52% positive；Squirrel 41.00% vs 39.36% / 40.51%；Cora 68.91% 略低于 unsigned controls。两个异配图只有 +0.46/+0.48pp。

**结论。** “精确保留负消息”成立，但“带来 ≥2pp 下游收益”的强假设失败。负结果必须保留；不能用 signed-spike 先例不足来弥补实验增益不足。

### 5. LR-C05：算子对齐低秩消息事件

**问题与故事。** 原始聚合消息 `A X` 维度高，但主要下游方向可能低秩。SVD 对齐应比同秩 random projection 更好地保留 hidden preactivation。

**实验。** Cora/Chameleon/Squirrel 的完整 raw messages，ranks 8/16/32/64/128；SVD 与 random projection 同秩同预算，CUDA 分解。

**结果。** rank128 压缩 7.32×、8.99×、11.64×；SVD logit error 0.091/0.182/0.330，而 random 为 0.566/0.935/1.251。

**结论。** 强证据表明 operator-aligned low-rank 优于 generic random；但 generic graph quantization/low-rank 先例很多，论文必须强调 frozen conversion 与 equal-budget 对照。

### 6. EDGE-C06：生物边权低比特事件

**问题与故事。** FlyWire 等生物图边权高度长尾，uniform alphabet 浪费码字。对数压缩应更符合权重分布。

**实验。** 385,946 个有限 `syn_count`，2–6 bits；uniform/log/quantile equal-bit 对照，并比较分组 weighted aggregation。

**结果。** 6-bit log error 2.82%，比 uniform 16.72% 低 83.2%；5.33× bit storage reduction，aggregate error 0.87%。

**结论。** 非均匀字母表优势很强；仍只是存储/保真结果，不能宣称硬件能效。

### 7. CERT-C11：仿射图聚合证书

**问题与故事。** 转换量化误差经过邻接聚合和线性权重后会被放大。逐输出列的 L1 传播比单个 global scalar bound 更紧。

**实验。** Cora/Chameleon/Squirrel，4/8 levels；proposed envelope 与 global scalar bound，检查 coverage、width/RMS、tightening。

**结果。** 6 个设置 coverage 都是 100%；width/RMS 3.06–6.72；比 global bound 紧 79.7–85.1%。

**结论。** 在所测 quantizer/operator 内证书有效且明显更紧。下一步应测更复杂 GNN 和分布外扰动。

### 8. POS-C13：hop-position 混合事件

**问题与故事。** hop positional messages 分布不均，uniform/per-channel 均匀码本误差偏大。8-level Lloyd 加少量 exact escapes 用很小的稀疏代价消除大误差。

**实验。** Chameleon/Squirrel 的 1–3 hop features；raw、global uniform、per-channel uniform、quantile、Lloyd、Lloyd+0.5% escapes。

**结果。** hybrid error 2.46%/3.06%，平均 3.145 bits/element，存储减少 10.17×；balanced accuracy 比 raw 高 2.13/2.20pp。

**结论。** 混合码本通过强门槛；需要与 SpikeZIP/ECMT 类 graph-transformer conversion 做更直接对照。

### 9. DLY-C14：延迟对齐因果残差

**问题与故事。** 不同传播路径的 residual event 需要对齐延迟，否则正确性与事件稀疏性无法同时成立。

**实验。** 与 DYN 相同的 DAVIS splits；delay 0/1/2 解码、wrong-delay control、未来扰动。

**结果。** 正确 delay 精确重构，5 seeds 解码 accuracy 与 raw 相同；重复事件减少 20.52%；wrong-delay error 4.33%。

**结论。** 支持 delay schedule 的窄结论。与 DYN 共用数据，不能包装成两个独立 dynamic-graph 性能论文。

### 10. READ-C18：top-two margin-pair readout

**问题与故事。** 图分类读出无需为所有类持续发事件；leader 与最强竞争者的 signed margin 可以保留原 argmax 并减少输出槽。

**实验。** 6 图×3 checkpoint seeds 的 T=2 logits；full/top2/top1、margin bins、输出槽成本。

**结果。** top2 对 full-output argmax 保持率 100%，输出槽中位减少 63.33%。top1 控制用于暴露近 margin 失败。

**结论。** 输出层压缩证据强，但 argmax preservation 有一定恒真性；论文价值取决于 calibration、near-margin failure 和真实 readout hardware/accounting。

## 四、总体科学判断

最强的三条证据链是：LR 的等预算低秩对照、EDGE 的长尾边权非均匀量化、CERT 的误差证书。POS 的 hybrid codebook 也很强，但 prior-art 距离较近。PERM/READ 是高质量 correctness/component 结果，适合作为系统论文模块。DYN/DLY 证明了编码与调度性质，但缺少动态边 GNN 桥梁。SIGN 是明确负结果。

因此，不建议把 10 项包装成一篇“十项均成功”的论文。更合理的路线是：把 LR+EDGE+CERT 组合成一个“图消息压缩与证书”主论文；把 POS+READ 组合成“图位置/读出事件编码”论文；DYN/DLY 在补上真实 temporal-edge GNN 后再立项；SIGN 暂停下游收益主张。
