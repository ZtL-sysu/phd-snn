# Execution Contract v1（f-research-v1 run，immutable）

> 生成 2026-11-10 17:23 GMT+8｜`f-research-v1` 运行局部不可变契约。修改须新建 v2 并在 `pipeline-state.json` 记 `reopen` 与整条后缀重验。

## 1. User goal（用户原话意图）

「不要那么悲观，我们的 gnn2snn 的转换方法还是有亮点的，尽管确实是借鉴的别人的。但组合起来也是有变化的，也是我们的创新。现在按 `f-research-v1` 流程去做，核心还是用我们 1028 现有的那套方法搞起，只是放到视觉上去；既然是图神经网络做视觉，就找那种带有图的视觉数据集来做，同时和别人的 ann 转换 snn 算法做对比，和 ann 做对比（+比能耗）」。

## 2. Authorized operations

- ✅ 只读：1028 成稿目录、资料库报告、v1 guidance 与全部证据、本机技能契约、公开数据集与文献
- ✅ 本地写：**仅限本 run root 内**；guidance 目录内新增 `guidance-v2.md` 与 `contract-change-v1-to-v2.md` 已完成
- ✅ 本机计算：`dyg-cold` 环境跑训练/转换/统计；数据下载到 run root `data/`
- ✅ 联网：公开数据集与文献检索
- ✅ 大规模实验：用户此前已授权 `novix-platform` / `exp-4090`；本轮 P0–P5 优先本机 3060，全量扩展时按需提交，不写端点或凭据
- ❌ 不修改、不投稿、不改写 1028 成稿；不修改资料库文档；不修改 v1 guidance 与其证据
- ❌ 不 commit / push / 发布 / 创建或修改定时任务；不提交任何平台任务除非明确需要且已授权
- ❌ 不编造数据、引用、结果、访问状态或评审分数；不把用户预判的能耗优势写成已得结论

## 3. Inputs（输入清单与哈希策略）

| 输入 | 位置 | 用途 |
|---|---|---|
| 权威契约 | `../guidance-v2.md` | 论文大纲、故事、实验计划、预期结果、citation scope |
| 契约变更 | `../contract-change-v1-to-v2.md` + `contracts/contract-change-v1-to-v2.md` | v1→v2 差异与理由 |
| v1 CCFA packet | `../ccfa-startup-packet/` | P1 加载；decision = `proceed`；claim-evidence 与强结果契约按 v2 重做 |
| v1 文献地图 | `../literature-baseline-matrix.md` | G0 证据复用（适用性已核对） |
| v1 三轮独立红队 | `../ccfa-startup-packet/idea-red-team-review*.md` | 保留为历史评审，不抬分、不删除 |
| v1 M0 实跑 | `../evidence-snapshots/m0-results.json` | 恒等式与失效边界的合成算子证据 |
| 1028 核心实现 | `C:\code\phd-snn\auto-paper\20261028-171500\Spiking-GNN-Conversion\f-research-v1-run-20261028-174053-gnn-snn-conv\experiments\core.py` | `train_ann` / `convert` / `check_identity` / `gauge_normalize` |
| 1028 数据加载 | 同目录 `protocols/graph_data.py` | 稀疏邻接处理参考 |
| 视觉图数据 | `https://data.pyg.org/datasets/benchmarking-gnns/{MNIST,CIFAR10}_v2.zip` | 官方 SuperPixel 图，含 train/val/test |
| 硬件探测 | `../hardware-profile.md` + 本轮环境实查 | G5 / P2 |

外部只读原始文件在 prose 中引用；用于验证的快照复制进 run root `contracts/`。

## 4. Scope（科学范围与边界）

- 目标档位：Q1–Q2 类脑与神经网络期刊（IEEE TNNLS / Neural Networks 档）
- 适用算子类：固定、非负、线性的超像素邻接 + 线性全局池化；动态图、注意力重加权、非线性池化排除并作失效边界
- 主指标：图级 top-1 与 conversion loss（pp）；效率量为 MAC/AC/SynOps 与理论算术能耗估算
- **能耗边界**：45 nm CMOS 表（MAC 4.6 pJ、AC 0.9 pJ）的理论估算，明确不是硬件实测焦耳数；用户预判的优势按可证伪假设预注册，由实验裁定
- 定位：组合与适配创新（组件继承逐条写明），不声称发明单个组件；1028 未发表成果只作方法出处与 baseline-calibrated 锚点
- 不主张：精度 SOTA、硬件实测能耗、生物保真、覆盖 ImageNet-1K 全量

