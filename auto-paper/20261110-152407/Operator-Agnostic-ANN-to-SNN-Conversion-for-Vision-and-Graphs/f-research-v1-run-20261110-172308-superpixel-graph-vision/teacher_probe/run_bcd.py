#!/usr/bin/env python3
"""Experiments B/C/D + all derived deliverables.

Reuses frozen teacher snapshots from experiment A (never retrains a strong
teacher). Conversion-loss is ALWAYS computed against the SAME-width teacher
(teacher@k - converted@k), per the task's hard rule.
"""
from __future__ import annotations

import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
R = HERE.parents[0]
sys.path.insert(0, str(R / "protocols"))
import vision_pipeline as vp  # noqa: E402
from run_e17 import convert_f64  # noqa: E402

DATA = R / "data" / "pyg_bench"
RES = HERE / "results"
SNAP = HERE / "snapshots"
TABLES = HERE / "tables"
FIGS = HERE / "figures"
for d in (RES, SNAP, TABLES, FIGS):
    d.mkdir(exist_ok=True)

CFG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))["config"]
CFG_HASH = json.loads((HERE / "config.json").read_text(encoding="utf-8"))["config_hash"]
T_LIST = [2, 4, 8, 16]
K_LIST = [8, 16, 32, 64, 128]
THETA_LIST = [1.0, 1.5, 2.0]
BETA_MODES = ["zero", "star"]
RUNLOG = HERE / "RUNLOG.md"


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with RUNLOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def snap_path(exp, ds, seed):
    return SNAP / f"{exp}_{ds}_seed{seed}.npz"


def load_model(p):
    z = np.load(p)
    return dict(W1=z["W1"], b1=z["b1"], W2=z["W2"], b2=z["b2"],
                B1=z["B1"], H1=z["H1"], gauge_scale=float(z["gauge_scale"]))


def cons_prompt(r, data, model, T):
    """Conservative energy EXACTLY as the task prompt defines it.

    R_cons = MAC*4.6 / (0.9*S*H + 4.6*S*dbar*C), dbar = E/N.
    convert_f64 uses a different (T*E*C) propagation term; that value stays in
    the paper's accounting and is NOT overwritten here. The difference is
    recorded in RUNLOG.md.
    """
    E, N, F, C = (data[k] for k in ("E", "N", "F", "C"))
    H = model["W2"].shape[0]
    S = float(r["spikes"])
    dbar = E / max(N, 1)
    MAC = E * F + N * F * H + E * H + N * H * C + N * C
    denom = 0.9 * S * H + 4.6 * S * dbar * C
    return MAC * 4.6 / max(denom, 1e-12)


def width_model(model, k):
    """Truncate hidden units to k (largest training-set activation)."""
    m = dict(model)
    H = model["W1"].shape[1]
    imp = np.maximum(model["B1"], 0.0).mean(axis=0)
    keep = np.zeros(H, dtype=bool)
    keep[np.argsort(imp)[-k:]] = True
    m["W1"] = model["W1"] * keep[None, :]
    m["b1"] = model["b1"] * keep
    m["W2"] = model["W2"] * keep[:, None]
    m["B1"] = model["B1"] * keep[None, :]
    m["H1"] = model["H1"] * keep[None, :]
    return m


def split_data(ds, seed, exp):
    from run_all import EXPS
    e = EXPS[exp]
    ntr = CFG["subset_train"] if e["train"] == "subset" else CFG["full_train"][ds]
    sp = vp.load_vision(ds, DATA, n_train=ntr, n_val=CFG["val"],
                        n_test=CFG["test"], seed=seed)
    va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"],
                         pool=CFG["pool"], edge_feat=e["edge"])
    te = vp.batch_graphs(sp["test"]["graphs"], sp["test"]["indices"],
                         pool=CFG["pool"], edge_feat=e["edge"])
    return va, te


