from __future__ import annotations

import numpy as np


def uniform_quantize(
    values: np.ndarray,
    levels: int,
    per_channel: bool,
) -> tuple[np.ndarray, np.ndarray | float, np.ndarray | float, int]:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError("values must be a two-dimensional matrix")
    if levels < 2:
        raise ValueError("levels must be >= 2")

    if per_channel:
        minima = matrix.min(axis=0)
        maxima = matrix.max(axis=0)
        ranges = maxima - minima
        steps = np.zeros(matrix.shape[1], dtype=np.float64)
        active = ranges > 0
        steps[active] = ranges[active] / (levels - 1)
        quantized = matrix.copy()
        clipping_count = 0
        for channel in np.flatnonzero(active):
            step = steps[channel]
            scaled = (matrix[:, channel] - minima[channel]) / step
            raw_indices = np.floor(scaled + 0.5)
            clipping_count += int(np.count_nonzero((raw_indices < 0) | (raw_indices > levels - 1)))
            indices = np.clip(raw_indices, 0, levels - 1)
            quantized[:, channel] = minima[channel] + indices * step
        radius = steps / 2.0
        return quantized, steps, radius, clipping_count

    minimum = float(matrix.min())
    maximum = float(matrix.max())
    if maximum == minimum:
        return matrix.copy(), 0.0, np.zeros(matrix.shape[1], dtype=np.float64), 0
    step = (maximum - minimum) / (levels - 1)
    scaled = (matrix - minimum) / step
    raw_indices = np.floor(scaled + 0.5)
    clipping_count = int(np.count_nonzero((raw_indices < 0) | (raw_indices > levels - 1)))
    indices = np.clip(raw_indices, 0, levels - 1)
    quantized = minimum + indices * step
    radius = np.full(matrix.shape[1], step / 2.0, dtype=np.float64)
    return quantized, step, radius, clipping_count


def certificate_bounds(
    adjacency: np.ndarray,
    downstream_weight: np.ndarray,
    radius: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    adjacency64 = np.asarray(adjacency, dtype=np.float64)
    weight64 = np.asarray(downstream_weight, dtype=np.float64)
    radius64 = np.asarray(radius, dtype=np.float64)
    if adjacency64.ndim != 2 or adjacency64.shape[0] != adjacency64.shape[1]:
        raise ValueError("adjacency must be square")
    if weight64.ndim != 2 or weight64.shape[0] != radius64.size:
        raise ValueError("radius must match the input dimension of downstream_weight")
    if np.any(radius64 < 0):
        raise ValueError("radius must be nonnegative")

    absolute_adjacency = np.abs(adjacency64)
    coefficient = absolute_adjacency @ absolute_adjacency @ np.ones(adjacency64.shape[0])
    absolute_weight = np.abs(weight64)
    proposed = coefficient[:, None] * (radius64[:, None] * absolute_weight).sum(axis=0)[None, :]
    minkowski = (
        coefficient[:, None]
        * np.linalg.norm(radius64)
        * np.linalg.norm(weight64, axis=0)[None, :]
    )
    global_column = (
        coefficient[:, None]
        * float(np.max(radius64))
        * absolute_weight.sum(axis=0)[None, :]
    )
    scalar = (
        coefficient[:, None]
        * float(np.max(radius64))
        * float(absolute_weight.sum())
    )
    return proposed, minkowski, global_column, scalar


def rowwise_quantize(
    values: np.ndarray,
    levels: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError("values must be a two-dimensional matrix")
    if levels < 2:
        raise ValueError("levels must be >= 2")
    minima = matrix.min(axis=1, keepdims=True)
    maxima = matrix.max(axis=1, keepdims=True)
    ranges = maxima - minima
    steps = np.where(ranges > 0, ranges / (levels - 1), 0.0)
    safe_steps = np.where(steps > 0, steps, 1.0)
    raw_indices = np.floor((matrix - minima) / safe_steps + 0.5)
    clipping_count = int(np.count_nonzero((raw_indices < 0) | (raw_indices > levels - 1)))
    indices = np.clip(raw_indices, 0, levels - 1)
    quantized = np.where(steps > 0, minima + indices * steps, matrix)
    radius = np.repeat(steps / 2.0, matrix.shape[1], axis=1)
    return quantized, steps, radius, clipping_count


def certificate_bounds_matrix(
    adjacency: np.ndarray,
    downstream_weight: np.ndarray,
    radius_matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    adjacency64 = np.asarray(adjacency, dtype=np.float64)
    weight64 = np.asarray(downstream_weight, dtype=np.float64)
    radius64 = np.asarray(radius_matrix, dtype=np.float64)
    if adjacency64.ndim != 2 or adjacency64.shape[0] != adjacency64.shape[1]:
        raise ValueError("adjacency must be square")
    if radius64.ndim != 2 or radius64.shape[1] != weight64.shape[0]:
        raise ValueError("radius_matrix must be N x H matching downstream_weight")
    if np.any(radius64 < 0):
        raise ValueError("radius must be nonnegative")

    absolute_adjacency = np.abs(adjacency64)
    absolute_weight = np.abs(weight64)
    proposed = absolute_adjacency @ absolute_adjacency @ radius64 @ absolute_weight
    coefficient = absolute_adjacency @ absolute_adjacency
    row_radius_norm = np.linalg.norm(radius64, axis=1)
    minkowski = (coefficient @ row_radius_norm)[:, None] * np.linalg.norm(weight64, axis=0)[None, :]
    coefficient_row = coefficient @ np.ones(adjacency64.shape[0])
    global_column = (
        coefficient_row[:, None]
        * float(np.max(radius64))
        * absolute_weight.sum(axis=0)[None, :]
    )
    scalar = (
        coefficient_row[:, None]
        * float(np.max(radius64))
        * float(absolute_weight.sum())
    )
    return proposed, minkowski, global_column, scalar


def evaluate_synthetic_chain() -> dict:
    adjacency = np.array(
        [[0.5, 0.3, 0.2], [0.1, 0.6, 0.3], [0.2, 0.2, 0.6]],
        dtype=np.float64,
    )
    features = np.array(
        [[0.2, -0.1, 0.4], [0.5, 0.3, -0.2], [-0.4, 0.7, 0.1]],
        dtype=np.float64,
    )
    weight0 = np.array([[0.3, -0.2], [0.4, 0.1], [-0.5, 0.6]], dtype=np.float64)
    bias0 = np.array([0.05, -0.1], dtype=np.float64)
    weight1 = np.array([[0.7, -0.4], [-0.2, 0.8]], dtype=np.float64)
    bias1 = np.array([0.1, -0.1], dtype=np.float64)

    message = features @ weight0
    quantized, _, radius, clipping_count = uniform_quantize(message, levels=8, per_channel=True)
    hidden = np.maximum(adjacency @ message + bias0, 0.0)
    hidden_quantized = np.maximum(adjacency @ quantized + bias0, 0.0)
    logits = adjacency @ hidden @ weight1 + bias1
    logits_quantized = adjacency @ hidden_quantized @ weight1 + bias1
    actual = np.abs(logits - logits_quantized)
    proposed, minkowski, _, _ = certificate_bounds(adjacency, weight1, radius)
    tolerance = 1e-10 + 1e-12 * np.abs(proposed)
    return {
        "containment": bool(np.all(actual <= proposed + tolerance)),
        "minkowski_valid": bool(np.all(proposed <= minkowski + tolerance)),
        "actual_rms": float(np.sqrt(np.mean(actual**2))),
        "clipping_count": clipping_count,
    }
