#!/usr/bin/env python3
"""Pre-flight diagnostic for the C3 predictor on graphs whose models already exist.

Runs BEFORE stage c3 and never touches held-out results. Its only purpose is to check that the
pre-registered predictor form (T ~ c*kappa) is identifiable; if it is not, the predictor is
repaired in a versioned pre-registration before c3 executes. No target is changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import run_campaign as rc  # noqa: E402
import snn_probe  # noqa: E402

EPS = 1.5
TGRID = [2, 4, 8, 16, 32]


def main():
    rows = []
    for name in ["cora", "citeseer", "pubmed", "chameleon"]:
        data = rc.make_data(name, "H3_sym")
        for seed in range(7):
            loaded, _ = rc.load_model(name, "H3_sym", seed)
            if loaded is None:
                continue
            model, _ = loaded
            diag = snn_probe.ann_diagnostics(data, model)
            gaps = {}
            for T in TGRID:
                r = snn_probe.simulate_l2(data, model, T, bias=True, neuron="if",
                                          perm_seed=seed)
                gaps[T] = (diag["ann_acc"] - r["acc"]) * 100
            valid = [T for T in TGRID if gaps[T] <= EPS]
            rows.append(dict(graph=name, seed=seed, kappa=diag["kappa"],
                             ann=diag["ann_acc"], T_min=min(valid) if valid else None,
                             gaps={str(k): round(v, 3) for k, v in gaps.items()}))
            print("%s s%d kappa=%.3f gaps=%s Tmin=%s"
                  % (name, seed, diag["kappa"],
                     [round(gaps[T], 2) for T in TGRID],
                     min(valid) if valid else None), flush=True)
    good = [r for r in rows if r["T_min"] is not None]
    print("\nusable rows:", len(good), "/", len(rows))
    if len(good) >= 3:
        k = np.array([r["kappa"] for r in good])
        t = np.array([r["T_min"] for r in good], float)
        c = float(np.median(t / k))
        pred = np.array([min([T for T in TGRID if T >= max(1, np.ceil(c * x))])
                         for x in k])
        hit = np.mean(np.abs(np.log2(pred / t)) <= 1.0)
        print("c=%.6g  pearson r=%.3f  median|log2 err|=%.3f  hit(<=1 step)=%.3f"
              % (c, np.corrcoef(k, t)[0, 1], np.median(np.abs(np.log2(pred / t))), hit))
        print("kappa range %.2f..%.2f ; T_min values %s" % (k.min(), k.max(), sorted(set(t))))
    (ROOT / "results" / "c3_prediagnostic.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
