# claude-journal-upgrade-20261118 (running)

## Task

用户 goal：审阅 Paper A/B 两篇成稿与 Fable 5.2 指导素材、f-guidance-builder-v1 指导书的口径偏差；
在本机 Conda/RTX3060 上按 f-research-v1 严格补实验强化到期刊级；完成后两篇分别用
f-submit-v1 + scientific-paper-writing 优化。不实际投稿。

## Run root

`auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261118-181848-journal-upgrade/`
（原两篇成稿在 `f-research-v1-run-20261028-174053-gnn-snn-conv/`，全程只读保护）。

## 已完成（截至本记录）

- P0/P1/P1A（一次记录在案的 reopen 重验收；P1A 又因 P1B 评审重开修订中）。
- 偏差审计 `audits/deviation-audit.md`：Paper B 3 高严重度（引言先例冲突 B-6、深度非目标契约漂移
  B-11 已调和、M-B1 能力缺口 B-1）+ 表1/表3 偏置 provenance（B-8）等；Paper A 3 高严重度
  （SpikeGCL 离散度错句/错归因 A-1、输入约定诊断缺失 A-2、普查总体过度声明 A-3）。0 造假数字。
- E 系列补实验方案：E-B1 逐层步数分配（绑定强结果）/E-B1a/E-B2/E-B3/E-B5、E-A1..A4、W-A/W-B。
- P1B 双独立评审：对抗评审 6/10（JB1 三处 P2 前硬伤 F1 公式/F2 新颖性检索/F3 不可达格，已修
  F1/F3）；完整性审计 BLOCK→R1–R4 已修。台账 `audits/concern-to-action-ledger.md`。
- F2 新颖性 workflow 完成（10 agents）：**逐层时间步分配在转换中已有先例**——PASCAL
  (arXiv:2505.01730) 明文逐层最优时间步、MT-SNN (Front. Neurosci. 2026) 转换管线逐层预算、
  LD-SNN (ISLPED 2022) 已有逐层省 1.67–3.84× 突触更新现象。JB1 已收窄为“闭式谱增益/间隔推导 +
  冻结实现 + 图转换 + ≥20% 结果”，禁“首个逐层分配”措辞，新增 PASCAL-adapted/LD-SNN-search/
  isolation 对照臂；地图 `audits/ccfa-novelty-map-E-B1.md`。
- P0/P1/P1A 已按契约 reopen 后重验收（v1.2/v4）；P1B 焦点复审（独立 agent）运行中。

## P1B–P3 进展（2026-11-18 晚）

- P1B 复审 PASS（8/10），R-A–R-J 残余全部关闭（κ≤1.2 门、整数网格 {1..64}、R-D 计量规格块、
  ≥4/6 可达格规则、L=2 退化声明、Rueckauer 必引等）。P1B 已过。
- P2 过：环境实测（RTX3060/torch2.11cu128/TeX Live 2026/WSL spikg 活/ARC 未装→本地替代）；
  冒烟 Cora 循环+恒等式残差 0.0；chameleon 2277 / squirrel 5201 / arxiv 原始数据在位。
- P3 过，**重大发现**：注册外部臂 `hidden=512` 参数从未进模型——实为 SGC+F→C 单层，
  其 SOP 记账（T×N×512）描述的是代码从未训练的模型（`audits/p3-baseline-findings.md`）。
  E-B2 容量跑 H=16/32 与注册512臂逐种子完全一致即为铁证。修复 E-B2b（真隐藏层 512/32/16 +
  三口径 SOP 记账）脚本已备好 `protocols/jB2b_truewidth.py`，待 P3A 裁决排序后运行。
- P3A 独立止损审计运行中。

## P4 结果结构（2026-11-18 深夜）

- **B 篇正能力（预注册确证）**：LD-SNN 式验证集搜索逐层时间窗分配，L=4 深区 held-out 6/8 格
  守 ANN−1.5pp 带且省 48–93% 层更新（squirrel 4/4；随机对照被击败）；试点同区 6/8（44–90%）；
  L=3 浅区无余量（1/8）。归属：想法家族 LD-SNN 先例，图上实例化+区间测量为本文证据
  （`audits/jB1-search-arm-outcome.md`）。
- **B 篇机制化负结果三连**：闭式分配 R1/R2（冻结判据失败）、JB1a 免扫描选择器（held-out κ 1.2/11、
  chameleon 未达带 → 预注册失败信号触发）、间隙预测器（wp7）。校准图上 JB1a κ=1.0 精确——
  “图内可刻画、跨图不迁移”成为论文核心诊断。
