# Novelty And Feasibility Report

## Input

- User technique: 项目内已成稿的 GNN→SNN 转换算法（精确误差恒等式 `B̂₂−B₂=A(E₁W₂)`、闭式偏置 `β*=θ/(2T)`、膜电位累加解码、margin 恢复定理；图节点分类实测 T≤8 达 ANN−1.5pp 带内，**未发表**）
- User-provided application scenario: 视觉方向，加入视觉数据集，用我们的转换算法与别的 ANN2SNN 转换算法对比；参考资料库报告 `DNmhLQWbiipm5eE1efL8oW`（今天的 GNN→SNN 视觉转换研究进展报告，主线 R91-v3 / DTP）
- Hardware: 本机 Windows 11 / RTX 3060 12GB / CUDA 12.8 / torch 2.11.0+cu128 / conda `dyg-cold`；大规模实验用户授权上 novix `exp-4090`
- Constraints: 成稿**完全不动**；资料库报告只读；图像侧 0 正式实验（guidance 阶段）；ImageNet-1K 属 G2 不可得；三轮独立红队结论必须原样保留

## Candidate Scenario Screening

| Scenario | Dataset access | Task validity | Theoretical fit | Novelty | Hardware | Baselines | Story | Decision |
|---|---|---|---|---|---|---|---|---|
| S1 标准 CNN 视觉横评 | G1 pass | pass | 弱（ρ≈1 上资产失效） | 1/5 | pass | pass | 2/5 | **拒**（降为 S2 的 B1 对照臂） |
| **S2 固定线性算子类统一刻画 + 跨骨干横评 + 失效边界** | G1 pass | pass | 4/5（ρ 加权 / ρ-不变 + M0 实跑） | 3/5（窄但已界定） | pass | pass | 4/5 | **选定**（加权 151） |
| S3 纯事件视觉时序 | G1 条件性 | pass | 2/5 | 2/5 | 3/5 | 3/5 | 2/5 | **拒**（降为可选 B5 稳健性臂） |

## Selected Scenario

- Scenario: **S2** —— 冻结 KNN 图 + 线性化聚合的视觉图骨干（线性化 ViG）与 GCN 消息传递层共用同一固定线性算子；标准 CNN 作 ρ≈1 对照臂；原版动态/非线性 ViG 作失效边界
- Reason for selection: G1–G4 硬门全过，加权总分最高（151 vs 103 vs 87）；唯一能同时用上成稿的 ρ 加权资产、满足"视觉数据集 + 全套转换算法对比"、且给出机制级新问题的场景
- Main risk: novelty 窄（三轮独立红队 2.5→3.2→3.4 / 5，均 `pivot-with-rescue-route`）；冻结/线性化削弱 ViG 表征力；PASCAL / TPP 复现
- Fallback scenario: 若第 0 批 PASCAL/TPP 等价或单调判据连续 failure → 收敛为「统一协议横评 + 实测失效边界」的 Q2 诊断型论文（S1 内容并入主表对照臂，不另起新场景）

## Dataset Access Audit

| Dataset | Source URL | License/terms | Direct public? | Friction | Decision |
|---|---|---|---|---|---|
| CIFAR-10 / CIFAR-100 | `https://www.cs.toronto.edu/~kriz/cifar.html` | NOT VERIFIED | 是 | 无 | ✅ 纳入 |
| Tiny-ImageNet | `https://cs231n.stanford.edu/tiny-imagenet-200.zip` | 非商业研究 | 是 | 无 | ✅ 纳入 |
| CIFAR10-DVS | `https://figshare.com/articles/dataset/CIFAR10_DVS_New/4724671` | CC BY 4.0 | 是 | 无 | ✅ 纳入（可选臂） |
| Planetoid Cora/CiteSeer/PubMed | `https://github.com/kimiyoung/planetoid` | NOT VERIFIED | 是 | 无 | ✅ 纳入 |
| ViG 代码 + 8 权重 | `https://github.com/huawei-noah/Efficient-AI-Backbones` | Apache-2.0 | 是 | 无 | ✅ 纳入 |
| ImageNet-1K / ILSVRC | `https://www.image-net.org/download.php` | 非商业研究 | **否** | 账号+机构邮箱+人工审批 | ❌ G2 排除 |
| ImageNet-100 | 无官方实体 | NOT VERIFIED | **否** | 无统一直链/split | ❌ G2 排除 |
| DVS128 Gesture | IBM Box | 许可冲突 | **否** | 需登录手动下载 | ❌ G2 排除 |
| N-MNIST | Mendeley / 作者页 | 许可冲突 | 条件性 | 登录要求未核验 | ⚠️ 待补证，本轮不用 |

完整实测字节数、md5、split 与摩擦见 `dataset-access-log.md`。

## Novelty Audit

