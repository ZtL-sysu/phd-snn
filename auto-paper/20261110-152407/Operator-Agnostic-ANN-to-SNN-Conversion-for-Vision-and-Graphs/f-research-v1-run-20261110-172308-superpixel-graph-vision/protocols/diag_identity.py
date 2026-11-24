#!/usr/bin/env python3
"""Diagnose why identity_f64 residual is ~2e-7 on narrow (unit-mask) networks."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vision_pipeline as vp  # noqa: E402
from run_e1 import identity_f64  # noqa: E402

R = HERE.parent
DATA = R / "data" / "pyg_bench"

sp = vp.load_vision("MNIST", DATA, n_train=300, n_val=60, n_test=60, seed=5)
tr = vp.batch_graphs(sp["train"]["graphs"], sp["train"]["indices"], pool="sum")
base = vp.train_ann(tr, hidden=64, seed=5, epochs=60, device="cpu")

H = base["W1"].shape[1]
k = max(1, int(round(H * 0.1)))
importance = np.maximum(tr["X"] @ base["W1"], 0.0).mean(axis=0)
mask = np.zeros(H, dtype=bool)
mask[np.argsort(importance)[-k:]] = True
model = vp.train_ann(tr, hidden=64, seed=5, epochs=60, device="cpu", unit_mask=mask)

T, theta = 3, 1.0
B1_32, H1_32 = vp.hidden_activation(tr, model)
A64 = tr["A"].astype(np.float64)
X64 = tr["X"].astype(np.float64)
W1_64 = model["W1"].astype(np.float64)
b1_64 = model["b1"].astype(np.float64)
inst1_64 = np.asarray(A64 @ (X64 @ W1_64), dtype=np.float64) + b1_64
print("max|fp32 B1 - fp64 inst1| =", float(np.max(np.abs(B1_32.astype(np.float64) - inst1_64))))
print("max|fp32 H1 - fp64 H1|   =",
      float(np.max(np.abs(H1_32.astype(np.float64) - np.maximum(inst1_64, 0.0)))))

rng1 = np.random.default_rng(5)
rng2 = np.random.default_rng(5)
tr32 = vp._spike_train(B1_32.astype(np.float32), T, theta, "ours", 0.0, rng1)
tr64 = vp._spike_train(inst1_64, T, theta, "ours", 0.0, rng2)
diff = sum(float(np.sum(np.abs(a.astype(np.float64) - b.astype(np.float64))))
           for a, b in zip(tr32, tr64))
print("spike-train L1 difference (fp32 vs fp64 inst1) =", diff)

print("identity_f64 (current) =", identity_f64(tr, model, T, theta, 1.0, 5))

# Fully self-consistent recomputation using the SAME fp32 inst1 as convert()
rng3 = np.random.default_rng(5)
trains = vp._spike_train(B1_32.astype(np.float32), T, theta, "ours", 0.0, rng3)
R64 = tr["R"].astype(np.float64)
W2 = model["W2"].astype(np.float64)
b2 = model["b2"].astype(np.float64)
H1 = H1_32.astype(np.float64)
B = np.asarray(R64 @ (np.asarray(A64 @ (H1 @ W2), dtype=np.float64)), dtype=np.float64) + b2
acc = np.zeros_like(B)
for s in trains:
    Z = np.asarray(A64 @ (s.astype(np.float64) @ W2), dtype=np.float64)
    acc += np.asarray(R64 @ Z, dtype=np.float64) + b2
B_hat = acc / float(T)
E1 = (np.sum(trains, axis=0) / float(T)).astype(np.float64) - H1
rhs = np.asarray(R64 @ (np.asarray(A64 @ (E1 @ W2), dtype=np.float64)), dtype=np.float64)
print("identity using convert's OWN fp32 trains =", float(np.max(np.abs((B_hat - B) - rhs))))
