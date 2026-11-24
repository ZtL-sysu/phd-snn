#!/usr/bin/env python3
"""Shared experimental core for WP1/WP3/WP4/WP5/WP6.

Why a new module instead of extending `protocols/snn_gnn_experiment.py`: that file hard-codes
a two-layer GCN (W1, W2 as separate variables). WP3 needs L layers, WP4 needs a sparsity
penalty, WP5 needs multi-view averaging -- all three are structural, not parametric. Rather
than fork four copies, everything here is written once around a *layer list*, and the
two-layer case is recovered exactly when L=2, alpha=0.

VERIFIED, not assumed: with L=2, alpha=0, CPU, 7 seeds, this module reproduces the shipped
numbers to 0.000-0.003 pp on Cora and PubMed (`experiments/wp0_reproduce.py`, gate PASS).
That is what licenses using it for everything downstream.

Model
-----
    H_0     = relu(A_hat @ X @ M_0 + b_0)                     # layer 1
    Z_l     = (1-alpha) A_hat @ H_{l-1} + alpha H_0           # l = 1 .. L-2
    H_l     = relu(Z_l @ M_l + b_l)
    logits  = A_hat @ H_{L-2} @ M_{L-1} + b_out

alpha = 0 is a plain GCN. alpha > 0 is GCNII's initial residual, with H_0 (not X) as the
residual source, which is what GCNII actually does: the first layer already maps F -> hidden,
so X cannot be added to a hidden-width tensor.

Identity (the thing every claim rests on)
----------------------------------------
    B_hat_l - B_l = (1 - alpha) * A_hat @ (E_{l-1} @ M_l),     E_l = count_l/T - relu(B_l)

with E_0 = 0, so the l=1 error is identically zero and depth enters only through the
product of per-layer gains. `check_identity` verifies this numerically for any L.

Design notes
------------
* ANN training is PyTorch on **CPU by default**. Measured: CUDA moves the PubMed ANN by
  +0.69 pp (7 seeds) because sparse-matrix reduction order on the GPU is not fixed and early
  stopping then lands on a different epoch. That is larger than the effect sizes reported
  here, so the frozen protocol trains on CPU; CUDA is opt-in for sweeps that record a
  device-pair noise measurement.
* Spiking simulation is NumPy: the T-step loop is dominated by Python/kernel-launch overhead,
  and on a 2.7k-node graph GPU gives no gain for it.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "protocols"))

import graph_data  # noqa: E402


# ------------------------------------------------------------------ data
def load(name: str, root: str | None = None) -> dict:
    """Load a dataset and return everything the experiments need, adjacency pre-normalised."""
    root = root or str(ROOT / "results" / ".data")
    d = graph_data.load_ds(name, root)
    adj = sp.csr_matrix(d["adj"], dtype=np.float32)
    deg = np.asarray(adj.sum(1)).ravel()
    dinv = np.power(np.maximum(deg, 1e-12), -0.5).astype(np.float32)
    norm = (sp.diags(dinv) @ adj @ sp.diags(dinv)).astype(np.float32).tocsr()
    X = np.asarray(d["features"], dtype=np.float32).copy()
    if d.get("row_normalize"):
        rs = X.sum(1)
        rs[rs == 0] = 1.0
        X = X / rs[:, None]
    labels = np.asarray(d["labels"], dtype=np.int64)
    return dict(name=name, X=X, y=labels, adj=norm,
                train=np.asarray(d["train_mask"], bool),
                val=np.asarray(d["val_mask"], bool),
                test=np.asarray(d["test_mask"], bool),
                N=int(X.shape[0]), F=int(X.shape[1]), C=int(labels.max()) + 1,
                E=int((adj.nnz - adj.shape[0]) // 2))


# ------------------------------------------------------------------ ANN
def train_ann(data, hidden=16, n_layers=2, seed=0, alpha=0.0, beta_idm=0.0,
              epochs=400, lr=0.01, wd=5e-4, dropout=0.5, patience=30,
              device="cpu", sparsity=0.0, sparsity_layer=0, val_mode="dropout",
              spec_norm=False, unit_mask=None) -> dict:
    """Train an L-layer GCN (or GCNII-style initial-residual variant).

    Model-changing parameters (not optimiser knobs):
      n_layers : L. L=2 with alpha=0 is exactly the shipped model.
      alpha    : initial-residual weight. alpha=0 disables it. Applies to layers 1..L-2.
      beta_idm : identity mapping, M_l = (1-beta) I + beta W_l on square matrices only.
      sparsity : coefficient on mean(relu(B_{sparsity_layer})). The WP4 knob: layer-1
                 activation mass is what sets the spike count (spikes/step = sum(relu(B1))/theta),
                 so this penalty buys energy rather than accuracy. 0 disables it.
      val_mode : "dropout" (validation accuracy measured with dropout active -- what the
                 shipped numbers used) or "clean" (separate dropout-free pass -- a protocol
                 change, report it as such).
      spec_norm: constrain every effective matrix to unit spectral norm, so the per-layer
                 conversion-error gain is (1-alpha) instead of ||M_l||. This is the WP3 design
                 rule; see experiments/wp3_depth.py for what it buys and what it costs.
      unit_mask: boolean (hidden,) mask; units with False are held at zero by projecting the
                 gradient step. This is the WP4 knob: a pruned unit emits no spikes, so the
                 spike count falls in proportion to the surviving fraction while the remaining
                 units keep their trained function. Passing a mask and re-running with fewer
                 epochs is "prune and finetune" without a second training loop.
    """
    import torch

    torch.manual_seed(seed)
    np.random.seed(seed)
    dev = torch.device(device if (device == "cpu" or torch.cuda.is_available()) else "cpu")

    X, y, adj = data["X"], data["y"], data["adj"]
    N, F, C = data["N"], data["F"], data["C"]
    Lt = int(n_layers)
    assert Lt >= 2

    coo = adj.tocoo()
    idx = torch.tensor(np.vstack([coo.row, coo.col]), dtype=torch.long, device=dev)
    vals = torch.tensor(coo.data, dtype=torch.float32, device=dev)
    A_t = torch.sparse_coo_tensor(idx, vals, (N, N), device=dev).coalesce()
    X_t = torch.tensor(X, dtype=torch.float32, device=dev)
    Y_t = torch.tensor(y, dtype=torch.long, device=dev)
    tr = torch.tensor(np.where(data["train"])[0], dtype=torch.long, device=dev)
    va = torch.tensor(np.where(data["val"])[0], dtype=torch.long, device=dev)

    def glorot(fan_in, fan_out):
        std = 1.0 / math.sqrt(fan_in)
        return torch.empty(fan_in, fan_out, device=dev).uniform_(-std, std)

    dims = [F] + [hidden] * (Lt - 1) + [C]
    Ws = [torch.nn.Parameter(glorot(dims[l], dims[l + 1])) for l in range(Lt)]
    b_hidden = torch.nn.Parameter(torch.zeros(max(Lt - 1, 1), hidden, device=dev))
    b_out = torch.nn.Parameter(torch.zeros(C, device=dev))
    params = Ws + [b_hidden, b_out]
    opt = torch.optim.Adam(params, lr=lr, weight_decay=wd)

    def eff(W, l):
        """Identity mapping M_l = (1-beta_l) I + beta_l W_l, with beta_l = beta_idm / l.

        The schedule is the point, not a detail: GCNII decays beta with depth precisely so that
        deep layers approach the identity map and the signal can travel 8-64 hops without
        vanishing. A constant beta does the opposite -- combined with any weight decay it drives
        M_l towards (1-beta) I, a pure scalar contraction, and training collapses (measured:
        Cora ANN 0.266 at L=4 with constant beta=0.5 and wd=0.01).
        """
        if beta_idm > 0 and W.shape[0] == W.shape[1]:
            b = beta_idm / max(l, 1)
            W = (1.0 - b) * torch.eye(W.shape[0], device=dev) + b * W
        if spec_norm:
            W = W / torch.linalg.matrix_norm(W, ord=2).clamp_min(1e-8)
        return W

    def forward(train=True):
        Bs, Hs = [], []
        H0 = None
        for l in range(Lt):
            if l == 0:
                Z = torch.sparse.mm(A_t, X_t)
            elif l == Lt - 1:
                Z = torch.sparse.mm(A_t, Hs[-1])
            else:
                Z = torch.sparse.mm(A_t, Hs[-1])
                if alpha > 0:
                    Z = (1.0 - alpha) * Z + alpha * H0
            B = Z @ eff(Ws[l], l) + (b_hidden[l] if l < Lt - 1 else b_out)
            Bs.append(B)
            if l < Lt - 1:
                H = torch.relu(B)
                if dropout > 0 and train:
                    H = torch.dropout(H, dropout, train=True)
                Hs.append(H)
                if l == 0:
                    H0 = H
        return Bs, Bs[-1], Hs

    best_val, best_state, bad = -1.0, None, 0
    hist = []
    for ep in range(epochs):
        opt.zero_grad()
        Bs, logits, _ = forward(train=True)
        loss = torch.nn.functional.cross_entropy(logits[tr], Y_t[tr])
        if sparsity > 0:
            loss = loss + sparsity * torch.relu(Bs[sparsity_layer]).mean()
        loss.backward()
        opt.step()
        if unit_mask is not None:
            with torch.no_grad():
                m_ = torch.tensor(unit_mask, device=dev)
                Ws[0][:, ~m_] = 0.0
                b_hidden[0][~m_] = 0.0
                for l in range(1, Lt - 1):
                    Ws[l][~m_, :] = 0.0
                    Ws[l][:, ~m_] = 0.0
                    b_hidden[l][~m_] = 0.0
        with torch.no_grad():
            lg = logits if val_mode == "dropout" else forward(train=False)[1]
            v = float((lg[va].argmax(1) == Y_t[va]).float().mean())
        hist.append(v)
        if v > best_val:
            best_val, bad = v, 0
            best_state = [p.detach().clone() for p in params]
        else:
            bad += 1
            if bad >= patience:
                break
    for p, s in zip(params, best_state):
        p.data.copy_(s)
    if unit_mask is not None:
        with torch.no_grad():
            m_ = torch.tensor(unit_mask, device=dev)
            Ws[0][:, ~m_] = 0.0
            b_hidden[0][~m_] = 0.0
            for l in range(1, Lt - 1):
                Ws[l][~m_, :] = 0.0
                Ws[l][:, ~m_] = 0.0
                b_hidden[l][~m_] = 0.0

    with torch.no_grad():
        Bs, logits, Hs = forward(train=False)
        pred = logits.argmax(1).cpu().numpy()
        acc_tr = float((pred[data["train"]] == y[data["train"]]).mean())
        acc_va = float((pred[data["val"]] == y[data["val"]]).mean())
        acc_te = float((pred[data["test"]] == y[data["test"]]).mean())
        Ms = [eff(Ws[l], l).detach().cpu().numpy().astype(np.float32) for l in range(Lt)]
        bs = [b_hidden[l].detach().cpu().numpy().astype(np.float32) for l in range(Lt - 1)]
        b_out_np = b_out.detach().cpu().numpy().astype(np.float32)
        B_np = [b.cpu().numpy().astype(np.float32) for b in Bs]
        H_np = [h.cpu().numpy().astype(np.float32) for h in Hs]
    return dict(Ms=Ms, bs_layers=bs, b_out=b_out_np, Bs=B_np, Hs=H_np,
                acc_test=acc_te, acc_val=acc_va, acc_train=acc_tr,
                n_layers=Lt, hidden=hidden, alpha=alpha, beta_idm=beta_idm, seed=seed,
                val_mode=val_mode, epochs_run=len(hist), val_curve=hist)


# ------------------------------------------------------------------ spectral summary
def spectral_gain(model) -> dict:
    """Per-layer and cumulative Lipschitz factors of the ANN's linear maps.

    The quantity the L-layer recursion multiplies error by at layer l is ||(1-alpha) M_l||_2
    (times ||A_hat||_2 <= 1 for a normalised adjacency). Reporting it turns "error compounds
    with depth" from a remark into a number that can be predicted before running the SNN.
    """
    Ms = model["Ms"]
    alpha = model.get("alpha", 0.0)
    gains = [float(np.linalg.norm((1.0 - alpha if i > 0 else 1.0) * M, 2))
             for i, M in enumerate(Ms[:-1])]
    return dict(per_layer=gains, cumulative=float(np.prod(gains)) if gains else 1.0)


def gauge_normalize(model) -> dict:
    """Reparametrise a trained ANN so every hidden layer has unit spectral gain.

    ReLU is positively homogeneous, so for alpha = 0 the map
        B_l -> B_l / c_l,  H_l -> H_l / c_l,  M_l -> M_l * c_{l-1}/c_l,  b_l -> b_l / c_l
    leaves every pre-activation of the *next* layer, and hence every prediction, unchanged.
    Choosing c_l = prod_{j<=l} ||M_j||_2 therefore sets ||M_l||_2 = 1 for all l at zero cost
    to the ANN -- and the conversion-error recursion then contracts instead of compounding:

        ||E_L|| <= eps * (1 - (1-alpha)^L) / alpha          (bounded in L)
        instead of
        ||E_L|| <= eps * prod_l ||M_l||_2                   (grows with L)

    Only valid for alpha = 0 (with a residual, the source H_0 carries its own scale and the
    one-parameter gauge no longer closes). Asserted, not assumed.
    """
    assert model.get("alpha", 0.0) == 0.0, "gauge_normalize requires alpha == 0"
    Ms = [m.astype(np.float64, copy=True) for m in model["Ms"]]
    bs = [b.astype(np.float64, copy=True) for b in model["bs_layers"]]
    L1 = len(bs)                       # number of hidden layers
    scales = []
    c = 1.0
    for l in range(L1):
        s_l = float(np.linalg.norm(Ms[l], 2))
        if s_l < 1e-12:
            s_l = 1.0
        scales.append(s_l)
        c *= s_l
        Ms[l] = Ms[l] / s_l            # unit spectral norm for this layer
        bs[l] = bs[l] / c              # its own bias is scaled by the cumulative factor
        if l + 1 < len(Ms):
            Ms[l + 1] = Ms[l + 1] * c  # next layer absorbs the cumulative scale
    out = dict(model)
    out["Ms"] = [m.astype(np.float32) for m in Ms]
    out["bs_layers"] = [b.astype(np.float32) for b in bs]
    out["gauge_scales"] = scales
    out["gauge_cumulative"] = float(np.prod(scales))
    return out


# ------------------------------------------------------------------ SNN conversion
def _const_terms(data, model):
    """Constant per-step input for each spiking layer (everything not driven by spikes)."""
    Ms, bs = model["Ms"], model["bs_layers"]
    alpha = model.get("alpha", 0.0)
    L1 = model["n_layers"] - 1
    const = []
    for l in range(L1):
        c = np.array(bs[l], dtype=np.float32, copy=True)
        if l > 0 and alpha > 0:
            c = c + alpha * (model["Hs"][0] @ Ms[l])
        const.append(np.asarray(c, dtype=np.float32))
    return const


def convert(data, model, T: int, theta: float = 1.0, betas=None, readout="membrane",
            l1_mode="if", seed=0, init_jitter: float = 0.0, record: bool = True,
            return_logits: bool = False, thetas=None) -> dict:
    """Convert an L-layer ANN to an L-layer spiking network and simulate T steps.

    Per timestep, hidden layer l accumulates
        inst_l,t = (1-alpha) A_hat @ s_{l-1,t} @ M_l + const_l
    with const_l carrying the initial-residual term (alpha H_0 M_l) and the bias. Summing over
    t gives the exact identity in the module docstring.

    thetas      : optional per-HIDDEN-LAYER thresholds (WP15). When None every layer uses `theta`,
                  which is exactly the behaviour of all earlier work in this project. When a list
                  is given, the default per-layer bias becomes theta_l/(2T), the layer-wise
                  generalisation of the identity's optimal bias beta* = theta/(2T). The output
                  layer keeps the global `theta`. Default behaviour is unchanged; no earlier
                  result depends on this parameter.
    betas       : per-layer forward bias. Default theta/(2T) at EVERY layer (or theta_l/(2T)
                  when `thetas` is supplied), the L-layer generalisation of the shipped layer-1
                  correction. Pass a list to test
                  alternatives (e.g. [beta] + [0]*(L-2) for the shipped layer-1-only setting).
    init_jitter : std of a random initial membrane offset (WP5's third perturbation axis).
    """
    X = data["X"]
    adj = data["adj"]
    N, C = data["N"], data["C"]
    Lt = model["n_layers"]
    Ms = model["Ms"]
    rng = np.random.default_rng(seed)
    L1 = Lt - 1

    if thetas is None:
        thetas = [theta] * L1
    thetas = (list(thetas) + [theta] * L1)[:L1]
    if betas is None:
        betas = [th / (2.0 * T) for th in thetas]
    betas = (list(betas) + [0.0] * L1)[:L1]

    const = _const_terms(data, model)
    inst1 = (np.asarray(adj @ (X @ Ms[0]).astype(np.float32))
             + model["bs_layers"][0]).astype(np.float32)

    us = [np.zeros((N, Ms[l].shape[1])) for l in range(L1)]
    if init_jitter > 0:
        us = [rng.normal(0.0, init_jitter, u.shape) for u in us]
    cnt = [np.zeros((N, Ms[l].shape[1]), np.int32) for l in range(L1)]
    acc_out = np.zeros((N, C), np.float64)   # un-reset accumulator -> membrane readout
    u_out = np.zeros((N, C), np.float64)
    cnt_out = np.zeros((N, C), np.int32)
    lat, spike_total = {}, 0.0

    for t in range(T):
        prev = None
        for l in range(L1):
            if l == 0:
                inst = inst1 + np.float32(betas[0])
            else:
                inst = (np.asarray(adj @ (prev.astype(np.float32) @ Ms[l]))
                        + const[l] + np.float32(betas[l]))
            us[l] += inst
            th_l = thetas[l]
            if l1_mode == "tpp":
                p = np.clip(us[l], 0.0, th_l) / th_l
                s = (rng.random(us[l].shape) < p).astype(np.int8)
            else:
                s = (us[l] >= th_l).astype(np.int8)
            us[l] -= s * th_l
            cnt[l] += s
            spike_total += float(s.sum())
            prev = s
        out = (np.asarray(adj @ (prev.astype(np.float32) @ Ms[-1]))
               + model["b_out"]).astype(np.float32)
        acc_out += out
        u_out += out
        fired = (u_out >= theta)
        cnt_out += fired
        u_out -= fired * theta
        spike_total += float(fired.sum())
        if record:
            pred_t = acc_out.argmax(1) if readout == "membrane" else cnt_out.argmax(1)
            lat[t + 1] = float((pred_t[data["test"]] == data["y"][data["test"]]).mean())

    pred = acc_out.argmax(1) if readout == "membrane" else cnt_out.argmax(1)
    acc = float((pred[data["test"]] == data["y"][data["test"]]).mean())
    out = dict(acc=acc,
                acc_membrane=float((acc_out.argmax(1)[data["test"]]
                                    == data["y"][data["test"]]).mean()),
                spikes=spike_total, spikes_per_node=spike_total / N,
                per_layer_spikes=[float(c.sum()) for c in cnt] + [float(cnt_out.sum())],
                latency=lat, T=T, theta=theta, thetas=thetas, betas=betas,
                sop_est=float(T * data["E"] * sum(m.shape[1] for m in Ms[:-1])))
    if return_logits:
        # WP5 needs the accumulator itself, not just its argmax, in order to average views.
        out["logits"] = acc_out / float(T)
    return out


def simulate_counts(data, model, T=8, theta=1.0, betas=None, init_jitter=0.0, seed=0):
    """Run the SNN and return (counts, B_hat, B) for every hidden layer.

    Kept next to `convert` rather than inside it so the identity check runs against the SAME
    simulation that produces the accuracies -- checking a second implementation would only
    prove the two agree, not that either is right.
    """
    X = data["X"]; adj = data["adj"]; N = data["N"]
    Lt = model["n_layers"]; Ms = model["Ms"]
    alpha = model.get("alpha", 0.0)
    L1 = Lt - 1
    if betas is None:
        betas = [theta / (2.0 * T)] * L1
    betas = (list(betas) + [0.0] * L1)[:L1]

    const = _const_terms(data, model)
    inst1 = (np.asarray(adj @ (X @ Ms[0]).astype(np.float32))
             + model["bs_layers"][0]).astype(np.float32)
    rng = np.random.default_rng(seed)
    us = [np.zeros((N, Ms[l].shape[1])) for l in range(L1)]
    if init_jitter > 0:
        us = [rng.normal(0.0, init_jitter, u.shape) for u in us]
    cnt = [np.zeros((N, Ms[l].shape[1])) for l in range(L1)]
    for _ in range(T):
        prev = None
        for l in range(L1):
            if l == 0:
                inst = inst1 + np.float32(betas[0])
            else:
                inst = (np.asarray(adj @ (prev.astype(np.float32) @ Ms[l]))
                        + const[l] + np.float32(betas[l]))
            us[l] += inst
            s = (us[l] >= theta).astype(np.float32)
            us[l] -= s * theta
            cnt[l] += s
            prev = s

    Bhats, Bs, Hats = [], [], []
    H = X
    for l in range(L1):
        if l == 0:
            Z = np.asarray(adj @ H)
        elif alpha > 0:
            Z = (1 - alpha) * np.asarray(adj @ H) + alpha * model["Hs"][0]
        else:
            Z = np.asarray(adj @ H)
        B = Z @ Ms[l] + model["bs_layers"][l]
        Bs.append(B)
        Bhats.append(B if l == 0
                     else (1 - alpha) * np.asarray(adj @ ((cnt[l - 1] / T) @ Ms[l])) + const[l])
        H = np.maximum(B, 0.0)
        Hats.append(H)
    return cnt, Bhats, Bs, Hats


def check_identity(data, model, T=8, theta=1.0, betas=None) -> dict:
    """Numeric check of  B_hat_l - B_l == (1-alpha) A_hat (E_{l-1} M_l)  at every layer."""
    cnt, Bhats, Bs, Hats = simulate_counts(data, model, T, theta, betas)
    adj = data["adj"]
    alpha = model.get("alpha", 0.0)
    Ms = model["Ms"]
    per, E_prev = [], None
    for l in range(len(Bs)):
        got = Bhats[l] - Bs[l]
        pred = (np.zeros_like(got) if l == 0
                else (1 - alpha) * np.asarray(adj @ (E_prev @ Ms[l])))
        per.append(dict(layer=l + 1, max_abs=float(np.max(np.abs(got - pred))),
                        got_max=float(np.max(np.abs(got))),
                        scale=float(np.max(np.abs(Bs[l])))))
        E_prev = (cnt[l] / T) - Hats[l]
    return dict(max_abs=max(p["max_abs"] for p in per), per_layer=per)


# ------------------------------------------------------------------ utilities
def seeds(n=7):
    return list(range(n))


def summarize(vals):
    a = np.asarray(vals, dtype=float)
    return dict(mean=float(a.mean()), std=float(a.std(ddof=0)), n=int(a.size))


def required_T(curve: dict, target: float):
    """Smallest T on the grid whose accuracy reaches `target`; None if the grid never does."""
    for T in sorted(int(k) for k in curve):
        if curve[str(T)] >= target:
            return T
    return None


def save(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, default=float), encoding="utf-8")
    return p


if __name__ == "__main__":
    d = load("cora")
    print({k: v for k, v in d.items() if k in ("name", "N", "F", "C", "E")})
    for L, al, hid in ((2, 0.0, 16), (3, 0.0, 16), (4, 0.0, 16), (4, 0.5, 64), (8, 0.5, 64)):
        m = train_ann(d, hidden=hid, n_layers=L, alpha=al, seed=0)
        r = convert(d, m, T=8)
        print(f"L={L} alpha={al} H={hid} ann={m['acc_test']:.4f} T8={r['acc']:.4f} "
              f"identity={check_identity(d, m, T=8)['max_abs']:.3e} "
              f"gain={spectral_gain(m)['cumulative']:.3f}", flush=True)
