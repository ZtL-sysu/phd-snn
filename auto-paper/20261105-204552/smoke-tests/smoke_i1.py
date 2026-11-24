"""Round-1 smoke test for I1: connectome topology x spiking dynamics interaction.

NOT a paper experiment. Fixed graph weights, trainable linear readout only,
short runs, one seed. Purpose: decide whether to keep or drop the idea.

Usage (run inside the dyg-cold conda env):
    python smoke_i1.py --data <dir with connections.csv> --stim <shapes dir> --steps 40
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from scipy.sparse import coo_matrix

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def find_any(dirpath: Path, names) -> Path:
    for name in names:
        hits = list(dirpath.rglob(name))
        if hits:
            return max(hits, key=lambda p: p.stat().st_size)
    raise FileNotFoundError(f"none of {names} found under {dirpath}")


def read_table(path: Path, **kw):
    sep = "\t" if ".tsv" in path.name else ","
    return pd.read_csv(path, sep=sep, **kw)


def load_images(stim_dir: Path, size: int = 32, limit: int = 120, seed: int = 0):
    xs, ys = [], []
    root = stim_dir
    for split in ("train", "test"):
        for ci, cname in enumerate(sorted([d.name for d in (root / split).iterdir() if d.is_dir()])):
            files = sorted((root / split / cname).glob("*.png"))[: limit // 2]
            for f in files:
                im = Image.open(f).convert("L").resize((size, size))
                # invert: cogstim uses a white background, ink must be the sparse signal
                xs.append(1.0 - np.asarray(im, dtype=np.float32) / 255.0)
                ys.append(ci)
    p = np.random.default_rng(seed).permutation(len(ys))
    return np.stack(xs)[p], np.array(ys, dtype=np.int64)[p]


def build_graph(data_dir: Path, device: torch.device, shuffle: bool, seed: int = 0):
    conn = read_table(find_any(data_dir, ["connections.csv", "connections_biological.csv.gz"]))
    cols = {c.lower(): c for c in conn.columns}
    pre, post, w = cols["pre_root_id"], cols["post_root_id"], cols["syn_count"]
    conn[pre] = conn[pre].astype(str)
    conn[post] = conn[post].astype(str)
    ids = pd.Index(pd.concat([conn[pre], conn[post]], ignore_index=True).unique())
    mapper = pd.Series(np.arange(len(ids), dtype=np.int64), index=ids)
    src = mapper.loc[conn[pre]].to_numpy()
    dst = mapper.loc[conn[post]].to_numpy()
    val = np.log1p(conn[w].to_numpy(dtype=np.float32))
    val = val / max(float(np.percentile(val, 95)), 1e-6)
    if shuffle:
        rng = np.random.default_rng(seed)
        dst = rng.permutation(dst)  # preserves in-degree statistics, destroys motifs
    n = len(ids)
    A = coo_matrix((val.astype(np.float32), (dst, src)), shape=(n, n)).tocsr()
    A.sum_duplicates()
    A.eliminate_zeros()
    # row-normalise so each postsynaptic neuron receives a weighted average (numerically stable)
    rs = np.asarray(A.sum(axis=1)).ravel()
    rs[rs == 0] = 1.0
    A = A.multiply((1.0 / rs)[:, None]).tocsr()
    A.eliminate_zeros()
    # torch sparse CSR: A[post, pre] @ x[pre] -> message into post
    A_t = torch.sparse_csr_tensor(
        torch.from_numpy(A.indptr.astype(np.int64)).to(device),
        torch.from_numpy(A.indices.astype(np.int64)).to(device),
        torch.from_numpy(A.data).to(device),
        size=(n, n),
        dtype=torch.float32,
        device=device,
    )
    info = {"nodes": n, "nnz": int(A.nnz), "shuffled": shuffle}

    # input nodes = photoreceptors, readout nodes = Kenyon cells (from annotations)
    try:
        cls = read_table(find_any(data_dir, ["classification.csv", "neuron_annotations_flywire_v2.1.0.tsv.gz"]))
        cc = {c.lower(): c for c in cls.columns}
        rid, ctype = cc["root_id"], cc["cell_type"]
        cls[rid] = cls[rid].astype(str)
        photo = cls[cls[ctype].astype(str).str.upper().str.startswith(("R1-6", "R7", "R8"), na=False)]
        photo_ids = [x for x in photo[rid].unique() if x in mapper.index]
        kc = cls[cls[ctype].astype(str).str.upper().str.startswith(("KC", "KENYON"), na=False)]
        kc_ids = [x for x in kc[rid].unique() if x in mapper.index]
    except Exception:
        photo_ids, kc_ids = [], []
    info["n_photoreceptor_nodes"] = len(photo_ids)
    info["n_kenyon_nodes"] = len(kc_ids)
    if not photo_ids:
        photo_ids = list(ids[:256])
    if not kc_ids:
        kc_ids = list(ids[-256:])
    pidx = torch.tensor(mapper.loc[[x for x in photo_ids if x in mapper.index]].to_numpy(), device=device, dtype=torch.long)
    kidx = torch.tensor(mapper.loc[[x for x in kc_ids if x in mapper.index]].to_numpy(), device=device, dtype=torch.long)
    return A_t, pidx, kidx, info


def encode(images: np.ndarray, pidx: torch.Tensor, device: torch.device):
    # simple deterministic retinal projection: flatten image -> interpolate onto photoreceptor nodes
    flat = torch.tensor(images.reshape(len(images), -1), dtype=torch.float32, device=device)
    n_p = pidx.numel()
    idx = torch.linspace(0, flat.shape[1] - 1, n_p, device=device).long()
    return flat[:, idx].t().contiguous()  # [n_p, B]


def forward(A, pidx, kidx, inp, dynamics, T=8, K=3, decay=0.6, thresh=0.7):
    n, B = A.shape[0], inp.shape[1]
    dev = inp.device
    x = torch.zeros(n, B, device=dev)
    x.index_copy_(0, pidx, 0.5 * inp)
    I_in = torch.zeros(n, B, device=dev)
    I_in.index_copy_(0, pidx, 0.5 * inp)
    total_spikes = 0.0
    if dynamics == "stateless":
        for _ in range(K):
            x = torch.tanh(torch.sparse.mm(A, x))
        feat = x.index_select(0, kidx).mean(0)  # [B]
        return feat.unsqueeze(1), 0.0
    # LIF with soft reset, membrane state carried across T steps
    v = torch.zeros(n, B, device=dev)
    acc = torch.zeros(n, B, device=dev)
    for t in range(T):
        I = torch.sparse.mm(A, x) + I_in
        v = decay * v + I
        s = (v >= thresh).float()
        total_spikes += float(s.sum().item())
        v = v - thresh * s
        x = s
        acc = acc + x
    feat = acc.index_select(0, kidx).mean(0) / T
    return feat.unsqueeze(1), total_spikes / (n * B * T)


def run_condition(A, pidx, kidx, imgs, labels, dynamics, steps, device, seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    n_tr = int(len(labels) * 0.75)
    head = torch.nn.Linear(1, 2).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=1e-2)
    lossf = torch.nn.CrossEntropyLoss()
    torch.cuda.reset_peak_memory_stats() if device.type == "cuda" else None
    t0 = time.time()
    losses, spike_rate = [], 0.0
    B = 16
    for step in range(steps):
        sel = torch.randint(0, n_tr, (B,), device=device)
        xb = torch.tensor(imgs[sel.cpu().numpy()], dtype=torch.float32)
        yb = torch.tensor(labels[sel.cpu().numpy()], dtype=torch.long, device=device)
        inp = encode(xb.numpy(), pidx, device)
        feat, sr = forward(A, pidx, kidx, inp, dynamics)
        spike_rate = sr
        loss = lossf(head(feat), yb)
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(float(loss.item()))
    elapsed = time.time() - t0
    with torch.no_grad():
        inp_te = encode(imgs[n_tr:], pidx, device)
        feat_te, _ = forward(A, pidx, kidx, inp_te, dynamics)
        pred = head(feat_te).argmax(1).cpu().numpy()
        acc = float((pred == labels[n_tr:]).mean())
    peak = torch.cuda.max_memory_allocated() / 1e6 if device.type == "cuda" else 0.0
    return {"dynamics": dynamics, "loss_first": round(losses[0], 4), "loss_last": round(losses[-1], 4),
            "test_acc": round(acc, 4), "spike_rate": round(spike_rate, 6),
            "peak_gpu_MB": round(peak, 1), "seconds": round(elapsed, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT.parent / "data" / "flywire_graph"))
    ap.add_argument("--stim", default=str(ROOT / "stimuli" / "shapes"))
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    result = {"device": str(device), "torch": torch.__version__, "steps": args.steps, "seed": args.seed,
              "disclaimer": "single-seed fixed-weight short smoke run; NOT a paper result"}
    imgs, labels = load_images(Path(args.stim), seed=args.seed)
    result["n_images"] = int(len(labels))
    conds = []
    for graph in ("biological", "shuffled"):
        A, pidx, kidx, info = build_graph(Path(args.data), device, shuffle=(graph == "shuffled"), seed=args.seed)
        result.setdefault("graph_info", {})[graph] = info
        for dyn in ("stateless", "lif"):
            r = run_condition(A, pidx, kidx, imgs, labels, dyn, args.steps, device, args.seed)
            r["graph"] = graph
            conds.append(r)
            print(f"[{graph:10s} {dyn:9s}] loss {r['loss_first']}->{r['loss_last']} "
                  f"acc={r['test_acc']} spike={r['spike_rate']} peak={r['peak_gpu_MB']}MB {r['seconds']}s", flush=True)
        del A
        torch.cuda.empty_cache()
    def get(g, d):
        return next(c for c in conds if c["graph"] == g and c["dynamics"] == d)
    interaction = ((get("biological", "lif")["test_acc"] - get("biological", "stateless")["test_acc"])
                   - (get("shuffled", "lif")["test_acc"] - get("shuffled", "stateless")["test_acc"]))
    result["conditions"] = conds
    result["interaction_acc"] = round(float(interaction), 4)
    result["failure_signals"] = {
        "oom_or_too_slow": any(c["seconds"] > 600 for c in conds),
        "no_learnable_signal": all(c["test_acc"] <= 0.55 for c in conds),
        "no_interaction": abs(float(interaction)) < 0.02 or interaction <= 0,
    }
    result["verdict"] = "KEEP" if not any(result["failure_signals"].values()) else "DROP_OR_REVISE"
    p = OUT / "smoke_i1.json"
    p.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("SMOKE_I1_RESULT=" + json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
