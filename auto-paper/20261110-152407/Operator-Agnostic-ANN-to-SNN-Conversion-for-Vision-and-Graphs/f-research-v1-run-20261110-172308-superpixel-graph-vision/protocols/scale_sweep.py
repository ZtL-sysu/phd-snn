#!/usr/bin/env python3
"""Zero-cost correction candidate: sweep the post-training gauge scale.

ReLU positive homogeneity means W1/s, b1/s, W2*s leaves every ANN logit
EXACTLY unchanged while changing the spiking constant current. So we can find
a better operating point without retraining. Combined with theta, this may
push the 1.5pp band down to T<=8 (frozen accuracy target).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vision_pipeline as vp  # noqa: E402

R = HERE.parent
DATA = R / "data" / "pyg_bench"


def rescale(model, s):
    m = dict(model)
    m["W1"] = model["W1"] / s
    m["b1"] = model["b1"] / s
    m["W2"] = model["W2"] * s
    m["B1"] = model["B1"] / s
    m["H1"] = model["H1"] / s
    return m


def main():
    splits = vp.load_vision("MNIST", DATA, n_train=2000, n_val=500, n_test=500, seed=0)
    tr = vp.batch_graphs(splits["train"]["graphs"], splits["train"]["indices"], pool="sum")
    te = vp.batch_graphs(splits["test"]["graphs"], splits["test"]["indices"], pool="sum")
    model = vp.train_ann(tr, hidden=128, seed=0, epochs=800, lr=0.01, device="cuda")
    base_logits = vp.ann_logits(te, model)
    ann = float((base_logits.argmax(1) == te["y"]).mean()) * 100
    print(f"ANN {ann:.2f}% gauge {model['gauge_scale']:.4f}", flush=True)

    rows = []
    for s in (0.5, 1.0, 2.0, 4.0, 8.0):
        m = rescale(model, s)
        drift = float(np.max(np.abs(vp.ann_logits(te, m) - base_logits)))
        for theta in (0.5, 1.0, 2.0):
            for T in (4, 8):
                r = vp.convert(te, m, T, theta=theta, method="ours",
                               readout="membrane", beta=0.0, seed=0)
                e = vp.energy_accounting(r, T)
                rows.append(dict(scale=s, theta=theta, T=T,
                                 acc=round(r["acc"] * 100, 3),
                                 loss_pp=round(ann - r["acc"] * 100, 3),
                                 energy=round(e["energy_ratio_ann_over_snn"], 3),
                                 spikes=int(r["total_spikes"]),
                                 ann_logit_drift=round(drift, 8)))
    strong = [x for x in rows if x["loss_pp"] <= 1.5]
    strong.sort(key=lambda x: (-x["energy"], x["T"]))
    out = dict(note="single-seed local CUDA diagnostic, NOT formal result",
               ann=ann, rows=rows, within_1_5pp=strong,
               best_by_loss=sorted(rows, key=lambda x: x["loss_pp"])[:6])
    (R / "results" / "scale_sweep.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("MAX ANN LOGIT DRIFT", max(x["ann_logit_drift"] for x in rows), flush=True)
    print("BEST LOSS", json.dumps(out["best_by_loss"], ensure_ascii=False), flush=True)
    print("WITHIN 1.5pp", json.dumps(strong[:8], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
