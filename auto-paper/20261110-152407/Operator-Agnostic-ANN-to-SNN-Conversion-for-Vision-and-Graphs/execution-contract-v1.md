# Execution Contract v1（immutable）

> 生成 2026-11-10 15:24 GMT+8｜本文件为运行局部的不可变契约；任何修改必须新建 v2 并在 `pipeline-state.json` 记录 `reopen` 与整条后缀重验。

## 1. User goal（用户原话意图）

基于项目内**已成稿但保持不动**的 GNN2SNN 文章，另起一篇**视觉方向**新作：加入视觉数据集，用我们的转换算法与别的 ANN→SNN 转换算法做对比实验。参考资料库文档 `https://www.workbuddy.cn/space/d/DNmhLQWbiipm5eE1efL8oW`。新的实验设置与故事讲法用 `f-guidance-builder-v1`；做实验写文章用 `f-research-v1`；大规模实验上 `novix-platform`；小规模本机 3060 跑 smoke。

## 2. Authorized operations（本轮授权范围）

- ✅ 只读：资料库报告、成稿 `auto-paper/20261028-171500/Spiking-GNN-Conversion/`、项目日志、本机技能契约、公开文献与数据集页
- ✅ 本地写：仅在 `auto-paper/20261110-152407/Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs/` 内产出 guidance 包；追加 `auto-paper/generated-research-directions.md` 一行；追加 `.workbuddy/memory/2026-11-10.md`
- ✅ 本机计算：`dyg-cold` 环境跑 M0 数值核验（已实跑）
- ✅ 联网：文献/数据集检索（已由 3 个独立 Agent 完成）
- ❌ **不修改、不投稿、不改写成稿**
- ❌ **不修改资料库文档**
- ❌ **本轮不提交 novix 远端任务**（guidance 阶段）；大规模实验授权是后续 P4 的 opt-in
- ❌ 不 commit / push / 发布 / 创建或修改定时任务
- ❌ 不编造数据集、引用、基准结果、访问状态、评审分数

## 3. Inputs（输入清单）

| 输入 | 位置 / 标识 | 用途 |
|---|---|---|
| 成稿方法 | `auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-.../writing/p7-draft.md` | 误差恒等式、β*、膜电位解码、margin 定理、ρ 加权与 ρ-不变 |
| 成稿契约 | `auto-paper/20261028-171500/Spiking-GNN-Conversion/guidance-v3.md` | 主张边界、Non-goals、创新性证据 |
| 资料库报告 | node `DNmhLQWbiipm5eE1efL8oW`（只读；快照 `_library_gnn2snn_vision_report.txt`） | 前作地图、DTP 主线、基线清单、已证伪的 degree 轴 |
| 技能 | `f-guidance-builder-v1`、`f-research-v1`（后续）、`novix-platform`（后续）、`ccf-*` 8 件套（本机路径） | 流程契约 |
| 独立核验 | 3 个 Agent：基线矩阵 / G4 新颖性 / G1 数据集 | G0、G4、G1 证据 |
| 独立评审 | 3 份 `ccf-idea-reviewer standard` 报告（2.5 / 3.2 / 3.4） | CCFA-startup 决策 |
| 本机探测 | `hardware_probe.py` + `nvidia-smi` + conda 包检查 | G5 |
| 本机实跑 | `protocols/m0_operator_theory_check.py` + `evidence-snapshots/m0-results.json` | G3 |

**重要事实认定**：资料库报告声称的 `auto-paper/20261110-145235/.../guidance.md` 与 12 门产物**在本机不存在**（`auto-paper/` 下只有 6 个更早目录），且报告写"本机 conda MPS"与本机 Windows+CUDA 不符 → 该报告属另一会话/另一台机器，只作参考，其"已通过校验"的结论不作为本地事实。

## 4. Scope（科学范围与边界）

- 目标档位：Q2-or-better，主投 IEEE TNNLS / Q1–Q2 期刊档；不主张 CVPR/ICCV 主会档
- 适用算子类：固定、非负、线性传播算子；动态图 / softmax 动态 attention / max 非线性聚合**明确排除**并作为失效边界
- 数据集：G1 直链公开的 CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS（可选）、Planetoid 三图、ViG 公开权重；G2 的 ImageNet-1K / ImageNet-100 / DVS128 一律排除
- 主指标：conversion loss（pp，越低越好）；全部效率量为 proxy
- 不主张：精度 SOTA、能耗实测、生物保真、发明已被占的数学组件、T1/T2/κ_n 为 prior-art 无法得到的新数学结果
- 未发表内部先验（图节点 T≤8 达 ANN−1.5pp 带内）**只作内部校准，绝不当公开证据**

