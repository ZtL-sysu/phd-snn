#!/usr/bin/env python3
"""E17 FINAL confirmation: frozen margin points + untouched holdout + fp64 forward.

Points are frozen from E16 (MNIST) and E15 (CIFAR10) multi-seed validation
screening. Holdout seeds 10-14 have NEVER been used for any test evaluation in
this project. The conversion path is fully float64 so the exact identity can be
verified below 1e-10; no separate fp32/fp64 paths remain.

Test is evaluated exactly once per seed. No tuning is permitted here.
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
OUT = R / "results" / "e17"
OUT.mkdir(parents=True, exist_ok=True)

POINTS = {
    # selected for small loss_std and large two-convention energy margins
    "MNIST": dict(margin_coef=0.4, keep_frac=0.08, theta=1.5, T=3),
    "CIFAR10": dict(margin_coef=0.2, keep_frac=0.08, theta=1.0, T=3),
}
SEEDS = (10, 11, 12, 13, 14)
CFG = dict(n_train=2000, n_val=1000, n_test=2000, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")
MIN_ANN = 20.0


def make_mask(base_model, tr, keep_frac):
    H = base_model["W1"].shape[1]
    k = max(1, int(round(H * keep_frac)))
    importance = np.maximum(tr["X"] @ base_model["W1"], 0.0).mean(axis=0)
    mask = np.zeros(H, dtype=bool)
    mask[np.argsort(importance)[-k:]] = True
    return mask


def convert_f64(data, model, T, theta, beta=0.0):
    """Fully float64 conversion; identity verified against the SAME forward."""
    A64 = data["A"].astype(np.float64)
    R64 = data["R"].astype(np.float64)
    X64 = data["X"].astype(np.float64)
    W1 = model["W1"].astype(np.float64)
    b1 = model["b1"].astype(np.float64)
    W2 = model["W2"].astype(np.float64)
    b2 = model["b2"].astype(np.float64)
    G, C = R64.shape[0], W2.shape[1]
    H = W2.shape[0]

    inst1 = np.asarray(A64 @ (X64 @ W1), dtype=np.float64) + b1
    H1 = np.maximum(inst1, 0.0)
    n = np.clip(np.rint(np.clip(inst1 + beta, 0.0, None) * T / theta), 0.0, float(T))
    trains = [np.rint(t * n / T) - np.rint((t - 1) * n / T)
              for t in range(1, T + 1)]

    B = np.asarray(R64 @ (np.asarray(A64 @ (H1 @ W2), dtype=np.float64)),
                   dtype=np.float64) + b2
    mem = np.zeros((G, C), dtype=np.float64)
    hidden_spikes = 0.0
    for s in trains:
        Z = np.asarray(A64 @ (s @ W2), dtype=np.float64)
        mem += np.asarray(R64 @ Z, dtype=np.float64) + b2
        hidden_spikes += float(s.sum())
    B_hat = mem / float(T)
    E1 = (np.sum(trains, axis=0) / float(T)) - H1
    rhs = np.asarray(R64 @ (np.asarray(A64 @ (E1 @ W2), dtype=np.float64)),
                     dtype=np.float64)
    identity_residual = float(np.max(np.abs((B_hat - B) - rhs)))

    ann_macs = vp._ann_macs(data, model)
    deg_mean = data["E"] / max(data["N"], 1)
    ac_ops = hidden_spikes * (H + deg_mean * C)
    ann_pj = ann_macs * vp.E_MAC_PJ
    snn_pj = ac_ops * vp.E_AC_PJ
    degenerate = hidden_spikes <= 0 or ac_ops <= 1e-9
    ratio_primary = 0.0 if degenerate else float(ann_pj / max(snn_pj, 1e-12))
    snn_cons_pj = hidden_spikes * H * vp.E_AC_PJ + T * data["E"] * C * vp.E_MAC_PJ
    ratio_conservative = float(ann_pj / max(snn_cons_pj, 1e-12))

    ann_acc = float((B.argmax(1) == data["y"]).mean())
    snn_acc = float((B_hat.argmax(1) == data["y"]).mean())
    return dict(ann_acc=ann_acc, snn_acc=snn_acc,
                loss_pp=(ann_acc - snn_acc) * 100.0,
                energy_primary=ratio_primary,
                energy_conservative=ratio_conservative,
                identity_residual=identity_residual,
                spikes=int(hidden_spikes),
                zero_spike=bool(degenerate))


def main():
    out = dict(meta=dict(note="E17 FINAL: frozen points, untouched holdout seeds 10-14, "
                              "fp64 unified forward, test once, NO tuning",
                         started=datetime.now().isoformat(), config=CFG,
                         frozen_points=POINTS, seeds=list(SEEDS),
                         min_ann_val=MIN_ANN),
               runs=[], summary={})
    t0 = time.time()
    for ds, pt in POINTS.items():
        for seed in SEEDS:
            ts = time.time()
            try:
                sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"],
                                    n_val=CFG["n_val"], n_test=CFG["n_test"], seed=seed)
                tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
                te = vp.batch_graphs(sp["test"]["graphs"], sp["test"]["indices"], pool="sum")
                base = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                    epochs=CFG["epochs"], lr=CFG["lr"], device=CFG["device"])
                mask = make_mask(base, tr, pt["keep_frac"])
                model = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                     epochs=CFG["epochs"], lr=CFG["lr"],
                                     device=CFG["device"], unit_mask=mask,
                                     margin_coef=pt["margin_coef"])
                r = convert_f64(te, model, pt["T"], pt["theta"])
                rec = dict(dataset=ds, seed=seed, point=pt,
                           ann_test=round(r["ann_acc"] * 100, 3),
                           test_loss_pp=round(r["loss_pp"], 3),
                           energy_primary=round(r["energy_primary"], 4),
                           energy_conservative=round(r["energy_conservative"], 4),
                           identity_residual=r["identity_residual"],
                           spikes=r["spikes"], zero_spike=r["zero_spike"],
                           kept_units=int(mask.sum()),
                           wall_sec=round(time.time() - ts, 1))
            except Exception as exc:
                rec = dict(dataset=ds, seed=seed,
                           error=f"{type(exc).__name__}: {exc}",
                           wall_sec=round(time.time() - ts, 1))
            out["runs"].append(rec)
            print(ds, seed, json.dumps({k: rec[k] for k in
                  ("ann_test", "test_loss_pp", "energy_primary",
                   "energy_conservative", "identity_residual", "error")
                  if k in rec}, ensure_ascii=False), flush=True)
            (OUT / "confirmation.json").write_text(
                json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

    for ds in POINTS:
        rs = [x for x in out["runs"] if x.get("dataset") == ds and "test_loss_pp" in x]
        if not rs:
            out["summary"][ds] = dict(error="no successful runs")
            continue
        loss = np.array([x["test_loss_pp"] for x in rs])
        ep = np.array([x["energy_primary"] for x in rs])
        ec = np.array([x["energy_conservative"] for x in rs])
        ann = np.array([x["ann_test"] for x in rs])
        out["summary"][ds] = dict(
            n=len(rs),
            ann_mean=round(float(ann.mean()), 3), ann_std=round(float(ann.std()), 3),
            loss_mean=round(float(loss.mean()), 3), loss_std=round(float(loss.std()), 3),
            loss_ci95=round(float(1.96 * loss.std() / np.sqrt(len(loss))), 3),
            energy_primary_mean=round(float(ep.mean()), 4),
            energy_conservative_mean=round(float(ec.mean()), 4),
            energy_primary_min=round(float(ep.min()), 4),
            energy_conservative_min=round(float(ec.min()), 4),
            identity_max=max(x["identity_residual"] for x in rs),
            teacher_ok=bool(ann.mean() >= MIN_ANN),
            accuracy_ok=bool(loss.mean() <= 1.5),
            energy_ok=bool(ep.mean() >= 5.0 and ec.mean() >= 5.0),
            identity_ok=bool(max(x["identity_residual"] for x in rs) < 1e-10),
        )
    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "confirmation.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", json.dumps(out["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
