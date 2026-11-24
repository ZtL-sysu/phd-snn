#!/usr/bin/env python3
"""Build a self-contained novix query with a base64 zip payload."""
from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[1]
TP = R / "teacher_probe"
FILES = [
    "protocols/vision_pipeline.py",
    "protocols/run_e17.py",
    "teacher_probe/run_all.py",
    "teacher_probe/run_bcd.py",
]
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in FILES:
        p = R / f
        assert p.is_file(), p
        z.write(p, f)
payload = base64.b64encode(buf.getvalue()).decode()
print("payload bytes", len(buf.getvalue()), "b64 chars", len(payload))

query = f"""# Novix 全量实验任务：teacher_probe（teacher 归因 + 强 teacher 转换 + 能量 + Table 1 自洽）

你在本任务的 4090 GPU 沙箱中执行一次**可复现的全量实验**。这是一个科研流水线的实验阶段，不是写作任务。所有数值必须由真实运行产生，**严禁编造、估算、插值或引用文献数值冒充实验结果**。

## 0. 输出契约（最高优先级，历史踩坑）

工作区根 `project/` 下必须有：`config.json`、`result.json`、`README.md`、`logs/run.log`、`protocols/*.py`、`teacher_probe/`。
`result.json` 必须落在 `project/` 内（可 pull），不得落在不可 pull 的临时路径。
每个 seed 完成即**追加**写 `project/result.json`；若运行时间将尽，先落盘脚本与阶段性结果再终止。
`project/result.json` 至少含：每个实验的逐 seed 记录、汇总均值±std、config_hash、异常记录。

## 1. 数据（官方 PyG SuperPixel）

下载到 `project/data/pyg_bench/<NAME>/raw/`：
- `https://data.pyg.org/datasets/benchmarking-gnns/MNIST_v2.zip`（192378381 B）
- `https://data.pyg.org/datasets/benchmarking-gnns/CIFAR10_v2.zip`（316368127 B）
用 `torch_geometric.datasets.GNNBenchmarkDataset(root=..., name="MNIST"/"CIFAR10", split=...)` 加载；已存在且字节数正确则跳过下载。校验字节数并记录。

## 2. 代码还原

把下面 §8 的 base64 载荷写入 `/tmp/tp_payload.b64`，执行：
```
base64 -d /tmp/tp_payload.b64 > /tmp/tp_payload.zip
unzip -o /tmp/tp_payload.zip -d project/
```
还原出 `protocols/` 与 `teacher_probe/`。**不要改写这些脚本里的实验配置**；唯一配置来源是 `teacher_probe/config.json`（由 `run_all.py` 生成，含 config_hash）。

## 3. 环境与硬件

检查 `torch.cuda.is_available()`、GPU 型号、torch/torch_geometric 版本；缺依赖则 pip 安装。
固定 `torch.manual_seed`、`numpy`、`random`、`torch.use_deterministic_algorithms(True)`；CUDA 稀疏归约非确定，因此每个点 5 个 seed 并报 std/95% CI。
所有命令在 `project/` 目录执行。

## 4. 执行顺序（按顺序，不要并行改配置）

```
cd project
python -c "import torch;print(torch.__version__, torch.cuda.is_available())"
python -m py_compile protocols/vision_pipeline.py protocols/run_e17.py teacher_probe/run_all.py teacher_probe/run_bcd.py
python -W ignore -u teacher_probe/run_all.py        # 实验 A：T0..T5 × 5 seeds × 2 datasets
python -W ignore -u teacher_probe/run_bcd.py        # 实验 B/C/D + CSV/TeX/图/FINDINGS
python -W ignore -u teacher_probe/repro_and_audit.py  # T0 复现 + Table1 同配置审计（seed 10）
```
`run_all.py` 支持 `--exps/--datasets/--seeds` 分片；**幂等**：已存在的 `(config_hash, seed)` 直接跳过，可断点续跑。
若 OOM/NaN/发散：记入 `teacher_probe/RUNLOG.md`，降 batch 重跑；**不换 seed、不删点、不降训练集规模**（train 规模是实验变量）。

## 5. 实验硬约束（违反即作废）

1. 先复现后扩展：已知论文现值 MNIST teacher 34.02±1.60%、CIFAR10 27.27±1.67%、loss 3.79±2.26pp / 1.57±0.67pp。本机复现发现**偏差超 ±2pp**，差异来源已定位并写在 `teacher_probe/REPRO_BLOCKER.md`（E17 未冻结 base teacher 权重与 unit_mask，mask 由 base 的训练集激活决定，CUDA 非确定导致 mask 不同）。**按该文件执行**：所有新实验把 base 权重与 mask 落盘冻结（`snapshots/`）。
2. **不许在 test split 上选任何东西**：所有 (k, θ, T) 只在 validation 上选，test 只报一次。
3. 报全部 seed，不报 best；每配置 5 seeds（0–4），输出 mean±std 与 95% CI。
4. `conversion loss := teacher_top1 − converted_top1`，**两者必须同配置**（同 k、同宽度、同训练集、同 A、同 R）。`run_bcd.py` 的 `width_model` 已保证这一点。
5. 不改数据管道、不改 split、不改评测；宁可得到负数结论并如实报告。
6. 恒等式 `max|B̂−B − R A(E1W2)|` 必须用**同一个 float64 forward pass**（`convert_f64`），预期 ~1e-14；记录 fp32 与 fp64 重算差距。
7. 能量两套口径都报（45nm：MAC 4.6pJ / AC 0.9pJ）；标注哪些点满足 `teacher > 2× chance`（10 类 → 20%），**不要偷偷放松**。
8. 零脉冲网络（`S=0`）不得报成能效优势。

## 6. 交付清单（全部在 `project/teacher_probe/`）

```
CONFIG_AUDIT.md  REPRO.md  REPRO_BLOCKER.md  RUNLOG.md  FINDINGS.md  run_all.sh
results/teacher_probe.csv
results/strong_teacher_conversion.csv
results/energy.csv
results/fidelity_width.csv
tables/tab_teacher_probe.tex
tables/tab_conversion_strong.tex
tables/tab_energy.tex
tables/tab_table1_fixed.tex
figures/fig_fidelity_width.pdf
figures/fig_frontier_strong.pdf
```
`FINDINGS.md` 必须回答 Q1（34%/27% 里多少来自 2k 图、多少来自宽度 16，用 T0→T1 / T0→T2 差值给点估计与 std）、Q2（强 teacher 上 loss 是否仍 ≤2pp）、Q3（去 β⋆ 是绝对还是相对收益、强 teacher 是否仍成立）、Q4（能量—保真 frontier 与 5× 消失的拐点）、Q5（Table 1 反超审计与泄露检查）。每条 ≤5 句，必须带数字和 CI。
`figures/` 用 matplotlib、无标题、字号 ≥9pt、可直接 `\includegraphics[width=\\linewidth]`。

## 7. 预算与终止

单 run 单卡 ≤10 分钟；若某配置 >30 分钟，停下来在 `result.json` 与 `RUNLOG.md` 记录并报告，不要硬跑。
终止条件：`REPRO.md` 任一偏差 >±2pp（已记录，按 REPRO_BLOCKER 处置）、T5 teacher 低于 T0（数据管道问题）、发现泄露 → 立即停并优先报告。

## 8. 代码载荷（base64 zip）

```
{payload}
```

完成后在最终回复里报告：`project/result.json` 的路径与 SHA-256、`teacher_probe/` 交付清单、以及 Q1–Q5 的一句话结论。
"""
# Windows/Git Bash ARG_MAX is ~32 KiB; trim prose if needed.
if len(query.encode("utf-8")) > 30000:
    marker = "## 3. 环境与硬件\n"
    tail_start = query.index(marker)
    head = query[:query.index("## 1. 数据（官方 PyG SuperPixel）")]
    query = head + query[tail_start:]
    query = query.replace(
        "## 3. 环境与硬件\n\n检查 `torch.cuda.is_available()`、GPU 型号、torch/torch_geometric 版本；缺依赖则 pip 安装。\n固定 `torch.manual_seed`、`numpy`、`random`、`torch.use_deterministic_algorithms(True)`；CUDA 稀疏归约非确定，因此每个点 5 个 seed 并报 std/95% CI。\n所有命令在 `project/` 目录执行。\n",
        "## 3. 环境\n检查 CUDA/torch/torch_geometric；缺依赖则 pip 安装。固定 `torch.manual_seed`、numpy、random、`torch.use_deterministic_algorithms(True)`；CUDA 稀疏归约非确定，每点 5 seeds 并报 std/95% CI。所有命令在 `project/` 执行。\n")
out = TP / "novix_query.md"
out.write_text(query, encoding="utf-8")
print("QUERY_WRITTEN", out, out.stat().st_size, "B", "chars", len(query))
