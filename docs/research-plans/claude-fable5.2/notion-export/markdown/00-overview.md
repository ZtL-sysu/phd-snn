# 视觉图网络免训练转脉冲网络：通俗讲解

> 本地化来源：[Notion 原页面](https://app.notion.com/p/41b0e3342e6f818f86b9d9a6cbc71968)；由 `export_notion.py` 从只读块数据导出。

> 📌
> 这份讲解写给项目所有者：用一张猫的照片贯穿全篇，说明“把训练好的视觉图神经网络，不重新训练就变成省电的脉冲网络”这个方向在做什么、别人做到了哪一步、还空着什么。所有事实都来自仓库 `literature/` 下已核实的条目（任务 01，PR #1 已合并）。

### 怎么读

- 先读“0 一页读懂”和“1 基础概念”，再按需要看后面的页面。
- 每页开头一句话说结论，结尾有“三句话小结”和“读完应该能回答的两个问题”。
- 每条事实后面的链接指向“11 文献库”里的对应论文。
### 三种标注块

> ✅
> **已核实的事实**：来自论文原文或官方代码，并在文献库中有记录。

> 💭
> **判断**：论文作者、Claude 或文献核查得出的看法，不是定论。

> ❓
> **未知**：还没有人研究，或需要做实验才能回答的问题。

### 仓库

- 文献与核查：[https://github.com/Casey-sketch-cyber/gnn2gsnn/tree/main/literature](https://github.com/Casey-sketch-cyber/gnn2gsnn/tree/main/literature)
- 本讲解的导出与图源文件：仓库 `notion/` 目录（分支 `gemini/notion-presentation`）
### 页面

[0 一页读懂](01-one-page.md)

[1 基础概念](02-foundations.md)

[2 时间线：转换技术](03-conversion-timeline.md)

[3 时间线：脉冲图网络](04-spiking-graph-timeline.md)

[4 时间线：视觉图模型](05-vision-graph-models.md)

[5 时间线：只算变化的部分](06-partial-computation.md)

[6 省电到底怎么算](07-energy-accounting.md)

[7 难点地图](08-difficulty-map.md)

[8 可以做的论文](09-paper-ideas.md)

[9 Claude 的判断哪里对、哪里错](10-claude-audit.md)

[10 术语表](11-glossary.md)

[11 文献库](12-literature.md)

**三句话小结**

1. 这组页面把“现成视觉图网络免训练转脉冲网络”拆成基础概念、四条时间线、省电账本、难点地图和候选选题。
1. 绿框是已核实事实，黄框是某一方的判断，灰框是尚待实验或复核的未知项。
1. 建议先读第 0、1 页建立直觉，再按关心的专题查阅第 2–11 页。
**读完应该能回答的两个问题**

- 页面里的绿、黄、灰三种标注块分别代表什么？
- 如果你想查某条事实的原始论文出处，应该点哪里？
