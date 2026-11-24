"""Exact serialized-cost primitives for sparse residual coefficient coding."""

from __future__ import annotations

import numpy as np
import torch


def _device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def basis_svd(matrix: np.ndarray, rank: int) -> dict:
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim != 2 or rank < 1 or rank > min(matrix.shape):
        raise ValueError("invalid matrix or rank")
    tensor = torch.as_tensor(matrix, dtype=torch.float32, device=_device())
    left, singular, right = torch.linalg.svd(tensor, full_matrices=False)
    reconstructed = ((left[:, :rank] * singular[:rank]) @ right[:rank]).cpu().numpy().astype(np.float64)
    error = float(np.linalg.norm(matrix - reconstructed) / max(np.linalg.norm(matrix), 1e-12))
    return {
        "reconstructed": reconstructed,
        "relative_error": error,
        "basis_bits": int((matrix.shape[0] * rank + rank + rank * matrix.shape[1]) * 32),
        "method": "svd",
    }


def basis_random(matrix: np.ndarray, rank: int, *, seed: int) -> dict:
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim != 2 or rank < 1 or rank > min(matrix.shape):
        raise ValueError("invalid matrix or rank")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    projection = torch.randn((matrix.shape[1], rank), generator=generator, dtype=torch.float32)
    projection = torch.linalg.qr(projection, mode="reduced")[0].to(_device())
    tensor = torch.as_tensor(matrix, dtype=torch.float32, device=_device())
    reconstructed = ((tensor @ projection) @ projection.T).cpu().numpy().astype(np.float64)
    error = float(np.linalg.norm(matrix - reconstructed) / max(np.linalg.norm(matrix), 1e-12))
    return {
        "reconstructed": reconstructed,
        "relative_error": error,
        "basis_bits": int((matrix.shape[0] * rank + rank * matrix.shape[1]) * 32),
        "method": "random_projection",
    }


