# I1 冒烟实验记录（结构 × 脉冲动力学）→ 首轮失败

环境：`dyg-cold`，RTX 3060 12 GB，torch 2.11+cu128 / PyG 2.8.0。
数据：**真实 FlyWire v783 生物图前缀子图**，取自 Zenodo
`connections_biological.csv.gz` 的前 2 MB gz 流式解压（198,761 行，8.19 MB CSV），
标注表为官方 `neuron_annotations_flywire_v2.1.0.tsv.gz`（7.7 MB）。
刺激：`cogstim ans --ratios easy --img-size 128 --seed 42`，固定 seed 打乱后 75/25 切分，204 张。
设计：{生物图, 打乱 post 列的度保持随机图} × {无状态 tanh 消息传递 K=3, LIF T=8}，
固定图权重（log1p(syn_count) + 行归一化），仅训练线性读出，40 steps，单 seed，batch 16。
**非论文实验，仅用于 Go/No-Go。**

## 实测结果

| 图 | 动力学 | loss 首→末 | test acc | spike rate | peak GPU | 单格耗时 |
|---|---|---|---:|---:|---:|---:|
| 生物图 | stateless | NaN → NaN | 0.5686 | 0.0 | 93.8 MB | 0.21 s |
| 生物图 | LIF | 0.7788 → 0.7213 | 0.4314 | 6.7e-05 | 169.3 MB | 0.27 s |
| 打乱图 | stateless | NaN → NaN | 0.5686 | 0.0 | 94.6 MB | 0.07 s |
| 打乱图 | LIF | 0.7788 → 0.7213 | 0.4314 | 6.7e-05 | 170.1 MB | 0.25 s |

图规模：87,564 节点 / 196,373 nnz；光感受器节点 580、Kenyon 节点 2,393（均来自官方标注表）。
交互项 `Δ = 0.0`。预注册失败信号：`no_interaction = True` → `verdict: DROP_OR_REVISE`。

## 判定：首轮失败，换 idea

按用户规则"I1 冒烟不理想 → 换 I6"。**但必须区分"实验失败"与"机制被证伪"**：

1. **生物图与打乱图结果逐位相同**，最可能的原因是 gz 前缀子图按 `pre_root_id` 排序，
   信息在 K=3 / T=8 步内根本没传播到 Kenyon 读出群体；读出层收到近零向量，
   线性分类器只能学到类别先验（0.5686 ≈ 多数类比例）。
   这等于实验灵敏度为 0，**不能据此断言"结构×动力学无交互"**。
2. **stateless 出现 NaN**，说明数值管线仍不稳定（需排查 syn_count 缺失值、
   行归一化分母、稀疏 CSR 的 dtype/索引）。
3. **LIF spike rate 6.7e-05**，阈值/输入增益不匹配，网络几乎不发放，
   脉冲动力学形同虚设。
4. 唯一确定的正面结论：**硬件与官方框架可行性通过**——真实 8.7 万节点图在
   12 GB 卡上仅占 169 MB、单格 0.27 s，`torch.sparse.mm` + PyG 路径可用，
   G5 与 I1 的"基线兼容性"致命风险已被实测解除。

## 若要复活 I1，必须先修的三件事

1. 用完整生物图（或按 BFS 从光感受器取连通视叶子图），并预检
   "固定随机输入下生物图/打乱图的最终活动向量差异 > 0"再开始训练。
2. 修 NaN：清洗 syn_count、检查 A.data 有限性、显式 dtype。
3. 重新标定 LIF（阈值、输入增益、泄漏），把 spike rate 拉到 0.05–0.3 的可用区间，
   并加入 surrogate gradient 使突触增益可训练。

以上任何一项都超出本轮 11 天窗口内的"轻量冒烟"预算，故本轮不继续。

## 产物

- `smoke_i1.py`、`smoke_i1.json`、本报告
- 官方基线校准：`data/zenodo/source_data_figure_3_task_accuracy.csv`
  （生物图 形状 64.0% / 数量 63.69%；Unconstrained 70.0% / 82.98%）
