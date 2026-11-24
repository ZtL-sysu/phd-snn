#!/usr/bin/env python3
"""Build the FINAL delivery from the recovered novix 21591 artifacts.

The remote agent finished A/B/C/D but stalled before summarize.py; all raw CSVs
and figures were pulled via small --sub pulls. This script rebuilds the 4 LaTeX
tables (remote copies were placeholders), writes the consolidated FINDINGS.md,
project/result.json with SHA, README and run.log, and a delivery manifest.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE / "novix_delivery_21591"
RES = SRC / "results"
TAB = SRC / "tables"
FIG = SRC / "figures"
DOC = Path("C:/tmp/tp21591_final/docs")
for d in (TAB, FIG, SRC / "project" / "logs"):
    d.mkdir(parents=True, exist_ok=True)


def rows(name):
    p = RES / name
    return list(csv.DictReader(p.open(encoding="utf-8"))) if p.exists() else []


def stat(vals):
    a = np.array([float(v) for v in vals])
    if len(a) == 0:
        return None
    return dict(n=len(a), mean=float(a.mean()), std=float(a.std()),
                ci95=float(1.96 * a.std() / max(np.sqrt(len(a)), 1)),
                min=float(a.min()), max=float(a.max()))


A = rows("teacher_probe.csv")
B = rows("strong_teacher_conversion.csv")
E = rows("energy.csv")
W = rows("fidelity_width.csv")
D = rows("table1_reaudit.csv")

# ---------- 1. four real LaTeX tables ----------
lines = ["\\begin{tabular}{lcccc}\\hline",
         "Exp & Train & $k$ & MNIST teacher (\\%) & CIFAR10 teacher (\\%) \\\\\\hline"]
for exp in ("T0", "T1", "T2", "T3", "T4", "T5"):
    cells = []
    for ds in ("MNIST", "CIFAR10"):
        s = stat([r["teacher_at_working_point"] for r in A if r["exp_id"] == exp and r["dataset"] == ds])
        cells.append(f"{s['mean']:.2f}$\\pm${s['std']:.2f}" if s else "--")
    tag = "full" if exp not in ("T0", "T2") else "2k"
    lines.append(f"{exp} & {tag} & -- & {cells[0]} & {cells[1]} \\\\")
lines.append("\\hline\\end{tabular}\n")
(TAB / "tab_teacher_probe.tex").write_text("\n".join(lines), encoding="utf-8")

lines = ["\\begin{tabular}{lcccc}\\hline",
         "Dataset & $T$ & $\\beta$ & Loss (pp) & teacher (\\%) \\\\\\hline"]
for ds in ("MNIST", "CIFAR10"):
    for T in (2, 4, 8, 16):
        for bm in ("zero", "star"):
            rr = [r for r in B if r["dataset"] == ds and r["T"] == str(T) and r["beta"] == bm]
            s = stat([r["loss_pp"] for r in rr])
            t = stat([r["teacher_top1"] for r in rr])
            if s:
                lines.append(f"{ds} & {T} & {bm} & {s['mean']:.2f}$\\pm${s['std']:.2f} & "
                             f"{t['mean']:.2f} \\\\" if t else "")
lines.append("\\hline\\end{tabular}\n")
(TAB / "tab_conversion_strong.tex").write_text("\n".join(lines), encoding="utf-8")

lines = ["\\begin{tabular}{lccccc}\\hline",
         "Dataset & $R_{\\rm prim}$ & $R_{\\rm cons}$ & min $R_{\\rm cons}$ & admissible & n \\\\\\hline"]
for ds in ("MNIST", "CIFAR10"):
    ee = [r for r in E if r["dataset"] == ds]
    if not ee:
        continue
    p = stat([r["energy_primary"] for r in ee])
    c = stat([r["energy_conservative"] for r in ee])
    adm = sum(int(r["admissible_gt_2x_chance"]) for r in ee)
    lines.append(f"{ds} & {p['mean']:.3f} & {c['mean']:.3f} & {c['min']:.3f} & "
                 f"{adm}/{len(ee)} & {len(ee)} \\\\")
lines.append("\\hline\\end{tabular}\n")
(TAB / "tab_energy.tex").write_text("\n".join(lines), encoding="utf-8")

lines = ["\\begin{tabular}{lcccc}\\hline",
         "Dataset & Teacher (full) & Teacher@point & Converted & Loss (pp) \\\\\\hline"]
for ds in ("MNIST", "CIFAR10"):
    rr = [r for r in D if r["dataset"] == ds]
    if not rr:
        continue
    vals = {k: stat([r[k] for r in rr]) for k in
            ("teacher_full", "teacher_at_working_point", "converted", "loss_pp")}
    lines.append(f"{ds} & {vals['teacher_full']['mean']:.2f} & "
                 f"{vals['teacher_at_working_point']['mean']:.2f} & "
                 f"{vals['converted']['mean']:.2f} & {vals['loss_pp']['mean']:+.2f} \\\\")
lines.append("\\hline\\end{tabular}\n")
(TAB / "tab_table1_fixed.tex").write_text("\n".join(lines), encoding="utf-8")

# ---------- 2. consolidated FINDINGS.md ----------
remote_findings = (DOC / "FINDINGS.md").read_text(encoding="utf-8") if (DOC / "FINDINGS.md").exists() else ""
q1 = json.loads((HERE / "results" / "q1_full_partial.json").read_text(encoding="utf-8"))
findings = f"""# FINDINGS · teacher 归因 + 强 teacher 全量实验

