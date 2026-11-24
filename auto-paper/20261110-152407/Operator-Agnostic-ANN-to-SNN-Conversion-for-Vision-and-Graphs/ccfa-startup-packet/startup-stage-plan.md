# startup-stage-plan.md

> CCFA-startup 阶段规划工件 · 按 `ccf-pipeline-orchestrator` 职责生成（只规划阶段/门/owner/handoff，不执行下游写作、检索、实验设计、评审）
> 生成者：CCFA startup 包撰写员（本 Agent）
> 日期：2026-11-10
> 模式：`standard`（`task-modes.md`：完整流程规划、可复用文件、多阶段 handoff）
> 纪律：不编造文献、结果、基线数值、评审分数、URL；已知事实与推断分离；隐私材料按 `privacy-and-evidence.md` 处理；本包内一律用文件名互引，不写个人绝对路径。

## 0. 本文档边界

- 本文档只做 **阶段 / 门 / 判定标准 / owner / handoff / 决策** 规划，不执行下游工作（orchestrator Core Rule）。
- `idea-red-team-review.md` 由另一个独立 Agent 生成；`feasibility-contract.json` 由主会话按哈希生成，本 Agent 只写 `strong-result-feasibility-contract.md` 草稿文本。
- 全部事实来自用户提供的「已核验事实」清单；凡用户未提供的一律标 `UNVERIFIED` / `needs-evidence` / `must-know`。

## 1. 项目状态（orchestrator Adaptive Output Contract）

| 字段 | 值 |
| --- | --- |
| Project goal | 在 ANN→SNN 转换中把传播算子抽象为固定、非负、线性矩阵 `A`，建立层类型无关的精确误差恒等式，在 T≤4 低时步下降低 conversion loss；以「ViG 首次脉冲化 + 同一算子跨视觉骨干与图消息传递的统一协议横评」作为协议贡献 |
| Current stage | `CCFA-startup`（启动包生成，本阶段） |
| Known artifacts | 本包内 6 个工件（本 Agent）；`idea-red-team-review.md`（独立 Agent）；`feasibility-contract.json`（主会话）；`evidence-snapshots/`、`protocols/` 目录当前为空 |
| Missing artifacts | `ccfa.yaml`（未找到 → **项目状态跟踪不可用**）；具体 target venue/tier 未指定；视觉侧 0 正式实验；`torchvision` 未装；novix 远端 4090 未提交（guidance 阶段不提交） |
| Gate decision | 见 §5 与 `startup-decision.md` |
| Next owner skill | 逐门见 §4；本阶段之后首个下游 owner = `ccf-experiment-designer`（承接 G6 实现就绪 → G7 执行） |
| Handoff packet | 见 §6 |
| ccfa.yaml update | 见 §7（只给 patch 建议，不静默改写用户状态） |
| Risks / blockers | 见 §8 |

## 2. 目标 venue / tier（诚实标注）

| 项 | 状态 |
| --- | --- |
| venue family | `CCF-A / AI, ML, CV`（依据 `ccf-a-venue-map.md`：AAAI / NeurIPS / ICML / ICLR / ACL / CVPR / ICCV） |
| 具体 venue | `UNKNOWN` — 用户未指定，按 `intake-protocol.md` 标为 `must-know` 待确认；不得假定为某会议并据此套用当年政策 |
| tier | 假设 `CCF-A`（保守默认，需用户确认） |
| 当年页限 / 匿名 / artifact / 伦理 / 评审表 | `UNVERIFIED` — 依 `privacy-and-evidence.md`，确认 venue 后必须核验官方页面，本包不套用任何具体规则 |

> 决策：本启动阶段 **不锁定具体 venue**；G8 / validation 之前必须由用户确认，否则只按 venue-family 通用证据期望（`evidence-design.md` AI/ML 条：强且近的基线、简单基线、消融、seeds/统计、算力、超参、稳健性、诊断）设计。

## 3. 约束（已核验事实，逐条登记）

