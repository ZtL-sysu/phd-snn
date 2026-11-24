# Manuscript Metadata · 唯一权威记录（P20）

> 模板与页数口径见 `submission-constraints.md`（CVPR 2026，正文 ≤ 8 页，参考文献另计）。
> 本文件是 TeX / PDF / 封面 / 补充材料 / 投稿表单的**唯一元数据来源**，所有字段必须逐字一致。

## 1. 已定稿字段

| 字段 | 值 | 来源 |
|---|---|---|
| Canonical title | **Converting Graph Neural Networks for Graph-Structured Vision: Exact Error Identity, Closed-Form Bias, and Energy-Efficient Spiking Inference on Superpixel Graphs** | `../guidance-v2.md`（用户 17:19 修订契约） |
| Target venue | CVPR 2026 主会（用户 22:25 指定模板与页数；由原 Q1–Q2 期刊档升档） | 用户指令 |
| Template | CVPR official LaTeX author kit（`cvpr.sty` / `ieeenat_fullname.bst` / `main.tex` / `preamble.tex`），`\usepackage[review]{cvpr}`；编译烟测 rc=0 | `submission-constraints.md` |
| Hard length | 正文 ≤ 8 页（含图表），仅参考文献页不计入 | CVPR 2026 Author Guidelines |
| Language | English | CVPR LaTeX guidelines |
| Main sections | 严格六节：`1 Introduction` … `6 Conclusion` | `f-research-v1` 非协商规则 |
| Review mode | 双盲；作者/单位/致谢/基金号/可识别链接一律不出现 | CVPR 2026 |
| Paper ID | 模板占位 `*****`（**未分配，不得编造**） | 官方 guidelines |
| Ruler | review 版保留 | 官方 LaTeX guidelines |

## 2. 作者管理的待决字段（不得推断填充）

| 字段 | 状态 | Owner | 影响面 |
|---|---|---|---|
| 作者姓名与顺序 | pending | 作者 | TeX 作者块（camera-ready）、OpenReview、cover letter |
| 单位 / 通讯作者 / 邮箱 | pending | 作者 | 同上 |
| OpenReview 资料完整性 | pending | 作者 | 未完成的资料会被 desk reject（官方明文） |
| Paper ID | pending | 投稿系统 | review 版页眉 |
| 摘要 / 关键词 | pending（正文摘要由 P7 依证据起草，最终由作者确认） | 作者 + 流水线 | TeX abstract |
| 基金 / 利益冲突 / 数据代码可用性 / 生成式 AI 声明 | pending，按 CVPR 表单路由，不默认插入正文 | 作者 | 单独声明与投稿表单 |
| Compute reporting 表单（CVPR 2026 新增，不影响评审） | pending | 作者 | 随全文提交 |
| 补充材料（代码 / 附加图表） | pending，鼓励但非强制 | 作者 | 单独 PDF/zip |
| 是否投稿 / 何时投稿 | **未授权** | 作者 | 不 submit、不 commit、不 push |

## 3. 一致性规则

- `declaration_mode = author-managed`：数据/代码可用性、利益冲突、基金、生成式 AI 声明不默认写进正文。
- 任何元数据变更必须新建版本并**重新编译** PDF，重算受约束字段（页数、摘要、图题），再重跑引用/图表/专业性检查。
- 最终 TeX、编译 PDF、参考文献、图、源码包、嵌套副本必须表示同一已接受修订；陈旧副本判交付失败。
- `submission_ready = false` 直至第 2 节全部待决项关闭；`workflow_complete` 与之分开记录。

## 4. 当前阶段

P5 强结果锁仍未通过（精度 1.5pp 带、带内能耗 5×、恒等式 <1e-10 待核）。按 `f-research-v1` 硬规则 **P6 起草被禁止**，本文件与 CVPR 模板属 P13/P15/P16/P20 的前置准备，不代表已进入写作阶段。
