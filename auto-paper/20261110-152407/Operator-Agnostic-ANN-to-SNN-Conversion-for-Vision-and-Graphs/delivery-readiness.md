# Delivery Readiness · 待决清单（可读视图）

> 机器权威：`delivery-readiness.json`。按 `f-guidance-builder-v1/references/deferred-completion.md` 维护。
> `workflow_complete` 与 `submission_ready` 分离：本地工作流可完成，投稿就绪仍为 **false**。

## 状态

- `delivery_mode`: `preparation`
- `workflow_complete`: **true**（12 门顺序通过、校验器通过、产物哈希一致）
- `submission_ready`: **false**（下列作者管理的事实未决）
- 这些**行政/生产待决项不阻塞本地科学阶段**；但科学证据、数据使用权、引用真实性、产物一致性仍是硬门。

| ID | 类别 | 状态 | Owner | 要求 | 来源 | 影响面 | 解锁动作 | 科学影响 |
|---|---|---|---|---|---|---|---|---|
| DR1 | `author-fact` | pending | 作者 | 作者姓名、单位、通讯作者与贡献声明 | 用户本轮未指定 | 首页、元数据、cover letter | 由作者提供后写入稿件元数据 | none |
| DR2 | `author-approval` | pending | 作者 | 是否同意把本新篇与已成稿 GNN2SNN 分开投稿、以及两篇的引用关系 | 用户本轮明确「成稿先不动」 | 相关工作要求、cover letter、潜在 companion 声明 | 由作者确认两篇关系与投稿时序 | none |
| DR3 | `author-fact` | pending | 作者 | 具体目标 venue / tier（当前按 IEEE TNNLS / Q1–Q2 期刊档设计） | 第三轮独立红队标 `must-know`，官方当年 policy 未核验 | 篇幅、图表规则、匿名与 artifact 要求 | 作者确认 venue 后核验官方当年规则 | none |
| DR4 | `access-route` | pending | 作者 | 代码、协议、teacher 权重与冻结图文件的发布/审稿访问安排 | 用户本轮未指定 | artifact、复现包、匿名仓库 | 由作者决定公开范围与时机 | none |
| DR5 | `production` | pending | 作者 | LaTeX 模板、页限、图表与补充材料规则 | 目标 venue 官方当年规则未核验 | 排版、图表数量、附录 | venue 确认后由官方页核验 | none |
| DR6 | `portal` | pending | 作者 | 投稿系统账号、ORCID、基金与利益冲突声明 | 用户本轮未指定 | 投稿表单、声明段落 | 由作者在投稿前填写 | none |
| DR7 | `author-approval` | pending | 作者 | 最终稿审批与所有作者同意投稿 | 用户本轮未授权投稿 | 投稿动作本身 | 由作者显式批准 | none |

## 明确不是待决项（属科学硬门，已由本轮处理）

- 公开数据集可达性与许可标注 —— `dataset-access-log.md`
- 引用真实性、命题级支撑、数量/年份算术 —— 本轮定 citation scope，最终核验由 `f-research-v1` P12/P14 执行
- `expected_strong` 的证据支撑 —— 全部标「预注册 / 非实测」，阈值在 G7 pilot 后锁定
- 成稿内部先验的使用边界 —— H1，全程标注「未公开先验」
- 产物一致性与哈希 —— `pipeline-state.json` + `feasibility-contract.json`

## 交接说明

本包是**本地准备完成、投稿未就绪**的研究契约。下游 `f-research-v1` 从 `guidance.md` 的契约抽取开始；P4 全量实验按 `novix-platform` 流程派往 `exp-4090`（用户已授权，本轮未提交）。`f-guidance-builder-v1` 明确不在此运行实验、不写论文。
