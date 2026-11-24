---
artifact_type: research_plan
research_plan_label: claude-fable5.2
import_status: local_source_snapshot
project_adoption_status: not_adopted
---

# claude-fable5.2 研究方案

本目录将用户指定的 GitHub 资料库与 Notion 讲解统一标记为 `claude-fable5.2` 研究方案。该标记表示来源与材料归档，不表示其中的科研判断已经通过本项目独立核验，也不改变当前 CERT-C11 → POS-C13 的执行路线。

## 本地入口

- GitHub 资料库快照：[README](github-gnn2gsnn/README.md)
- GitHub 文献树：[literature-tree-v1.md](github-gnn2gsnn/docs/literature-tree/literature-tree-v1.md)
- GitHub 文献核查：[literature/](github-gnn2gsnn/literature/)
- Notion 全量导出：[Notion 本地导出](notion-export/markdown/README.md)
- 可复跑导出器：[export_notion.py](export_notion.py)
- 来源与校验信息：[source-manifest.json](source-manifest.json)

## 已核实的归档状态

- GitHub 仓库 `Casey-sketch-cyber/gnn2gsnn` 已浅克隆到 `github-gnn2gsnn/`，固定到提交 `14f616f6b5d589af4c3a983fde0c61d729344133`，克隆工作树干净。
- Notion 主页面及其 12 个子页面已导出为 13 份 Markdown。
- Notion“文献库”数据库已导出 115 条记录，原始 JSON 保留在 `notion-export/raw/`。
- 5 个 SVG 与 4 个交互动画 HTML 已下载到 `notion-export/assets/`，9 个附件均有 SHA256。
- 完整性检查结果：0 个缺失块、0 个空页面、0 个附件下载错误、0 个导出中的 `Not found` 标记。

## 尚未验证

- 未独立复核文献事实、论文结论、性能数字或研究空白。
- 未运行该方案中的实验，也未把其中候选选题纳入当前论文任务。
- GitHub clone 含独立 `.git` 元数据，属于本地来源快照，不应直接作为顶层 Git 子模块提交。
