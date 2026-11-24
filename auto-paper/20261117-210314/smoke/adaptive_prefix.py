"""Causal confidence-guided prefix selection for frozen GNN→SNN conversion."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def make_internal_partitions(
    official_ids: np.ndarray, *, seed: int, dev: int, tune: int, validation: int
) -> dict[str, np.ndarray]:
    official_ids = np.asarray(official_ids)
    if official_ids.ndim != 1 or len(np.unique(official_ids)) != len(official_ids):
        raise ValueError("official_ids must be a one-dimensional unique array")
    required = dev + tune + validation
    if min(dev, tune, validation) <= 0 or required > len(official_ids):
        raise ValueError("partition sizes are invalid")
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(official_ids))
    selected = official_ids[order[:required]]
    return {
        "dev": selected[:dev].copy(),
        "tune": selected[dev : dev + tune].copy(),
        "validation": selected[dev + tune :].copy(),
    }


def _margin(logits: np.ndarray) -> np.ndarray:
    logits = np.asarray(logits)
    if logits.ndim != 2 or logits.shape[1] < 2:
        raise ValueError("logits must be [examples, classes]")
    values = -np.partition(-logits, kth=1, axis=1)
    return values[:, 0] - values[:, 1]


def uncertainty_scores(t1_logits: np.ndarray, t2_logits: np.ndarray) -> np.ndarray:
    t1_logits = np.asarray(t1_logits)
    t2_logits = np.asarray(t2_logits)
    if t1_logits.shape != t2_logits.shape or t1_logits.ndim != 2:
        raise ValueError("T1 and T2 logits must have identical two-dimensional shapes")
    if not np.isfinite(t1_logits).all() or not np.isfinite(t2_logits).all():
        raise ValueError("logits must be finite")
    disagreement = (np.argmax(t1_logits, axis=1) != np.argmax(t2_logits, axis=1)).astype(float)
    t2_margin = _margin(t2_logits)
    t2_penalty = 1.0 / (1.0 + np.maximum(t2_margin, 0.0))
    margin_scale = float(np.quantile(t2_penalty, 0.9)) or 1.0
    return disagreement + t2_penalty / margin_scale


def selective_prefix(
    t2_logits: np.ndarray,
    t4_logits: np.ndarray,
    scores: np.ndarray,
    *,
    uncertainty_threshold: float,
) -> tuple[np.ndarray, np.ndarray]:
    t2_logits = np.asarray(t2_logits)
    t4_logits = np.asarray(t4_logits)
    scores = np.asarray(scores)
    if t2_logits.shape != t4_logits.shape or t2_logits.ndim != 2:
        raise ValueError("T2 and T4 logits must have identical shape")
    if scores.shape != (t2_logits.shape[0],):
        raise ValueError("score shape mismatch")
    if not np.isfinite(scores).all():
        raise ValueError("scores must be finite")
    use_t4 = scores >= uncertainty_threshold
    output = np.array(t2_logits, copy=True)
    output[use_t4] = t4_logits[use_t4]
    return output, use_t4


def choose_thresholds(
    t1_logits: np.ndarray,
    t2_logits: np.ndarray,
    t4_logits: np.ndarray,
    teacher_logits: np.ndarray,
    *,
    fractions: Iterable[float],
) -> dict:
    arrays = [np.asarray(x) for x in (t1_logits, t2_logits, t4_logits, teacher_logits)]
    if len({x.shape for x in arrays}) != 1 or arrays[0].ndim != 2:
        raise ValueError("all logits must have identical shape")
    scores = uncertainty_scores(arrays[0], arrays[1])
    teacher_pred = np.argmax(arrays[3], axis=1)
    candidates = []
    for fraction in fractions:
        fraction = float(fraction)
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("fractions must lie in [0, 1]")
        if fraction == 1.0:
            threshold = -np.inf
        elif fraction == 0.0:
            threshold = np.inf
        else:
            threshold = float(np.quantile(scores, 1.0 - fraction))
        converted, use_t4 = selective_prefix(
            arrays[1], arrays[2], scores, uncertainty_threshold=threshold
        )
        candidates.append(
            {
                "fraction": fraction,
                "threshold": threshold,
                "upgraded": int(use_t4.sum()),
                "teacher_agreement": float(
                    np.mean(np.argmax(converted, axis=1) == teacher_pred)
                ),
                "validation_note": "thresholds are fit on tune only",
            }
        )
    best = max(
        candidates,
        key=lambda row: (row["teacher_agreement"], row["fraction"]),
    )
    output = dict(best)
    output["all_candidates"] = [dict(candidate) for candidate in candidates]
    return output