### 3.1 硬件 / 软件
- Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / 548 GB 空闲 / conda `dyg-cold`。
- **缺失组件**：`torchvision` 缺失，需补装（G6 blocker）。
- 大规模实验用户已授权上远端 4090（novix），但 **guidance 阶段不提交**（本阶段不触发，G7 按需）。

### 3.2 数据（G1 可得 / G2 排除）
- 详见 `prior-art-opportunity-map.md` 数据集表。
- 诚实边界：CIFAR-10/100 **无官方 val split**，须预注册从 train 切；test 只在最终评测用一次；Tiny-ImageNet test 无标签；CIFAR10-DVS 无官方 split（社区 9000/1000）。

### 3.3 证据 / 隐私
- 用户未发表内部先验（图节点分类 T≤8 达 ANN−1.5pp 带内）仅作 **内部校准**，绝不当公开证据；本次视觉侧 0 正式实验。
- 不声称发明 `β*=θ/(2T)` / 膜电位解码 / 两阶段；不声称精度 SOTA、能耗实测、生物保真。
- 所有 `expected_strong` 写成「预注册目标 / 非实测」+ baseline-calibrated 依据 + failure signal。

### 3.4 范围
- G4 判定 `pass-with-narrowing`，主攻仅限三处真空白（见 `prior-art-opportunity-map.md` §1、§6）。

## 4. 12 个 canonical 阶段

> **编号约定（本包内部组织约定，非外部权威标准）**：`CCFA-startup` → `G0…G8` → `validation` → `handoff`，共 12 门。用户已锚定的语义：`G1` = 数据可得性、`G2` = 数据合规排除、`G4` = novelty gap 判定（`pass-with-narrowing`）；其余按 CCFA 流水线自洽展开并显式标注。
> 每门列：输入 / 输出工件 / pass 判定标准 / blocker 与回退 / owner / handoff / 本启动阶段需做的决定。

