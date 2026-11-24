"""Training-only operator-conditioned threshold selection for frozen GCN conversion."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def teacher_logits(data: dict, model: dict) -> np.ndarray:
    adjacency = data["adj"]
    hidden = np.asarray(model["Hs"][-1], dtype=np.float32)
    logits = np.asarray(adjacency @ hidden) @ np.asarray(model["Ms"][-1], dtype=np.float32)
    logits += np.asarray(model["b_out"], dtype=np.float32)
    return np.asarray(logits, dtype=np.float32)


def fit_operator_factor(
    *,
    data: dict,
    model: dict,
    target_logits: np.ndarray,
    train_mask: np.ndarray,
    factors: Sequence[float],
    t_steps: int,
    convert,
) -> dict:
    if not factors:
        raise ValueError("factors must be nonempty")
    target_logits = np.asarray(target_logits)
    train_mask = np.asarray(train_mask, dtype=bool)
    if target_logits.ndim != 2 or train_mask.shape != (target_logits.shape[0],):
        raise ValueError("target_logits and train_mask shape mismatch")
    rows = []
    for factor in factors:
        factor = float(factor)
        if not np.isfinite(factor) or factor <= 0:
            raise ValueError("factors must be finite and positive")
        result = convert(data, model, T=t_steps, thetas=[factor] * (len(model["Ms"]) - 1), return_logits=True)
        logits = np.asarray(result["logits"])[train_mask]
        agreement = float(np.mean(np.argmax(logits, axis=1) == np.argmax(target_logits[train_mask], axis=1)))
        rows.append({"factor": factor, "agreement": agreement, "spikes_per_node": float(result["spikes_per_node"])})
    best = max(rows, key=lambda row: (row["agreement"], row["factor"]))
    return {"factor": float(best["factor"]), "train_agreement": float(best["agreement"]), "candidates": rows}


def evaluate_factor(*, data: dict, model: dict, target_logits: np.ndarray, mask: np.ndarray, factor: float, t_steps: int, convert) -> dict:
    result = convert(data, model, T=t_steps, thetas=[float(factor)] * (len(model["Ms"]) - 1), return_logits=True)
    logits = np.asarray(result["logits"])[np.asarray(mask, dtype=bool)]
    target = np.asarray(target_logits)[np.asarray(mask, dtype=bool)]
    return {
        "factor": float(factor),
        "accuracy": float(np.mean(np.argmax(logits, axis=1) == np.asarray(data["y"])[np.asarray(mask, dtype=bool)])),
        "teacher_agreement": float(np.mean(np.argmax(logits, axis=1) == np.argmax(target, axis=1))),
        "logit_mse": float(np.mean((logits - target) ** 2)),
        "spikes_per_node": float(result["spikes_per_node"]),
        "logits": logits,
    }
