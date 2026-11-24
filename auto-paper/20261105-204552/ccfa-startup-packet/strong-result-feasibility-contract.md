# Strong-Result Feasibility Contract（筛选轮）

本文件是**计划契约**，不是结果。`expected_strong` 采用可证伪的关系式而非编造的数值提升；
绝对数值阈值须在官方基线 `train-your-fly` 本机复跑后冻结。唯一可引用的已发布参照是
`connectome` 仓库 manifolds 示例中给出的 circles-vs-stars 模型 77% test accuracy
（探索性示例，非论文主结果），仅用于说明任务并非不可学，不作为目标数字。

## C1（I1，主 claim）

- Claim / mechanism / assumptions / falsifying ablation：见 `claim-evidence-matrix.md` C1。
- Dataset / split：FlyWire v783 图（https://github.com/eudald-seeslab/train-your-fly/releases/tag/v0.1.0）
  + cogstim `lines`/时序刺激；`--seed` 固定，train/val/test 按论文 5000/5000/5000 缩放到本机预算。
- Primary metric：等 synaptic-op 预算下 test accuracy（higher）；
  secondary：交互项 `Δ = (acc_LIF,bio − acc_stateless,bio) − (acc_LIF,shuf − acc_stateless,shuf)`、
  spike rate（lower）、首次正确判别时刻、peak GPU memory。
- minimum：官方无状态基线在本机可复跑，且 2×2 四格全部能完成训练与评估、loss 可下降。
- expected_strong：交互项 `Δ` 的多种子 95% CI 不含 0 且为正，且在等预算下
  生物图+LIF 优于打乱图+LIF；该结论在 ≥2 个时序任务上方向一致。
- failure：交互项 <=0 或 |Δ| 小于预注册的最小可分辨效应；或 OOM / 单格 >600s；
  或生物图优势在无状态下同样大（机制被证伪）。
- Implementation readiness：官方 `train-your-fly` 源码已 clone 到 `../smoke-tests/train-your-fly`，
  在 `dyg-cold` 的导入/构图兼容性已实测通过（S0）；缺失组件 = LIF 消息传递层、
  时序刺激、等预算统计；prototype = `smoke_i1.py`。
- Compute budget：单格 <= 15 min GPU、<= 10 GB 显存；seeds 最终 >= 5；
  search_trials 最终 <= 12（τ / thresh / T / lr）。本轮冒烟 seeds=1、trials=0。
- Reviewer question answered by：主实验回答"结构与动力学是否交互"；
  消融 (a)(b) 回答"是否只是稀疏"；鲁棒性测试回答"是否只在特定 τ 成立"；
  效率测量回答"是否值得为生物结构付出代价"。
- Stop-and-return：任一 failure 触发 → 回到场景/方法设计，不降低 binding target，
  不继续训练朝不可能的目标；按用户规则换到 I3。

## C2（I3，前端 claim）

- Dataset / split：同上图包的 `right_visual_positions_all_neurons.csv` + cogstim `shapes` / CIFAR-10。
- Primary metric：等输入脉冲数下 test accuracy（higher）；secondary：脉冲数、参数量、时延。
- minimum：Voronoi 与规则网格前端都能训练且 test acc 高于 chance。
- expected_strong：Voronoi 在等脉冲预算下显著优于规则网格与随机种子，
  且在 ≥2 个下游 backbone 上方向一致；随机种子对照不成立时几何特异性不成立。
- failure：等脉冲数下 delta_acc <= 0.02 或方向反转；或只在单一 backbone 出现。
- Implementation readiness：`smoke_i3.py` 已实现 cKDTree Voronoi / grid / 可导软脉冲下游；
  缺失 = 真实光谱通道、跨 backbone、跨数据集。
- Compute budget：单条件 <= 15 min、<= 10 GB；seeds 最终 >= 5；本轮 1。
- Stop-and-return：几何增益不成立 → 淘汰 I3，换 I6 缩范围 mini-benchmark。

## C3（I6，基准 claim）

- minimum：2×2×1 四格可跑通，单格耗时/显存可测，外推给出全网格成本上界。
- expected_strong：缩范围网格多种子排名稳定性可报告，且交互效应与 I1 一致。
- failure：外推显示即使缩范围也超出 12 GB / 11 天预算 → 降级为 I1 附表，不独立投稿。

## 明确不生成的文件

`feasibility-contract.json` 在本轮**不生成**：其 schema 强制 `decision: "proceed"`，
而本轮 CCFA startup 结论不是 proceed（见 `startup-decision.md`）。
写一个假的 proceed 或用不合格 JSON 过验证都会违反真实性要求。
选定 idea 并重新走完整启动流程后再生成该 JSON 与 `guidance.md`。

## 预算与不确定项

- 本机：RTX 3060 12 GB / 31.9 GB RAM / 磁盘 ~510 GiB 空闲，见 `../hardware-profile.md`。
- 未核验：arXiv:2609.01330 代码直链、Reiser Cell 2026 官方出版页、flyvis 数据直连性。
- 数据使用许可：MaleCNS CC-BY 4.0；FlyWire 派生数据 CC BY 4.0；代码 Apache-2.0 / MIT。
  所有引用须遵守上游 citation 要求。
