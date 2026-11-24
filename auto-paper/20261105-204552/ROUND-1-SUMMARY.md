# Round 1 汇总：GNN × SNN × 果蝇连接组 × 视觉（CVPR 2027 选题筛选）

生成时间 2026-11-05。运行根：`C:\code\phd-snn\auto-paper\20261105-204552`。
技能链：`f-guidance-builder-v1`（选题/证据/门槛）+ `ccf-paper-reviewer`（6 份独立评审）
+ 本机 `dyg-cold` Conda 冒烟实验。

## 一句话结论

**6 个 idea 全部通过评审漏斗后，没有一个达到"值得继续投入"的标准（0 个 GO）**；
两轮真实数据冒烟分别淘汰 I3、判 I1 首轮失败，只剩 I6 的缩范围 mini-benchmark 在算力上可行。
大方向本身成立且基础设施已全部打通，但**距离 CVPR 2027 全文截止只剩 11 天，
冲主会不现实**；建议换投稿窗口或把贡献收窄到一个可验证的机制结论。

## 硬约束（先说最重要的）

CVPR 2027：论文注册 **2026-11-10 AOE**，全文 **2026-11-16 AOE**（北京时间 11/17 19:59），
补充材料 11-23，会议 2027-06-20~25 西雅图。来源
https://cvpr.thecvf.com/Conferences/2027/CallForPapers （访问 2026-11-05）。
今天 11-05，**剩 11 天**。2026-09-15 之后上线的论文算 contemporaneous，
不会仅因比较被拒，但高度相似会加审 —— 而我们的最大对手恰好落在这个窗口里。

## 参考资料核验结论

| 项 | 核验结果 |
|---|---|
| Google Research 博客 / MaleCNS | 166,691 神经元、1.25 亿突触、>11,700 细胞类型；Cell 2026, DOI 10.1016/j.cell.2026.08.015；Neuroglancer 可下载 |
| MaleCNS 全图直连 | `connectome-weights-...feather` 1,051,241,946 B，HTTP 200、无鉴权、CC-BY 4.0；标注表 14.5 MB、递质表 42 MB 同样直连 |
| awesome-fly 里的开源框架 | 最贴合的是 `eudald-seeslab/train-your-fly`（Apache-2.0）：复眼 Voronoi + FlyWire v783 全脑 PyG 消息传递 + Kenyon 线性读出；配套 `connectome`（MIT，4 种随机图）与 `cogstim`（MIT，8 类刺激）；数据 Zenodo 10.5281/zenodo.21549559（CC BY 4.0） |
| 官方基线在本机 | **可跑**：`dyg-cold` torch 2.11+cu128 / PyG 2.8.0 / torch_scatter / spikingjelly / cv2 齐备；补装 imageio+seaborn 后官方框架可导入、可构图；缺 `torch_sparse` 不阻塞 |
| 硬件 | Windows 11，12 核，31.9 GB RAM，RTX 3060 12 GB，CUDA 12.8，磁盘空闲 ~510 GiB |

## 去重红线（决定了所有 idea 的形状）

- **arXiv:2610.10023**（2026-10-08）`train-your-fly` 已占满「复眼 → 全图无状态 GNN → 视觉分类 → 等布线预算下生物图 vs 4 种随机图」，代码/数据/刺激全公开。
- **arXiv:2609.01330**（NeurIPS 2025）已做「完整连接组 + 脉冲神经元 + 朝向图涌现」。
- Nature 2024 `flyvis`、BrainTrace（Nat Commun 2026）、BioReservoir / ESA reservoir、
  MaleCNS 读 X 光博客、JEPA-on-connectome 又占了「结构先验 / 大图 SNN 训练 / 固定 reservoir / 通用 backbone / 脉冲自监督」。
- 因此**不能再做"把连接组接到视觉输入上"或"第一次训练果蝇 SNN"**，只能往
  「时间维度 × 结构归因」「等突触操作预算」「受控负结果」这些空格走。

