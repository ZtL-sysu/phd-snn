#!/usr/bin/env python3
"""Simulation kernels for S1 mechanism probes and the Table 1 method rows.

This module is deliberately independent of core.convert(): the probes need to manipulate the
*spike train between layers* and the *per-edge arrival phase inside one aggregation*, neither of
which is expressible in a single-pass loop. All neuron models operate on the same constant-current
input, the same weights, the same aggregation and the same seeds.

Neuron models
-------------
if            : integrate-and-fire, s = 1[u >= theta], u -= theta*s
tpp_simple    : the companion kernel's membrane-proportional Bernoulli, s ~ Bern(clip(u,0,th)/th)
tpp_faithful  : ICML'25 two-phase TPP. The accumulation phase fixes the target number of spikes
                T*r from the ANN rate r = clip(B/theta, 0, 1); the firing phase emits with
                p_t = clip((T*r - fired)/(T-t), 0, 1), an increasing-per-step probability whose
                cumulative expectation satisfies Eq. (8): ((T-t+1)theta/T) E[sum_{i<=t} s_i]
                = ReLU_theta(X). Derived from arXiv:2502.14487v2, Eq. (8)-(13).

Probes
------
inter_perm    : randomly permute the first hidden layer's spike train along the T axis before it
                is fed to the next layer. For L=2 the next layer is the membrane accumulator, so
                the effect is exactly zero up to float summation order -- that null result IS the
                mechanism evidence. For L=3 it is replayed through an IF hidden layer, which is
                the faithful replication of ICML'25 Fig.1.
intra_phase   : give every edge (i,j) a random delay d_ij in {0,1,2}, and aggregate
                msg[t] = sum_d adj_d @ S[t-d]. Pulses pushed past the T-step window are lost,
                which changes the per-node quantised rate that the exact identity describes.
                A plain reordering of a sum would be a mathematical no-op and is NOT used.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def phase_matrices(adj: sp.csr_matrix, rng: np.random.Generator, max_delay: int = 2):
    """Split a normalised adjacency into per-delay buckets (same weights, random phases)."""
    csr = adj.tocsr()
    buckets = []
    delays = rng.integers(0, max_delay + 1, size=csr.nnz, dtype=np.int64)
    for d in range(max_delay + 1):
        mask = (delays == d)
        rows = np.repeat(np.arange(csr.shape[0], dtype=np.int64), np.diff(csr.indptr))
        data = np.where(mask, csr.data, 0.0).astype(np.float32)
        buckets.append(sp.csr_matrix((data, csr.indices.copy(), csr.indptr.copy()),
                                     shape=csr.shape, dtype=np.float32))
    del rows
    return buckets


def _emit(us, fired, target, t, T, theta, neuron, rng):
    if neuron == "if":
        s = (us >= theta).astype(np.float32)
        us -= s * theta
        return s, us, fired
    if neuron == "tpp_simple":
        p = np.clip(us, 0.0, theta) / theta
        s = (rng.random(us.shape) < p).astype(np.float32)
        us -= s * theta
        return s, us, fired
    if neuron == "tpp_faithful":
        remaining_steps = max(T - t, 1)
        p = np.clip((target - fired) / remaining_steps, 0.0, 1.0)
        s = (rng.random(p.shape) < p).astype(np.float32)
        return s, us, fired + s
    raise ValueError("unknown neuron " + neuron)


def simulate_l2(data, model, T, theta=1.0, bias=True, neuron="if", readout="membrane",
                intra_phase=False, inter_perm=False, perm_seed=0, phase_seed=0,
                host_scaled=True):
    """Two-layer conversion with optional probes. Returns accuracy, spikes and diagnostics."""
    rng = np.random.default_rng(perm_seed * 100003 + phase_seed * 7919 + int(T))
    adj = data["adj"].tocsr()
    X = data["X"]
    M0, M1 = model["Ms"][0], model["Ms"][1]
    b0, b_out = model["bs_layers"][0], model["b_out"]
    N, H = X.shape[0], M0.shape[1]
    C = b_out.shape[0]
    beta = theta / (2.0 * T) if bias else 0.0
    inst1 = (np.asarray(adj @ (X @ M0).astype(np.float32)) + b0).astype(np.float32)
    target = np.clip(inst1 / theta, 0.0, 1.0) * T

    us = np.zeros((N, H), np.float32)
    fired = np.zeros((N, H), np.float32)
    S = []
    spike_total = 0.0
    for t in range(T):
        us = us + inst1 + np.float32(beta)
        s, us, fired = _emit(us, fired, target, t, T, theta, neuron, rng)
        S.append(s)
        spike_total += float(s.sum())
    S = np.stack(S, axis=0)  # (T,N,H)

    if inter_perm:
        order = rng.permutation(T)
        S_used = S[order]
    else:
        S_used = S

    if intra_phase:
        buckets = phase_matrices(adj, rng, max_delay=2)
        acc_out = np.zeros((N, C), np.float64)
        for t in range(T):
            msg = np.zeros((N, H), np.float32)
            for d, mat in enumerate(buckets):
                if t - d >= 0:
                    msg += np.asarray(mat @ S_used[t - d].astype(np.float32))
            acc_out += np.asarray(msg @ M1, np.float64) + b_out
    else:
        acc_out = np.zeros((N, C), np.float64)
        for t in range(T):
            msg = np.asarray(adj @ S_used[t].astype(np.float32))
            acc_out += np.asarray(msg @ M1, np.float64) + b_out

    u_out = np.zeros((N, C), np.float64)
    cnt_out = np.zeros((N, C), np.float64)
    for t in range(T):
        if intra_phase:
            msg = np.zeros((N, H), np.float32)
            for d, mat in enumerate(buckets):
                if t - d >= 0:
                    msg += np.asarray(mat @ S_used[t - d].astype(np.float32))
        else:
            msg = np.asarray(adj @ S_used[t].astype(np.float32))
        step = np.asarray(msg @ M1, np.float64) + b_out
        u_out += step
        f = (u_out >= theta)
        cnt_out += f
        u_out -= f * theta
        spike_total += float(f.sum())

    pred = acc_out.argmax(1) if readout == "membrane" else cnt_out.argmax(1)
    acc = float((pred[data["test"]] == data["y"][data["test"]]).mean())
    return dict(acc=acc, spikes=spike_total, spikes_per_node=spike_total / N,
                sop_est=float(T * data["E"] * H), T=T, neuron=neuron, bias=bool(bias),
                readout=readout, intra_phase=bool(intra_phase), inter_perm=bool(inter_perm))


def simulate_l3_interlayer(data, model, T, theta=1.0, bias=True, perm_seed=0,
                           permute=False):
    """Faithful ICML'25 Fig.1 replication: three layers, permute layer-1 spike train in time."""
    rng = np.random.default_rng(perm_seed * 100003 + 17)
    adj = data["adj"].tocsr()
    X = data["X"]
    M0, M1, M2 = model["Ms"]
    b0, b1, b_out = model["bs_layers"][0], model["bs_layers"][1], model["b_out"]
    N, H = X.shape[0], M0.shape[1]
    C = b_out.shape[0]
    beta = theta / (2.0 * T) if bias else 0.0
    inst1 = (np.asarray(adj @ (X @ M0).astype(np.float32)) + b0).astype(np.float32)

    us0 = np.zeros((N, H), np.float32)
    S0 = []
    for _ in range(T):
        us0 = us0 + inst1 + np.float32(beta)
        s0 = (us0 >= theta).astype(np.float32)
        us0 -= s0 * theta
        S0.append(s0)
    S0 = np.stack(S0, axis=0)

    if permute:
        order = rng.permutation(T)
        S0 = S0[order]

    us1 = np.zeros((N, H), np.float32)
    acc_out = np.zeros((N, C), np.float64)
    spikes = float(S0.sum())
    for t in range(T):
        inst2 = (np.asarray(adj @ (S0[t].astype(np.float32) @ M1)) + b1
                 + np.float32(beta)).astype(np.float32)
        us1 = us1 + inst2
        s1 = (us1 >= theta).astype(np.float32)
        us1 -= s1 * theta
        spikes += float(s1.sum())
        out = np.asarray(adj @ (s1 @ M2)).astype(np.float64) + b_out
        acc_out += out
    pred = acc_out.argmax(1)
    acc = float((pred[data["test"]] == data["y"][data["test"]]).mean())
    return dict(acc=acc, spikes=spikes, T=T, permute=bool(permute), n_layers=3)


