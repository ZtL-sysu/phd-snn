#!/usr/bin/env python3
"""E8: train a genuinely narrow network from scratch under a unit mask.

E7 amputated a trained wide teacher and its ANN collapsed to chance, which
faked a "0pp conversion loss" and a huge energy ratio. E8 instead TRAINS a
narrow network from scratch while holding masked units at zero (1028
unit_mask "prune-and-finetune" mechanism), so the teacher can recover.

Strict acceptance (all must hold):
  * teacher val accuracy >= 2 x chance (20% for 10 classes)
  * val conversion loss <= 1.5pp
  * non-zero spikes (no degenerate zero-pulse network)
  * BOTH energy conventions >= 5x
Validation-only screening: test is never touched.
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
OUT = R / "results" / "e10"
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ("MNIST", "CIFAR10")
SEED = 0
KEEP_FRACS = (0.3, 0.2, 0.15, 0.1, 0.08)
THETAS = (1.0, 1.5, 2.0, 2.5, 3.0)
TS = (2, 3, 4)
MIN_ANN_VAL = 20.0  # 2x chance for 10-class
CFG = dict(n_train=2000, n_val=500, n_test=500, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")


def make_mask(base_model, tr, keep_frac, seed):
    H = base_model["W1"].shape[1]
    k = max(1, int(round(H * keep_frac)))
    importance = np.maximum(tr["X"] @ base_model["W1"], 0.0).mean(axis=0)
    mask = np.zeros(H, dtype=bool)
    mask[np.argsort(importance)[-k:]] = True
    return mask


def conservative_ratio(r, data, model, T):
    H, C = model["W2"].shape
    ann_pj = r["ann_macs"] * vp.E_MAC_PJ
    snn_pj = r["hidden_spikes"] * H * vp.E_AC_PJ + T * data["E"] * C * vp.E_MAC_PJ
    return float(ann_pj / max(snn_pj, 1e-12))


def main():
    out = dict(meta=dict(note="E10 validation-only fine grid near the accuracy/energy crossing; test never touched",
                         started=datetime.now().isoformat(), config=CFG, seed=SEED,
                         keep_fracs=list(KEEP_FRACS), min_ann_val=MIN_ANN_VAL),
               datasets={})
    t0 = time.time()
    for ds in DATASETS:
        sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"], n_val=CFG["n_val"],
                            n_test=CFG["n_test"], seed=SEED)
        tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
        va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"], pool="sum")
        base = vp.train_ann(tr, hidden=CFG["hidden"], seed=SEED,
                            epochs=CFG["epochs"], lr=CFG["lr"], device=CFG["device"])
        rows = []
        for kf in KEEP_FRACS:
            mask = make_mask(base, tr, kf, SEED)
            model = vp.train_ann(tr, hidden=CFG["hidden"], seed=SEED,
                                 epochs=CFG["epochs"], lr=CFG["lr"],
                                 device=CFG["device"], unit_mask=mask)
            ann_val = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean()) * 100
            for th in THETAS:
                for T in TS:
                    r = vp.convert(va, model, T, theta=th, method="ours",
                                   readout="membrane", beta=0.0, seed=SEED)
                    e = vp.energy_accounting(r, T)
                    rows.append(dict(
                        keep_frac=kf, kept_units=int(mask.sum()), theta=th, T=T,
                        ann_val=round(ann_val, 3),
                        val_loss_pp=round(ann_val - r["acc"] * 100, 3),
                        energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                        energy_conservative=round(conservative_ratio(r, va, model, T), 4),
                        spikes=int(r["total_spikes"]),
                        zero_spike=e.get("zero_spike_degenerate", False)))
            print(f"{ds} keep={kf} kept={int(mask.sum())} ann_val={ann_val:.2f}% "
                  f"rows={len(rows)} elapsed={time.time()-t0:.1f}s", flush=True)
            out["datasets"][ds] = dict(rows=rows)
            (OUT / "val_sweep.json").write_text(
                json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

        strict = [x for x in rows
                  if x["ann_val"] >= MIN_ANN_VAL
                  and x["val_loss_pp"] <= 1.5
                  and not x["zero_spike"]
                  and x["energy_primary"] >= 5.0
                  and x["energy_conservative"] >= 5.0]
        strict.sort(key=lambda x: (-min(x["energy_primary"], x["energy_conservative"]),
                                   x["val_loss_pp"]))
        valid_teacher = [x for x in rows if x["ann_val"] >= MIN_ANN_VAL]
        best = sorted(valid_teacher,
                      key=lambda x: (x["val_loss_pp"],
                                     -min(x["energy_primary"], x["energy_conservative"])))[:5]
        out["datasets"][ds] = dict(n_rows=len(rows), strict_qualifying=strict,
                                   best_with_valid_teacher=best, rows=rows)
        print(f"{ds} STRICT QUALIFYING={len(strict)} "
              f"best={json.dumps(best[:2], ensure_ascii=False)}", flush=True)

    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "val_sweep.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
