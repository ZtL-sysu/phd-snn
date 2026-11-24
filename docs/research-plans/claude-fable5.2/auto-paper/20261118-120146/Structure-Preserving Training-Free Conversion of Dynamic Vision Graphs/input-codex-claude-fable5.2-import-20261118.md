# codex-claude-fable5.2-import-20261118

## Task

把用户指定的 GitHub 仓库和 Notion 页面拉到本地，并统一标记为 `claude-fable5.2` 研究方案。

## Actions

- 浅克隆 `https://github.com/Casey-sketch-cyber/gnn2gsnn.git` 到 `docs/research-plans/claude-fable5.2/github-gnn2gsnn/`。
- 抓取 Notion 主页面、12 个子页面和“文献库”数据库，保留原始 JSON、Markdown 和附件。
- 新建 `README.md`、`source-manifest.json` 和可复跑的 `export_notion.py`。

## Verified

- GitHub HEAD 为 `14f616f6b5d589af4c3a983fde0c61d729344133`，21 个跟踪文件，工作树干净。
- Notion 导出包含 13 份页面 Markdown、115 条文献记录、9 个附件和 19 份原始 JSON。
- 校验结果为 0 个缺失块、0 个空页面、0 个附件错误。

## Decisions

- `claude-fable5.2` 仅作为外部研究方案来源标签，不视为项目已采纳路线。
- 当前 CERT-C11 → POS-C13 顺序保持不变。
- GitHub clone 保留独立 `.git` 元数据，作为本地来源快照，不作为顶层 Git 子模块提交。

## Open Items

- 文献事实、性能数字、研究空白和候选选题尚未独立复核。
- 是否把该方案中的候选方向接入现有实验，需要用户另行决定。

## Resume Entry

目标：继续评估或使用 `claude-fable5.2` 材料。入口文件是 `docs/research-plans/claude-fable5.2/README.md`；先读 `notion-export/markdown/README.md` 和 GitHub 的 `docs/literature-tree/literature-tree-v1.md`，再按需要查询 `notion-export/markdown/12-literature.md`。不要把导入材料直接写成已验证结论，也不要覆盖当前 CERT-C11 任务。