def ann_diagnostics(data, model):
    """Quantities computable from the trained ANN alone, with NO spiking simulation.

    kappa is the bound-derived scale in Theorem G1(d): the identity gives
    ||B_hat_2 - B_2|| <= ||A_hat M_2|| * theta/(2T) * sqrt(H), so the timestep needed to keep
    the logit perturbation under the classifier margin scales as kappa / T.
    """
    adj = data["adj"].tocsr()
    X = data["X"]
    M0, M1 = model["Ms"][0], model["Ms"][1]
    b0, b_out = model["bs_layers"][0], model["b_out"]
    B1 = np.asarray(adj @ (X @ M0)) + b0
    H1 = np.maximum(B1, 0.0)
    logits = np.asarray(adj @ (H1 @ M1)) + b_out
    te = data["test"]
    lg = logits[te]
    yy = data["y"][te]
    correct = lg[np.arange(len(yy)), yy].copy()
    lg2 = lg.copy()
    lg2[np.arange(len(yy)), yy] = -np.inf
    # Absolute signed margin: a low-accuracy graph has a negative *signed* margin, which would
    # make the bound-derived scale diverge. The perturbation tolerance is a magnitude, so the
    # median absolute gap between the true-class logit and the strongest competitor is the
    # correct quantity. Frozen before any held-out measurement (pre-registration-c3 v3).
    margin = float(np.median(np.abs(correct - lg2.max(1))))
    # ||A_hat M_2|| <= ||A_hat|| * ||M_2||; rho (max row sum) bounds the former for a
    # non-negative normalised aggregation. Neither quantity needs a spiking simulation.
    op_norm = float(np.linalg.norm(M1, ord=2))
    rho = float(np.max(np.asarray(adj.sum(1)).ravel()))
    H = M0.shape[1]
    kappa = op_norm * rho * np.sqrt(H) / (2.0 * max(margin, 1e-6))
    return dict(margin=margin, kappa=float(kappa), rho=rho,
                op_norm=op_norm, ann_acc=float(model["acc_test"]),
                logit_scale=float(np.std(logits)))
