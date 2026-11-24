# 独立 CCFA 评审

Review execution: `independent-agent`. 评审 Agent 只读冻结证据包，不修改文件。

**评审口径**
- 目标：Q2+ 期刊或强专门会议；评分表示当前独立论文开发就绪度，不是录取概率。
- 文献依据：仅使用冻结包中的 literature matrix；未进行外部补充检索，因此新颖性判断不赋予高置信度。
- 总体结论：**作为内部机制审计成立；作为 10 篇独立论文组合不成立。**
- 标称结果为 9 个 strong-pass、1 个 strong-fail，但若严格扣除构造恒等式、缺失桥接和弱基线，真正达到 `accept-to-develop` 的方案为 **0 个**。

## 排名

| 排名 | ID | 分数 | 置信度 | 建议 |
|---:|---|---:|---|---|
| 1 | LR-C05 | 5.7/10 | medium | revise |
| 2 | CERT-C11 | 5.2/10 | medium | revise |
| 3 | POS-C13 | 5.0/10 | medium | revise |
| 4 | EDGE-C06 | 4.5/10 | medium | pivot-with-rescue |
| 5 | EQ-C02 | 4.2/10 | medium | pivot-with-rescue |
| 6 | DYN-C01 | 3.4/10 | high | pivot-with-rescue |
| 7 | PERM-C03 | 3.1/10 | medium | pivot-with-rescue |
| 8 | READ-C18 | 2.7/10 | high | reject-current-form |
| 9 | DLY-C14 | 2.3/10 | high | reject-current-form |
| 10 | SIGN-C04 | 1.9/10 | high | reject-current-form |

## 逐项评审

### 1. LR-C05 — 5.7/10，confidence: medium
- **故事强度：中。** “算子对齐的低秩消息编码”问题明确；但冻结实验实际只比较 SVD 截断和随机投影，没有实现故事中的 residual events。
- **证据强度：中。** 三个图上 rank128 达到 7.32×/8.99×/11.64× 压缩，SVD logit error 比随机投影低 3.79–6.20×；但只有 checkpoint seed 0，没有下游分类、SNN 事件或运行成本，随机投影也不是强低秩基线。
- **先验风险：高。** A²Q、AdaQP 已覆盖图消息量化，One-Spike/ASGCN 覆盖图转换；剩余增量仅是 equal-rank operator alignment。
- **建议：`revise`。** 当前证据只支持“低秩压缩保真度筛选”。未来工作不计分：补 residual-event 路径、强低秩基线、端到端转换和任务/延迟/内存结果。

### 2. CERT-C11 — 5.2/10，confidence: medium
- **故事强度：中高。** 算子感知误差证书比普通压缩更具理论辨识度。
- **证据强度：中。** 3 图×2 量化级上 width/RMS 为 3.06–6.72，较 global bound 收紧 79.7–85.1%；但 100% coverage 来自用全量最大误差构造上界，因此是构造保证，不是独立统计覆盖。global comparator 又把所有输出维度合并为一个明显更松的标量界。
- **先验风险：中。** supplied matrix 没有直接证书论文命中，但这不能证明高新颖性；SEENN/Fast-SNN 仍限制转换误差与选择声明。
- **建议：`revise`。** 当前证据支持单个 affine map 的误差包络。未来工作不计分：扩展到多层、非线性激活、邻接传播，并与逐层 Lipschitz/范数证书比较。

### 3. POS-C13 — 5.0/10，confidence: medium
- **故事强度：中高。** hop-position 编码是明确的图特异机制，而不是普通图像转换。
- **证据强度：中偏低。** 两图上误差 2.46%/3.06%、存储降低 10.17×、balanced accuracy 较 raw 提升 2.13/2.20 pp；但只有一个 split seed，无区间估计，而且 mandatory permutation/shuffled-hop 控制未出现在最终 raw JSON。hybrid 也不是准确率最高的量化变体。
- **先验风险：高。** SpikeGraphormer、SpikeZIP-TF、ECMT、TTFSFormer 已覆盖位置编码/Transformer 转换；剩余增量较窄。
- **建议：`revise`。** nominal strong-pass 不能完整采信。未来工作不计分：补排列与 shuffled-hop 证书、多 seed/CI，并进入真实 graph-transformer→SNN 转换。

### 4. EDGE-C06 — 4.5/10，confidence: medium
- **故事强度：中。** FlyWire 生物边权场景具体，但机制仍是标量非均匀量化。
- **证据强度：中。** 385,946 个权重上，6-bit log coding 达到 2.82% error、5.33× storage reduction，并比 equal-bit uniform 好 83.2%；但聚合检验是合成分组，不含真实邻域任务、稀疏图通信或硬件结果。
- **先验风险：高。** A²Q、AdaQP、Fast-SNN 已覆盖图量化/压缩；“6-bit”本身没有新颖性。
- **建议：`pivot-with-rescue`。** 保留生物边权问题，转向真实 connectome graph task，并比较图量化与转换基线。未来工作不计分：端到端精度、消息流量和硬件延迟/能耗。

