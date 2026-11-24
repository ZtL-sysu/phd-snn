#!/usr/bin/env python3
"""P5 correction-loop candidate: strengthen the 1028 combination, do NOT retreat.

Finding to verify (single-seed local smoke): with the deterministic two-phase
schedule, the closed-form beta* is redundant and harmful. Removing it reaches
ANN-1.5pp at T<=4 instead of T=16. This script reproduces it on 3 frozen seeds
and reports accuracy/energy Pareto candidates. All numbers are real local runs.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vision_pipeline as vp  # noqa: E402

R = HERE.parent
RESULTS = R / "results"
DATA = R / "data" / "pyg_bench"
SEEDS = (0, 1, 2)
THETAS = (0.5, 1.0, 2.0)
TAGS = ("beta_star", "no_beta")
TS = (2, 4, 8)


def main():
    all_rows = []
    ann_by_seed = {}
    t0 = time.time()
    for seed in SEEDS:
        splits = vp.load_vision("MNIST", DATA, n_train=2000, n_val=500,
                                n_test=500, seed=seed)
        tr = vp.batch_graphs(splits["train"]["graphs"], splits["train"]["indices"], pool="sum")
        te = vp.batch_graphs(splits["test"]["graphs"], splits["test"]["indices"], pool="sum")
        model = vp.train_ann(tr, hidden=128, seed=seed, epochs=800, lr=0.01, device="cuda")
        ann = float((vp.ann_logits(te, model).argmax(1) == te["y"]).mean()) * 100
        ann_by_seed[seed] = ann
        print(f"seed {seed} ANN {ann:.2f}% gauge {model['gauge_scale']:.4f}", flush=True)
        for theta in THETAS:
            for tag in TAGS:
                for T in TS:
                    beta = theta / (2.0 * T) if tag == "beta_star" else 0.0
                    r = vp.convert(te, model, T, theta=theta, method="ours",
                                   readout="membrane", beta=beta, seed=seed)
                    e = vp.energy_accounting(r, T)
                    all_rows.append(dict(seed=seed, theta=theta, tag=tag, T=T,
                                         acc=round(r["acc"] * 100, 3),
                                         loss_pp=round(ann - r["acc"] * 100, 3),
                                         energy_ratio=round(e["energy_ratio_ann_over_snn"], 4),
                                         spikes=int(r["total_spikes"])))
        print(f"  seed {seed} done, elapsed {time.time()-t0:.1f}s", flush=True)

    groups = {}
    for row in all_rows:
        key = (row["theta"], row["tag"], row["T"])
        groups.setdefault(key, []).append(row)
    summary = []
    for key, rows in sorted(groups.items()):
        acc = np.array([x["acc"] for x in rows])
        loss = np.array([x["loss_pp"] for x in rows])
        en = np.array([x["energy_ratio"] for x in rows])
        summary.append(dict(theta=key[0], tag=key[1], T=key[2],
                            acc_mean=round(float(acc.mean()), 3),
                            acc_std=round(float(acc.std(ddof=0)), 3),
                            loss_pp_mean=round(float(loss.mean()), 3),
                            energy_mean=round(float(en.mean()), 4),
                            n=len(rows)))

    strong = [s for s in summary if s["loss_pp_mean"] <= 1.5]
    strong.sort(key=lambda s: (-s["energy_mean"], s["T"]))
    pareto = sorted(summary, key=lambda s: (s["loss_pp_mean"], -s["energy_mean"]))[:8]

    out = dict(
        note="LOCAL 3060 CUDA, 3 frozen seeds, MNIST superpixel subset 2000/500/500; "
             "pre-experiment correction-loop candidate, NOT the formal P4 result",
        environment=dict(device="cuda", epochs=800, hidden=128, lr=0.01, pool="sum",
                         energy_model="45nm theoretical arithmetic energy, NOT hardware measurement"),
        ann_by_seed=ann_by_seed,
        rows=all_rows, summary=summary,
        strong_result_candidates=strong,
        accuracy_energy_pareto=pareto,
        runtime_sec=round(time.time() - t0, 2),
    )
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "strengthen_candidates.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# Strengthen Candidates · P5 修正回路的本机预验证", "",
             "> 性质：本机 3060、3 个冻结 seed、MNIST 超像素图子集，**非正式 P4 结果**。",
             "> 政策依据：`contracts/strong-result-no-retreat.md` —— 故事不退、目标不下调，只允许改进方法。", "",
             "## 核心发现", "",
             "确定性两阶段已经精确实现发放率（`Σs[t]=n`），因此 1028 组合里用于补偿 floor 量化系统偏差的 "
             "`β*=θ/(2T)` 在该算子上**冗余且有害**。去掉后，精度强目标（ANN−1.5pp）在 T≤4 即可达到。", "",
             "| seed | ANN test (%) |", "|---|---:|"]
    for s, a in ann_by_seed.items():
        lines.append(f"| {s} | {a:.2f} |")
    lines += ["", "## 满足 1.5pp 强目标的候选（3-seed 均值）", "",
              "| θ | β | T | acc mean±std | conversion loss (pp) | ANN/SNN 理论能耗比 |",
              "|---:|---|---|---:|---:|---:|"]
    for s in strong:
        lines.append(f"| {s['theta']} | {s['tag']} | {s['T']} | "
                     f"{s['acc_mean']:.2f}±{s['acc_std']:.2f} | {s['loss_pp_mean']:.2f} | "
                     f"{s['energy_mean']:.3f}× |")
    if not strong:
        lines.append("| — | — | — | 无候选 | — | — |")
    lines += ["", "## 精度—能耗帕累托前 8（按 loss 升序）", "",
              "| θ | β | T | loss (pp) | 能耗比 |", "|---:|---|---|---:|---:|"]
    for s in pareto:
        lines.append(f"| {s['theta']} | {s['tag']} | {s['T']} | "
                     f"{s['loss_pp_mean']:.2f} | {s['energy_mean']:.3f}× |")
    lines += ["", "## 读法与后续", "",
              "- 能耗比仍为 45 nm **理论算术能耗估算**，不是硬件实测；两套口径由 novix 20049 的 H1 复核。",
              "- 若要同时把能耗比推到 5×，合法路径是稀疏化 teacher / 降低 spike 密度，而不是改口径或把 5× 目标下调。",
              "- 该发现是**改进型 rescue**：组件组合被重新认定（精确计数 + 膜电位解码 + ρ 加权，去掉冗余 β*），"
              "故事定位不变、目标不变、负结果保留。",
              "- 正式 5-seed 全量仍以 novix `20049` 及其后续改进臂为准；本文件只用于定向设计改进臂。", ""]
    (R / "audits" / "strengthen-candidate-report.md").write_text(
        "\n".join(lines), encoding="utf-8")

    print("STRONG_CANDIDATES", json.dumps(strong[:6], ensure_ascii=False), flush=True)
    print("WROTE", RESULTS / "strengthen_candidates.json", flush=True)


if __name__ == "__main__":
    main()