## 6 个 idea 与 CCF 独立评审

3 组独立子代理按 `ccf-paper-reviewer` standard scientific 契约出 6 份报告
（YAML 评分 + 15 章节 + 3 人 reviewer panel + AC meta-review），
详见 `ccfa-review-reports/`。判定规则：overall ≥ 6.5 且无致命风险才为 GO。

| Idea | 一句话 | Overall | Conf. | 判定 | 冒烟 | 结局 |
|---|---|---:|---:|---|---|---|
| I1 结构 × 脉冲动力学 | 2×2 交互项证明拓扑与时间动力学超可加 | 5.4 | 0.70 | REVISE | GO | **首轮失败** |
| I3 复眼脉冲前端 | 实测光感受器几何做成可插拔编码层 | 5.2 | 0.80 | REVISE | GO | **淘汰** |
| I6 受控基准 | 结构×动力学×预算的统一网格与负结果 | 5.1 | 0.77 | REVISE | GO(成本外推) | 兜底可行 |
| I2 鲁棒性正则 | 生物接线 + LIF 抗腐蚀 | 4.6 | 0.66 | NO-GO | 否 | 淘汰 |
| I5 结构蒸馏 | 视觉基础模型蒸馏进连接组脉冲图 | 3.3 | 0.83 | NO-GO | 否 | 淘汰 |
| I4 跨连接组 motif | 雄/雌双图保守 motif 迁移 | 2.8 | 0.88 | NO-GO | 否 | 淘汰 |

评审一致意见：相对 arXiv:2610.10023 的增量不足以撑起 CVPR 主会；
`executability_11d` 普遍 1-2 分；任何"只换数据集/加模块/换训练法"都会被判 incremental。

## 冒烟漏斗（按你的规则：不理想就换）

```
6 ideas
  └─ CCF 打分 → 淘汰 I2 / I4 / I5，保留 I1 / I3 / I6
       └─ S0 兼容性验证（官方框架在本机）→ PASS，I1 致命风险解除
            └─ 冒烟 I3 → R0 dry-run 发现白底饱和+切分 bug
                        → R1 坐标列 bug（用了 3D x/y）
                        → R2 修复后 Voronoi 0.3725 vs grid 0.4118，delta −0.0393
                        → 淘汰，换 I1
                 └─ 冒烟 I1（真实 FlyWire 前缀子图 87,564 节点 / 196,373 边）
                        → stateless loss NaN；LIF spike rate 6.7e-05；
                          生物图与打乱图输出完全相同，交互项 0.0
                        → 首轮失败（但主因是实验设计缺陷，不是机制被证伪）
                        → 换 I6
                      └─ I6 成本外推（用 I1 真实计时）
                        → 全图单格 ≈459 s / 1.46 GB；
                          全网格 60 格×5 seeds ≈38.2 GPU h（预算 105.6 h 内）；
                          mini 4 格×3 seeds ≈1.5 GPU h
                        → MINI_BENCHMARK_FEASIBLE
```

### 冒烟中拿到的硬数据

- **I3**：等脉冲预算（实测输入脉冲率 0.1147 vs 0.1071），Voronoi 未优于规则网格；
  两轮方向一致。但 train loss 降到 0.14/0.21 而 test acc 仅 0.37/0.41，属小样本过拟合，
  不能断言任务不可学。
- **I1**：真实 8.7 万节点图在 12 GB 卡上峰值 **169 MB**、单格 **0.27 s**，
  证明大规模连接组脉冲消息传递在本机完全跑得动（G5 通过）。
  失败源于：gz 前缀子图按 pre 排序导致 Kenyon 读出收不到信息、数值 NaN、LIF 阈值失配。
- **I6**：评审判的"全网格算力空头支票"被实测部分推翻——纯 GPU 时间其实够；
  但 38.2 GPU h 不含基线复跑、调参、失败重跑与论文写作，11 天墙钟内仍不足以交付主会论文。
