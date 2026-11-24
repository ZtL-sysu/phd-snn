"""Additional conversion primitives for certificate, edge, positional and delay screens."""

from __future__ import annotations

import numpy as np


def affine_error_envelope(adjacency: np.ndarray, weight: np.ndarray, coordinate_error: float) -> np.ndarray:
    adjacency = np.asarray(adjacency, dtype=np.float64)
    weight = np.asarray(weight, dtype=np.float64)
    if adjacency.ndim != 2 or adjacency.shape[0] != adjacency.shape[1] or weight.ndim != 2:
        raise ValueError("adjacency/weight shape mismatch")
    if not np.isfinite(coordinate_error) or coordinate_error < 0:
        raise ValueError("coordinate_error must be finite and nonnegative")
    row_gain = np.abs(adjacency).sum(axis=1)
    weight_gain = np.abs(weight).sum(axis=0)
    return np.outer(row_gain, weight_gain) * coordinate_error


def quantize_uniform(values: np.ndarray, *, levels: int = 8) -> tuple[np.ndarray, float]:
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or levels < 2:
        raise ValueError("values must be [N,D] and levels >= 2")
    minimum = values.min(axis=0)
    maximum = values.max(axis=0)
    span = np.maximum(maximum - minimum, np.finfo(np.float64).eps)
    step = span / (levels - 1)
    quantized = np.round((values - minimum) / step) * step + minimum
    return quantized, float(np.max(step))


def hop_position_messages(adjacency: np.ndarray, features: np.ndarray, *, hops: int = 3) -> np.ndarray:
    adjacency = np.asarray(adjacency, dtype=np.float64)
    features = np.asarray(features, dtype=np.float64)
    if adjacency.shape != (features.shape[0], features.shape[0]) or hops < 1:
        raise ValueError("adjacency/features shape or hops invalid")
    output = [features]
    current = features
    for _ in range(hops):
        current = adjacency @ current
        output.append(current)
    return np.concatenate(output, axis=1)


def prune_lowest_edges(adjacency: np.ndarray, *, keep_fraction: float) -> tuple[np.ndarray, int]:
    adjacency = np.asarray(adjacency, dtype=np.float64)
    if adjacency.ndim != 2 or adjacency.shape[0] != adjacency.shape[1] or not 0 < keep_fraction <= 1:
        raise ValueError("square adjacency and keep_fraction in (0,1] required")
    values = adjacency.ravel()
    candidates = np.flatnonzero(values > 0)
    keep_count = int(np.ceil(keep_fraction * len(candidates)))
    if keep_count == 0:
        raise ValueError("keep_fraction removes all edges")
    keep_indices = candidates[np.argsort(values[candidates])[-keep_count:]]
    mask = np.zeros(values.shape, dtype=bool)
    mask[keep_indices] = True
    pruned = np.where(mask.reshape(adjacency.shape), adjacency, 0.0)
    return pruned, len(candidates) - keep_count


def delayed_residual_events(frames: np.ndarray, *, delay: int = 1) -> np.ndarray:
    frames = np.asarray(frames, dtype=np.float64)
    if frames.shape[0] <= delay or delay < 1:
        raise ValueError("frames must exceed delay")
    return frames[1:] - frames[:-1]