## 5. Resource / runtime envelope

- 本机：Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / 548 GB 空闲 / `dyg-cold`
- 本机 smoke ≤10 min、总预算 ≤24 h；远端单臂 ≤6 h、不设 `--max-turns`/`--timeout` 参数
- 5 冻结 seeds、T∈{1,2,4,8,16}、每方法超参搜索 ≤12 组且只在验证集上选择
- 远端：用户授权 `novix-platform` / `exp-4090`；本轮不提交；不记录端点或凭据

## 6. Output root

`C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\`（按技能默认 `auto-paper/<yyyyMMdd-HHmmss>/<paper-title>/`）

产出：`guidance.md`、`novelty-feasibility-report.md`、`dataset-access-log.md`、`hardware-profile.md`、`scenario-decision-log.md`、`literature-baseline-matrix.md`、`theoretical-feasibility-audit.md`、`story-strength-audit.md`、`matched-protocol.md`、`guidance-pipeline-state.md`、`execution-contract-v1.md`、`delivery-readiness.json`、`pipeline-state.json`、`ccfa-startup-packet/`（7 工件 + 3 份增补评审 + 修订卡 + `feasibility-contract.json`）、`protocols/`、`evidence-snapshots/`。

## 7. Quality requirements

- `validate_guidance.py <guidance.md> --strict --packet <ccfa-startup-packet>` 必须通过
- `pipeline_state.py --before <stage>` 逐门按 canonical 顺序通过；`--workflow-complete` 通过；`--submission-ready` 明确为 false
- 绑定引用默认：`min_unique=36`、`as_of=2026`、`recent_window_years=5`（2022–2026）、严格近期多数；最终核验由 `f-research-v1` P12/P14 执行
- 三轮独立评审原文与分数完整保留，不修改、不抬分
- 所有 `expected_strong` 标「预注册目标 / 非实测」；G7 pilot 后锁阈值
- 不出现虚构实验数值、虚构 URL、虚构评审分数；负结果全部保留

## 8. Relevant user preferences（本轮明示）

- 「跑代码在本机 conda 里跑，有不少环境在里面」→ 已选 `dyg-cold`，并实测其它环境（`spikinggcn36` 为 py3.6+CPU，不适用）
- 「小规模的本机 3060 跑跑 smoke 更快点」→ M0 已在本机实跑（<5 s）
- 「大规模实验上 novix-platform」→ 授权但本轮不提交
- 「这篇先不动，先这样放着」→ 成稿目录零改动

## 9. Installed dependencies / tools / environment

- Conda 环境：`base`、`dyg-cold`（选用）、`dyg-writing`、`jiewu-research`、`siigm`、`spikinggcn36` 等
- `dyg-cold`：Python 3.13.13、torch 2.11.0+cu128、numpy、`spikingjelly`（版本属性缺失，NOT VERIFIED）；**`torchvision` 缺失 → G6 blocker**
- 技能脚本：`f-guidance-builder-v1/scripts/{hardware_probe,pipeline_state,validate_guidance,delivery_readiness}.py`
- 本机技能：`ccf-pipeline-orchestrator`、`ccf-idea-optimizer`、`ccf-literature-searcher`、`ccf-idea-reviewer`、`ccf-experiment-designer` 等（`C:\Users\xhf\.workbuddy\skills\`）
- 运行模型/effort：本会话未暴露实际模型标识，不推断；不改全局设置

## 10. Delivery readiness

`workflow_complete` 与 `submission_ready` 分开记录。当前 `delivery_mode = preparation`、`submission_ready = false`：作者信息、投稿确认、代码发布安排、目标 venue 官方当年规则等属作者管理的待决事实，见 `delivery-readiness.json` 与 `delivery-readiness.md`。这些行政待决项按 `deferred-completion.md` 不阻塞本地科学阶段；科学证据、数据使用权、引用真实性、产物一致性仍是硬门。
