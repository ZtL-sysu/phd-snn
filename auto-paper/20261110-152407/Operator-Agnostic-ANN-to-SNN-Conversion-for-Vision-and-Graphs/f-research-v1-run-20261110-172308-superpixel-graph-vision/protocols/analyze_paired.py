#!/usr/bin/env python3
"""Paired strong-result audit: local_full (beta*) vs local_full_v2 (beta removed).

Computes 5-seed conversion loss, paired differences with 95% CI, baseline
margins, energy ratios, and the frozen expected_strong verdict.
All numbers come from the two real result.json files; nothing is hand-entered.
"""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parents[1]
V1 = R / "results" / "local_full" / "result.json"
V2 = R / "results" / "local_full_v2" / "result.json"
OUT = R / "results" / "paired_analysis.json"
REPORT = R / "audits" / "paired-strong-result-audit.md"
TS = (1, 2, 4, 8, 16)
BASELINES = ("naive", "qcfs", "ftbc", "tpp", "parallel")


def load(p):
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def ci95(a):
    a = np.asarray(a, dtype=float)
    if a.size == 0:
        return 0.0
    return float(1.96 * a.std(ddof=0) / math.sqrt(a.size))


def index(d):
    out = {}
    for r in (d or {}).get("runs", []):
        if "ann" not in r or "methods" not in r:
            continue
        out[(r["dataset"], int(r["seed"]))] = r
    return out


def loss(rec, T):
    return (rec["ann"]["test_acc"] - rec["methods"][f"ours_T{T}"]["acc"]) * 100.0