- **官方基线校准**（评审后新增，Zenodo `source_data_figure_3_task_accuracy.csv`）：
  生物图无状态 GNN 形状 64.0% / 数量 63.69%；随机图 Unconstrained 70.0% / **82.98%**；
  Connection-pruned 69.0% / 78.13%。→ **"生物接线带来绝对精度优势"不成立**，
  这进一步压缩了以精度为主指标的所有故事，I1 只能靠交互项立论。

## 评审分数变化条件核对

| Idea | 评审预设条件 | 实测 | 分数变化 |
|---|---|---|---|
| I1 | 官方基线可运行 + 2×2 出现显著交互 → +0.5~1.0 | 兼容性满足，但交互项 0.0 且 NaN | 不触发上调；新增数值/读出风险，净持平或下调 |
| I1 | 交互项不显著 → −0.5~−1.5 转 NO-GO | 交互项 0.0（但实验灵敏度为 0） | 暂记"实验无效"，不按机制证伪处理 |
| I3 | Voronoi 显著优于网格 → +0.5~1.0 | delta −0.0393 | 触发下调条件，转淘汰 |
| I6 | 成本外推显示缩范围可行 → +0.5 | mini 1.5 GPU h、显存 1.46 GB | 满足，5.1 → 约 5.6，仍低于 6.5，非 GO |

## 结论与建议

1. **本轮按你的规则完成了"多想 idea → 逐个 CCF 打分 → 有搞头就冒烟 → 不理想就换"的完整闭环**，
   且所有数字都来自真实本机运行，没有编造结果。
2. **CVPR 2027 主会 11 天窗口不建议硬冲**：0 个 GO、强基线刚发布、需要完整多种子实验与写作。
   更现实的是：CVPR 2027 workshop、ICCV 2027、或 CVPR 2028 主会。
3. **大方向仍然值得做**，而且本轮把最贵的准备工作做完了：公开数据直连、官方框架本机兼容、
   刺激生成器、评测协议、官方基线数值、硬件预算全部核验。
4. 若要继续，最省力的路线是：**先修 I1 的三个工程缺陷（完整/视叶子图、NaN、LIF 标定），
   用 I6 的 mini-benchmark 网格(4 格×3 seeds，约 1.5 GPU h)做第一次可信的机制判定**，
   再决定是否值得写论文。

## 交付文件索引

| 文件 | 内容 |
|---|---|
| `ROUND-1-SUMMARY.md` | 本报告 |
| `ideas/idea-cards.md` | 6 个机制级 idea 卡片 |
| `ccfa-review-reports/score-matrix.md` + `idea-I*-review.md` | CCF 打分矩阵与 6 份独立评审 |
| `smoke-tests/results/smoke_i3_report.md` | I3 冒烟（含两次 bug 修复）与淘汰结论 |
| `smoke-tests/results/smoke_i1_report.md` | I1 冒烟（真实 8.7 万节点图）与失败分析 |
| `smoke-tests/results/smoke_i6.json` | I6 成本外推 |
| `smoke-tests/smoke_i1.py` / `smoke_i3.py` / `smoke_i6.py` | 可复现脚本 |
| `literature-baseline-matrix.md` / `prior-art-dedup-log.md` | 强基线与去重记录 |
| `dataset-access-log.md` / `hardware-profile.md` | 公开数据与本机硬件 |
| `ccfa-startup-packet/` | 启动阶段计划、机会图、红队、claim-evidence 与强结果契约、startup decision |
| `execution-contract-v1.md` / `guidance-pipeline-state.md` / `scenario-decision-log.md` | 运行契约、阶段账本、决策日志 |

本轮为 **idea-screening round**，未生成 `guidance.md`、未交接 `f-research-v1`、
未声称 G6-G8 / validation / handoff 通过；原因见 `execution-contract-v1.md` 第 3 节。
