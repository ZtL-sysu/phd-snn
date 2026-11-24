#!/usr/bin/env python3
"""E2: sparsity + threshold + gauge sweep to close the 5x energy target.

Coarse screening stage: EVERYTHING is evaluated on the frozen validation
split only. Test is never touched here; the selected working point goes to a
separate 5-seed confirmation run (test once). This preserves test isolation.

Two energy conventions are reported simultaneously (H1):
  primary      = event-driven AC only
  conservative = A-propagation counted as MAC
A point counts only if val_loss <= 1.5pp AND BOTH ratios >= 5x.
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
OUT = R / "results" / "e2"
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ("MNIST", "CIFAR10")
SEED = 0
SPARSITIES = (0.0, 1e-4, 1e-3, 1e-2)
SCALES = (0.5, 1.0, 2.0)
THETAS = (1.0, 2.0, 4.0, 8.0)
TS = (4, 8)
CFG = dict(n_train=2000, n_val=500, n_test=500, epochs=800,
           hidden=128, lr=0.01, device="cuda", pool="sum")


def rescale(model, s):
    m = dict(model)
    m["W1"], m["b1"], m["W2"] = model["W1"] / s, model["b1"] / s, model["W2"] * s
    m["B1"], m["H1"] = model["B1"] / s, model["H1"] / s
    return m


def conservative_ratio(r, data, model, T):
    H, C = model["W2"].shape
    ann_pj = r["ann_macs"] * vp.E_MAC_PJ
    snn_pj = r["hidden_spikes"] * H * vp.E_AC_PJ + T * data["E"] * C * vp.E_MAC_PJ
    return float(ann_pj / max(snn_pj, 1e-12))


def main():
    out = dict(meta=dict(note="E2 coarse VALIDATION-ONLY screening; test never touched",
                         started=datetime.now().isoformat(), config=CFG,
                         seed=SEED, sparsities=list(SPARSITIES),
                         scales=list(SCALES), thetas=list(THETAS), Ts=list(TS)),
               datasets={})
    t0 = time.time()
    for ds in DATASETS:
        sp = vp.load_vision(ds, DATA, n_train=CFG["n_train"], n_val=CFG["n_val"],
                            n_test=CFG["n_test"], seed=SEED)
        tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
        va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"], pool="sum")
        rows = []
        for lam in SPARSITIES:
            ts = time.time()
            model = vp.train_ann(tr, hidden=CFG["hidden"], seed=SEED,
                                 epochs=CFG["epochs"], lr=CFG["lr"],
                                 device=CFG["device"], sparsity=lam)
            ann_val = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean()) * 100
            for s in SCALES:
                m = rescale(model, s)
                for th in THETAS:
                    for T in TS:
                        r = vp.convert(va, m, T, theta=th, method="ours",
                                       readout="membrane", beta=0.0, seed=SEED)
                        e = vp.energy_accounting(r, T)
                        rows.append(dict(
                            sparsity=lam, scale=s, theta=th, T=T,
                            ann_val=round(ann_val, 3),
                            val_loss_pp=round(ann_val - r["acc"] * 100, 3),
                            energy_primary=round(e["energy_ratio_ann_over_snn"], 4),
                            energy_conservative=round(conservative_ratio(r, va, m, T), 4),
                            spikes=int(r["total_spikes"])))
            print(f"{ds} sparsity={lam} ann_val={ann_val:.2f}% "
                  f"rows={len(rows)} elapsed={time.time()-t0:.1f}s", flush=True)
            # incremental persistence
            out["datasets"][ds] = dict(rows=rows)
            (OUT / "val_sweep.json").write_text(
                json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")

        qualifying = [x for x in rows
                      if x["val_loss_pp"] <= 1.5
                      and x["energy_primary"] >= 5.0
                      and x["energy_conservative"] >= 5.0]
        qualifying.sort(key=lambda x: (-min(x["energy_primary"], x["energy_conservative"]),
                                       x["val_loss_pp"]))
        pareto = sorted(rows, key=lambda x: (x["val_loss_pp"],
                                            -min(x["energy_primary"], x["energy_conservative"])))[:10]
        out["datasets"][ds] = dict(
            n_rows=len(rows), qualifying=qualifying, pareto_top10=pareto, rows=rows)
        print(f"{ds} QUALIFYING={len(qualifying)} "
              f"best={json.dumps(qualifying[:3], ensure_ascii=False)}", flush=True)

    out["meta"]["finished"] = datetime.now().isoformat()
    out["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "val_sweep.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print("DONE", json.dumps({k: {"qualifying": len(v["qualifying"]),
                                  "best": v["qualifying"][:2]}
                              for k, v in out["datasets"].items()}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
