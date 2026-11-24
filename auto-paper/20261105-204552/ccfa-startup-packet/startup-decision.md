# CCFA Startup Decision（筛选轮）

**Decision: `pivot-with-rescue-route`**（不是 `proceed`）

记录时间 2026-11-05。冻结输入：6 个 idea 卡片、6 份 CCF 独立评审报告、
`../literature-baseline-matrix.md`、`../prior-art-dedup-log.md`、`../dataset-access-log.md`、
`../hardware-profile.md`、`execution-contract-v1.md`。

## 为什么不是 proceed

1. CCF 评审对 6 个 idea 给出 **0 个 GO**：最好 I1 只有 5.4/10（confidence 0.70），
   且存在未解除的致命风险（must-rerun 基线在本机的兼容性、等预算对照前提）。
2. 相对 arXiv:2610.10023 的增量一致性不足：三位独立评审都认为
   "换数据集 / 加一个模块 / 换训练法"撑不起 CVPR 主会。
3. 硬时间窗只剩 11 天（注册 11-10、全文 11-16），单卡 12 GB，
   没有任何 idea 的 `executability_11d` 达到 4 分以上（唯一例外 I3 得 4 分，但已被冒烟淘汰）。
4. 评审后新增的官方证据进一步收紧了可行性：Zenodo
   `source_data_figure_3_task_accuracy.csv` 显示生物图无状态 GNN 在
   形状辨别 64.0%、数量辨别 63.69%，而随机图 Unconstrained 达 70.0% / 82.98%，
   Connection-pruned 达 69.0% / 78.13%。即"生物接线带来绝对精度优势"不成立，
   任何以精度为主指标的主张都需要重新设计。

## Rescue route（本轮实际执行）

| 步骤 | 动作 | 结果 |
|---|---|---|
| 1 | 淘汰 I2 / I4 / I5 | 无窗口内修复路径，保留失败原因 |
| 2 | 验证 I1 致命风险：官方 `train-your-fly` 在 `dyg-cold` 能否导入/构图 | **通过**（torch 2.11 + PyG 2.8 + torch_scatter 可用；缺 torch_sparse 不阻塞；补 imageio/seaborn 后 OK） |
| 3 | 冒烟 I3（最快出结果） | **淘汰**：两轮真实数据下 Voronoi 几何无增益（修复坐标列后 delta = −0.0393） |
| 4 | 冒烟 I1（真实生物图 × 打乱图 × 无状态/LIF 2×2） | 进行中，数据并行下载 |
| 5 | 若 I1 失败 → 换 I6 缩范围 mini-benchmark（用 I1 计时做成本外推） | 待定 |

## 允许的下一步与禁止项

允许：继续 I1 冒烟、按失败信号换 idea、把结果写回评审分数变化条件、
向用户如实汇报 11 天窗口的风险。

禁止：据此生成 `guidance.md`、声称 G6-G8 通过、运行 `validate_guidance.py`、
生成 `feasibility-contract.json`（其 schema 强制 `decision: proceed`，本轮不满足）、
把 `planned_claim` 写成 `observed_finding`、把冒烟单 seed 结果当作论文结论。

## 待办清单（deferred facts，不影响本地研究）

| ID | 类别 | 状态 | 说明 |
|---|---|---|---|
| A1 | author-fact | pending | 作者姓名/单位/邮箱未由用户提供 |
| A2 | author-approval | pending | 是否真的要投 CVPR 2027（11 天）需用户决定 |
| A3 | portal | pending | OpenReview 账号与 11-10 前注册需作者本人完成 |
| A4 | access-route | pending | 代码/数据发布安排未定 |
| A5 | production | pending | 最终 PDF/补充材料制作未启动 |

以上为行政/制作事项，不构成本地科学工作的阻断；科学证据、数据使用许可与真实性仍是硬门槛。
