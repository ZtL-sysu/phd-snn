#!/usr/bin/env python3
"""E15: margin regularisation (1028 bound) to lower low-T conversion loss.

Validation-only coarse screening. Trains narrow networks with a hinge that
enlarges the ANN logit margin Delta, then checks whether a low-T working point
satisfies the strict four conditions on BOTH datasets' validation splits.
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
OUT = R / "results" / "e16"
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ("MNIST",)
VAL_SEEDS = (0, 1)
MARGIN_COEFS = (0.3, 0.4, 0.5, 0.6, 0.8)
KEEPS = {"MNIST": (0.08, 0.1, 0.12, 0.15), "CIFAR10": (0.08, 0.15)}
THETAS = (1.25, 1.5, 1.75, 2.0)
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
    out = dict(meta=dict(note="E16 MNIST fine grid around the 0.15pp gap; test never touched",
                         started=datetime.now().isoformat(), config=CFG,
                         val_seeds=list(VAL_SEEDS), margin_coefs=list(MARGIN_COEFS)),
               datasets={})
    t0 = time.time()
    for ds in DATASETS:
        rows = []
        for seed in VAL_SEEDS:
            sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"],
                                n_val=CFG["n_val"], n_test=CFG["n_test"], seed=seed)
            tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
            va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"], pool="sum")
            base = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                epochs=CFG["epochs"], lr=CFG["lr"], device=CFG["device"])
            for mc in MARGIN_COEFS:
                for kf in KEEPS[ds]:
                    mask = make_mask(base, tr, kf)
                    model = vp.train_ann(tr, hidden=CFG["hidden"], seed=seed,
                                         epochs=CFG["epochs"], lr=CFG["lr"],
                                         device=CFG["device"], unit_mask=mask,
                                         margin_coef=mc)
                    ann_val = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean()) * 100
                    for th in THETAS:
                        for T in TS:
                            r = vp.convert(va, model, T, theta=th, method="ours",
                                           readout="membrane", beta=0.0, seed=seed)
                            e = vp.energy_accounting(r, T)
                            rows.append(dict(
                                seed=seed, margin_coef=mc, keep_frac=kf,
                                theta=th, T=T, ann_val=round(ann_val, 3),
                                val_loss_pp=round(ann_val - r["acc"] * 100, 3),
                                energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                                energy_conservative=round(conservative_ratio(r, va, model, T), 4),
                                spikes=int(r["total_spikes"]),
                                zero_spike=e.get("zero_spike_degenerate", False)))
                print(f"{ds} seed={seed} margin={mc} rows={len(rows)} "
                      f"elapsed={time.time()-t0:.1f}s", flush=True)
                (OUT / "val_sweep.json").write_text(
                    json.dumps(dict(meta=out["meta"], datasets={ds: dict(rows=rows)}),
                               ensure_ascii=False, indent=2, default=float), encoding="utf-8")

        groups = {}
        for row in rows:
            key = (row["margin_coef"], row["keep_frac"], row["theta"], row["T"])
            groups.setdefault(key, []).append(row)
        agg = []
        for key, rr in groups.items():
            agg.append(dict(
                margin_coef=key[0], keep_frac=key[1], theta=key[2], T=key[3],
                n=len(rr),
                ann_mean=round(float(np.mean([x["ann_val"] for x in rr])), 3),
                loss_mean=round(float(np.mean([x["val_loss_pp"] for x in rr])), 3),
                loss_std=round(float(np.std([x["val_loss_pp"] for x in rr])), 3),
                energy_primary_mean=round(float(np.mean([x["energy_primary"] for x in rr])), 4),
                energy_conservative_mean=round(float(np.mean([x["energy_conservative"] for x in rr])), 4),
                any_zero_spike=any(x["zero_spike"] for x in rr)))
        qualifying = [x for x in agg if x["ann_mean"] >= MIN_ANN
                      and x["loss_mean"] <= 1.5 and not x["any_zero_spike"]
                      and x["energy_primary_mean"] >= 5.0
                      and x["energy_conservative_mean"] >= 5.0]
        qualifying.sort(key=lambda x: (-min(x["energy_primary_mean"],
                                            x["energy_conservative_mean"]), x["loss_mean"]))
        out["datasets"][ds] = dict(
            n_rows=len(rows), n_points=len(agg), qualifying=qualifying,
            best_loss=sorted(agg, key=lambda x: x["loss_mean"])[:5],
            margin0_best=sorted([x for x in agg if x["margin_coef"] == 0.0],
                                key=lambda x: x["loss_mean"])[:3],
            all_points=agg)
        print(f"{ds} QUALIFYING={len(qualifying)} "
              f"best={json.dumps(qualifying[:3], ensure_ascii=False)}", flush=True)
        (OUT / "val_sweep.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "val_sweep.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