def main():
    d1, d2 = load(V1), load(V2)
    i1, i2 = index(d1), index(d2)
    result = dict(
        generated=datetime.now().isoformat(),
        v1_runs=len(i1), v2_runs=len(i2),
        note="v1 = ours_beta=star (original 1028 combination); "
             "v2 = ours_beta=zero (redundant beta removed). "
             "All values are real local 3060 CUDA runs, NOT the novix 20049 result.",
        datasets={},
    )
    for ds in ("MNIST", "CIFAR10"):
        keys1 = sorted(k for k in i1 if k[0] == ds)
        keys2 = sorted(k for k in i2 if k[0] == ds)
        paired = [k for k in keys2 if k in i1]
        blk = dict(n_v1=len(keys1), n_v2=len(keys2), n_paired=len(paired),
                   ann_mean=float(np.mean([i1[k]["ann"]["test_acc"] for k in keys1])) * 100
                   if keys1 else None,
                   by_T={}, baseline_margin={}, paired_beta={}, energy={}, verdict={})
        for T in TS:
            l1 = [loss(i1[k], T) for k in keys1]
            l2 = [loss(i2[k], T) for k in keys2]
            pd = [loss(i1[k], T) - loss(i2[k], T) for k in paired]
            blk["by_T"][f"T{T}"] = dict(
                v1_loss_mean=round(float(np.mean(l1)), 3) if l1 else None,
                v2_loss_mean=round(float(np.mean(l2)), 3) if l2 else None,
                v2_loss_std=round(float(np.std(l2)), 3) if l2 else None,
                v2_loss_ci95=round(ci95(l2), 3) if l2 else None,
                paired_gain_pp=round(float(np.mean(pd)), 3) if pd else None,
                paired_gain_ci95=round(ci95(pd), 3) if pd else None)
            e1 = [i1[k]["energy"][f"ours_T{T}"]["energy_ratio_ann_over_snn"] for k in keys1
                  if f"ours_T{T}" in i1[k].get("energy", {})]
            e2 = [i2[k]["energy"][f"ours_T{T}"]["energy_ratio_ann_over_snn"] for k in keys2
                  if f"ours_T{T}" in i2[k].get("energy", {})]
            blk["energy"][f"T{T}"] = dict(
                v1_mean=round(float(np.mean(e1)), 3) if e1 else None,
                v2_mean=round(float(np.mean(e2)), 3) if e2 else None)
        for T in (4, 8):
            best = []
            for k in keys2:
                vals = [i2[k]["methods"][f"{b}_T{T}"]["acc"] for b in BASELINES
                        if f"{b}_T{T}" in i2[k]["methods"]]
                if vals:
                    best.append(i2[k]["methods"][f"ours_T{T}"]["acc"] * 100 - max(vals) * 100)
            blk["baseline_margin"][f"T{T}"] = dict(
                margin_pp_mean=round(float(np.mean(best)), 3) if best else None,
                margin_pp_ci95=round(ci95(best), 3) if best else None)
        # frozen expected_strong evaluation (v2 only)
        losses_le8 = [blk["by_T"][f"T{T}"]["v2_loss_mean"] for T in (1, 2, 4, 8)
                      if blk["by_T"][f"T{T}"]["v2_loss_mean"] is not None]
        t_band = min(losses_le8) if losses_le8 else None
        t4_margin = blk["baseline_margin"]["T4"]["margin_pp_mean"]
        max_e = max([v["v2_mean"] for v in blk["energy"].values()
                     if v["v2_mean"] is not None] or [0])
        # The frozen target requires >=5x at a timestep that ALSO stays inside
        # the 1.5pp accuracy band. A high ratio at T=1 with 20-44pp loss does
        # NOT count (this was the earlier overly-permissive check).
        eligible = [(T, blk["energy"][f"T{T}"]["v2_mean"]) for T in TS
                    if blk["by_T"][f"T{T}"]["v2_loss_mean"] is not None
                    and blk["by_T"][f"T{T}"]["v2_loss_mean"] <= 1.5
                    and blk["energy"][f"T{T}"]["v2_mean"] is not None]
        e_in_band = round(max(e for _, e in eligible), 3) if eligible else None
        blk["verdict"] = dict(
            accuracy_1_5pp_at_Tle8=dict(target="<=1.5pp at any T<=8", observed=t_band,
                                        passed=(t_band is not None and t_band <= 1.5)),
            baseline_margin_1pp_at_T4=dict(target=">=1.0pp", observed=t4_margin,
                                           passed=(t4_margin is not None and t4_margin >= 1.0)),
            energy_5x_within_band=dict(target=">=5x at a T inside the 1.5pp band",
                                       observed=e_in_band,
                                       passed=(e_in_band is not None and e_in_band >= 5.0)),
            energy_max_any_T_reference_only=dict(
                target="reference only; NOT an acceptance criterion",
                observed=round(max_e, 3), passed=False),
            identity_residual=dict(target="<1e-10",
                                   status="pending float64 recheck (H3 on novix 20049)"),
        )
        result["datasets"][ds] = blk

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# Paired Strong-Result Audit", "",
             f"> 生成 {result['generated']}｜v1 runs {result['v1_runs']}，v2 runs {result['v2_runs']}",
             "> 来源：本机 3060 CUDA 两份真实 `result.json`；**不是** novix `20049` 的产物。",
             "> 政策：`contracts/strong-result-no-retreat.md`，故事与目标冻结，只按改进路径冲。", "",
             "## 5-seed conversion loss（越低越好）", "",
             "| 数据集 | T | v1 带 β* | v2 去 β* | 配对改善 | v2 95% CI |",
             "|---|---|---:|---:|---:|---:|"]
    for ds, blk in result["datasets"].items():
        for T in TS:
            r = blk["by_T"][f"T{T}"]
            lines.append(f"| {ds} | {T} | "
                         f"{r['v1_loss_mean'] if r['v1_loss_mean'] is not None else '—'} | "
                         f"{r['v2_loss_mean'] if r['v2_loss_mean'] is not None else '—'} | "
                         f"{r['paired_gain_pp'] if r['paired_gain_pp'] is not None else '—'} | "
                         f"±{r['v2_loss_ci95'] if r['v2_loss_ci95'] is not None else '—'} |")
    lines += ["", "## 相对最强单点转换基线的领先（v2）", "",
              "| 数据集 | T | 领先 (pp) | 95% CI |", "|---|---|---:|---:|"]
    for ds, blk in result["datasets"].items():
        for T in (4, 8):
            m = blk["baseline_margin"][f"T{T}"]
            lines.append(f"| {ds} | {T} | {m['margin_pp_mean']} | ±{m['margin_pp_ci95']} |")
    lines += ["", "## 理论算术能耗比 ANN/SNN（45 nm 估算，非硬件实测）", "",
              "| 数据集 | T | v1 | v2 |", "|---|---|---:|---:|"]
    for ds, blk in result["datasets"].items():
        for T in TS:
            e = blk["energy"][f"T{T}"]
            lines.append(f"| {ds} | {T} | {e['v1_mean']} | {e['v2_mean']} |")
    lines += ["", "## 冻结强目标判定", ""]
    for ds, blk in result["datasets"].items():
        lines.append(f"### {ds}")
        for k, v in blk["verdict"].items():
            lines.append(f"- `{k}`：目标 {v.get('target', v.get('status'))}，"
                         f"实测 {v.get('observed', '—')}，"
                         f"{'PASS' if v.get('passed') else '未达/待核'}")
        lines.append("")
    lines += ["## 读法", "",
              "- v2 未完成全部 seeds 时，其数值按已完成 seeds 计算，并在 `paired_analysis.json` 记录 `n_v2`。",
              "- 未达项按 `strong-result-no-retreat.md` 只走改进重跑，不改定位、不降阈值、不挑 seed。",
              "- CUDA 稀疏归约非确定，v1/v2 的 ANN 有约 0.5pp 差异；配对比较一律用各自运行内的 conversion loss。", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({ds: blk["verdict"] for ds, blk in result["datasets"].items()},
                     ensure_ascii=False, indent=2))
    print("WROTE", OUT, REPORT)


if __name__ == "__main__":
    main()
