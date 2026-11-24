"""Operator-aligned low-rank and residual-event primitives."""

from __future__ import annotations

import numpy as np
import torch


def _device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def low_rank_reconstruct(matrix: np.ndarray, rank: int) -> dict:
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim != 2 or rank < 1 or rank > min(matrix.shape):
        raise ValueError("invalid matrix or rank")
    tensor = torch.as_tensor(matrix, dtype=torch.float32, device=_device())
    left, singular, right = torch.linalg.svd(tensor, full_matrices=False)
    reconstructed = ((left[:, :rank] * singular[:rank]) @ right[:rank]).cpu().numpy().astype(np.float64)
    denominator = float(np.linalg.norm(matrix)) or 1.0
    return {
        "reconstructed": reconstructed,
        "rank": int(rank),
        "relative_error": float(np.linalg.norm(matrix - reconstructed) / denominator),
        "compressed_dimension": int(rank * sum(matrix.shape)),
        "device": str(_device()),
    }


def select_residual_indices(residual: np.ndarray, downstream_weight: np.ndarray, *, count: int) -> np.ndarray:
    residual = np.asarray(residual, dtype=np.float64)
    weight = np.asarray(downstream_weight, dtype=np.float64)
    if residual.ndim != 2 or weight.ndim != 2 or residual.shape[1] != weight.shape[0]:
        raise ValueError("residual/weight shape mismatch")
    if count < 1 or count > residual.size:
        raise ValueError("count must be in [1, residual.size]")
    sensitivity = np.abs(residual) * np.abs(weight).sum(axis=1)[None, :]
    flat = np.argpartition(sensitivity.ravel(), -count)[-count:]
    return np.column_stack(np.unravel_index(flat, residual.shape)).astype(np.int64)


def residual_reconstruct(residual: np.ndarray, indices: np.ndarray) -> np.ndarray:
    residual = np.asarray(residual, dtype=np.float64)
    indices = np.asarray(indices, dtype=np.int64)
    if residual.ndim != 2 or indices.ndim != 2 or indices.shape[1] != 2:
        raise ValueError("invalid residual or indices")
    output = np.zeros_like(residual)
    if len(indices):
        output[indices[:, 0], indices[:, 1]] = residual[indices[:, 0], indices[:, 1]]
    return output


def random_residual_indices(shape: tuple[int, int], *, count: int, seed: int) -> np.ndarray:
    if len(shape) != 2 or count < 1 or count > shape[0] * shape[1]:
        raise ValueError("invalid shape or count")
    generator = np.random.default_rng(seed)
    flat = generator.choice(shape[0] * shape[1], size=count, replace=False)
    return np.column_stack(np.unravel_index(flat, shape)).astype(np.int64)


def storage_bits(shape: tuple[int, int], *, rank: int, residual_count: int) -> int:
    if len(shape) != 2 or rank < 1 or residual_count < 0:
        raise ValueError("invalid storage parameters")
    coordinate_values = rank * sum(shape)
    index_bits = int(np.ceil(np.log2(shape[0] * shape[1]))) + 2
    return int(coordinate_values * 32 + residual_count * (32 + index_bits))


def uniform_residual_reconstruct(residual: np.ndarray, *, bits: int) -> np.ndarray:
    residual = np.asarray(residual, dtype=np.float64)
    if residual.ndim != 2 or bits < 1:
        raise ValueError("invalid residual or bits")
    maximum = float(np.max(np.abs(residual)))
    if maximum == 0.0:
        return np.zeros_like(residual)
    levels = max(1, 2 ** (bits - 1) - 1)
    return np.rint(np.clip(residual / maximum * levels, -levels, levels)) / levels * maximum


def rate_convert_hidden(hidden: np.ndarray, *, t_steps: int) -> np.ndarray:
    hidden = np.asarray(hidden, dtype=np.float64)
    if hidden.ndim != 2 or t_steps < 1:
        raise ValueError("hidden must be [N,H] and t_steps positive")
    positive = np.maximum(hidden, 0.0)
    theta = np.maximum(positive.max(axis=0, keepdims=True), 1e-8)
    counts = np.rint(positive / theta * t_steps)
    return counts * theta / t_steps