## 5. Resource / runtime envelope

- 本机 Windows 11 / 12 核 / RTX 3060 12288 MiB / CUDA 12.8 / torch 2.11.0+cu128 / Python 3.13.13 / numpy 2.4.4 / scipy 1.18.0 / PyG 2.8.0.post1 / 548 GB 空闲
- 已装：torch、numpy、scipy、scikit-learn、torch-geometric、matplotlib、pandas；`torchvision`、`skimage` 缺失（本方案不依赖）
- 本机单臂 ≤30 min（含 5 seeds）；全量扩展转远端 `exp-4090` ≤6 h/臂；5 冻结 seeds、T∈{1,2,4,8,16}、每方法超参 ≤12 组
- 数据：官方两个 zip 合计约 509 MB（192,378,381 B + 316,368,127 B）

## 6. Output root（路径边界）

`C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\`

所有 protocol、trace、log、result table、figure source、TeX、PDF、audit、manifest 与交付包均在此目录内；外部计算目录与工具缓存仅为临时位置，用于主张或交付的内容必须同步进本目录并登记。

## 7. Quality requirements

- `pipeline_state.py --before <stage>` 逐门通过；`--complete` 通过；`--submission-ready` 明确为 false
- P1 校验 guidance-v2 结构；P1A 强结果锁全 pass 才进 P2；P1B/P3A/P5A 为停损门
- P5 未达 `expected_strong` 不得进 P6 写作（技能硬规则）
- 引用绑定：`min_unique=36`、`as_of=2026`、窗口 2022–2026、严格近期多数
- 论文六个主节严格为 `1 Introduction` / `2 Related Work` / `3 Method` / `4 Experiments and Results` / `5 Discussion` / `6 Conclusion`
- 所有数值由脚本从结果文件生成；负结果保留；`observed_finding` 不早于 P5A

## 8. Writing / editing scope（f-research-v1 启动要求）

- `edit_scope`: 仅本 run root 内由本流程生成的手稿与产物；1028 成稿、v1 guidance 及其证据为只读
- `protected_sections`: 1028 成稿全部章节；v1 guidance 与其 CCFA packet 原文
- `protected_artifacts`: `../guidance.md`、`../guidance-pipeline-state.md`、`../ccfa-startup-packet/*`、`../evidence-snapshots/m0-results.json`
- `declaration_mode`: `author-managed`（数据/代码可用性、利益冲突、基金、生成式 AI 声明待作者决定，不默认插入正文）
- `allow_new_experiments`: 是，但须在授权范围内、记录 trial ledger、不得使用受限数据
- `editing_round_budget`: 3 轮；连续两轮未减少具体缺陷则停止并报告

## 9. Relevant user preferences

- 「跑代码在本机 conda 里跑」→ `dyg-cold`
- 「小规模本机 3060 smoke 更快」→ P2/P3 先本机小子集
- 「大规模实验上 novix-platform」→ 已授权，本轮按需
- 「组合创新也是创新」→ 论文定位按组合与适配创新，不主动唱衰，但不虚构归属
- 「和 ann 比能耗，一定有优势」→ 做成核心对照实验与预注册可证伪假设，由真实结果裁定

## 10. Installed dependencies / availability notes

- `f-research-v1` 技能与 `scripts/pipeline_state.py` 已安装并验证
- AutoResearchClaw 阶段 16/17/18/19/20/22/23、`nature-figure`、`ml-paper-writing`、`paper-compile` 等依赖按 `references/dependency-map.md` 在 P2 前核验实际接口，未核验不得谎称已执行
- 运行模型/effort 本会话未暴露，不推断；不改全局设置

## 11. Delivery readiness

`workflow_complete` 与 `submission_ready` 分开记录；当前 `delivery_mode = preparation`、`submission_ready = false`。作者信息、投稿确认、代码发布、目标 venue 官方规则属作者管理待决项，不阻塞本地科学阶段。
