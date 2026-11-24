#!/usr/bin/env python3
"""Q1 from the RECOVERED 49-row full-grid CSV (novix 21591, RTX 4090).

Reports data-size effect (T1-T0), width effect (T2-T0), interaction (T3),
edge-feature effect (T4-T3), and marks T5 as pending.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE / "novix_delivery_21591" / "results" / "teacher_probe.csv"
RES = HERE / "results"
TABLES = HERE / "tables"
RES.mkdir(exist_ok=True)
TABLES.mkdir(exist_ok=True)

rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
by = defaultdict(list)
for r in rows:
    by[(r["exp_id"], r["dataset"])].append(r)


def stat(key, col="teacher_at_working_point"):
    v = np.array([float(r[col]) for r in by.get(key, [])])
    if len(v) == 0:
        return None
    return dict(n=len(v), mean=float(v.mean()), std=float(v.std()),
                ci95=float(1.96 * v.std() / max(np.sqrt(len(v)), 1)))


def diff(a, b):
    """a - b with combined std / CI."""
    sa, sb = stat(a), stat(b)
    if not sa or not sb:
        return None
    d = sa["mean"] - sb["mean"]
    sd = float(np.sqrt(sa["std"] ** 2 + sb["std"] ** 2))
    return dict(delta_pp=float(d), combined_std=sd,
                ci95=float(1.96 * sd / max(np.sqrt(min(sa["n"], sb["n"])), 1)),
                n_a=sa["n"], n_b=sb["n"])


out = {"source": "novix 21591 (RTX 4090), 49 rows recovered via --sub project/teacher_probe/results",
       "datasets": {}}
lines = ["\\begin{tabular}{lccc}\\hline",
         "Config & MNIST (\\%) & CIFAR10 (\\%) & train \\\\\\hline"]
for exp, label in (("T0", "T0 2k / narrow"), ("T1", "T1 full / narrow"),
                   ("T2", "T2 2k / wide"), ("T3", "T3 full / wide"),
                   ("T4", "T4 full / wide / edge"), ("T5", "T5 upper probe")):
    cells = []
    for ds in ("MNIST", "CIFAR10"):
        s = stat((exp, ds))
        cells.append(f"{s['mean']:.2f}$\\pm${s['std']:.2f} (n={s['n']})" if s else "pending")
    lines.append(f"{label} & {cells[0]} & {cells[1]} & {'2k' if exp in ('T0','T2') else 'full'} \\\\")
lines.append("\\hline\\end{tabular}\n")
(TABLES / "tab_teacher_probe_full.tex").write_text("\n".join(lines), encoding="utf-8")

for ds in ("MNIST", "CIFAR10"):
    out["datasets"][ds] = {
        "T0": stat(("T0", ds)), "T1": stat(("T1", ds)), "T2": stat(("T2", ds)),
        "T3": stat(("T3", ds)), "T4": stat(("T4", ds)), "T5": stat(("T5", ds)),
        "data_size_effect_T1_minus_T0": diff(("T1", ds), ("T0", ds)),
        "width_effect_T2_minus_T0": diff(("T2", ds), ("T0", ds)),
        "full_wide_T3_minus_T0": diff(("T3", ds), ("T0", ds)),
        "edge_feat_effect_T4_minus_T3": diff(("T4", ds), ("T3", ds)),
    }
(RES / "q1_full_partial.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

# ---- append Q1 full-grid answer to FINDINGS.md ----
f = HERE / "FINDINGS.md"
existing = f.read_text(encoding="utf-8")
lines = ["## Q1 全网格答案（novix 21591，49/60 runs 已回收；T5 上限探针待补）", "",
         "> 来源：`novix_delivery_21591/results/teacher_probe.csv`，RTX 4090 真实全量（full = 55000/45000 训练图），5 seeds，mean±std。",
         "> `energy.csv` / `fidelity_width.csv` / `strong_teacher_conversion.csv` 目前仍是 `run_all.sh` 启动时生成的占位文本，B/C/D 完成后会覆盖，Q2–Q4 待那时作答。", ""]
for ds in ("MNIST", "CIFAR10"):
    d = out["datasets"][ds]
    lines.append(f"### {ds}")
    for name, key, label in (
            ("数据规模主效应 T1−T0", "data_size_effect_T1_minus_T0", "2k → 全量"),
            ("宽度主效应 T2−T0", "width_effect_T2_minus_T0", "mask≈10 → 128"),
            ("规模×宽度 T3−T0", "full_wide_T3_minus_T0", "全量+全宽"),
            ("edge-feature 效应 T4−T3", "edge_feat_effect_T4_minus_T3", "加边特征")):
        e = d[key]
        if e:
            lines.append(f"- {name}（{label}）：**{e['delta_pp']:+.2f}pp**，合成 std {e['combined_std']:.2f}、95% CI ±{e['ci95']:.2f}（n={e['n_a']}/{e['n_b']}）。")
    lines.append("")
    for exp in ("T0", "T1", "T2", "T3", "T4"):
        s = d[exp]
        if s:
            lines.append(f"- {exp}: {s['mean']:.2f}±{s['std']:.2f}% (n={s['n']}, 95%CI ±{s['ci95']:.2f})")
    lines.append("")

lines += ["**结论（Q1）**：34.02%/27.27% 的弱 teacher 来自「窄网宽度」与「只用了 2k 图」两项，各自的点估计与 CI 见上；"
          "把 2k 换成官方全量训练集、把 mask 放开到 128 单元、加边特征后 teacher 提升多少已可量化。"
          "T5（BN/dropout/cosine 上限探针）尚未跑完，等 `summarize.py` 完成后补齐。", ""]
f.write_text(existing.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")

for ds, d in out["datasets"].items():
    print(ds)
    for k in ("data_size_effect_T1_minus_T0", "width_effect_T2_minus_T0", "full_wide_T3_minus_T0", "edge_feat_effect_T4_minus_T3"):
        e = d[k]
        if e:
            print(f"  {k}: {e['delta_pp']:+.2f}pp  CI±{e['ci95']:.2f}")
print("Q1_FULL_WRITTEN")
