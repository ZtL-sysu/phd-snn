#!/usr/bin/env python3
"""f-research-v1 P3/P4 runner: baseline-first conversion comparison on
official SuperPixel graph vision datasets.

Emits one JSON per (dataset, seed) with ANN teacher, all conversion baselines,
ablations, identity diagnostics and theoretical energy accounting.
All numbers are produced by this script; nothing is hand-entered.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vision_pipeline as vp  # noqa: E402

ROOT = HERE.parent
RESULTS = ROOT / "results"
DATA = ROOT / "data" / "pyg_bench"


def method_config(method, T, theta=1.0, ours_beta="star"):
    """Frozen readout/beta policy for each compared conversion family.

    ours_beta="star"  -> the original 1028 combination (beta* = theta/2T)
    ours_beta="zero"  -> corrected combination with the redundant beta removed
                         (deterministic two-phase already realises the rate)
    Both are recorded explicitly so paired runs remain auditable.
    """
    if method == "ours":
        return dict(readout="membrane",
                    beta=theta / (2.0 * T) if ours_beta == "star" else 0.0)
    if method == "parallel":
        return dict(readout="count", beta=0.0)
    if method == "tpp":
        return dict(readout="count", beta=theta / (2.0 * T))
    if method == "qcfs":
        return dict(readout="count", beta=0.0)
    if method == "ftbc":
        return dict(readout="count", beta=None)  # calibrated on validation
    return dict(readout="count", beta=0.0)      # naive


def calibrate_ftbc_beta(val_sys, model, T, theta=1.0):
    """FTBC-style forward bias selected ONLY on the frozen validation split."""
    grid = np.linspace(-0.5 / T, 1.0 / T, 21)
    scores = []
    for b in grid:
        r = vp.convert(val_sys, model, T, theta=theta, method="ftbc",
                       readout="count", beta=float(b), seed=0)
        scores.append((r["acc"], float(b)))
    return max(scores)[1]


def run_one(dataset, seed, n_train, n_val, n_test, epochs, theta=1.0,
            device="cuda", hidden=64, lr=0.01, pool="sum", ours_beta="star"):
    t0 = time.time()
    splits = vp.load_vision(dataset, DATA, n_train=n_train, n_val=n_val,
                            n_test=n_test, seed=seed)
    systems = {}
    for split in ("train", "val", "test"):
        d = splits[split]
        systems[split] = vp.batch_graphs(d["graphs"], d["indices"], pool=pool)
    tr, va, te = systems["train"], systems["val"], systems["test"]

    model = vp.train_ann(tr, hidden=hidden, seed=seed, epochs=epochs, lr=lr,
                         device=device)
    ann_val = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean())
    ann_test = float((vp.ann_logits(te, model).argmax(1) == te["y"]).mean())

    out = dict(
        dataset=dataset, seed=seed, theta=theta, ours_beta=ours_beta,
        split_sizes={k: int(len(v["indices"])) for k, v in splits.items()},
        n_total={k: int(v["n_total"]) for k, v in splits.items()},
        graph_stats={k: dict(N=int(v["N"]), G=int(v["G"]), F=int(v["F"]),
                             C=int(v["C"]), E=int(v["E"]),
                             rho_mean=round(v["rho_mean"], 4),
                             rho_max=round(v["rho_max"], 4),
                             rho_std=round(v["rho_std"], 4))
                     for k, v in systems.items()},
        ann=dict(train_acc=model["acc"], val_acc=ann_val, test_acc=ann_test,
                 epochs=model["epochs"], hidden=hidden,
                 gauge_scale=model["gauge_scale"]),
        methods={}, ablations={}, energy={}, identity=[],
        environment=dict(python=platform.python_version(), numpy=np.__version__,
                         platform=platform.platform(), device=device, pool=pool,
                         note="Teacher trained on the selected device; CUDA sparse reduction is non-deterministic, so 5 frozen seeds with std/CI are reported"),
    )

    for T in vp.T_GRID:
        ftbc_beta = calibrate_ftbc_beta(va, model, T, theta)
        for method in vp.METHODS:
            cfg = method_config(method, T, theta, ours_beta)
            beta = ftbc_beta if method == "ftbc" else cfg["beta"]
            r = vp.convert(te, model, T, theta=theta, method=method,
                           readout=cfg["readout"], beta=beta, seed=seed,
                           return_diag=(method == "ours"))
            key = f"{method}_T{T}"
            out["methods"][key] = {k: v for k, v in r.items()
                                   if k not in ("b_hat", "b")}
            if method == "ftbc":
                out["methods"][key]["calibrated_beta"] = float(beta)
            if method == "ours":
                out["energy"][f"ours_T{T}"] = vp.energy_accounting(r, T)
                out["energy"]["ann"] = dict(macs=r["ann_macs"],
                                            energy_pj=r["ann_macs"] * vp.E_MAC_PJ)
        if T == 8:
            # ablations isolate each component of the 1028 combination
            abl = {
                "ours_no_beta": dict(method="ours", readout="membrane", beta=0.0),
                "ours_count_readout": dict(method="ours", readout="count", beta=theta / (2.0 * T)),
                "ours_tpp_phase": dict(method="tpp", readout="membrane", beta=theta / (2.0 * T)),
                "ours_naive_if": dict(method="naive", readout="membrane", beta=theta / (2.0 * T)),
            }
            for name, cfg in abl.items():
                r = vp.convert(te, model, T, theta=theta, seed=seed, **cfg)
                out["ablations"][name] = r
        out["identity"].append(vp.check_identity(te, model, T, theta=theta, seed=seed))

    out["runtime_sec"] = round(time.time() - t0, 2)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="MNIST", choices=["MNIST", "CIFAR10"])
    p.add_argument("--seeds", default="0")
    p.add_argument("--n-train", type=int, default=1000)
    p.add_argument("--n-val", type=int, default=300)
    p.add_argument("--n-test", type=int, default=500)
    p.add_argument("--epochs", type=int, default=400)
    p.add_argument("--hidden", type=int, default=64)
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--device", default="cuda")
    p.add_argument("--pool", default="sum", choices=["sum", "mean"])
    p.add_argument("--ours-beta", default="star", choices=["star", "zero"])
    p.add_argument("--tag", default="smoke")
    a = p.parse_args()
    seeds = [int(s) for s in a.seeds.split(",")]
    for s in seeds:
        rec = run_one(a.dataset, s, a.n_train, a.n_val, a.n_test, a.epochs,
                      device=a.device, hidden=a.hidden, lr=a.lr, pool=a.pool,
                      ours_beta=a.ours_beta)
        RESULTS.mkdir(parents=True, exist_ok=True)
        fn = RESULTS / f"{a.tag}_{a.dataset}_seed{s}.json"
        fn.write_text(json.dumps(rec, ensure_ascii=False, indent=2, default=float) + "\n",
                      encoding="utf-8")
        ann = rec["ann"]["test_acc"] * 100
        best = max((v["acc"] for k, v in rec["methods"].items()
                    if k.startswith("ours_T")), default=0) * 100
        en = rec["energy"].get("ours_T8", {}).get("energy_ratio_ann_over_snn", 0)
        print(f"[{fn.name}] ANN={ann:.2f}%  ours_best={best:.2f}%  "
              f"energy_ratio_ANN/SNN={en:.2f}x  "
              f"identity_max={max(x['max_abs_identity_residual'] for x in rec['identity']):.2e}  "
              f"runtime={rec['runtime_sec']}s", flush=True)


if __name__ == "__main__":
    main()
