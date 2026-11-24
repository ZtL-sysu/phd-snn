# Tasks

| Task | Status | Owner | Scope / files | Depends on |
|---|---|---|---|---|
| 盘点同级 gnn2snn 目录与 Git/worktree 状态 | done | codex-reorg-20261117 | `C:\code\gnn2snn*` | none |
| 把同级 gnn2snn 资料收拢到统一入口 | done | codex-reorg-20261117 | `archive-gnn2snn/` | 盘点 |
| 保留数据集、研究代码和有用权重 | done | codex-reorg-20261117 | `auto-paper/`、`third_party/`、`archive-gnn2snn/` | 盘点 |
| 删除/隔离无用重复项 | done | codex-reorg-20261117 | `archive-gnn2snn/trash/` | SHA256 去重；用户确认后已永久删除 |
| 建立本地研究同步日记 | done | codex-reorg-20261117 | `AGENTS.md`、`collaboration/` | none |
| 初始化顶层 Git 并同步到 GitHub | done | codex-reorg-20261117 | 顶层 `.gitignore`、`AGENTS.md`、`collaboration/`、少量文档 | 历史授权已确认 `ZtL-sysu/gnn2snn`；远端 SHA 已验证 |
| 永久删除 trash | done | codex-reorg-20261117 | `archive-gnn2snn/trash/` | 用户确认；124 文件约 6.38 GiB 已删除 |
| 创建 GitHub PR | todo | unassigned | `docs/resource-reorg-20261117` | 用户确认 |
| 根目录二次整理：脚本与 `_nv*` 归档 | done | codex-reorg-20261117 | `legacy/`、根目录兼容链接 | 用户要求 |
| 删除根目录 `_nv*` 兼容链接并收拢 docs | done | codex-reorg-20261117 | `legacy/`、`docs/agent-prompts/` | 用户再次明确要求 |
| 系统检索 GNN→SNN 空白并循环验证 10 个候选 | done | codex-idea-smoke-20261117 | `auto-paper/20261117-210314/`；10 项通过冻结 smoke，9 项拒绝/不确定；32/32 tests | 本机 Conda/CUDA；结果见 `idea-portfolio.md`、`rejection-summary.md` |
| 按 10 个 idea 顺序执行 f-research-v1 全量实验并独立 CCFA 评分 | done | codex-full-experiments-20261117 | `auto-paper/20261117-210314/full-experiments/f-research-v1-run-20261117-220203-ten-idea-full/` | RTX3060；P0–P5A passed，13/13 tests；交付 `deliverables/ten-idea-full-experiment-and-ccfa-review.md` |
| 完成评分≥5的 LR/CERT/POS 全部 f-research-v1 流程 | done | codex-score5-full-pipeline-20261117；codex-fable5-research-20261118 完成 POS 收口 | `auto-paper/20261117-210314/full-experiments/selected/`；LR/CERT/POS P0–P21 passed 并交付最终包；POS 最终包为 `...POS-C13\f-research-v1-run-20261118-113346-pos-hop-event-controls-v3\deliverables\POS-C13-final-v2` | RTX3060/ARC/TeX；不降低强门槛；`POS-C13-final-v1` 与 fable5 V2 均保留为负证据 |
| LR-C05 冻结稿件 CCFA full integrity audit | done | codex-ccfa-integrity-auditor-20261118 | `auto-paper/20261117-210314/full-experiments/selected/LR-C05/f-research-v1-run-20261118-004321-lr-logit-fidelity-v3/ccfa-full-integrity-audit.md`；只读核对 claim/numeric/figure/citation，未修改稿件 | 指定 JSON/CSV/审计文件；F8 evidence-path 与 Figure 1 direct-GPT gate 需后续闭环 |
| LR-C05 冻结稿独立 CCFA full review | done | codex-ccfa-full-review-20261118 | 只读评审 `auto-paper/20261117-210314/full-experiments/selected/LR-C05/f-research-v1-run-20261118-004321-lr-logit-fidelity-v3/` 指定手稿、证据、ARC 评审和原始结果摘要；已输出 `ccfa-full-paper-review.md` | 不改手稿、不跑实验；校准 5/10、confidence 4/5 |
| 拉取 GitHub/Notion 并标记 claude-fable5.2 研究方案 | done | codex-claude-fable5.2-import-20261118 | `docs/research-plans/claude-fable5.2/`；GitHub 快照提交 `14f616f`、Notion 13 页/115 条文献/9 个附件、来源清单与导出器 | 已完成；材料仅标记为外部研究方案，未改变 CERT-C11 → POS-C13 路线 |
| 用 claude-fable5.2 材料构建并执行不降级研究管线 | doing | codex-fable5-research-20261118 | `docs/research-plans/claude-fable5.2/auto-paper/20261118-120146/`；builder 全门通过，选定动态视觉图免训练转换方向；f-research-v1 P0 运行根已建立 | 用户明确要求以该材料开展研究并循环到强结果；本机 Conda/CUDA |
| 两篇成稿的指导偏差审计、期刊实验增强与投稿写作优化 | done | claude-journal-upgrade-20261118 | `auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261118-181848-journal-upgrade/`；偏差审计+实验+E系列+两篇期刊稿+scientific-paper-writing+f-submit-v1 双管线 S0–S10 交付包；验证器全过 | 用户 goal；严格 f-research-v1 P0–P21；未投稿，作者/期刊字段 author-pending |
| 两篇稿件+文档+code+fable 素材上传公开仓库 gnn2snn-v2 | done | claude-journal-upgrade-20261118 | `https://github.com/ZtL-sysu/gnn2snn-v2`（公开，main@a622b46）；233 文件/11MB：两篇 LaTeX+PDF、审计与 f-submit 文档、protocols/writing/engine 代码、结果 JSON、fable-material；数据集/权重/凭证/本地路径已排除（路径已脱敏 [WORKSPACE]，秘密扫描 0 命中） | 用户明确要求；本地暂存 `C:/code/gnn2snn-v2` |