def select_residual_indices(
    residual: np.ndarray,
    downstream_weight: np.ndarray,
    *,
    count: int,
    mode: str,
    seed: int = 0,
    output_weight: np.ndarray | None = None,
    jacobian_norm: np.ndarray | None = None,
) -> np.ndarray:
    residual = np.asarray(residual, dtype=np.float64)
    weight = np.asarray(downstream_weight, dtype=np.float64)
    if residual.ndim != 2 or weight.ndim != 2 or residual.shape[1] != weight.shape[0]:
        raise ValueError("shape mismatch")
    if count < 1 or count > residual.size:
        raise ValueError("count out of range")
    sensitivity = np.abs(weight).sum(axis=1)[None, :]
    if mode == "downstream":
        score = np.abs(residual) * sensitivity
        flat = np.argpartition(score.ravel(), -count)[-count:]
    elif mode == "downstream_hidden":
        score = residual**2 * np.sum(weight**2, axis=1)[None, :]
        flat = np.argpartition(score.ravel(), -count)[-count:]
    elif mode == "downstream_logit":
        if output_weight is None:
            raise ValueError("downstream_logit requires output_weight")
        path = weight @ np.asarray(output_weight, dtype=np.float64)
        score = residual**2 * np.sum(path**2, axis=1)[None, :]
        flat = np.argpartition(score.ravel(), -count)[-count:]
    elif mode == "downstream_jacobian":
        if jacobian_norm is None:
            raise ValueError("downstream_jacobian requires jacobian_norm")
        jacobian_norm = np.asarray(jacobian_norm, dtype=np.float64)
        if jacobian_norm.shape != residual.shape:
            raise ValueError("jacobian_norm shape mismatch")
        score = residual**2 * jacobian_norm**2
        flat = np.argpartition(score.ravel(), -count)[-count:]
    elif mode == "top_abs":
        flat = np.argpartition(np.abs(residual).ravel(), -count)[-count:]
    elif mode == "random":
        flat = np.random.default_rng(seed).choice(residual.size, size=count, replace=False)
    elif mode == "a2q_node_budget":
        row_score = (np.abs(residual) * sensitivity).sum(axis=1)
        rows = np.argsort(-row_score)
        flat_list: list[int] = []
        row_cursor = 0
        per_row = max(1, count // residual.shape[0])
        while len(flat_list) < count and row_cursor < len(rows):
            row = int(rows[row_cursor])
            candidates = np.argsort(-np.abs(residual[row]))[:per_row]
            flat_list.extend((row * residual.shape[1] + int(column)) for column in candidates)
            row_cursor += 1
        if len(flat_list) < count:
            remaining = np.setdiff1d(np.arange(residual.size), np.asarray(flat_list, dtype=np.int64), assume_unique=False)
            order = np.argsort(-np.abs(residual.ravel()[remaining]))
            flat_list.extend(remaining[order][: count - len(flat_list)].tolist())
        flat = np.asarray(flat_list[:count], dtype=np.int64)
    else:
        raise ValueError(f"unknown mode: {mode}")
    return np.column_stack(np.unravel_index(np.asarray(flat, dtype=np.int64), residual.shape)).astype(np.int64)


def sparse_reconstruct(residual: np.ndarray, indices: np.ndarray) -> np.ndarray:
    residual = np.asarray(residual, dtype=np.float64)
    indices = np.asarray(indices, dtype=np.int64)
    output = np.zeros_like(residual)
    if len(indices):
        output[indices[:, 0], indices[:, 1]] = residual[indices[:, 0], indices[:, 1]]
    return output


def sparse_cost_bits(shape: tuple[int, int], *, count: int) -> int:
    return int(count * 64)


def dense_uniform_at_budget(residual: np.ndarray, *, target_bits: int) -> dict:
    residual = np.asarray(residual, dtype=np.float64)
    values = residual.size
    scale_bits = residual.shape[1] * 32
    best_bits = 1
    for bits in range(1, 9):
        if values * bits + scale_bits <= target_bits:
            best_bits = bits
        else:
            break
    maximum = float(np.max(np.abs(residual))) or 1.0
    levels = max(1, 2 ** (best_bits - 1) - 1)
    reconstructed = np.rint(np.clip(residual / maximum * levels, -levels, levels)) / levels * maximum
    payload_bits = values * best_bits + scale_bits
    return {
        "reconstructed": reconstructed,
        "bits_per_value": best_bits,
        "payload_bits": int(payload_bits),
        "padded_bits": int(target_bits),
        "padding_bits": int(target_bits - payload_bits),
    }


def one_spike_at_budget(residual: np.ndarray, *, target_bits: int) -> dict:
    residual = np.asarray(residual, dtype=np.float64)
    bits_per_coefficient = 35
    count = min(residual.size, int(target_bits // bits_per_coefficient))
    if count < 1:
        raise ValueError("target too small for one-spike coefficient")
    indices = select_residual_indices(residual, np.ones((residual.shape[1], 1)), count=count, mode="top_abs")
    maximum = float(np.max(np.abs(residual))) or 1.0
    levels = 3
    output = np.zeros_like(residual)
    values = residual[indices[:, 0], indices[:, 1]]
    quantized = np.rint(np.clip(values / maximum * levels, -levels, levels)) / levels * maximum
    output[indices[:, 0], indices[:, 1]] = quantized
    payload_bits = count * bits_per_coefficient
    return {
        "reconstructed": output,
        "coefficient_count": int(count),
        "payload_bits": int(payload_bits),
        "padded_bits": int(target_bits),
        "padding_bits": int(target_bits - payload_bits),
    }


def rate_convert_hidden(hidden: np.ndarray, *, t_steps: int) -> np.ndarray:
    hidden = np.maximum(np.asarray(hidden, dtype=np.float64), 0.0)
    theta = np.maximum(hidden.max(axis=0, keepdims=True), 1e-8)
    counts = np.rint(hidden / theta * t_steps)
    return counts * theta / t_steps
