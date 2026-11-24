#!/usr/bin/env python3
"""E7: structural pruning (unit mask) as the last energy-improvement route.

E2 showed that a soft sparsity penalty barely changes the spike count. Here we
remove hidden units outright (W1 columns, b1, W2 rows), which cuts spikes
proportionally. This is a VALIDATION-ONLY screening run; test is untouched.
A point counts only if val_loss <= 1.5pp AND both energy conventions >= 5x.
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
OUT = R / "results" / "e7"
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ("MNIST", "CIFAR10")
SEED = 0
PRUNE = (0.0, 0.5, 0.8, 0.9, 0.95)
THETAS = (1.0, 2.0, 4.0)
TS = (4, 8)
CFG = dict(n_train=2000, n_val=500, n_test=500, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")


def prune_model(model, keep_frac, tr):
    m = dict(model)
    B1 = tr["X"] @ model["W1"]
    importance = np.maximum(B1, 0.0).mean(axis=0)
    k = max(1, int(round(model["W1"].shape[1] * keep_frac)))
    keep = np.zeros(model["W1"].shape[1], dtype=bool)
    keep[np.argsort(importance)[-k:]] = True
    m["W1"] = model["W1"] * keep[None, :]
    m["b1"] = model["b1"] * keep
    m["W2"] = model["W2"] * keep[:, None]
    return m, float(keep.mean())


def conservative_ratio(r, data, model, T):
    H, C = model["W2"].shape
    ann_pj = r["ann_macs"] * vp.E_MAC_PJ
    snn_pj = r["hidden_spikes"] * H * vp.E_AC_PJ + T * data["E"] * C * vp.E_MAC_PJ
    return float(ann_pj / max(snn_pj, 1e-12))


def main():
    out = dict(meta=dict(note="E7 validation-only structural-pruning screening; test never touched",
                         started=datetime.now().isoformat(), config=CFG, seed=SEED,
                         prune=list(PRUNE), thetas=list(THETAS), Ts=list(TS)),
               datasets={})
    t0 = time.time()
    for ds in DATASETS:
        sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"], n_val=CFG["n_val"],
                            n_test=CFG["n_test"], seed=SEED)
        tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
        va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"], pool="sum")
        model = vp.train_ann(tr, hidden=CFG["hidden"], seed=SEED,
                             epochs=CFG["epochs"], lr=CFG["lr"], device=CFG["device"])
        rows = []
        for p in PRUNE:
            m, kept = prune_model(model, 1.0 - p, tr)
            ann_val = float((vp.ann_logits(va, m).argmax(1) == va["y"]).mean()) * 100
            for th in THETAS:
                for T in TS:
                    r = vp.convert(va, m, T, theta=th, method="ours",
                                   readout="membrane", beta=0.0, seed=SEED)
                    e = vp.energy_accounting(r, T)
                    rows.append(dict(prune=p, kept_frac=round(kept, 3),
                                     theta=th, T=T,
                                     ann_val=round(ann_val, 3),
                                     val_loss_pp=round(ann_val - r["acc"] * 100, 3),
                                     energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                                     energy_conservative=round(conservative_ratio(r, va, m, T), 4),
                                     spikes=int(r["total_spikes"]),
                                     zero_spike=e.get("zero_spike_degenerate", False)))
            print(f"{ds} prune={p} kept={kept:.3f} ann_val={ann_val:.2f}% "
                  f"rows={len(rows)} elapsed={time.time()-t0:.1f}s", flush=True)
            out["datasets"][ds] = dict(rows=rows)
            (OUT / "val_sweep.json").write_text(
                json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

        qualifying = [x for x in rows
                      if x["val_loss_pp"] <= 1.5
                      and not x["zero_spike"]
                      and x["energy_primary"] >= 5.0
                      and x["energy_conservative"] >= 5.0]
        qualifying.sort(key=lambda x: (-min(x["energy_primary"], x["energy_conservative"]),
                                       x["val_loss_pp"]))
        in_band = sorted([x for x in rows if x["val_loss_pp"] <= 1.5 and not x["zero_spike"]],
                         key=lambda x: -min(x["energy_primary"], x["energy_conservative"]))
        out["datasets"][ds] = dict(
            n_rows=len(rows), qualifying=qualifying,
            best_in_band=in_band[:5], rows=rows)
        print(f"{ds} QUALIFYING={len(qualifying)} best_in_band="
              f"{json.dumps(in_band[:2], ensure_ascii=False)}", flush=True)

    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "val_sweep.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
