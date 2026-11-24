"""Exact zero-row message pruning certificate."""

from __future__ import annotations

import numpy as np


def zero_message_mask(hidden_spike_counts: np.ndarray) -> np.ndarray:
    counts = np.asarray(hidden_spike_counts)
    if counts.ndim != 2:
        raise ValueError("counts must be two-dimensional")
    return np.all(counts == 0, axis=1)


def prune_zero_rows(values: np.ndarray, mask: np.ndarray) -> np.ndarray:
    values = np.asarray(values)
    mask = np.asarray(mask, dtype=bool)
    if values.ndim != 2 or mask.shape != (values.shape[0],):
        raise ValueError("value/mask shape mismatch")
    output = np.array(values, copy=True)
    output[mask] = 0
    return output