| # | 阶段 | owner skill | 输入 | 输出工件 | pass 判定标准 | blocker / 回退 | 本启动阶段需做的决定 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `CCFA-startup` | `ccf-pipeline-orchestrator` | 用户「已核验事实」清单 | 本包 6 工件 + 红队 + 契约草案 | 6 工件齐 + `startup-decision` 取四值之一 + G4 判定已登记 + 无虚构数值/URL/评审分数 + `ccfa.yaml` 缺失已报告 | 缺任一工件 → 不 handoff；venue 未定 → 标 `must-know` | 选 decision 取值；锁定 narrowing 条件与 stop-and-return；确认交付范围不含红队撰写/JSON 生成 |
| 2 | `G0` 资源与可行性基线冻结 | `ccf-pipeline-orchestrator` + `ccf-experiment-designer` | §3 约束 | 环境锁文件、split 预注册、统计协议 | 硬件清单核实、`torchvision` 补装计划、T∈{1,2,4,8,16} / 5 冻结 seeds / 配对 bootstrap R=5000 + sign-flip 1000 + BH / train 切 val 规则锁定 | `torchvision` 未装、split 未预注册 → 停在 G0 | 确认这些属 G0 承接，本阶段只登记不执行 |
| 3 | `G1` 数据可得性 | `ccf-literature-searcher` | 数据集清单 | G1 数据集表 | CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS、Planetoid、ViG 权重直链与字节数已核验（HTTP 200） | 任一链接失效 → 重新核验后再用 | 确认清单为「直接公开」且已写入 `prior-art-opportunity-map.md` |
| 4 | `G2` 数据合规与排除 | `ccf-literature-searcher` | G1 表 | 排除清单 | ImageNet-1K / ILSVRC、ImageNet-100、DVS128 Gesture 明确排除；N-MNIST 标条件性待补证 | 若实验设计偷偷依赖被排除数据 → 打回 G5 | 确认不得用 ImageNet 自跑；官方 ImageNet 数值仅作文献背景，不作本项目 headline 对照 |
| 5 | `G3` 先验与基线 grounding | `ccf-literature-searcher` | 已核验事实 | closest-work 聚类 + 基线代码表 + 官方数值表 | must-rerun 6 个官方仓库已核验；adaptation-attempt 3 个标无代码；literature-context 齐全；官方数值注明来源；TPP 图注不一致已标注 | 某基线代码不可得 → 标 `NOT VERIFIED` 并降级 | 确认「无官方数值一律 NOT VERIFIED」；确认未执行新检索（事实由用户提供） |
| 6 | `G4` novelty gap 判定 | `ccf-idea-optimizer` + 独立红队 Agent | G3 聚类 | `pass-with-narrowing` + 三处真空白 + 硬风险对策 | 数学组件被占清单完整；三处真空白成立；ViG 失效边界诊断已列入 C5 | 若「固定线性算子层类型无关精确统一」被未检索到的论文覆盖 → 回 G3 重搜 | 接受 narrowing，主攻不越界；不声称发明已占组件 |
| 7 | `G5` 主张与契约冻结 | `ccf-experiment-designer` | C1–C5 建议 | `claim-evidence-matrix.md` + `strong-result-feasibility-contract.md` + `feasibility-contract.json`（主会话） | C1–C5 逐条映射完整；只放占位符与决策规则；`expected_strong` 标预注册/非实测且 baseline-calibrated；有 stop-and-return | 出现任何实验结果数值或虚构 URL → 作废重写 | 确认契约阈值由 G7 pilot 后锁定，而非现在填绝对 headline gain |
| 8 | `G6` 实现就绪 / prototype | `ccf-experiment-designer` + 工程执行 | G5 契约 | prototype 里程碑 + 环境锁 + 缺失组件清单 | `torchvision` 补装；统一 `A` 抽象层 / 确定性 `s[t]` 调度器 / 膜电位累加解码 / 恒等式残差探针 / 跨骨干横评 harness 均有里程碑 | ViG 冻结图线性化实现失败 → 回 G4 重估 | 确认不提交 novix；prototype 先跑本机 3060 |
| 9 | `G7` 实验执行与复现 | `ccf-experiment-designer` + 运行 | G6 prototype | must-rerun 基线复现值 + 5 seeds 主实验 + 统计检验 | 基线复现与官方数值偏差在容差内；T∈{1,2,4,8,16}；5 冻结 seeds；配对 bootstrap R=5000 + sign-flip 1000 + BH；test 只用一次 | 基线复现失败 → stop-and-return 到 G6 | 确认大规模实验授权仅在此门之后按需上 4090 |
| 10 | `G8` 结果对齐与评审应答 | `ccf-experiment-designer` → `ccf-paper-writer` | G7 结果 | 结果表/图 spec + claim-evidence 对齐 + failure/boundary 诊断 | 每条 claim 有对应证据且方向一致；C5 失效边界按预测；回答 `evidence-design.md` 的 7 类评审问题 | claim 与证据不一致 → 回 G5 收窄主张 | 确认停在证据包，不写论文散文（本包职责外） |
| 11 | `validation` 诚信与完整性审计 | `ccf-integrity-auditor` | G8 证据包 | 数值/claim/图表一致性审计 + 诚实边界核查 | 无虚构数值/URL/评审分数；内部先验未当公开证据；不声称发明已占组件/能耗实测/生物保真；TPP 图注不一致标注保留 | 任一虚构 → 打回 | 确认审计为 handoff 前必过门 |
| 12 | `handoff` 交付 | `ccf-pipeline-orchestrator` → 主会话 / 下一阶段 | 全套工件 | startup packet 全套 + `ccfa.yaml` patch 建议 + next-owner | 6+1+1 工件齐；decision 已取一值；stop-and-return 显式；patch 建议已给 | 缺任一工件 → 不 handoff | 确认交付范围不含红队撰写与 JSON 生成 |

