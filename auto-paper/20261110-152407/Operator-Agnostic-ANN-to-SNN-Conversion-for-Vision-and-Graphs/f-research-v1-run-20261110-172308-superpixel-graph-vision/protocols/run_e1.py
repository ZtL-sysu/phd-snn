#!/usr/bin/env python3
"""E1: 5-seed validation of the gauge/theta working point (P5 correction loop).

Also performs E4 (float64 exact-identity residual) and reports BOTH energy
accounting conventions (primary event-driven AC, conservative A-propagation MAC)
so H1 is closed locally rather than waiting on the stalled novix task.

Protocol: the working point is selected ONLY on the frozen validation split;
test is evaluated exactly once with the selected point.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vision_pipeline as vp  # noqa: E402

R = HERE.parent
DATA = R / "data" / "pyg_bench"
OUT = R / "results" / "e1"
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ("MNIST", "CIFAR10")
SEEDS = (0, 1, 2, 3, 4)
SCALES = (0.5, 1.0, 2.0)
THETAS = (1.0, 2.0)
TS = (4, 8)
CFG = dict(n_train=2000, n_val=500, n_test=500, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")


def rescale(model, s):
    m = dict(model)
    m["W1"], m["b1"], m["W2"] = model["W1"] / s, model["b1"] / s, model["W2"] * s
    m["B1"], m["H1"] = model["B1"] / s, model["H1"] / s
    return m


def identity_f64(data, model, T, theta, scale, seed=0):
    """E4: exact identity in float64, using the SAME deterministic spike train."""
    # Everything in float64 FROM THE START: mixing an fp32 inst1 with fp64
    # accumulators inflated the residual to ~2e-7 on narrow networks.
    A64 = data["A"].astype(np.float64)
    R64 = data["R"].astype(np.float64)
    X64 = data["X"].astype(np.float64)
    W1_64 = model["W1"].astype(np.float64)
    b1_64 = model["b1"].astype(np.float64)
    W2 = model["W2"].astype(np.float64)
    b2_64 = model["b2"].astype(np.float64)
    inst1 = np.asarray(A64 @ (X64 @ W1_64), dtype=np.float64) + b1_64
    H1 = np.maximum(inst1, 0.0)
    rng = np.random.default_rng(seed)
    trains = vp._spike_train(inst1, T, theta, "ours", 0.0, rng)
    B = np.asarray(R64 @ (np.asarray(A64 @ (H1 @ W2), dtype=np.float64)),
                   dtype=np.float64) + b2_64
    acc = np.zeros_like(B)
    for s in trains:
        Z = np.asarray(A64 @ (s.astype(np.float64) @ W2), dtype=np.float64)
        acc += np.asarray(R64 @ Z, dtype=np.float64) + b2_64
    B_hat = acc / float(T)
    E1 = (np.sum(trains, axis=0) / float(T)).astype(np.float64) - H1
    rhs = np.asarray(R64 @ (np.asarray(A64 @ (E1 @ W2), dtype=np.float64)), dtype=np.float64)
    return float(np.max(np.abs((B_hat - B) - rhs)))


def conservative_ratio(r, data, model, T):
    H = model["W2"].shape[0]
    C = model["W2"].shape[1]
    ann_pj = r["ann_macs"] * vp.E_MAC_PJ
    snn_pj = r["hidden_spikes"] * H * vp.E_AC_PJ + T * data["E"] * C * vp.E_MAC_PJ
    return float(ann_pj / max(snn_pj, 1e-12))


def main():
    result = dict(meta=dict(note="E1/E4 real local 3060 CUDA runs; val-selected, test once",
                            started=datetime.now().isoformat(), config=CFG),
                  runs=[])
    t0 = time.time()
    for ds in DATASETS:
        for seed in SEEDS:
            ts = time.time()
            try:
                sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"],
                                    n_val=CFG["n_val"], n_test=CFG["n_test"], seed=seed)
                tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
                va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"], pool="sum")
                te = vp.batch_graphs(sp["test"]["graphs"], sp["test"]["indices"], pool="sum")
                model = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                     epochs=CFG["epochs"], lr=CFG["lr"], device=CFG["device"])
                ann_val = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean()) * 100
                ann_test = float((vp.ann_logits(te, model).argmax(1) == te["y"]).mean()) * 100

                cands = []
                for s in SCALES:
                    m = rescale(model, s)
                    for th in THETAS:
                        for T in TS:
                            rv = vp.convert(va, m, T, theta=th, method="ours",
                                            readout="membrane", beta=0.0, seed=seed)
                            cands.append(dict(scale=s, theta=th, T=T,
                                              val_loss_pp=round(ann_val - rv["acc"] * 100, 3)))
                best = min(cands, key=lambda x: x["val_loss_pp"])
                m = rescale(model, best["scale"])
                r = vp.convert(te, m, best["T"], theta=best["theta"], method="ours",
                               readout="membrane", beta=0.0, seed=seed)
                e = vp.energy_accounting(r, best["T"])
                resid = identity_f64(te, m, best["T"], best["theta"], best["scale"], seed)
                rec = dict(dataset=ds, seed=seed, ann_val=round(ann_val, 3),
                           ann_test=round(ann_test, 3), selected=best,
                           test_acc=round(r["acc"] * 100, 3),
                           test_loss_pp=round(ann_test - r["acc"] * 100, 3),
                           energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                           energy_conservative=round(conservative_ratio(r, te, m, best["T"]), 4),
                           spikes=int(r["total_spikes"]),
                           identity_f64_residual=resid,
                           ann_logit_drift=float(np.max(np.abs(
                               vp.ann_logits(te, m) - vp.ann_logits(te, model)))),
                           wall_sec=round(time.time() - ts, 1))
            except Exception as exc:
                rec = dict(dataset=ds, seed=seed,
                           error=f"{type(exc).__name__}: {exc}",
                           wall_sec=round(time.time() - ts, 1))
            result["runs"].append(rec)
            print(ds, seed, json.dumps({k: rec[k] for k in
                  ("ann_test", "selected", "test_loss_pp", "energy_primary",
                   "energy_conservative", "identity_f64_residual", "error")
                  if k in rec}, ensure_ascii=False), flush=True)
            (OUT / "result.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

    summary = {}
    for ds in DATASETS:
        rs = [r for r in result["runs"] if r.get("dataset") == ds and "test_loss_pp" in r]
        if not rs:
            summary[ds] = dict(error="no successful runs")
            continue
        summary[ds] = dict(
            n=len(rs),
            ann_mean=round(float(np.mean([r["ann_test"] for r in rs])), 3),
            loss_mean=round(float(np.mean([r["test_loss_pp"] for r in rs])), 3),
            loss_std=round(float(np.std([r["test_loss_pp"] for r in rs])), 3),
            loss_ci95=round(float(1.96 * np.std([r["test_loss_pp"] for r in rs]) / np.sqrt(len(rs))), 3),
            energy_primary_mean=round(float(np.mean([r["energy_primary"] for r in rs])), 4),
            energy_conservative_mean=round(float(np.mean([r["energy_conservative"] for r in rs])), 4),
            identity_max=max(r["identity_f64_residual"] for r in rs),
            selected_counts={str((r["selected"]["scale"], r["selected"]["theta"],
                                  r["selected"]["T"])):
                             sum(1 for x in rs if (x["selected"]["scale"],
                                                   x["selected"]["theta"],
                                                   x["selected"]["T"]) ==
                                 (r["selected"]["scale"], r["selected"]["theta"],
                                  r["selected"]["T"])) for r in rs},
        )
    result["summary"] = summary
    result["meta"]["finished"] = datetime.now().isoformat()
    result["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
