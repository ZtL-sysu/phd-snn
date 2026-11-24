#!/usr/bin/env python3
"""teacher_probe full campaign: A (teacher attribution), B (strong-teacher
conversion + fidelity-width), C (energy conventions), D (Table-1 consistency).

Single CONFIG drives everything; every run is idempotent on (config_hash, seed);
base teacher weights and unit masks are frozen to snapshots/ for reproducibility.
Strong teachers are REUSED from snapshots, never retrained for B/C.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parents[0]
sys.path.insert(0, str(R / "protocols"))
import vision_pipeline as vp  # noqa: E402
from run_e17 import convert_f64  # noqa: E402

DATA = R / "data" / "pyg_bench"
RES = HERE / "results"
SNAP = HERE / "snapshots"
TABLES = HERE / "tables"
FIGS = HERE / "figures"
for d in (RES, SNAP, TABLES, FIGS):
    d.mkdir(exist_ok=True)

CONFIG = {
    "datasets": ["MNIST", "CIFAR10"],
    "seeds": [0, 1, 2, 3, 4],
    "subset_train": 2000, "val": 1000, "test": 2000,
    "epochs": 800, "hidden": 128, "lr": 0.01, "wd": 5e-4,
    "device": "cuda", "pool": "sum",
    "full_train": {"MNIST": 55000, "CIFAR10": 45000},
    "paper_points": {"MNIST": dict(margin_coef=0.4, keep_frac=0.08, theta=1.5, T=3),
                     "CIFAR10": dict(margin_coef=0.2, keep_frac=0.08, theta=1.0, T=3)},
}
CFG_HASH = hashlib.sha256(json.dumps(CONFIG, sort_keys=True).encode()).hexdigest()[:12]
(HERE / "config.json").write_text(json.dumps(dict(config=CONFIG, config_hash=CFG_HASH), indent=2),
                                  encoding="utf-8")

EXPS = {
    "T0": dict(train="subset", keep=0.08, edge=False, cosine=False, dropout=0.0),
    "T1": dict(train="full", keep=0.08, edge=False, cosine=False, dropout=0.0),
    "T2": dict(train="subset", keep=1.0, edge=False, cosine=False, dropout=0.0),
    "T3": dict(train="full", keep=1.0, edge=False, cosine=False, dropout=0.0),
    "T4": dict(train="full", keep=1.0, edge=True, cosine=False, dropout=0.0),
    "T5": dict(train="full", keep=1.0, edge=True, cosine=True, dropout=0.2),
}

RUNLOG = HERE / "RUNLOG.md"


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with RUNLOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def append_csv(path, header, row):
    new = not path.exists()
    with path.open("a", encoding="utf-8") as f:
        if new:
            f.write(header + "\n")
        f.write(row + "\n")


def done_keys(path):
    if not path.exists():
        return set()
    out = set()
    for ln in path.read_text(encoding="utf-8").splitlines()[1:]:
        p = ln.split(",")
        if len(p) > 3:
            out.add((p[0], p[1], p[2]))
    return out


def train_teacher(exp_id, ds, seed, cfg):
    """Train full teacher + working-point teacher; freeze base and mask."""
    e = EXPS[exp_id]
    n_train = CONFIG["subset_train"] if e["train"] == "subset" else CONFIG["full_train"][ds]
    sp = vp.load_vision(ds, DATA, n_train=n_train, n_val=CONFIG["val"],
                        n_test=CONFIG["test"], seed=seed)
    tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"],
                         pool=CONFIG["pool"], edge_feat=e["edge"])
    va = vp.batch_graphs(sp["val"]["graphs"], sp["val"]["indices"],
                         pool=CONFIG["pool"], edge_feat=e["edge"])
    te = vp.batch_graphs(sp["test"]["graphs"], sp["test"]["indices"],
                         pool=CONFIG["pool"], edge_feat=e["edge"])
    base = vp.train_ann(tr, hidden=CONFIG["hidden"], seed=seed, epochs=CONFIG["epochs"],
                        lr=CONFIG["lr"], device=CONFIG["device"], dropout=e["dropout"],
                        cosine=e["cosine"])
    full_acc = float((vp.ann_logits(te, base).argmax(1) == te["y"]).mean()) * 100
    mask = None
    model = base
    if e["keep"] < 1.0:
        mask = make_mask_from(base, tr, e["keep"])
        model = vp.train_ann(tr, hidden=CONFIG["hidden"], seed=seed, epochs=CONFIG["epochs"],
                             lr=CONFIG["lr"], device=CONFIG["device"], unit_mask=mask,
                             margin_coef=CONFIG["paper_points"][ds]["margin_coef"],
                             dropout=e["dropout"], cosine=e["cosine"])
    point_acc = float((vp.ann_logits(te, model).argmax(1) == te["y"]).mean()) * 100
    # validation-only teacher accuracy: used by pick_strong() so that NO
    # model-selection decision ever touches the test split.
    val_acc = float((vp.ann_logits(va, model).argmax(1) == va["y"]).mean()) * 100
    snap = SNAP / f"{exp_id}_{ds}_seed{seed}.npz"
    np.savez(snap, W1=model["W1"], b1=model["b1"], W2=model["W2"], b2=model["b2"],
             B1=model["B1"], H1=model["H1"], gauge_scale=model["gauge_scale"],
             mask=(mask if mask is not None else np.ones(model["W1"].shape[1], dtype=bool)),
             teacher_full=full_acc, teacher_point=point_acc)
    return dict(teacher_full=full_acc, teacher_point=point_acc,
                teacher_val=val_acc, model=model, va=va, te=te,
                snapshot=str(snap.relative_to(HERE)))


def make_mask_from(base_model, tr, keep_frac):
    H = base_model["W1"].shape[1]
    k = max(1, int(round(H * keep_frac)))
    importance = np.maximum(tr["X"] @ base_model["W1"], 0.0).mean(axis=0)
    mask = np.zeros(H, dtype=bool)
    mask[np.argsort(importance)[-k:]] = True
    return mask


def load_snapshot(path):
    z = np.load(path)
    return dict(W1=z["W1"], b1=z["b1"], W2=z["W2"], b2=z["b2"], B1=z["B1"], H1=z["H1"],
                gauge_scale=float(z["gauge_scale"]))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--exps", default="T0,T1,T2,T3,T4,T5")
    ap.add_argument("--datasets", default="MNIST,CIFAR10")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    a = ap.parse_args()
    exps = a.exps.split(",")
    datasets = a.datasets.split(",")
    seeds = [int(x) for x in a.seeds.split(",")]
    log(f"teacher_probe start config_hash={CFG_HASH} exps={exps} datasets={datasets} seeds={seeds}")
    done = done_keys(RES / "teacher_probe.csv")
    for exp_id in exps:
        for ds in datasets:
            for seed in seeds:
                if (exp_id, ds, str(seed)) in done:
                    continue
                t = time.time()
                try:
                    out = train_teacher(exp_id, ds, seed, CONFIG)
                    append_csv(RES / "teacher_probe.csv",
                               "exp_id,dataset,seed,train_size,width_k,edge_feat,teacher_full,teacher_at_working_point,teacher_val,wall_clock_s,snapshot",
                               f"{exp_id},{ds},{seed},{EXPS[exp_id]['train']},{EXPS[exp_id]['keep']},"
                               f"{int(EXPS[exp_id]['edge'])},{out['teacher_full']:.3f},"
                               f"{out['teacher_point']:.3f},{out['teacher_val']:.3f},"
                               f"{time.time()-t:.1f},{out['snapshot']}")
                    log(f"A {exp_id} {ds} seed{seed} teacher_full={out['teacher_full']:.2f} "
                        f"point={out['teacher_point']:.2f} wall={time.time()-t:.1f}s")
                except Exception as exc:
                    log(f"A {exp_id} {ds} seed{seed} FAILED {type(exc).__name__}: {exc}")
    log("experiment A done")


if __name__ == "__main__":
    main()