**Handoff 链**：1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12。任一门 blocker 触发时按该门「回退」列执行，不跳门。

## 5. 本阶段（CCFA-startup）Gate decision

- 前置：G1 / G2 / G3 / G4 的事实已由用户提供并核验；G0 / G5 的规划类工件在本包内产出；G6–G8、validation 尚未执行（本阶段不执行）。
- 本阶段 pass 条件：6 个工件齐（含本文件）、`startup-decision.md` 取四值之一、无虚构数值/URL/评审分数、`ccfa.yaml` 缺失已报告、三处真空白与硬风险对策已登记。
- 结论：见 `startup-decision.md`（取值 + 依据 + conditions + stop-and-return）。

## 6. Handoff packet

- 本 Agent 产出 6 个：`startup-stage-plan.md`、`idea-cards.md`、`prior-art-opportunity-map.md`、`claim-evidence-matrix.md`、`strong-result-feasibility-contract.md`、`startup-decision.md`。
- 独立 Agent：`idea-red-team-review.md`。
- 主会话：`feasibility-contract.json`（按 `strong-result-feasibility-contract.md` 内容哈希生成）。
- Next owner：`ccf-experiment-designer`（承接 G6 → G7）。
- 首个下游动作：补装 `torchvision`；按 G0 锁定 split / 统计预注册；按 G5 契约在 pilot 后锁定 baseline-calibrated 阈值。

## 7. ccfa.yaml 更新建议（不静默改写）

- 现状：项目目录内未找到 `ccfa.yaml` → **project-state tracking unavailable**（orchestrator Workflow §2）。
- 建议由 `ccf-project-scaffolder` 创建，或由主会话在 handoff 时按 `ccfa-yaml-contract.md` 初始化：`version`、`project`、`target_venue`（填 `UNKNOWN/待确认`）、`stage: CCFA-startup`、`artifacts`（登记 6+1 工件）、`claims`（C1–C5 占位）、`experiments`（占位）、`reviews`（登记红队）、`revision_ledger`、`submission_checks`。
- G4 的 `pass-with-narrowing` 建议写入 `stage` / gate 备注。

## 8. 风险 / blockers（分级，按 `ccf-idea-optimizer` 风险标签）

| 风险 | 标签 | 处置 |
| --- | --- | --- |
| 原版 ViG 的 max-relative 聚合含 max 非线性 + KNN 动态图，破坏线性/固定算子假设 | `design-fixable`（已列入 C5 失效边界诊断） | 冻结图 + 线性化；原版 ViG 作为失效边界诊断实验 |
| 数学组件已被占（β* / 零期望偏置 / 膜电位+等式 / 确定性计数 / 两阶段 / 跨 CNN+GCN） | `writing-fixable`（定位收窄） | 只主张三处真空白，不声称发明已占组件 |
| 视觉侧 0 正式实验 | `requires-new-result` | G6 / G7 承接，本阶段不得填任何结果数值 |
| `torchvision` 缺失 | `design-fixable` | G6 blocker，补装 |
| 具体 venue / tier 未定 | `venue-mismatch`（潜在） | 标 `must-know`，确认前只按 family 通用期望 |
| `ccfa.yaml` 缺失 | `design-fixable` | 报告不可用 + 给 patch 建议 |
| 官方 ImageNet 数值不可作本项目自跑对照（G2 排除） | `evidence-fixable` | 仅作文献背景；阈值以 G7 同协议复现值为锚 |
| 内部先验不可公开 | `evidence-fixable` | 仅内部校准，绝不当证据 |

## 9. No-fabrication / 自检状态

```
Mode: standard
Checks run: 12 门齐、owner/handoff 命名、约束登记、隐私边界、无虚构数值/URL/评审分数
Checks skipped: 未做下游检索/实验/评审（orchestrator 职责边界）
Unresolved: 具体 venue/tier、ccfa.yaml、torchvision、novix 提交时机、C1–C5 实测数值（一律 TBD）
```
