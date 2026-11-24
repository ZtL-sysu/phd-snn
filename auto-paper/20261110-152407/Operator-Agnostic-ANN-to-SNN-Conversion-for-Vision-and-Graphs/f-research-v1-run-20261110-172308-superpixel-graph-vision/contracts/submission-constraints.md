# Submission Constraints · CVPR 2026（P16 / P20 硬限）

> 用户 2026-11-10 22:25 指令：「模版你用 cvpr 的就行，页数要求也是按 cvpr 的要求来」。
> 核验来源：CVPR 2026 Author Guidelines（https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines）与 CVPR 2026 LaTeX Author Guidelines（Overleaf 官方模板 PDF）。核验日期 2026-11-10。

## 1. 官方原句（逐字）

> "Papers are limited to eight pages, including figures and tables, in the CVPR style. Additional pages containing only cited references are allowed. Please download the CVPR 2026 Submission Template for detailed formatting instructions."
>
> "Papers that are not properly anonymized, or do not use the template, or have more than eight pages (excluding references) will be rejected without review."
>
> "Papers, excluding the references section, must be no longer than eight pages in length. The references section will not be included in the page count, and there is no limit on the length of the references section."
>
> "Overlength papers will simply not be reviewed. This includes papers where margins and formatting are deemed to have been significantly altered from those laid down by this style guide."

## 2. 绑定硬限（不可被偏好放宽）

| 项 | 约束 | 判定方式 |
|---|---|---|
| **正文页数** | **≤ 8 页**，含所有图、表、公式、正文；**仅含已引用参考文献**的附加页不计入且无限制 | 编译后 PDF 页数；第 9 页起若出现非参考文献内容即违规 |
| **模板** | 必须使用 CVPR 官方 LaTeX author kit（`cvpr.sty` / `ieeenat_fullname.bst` / `main.tex` / `preamble.tex`），`\documentclass[10pt,twocolumn,letterpaper]{article}` + `\usepackage[review]{cvpr}`；双栏 Times 风格 | 不使用或显著改边距 → desk reject |
| **双盲** | `\usepackage[review]{cvpr}`；不得出现作者/单位/致谢/基金号/可识别链接；自引不得用 "our previous work" 之类自我指代 | 全文扫描 |
| **语言** | 英文 | 全文 |
| **Ruler** | review 版保留行号尺；camera-ready 去掉 | 模板选项 |
| **Paper ID** | review 版显示投稿系统 Paper ID（当前未分配 → 保持模板占位 `*****`，不得编造） | 待作者提供 |
| **外部链接** | 不得以网页/图片/视频链接扩展内容或绕过页数限制 | 全文扫描 |
| **补充材料** | 可选、单独 PDF/zip，不计入 8 页；鼓励附代码，但不强制；评审无义务阅读 | 单独交付物 |
| **Compute reporting** | CVPR 2026 新增计算资源报告表（不影响评审、不向评审展示），随全文提交 | 属作者管理待决表单 |
| **Camera-ready** | 录用后可 +1 页（共 9 页）；本轮按**投稿版 8 页**执行 | 不适用 |

## 3. 与 f 系列流水线约束的叠加

- f 系列六个主节严格为 `1 Introduction` / `2 Related Work` / `3 Method` / `4 Experiments and Results` / `5 Discussion` / `6 Conclusion`；CVPR 允许 `\section` 自定义，但本项目**仍按六节**，取两者交集。
- 结论之后只允许致谢/基金/数据代码声明、参考文献与必需声明；不加附录、不复现性清单、不凑页。
- 引用绑定：`min_unique ≥ 36`，2022–2026 冻结窗口严格多数；参考文献页不计入 8 页，因此不因页数裁掉必需引用。
- 摘要无官方字数硬限（模板要求 10pt 单栏 italic、置顶），按简洁处理。
- 图 1 为整体框架图，数据图由 `nature-figure` 风格生成；图表必须靠近首次讨论处。

## 4. 当前状态

- 目标档位由此前 Q1–Q2 期刊**升为 CVPR 2026 主会档**（用户指定模板与页数；属升档，不违反「故事不能再退」）。五条故事定位与四项 `expected_strong` 仍冻结不变。
- 本机 TeX Live 2026 工具链可用（`pdflatex` / `latexmk` / `bibtex` / `xelatex`）。
- 官方模板已取自 `github.com/cvpr-org/author-kit`（main 分支，模板内标注 **CVPR 2027**）；其自带 `sec/1_intro.tex` 的页数条款为「Papers, excluding the references section, must be no longer than eight pages」，与 CVPR 2026 官方指南逐字一致，故 8 页口径对两个版本都成立。文件：`tex/cvpr.sty`(17,883 B)、`tex/ieeenat_fullname.bst`(26,900 B)、`tex/main.tex`、`tex/preamble.tex`、`tex/rebuttal.tex` 及 `tex/sec/*`、`tex/fig/*`。
- **编译烟测通过**：在 `tex/` 下 `latexmk -pdf main.tex` rc=0，产出 `tex/main.pdf`(209,465 B)。模板自带示例引用未定义属示例占位，非编译错误；正式稿由本项目 `references.bib` 替换。
- 若 CVPR 2027 官方 Author Guidelines 后续发布且与本文件冲突，以官方最新口径为准并版本化更新本文件。
- **P5 强结果锁仍未通过**（精度 1.5pp 带、带内能耗 5×、恒等式 <1e-10 待核）。按 `f-research-v1` 非协商规则，**P5 未过不得进 P6 起草**；本轮继续按 E1–E4 改进冲强结果，达标后立即进入写作与 CVPR 排版。
- `submission_ready = false`：作者信息、Paper ID、OpenReview 资料、compute reporting 表单等属作者管理待决项，见 `manuscript-metadata.md` 与 `delivery-readiness.json`。
