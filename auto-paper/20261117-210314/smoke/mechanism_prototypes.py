"""Small, auditable primitives for diversified GNN→SNN conversion mechanisms."""

from __future__ import annotations

import numpy as np


def signed_split(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values)
    if not np.issubdtype(values.dtype, np.number):
        raise ValueError("values must be numeric")
    return np.maximum(values, 0), np.maximum(-values, 0)


def permutation_equivariant_mean(features: np.ndarray, adjacency: np.ndarray) -> np.ndarray:
    features = np.asarray(features, dtype=np.float64)
    adjacency = np.asarray(adjacency, dtype=np.float64)
    if features.ndim != 2 or adjacency.shape != (features.shape[0], features.shape[0]):
        raise ValueError("feature/adjacency shape mismatch")
    return adjacency @ features


def radial_event_encode(points: np.ndarray, *, levels: int = 8) -> dict:
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] < 1 or levels < 1:
        raise ValueError("points must be [N,D] and levels positive")
    norms = np.linalg.norm(points, axis=1)
    safe = np.maximum(norms, np.finfo(np.float64).eps)
    directions = points / safe[:, None]
    maximum = float(norms.max()) if len(norms) else 1.0
    step = maximum / levels
    quantized = np.round(norms / step) * step
    return {
        "norm_quantized": quantized,
        "directions": directions,
        "reconstructed": quantized[:, None] * directions,
        "event_levels": int(levels),
        "step": step,
    }


def centroid_event_encode(points: np.ndarray, *, levels: int = 8) -> dict:
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[0] == 0:
        raise ValueError("points must be a nonempty [N,D] array")
    centered = points - points.mean(axis=0, keepdims=True)
    scale = np.sqrt(np.mean(centered**2, axis=0))
    scale = np.where(scale > 0, scale, 1.0)
    normalized = centered / scale
    output = radial_event_encode(normalized, levels=levels)
    output["reconstructed"] = output["reconstructed"] * scale
    output["directions"] = output["directions"] * scale
    output["scale"] = scale
    output["centroid"] = points.mean(axis=0)
    output["centered"] = centered
    return output


def centroid_quantile_event_encode(points: np.ndarray, *, levels: int = 8) -> dict:
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[0] < levels:
        raise ValueError("points must contain at least `levels` rows")
    centered = points - points.mean(axis=0, keepdims=True)
    scale = np.sqrt(np.mean(centered**2, axis=0))
    scale = np.where(scale > 0, scale, 1.0)
    normalized = centered / scale
    norms = np.linalg.norm(normalized, axis=1)
    directions = np.divide(normalized, norms[:, None], out=np.zeros_like(normalized), where=norms[:, None] > 0)
    edges = np.quantile(norms, np.linspace(0.0, 1.0, levels + 1))
    bins = np.clip(np.searchsorted(edges[1:-1], norms, side="right"), 0, levels - 1)
    representatives = np.array([np.median(norms[bins == index]) if np.any(bins == index) else edges[index + 1] for index in range(levels)])
    quantized_norms = representatives[bins]
    reconstructed = quantized_norms[:, None] * directions * scale
    return {
        "reconstructed": reconstructed,
        "norm_quantized": quantized_norms,
        "bins": bins,
        "representatives": representatives,
        "scale": scale,
        "centered": centered,
    }


def causal_residual_frames(frames: np.ndarray) -> np.ndarray:
    frames = np.asarray(frames, dtype=np.float64)
    if frames.ndim < 2 or frames.shape[0] < 2:
        raise ValueError("frames must contain at least two time steps")
    return np.diff(frames, axis=0)


def low_rank_message(matrix: np.ndarray, *, rank: int) -> dict:
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim != 2 or rank < 1 or rank > min(matrix.shape):
        raise ValueError("rank must be between 1 and min(matrix.shape)")
    left, singular, right = np.linalg.svd(matrix, full_matrices=False)
    reconstructed = (left[:, :rank] * singular[:rank]) @ right[:rank]
    denominator = float(np.linalg.norm(matrix)) or 1.0
    return {
        "rank": int(rank),
        "compressed_dimension": int(rank * (matrix.shape[0] + matrix.shape[1])),
        "reconstructed": reconstructed,
        "relative_error": float(np.linalg.norm(matrix - reconstructed) / denominator),
        "singular_values": singular.copy(),
    }