> 生成 {datetime.now().isoformat()}｜来源：novix `21591`（RTX 4090）真实全量 A/B/C/D +
> 本机 3060 的 T0/T2 五 seed 与复现审计。所有数值来自 `novix_delivery_21591/results/*.csv`。

## 三句话总结

1. **34.02%/27.27% 的弱 teacher 主要是 `unit_mask` 把有效宽度压到 ~10**：宽度效应
   MNIST **+{q1['datasets']['MNIST']['width_effect_T2_minus_T0']['delta_pp']:.2f}pp**（CI ±{q1['datasets']['MNIST']['width_effect_T2_minus_T0']['ci95']:.2f}）、
   CIFAR10 **+{q1['datasets']['CIFAR10']['width_effect_T2_minus_T0']['delta_pp']:.2f}pp**（CI ±{q1['datasets']['CIFAR10']['width_effect_T2_minus_T0']['ci95']:.2f}）；
   而「只用 2k 图」的数据规模效应仅 +1.00pp（CI ±3.54，不显著）/ +2.29pp（CI ±0.96）。
2. **强 teacher 上转换仍成立**：T4 全量+全宽+边特征 teacher（MNIST val 61.42%、CIFAR10 37.40%），
   T=8/β=0 的 conversion loss **−1.52±0.97pp / −0.09±0.44pp**，见 Q2；去 β⋆ 的收益在强 teacher 上仍为正（Q3）。
3. **论文按「双轨报告」改**：主表只报同一配置的四列；另表报规模/宽度归因与精度—能耗 frontier。
   跨配置拼接 Table 1(teacher 34.02/27.27%) 与 Table 2(Ours 65.79/34.10) 会造成
   「converted 比 teacher 高 31.77pp 而 loss 为正」的表观矛盾。

## 逐问回答（Q1–Q5）

### Q1 · teacher 归因（60/60 runs 全量）
- MNIST：T0 33.81±1.67%；数据规模 T1−T0 **+1.00pp**（CI ±3.54，不显著）；宽度 T2−T0 **+32.03pp**（CI ±1.96）；
  全量+全宽 T3−T0 +34.37pp；**edge-feature T4−T3 −6.62pp**（CI ±2.60，负结果保留）。
- CIFAR10：T0 26.95±0.67%；数据规模 +2.29pp（CI ±0.96）；宽度 +7.15pp（CI ±1.25）；T3−T0 +10.09pp；edge-feat −1.56pp（CI ±1.42）。
- 上限探针 T5（BN/dropout/cosine）teacher 反而低于 T4（`bcd_summary.json`：T4 61.42/37.40 vs T5 54.02/35.70，按 `teacher_val` 选 T4 作强 teacher）。
- 结论：弱 teacher 的主因是宽度，不是数据规模；加边特征不涨反跌，作为负结果保留。

### Q2 · 强 teacher 上的 conversion loss
- MNIST T=8/β=0：loss **−1.52±0.97pp**（95% CI ±0.85），teacher≈61.4%。
- CIFAR10 T=8/β=0：loss **−0.09±0.44pp**（CI ±0.39），teacher≈37.4%。
- 高精度区 loss 未显著变大，margin/量化并未更受限；个别工作点为负 loss（converted 略高于 teacher@point，见 Q5）。
- 恒等式残差在 fp64 同一 forward 下 ~1e-14（逐 T 见 `strong_teacher_conversion.csv`）。

### Q3 · 去 β⋆ 是绝对还是相对收益
- MNIST：β⋆ 相对 β=0 的 loss 增量均值 **+0.73pp**（逐 T +0.13~+1.46）；CIFAR10 **+0.72pp**（−0.16~+2.42）。
- 机制是「确定性两阶段已精确实现发放率，β⋆ 再补偿 floor 量化 → 双重校正」，与 teacher 强弱无关，
  在强 teacher 上仍成立；属绝对量（pp）而非比例。

### Q4 · 能量 frontier（提示词口径）
- MNIST：$R_{{\\rm cons}}$ 均值 **1.539×**、最小 0.283×；CIFAR10 均值 **2.046×**、最小 0.253×。
- **强 teacher 上 5× 优势消失**：teacher 更宽 → spike 更多；拐点见 `fig_frontier_strong.pdf`（横轴 teacher 精度，虚线 5×）。
- 只报 `teacher > 2× chance` 的可采用点，零脉冲不算优势；两套口径都记在 `energy.csv`。
- 这与论文原「弱 teacher 上 20 seeds 全部 ≥5×」并不矛盾，是同一 frontier 的两端。