### 5. EQ-C02 — 4.2/10，confidence: medium
- **故事强度：中。** radial magnitude + direction 是简洁的等变事件编码。
- **证据强度：中偏低。** 5 splits 上量化误差 3.78%，平均 balanced accuracy 比 raw/component 高 1.64/1.50 pp；但旋转误差 2.91e-11 基本由构造保证，且实验只是坐标线性 probe，不是 E(3) GNN 消息传递。
- **先验风险：中高。** MSG、GC-LIF、SGSPose 已覆盖 geometric/equivariant spiking 模型。
- **建议：`pivot-with-rescue`。** 当前只支持 coordinate encoder。未来工作不计分：端到端 E(3) teacher、旋转/反射消息层及完整 equivariant GNN 转换。

### 6. DYN-C01 — 3.4/10，confidence: high
- **故事强度：中。** causal residual state coding 直观，但被包装成动态图转换时明显超出证据。
- **证据强度：低。** 20.52% 是帧状态非零差分下降，不是 SNN spike cost；所谓 decoded exactness 将 `decoded` 直接设为 raw，因而准确性完全相同属于恒等式。direct residual probe 还在 −7.53 至 +10.96 pp 间波动。
- **先验风险：高。** ASGCN、SpikeNet、Dy-SIGN、SiGNN 已覆盖 event/temporal graph。
- **建议：`pivot-with-rescue`。** 当前证据只支持差分编码的稀疏性。未来工作不计分：真实 dynamic-edge GNN、实际事件流、因果延迟与端到端任务。

### 7. PERM-C03 — 3.1/10，confidence: medium
- **故事强度：低到中。** 排列正确性可作为转换系统质量控制，但不足以独立成方法论文。
- **证据强度：低到中。** 3 图×5 permutations 的 deterministic error ≤1.11e-16，naive error 0.50–0.95；然而 deterministic 只是验证 `P(AX)=PA(P⁻¹...)` 的标准矩阵等变性，naive control 则故意不排列输出。
- **先验风险：中。** supplied matrix 无直接命中，但标准 scatter/reduction 的概念新颖性低。
- **建议：`pivot-with-rescue`。** 转成转换 scheduler/pooling correctness certificate，并测量发现真实实现错误的能力和开销。

### 8. READ-C18 — 2.7/10，confidence: high
- **故事强度：低到中。** top-two margin-pair 是清晰的输出编码，但贡献边界很窄。
- **证据强度：低。** 100% top2 preservation 是定义保证，因为 top2 必含 argmax；top1 也被直接定义为同一个 `argmax(logits)`，所以 margin bins 的 zero failure 同样是恒等式。63.33% slot reduction 基本由 `1-2/C` 决定。
- **先验风险：中高。** One-Spike 已是 output-code anchor，SEENN 覆盖 early-exit/selection。
- **建议：`reject-current-form`。** 未来工作不计分：测试噪声/量化后的 top-k、真实传输延迟、校准误差和 lossy failure，而非 argmax 恒等式。

### 9. DLY-C14 — 2.3/10，confidence: high
- **故事强度：低到中。** propagation-delay scheduling 理论上独立于 residual sparsity。
- **证据强度：很低。** DLY 与 DYN 调用同一 runner，最终 rows 完全相同；delay1/2 reconstruction error 被硬编码为 0，wrong-delay 只是 `np.roll` 诊断。没有 dynamic edge 或真实传播延迟。
- **先验风险：极高。** Delay-DSGN 已直接研究 delayed dynamic SNN，ASGCN/Dy-SIGN 又覆盖事件动态图。
- **建议：`reject-current-form`。** 未来工作不计分：必须在真实 temporal graph 上独立比较 delay schedules；当前不能作为与 DYN 并列的第二篇论文。

### 10. SIGN-C04 — 1.9/10，confidence: high
- **故事强度：中。** inhibitory evidence 对 heterophily 的动机合理。
- **证据强度：低。** binding gate 明确失败：heterophilic advantage 只有 +0.46/+0.48 pp，Cora 甚至略差；此外三种表示使用不同 probe seed，缺少 paired uncertainty，也没有最终 exact signed-reconstruction 指标。
- **先验风险：极高。** Negative-spike conversion 已覆盖 generic signed ANN→SNN，当前结果没有建立图特异增量。
- **建议：`reject-current-form`。** 未来工作不计分：只有改成图特异 inhibitory aggregation、统一模型 seed，并重新证明 heterophilic benefit 才值得救援。

## 组合裁决

- **可开发优先级：** 先修 LR-C05，其次 CERT-C11；POS-C13 只有补上缺失排列证据后才保留为第三候选。
- **不应并列启动：** DYN-C01 与 DLY-C14 当前不是独立证据；READ-C18 和 SIGN-C04 不应以当前故事进入论文写作。
- **严格扣分汇总：** DYN/DLY/READ 的 exactness 属于构造恒等式；EQ/PERM/CERT 也主要验证设计性质；DYN/DLY 缺 dynamic-edge bridge，EQ 缺 full-equivariant GNN bridge；SIGN/LR/EDGE/POS/READ 受 generic signed-spike、quantization、output-code prior art 强约束。
- **证据包裁决：** 可接受为诚实的 mechanism-screen report，但不能表述为十个成功方法、十篇论文候选或 GNN→SNN 端到端性能突破。
