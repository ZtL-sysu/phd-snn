#!/usr/bin/env python3
"""Compact self-contained novix query v2 (with result.json + path sync)."""
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
    "teacher_probe/summarize.py",
    "teacher_probe/run_all.sh",
]
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in FILES:
        p = R / f
        assert p.is_file(), p
        z.write(p, f)
payload = base64.b64encode(buf.getvalue()).decode()
print("payload bytes", len(buf.getvalue()), "b64", len(payload))

query = f"""# Novix 全量实验：teacher_probe A/B/C/D（v2）

4090 沙箱中执行一次可复现全量实验。所有数值必须由真实运行产生，**严禁编造、估算、插值或引用文献数值冒充实验结果**。

## 0 输出契约（最高优先级）
唯一可 pull 目录是 `/mnt/novix-k8s-workspace-root/session_<id>/workspace`。若 cwd 是 `/home/novix/workspace`，`summarize.py` 会自动把整个 `project/` 同步过去，**必须执行它并确认同步成功**。
顶层必须有 `project/result.json`（逐 seed 记录、mean±std/95%CI、config_hash、异常、交付清单）、`project/README.md`、`project/logs/run.log`。每个 seed 完成即追加写 CSV；时间将尽先落盘脚本与阶段结果。

## 1 数据
下载到 `project/data/pyg_bench/<NAME>/raw/` 并校验字节数：
MNIST https://data.pyg.org/datasets/benchmarking-gnns/MNIST_v2.zip (192378381 B)；
CIFAR10 https://data.pyg.org/datasets/benchmarking-gnns/CIFAR10_v2.zip (316368127 B)。
用 `torch_geometric.datasets.GNNBenchmarkDataset(root=..., name=..., split=...)` 加载。

## 2 还原代码
把 §8 base64 写 `/tmp/p.b64`，执行 `base64 -d /tmp/p.b64 > /tmp/p.zip && unzip -o /tmp/p.zip -d project/`。
得到 `protocols/` 与 `teacher_probe/`。**不要改脚本里的实验配置**；唯一配置来源是 `teacher_probe/config.json`（`run_all.py` 生成，含 config_hash）。

## 3 环境
检查 CUDA/torch/torch_geometric；缺依赖则 pip 安装。固定 `torch.manual_seed`、numpy、random、`torch.use_deterministic_algorithms(True)`。CUDA 稀疏归约非确定 → 每点 5 seeds(0-4) 并报 std/95%CI。

## 4 执行（cwd = 含 project/ 的工作区根）
```
python -m py_compile project/protocols/vision_pipeline.py project/protocols/run_e17.py project/teacher_probe/run_all.py project/teacher_probe/run_bcd.py project/teacher_probe/summarize.py
python -W ignore -u project/teacher_probe/run_all.py
python -W ignore -u project/teacher_probe/run_bcd.py
python -W ignore -u project/teacher_probe/summarize.py
find /mnt/novix-k8s-workspace-root/session_*/workspace/project -maxdepth 2 -type f | sort
```
`run_all.py` 支持 `--exps/--datasets/--seeds` 分片且幂等（已有 `config_hash+seed` 跳过），可断点续跑。

## 5 硬约束
1. 先复现后扩展：本机复现偏差 >±2pp，来源已定位为「E17 未冻结 base teacher 权重与 unit_mask，mask 由 base 训练集激活决定，CUDA 非确定使 mask 不同」，**不是数据/split/标签泄露**。所有新实验把 base 权重与 mask 落盘 `snapshots/`；不得改数据管道凑数。
2. 只在 validation 选 (k,θ,T)；test 只报一次。
3. 报全部 5 seeds，不报 best/max。
4. `conversion loss := teacher@k − converted@k`，必须同配置（同 k/宽度/训练集/A/R）；`run_bcd.width_model` 已保证。
5. OOM/NaN 记 `RUNLOG.md` 并降 batch 重跑；不换 seed、不删点、不降 train 规模。
6. 恒等式用同一 float64 forward（`convert_f64`）报 `max|B̂−B−RA(E1W2)|`（预期 ~1e-14）及 fp32/fp64 差。
7. 两套能耗口径都报（45nm MAC 4.6pJ/AC 0.9pJ）；标注 `teacher>2×chance`(20%) 可采用；零脉冲不算优势。
8. `FINDINGS.md` 回答 Q1–Q5，每条 ≤5 句且带数字和 CI。

## 6 交付（全在 `project/teacher_probe/`）
`results/teacher_probe.csv`、`results/strong_teacher_conversion.csv`、`results/energy.csv`、`results/fidelity_width.csv`、`tables/*.tex`(4)、`figures/fig_fidelity_width.pdf`、`figures/fig_frontier_strong.pdf`、`FINDINGS.md`、`RUNLOG.md`、`run_all.sh`。
另请补写 `CONFIG_AUDIT.md`（从代码提取全部超参：optimizer/lr/batch/H/dropout/特征维/mask/θ/T/能耗常数）、`REPRO.md`（论文现值 vs 本次复现 vs 偏差）、`REPRO_BLOCKER.md`（复现偏差 >±2pp 的来源说明，按上面第 1 条）。本机已有同内容文档，按要点补齐即可。

## 7 预算与终止
单 run ≤10min；某配置 >30min 停下记 `RUNLOG.md` 并报告，不要硬跑。终止条件：T5 teacher 反而低于 T0（数据管道问题）、或反超审计发现泄露 → 立即停并优先报告。

## 8 代码载荷（base64 zip）

```
{payload}
```

完成后在 finalReply 报告：`project/result.json` 路径与 SHA-256、交付清单、Q1–Q5 各一句话结论。
"""
out = TP / "novix_query_v2.md"
out.write_text(query, encoding="utf-8")
print("QUERY_V2", out, out.stat().st_size, "B", "chars", len(query))