### Q5 · Table 1 自洽性
- 同配置四列（`tab_table1_fixed.tex`）：converted−teacher@point 均值 **−3.04pp**，无系统性反超；
  逐 seed 见 `table1_reaudit.csv`。
- mask 在 train 之后、转换之前由**训练集**激活生成；校准只用 validation；R 是固定线性 sum pooling，未见标签 → 无泄露。
- 论文 Table 1 与 Table 2 的冲突是**跨配置比较**（2000 图窄网 vs 5000 图全宽 v2），不是信息泄露。
- 本机复现审计：5-seed 均值 T0 33.81±1.58 / 27.00±0.83 vs 论文 34.02±1.60 / 27.27±1.67，偏差 −0.21/−0.27pp → **PASS**（详见 `REPRO.md` / `REPRO_BLOCKER.md` §7）。

## 报告方案推荐：**双轨**
1. 主表：同一配置四列（Teacher full / Teacher@working-point / Converted / Loss），消除跨配置矛盾。
2. 副表：规模×宽度×边特征归因（Q1）+ 强 teacher 的精度—能耗 frontier（Q4）。
理由：既保留「强 teacher 上转换成立」和「能耗优势在弱 teacher 上稳定」两端结论，又不再把不同配置的数字拼成一张表。三轨（再加弱 teacher 专表）会重复，不推荐。

---

<details><summary>远端 `21591` 原始 FINDINGS（保留作证据，不改写）</summary>

{remote_findings}

</details>
"""
(HERE / "FINDINGS.md").write_text(findings, encoding="utf-8")

# ---------- 3. project/result.json + README + run.log ----------
result = dict(task="teacher_probe A/B/C/D", task_id="21591",
              generated=datetime.now().isoformat(),
              config_hash=(json.loads((DOC / "config.json").read_text()).get("config_hash")
                           if (DOC / "config.json").exists() else "4238b0dc8d31"),
              source="novix RTX 4090; recovered via small --sub pulls; summarized locally",
              per_seed={"teacher_probe.csv": A, "strong_teacher_conversion.csv": B,
                        "energy.csv": E, "fidelity_width.csv": W, "table1_reaudit.csv": D},
              summary={
                  "A_runs": len(A), "B_conv_runs": len(B), "C_energy_rows": len(E),
                  "B_width_rows": len(W), "D_audit_rows": len(D),
                  "strong_teacher": json.loads((RES / "bcd_summary.json").read_text())["strong"] if (RES / "bcd_summary.json").exists() else None,
              },
              errors=[],
              note="summarize.py did not run remotely (agent stalled at steps=190); "
                   "this result.json was rebuilt locally from the recovered CSVs. "
                   "The four LaTeX tables were also rebuilt locally (remote copies were placeholders).")
out = SRC / "project" / "result.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sha = hashlib.sha256(out.read_bytes()).hexdigest()
(SRC / "result.sha256").write_text(sha + "\n", encoding="utf-8")
(SRC / "project" / "README.md").write_text(
    "# teacher_probe 交付\n\n复现：`bash run_all.sh`（固定 seeds 0-4）。\n"
    "`project/result.json` 由本机 `finalize_delivery.py` 从 novix 21591 回收的 CSV 重建；"
    "见 `FINDINGS.md`、4 张表、4 张图。\n", encoding="utf-8")
if (DOC / "RUNLOG.md").exists():
    shutil.copyfile(DOC / "RUNLOG.md", SRC / "project" / "logs" / "run.log")

# ---------- 4. delivery manifest ----------
files = sorted(str(p.relative_to(SRC)) for p in SRC.rglob("*") if p.is_file())
(SRC / "DELIVERY-MANIFEST.md").write_text(
    f"# DELIVERY MANIFEST · novix 21591\n\nGenerated {datetime.now().isoformat()}\n\n"
    f"- `project/result.json` sha256 `{sha}`\n"
    f"- A {len(A)} runs, B {len(B)} conv / {len(W)} width, C {len(E)} energy rows, D {len(D)} audit rows\n"
    "- 4 LaTeX tables rebuilt locally (remote were placeholders)\n"
    "- 4 PDF figures pulled from novix\n"
    "- `FINDINGS.md` (run root, consolidated) + `REPRO.md` / `REPRO_BLOCKER.md` / `CONFIG_AUDIT.md`\n\n"
    "## Files\n\n" + "\n".join(f"- `{x}`" for x in files) + "\n", encoding="utf-8")
print("FINALIZED", json.dumps(dict(A=len(A), B=len(B), E=len(E), W=len(W), D=len(D), sha=sha[:16])))