| Paper | Year | Source | Method | Task/domain | Dataset | Overlap level | Decision |
|---|---:|---|---|---|---|---|---|
| Deng & Gu | 2021 | ICLR 2021 | `β*=θ/(2T)` + 逐层误差递归 | 转换误差 | CIFAR/ImageNet | `duplicate`（该组件） | 不得声称发明 β* |
| QCFS | 2022 | ICLR 2022 / arXiv:2303.04347 | clip-floor-shift + 零期望偏置 | 低时延转换 | CIFAR/ImageNet | `high` | 必比锚点基线 |
| FTBC | 2024 | ECCV 2024 / arXiv:2403.18388 | 前向时间偏置校正 | 低时延转换 | CIFAR/ImageNet | `high` | 必比基线 |
| Dual-Phase | 2024 | IEEE TNNLS 2024 | 膜电位替代计数读出 + 精确误差等式 | 转换误差 | 视觉 | `duplicate`（该组件） | 不得声称发明解码/等式 |
| One-Spike SNN | 2024/25 | IEEE TETC / arXiv:2403.08786 | 单脉冲相位编码，跨 CNN + GCN | 转换 | CIFAR/ImageNet/文本 GCN | `high` | "跨骨干"不新 |
| PASCAL | 2025 | TMLR 2025 / arXiv:2505.01730 | 确定性精确计数 + 逐层自适应 T | 低时延转换 | CIFAR/ImageNet | `high` | 第 0 批必跑（无码自行复现） |
| TPP | 2025 | ICML 2025 / arXiv:2502.14487 | 两阶段概率神经元 | 低时延转换 | CIFAR/ImageNet/DVS | `high` | 第 0 批必跑（官方码） |
| Parallel / DCGS / AdaFire | 2025 | ICML / ICML / AAAI | 并行转换 / 差分编码 / 自适应 burst | 低时延转换 | CIFAR/ImageNet | `medium` | 统一协议必比 |
| CS-QCFS / ECL | 2025 | Neural Networks / arXiv | 逐通道阈值 / 误差补偿学习 | T=1 / T=2 转换 | CIFAR | `medium` | 自行复现 |
| Adaptive Fission / RMP-Alignment / GTDL | 2025/26 | NeurIPS / arXiv / IEEE DLCV | 后训练裂变 / 残差膜电位 / 分组阈值 | 低时延转换 | 视觉 | `low` | 仅文献对照 |

**G4 判定 `pass-with-narrowing`**。三处剩余真空白：① 固定线性算子类上的层类型无关精确统一（须由 G3 证其非平凡性）；② 特定确定性化相对 PASCAL/TPP 的可测增益；③ 首次冻结图视觉骨干与图消息传递的统一协议横评 + 实测失效边界。**整包 duplicate 不存在**，但"发明数学组件"的主张全部不成立（三轮独立红队一致结论）。

## Theory Fit

- Domain bottleneck: ρ≈1 上推导的校准律在 ρ_n≠1 的固定线性算子上缺少检验与失效判据
- Method mechanism: 误差经 `A(E₁W₂)` 线性传播；系统项按 ρ_n 加权；相对误差由 `‖a_n‖₂‖DW‖₂/(TΔ_n)` 控制（ρ-不变）
- Expected advantage: 可先验计算 `κ_n = ρ_n/‖a_n‖₂` 并预测何时失效；ρ≈1 臂上非劣效
- Required adaptation: 冻结 KNN 图 + 线性化 max-relative 聚合；代价必须量化；原版动态/非线性算子作为失效边界
- Failure mode: T1 被证明可一行照搬；κ_n 单调性在真实网络上不成立；与 PASCAL/TPP 等价
- 完整推导、假设、可证伪消融与 M0 实跑证据见 `theoretical-feasibility-audit.md`

## Feasibility

- Hardware fit: 3060 12GB 跑 smoke / 基线回归；全量转用户授权 4090；548 GB 空闲
- Runtime estimate: 本机 smoke ≤10 min（M0 实跑 <5 s）；远端单臂 ≤6 h；本机总预算 ≤24 h
- Implementation complexity: 中—高。6 个官方基线仓库需统一 env（torch 2.11 兼容性 NOT VERIFIED，先以 QCFS 回归测试锁定）；PASCAL/CS-QCFS/ECL 无码须自行复现；ViG KNN 冻结与脉冲域实现需自写；`torchvision` 缺失为 G6 blocker
- Baseline availability: 6 个 must-rerun 官方码 + 3 个自行复现；第 0 批 PASCAL/TPP 必跑
- Ablation availability: A1–A7 七项，覆盖 β*、解码、确定性化、累积相、固定/动态图、线性/非线性、跨臂对照

## Q2+ Story Check

- Problem importance: 视觉骨干走向非网格聚合而转换理论仍隐含 ρ=1；属理论 + 评估缺口
- Prior-work gap: 最近邻密集但各自校准自己的算子，缺统一算子类判据与统一协议横评
- Core insight: 误差适用边界由传播算子类决定，可由 ρ_n、margin、T 先验计算
- Evidence chain: M0 恒等式/上界/失效边界实跑 → 统一协议横评（含第 0 批）→ 单调性趋势检验 → A1–A7 消融 → B4 边界 → 5 seeds 配对 CI + BH
- Limitations plan: 适用类只含固定线性算子；冻结/线性化代价；G2 排除 ImageNet 对外部效度的影响；T1 非平凡性未定；κ_n–T2 张力
- Reproducibility plan: `matched-protocol.md` 冻结版；teacher/图文件 SHA-256；seed 清单；环境快照；所有表由脚本从结果文件生成

## Verdict

- Final decision: **G0–G8 全部通过（G3/G4/G5/G6/G7 带明示硬前置），`startup-decision = proceed (conditional)`**。三轮独立红队分数 2.5 → 3.2 → 3.4（1–5 尺度）、recommendation 三次均 `pivot-with-rescue-route`，第三轮判定 **未解 fatal risk = 0** 并建议 conditional proceed
- Conditions before handoff to `f-research-v1`: **H1–H9 全部**（见 `ccfa-startup-packet/startup-decision.md` §3）；尤其 H2（T1 非平凡性、κ_n–T2 张力、‖A‖ 严格界、推论层检索须在 P4 前关闭）、H3（第 0 批 PASCAL/TPP 必跑）、H7（`expected_strong` 一律预注册、G7 pilot 后锁阈值）、H9（G0/G3/G7 命中回退条件即 `pivot-with-rescue-route`）。`submission_ready = false`。
