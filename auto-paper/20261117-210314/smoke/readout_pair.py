"""Certified top-two graph readout event compression."""

from __future__ import annotations

import numpy as np


def top2_pair_readout(logits: np.ndarray) -> dict:
    logits = np.asarray(logits)
    if logits.ndim != 2 or logits.shape[1] < 2 or not np.isfinite(logits).all():
        raise ValueError("logits must be finite [N,C], C>=2")
    order = np.argpartition(-logits, kth=1, axis=1)[:, :2]
    rows = np.arange(logits.shape[0])[:, None]
    values = logits[rows, order]
    sorted_order = np.take_along_axis(order, np.argsort(-values, axis=1), axis=1)
    sorted_values = np.take_along_axis(values, np.argsort(-values, axis=1), axis=1)
    pair_prediction = sorted_order[:, 0]
    return {
        "class_indices": sorted_order,
        "class_logits": sorted_values,
        "margin": sorted_values[:, 0] - sorted_values[:, 1],
        "predictions": pair_prediction,
        "output_slots_per_graph": 2,
        "full_slots_per_graph": int(logits.shape[1]),
    }
