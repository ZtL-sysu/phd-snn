# Dataset Access Log（G1 / G2）

> 核验日期 2026-11-10｜由独立核验 Agent 用 WebFetch/WebSearch + HTTP 实测定成；标「实测」的字节数来自本次 HTTP 请求。
> 判定口径：**G1 直接公开** = 存在可核验直链且无需登录/申请/机构审批/付费；使用条款限制（如非商业）≠ 访问审批，单独标注。
> 绝不把 "available on request" / "contact authors" / 需登录手动下载写成直接公开。

## 1. 纳入 G1 的数据集（主实验可用）

| 数据集 | 官方 URL / 直链 | 实测大小 | 许可/条款 | 规模与 split | 访问摩擦 | 决定 |
|---|---|---|---|---|---|---|
| **CIFAR-10** | `https://www.cs.toronto.edu/~kriz/cifar.html` → `cifar-10-python.tar.gz`（301→`cave.cs.toronto.edu`）；HF `huggingface.co/datasets/uoft-cs/cifar10` | 170,498,071 B（HTTP 200，`application/x-gzip`），md5 `c58f30108f718f92721af3b95e74349a` | **license NOT VERIFIED**（官方页仅要求引用 Krizhevsky 2009；HF 标 `unknown`） | 60,000 张 32×32、10 类；官方 50,000 train / 10,000 test；**无官方 val split** | 无 | ✅ G1 |
| **CIFAR-100** | 同上 `cifar-100-python.tar.gz`；HF `.../cifar100` | 169,001,437 B，md5 `eb9058c3a382ffc7106e4002c42a8d85` | 同 CIFAR-10，NOT VERIFIED | 100 细类 + 20 超类；50,000/10,000 | 无 | ✅ G1 |
| **Tiny-ImageNet** | `http://cs231n.stanford.edu/tiny-imagenet-200.zip` → 301 → HTTPS | 248,100,043 B（HTTP 200，`application/zip`） | 底层图像源自 ImageNet，镜像注明 **non-commercial research**；Stanford 直链无独立 license 声明 | 200 类 64×64；100,000 train / 10,000 val / 10,000 test（**test 无标签**） | 无（可直接 wget） | ✅ G1（附使用限制） |
| **CIFAR10-DVS** | figshare `https://figshare.com/articles/dataset/CIFAR10_DVS_New/4724671`，DOI `10.6084/m9.figshare.4724671`；直链 `ndownloader.figshare.com/files/{id}` | 8,384,752,624 B（figshare API 精确总和）；GET Range 实测 206 | **CC BY 4.0** | 10,000 段事件流、10 类、128×128；**无官方 split**，社区惯例 9000/1000（SpikingJelly `split_ratio=0.9`） | 无 | ✅ G1 |
| **Cora / CiteSeer / PubMed** | `https://github.com/kimiyoung/planetoid`（`data/`）；PyG Planetoid 文档 | `ind.cora.x` 实测 22,119 B（raw 直链 HTTP 200）；整包大小 NOT VERIFIED | **NOT VERIFIED**（仓库无 License 文件，仅要求引用 Yang et al. ICML 2016） | Cora 2708/10556/1433/7类；CiteSeer 3327/9104/3703/6类；PubMed 19717/88648/500/3类；`split='public'` 每类 20 train / 500 val / 1000 test | 无，程序化 `download=True` | ✅ G1 |
| **ViG 代码 + 预训练权重** | `https://github.com/huawei-noah/Efficient-AI-Backbones`（原 `CV-Backbones` 已更名重定向），`vig_pytorch/` | 8 个权重实测：vig_ti 29,090,248 B … pvig_b 382,087,395 B | **Apache-2.0**（`vig_pytorch/License.txt` 已核验） | 模型仓库非数据集；ViG-Ti 7.1M/1.3G、ViG-S 22.7M/4.5G、ViG-B 86.8M/17.7G，ImageNet-1K Top-1 73.9/80.4/82.3% | GitHub Release 公开直链，无登录 | ✅ G1（权重）；训练复现路径依赖 G2 |

## 2. 排除的数据集（G2，不得记为直接公开）

| 数据集 | 官方 URL | 摩擦 | 决定 |
|---|---|---|---|
| **ImageNet-1K / ILSVRC 2012** | `https://www.image-net.org/download.php`（本轮 3 次 WebFetch 均 fetch failed；条款由 UW Hyak / U Alberta / HF timm 三处交叉核验） | 注册账号 + 机构邮箱 + Research Purpose + 同意 non-commercial 条款 + **人工审批**；`ILSVRC2012_img_train.tar` 等链接审批后下发；HF `timm/imagenet-1k-wds` 为 gated | ❌ G2 |
| **ImageNet-100** | 无官方实体；Kaggle `ambityga/imagenet100`、GitHub 派生集 | 非官方标准数据集、无统一直链/标准 split/统一许可；需 Kaggle 账号或网盘提取码或先持有 ILSVRC 全量 | ❌ G2 |
| **DVS128 Gesture** | 原项目页已失效；现 IBM Box 共享文件夹 | SpikingJelly 文档原文明确「does not allow ... without login ... download manually」；Kaggle 镜像需账号 | ❌ G2 |
| **N-MNIST** | 作者页 `garrickorchard.com/datasets/n-mnist`；Mendeley DOI `10.17632/468j46mzdv.1` | 无单一官方静态直链；**许可冲突**（CC BY-SA 4.0 vs CC BY 4.0）；Mendeley 是否需登录 NOT VERIFIED | ⚠️ 条件性待补证，本轮不用 |

## 3. NOT VERIFIED / 冲突项（不得当已核实事实使用）

CIFAR-10/100 许可状态；CIFAR matlab/binary 版精确字节；Planetoid 仓库 license 与整包大小；N-MNIST 许可与登录要求；DVS128 许可冲突（数据内 CC BY 4.0 vs Kaggle Apache 2.0）与精确字节；ImageNet-1K 官方 tar 精确字节（138 GB 仅第三方 README）；ImageNet-100 规模/split/许可；CIFAR10-DVS 官方 split（**不存在**，9000/1000 为社区惯例）。

## 4. 本项目的 split 预注册（写入 `matched-protocol.md` §5）

- CIFAR-10/100 无官方 val → 固定 seed 从 50,000 train 切 45,000/5,000；test 10,000 **只在最终评测用一次**。
- Tiny-ImageNet 用官方 val 10,000 作最终评测（test 无标签不可用）。
- CIFAR10-DVS 预注册 9,000/1,000，降采样 48×48、T≤20、batch≤32–64（8.38 GB 全分辨率会 OOM）。
- Planetoid 用 `split='public'`，不重切。
- 任何用于方法/超参选择的切分，之后不得再被称为 unseen。

## 5. G1 / G2 结论

**可直接进实验管线的只有**：CIFAR-10/100、Tiny-ImageNet、CIFAR10-DVS、Planetoid 三图、ViG 代码与 8 个公开权重。
**必须排除**：ImageNet-1K、DVS128 Gesture、ImageNet-100。
**合规标注**：CIFAR 系列、Planetoid、N-MNIST 的许可状态未核验或冲突，虽不影响下载，须在论文与实验记录中显式标注；Tiny-ImageNet 底层非商业条款须遵守。

> 因此本 guidance **不做 ImageNet-1K 全量训练**，主战场规模与 IEEE TNNLS / Q1–Q2 期刊档自洽；文献里的 ImageNet 官方数值只作背景，不作本协议下的对照阈值。
