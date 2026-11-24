#!/usr/bin/env python3
"""Quantify run-to-run variability of the T0 reproduction (same seed, N repeats)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parents[0]
sys.path.insert(0, str(R / "protocols"))
import vision_pipeline as vp  # noqa: E402
from run_e17 import convert_f64, make_mask  # noqa: E402

DATA = R / "data" / "pyg_bench"
POINTS = {"MNIST": dict(margin_coef=0.4, keep_frac=0.08, theta=1.5, T=3),
          "CIFAR10": dict(margin_coef=0.2, keep_frac=0.08, theta=1.0, T=3)}
SEED = 10
N = 3
paper = json.loads((R / "results" / "e17" / "confirmation.json").read_text(encoding="utf-8"))
by_seed = {(r["dataset"], r["seed"]): r for r in paper["runs"]}

out = {}
for ds, pt in POINTS.items():
    sp = vp.load_vision(ds, DATA, n_train=2000, n_val=1000, n_test=2000, seed=SEED)
    tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
    te = vp.batch_graphs(sp["test"]["graphs"], sp["test"]["indices"], pool="sum")
    base = vp.train_ann(tr, hidden=128, seed=SEED, epochs=800, lr=0.01, device="cuda")
    mask = make_mask(base, tr, pt["keep_frac"])
    runs = []
    for i in range(N):
        model = vp.train_ann(tr, hidden=128, seed=SEED, epochs=800, lr=0.01,
                             device="cuda", unit_mask=mask, margin_coef=pt["margin_coef"])
        r = convert_f64(te, model, pt["T"], pt["theta"])
        runs.append(dict(teacher=r["ann_acc"] * 100, converted=r["snn_acc"] * 100,
                         loss=r["loss_pp"]))
        print(ds, "repeat", i, runs[-1], flush=True)
    t = np.array([x["teacher"] for x in runs])
    l = np.array([x["loss"] for x in runs])
    p = by_seed[(ds, SEED)]
    out[ds] = dict(
        teacher_mean=float(t.mean()), teacher_std=float(t.std()),
        loss_mean=float(l.mean()), loss_std=float(l.std()),
        paper_teacher=p["ann_test"], paper_loss=p["test_loss_pp"],
        teacher_dev=float(t.mean() - p["ann_test"]),
        loss_dev=float(l.mean() - p["test_loss_pp"]),
        n=N, runs=runs)
    print(ds, json.dumps({k: round(v, 3) if isinstance(v, float) else v
                          for k, v in out[ds].items() if k != "runs"}), flush=True)

(HERE / "results" / "repro_stability.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("STABILITY_DONE")
