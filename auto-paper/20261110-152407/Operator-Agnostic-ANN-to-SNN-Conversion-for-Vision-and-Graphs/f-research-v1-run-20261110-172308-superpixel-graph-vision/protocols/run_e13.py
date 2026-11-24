#!/usr/bin/env python3
"""E13: multi-seed validation working-point selection (val-only, no test).

E10 selected a point from 75 candidates using ONE seed's validation split;
E11/E12 showed a large val->test gap. Here we aggregate over 3 val seeds and
pick the point with the best margin under the strict four conditions.

A selected point is a VERSIONED new screening result; it must be confirmed on
a fresh untouched holdout (seeds 10-14) before any P5 claim.
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
from run_e1 import conservative_ratio  # noqa: E402

R = HERE.parent
DATA = R / "data" / "pyg_bench"
OUT = R / "results" / "e13"
OUT.mkdir(parents=True, exist_ok=True)

VAL_SEEDS = (0, 1, 2)
GRID = {
    "MNIST": dict(keeps=(0.1, 0.15, 0.2, 0.3)),
    "CIFAR10": dict(keeps=(0.08, 0.1, 0.15, 0.2)),
}
THETAS = (1.0, 1.5, 2.0)
TS = (2, 3, 4)
MIN_ANN = 20.0
CFG = dict(n_train=2000, n_val=1000, n_test=500, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")


def make_mask(base_model, tr, keep_frac):
    H = base_model["W1"].shape[1]
    k = max(1, int(round(H * keep_frac)))
    importance = np.maximum(tr["X"] @ base_model["W1"], 0.0).mean(axis=0)
    mask = np.zeros(H, dtype=bool)
    mask[np.argsort(importance)[-k:]] = True
    return mask


def main():
    out = dict(meta=dict(note="E13 multi-seed VAL-ONLY robust selection; test never touched",
                         started=datetime.now().isoformat(), config=CFG,
                         val_seeds=list(VAL_SEEDS), thetas=list(THETAS), Ts=list(TS),
                         min_ann_val=MIN_ANN),
               per_seed={}, aggregated={})
    t0 = time.time()
    for ds, g in GRID.items():
        all_rows = []
        for seed in VAL_SEEDS:
            sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"],
                                n_val=CFG["n_val"], n_test=CFG["n_test"], seed=seed)
            tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
            va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"], pool="sum")
            base = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                epochs=CFG["epochs"], lr=CFG["lr"], device=CFG["device"])
            for kf in g["keeps"]:
                mask = make_mask(base, tr, kf)
                model = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                     epochs=CFG["epochs"], lr=CFG["lr"],
                                     device=CFG["device"], unit_mask=mask)
                ann_val = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean()) * 100
                for th in THETAS:
                    for T in TS:
                        r = vp.convert(va, model, T, theta=th, method="ours",
                                       readout="membrane", beta=0.0, seed=seed)
                        e = vp.energy_accounting(r, T)
                        all_rows.append(dict(
                            seed=seed, keep_frac=kf, theta=th, T=T,
                            ann_val=round(ann_val, 3),
                            val_loss_pp=round(ann_val - r["acc"] * 100, 3),
                            energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                            energy_conservative=round(conservative_ratio(r, va, model, T), 4),
                            spikes=int(r["total_spikes"]),
                            zero_spike=e.get("zero_spike_degenerate", False)))
                print(f"{ds} seed={seed} keep={kf} ann_val={ann_val:.2f}% "
                      f"rows={len(all_rows)} elapsed={time.time()-t0:.1f}s", flush=True)
            out["per_seed"][f"{ds}_seed{seed}"] = all_rows[-len(g["keeps"]) * len(THETAS) * len(TS):]
            (OUT / "val_multiseed.json").write_text(
                json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

        groups = {}
        for row in all_rows:
            key = (row["keep_frac"], row["theta"], row["T"])
            groups.setdefault(key, []).append(row)
        agg = []
        for key, rows in groups.items():
            agg.append(dict(
                keep_frac=key[0], theta=key[1], T=key[2], n=len(rows),
                ann_mean=round(float(np.mean([x["ann_val"] for x in rows])), 3),
                loss_mean=round(float(np.mean([x["val_loss_pp"] for x in rows])), 3),
                loss_std=round(float(np.std([x["val_loss_pp"] for x in rows])), 3),
                energy_primary_mean=round(float(np.mean([x["energy_primary"] for x in rows])), 4),
                energy_conservative_mean=round(float(np.mean([x["energy_conservative"] for x in rows])), 4),
                energy_primary_min=round(float(np.min([x["energy_primary"] for x in rows])), 4),
                energy_conservative_min=round(float(np.min([x["energy_conservative"] for x in rows])), 4),
                any_zero_spike=any(x["zero_spike"] for x in rows)))
        qualifying = [x for x in agg
                      if x["ann_mean"] >= MIN_ANN
                      and x["loss_mean"] <= 1.5
                      and not x["any_zero_spike"]
                      and x["energy_primary_mean"] >= 5.0
                      and x["energy_conservative_mean"] >= 5.0]
        qualifying.sort(key=lambda x: (-min(x["energy_primary_mean"],
                                            x["energy_conservative_mean"]),
                                       x["loss_mean"]))
        out["aggregated"][ds] = dict(
            n_rows=len(all_rows), n_points=len(agg),
            qualifying=qualifying,
            best_loss=sorted(agg, key=lambda x: x["loss_mean"])[:5],
            all_points=agg)
        print(f"{ds} MULTISEED QUALIFYING={len(qualifying)} "
              f"top={json.dumps(qualifying[:3], ensure_ascii=False)}", flush=True)

    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "val_multiseed.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
