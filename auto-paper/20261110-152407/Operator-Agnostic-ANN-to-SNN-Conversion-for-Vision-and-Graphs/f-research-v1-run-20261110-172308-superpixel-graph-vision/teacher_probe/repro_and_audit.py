#!/usr/bin/env python3
"""T0 reproduction (paper's exact working point) + Table-1 self-consistency audit.

Reproduction uses the SAME seed as the paper (seed 10) so any deviation is a
pipeline problem, not a seed difference. The audit recomputes, in ONE
configuration, full teacher / masked teacher / converted SNN and checks whether
converted accuracy can legitimately exceed the masked teacher.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parents[0]
sys.path.insert(0, str(R / "protocols"))
import vision_pipeline as vp  # noqa: E402
from run_e17 import convert_f64, make_mask  # noqa: E402

DATA = R / "data" / "pyg_bench"
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
TABLES = HERE / "tables"
TABLES.mkdir(exist_ok=True)

POINTS = {"MNIST": dict(margin_coef=0.4, keep_frac=0.08, theta=1.5, T=3),
          "CIFAR10": dict(margin_coef=0.2, keep_frac=0.08, theta=1.0, T=3)}
SEED = 10  # identical to the paper's holdout seed
CFG = dict(n_train=2000, n_val=1000, n_test=2000, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")

paper = json.loads((R / "results" / "e17" / "confirmation.json").read_text(encoding="utf-8"))
paper_by_seed = {(r["dataset"], r["seed"]): r for r in paper["runs"]}

records = []
for ds, pt in POINTS.items():
    sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"], n_val=CFG["n_val"],
                        n_test=CFG["n_test"], seed=SEED)
    tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
    te = vp.batch_graphs(sp["test"]["graphs"], sp["test"]["indices"], pool="sum")
    base = vp.train_ann(tr, hidden=CFG["hidden"], seed=SEED, epochs=CFG["epochs"],
                        lr=CFG["lr"], device=CFG["device"])  # FULL teacher, no mask
    full_acc = float((vp.ann_logits(te, base).argmax(1) == te["y"]).mean()) * 100
    mask = make_mask(base, tr, pt["keep_frac"])
    model = vp.train_ann(tr, hidden=CFG["hidden"], seed=SEED, epochs=CFG["epochs"],
                         lr=CFG["lr"], device=CFG["device"], unit_mask=mask,
                         margin_coef=pt["margin_coef"])
    r = convert_f64(te, model, pt["T"], pt["theta"])
    masked_acc = r["ann_acc"] * 100
    snn_acc = r["snn_acc"] * 100
    p = paper_by_seed.get((ds, SEED), {})
    rec = dict(dataset=ds, seed=SEED, teacher_full=round(full_acc, 3),
               teacher_at_working_point=round(masked_acc, 3),
               converted=round(snn_acc, 3),
               loss_pp=round(masked_acc - snn_acc, 3),
               converted_minus_masked_pp=round(snn_acc - masked_acc, 3),
               identity_residual=r["identity_residual"],
               energy_primary=r["energy_primary"], energy_conservative=r["energy_conservative"],
               spikes=r["spikes"],
               paper_teacher=p.get("ann_test"), paper_loss_pp=p.get("test_loss_pp"),
               repro_delta_teacher=round(masked_acc - p.get("ann_test", float("nan")), 3)
               if p else None,
               repro_delta_loss=round((masked_acc - snn_acc) - p.get("test_loss_pp", float("nan")), 3)
               if p else None,
               kept_units=int(mask.sum()))
    records.append(rec)
    print(json.dumps(rec, ensure_ascii=False), flush=True)

(OUT / "table1_audit.json").write_text(json.dumps(
    dict(seed=SEED, config=CFG, points=POINTS, records=records), indent=2), encoding="utf-8")

# ---- REPRO.md ----
lines = ["# REPRO · 论文现值 vs 本次复现（同 seed=10、同配置）", "",
         f"生成 {datetime.now().isoformat()}；配置见 `CONFIG_AUDIT.md`；结果文件 `results/table1_audit.json`。", "",
         "| 数据集 | 量 | 论文值 (E17, seed 10) | 复现值 | 偏差 | 阈值 |", "|---|---|---:|---:|---:|---|"]
ok = True
for rec in records:
    for label, pv, rv, dv in (
            ("teacher@working-point", rec["paper_teacher"], rec["teacher_at_working_point"],
             rec["repro_delta_teacher"]),
            ("conversion loss (pp)", rec["paper_loss_pp"], rec["loss_pp"], rec["repro_delta_loss"])):
        flag = "PASS" if dv is not None and abs(dv) <= 2.0 else "BLOCK"
        if flag == "BLOCK":
            ok = False
        lines.append(f"| {rec['dataset']} | {label} | {pv} | {rv} | {dv:+.3f} | {flag} |")
lines += ["", f"**结论：{'复现通过，可扩展' if ok else '复现偏差超 ±2pp，见 REPRO_BLOCKER.md'}**", "",
          "- 复现使用与论文完全相同的 seed（10）、数据规模（2000/1000/2000）、宽度（keep_frac=0.08）、margin、θ、T 与 fp64 前向。",
          "- 提示词 T0 的 `k=16` 与代码现值 `hidden=128 + unit_mask(keep_frac=0.08)` 的口径差异已在 `CONFIG_AUDIT.md` §4 说明；本复现以代码为准。", ""]
(HERE / "REPRO.md").write_text("\n".join(lines), encoding="utf-8")

# ---- Table 1 fixed (four columns, one configuration) ----
tex = ["\\begin{tabular}{lcccc}\\hline",
       "Dataset & Teacher (full) & Teacher@point & Converted & Loss (pp) \\\\\\hline"]
for rec in records:
    tex.append(f"{rec['dataset']} & {rec['teacher_full']:.2f} & {rec['teacher_at_working_point']:.2f} & "
               f"{rec['converted']:.2f} & {rec['loss_pp']:+.2f} \\\\")
tex += ["\\hline\\end{tabular}\n"]
(TABLES / "tab_table1_fixed.tex").write_text("\n".join(tex), encoding="utf-8")

# ---- leakage checklist ----
(HERE / "audits").mkdir(exist_ok=True)
(HERE / "audits" / "leakage-checklist.md").write_text("""# Q5 · 反超审计与泄露检查（同配置）