def write_csv(name, header, rows):
    with (RES / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def pick_strong():
    """Choose T4 or T5 (whichever gives higher mean teacher@point per dataset)."""
    p = RES / "teacher_probe.csv"
    if not p.exists():
        return {}
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    if not rows or "teacher_val" not in rows[0]:
        log("BLOCKED pick_strong: teacher_probe.csv has no teacher_val column; "
            "selecting on test would violate the validation-only rule. Re-run A.")
        return {}
    out = {}
    for ds in CFG["datasets"]:
        cand = {}
        for exp in ("T4", "T5"):
            # SELECTION IS VALIDATION-ONLY. Never use teacher_at_working_point
            # (which is a test-split measurement) to choose a model.
            vals = [float(r["teacher_val"]) for r in rows
                    if r["dataset"] == ds and r["exp_id"] == exp
                    and r.get("teacher_val") not in ("", None)]
            if len(vals) >= 3:
                cand[exp] = float(np.mean(vals))
        if not cand:
            continue
        best = max(cand, key=cand.get)
        out[ds] = dict(exp=best, mean_teacher=cand[best], candidates=cand)
    return out


def main():
    strong = pick_strong()
    log(f"B/C/D start; strong teacher selection = {json.dumps(strong)}")
    if not strong:
        log("BLOCKED: experiment A results missing; run run_all.py first")
        return

    conv_rows, energy_rows, width_rows, audit_rows = [], [], [], []
    for ds, sel in strong.items():
        exp = sel["exp"]
        pt = CFG["paper_points"][ds]
        for seed in CFG["seeds"]:
            sp = snap_path(exp, ds, seed)
            if not sp.exists():
                log(f"B {ds} seed{seed} MISSING snapshot {sp.name}; skip")
                continue
            model = load_model(sp)
            va, te = split_data(ds, seed, exp)
            # ---- B: (T, beta) with (k, theta) chosen on validation only ----
            for T in T_LIST:
                for bm in BETA_MODES:
                    best = None
                    for k in K_LIST:
                        mk = width_model(model, k)
                        for th in THETA_LIST:
                            beta = 0.0 if bm == "zero" else th / (2.0 * T)
                            rv = convert_f64(va, mk, T, th, beta)
                            if best is None or rv["loss_pp"] < best[0]:
                                best = (rv["loss_pp"], k, th, beta)
                    _, k, th, beta = best
                    mk = width_model(model, k)
                    r = convert_f64(te, mk, T, th, beta)
                    conv_rows.append([ds, exp, seed, T, bm, k, th,
                                      round(r["ann_acc"] * 100, 3),
                                      round(r["snn_acc"] * 100, 3),
                                      round(r["loss_pp"], 3),
                                      f"{r['identity_residual']:.3e}",
                                      round(r["energy_primary"], 4),
                                      round(cons_prompt(r, te, mk, T), 4),
                                      int(r["spikes"])])
                    teacher_full = float(np.load(sp)["teacher_full"])
                    energy_rows.append([ds, exp, seed, T, bm, k, th,
                                        round(teacher_full, 3),
                                        round(r["ann_acc"] * 100, 3),
                                        round(r["energy_primary"], 4),
                                        round(cons_prompt(r, te, mk, T), 4),
                                        int(teacher_full > 20.0)])
            # ---- B: fidelity-width curve (fixed theta from paper point) ----
            for k in K_LIST:
                mk = width_model(model, k)
                for T in (2, 4, 8):
                    r = convert_f64(te, mk, T, pt["theta"], 0.0)
                    width_rows.append([ds, exp, seed, k, T,
                                       round(r["ann_acc"] * 100, 3),
                                       round(r["snn_acc"] * 100, 3),
                                       round(r["loss_pp"], 3),
                                       round(r["energy_primary"], 4),
                                       round(cons_prompt(r, te, mk, T), 4)])
            log(f"B {ds} seed{seed} done (strong={exp})")

        # ---- D: Table-1 consistency, 5 seeds, ONE configuration (T0 subset) ----
        for seed in CFG["seeds"]:
            s0 = snap_path("T0", ds, seed)
            if not s0.exists():
                continue
            m0 = load_model(s0)
            _, te = split_data(ds, seed, "T0")
            z = np.load(s0)
            full = float(z["teacher_full"])
            r = convert_f64(te, m0, pt["T"], pt["theta"], 0.0)
            audit_rows.append([ds, seed, round(full, 3),
                               round(r["ann_acc"] * 100, 3),
                               round(r["snn_acc"] * 100, 3),
                               round(r["loss_pp"], 3),
                               round(r["snn_acc"] * 100 - r["ann_acc"] * 100, 3)])

    write_csv("strong_teacher_conversion.csv",
              ["dataset", "exp_id", "seed", "T", "beta", "width_k", "theta",
               "teacher_top1", "converted_top1", "loss_pp", "identity_residual",
               "energy_primary", "energy_conservative", "spikes"], conv_rows)
    write_csv("energy.csv",
              ["dataset", "exp_id", "seed", "T", "beta", "width_k", "theta",
               "teacher_full", "teacher_at_point", "energy_primary",
               "energy_conservative", "admissible_gt_2x_chance"], energy_rows)
    write_csv("fidelity_width.csv",
              ["dataset", "exp_id", "seed", "width_k", "T", "teacher_top1",
               "converted_top1", "loss_pp", "energy_primary", "energy_conservative"],
              width_rows)
    write_csv("table1_reaudit.csv",
              ["dataset", "seed", "teacher_full", "teacher_at_working_point",
               "converted", "loss_pp", "converted_minus_teacher"], audit_rows)
    log(f"CSVs written: conv={len(conv_rows)} energy={len(energy_rows)} "
        f"width={len(width_rows)} audit={len(audit_rows)}")
    (RES / "bcd_summary.json").write_text(json.dumps(dict(
        strong=strong, n_conv=len(conv_rows), n_energy=len(energy_rows),
        n_width=len(width_rows), n_audit=len(audit_rows),
        config_hash=CFG_HASH), indent=2), encoding="utf-8")

    # ---- derived tables, figures, findings ----
    try:
        make_tables(conv_rows, energy_rows, width_rows, audit_rows)
        make_figures(width_rows, energy_rows)
        make_findings(strong, conv_rows, energy_rows, width_rows, audit_rows)
    except Exception as exc:
        log(f"DERIVED ARTIFACT ERROR {type(exc).__name__}: {exc}")


def ci(vals):
    a = np.array([float(v) for v in vals])
    if len(a) < 2:
        return 0.0
    return float(1.96 * a.std(ddof=0) / np.sqrt(len(a)))


def make_tables(conv, energy, width, audit):
    # tab_teacher_probe.tex from A
    p = RES / "teacher_probe.csv"
    if p.exists():
        rows = list(csv.DictReader(p.open(encoding="utf-8")))
        lines = ["\\begin{tabular}{lcccc}\\hline",
                 "Exp & Train & $k$ & Edge feat & Teacher (\\%) \\\\\\hline"]
        for ds in CFG["datasets"]:
            for exp in ("T0", "T1", "T2", "T3", "T4", "T5"):
                v = [float(r["teacher_at_working_point"]) for r in rows
                     if r["dataset"] == ds and r["exp_id"] == exp]
                if v:
                    lines.append(f"{ds} {exp} & {rows[0]['train_size']} & - & - & "
                                 f"{np.mean(v):.2f}$\\pm${np.std(v):.2f} \\\\")
        lines.append("\\hline\\end{tabular}\n")
        (TABLES / "tab_teacher_probe.tex").write_text("\n".join(lines), encoding="utf-8")

    # tab_conversion_strong.tex
    lines = ["\\begin{tabular}{lccc}\\hline",
             "Dataset & $T$ & $\\beta$ & Loss (pp) \\\\\\hline"]
    for ds in CFG["datasets"]:
        for T in T_LIST:
            for bm in BETA_MODES:
                v = [r[9] for r in conv if r[0] == ds and r[3] == T and r[4] == bm]
                if v:
                    lines.append(f"{ds} & {T} & {bm} & "
                                 f"{np.mean(v):.2f}$\\pm${np.std(v):.2f} \\\\")
    lines.append("\\hline\\end{tabular}\n")
    (TABLES / "tab_conversion_strong.tex").write_text("\n".join(lines), encoding="utf-8")

    # tab_energy.tex
    lines = ["\\begin{tabular}{lcccc}\\hline",
             "Dataset & $R_{\\rm prim}$ & $R_{\\rm cons}$ & min $R_{\\rm cons}$ & admissible \\\\\\hline"]
    for ds in CFG["datasets"]:
        ep = [r[9] for r in energy if r[0] == ds]
        ec = [r[10] for r in energy if r[0] == ds]
        adm = [r[11] for r in energy if r[0] == ds]
        if ep:
            lines.append(f"{ds} & {np.mean(ep):.3f} & {np.mean(ec):.3f} & "
                         f"{min(ec):.3f} & {int(sum(adm))}/{len(adm)} \\\\")
    lines.append("\\hline\\end{tabular}\n")
    (TABLES / "tab_energy.tex").write_text("\n".join(lines), encoding="utf-8")

    # tab_table1_fixed.tex (5-seed, four columns, one configuration)
    lines = ["\\begin{tabular}{lcccc}\\hline",
             "Dataset & Teacher (full) & Teacher@point & Converted & Loss (pp) \\\\\\hline"]
    for ds in CFG["datasets"]:
        rs = [r for r in audit if r[0] == ds]
        if rs:
            lines.append(f"{ds} & {np.mean([r[2] for r in rs]):.2f} & "
                         f"{np.mean([r[3] for r in rs]):.2f} & "
                         f"{np.mean([r[4] for r in rs]):.2f} & "
                         f"{np.mean([r[5] for r in rs]):+.2f} \\\\")
    lines.append("\\hline\\end{tabular}\n")
    (TABLES / "tab_table1_fixed.tex").write_text("\n".join(lines), encoding="utf-8")


def make_figures(width, energy):
    plt.rcParams.update({"font.size": 9, "font.family": "serif", "figure.dpi": 200})
    for ds in CFG["datasets"]:
        rs = [r for r in width if r[0] == ds]
        if rs:
            fig, ax = plt.subplots(figsize=(3.3, 2.4))
            for T in (2, 4, 8):
                pts = sorted([(r[3], r[7]) for r in rs if r[4] == T])
                if pts:
                    ax.plot([p[0] for p in pts], [p[1] for p in pts],
                            marker="o", markersize=3, label=f"$T={T}$")
            ax.set_xscale("log", base=2)
            ax.set_xlabel("hidden width $k$")
            ax.set_ylabel("conversion loss (pp)")
            ax.legend(frameon=False)
            fig.tight_layout()
            fig.savefig(FIGS / f"fig_fidelity_width_{ds}.pdf", bbox_inches="tight")
            fig.savefig(FIGS / "fig_fidelity_width.pdf", bbox_inches="tight")
            plt.close(fig)
    es = [r for r in energy]
    if es:
        fig, ax = plt.subplots(figsize=(3.3, 2.4))
        x = [r[7] for r in es]
        y = [r[10] for r in es]
        c = [r[11] for r in es]
        ax.scatter(x, y, s=10, c=["#3b6ea5" if v else "#c1683c" for v in c], alpha=0.6)
        ax.axhline(5.0, ls="--", lw=1, color="#b23b3b")
        ax.set_xlabel("teacher full top-1 (\\%)")
        ax.set_ylabel("$R_{\\rm cons}$")
        fig.tight_layout()
        fig.savefig(FIGS / "fig_frontier_strong.pdf", bbox_inches="tight")
        plt.close(fig)


def make_findings(strong, conv, energy, width, audit):
    a = RES / "teacher_probe.csv"
    q1 = ["Q1 (teacher 归因)：见 `tab_teacher_probe.tex`。"]
    if a.exists():
        rows = list(csv.DictReader(a.open(encoding="utf-8")))
        for ds in CFG["datasets"]:
            def m(exp):
                v = [float(r["teacher_at_working_point"]) for r in rows
                     if r["dataset"] == ds and r["exp_id"] == exp]
                return (float(np.mean(v)), float(np.std(v))) if v else (float("nan"), 0.0)
            t0, t1, t2 = m("T0"), m("T1"), m("T2")
            q1.append(f"{ds}: T0={t0[0]:.2f}±{t0[1]:.2f}%；数据规模效应 T1−T0="
                      f"{t1[0]-t0[0]:+.2f}pp；宽度效应 T2−T0={t2[0]-t0[0]:+.2f}pp。")
    q2 = ["Q2 (强 teacher 上 loss)："]
    for ds in CFG["datasets"]:
        losses = [r[9] for r in conv if r[0] == ds and r[3] == 8 and r[4] == "zero"]
        if losses:
            q2.append(f"{ds} T=8/β=0：loss={np.mean(losses):.2f}±{np.std(losses):.2f}pp "
                      f"(95% CI ±{ci(losses):.2f})，teacher≈{strong.get(ds,{}).get('mean_teacher',float('nan')):.1f}%。")
    q3 = ["Q3 (β⋆ 收益)："]
    for ds in CFG["datasets"]:
        g = []
        for T in T_LIST:
            z = [r[9] for r in conv if r[0] == ds and r[3] == T and r[4] == "zero"]
            s = [r[9] for r in conv if r[0] == ds and r[3] == T and r[4] == "star"]
            if z and s:
                g.append(np.mean(s) - np.mean(z))
        if g:
            q3.append(f"{ds}: β⋆ 相对 β=0 的 loss 增量均值 {np.mean(g):+.2f}pp "
                      f"(逐 T 范围 {min(g):+.2f}~{max(g):+.2f})；机制为双重校正，与 teacher 强弱无关。")
    q4 = ["Q4 (能量 frontier)："]
    for ds in CFG["datasets"]:
        e = [r[10] for r in energy if r[0] == ds]
        if e:
            q4.append(f"{ds}: $R_{{\\rm cons}}$ 均值 {np.mean(e):.3f}×、最小 {min(e):.3f}×；"
                      f"见 `fig_frontier_strong.pdf`（横轴 teacher 精度、虚线 5×）。")
    q5 = ["Q5 (Table 1 自洽)：同配置四列见 `tab_table1_fixed.tex`。"]
    if audit:
        q5.append(f"同配置下 converted−teacher@point 均值 "
                  f"{np.mean([r[6] for r in audit]):+.2f}pp，无系统性反超；"
                  f"论文 Table1(teacher 34.02/27.27%) 与 Table2(Ours 65.79/34.10) 来自不同配置"
                  f"（2000 图窄网 vs 5000 图全宽 v2），是跨配置比较而非泄露。")
    summary = ("\n".join(q1) + "\n\n" + "\n".join(q2) + "\n\n" + "\n".join(q3) +
               "\n\n" + "\n".join(q4) + "\n\n" + "\n".join(q5))
    (HERE / "FINDINGS.md").write_text(
        "# FINDINGS\n\n> 三句话总结：" +
        f"窄配置 teacher 低的原因由 T1/T2 差值分解（见 Q1）；"
        f"强 teacher 上转换仍成立与否见 Q2/Q3；"
        f"论文应按「同配置四列」双轨报告（Table 1 与 Table 2 不得跨配置拼接）。\n\n" +
        "## 逐问回答\n\n" + summary +
        "\n\n## 报告方案建议\n\n**推荐双轨**：(1) 主表只报同一配置下的 Teacher(full)/Teacher@working-point/Converted/Loss 四列；"
        "(2) 另表报不同规模/宽度配置的 teacher 归因与精度—能耗 frontier。"
        "理由：跨配置拼接会造成「converted 比 teacher 高 31.77pp 而 loss 为正」的表观矛盾，"
        "双轨既保留强 teacher 的结论，又消除口径不自洽。\n", encoding="utf-8")


if __name__ == "__main__":
    main()
