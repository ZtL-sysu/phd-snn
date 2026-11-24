# Prior-Art Opportunity Map（CCFA Startup Packet）

完整去重记录见 `../prior-art-dedup-log.md`，基线与代码状态见 `../literature-baseline-matrix.md`。
访问日期 2026-11-05。

## 最近工作簇

| 簇 | 代表工作 | 已占据的主张 | 公开资产 |
|---|---|---|---|
| C1 连接组 = 静态视觉 backbone | arXiv:2610.10023 / `train-your-fly`（2026-10-08） | 复眼 + 全图无状态 GNN + 等布线预算下生物图更优 | 代码 Apache-2.0、1.3 GB 图包、4 种随机图、cogstim、Zenodo |
| C2 连接组 = 结构先验（神经活动预测） | Nature 2024 `flyvis` / Cell 2026 Reiser 视觉通路 | 视叶 DMN 预测神经反应；ON/OFF、层级、通路组织 | flyvis MIT + 预训练模型；MaleCNS 视叶代码 |
| C3 连接组 + 脉冲 = 神经科学仿真 | arXiv:2609.01330（NeurIPS 2025）、BrainTrace（Nat Commun 2026） | 朝向图涌现；12.5 万神经元全脑 SNN 在线训练 | 代码状态部分未核验 |
| C4 连接组 = 固定 reservoir / 通用 backbone | BioReservoir、ESA reservoir、MaleCNS X-ray 博客、JEPA-on-connectome | 拓扑抗过拟合；连接组读 X 光；连接组脉冲自监督 | 多数开源 / 博客 |
| C5 SNN 视觉强基线 | CVPR 2026 SpikeTrack、TAPFormer | 脉冲跟踪、帧-事件融合 | 均开源 |

## 机会地图：还空着的格子

1. **时间维度 × 结构归因**：C1 明确写"neurons keep no state between steps"，
   C3 只做仿真不做可训练 CV 任务/能效归因。二者交叉处空白。→ I1。
2. **能效轴换成 synaptic ops / spike rate**：C1 只比较 wiring cost；
   没有人在等脉冲预算下比较生物图与随机图。→ I1 / I6。
3. **复眼几何作为解耦的可插拔前端**：C1 里 eye 与全脑图死绑；
   没有人在标准 CV 基准上把它当独立编码层做脉冲预算-精度曲线。→ I3（但增量偏小）。
4. **受控网格与负结果**：所有簇都只报告正向结论，缺统一网格与排名稳定性分析。→ I6。
5. **两个完整连接组（雄/雌）的对比**：MaleCNS 2026-09 才齐备，`ol_annotations` 已有视叶匹配，
   但 CV 侧尚无人使用。→ I4（CVPR fit 弱）。

## 公开数据集与指标

- 图：FlyWire v783（139,255 节点 / 5,450 万突触）、MaleCNS v1.0（166,691 节点 / 1.25 亿突触）。
- 刺激：cogstim 8 类合成任务（MIT）；论文标准规模每类 5,000/5,000/5,000。
- 指标：test accuracy + 95% CI、accuracy-vs-Weber、等预算 accuracy、spike rate、synaptic ops。
- 基线可得性：`train-your-fly` 是 must-rerun；本机兼容性已在
  `../smoke-tests/` 的 S0 中验证（可导入、可构图，缺 `torch_sparse` 不阻塞）。

## 差异化路线（按可行性排序）

1. I1：{生物图, 随机图} × {无状态, LIF} 2×2 交互项 + 等突触操作预算 → 机制结论。
2. I3：复眼几何作为独立前端，跨 backbone 验证 → 组件贡献（最快，但故事小）。
3. I6：把 1 的网格缩成 mini-benchmark + 成本外推 → 基准/负结果兜底。

## 来源质量政策

优先官方页面、arXiv、Nature/Cell、CVF、GitHub release、Zenodo、PyPI。
本轮所有"已占据主张"均可追溯到具体 URL；中文媒体报道只用于线索，
未核验出版页的条目（Reiser Cell 2026、BrainTrace 期刊页）在基线矩阵中已标注"本轮未核验"，
不作为硬结论依据。