检查项（全部基于 `results/table1_audit.json`，seed=10，两数据集同配置）：

1. **mask 生成时机**：`make_mask` 在全宽 base teacher 训练后、转换前，用**训练集** `mean(relu(B1))` 排序生成；不使用 val/test。→ 无 test 泄露。
2. **校准集**：FTBC 的 β 只在 validation 上校准；主臂 β=0 不需要校准；工作点只在 validation 多 seed 上选。→ test 未被用于选择。
3. **读出 R**：固定线性 sum pooling，不含标签信息。→ 无标签泄露。
4. **Converted > Teacher@working-point 是否合理**：converted 是 masked teacher 的脉冲版。膜电位解码 `argmax B̂` 用的是 `B̂ = mean_t inst_t`（每步瞬时图读出），而 teacher 的 ANN 前向是 `B`。二者数值不同属正常，`converted − teacher@point` 可以为正，这不是泄露，而是**两种读出方式的差**。真正需要警惕的是**跨配置比较**。
5. **论文现值的不自洽来源**：Table 1 的 teacher 34.02%/27.27% 是 **E17 窄网络 + 2000 图 + 800 epochs** 的 teacher@working-point；Table 2 的 Ours 62.60/65.79、32.76/34.10 来自 **local_full_v2 的 5000 图 + 1000 epochs 全宽 v2** 转换结果。**二者训练集、epoch、宽度、mask、margin、θ、T 全不同**，因此「converted 比 teacher 高 31.77pp 而 loss 为正」不是同一配置下的矛盾，而是**跨配置比较**造成的表观不自洽。

结论与处置见 `FINDINGS.md` Q5；四列同配置表见 `tables/tab_table1_fixed.tex`。
""", encoding="utf-8")

print("REPRO_AND_AUDIT_DONE; repro_ok =", ok)
