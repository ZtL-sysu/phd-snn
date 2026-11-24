#!/usr/bin/env python3
"""Graph-structured vision conversion pipeline (f-research-v1, guidance-v2).

Method lineage (all components inherited from the 1028 manuscript, adapted here
to graph-level visual classification):
  * exact error identity   B_hat - B = R A (E1 W2)
  * closed-form bias       beta* = theta / (2T)
  * membrane-potential readout instead of spike counting
  * rho_n-weighted systematic error / neighbourhood temporal misalignment

The ONLY structural change relative to 1028 is a fixed linear global-mean
pooling matrix R between the last message-passing layer and the graph logits.
R is linear, so the identity remains EXACT (verified by check_identity below).

Datasets: official SuperPixel MNIST / CIFAR10 (GNNBenchmarkDataset,
Benchmarking GNNs, Dwivedi et al. JMLR 2023), i.e. vision datasets that
*ship as graphs* (SLIC superpixels + 8-NN weighted adjacency).

All energy figures are op-count-based THEORETICAL arithmetic-energy estimates
(45 nm CMOS: MAC 4.6 pJ, AC 0.9 pJ), NOT hardware measurements.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import scipy.sparse as sp

E_MAC_PJ = 4.6
E_AC_PJ = 0.9
T_GRID = (1, 2, 4, 8, 16)
METHODS = ("naive", "qcfs", "ftbc", "tpp", "parallel", "ours")


# ------------------------------------------------------------------ data
def _data_to_numpy(d):
    x = np.asarray(d.x.numpy() if hasattr(d.x, "numpy") else d.x, dtype=np.float32)
    ei = np.asarray(d.edge_index.numpy() if hasattr(d.edge_index, "numpy") else d.edge_index,
                    dtype=np.int64)
    if d.edge_attr is None:
        ea = np.ones(ei.shape[1], dtype=np.float32)
    else:
        ea = np.asarray(d.edge_attr.numpy() if hasattr(d.edge_attr, "numpy") else d.edge_attr,
                        dtype=np.float32).reshape(-1)
    y = int(d.y.item() if hasattr(d.y, "item") else d.y)
    pos = None
    if getattr(d, "pos", None) is not None:
        pos = np.asarray(d.pos.numpy() if hasattr(d.pos, "numpy") else d.pos, dtype=np.float32)
    return x, ei, ea, y, pos


def _normalize_features(x):
    """Scale node features into [0, 1] so an absolute threshold theta=1 is meaningful."""
    x = np.asarray(x, dtype=np.float32).copy()
    if x.ndim == 1:
        x = x[:, None]
    if x.shape[1] > 1:
        lo = x.min(axis=0, keepdims=True)
        hi = x.max(axis=0, keepdims=True)
        x = (x - lo) / np.maximum(hi - lo, 1e-6)
    else:
        x = np.clip(x, 0.0, 1.0) if x.max() <= 1.5 else x / 255.0
    return np.clip(x, 0.0, 1.0).astype(np.float32)


def batch_graphs(graphs, indices, sym_norm=True, pool="sum", edge_feat=False):
    """Concatenate a list of superpixel graphs into one block-diagonal system.

    Returns X (Ntot,F), A (Ntot,Ntot CSR), R (G,Ntot CSR), y (G,), and
    per-graph metadata. A and R are fixed, non-negative and linear, which is
    exactly the operator class the 1028 error identity requires.
    """
    Xs, rr, cc, vv, Rr, Rc, Rv, ys, sizes = [], [], [], [], [], [], [], [], []
    off = 0
    for gi, idx in enumerate(indices):
        x, ei, ea, y, pos = _data_to_numpy(graphs[int(idx)])
        x = _normalize_features(x)
        if pos is not None:
            x = np.concatenate([x, _normalize_features(pos)], axis=1).astype(np.float32)
        n = x.shape[0]
        if edge_feat:
            # per-node incident edge-weight statistics from the RAW adjacency,
            # appended as two extra feature channels (F: 3 -> 5)
            w = np.zeros(n, dtype=np.float32)
            cnt = np.zeros(n, dtype=np.float32)
            mx = np.zeros(n, dtype=np.float32)
            np.add.at(w, ei[0], ea.astype(np.float32))
            np.add.at(cnt, ei[0], 1.0)
            np.maximum.at(mx, ei[0], ea.astype(np.float32))
            x = np.concatenate([x, (w / np.maximum(cnt, 1.0))[:, None],
                                mx[:, None]], axis=1).astype(np.float32)
        Xs.append(x)
        rr.append(ei[0] + off)
        cc.append(ei[1] + off)
        vv.append(ea)
        Rr.append(np.full(n, gi, dtype=np.int64))
        Rc.append(np.arange(off, off + n, dtype=np.int64))
        # sum pooling keeps the readout linear (so the exact identity still
        # holds) while avoiding the 1/n gradient attenuation of mean pooling.
        # mean pooling remains available as a robustness variant.
        Rv.append(np.full(n, 1.0 if pool == "sum" else 1.0 / n, dtype=np.float32))
        ys.append(y)
        sizes.append(n)
        off += n
    X = np.concatenate(Xs, axis=0).astype(np.float32)
    A = sp.csr_matrix((np.concatenate(vv), (np.concatenate(rr), np.concatenate(cc))),
                      shape=(off, off), dtype=np.float32)
    A = A + sp.eye(off, dtype=np.float32, format="csr")
    A = A.maximum(A.T).tocsr()
    A.data = np.maximum(A.data, 0.0)
    if sym_norm:
        deg = np.asarray(A.sum(1)).ravel()
        dinv = np.power(np.maximum(deg, 1e-12), -0.5).astype(np.float32)
        A = (sp.diags(dinv) @ A @ sp.diags(dinv)).astype(np.float32).tocsr()
    R = sp.csr_matrix((np.concatenate(Rv), (np.concatenate(Rr), np.concatenate(Rc))),
                      shape=(len(indices), off), dtype=np.float32)
    rho = np.asarray(A.sum(1)).ravel()
    return dict(X=X, A=A, R=R, y=np.asarray(ys, dtype=np.int64), sizes=np.asarray(sizes),
                N=off, G=len(indices), F=X.shape[1], C=int(max(ys)) + 1,
                E=int(A.nnz), rho_mean=float(rho.mean()), rho_max=float(rho.max()),
                rho_std=float(rho.std()), adj_diag_mean=float(np.mean(1.0 / np.maximum(rho, 1e-9))))


def load_vision(name, root, n_train=2000, n_val=500, n_test=1000, seed=0):
    """Load official SuperPixel graphs and freeze split identities."""
    from torch_geometric.datasets import GNNBenchmarkDataset
    rng = np.random.default_rng(seed)
    out = {}
    for split, cap in (("train", n_train), ("val", n_val), ("test", n_test)):
        ds = GNNBenchmarkDataset(root=str(root), name=name, split=split)
        idx = np.arange(len(ds))
        if cap is not None and cap < len(idx):
            idx = np.sort(rng.choice(idx, size=cap, replace=False))
        out[split] = dict(graphs=ds, indices=idx, n_total=len(ds))
    return out


# ------------------------------------------------------------------ ANN teacher
def train_ann(data, hidden=64, seed=0, epochs=400, lr=0.01, wd=5e-4,
              dropout=0.0, patience=40, device="cuda", quantize_L=None,
              theta=1.0, gauge=True, sparsity=0.0, unit_mask=None,
              margin_coef=0.0, cosine=False):
    """Two-layer GCN + linear global-mean readout for graph-level classification.

    quantize_L: when set, replace ReLU with the QCFS clip-floor-shift activation
    (L quantisation levels) so the QCFS baseline trains its own source ANN.
    """
    import torch
    torch.manual_seed(seed)
    np.random.seed(seed)
    dev = torch.device(device if (device == "cpu" or torch.cuda.is_available()) else "cpu")
    X, A, R, y = data["X"], data["A"], data["R"], data["y"]
    N, F, C, G = data["N"], data["F"], data["C"], data["G"]

    coo = A.tocoo()
    idx = torch.tensor(np.vstack([coo.row, coo.col]), dtype=torch.long, device=dev)
    vals = torch.tensor(coo.data, dtype=torch.float32, device=dev)
    A_t = torch.sparse_coo_tensor(idx, vals, (N, N), device=dev).coalesce()
    rcoo = R.tocoo()
    R_t = torch.sparse_coo_tensor(
        torch.tensor(np.vstack([rcoo.row, rcoo.col]), dtype=torch.long, device=dev),
        torch.tensor(rcoo.data, dtype=torch.float32, device=dev),
        (G, N), device=dev).coalesce()
    X_t = torch.tensor(X, dtype=torch.float32, device=dev)
    Y_t = torch.tensor(y, dtype=torch.long, device=dev)

    W1 = torch.nn.Parameter(torch.empty(F, hidden, device=dev).uniform_(-1 / math.sqrt(F), 1 / math.sqrt(F)))
    b1 = torch.nn.Parameter(torch.zeros(hidden, device=dev))
    W2 = torch.nn.Parameter(torch.empty(hidden, C, device=dev).uniform_(-1 / math.sqrt(hidden), 1 / math.sqrt(hidden)))
    b2 = torch.nn.Parameter(torch.zeros(C, device=dev))
    opt = torch.optim.Adam([W1, b1, W2, b2], lr=lr, weight_decay=wd)
    mask_t = (torch.tensor(np.asarray(unit_mask, dtype=bool), dtype=torch.bool, device=dev)
              if unit_mask is not None else None)

    # frozen split: full train batch, validation is a separate graph system
    # Fixed-epoch training with NO selection on train or test. All method and
    # hyperparameter selection happens later on the frozen validation split
    # (research-recovery test-isolation rule).
    for ep in range(epochs):
        if cosine:
            lr_now = lr * 0.5 * (1.0 + math.cos(math.pi * ep / max(epochs, 1)))
            for g in opt.param_groups:
                g["lr"] = lr_now
        opt.zero_grad()
        B1 = torch.sparse.mm(A_t, X_t) @ W1 + b1
        H1 = torch.relu(B1)
        if quantize_L is not None:
            lam = max(float(H1.detach().max().item()) / quantize_L, 1e-6)
            H1 = torch.clamp(torch.floor(H1 / lam) * lam, 0.0, lam * quantize_L)
        if dropout > 0:
            H1 = torch.dropout(H1, dropout, train=True)
        Z = torch.sparse.mm(A_t, H1) @ W2
        logits = torch.sparse.mm(R_t, Z) + b2
        loss = torch.nn.functional.cross_entropy(logits, Y_t)
        if sparsity > 0:
            # 1028 WP4 sparsity penalty: layer-1 activation mass sets the
            # spike count (spikes/step = sum(relu(B1))/theta). Penalising it
            # buys energy at training time instead of by changing the readout.
            loss = loss + sparsity * torch.relu(B1).mean()
        if margin_coef > 0:
            # 1028 margin-recovery bound T = O(||a_n|| ||DW|| / Delta):
            # enlarge the ANN logit margin Delta so fewer timesteps suffice.
            rows = torch.arange(logits.shape[0], device=dev)
            rival = logits.clone()
            rival[rows, Y_t] = -1e9
            gap = logits[rows, Y_t] - rival.max(1).values
            loss = loss + margin_coef * torch.relu(1.0 - gap).mean()
        loss.backward()
        opt.step()
        if mask_t is not None:
            # 1028 unit-mask "prune and finetune": keep the surviving hidden
            # units trainable while holding all others exactly at zero, so a
            # narrow network is trained from scratch instead of a wide network
            # being amputated after training.
            with torch.no_grad():
                W1[:, ~mask_t] = 0.0
                b1[~mask_t] = 0.0
                W2[~mask_t, :] = 0.0
    with torch.no_grad():
        B1_np = (torch.sparse.mm(A_t, X_t) @ W1 + b1).cpu().numpy().astype(np.float64)
        W1_np = W1.detach().cpu().numpy().astype(np.float64)
        b1_np = b1.detach().cpu().numpy().astype(np.float64)
        W2_np = W2.detach().cpu().numpy().astype(np.float64)
        b2_np = b2.detach().cpu().numpy().astype(np.float64)
        H1_np = np.maximum(B1_np, 0.0)
        if quantize_L is not None:
            lam = max(float(H1_np.max()) / quantize_L, 1e-6)
            H1_np = np.clip(np.floor(H1_np / lam) * lam, 0.0, lam * quantize_L)
        # ReLU is positively homogeneous: divide hidden activations by `scale`
        # and multiply W2 by `scale`, leaving every ANN logit EXACTLY unchanged.
        # This is the 1028 gauge transform, and it is what puts the spiking
        # constant current inside [0, theta] so IF units actually fire
        # sparsely instead of saturating every timestep.
        scale = 1.0
        if gauge:
            hi = float(np.percentile(H1_np, 99.5))
            scale = max(hi / theta, 1e-6)
            W1_np, b1_np, B1_np = W1_np / scale, b1_np / scale, B1_np / scale
            H1_np = np.maximum(B1_np, 0.0) if quantize_L is None else H1_np / scale
            W2_np = W2_np * scale
        Z = np.asarray(A @ (H1_np @ W2_np), dtype=np.float64)
        logits = np.asarray(R @ Z, dtype=np.float64) + b2_np
        acc = float((logits.argmax(1) == y).mean())
    return dict(W1=W1_np.astype(np.float32), b1=b1_np.astype(np.float32),
                W2=W2_np.astype(np.float32), b2=b2_np.astype(np.float32),
                B1=B1_np.astype(np.float32), H1=H1_np.astype(np.float32),
                acc=acc, epochs=ep + 1, seed=seed, hidden=hidden,
                quantize_L=quantize_L, gauge_scale=float(scale))


def hidden_activation(data, model):
    """Hidden activation recomputed for THIS graph system (never reuse train H1)."""
    B1 = np.asarray(data["A"] @ (data["X"] @ model["W1"]), dtype=np.float32) + model["b1"]
    return B1, np.maximum(B1, 0.0).astype(np.float32)


def ann_logits(data, model):
    _, H1 = hidden_activation(data, model)
    Z = np.asarray(data["A"] @ (H1 @ model["W2"]), dtype=np.float32)
    return np.asarray(data["R"] @ Z, dtype=np.float32) + model["b2"]


# ------------------------------------------------------------------ SNN conversion
def _spike_train(inst1, T, theta, method, beta, rng):
    """Return the per-step hidden-layer spike trains and total spike count."""
    N, H = inst1.shape
    if method == "tpp":
        u = np.zeros((N, H), dtype=np.float32)
        trains = []
        for _ in range(T):
            u = u + inst1 + np.float32(beta)
            p = np.clip(u, 0.0, theta) / theta
            s = (rng.random(u.shape) < p).astype(np.float32)
            u -= s * theta
            trains.append(s)
        return trains
    if method in ("ours", "parallel"):
        # deterministic two-phase: cache the total count, then diffuse the
        # temporal error with round(t n / T) - round((t-1) n / T)
        # A physical IF unit emits at most ONE spike per timestep, so the
        # total count n must be clipped to T. Without this clip the two-phase
        # schedule invents multi-spike steps and inflates the energy bill.
        n = np.clip(np.rint(np.clip(inst1 + beta, 0.0, None) * T / theta), 0.0, float(T))
        trains = []
        for t in range(1, T + 1):
            s = np.rint(t * n / T) - np.rint((t - 1) * n / T)
            trains.append(s.astype(np.float32))
        return trains
    if method == "qcfs":
        # clip-floor-shift style quantised rate: L = T levels, count decoding
        lam = theta / max(T, 1)
        levels = np.clip(np.floor(np.clip(inst1, 0.0, None) / lam), 0, T)
        trains = []
        for t in range(1, T + 1):
            trains.append((levels >= t).astype(np.float32))
        return trains
    # naive / ftbc: deterministic integrate-and-fire with subtractive reset
    u = np.zeros((N, H), dtype=np.float32)
    trains = []
    for _ in range(T):
        u = u + inst1 + np.float32(beta)
        s = (u >= theta).astype(np.float32)
        u -= s * theta
        trains.append(s)
    return trains


def convert(data, model, T, theta=1.0, method="ours", readout="membrane",
            beta=None, seed=0, return_diag=False):
    """Simulate T spiking timesteps for one of the conversion baselines."""
    rng = np.random.default_rng(seed)
    A, R, W2, b2 = data["A"], data["R"], model["W2"], model["b2"]
    B1, H1 = hidden_activation(data, model)
    inst1 = B1.astype(np.float32)
    if beta is None:
        beta = theta / (2.0 * T) if method == "ours" else 0.0
    trains = _spike_train(inst1, T, theta, method, beta, rng)
    mem = np.zeros((data["G"], data["C"]), dtype=np.float64)
    cnt_out = np.zeros((data["G"], data["C"]), dtype=np.float32)
    u_out = np.zeros((data["G"], data["C"]), dtype=np.float64)
    hidden_spikes = 0.0
    ac_ops = 0.0
    deg_mean = data["E"] / max(data["N"], 1)
    for s in trains:
        Z = np.asarray(A @ (s.astype(np.float32) @ W2), dtype=np.float32)
        out_t = np.asarray(R @ Z, dtype=np.float32) + b2
        mem += out_t
        u_out += out_t
        fired = (u_out >= theta)
        cnt_out += fired
        u_out -= fired * theta
        ns = float(s.sum())
        hidden_spikes += ns
        ac_ops += ns * W2.shape[0] + ns * deg_mean * W2.shape[1]
    B = ann_logits(data, model)
    B_hat = mem / float(T)
    pred = B_hat.argmax(1) if readout == "membrane" else cnt_out.argmax(1)
    acc = float((pred == data["y"]).mean())
    out = dict(acc=acc, conversion_loss_pp=float((B.argmax(1) == data["y"]).mean() * 100.0 - acc * 100.0),
               T=int(T), method=method, readout=readout, beta=float(beta),
               hidden_spikes=float(hidden_spikes),
               output_spikes=float(cnt_out.sum()),
               total_spikes=float(hidden_spikes + cnt_out.sum()),
               ac_ops=float(ac_ops),
               ann_macs=float(_ann_macs(data, model)),
               G=int(data["G"]), identity_residual=None)
    if return_diag:
        E1 = np.asarray(np.sum(trains, axis=0) / float(T), dtype=np.float32) - H1
        rhs = np.asarray(R @ (np.asarray(A @ (E1 @ W2), dtype=np.float32)), dtype=np.float32)
        out["identity_residual"] = float(np.max(np.abs(B_hat - B - rhs)))
        out["argmax_agreement"] = float((B_hat.argmax(1) == B.argmax(1)).mean())
        out["sum_n_hit_rate"] = float(np.mean(
            np.sum(trains, axis=0) == np.clip(
                np.rint(np.clip(inst1 + beta, 0.0, None) * T / theta), 0.0, float(T)))) \
            if method in ("ours", "parallel") else None
        out["b_hat"] = B_hat
        out["b"] = B
    return out


def _ann_macs(data, model):
    """Exact dense-equivalent MAC count of one ANN forward pass (all graphs)."""
    N, F, H, C, E = data["N"], data["F"], model["W1"].shape[1], data["C"], data["E"]
    return (E * F + N * F * H + E * H + N * H * C + N * C)


def energy_accounting(result, T):
    """45 nm theoretical arithmetic energy; ANN MAC vs SNN AC (NOT hardware J)."""
    ann_pj = result["ann_macs"] * E_MAC_PJ
    snn_pj = result["ac_ops"] * E_AC_PJ
    # A zero-spike network is degenerate, not energy-efficient: its accuracy
    # collapses to chance. Never report a near-infinite ratio as an advantage.
    degenerate = (result.get("total_spikes", 1) <= 0) or (result["ac_ops"] <= 1e-9)
    ratio = 0.0 if degenerate else float(ann_pj / max(snn_pj, 1e-12))
    return dict(ann_macs=float(result["ann_macs"]), snn_ac_ops=float(result["ac_ops"]),
                ann_energy_pj=float(ann_pj), snn_energy_pj=float(snn_pj),
                energy_ratio_ann_over_snn=ratio,
                zero_spike_degenerate=bool(degenerate),
                ann_energy_per_graph_pj=float(ann_pj / max(result["G"], 1)),
                model="45 nm CMOS theoretical arithmetic energy; MAC=4.6 pJ, AC=0.9 pJ; NOT a hardware measurement")


def check_identity(data, model, T, theta=1.0, seed=0):
    r = convert(data, model, T, theta=theta, method="ours", readout="membrane",
                seed=seed, return_diag=True)
    return dict(T=T, max_abs_identity_residual=r["identity_residual"],
                argmax_agreement=r["argmax_agreement"],
                sum_n_hit_rate=r["sum_n_hit_rate"])


def summarize(vals):
    a = np.asarray(vals, dtype=float)
    return dict(mean=float(a.mean()), std=float(a.std(ddof=0)), n=int(a.size),
                ci95_half=float(1.96 * a.std(ddof=0) / math.sqrt(max(a.size, 1))))
