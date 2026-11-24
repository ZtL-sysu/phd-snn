# Dataset Access Log（G1 硬门槛证据）

访问日期：2026-11-05。判定标准：必须能**直接公开下载**，凡需邮件/人工审批/账号审核/
IRB/NDA/付费/"on request" 一律不算通过。

## 通过（可直接下载）

| 数据集 | 直接 URL | 许可 | 体量 | 标签/目标 | 访问摩擦 | 判定 |
|---|---|---|---|---|---|---|
| MaleCNS v1.0 全连接图 | https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/connectome-weights-male-cns-v1.0-minconf-0.5.feather | CC-BY 4.0 | 1.1 GB | `body_pre/body_post/weight` 有向边，作图结构先验 | 无（HTTPS 直连） | PASS |
| MaleCNS 神经元标注（class/type/side） | https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-annotations-male-cns-v1.0-minconf-0.5.feather | CC-BY 4.0 | 13 MB | 细胞类型、脑区、左右侧 | 无 | PASS |
| MaleCNS 神经递质预测 | https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/body-neurotransmitters-male-cns-v1.0.feather | CC-BY 4.0 | 42 MB | 每神经元递质概率 → 边符号 | 无 | PASS |
| FlyWire v783 图包（train-your-fly） | https://github.com/eudald-seeslab/train-your-fly/releases/latest （首次运行自动下载到 `connectome_data/`） | Apache-2.0 代码 / 数据 CC BY 4.0 | ~1.3 GB | `connections.csv`, `classification.csv`, 光感受器 2D 坐标, 4 种随机图 | 无 | PASS |
| 论文用图与随机图存档 | https://doi.org/10.5281/zenodo.21549559 | CC BY 4.0 | — | 生物图 + 4 种随机图 + 注释 + 视网膜映射 | 无 | PASS |
| cogstim 合成视觉刺激 | https://pypi.org/project/cogstim/ 与 https://github.com/eudald-seeslab/cogstim | MIT | 按需生成 | `shapes / colours / ans / one-colour / match-to-sample / lines / fixation / custom`，按类分文件夹 | 无 | PASS |
| FlyWire 注释 v2.1.0 | https://github.com/flyconnectome/flywire_annotations/releases/tag/v2.1.0 | 见仓库 | — | 139,255 神经元 cell type | 无 | PASS |
| 视叶跨数据集 cell-type 匹配 | https://github.com/flyconnectome/ol_annotations | 见仓库 | 小 | FAFB/FlyWire ↔ MaleCNS 视叶对应 | 无 | PASS |

## 有摩擦 / 拒绝

| 资源 | 摩擦 | 判定 |
|---|---|---|
| neuPrint `male-cns:v1.0` API | 需注册账号并获取 API token；官网 Python/R 示例明确要求 token | 不作为 G1 依据（bulk feather 已足够） |
| MIMIC-CXR（X-ray 果蝇博客用到） | 需机构认证/数据使用协议 | REJECT |
| flyvis 神经活动响应数据 | 需按项目文档单独获取，本轮未核验为无摩擦直连 | 暂不作为 G1 依据，仅作 literature-context |
| 商业/私有事件相机数据集 | 需授权 | REJECT |

## G2 任务与评测有效性

- 输入：512×512 PNG 图像（或时序化的图像序列/事件流）；输出：类别标签。
- 已公开任务：颜色辨别（yellow/blue）、形状辨别（circle/star，位置尺寸抖动）、
  数量辨别（ANS，面积受控，Weber ratio 可调）、朝向条纹（`cogstim lines`，角度可设）。
- 论文标准规模：每类 5,000 train / 5,000 val / 5,000 test（train-your-fly 论文）。
  cogstim `--seed` 保证可复现划分。
- 主指标：test accuracy（含 95% CI）；次级：accuracy-vs-Weber-ratio 曲线、
  在等布线/等突触操作预算下的准确率、spike rate、时序任务的首次正确判别时刻。
- 评测协议：固定 seed 生成 train/test，固定图与随机图，线性 Kenyon-cell 读出。
