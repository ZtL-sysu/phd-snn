"""Risk-controlled selective acceptance for converted graph logits."""

from __future__ import annotations

import numpy as np


def uncertainty_scores(t1_logits: np.ndarray, t2_logits: np.ndarray) -> np.ndarray:
    t1_logits = np.asarray(t1_logits)
    t2_logits = np.asarray(t2_logits)
    if t1_logits.shape != t2_logits.shape or t1_logits.ndim != 2:
        raise ValueError("logit shape mismatch")
    disagreement = (np.argmax(t1_logits, axis=1) != np.argmax(t2_logits, axis=1)).astype(float)
    sorted_logits = -np.partition(-t2_logits, kth=1, axis=1)
    margin = sorted_logits[:, 0] - sorted_logits[:, 1]
    return disagreement + 1.0 / (1.0 + np.maximum(margin, 0.0))


def fit_risk_threshold(scores: np.ndarray, correct: np.ndarray, *, target_risk: float) -> dict:
    scores = np.asarray(scores, dtype=float)
    correct = np.asarray(correct, dtype=bool)
    if scores.shape != correct.shape or not 0 < target_risk < 1:
        raise ValueError("scores/correct shape or target_risk invalid")
    candidates = np.unique(np.concatenate(([-np.inf], scores, [np.inf])))
    feasible = []
    for threshold in candidates:
        accepted = scores <= threshold
        if accepted.any():
            risk = float(1.0 - correct[accepted].mean())
            if risk <= target_risk:
                feasible.append((float(accepted.mean()), float(threshold), risk))
    if not feasible:
        return {"threshold": -np.inf, "coverage": 0.0, "risk": 1.0, "status": "no-safe-threshold"}
    coverage, threshold, risk = max(feasible, key=lambda row: (row[0], row[1]))
    return {"threshold": threshold, "coverage": coverage, "risk": risk, "status": "calibrated"}


def selective_result(logits: np.ndarray, labels: np.ndarray, scores: np.ndarray, threshold: float) -> dict:
    logits = np.asarray(logits)
    labels = np.asarray(labels)
    scores = np.asarray(scores)
    accepted = scores <= threshold
    if accepted.any():
        error = float(np.mean(np.argmax(logits[accepted], axis=1) != labels[accepted]))
    else:
        error = 1.0
    return {"coverage": float(accepted.mean()), "selective_error": error, "accepted": accepted}
