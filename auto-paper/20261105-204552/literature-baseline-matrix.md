# Literature / Baseline Matrix（G0 证据，访问 2026-11-05）

目标：CVPR 2027 主会。下列工作按"能否在本机直接复跑"与"是否构成直接竞争"分层。
`direct-rerun` 可行性依据 `hardware-profile.md`（RTX 3060 12GB / `dyg-cold`：torch 2.11+cu128, PyG 2.8.0）。

| 工作 | 年份 / 出处 | 官方 URL | 任务 / 数据 / 指标 | 代码 / checkpoint | 本机可复跑性 | 角色 | 为何强 / 为何保留 |
|---|---|---|---|---|---|---|---|
| **Structure alone supports efficient visual computation in the Drosophila visual system**（Correig-Fraga, Guimerà, Sales-Pardo） | 2026-10-08, arXiv:2610.10023 | https://arxiv.org/abs/2610.10023 | 复眼 Voronoi + FlyWire v783 全脑无状态消息传递 GNN；颜色/形状/数量辨别；accuracy + wiring cost | `train-your-fly` (Apache-2.0) + `connectome` (MIT) + Zenodo 图数据 | **高**：1.3 GB 图可直下，PyG 可用；但官方 pin torch 2.6/PyG 2.6/torch-sparse，本机 2.11/2.8 需兼容验证 | **must-rerun + 最强直接竞争** | 最近、最同构、代码与随机图 ensemble 全公开；任何新 idea 必须相对它给出差异 |
| **Connectome-Based Modelling Reveals Orientation Maps in the Drosophila Optic Lobe**（Liew et al., 胡晓林组） | NeurIPS 2025 / arXiv:2609.01330 (2026-09-01) | https://arxiv.org/abs/2609.01330 | 完整果蝇连接组 + 生物脉冲神经元 + 朝向刺激 → 视叶朝向图涌现 | 页面标注 Has Code（本轮未核验直链） | 中（未核验） | **literature-context + 去重红线** | 证明"连接组 + SNN + 视觉刺激"已被做过，但它是神经科学仿真，不是可训练 CV 任务 |
| **Connectome-constrained networks predict neural activity across the fly visual system**（Lappalainen et al.） | Nature 2024 | https://www.nature.com/articles/s41586-024-07939-3 | 视叶 DMN，光流任务，预测 26 项实验的神经反应 | `TuragaLab/flyvis` (MIT)，预训练模型 + Colab 教程 | 中（数据需另取） | **adaptation-attempt / literature-context** | 连接组约束视觉建模的权威基线，CV 侧须引用 |
| **Neuronal wiring diagram of an adult brain**（Dorkenwald et al.） | Nature 2024 | https://doi.org/10.1038/s41586-024-07558-y | FlyWire v783：139,255 神经元 / 5,450 万突触 | 数据经 flywire.ai / annotations | 高（图数据） | 数据来源 | 图结构来源，必引 |
| **Whole-brain annotation and multi-connectome cell typing**（Schlegel et al.） | Nature 2024 | https://doi.org/10.1038/s41586-024-07686-5 | 跨连接组 cell typing | `flywire_annotations` | 高 | 数据来源 | cell type / 读出群体定义依据 |
| **Sexual dimorphism in the complete connectome of the Drosophila male CNS** | Cell 2026, DOI 10.1016/j.cell.2026.08.015 | https://male-cns.janelia.org/ | MaleCNS v1.0：166,691 神经元 / 1.25 亿突触 / >11,700 细胞类型 | bulk feather 直连 | 高 | 数据来源 | 用户提供博客对应的原始数据 |
| **The organization of visual pathways in the Drosophila brain**（Reiser et al.） | Cell 2026 | https://www.163.com/dy/article/L7U9JRDI0532BT7X.html （中文解读；本轮未核验出版页） | 视叶 ON/OFF、L1-L3、R7/R8、层级/通路/空间组织框架 | `reiserlab/male-drosophila-visual-system-connectome-code` | 中 | 机制依据 | 为"结构先验 → 时间计算"提供生物学支持 |
| **Model-agnostic linear-memory online learning in SNNs（BrainTrace）** | Nature Communications 2026-01-19 | https://view.inews.qq.com/a/20260124A01W9800 （报道；本轮未核验期刊页） | 12.5 万神经元 / 5,000 万突触果蝇全脑 SNN 在线训练 | 未核验 | 低（未核验） | 可行性依据 + 去重 | 证明大规模连接组 SNN 可训练；同时说明"大图 SNN 训练"已不新 |
| **SpikeTrack**（同济等） | CVPR 2026 | https://arxiv.org/abs/2602.23963 ; https://github.com/faicaiwawa/SpikeTrack | 脉冲驱动 RGB 目标跟踪，精度/能耗 | 已开源 | 中 | **strong recent SNN baseline（若走时序/跟踪）** | CVPR 同赛道强基线，代码公开 |
| **TAPFormer** | CVPR 2026 | https://arxiv.org/abs/2603.04989 ; https://github.com/ljx1002/tapformer | 帧-事件异步融合任意点跟踪 | 已开源 | 中 | 事件视觉基线 | 事件/时序视觉方向的顶会标尺 |
| **CogStim** | 2026 | https://github.com/eudald-seeslab/cogstim | 8 类合成视觉刺激生成 | MIT, pip | 高 | 数据工具 | 直接可用的任务生成器 |
| **BioReservoir / ESA 类 connectome reservoir** | 2026 | https://github.com/igdigitallab/bioreservoir | MaleCNS 固定 reservoir + LIF，文本→感觉群→下行神经元 | 开源 | 高 | 去重 + 对照 | "连接组拓扑比随机 reservoir 更抗过拟合"已被提出，需避开 |
| **ConnectomeLens / fault-lines / price-of-thought** | 2026 | https://github.com/dhruvin-sarkar/ConnectomeLens 等 | MaleCNS 静态分类、攻击容忍、布线成本 | 开源 | 高 | 相关工作 | 说明 MaleCNS 图分析已很拥挤 |
| **We Taught a Fly to Read X-Rays**（博客，非同行评审） | 2026 | https://www.mecha-health.ai/blog/Teaching-a-Fly-to-Read-X-Rays | MaleCNS + R1-R6 直采 + 全图传播 → 胸腔积液分类，82% val AUROC | 博客 | — | 去重 | "连接组当视觉 backbone" 已被演示过，须避免只换数据集 |
| **Wiring the Fly Brain into a World Model**（JEPA on connectome） | 2026 工作论文 | https://louistier.github.io/projects/3_hack_the_worlds | 连接组脉冲编码器 + JEPA 世界模型 | 工作论文 | 低 | 去重 | 说明"连接组 + 脉冲 + 自监督表征"已被探索 |

## 基线层级结论

- **必须直接复跑/适配**：`train-your-fly`（含 4 种随机图 ensemble）。它是唯一同时具备
  开源代码、公开图数据、公开刺激生成器与明确指标的最近权威基线。
- **内部匹配对照**：同参数量的无状态 GNN、规则网格/随机图、 ANN/ResNet 小模型、
  spikingjelly LIF 基线。
- **仅文献对照**：flyvis、BrainTrace、CVPR 2026 SpikeTrack/TAPFormer（除非选定对应任务）。
- **不可仅与 ANN toy baseline 比较**：CVPR 主会评审不会接受。
