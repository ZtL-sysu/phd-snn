# Execution Contract v2（immutable，版本化契约变更）

> 生成 2026-11-10｜取代 `execution-contract-v1.md`（原文保留，不删除、不改写）。
> 变更触发：用户明确授权「按证据定稿」，见 `contracts/precision-claim-authorization.md`；权威契约由 `../guidance-v2.md` 变更为 `../guidance-v3.md`。
> 按 `f-research-v1` 修正回路与 `research-recovery.md`，本次契约变更使 canonical 顺序从 P0 重新起算；未受影响的实验证据经适用性核对后复用。

## 1. User goal（完整指令链）

- 17:19：核心用 1028 成稿那套方法，放到**自带图的视觉数据集**；与别人的 ANN→SNN 转换算法对比、与 ANN 对比并比能耗；组合创新是主张；按 `f-research-v1` 全流程做。
- 18:00：跑代码用显卡（3060 CUDA）加速；后续全量实验放 novix（后因平台长时间零分配而改回本机）。
- 18:42：目标肯定是冲强结果，**故事不能再退**。
- 22:25：4090 仍在排队就**不等了**，直接本机 3060；模板用 CVPR，页数按 CVPR 要求。
- 本轮：选择「按证据定稿」，授权把精度主张改为实测 conversion loss + 显式精度—能耗 Pareto 前沿，随即进 P6–P21 写作排版链。

## 2. Authorized operations

- ✅ 只读：1028 成稿、资料库报告、v1/v2 guidance 与全部 E1–E18 证据
- ✅ 本地写：**仅限本 run root 内**（guidance_dir 根另新增 `guidance-v3.md`）
- ✅ 本机计算：`dyg-cold` / CUDA；数据已完整落盘
- ✅ 写作链：P6–P21 全部本地执行，含 TeX 编译（TeX Live 2026 可用）
- ✅ 图表：数据图由 matplotlib 从结果文件生成；整体框架图按技能要求用图像生成模型
- ❌ 不改故事五条定位、不下调横评/能耗/恒等式三项目标
- ❌ 不把 1.57pp 表述为达到 1.5pp 带；不隐藏 E18 负结果；不把 val 冒充 test；不把理论能耗写成硬件实测
- ❌ 不投稿、不 commit/push、不填写作者/Paper ID 等待决项

## 3. Inputs（复用证据的适用性核对）

| 输入 | 位置 | 适用性核对 |
|---|---|---|
| 权威契约 | `../guidance-v3.md`（快照 `contracts/guidance-v3.snapshot.md`） | `--strict` 与 `--strict --packet` 均 rc=0 |
| 授权凭证 | `contracts/precision-claim-authorization.md` | 明确记录授权范围与禁止项 |
| 提交约束 | `contracts/submission-constraints.md`、`contracts/manuscript-metadata.md` | CVPR 官方指南 + author-kit，编译烟测 rc=0 |
| 实验原始结果 | `results/*.json`（E1–E18 全部） | 数据/split/seed/环境/门准则未变；四组 holdout 互不相交 |
| 主结果 | `results/e17/confirmation.json`、`results/e18/confirmation.json` | E17 为第三组 holdout 5-seed；E18 为第四组（负结果） |
| 横评与消融 | `results/local_full/`、`results/local_full_v2/`、`results/paired_analysis.json` | 5-seed 全量，配对差值 |
| 恒等式 | `protocols/run_e17.py` 的 `convert_f64` | 全程 fp64，冒烟 2.47e-15 |
| 历史评审与审计 | `audits/`、`contracts/`、`ccfa-startup-packet/` | 三轮独立红队原文保留，未抬分 |

**复用条件**：以上结果的代码、数据、split、seed、环境（Windows 11 / 3060 / CUDA 12.8 / torch 2.11.0 / `dyg-cold`）与门准则均未改变；v3 仅改变精度带的验收表述，不改变任何已报告数值。

## 4. Scope（科学范围）

- 覆盖固定、非负、线性超像素邻接 + 线性全局池化；不覆盖动态图、动态注意力、非线性池化
- 主指标：图级 top-1 与 conversion loss（pp）；效率量均为 45 nm 理论算术能耗估算
- 精度主张（授权后）：在双口径 ≥5× 能效约束下报告实测 conversion loss 与显式精度—能耗 Pareto 前沿
- 不主张：精度 SOTA、硬件实测能耗、生物保真、ImageNet-1K 规模
- 目标档位：CVPR 主会档；正文 ≤8 页（含图表），仅参考文献页不计入

## 5. Resource / runtime envelope

- 本机：Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / 548 GB 空闲
- 已装：`numpy`、`scipy`、`torch`、`torch_geometric`、`matplotlib`、`pandas`；`torchvision`/`skimage` 缺失但本方案不依赖
- TeX Live 2026：`pdflatex` / `latexmk` / `bibtex` / `xelatex`
- 远端 novix `exp-4090`：任务 `20049` 长时间 `queued / NO_ALLOCATION`，按用户指令不再等待；不 cancel、不重提
- 写作链在 run root 内完成，产物不落到全局目录

## 6. Output root

`C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\`

写作链产物：`writing/`（大纲与草稿）、`figures/`、`tex/`（主 TeX、章节、表格、参考文献、编译 PDF）、`audits/`、`DELIVERY-MANIFEST.md`。

## 7. Quality requirements

- `pipeline_state.py --before <stage>` 逐门通过；`--complete` 通过；`--submission-ready` 明确为 false
- P5 依 v3 验收口径接受；P6 前不得起草
- 引用 ≥36 条、2022–2026 严格多数、去重审计
- 六节主结构严格为 `1 Introduction` … `6 Conclusion`；结论后无研究内容
- 编译 PDF 与 TeX/参考文献/图表同源；8 页硬限由 PDF 页数核验
- 所有数值由脚本从结果文件生成，禁止手抄进表

## 8. Writing / editing scope

- `edit_scope`：本 run root 内由本流程生成的手稿与产物
- `protected_artifacts`：1028 成稿、`../guidance.md`、`../guidance-v2.md`、`../ccfa-startup-packet/*`、`results/*.json` 原始数据
- `declaration_mode`：`author-managed`（数据/代码可用性、利益冲突、基金、生成式 AI 声明不默认写进正文）
- `allow_new_experiments`：是，但须在授权范围内且记录 trial ledger
- `editing_round_budget`：3 轮；连续两轮未减少具体缺陷则停止并报告

## 9. Delivery readiness

`workflow_complete` 与 `submission_ready` 分开记录。当前 `delivery_mode = preparation`、`submission_ready = false`：作者信息、Paper ID、OpenReview 资料、compute reporting 表单、投稿授权均待作者管理，见 `contracts/manuscript-metadata.md` 与 `delivery-readiness.json`。
