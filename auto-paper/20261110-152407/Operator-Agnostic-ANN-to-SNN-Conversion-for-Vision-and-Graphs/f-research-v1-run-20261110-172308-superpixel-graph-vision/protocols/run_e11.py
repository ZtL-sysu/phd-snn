#!/usr/bin/env python3
"""E11: frozen-working-point 5-seed confirmation (test evaluated ONCE).

E10 found strict-qualifying working points on validation with seed 0. This run
FREEZES those points and re-trains the narrow network on 5 frozen seeds, then
evaluates each on its held-out test split exactly once. No further tuning is
permitted here: any tuning would require a new versioned screening run.

Acceptance for P5: both datasets have 5-seed mean loss <= 1.5pp AND both
energy conventions >= 5x, with teacher accuracy above 2x chance.
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
from run_e1 import identity_f64, conservative_ratio  # noqa: E402

R = HERE.parent
DATA = R / "data" / "pyg_bench"
OUT = R / "results" / "e11"
OUT.mkdir(parents=True, exist_ok=True)

# FROZEN from E10 validation screening (strict qualifying points).
POINTS = {
    "MNIST": dict(keep_frac=0.1, theta=1.5, T=3),
    "CIFAR10": dict(keep_frac=0.08, theta=1.0, T=3),
}
SEEDS = (0, 1, 2, 3, 4)
CFG = dict(n_train=2000, n_val=500, n_test=500, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")
MIN_ANN = 20.0


def make_mask(base_model, tr, keep_frac):
    H = base_model["W1"].shape[1]
    k = max(1, int(round(H * keep_frac)))
    importance = np.maximum(tr["X"] @ base_model["W1"], 0.0).mean(axis=0)
    mask = np.zeros(H, dtype=bool)
    mask[np.argsort(importance)[-k:]] = True
    return mask


def main():
    out = dict(meta=dict(note="E11 frozen working point, 5 seeds, test once; NO tuning",
                         started=datetime.now().isoformat(), config=CFG,
                         frozen_points=POINTS, seeds=list(SEEDS)),
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
                                     device=CFG["device"], unit_mask=mask)
                ann_test = float((vp.ann_logits(te, model).argmax(1) == te["y"]).mean()) * 100
                r = vp.convert(te, model, pt["T"], theta=pt["theta"], method="ours",
                               readout="membrane", beta=0.0, seed=seed)
                e = vp.energy_accounting(r, pt["T"])
                resid = identity_f64(te, model, pt["T"], pt["theta"],
                                     1.0, seed)  # scale arg unused; no extra gauge here
                rec = dict(dataset=ds, seed=seed, point=pt,
                           ann_test=round(ann_test, 3),
                           test_loss_pp=round(ann_test - r["acc"] * 100, 3),
                           energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                           energy_conservative=round(conservative_ratio(r, te, model, pt["T"]), 4),
                           spikes=int(r["total_spikes"]),
                           zero_spike=e.get("zero_spike_degenerate", False),
                           identity_f64_residual=resid,
                           kept_units=int(mask.sum()),
                           wall_sec=round(time.time() - ts, 1))
            except Exception as exc:
                rec = dict(dataset=ds, seed=seed,
                           error=f"{type(exc).__name__}: {exc}",
                           wall_sec=round(time.time() - ts, 1))
            out["runs"].append(rec)
            print(ds, seed, json.dumps({k: rec[k] for k in
                  ("ann_test", "test_loss_pp", "energy_primary",
                   "energy_conservative", "identity_f64_residual", "error")
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
            identity_max=max(x["identity_f64_residual"] for x in rs),
            teacher_ok=bool(ann.mean() >= MIN_ANN),
            accuracy_ok=bool(loss.mean() <= 1.5),
            energy_ok=bool(ep.mean() >= 5.0 and ec.mean() >= 5.0),
        )
    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "confirmation.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", json.dumps(out["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