- **SOP 记账敏感性**：预声明事件驱动口径下 WP2 判据触发（F→C 线性读出 T=4 支配 cora/citeseer），
  静态口径转换 3/3 最便宜；Pareto 廉价主张按失败信号收窄，敏感性本身入稿。
- **A 篇**：E-A1 八格补齐（Cora 20.5×/CiteSeer 1.37×/PubMed 0.73× → PubMed 预注册收窄）；
  E-A3 逐字切分原文（Split I/II 原文已取）；E-A4 重放 0 不匹配；E-A2 五变体诊断运行中——
  已确证 50/13/13 三行、纠正第四行（raw 去自环不崩，0.515）。
- 在途：E-A2 五变体、JB1a arxiv 补格。完成后一次性主张登记+契约重验收 → P5/P5A → 写作。

1. 收 F2 novelty workflow 结果 → 写 novelty map、关 `JB1-F2-novelty-gate`。
2. 重收 P1A（v2/v3 契约）→ P1B 焦点复审 → 过 P1B。
3. P2/P3：本机协议、AutoResearchClaw 探测（历史记录显示未安装，须复核）、baseline-first；
   E-B1 原型止损门（headroom ≥1.3、κ≤1.6、冻结引擎恒等式）。
4. P3A/P4/P5：E 系列全量 + 强结果锁；P5A 后进入两篇期刊版写作（六节、预测失败负结果保留）。
5. P19 `scientific-paper-writing`、P20 `f-submit-v1`、P21 交付；作者/venue 事实仍 pending，
   不投稿。

## 关键口径

- `planned_claim` ≠ `observed_finding`；预测 MAE≤1pp 的旧绑定强目标已失败且须保留为负结果。
- guidance-v3“深度>2”非目标 = 禁能力主张，深度边界负结果允许（B-11 调和记录在案）。
- 保护：prior run 全部只读；results/logs append-only。

## 完成记录（2026-11-19）

- f-research-v1 P0–P21 全过（验证器 PASS）；两篇 f-submit-v1 S0–S10 全过（各 `--complete` PASS）。
- 交付：`tex-journal/f-submit-v1-run-20261119-003907-paperB/delivery/` 与
  `tex_audit-journal/f-submit-v1-run-20261119-003907-paperA/delivery/`，各含修订稿 PDF、来源 ZIP
  （干净解包编译 0 错）、上传映射（作者待定字段明列）、交付清单（SHA-256 全量）。
- P9/P5A 双轮独立评审的所有 major 均闭环；S7/S8 三轮编辑逐轮缺陷递减并终验闭合。
- 最终主张结构：B 篇=恒等式/定律 + 深区搜索式逐层分配能力（held-out 6/8、22.7–93.4%，先例归属
  LD-SNN/PASCAL/MT-SNN）+ 三条跨图迁移负结果 + 记账敏感性；A 篇=三种失效模式 + 逐数据集可迁移性
  （1.35×/1.37×/0.73×，一致噪声源重算）+ 五变体约定因果 + 重放闭环。
- 未投稿；作者/期刊/声明字段 author-pending；红线：原两篇成稿（prior run）全程只读未改。

## GitHub 公开仓库交付（2026-11-19）

- 用户要求：把两篇稿件 LaTeX、文档、Fable 5.2 素材、代码上传公开仓库 `gnn2snn-v2`；数据集不上传。
- 仓库：https://github.com/ZtL-sysu/gnn2snn-v2（PUBLIC，`main@a622b46`，233 文件约 11MB）；
  本地暂存树 `C:/code/gnn2snn-v2`（git 身份 repo-local ZtL-sysu）。
- 内容：`paper-b-conversion/`+`paper-a-audit/`（f-submit 终稿 LaTeX+revised-manuscript.pdf，
  哈希已对 delivery-manifest 核验一致）、`docs/journal-upgrade-audits/`+`docs/f-submit-paper-{a,b}/`、
  `code/{protocols,writing,engine}/`、`results/*.json`、`fable-material/`（github 快照+Notion 导出，无 .git）。
- 排除：数据集（.data/Planetoid/ogbn/PyG 缓存）、模型权重、凭证、构建中间件、含本地路径的 logs。
- 安全处理：秘密扫描（ghp_/sk-/AKIA/xox/私钥）0 命中；28 个文本文件本地绝对路径脱敏为 `[WORKSPACE]`；
  残留 `xhf` 命中均为 Notion CRDT base64 ID 误报。README 声明 fable-material 为外部方案素材（未经独立核验）。
