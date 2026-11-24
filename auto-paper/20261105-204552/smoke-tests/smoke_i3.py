"""Round-1 smoke test for I3: connectome-measured Voronoi eye geometry vs regular grid.

NOT a paper experiment. One seed, short run, shared downstream readout.
Purpose: falsify "photoreceptor geometry helps under an equal spike budget".

Usage: python smoke_i3.py --data <dir with right_visual_positions_all_neurons.csv> --stim <shapes dir>
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def find(dirpath: Path, name: str) -> Path:
    hits = list(dirpath.rglob(name))
    if not hits:
        raise FileNotFoundError(f"{name} not found under {dirpath}")
    return max(hits, key=lambda p: p.stat().st_size)


def load_images(stim_dir: Path, size: int = 64, limit: int = 120, seed: int = 0):
    xs, ys = [], []
    for split in ("train", "test"):
        for ci, cname in enumerate(sorted([d.name for d in (stim_dir / split).iterdir() if d.is_dir()])):
            for f in sorted((stim_dir / split / cname).glob("*.png"))[: limit // 2]:
                # invert: white background -> sparse ink signal
                xs.append(1.0 - np.asarray(Image.open(f).convert("L").resize((size, size)), dtype=np.float32) / 255.0)
                ys.append(ci)
    p = np.random.default_rng(seed).permutation(len(ys))
    return np.stack(xs)[p], np.array(ys, dtype=np.int64)[p]


def load_seeds(data_dir: Path, max_seeds: int = 400):
    df = pd.read_csv(find(data_dir, "right_visual_positions_all_neurons.csv"))
    # prefer the projected eye-plane coordinates; raw x/y are 3D voxel coordinates
    xc = "x_axis" if "x_axis" in df.columns else next(c for c in df.columns if c.lower() == "x")
    yc = "y_axis" if "y_axis" in df.columns else next(c for c in df.columns if c.lower() == "y")
    tcol = next((c for c in df.columns if "type" in c.lower() or "cell" in c.lower()), None)
    sub = df
    if tcol is not None:
        r7 = df[df[tcol].astype(str).str.upper().str.startswith("R7", na=False)]
        if len(r7) >= 50:
            sub = r7
    xy = sub[[xc, yc]].to_numpy(dtype=np.float64)
    xy = xy[np.isfinite(xy).all(1)]
    if len(xy) > max_seeds:
        idx = np.linspace(0, len(xy) - 1, max_seeds).astype(int)
        xy = xy[idx]
    lo, hi = xy.min(0), xy.max(0)
    xy = (xy - lo) / np.maximum(hi - lo, 1e-9)
    return xy, {"columns": list(df.columns), "x_col": xc, "y_col": yc, "type_col": tcol,
                "n_seeds_used": int(len(xy)), "n_rows": int(len(df))}


def voronoi_encode(images, seeds, size):
    # assign every pixel to its nearest measured photoreceptor seed
    yy, xx = np.mgrid[0:size, 0:size]
    pixels = np.stack([xx.ravel() / (size - 1), yy.ravel() / (size - 1)], axis=1)
    tree = cKDTree(seeds)
    _, lab = tree.query(pixels, k=1)
    n = len(seeds)
    out = np.zeros((len(images), n), dtype=np.float32)
    for i, im in enumerate(images):
        sums = np.bincount(lab, weights=im.ravel(), minlength=n)
        cnt = np.bincount(lab, minlength=n)
        out[i] = sums / np.maximum(cnt, 1)
    return out


def grid_encode(images, n, size):
    k = int(np.ceil(np.sqrt(n)))
    imgs = torch.tensor(images).unsqueeze(1).float()
    pooled = torch.nn.functional.adaptive_avg_pool2d(imgs, (k, k)).numpy().reshape(len(images), -1)
    if pooled.shape[1] >= n:
        return pooled[:, :n].astype(np.float32)
    return np.pad(pooled, ((0, 0), (0, n - pooled.shape[1])), mode="edge").astype(np.float32)


def run_encoder(feats, labels, steps, device, seed, rate_scale, T=8):
    torch.manual_seed(seed); np.random.seed(seed)
    n = feats.shape[1]
    n_tr = int(len(labels) * 0.75)
    W1 = torch.nn.Linear(n, 64, bias=False).to(device)
    W2 = torch.nn.Linear(64, 2).to(device)
    opt = torch.optim.Adam(list(W1.parameters()) + list(W2.parameters()), lr=1e-2)
    lossf = torch.nn.CrossEntropyLoss()
    torch.cuda.reset_peak_memory_stats() if device.type == "cuda" else None
    t0 = time.time(); losses = []
    B = 16
    total_spikes = 0
    for step in range(steps):
        sel = np.random.randint(0, n_tr, B)
        s = torch.tensor(feats[sel], device=device)
        y = torch.tensor(labels[sel], device=device, dtype=torch.long)
        v = torch.zeros(B, 64, device=device); acc = torch.zeros(B, 64, device=device)
        for t in range(T):
            spike = (torch.rand_like(s) < s * rate_scale).float()
            total_spikes += float(spike.sum().item())
            v = 0.8 * v + spike @ W1.weight.t()
            acc = acc + torch.sigmoid(v - 0.5)  # differentiable surrogate of spike count
        logits = W2(acc / T)
        loss = lossf(logits, y)
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(float(loss.item()))
    with torch.no_grad():
        s = torch.tensor(feats[n_tr:], device=device)
        v = torch.zeros(len(s), 64, device=device); acc = torch.zeros(len(s), 64, device=device)
        for t in range(T):
            spike = (torch.rand_like(s) < s * rate_scale).float()
            v = 0.8 * v + spike @ W1.weight.t()
            acc = acc + torch.sigmoid(v - 0.5)
        pred = W2(acc / T).argmax(1).cpu().numpy()
        test_acc = float((pred == labels[n_tr:]).mean())
    peak = torch.cuda.max_memory_allocated() / 1e6 if device.type == "cuda" else 0.0
    return {"loss_first": round(losses[0], 4), "loss_last": round(losses[-1], 4),
            "test_acc": round(test_acc, 4), "mean_input_spike_rate": round(total_spikes / (steps * B * n * T), 6),
            "peak_gpu_MB": round(peak, 1), "seconds": round(time.time() - t0, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT.parent / "data" / "flywire_graph"))
    ap.add_argument("--stim", default=str(ROOT / "stimuli" / "shapes"))
    ap.add_argument("--steps", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    result = {"device": str(device), "steps": args.steps, "seed": args.seed,
              "disclaimer": "single-seed short smoke run; NOT a paper result"}
    seeds, meta = load_seeds(Path(args.data))
    result["seed_info"] = meta
    imgs, labels = load_images(Path(args.stim), seed=args.seed)
    n = len(seeds)
    fv = voronoi_encode(imgs, seeds, imgs.shape[1])
    fg = grid_encode(imgs, n, imgs.shape[1])
    result["feature_dim"] = n
    result["mean_input_intensity"] = {"voronoi": round(float(fv.mean()), 4), "grid": round(float(fg.mean()), 4)}
    # equalize spike budget: both encoders target the same mean input spike rate
    target_rate = 0.20
    scale_v = min(5.0, target_rate / max(float(fv.mean()), 1e-6))
    scale_g = min(5.0, target_rate / max(float(fg.mean()), 1e-6))
    result["target_input_spike_rate"] = target_rate
    result["rate_scale"] = {"voronoi": round(scale_v, 4), "grid": round(scale_g, 4)}
    r = {}
    r["voronoi"] = run_encoder(fv, labels, args.steps, device, args.seed, scale_v)
    r["grid"] = run_encoder(fg, labels, args.steps, device, args.seed, scale_g)
    result["conditions"] = r
    delta = r["voronoi"]["test_acc"] - r["grid"]["test_acc"]
    result["delta_acc_voronoi_minus_grid"] = round(float(delta), 4)
    result["failure_signals"] = {
        "no_geometry_gain": delta < 0.02,
        "no_learnable_signal": max(r["voronoi"]["test_acc"], r["grid"]["test_acc"]) <= 0.55,
        "too_slow": max(r["voronoi"]["seconds"], r["grid"]["seconds"]) > 600,
    }
    result["verdict"] = "KEEP" if not any(result["failure_signals"].values()) else "DROP_OR_REVISE"
    (OUT / "smoke_i3.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("SMOKE_I3_RESULT=" + json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
