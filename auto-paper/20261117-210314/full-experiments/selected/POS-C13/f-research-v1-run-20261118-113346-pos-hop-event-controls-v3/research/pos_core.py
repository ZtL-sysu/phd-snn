from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class EncodedValues:
    reconstructed: np.ndarray
    representatives: np.ndarray
    assignments: np.ndarray
    escape_mask: np.ndarray
    alphabet_size: int
    escape_fraction: float


def hop_features(adjacency: np.ndarray, features: np.ndarray, hops: int = 3) -> np.ndarray:
    adjacency64 = np.asarray(adjacency, dtype=np.float64)
    features64 = np.asarray(features, dtype=np.float64)
    row_sum = adjacency64.sum(axis=1, keepdims=True)
    normalized = adjacency64 / np.where(row_sum > 0, row_sum, 1.0)
    outputs = [features64]
    current = features64
    for _ in range(hops):
        current = normalized @ current
        outputs.append(current)
    return np.concatenate(outputs, axis=1)


def shuffle_hop_blocks(values: np.ndarray, feature_dim: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[1] % feature_dim != 0:
        raise ValueError("values must be N x (hops*feature_dim)")
    hop_count = matrix.shape[1] // feature_dim
    permutation = np.random.default_rng(seed).permutation(hop_count)
    blocks = [matrix[:, index * feature_dim : (index + 1) * feature_dim] for index in permutation]
    return np.concatenate(blocks, axis=1), permutation


def serialized_bit_ledger(nodes: int, channels: int, escape_fraction: float) -> dict:
    if nodes <= 0 or channels <= 0:
        raise ValueError("nodes and channels must be positive")
    if not 0 <= escape_fraction < 1:
        raise ValueError("escape_fraction must be in [0,1)")
    average_bits = 4.0 + 32.0 * escape_fraction + 256.0 / nodes
    total_bits = average_bits * nodes * channels
    return {
        "symbol_bits_per_value": 4.0,
        "escape_payload_bits_per_value": 32.0 * escape_fraction,
        "codebook_bits_per_value": 256.0 / nodes,
        "average_bits_per_value": average_bits,
        "total_bits": total_bits,
        "float32_bits": 32.0,
        "storage_reduction": 32.0 / average_bits,
    }


def _lloyd_representatives(values: np.ndarray, levels: int, iterations: int = 25) -> np.ndarray:
    representatives = np.empty((values.shape[1], levels), dtype=np.float64)
    for channel in range(values.shape[1]):
        column = np.sort(values[:, channel])
        quantiles = (np.arange(levels, dtype=np.float64) + 0.5) / levels
        centers = np.quantile(column, quantiles)
        for _ in range(iterations):
            distances = np.abs(column[:, None] - centers[None, :])
            assignment = np.argmin(distances, axis=1)
            updated = centers.copy()
            for level in range(levels):
                members = column[assignment == level]
                if members.size:
                    updated[level] = members.mean()
            if np.allclose(updated, centers, rtol=0, atol=1e-12):
                centers = updated
                break
            centers = updated
        representatives[channel] = np.sort(centers)
    return representatives


def _assign(values: np.ndarray, representatives: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    assignments = np.empty(values.shape, dtype=np.int16)
    reconstructed = np.empty_like(values, dtype=np.float64)
    for channel in range(values.shape[1]):
        centers = representatives[channel]
        distances = np.abs(values[:, channel, None] - centers[None, :])
        assignment = np.argmin(distances, axis=1)
        assignments[:, channel] = assignment
        reconstructed[:, channel] = centers[assignment]
    return reconstructed, assignments


def _top_fraction_escape_mask(errors: np.ndarray, escape_fraction: float) -> tuple[np.ndarray, float]:
    mask = np.zeros(errors.shape, dtype=bool)
    count = int(round(escape_fraction * errors.size))
    if not count:
        return mask, 0.0
    threshold = float(np.partition(errors.ravel(), -count)[-count])
    return errors >= threshold, threshold


def hybrid_lloyd_escape_encode(
    values: np.ndarray,
    levels: int,
    escape_fraction: float,
    fit_mask: np.ndarray | None = None,
    escape_mask: np.ndarray | None = None,
) -> EncodedValues:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError("values must be a matrix")
    if levels < 2:
        raise ValueError("levels must be >=2")
    if not 0 <= escape_fraction < 1:
        raise ValueError("escape_fraction must be in [0,1)")
    selected = np.ones(matrix.shape[0], dtype=bool) if fit_mask is None else np.asarray(fit_mask, dtype=bool)
    if selected.shape != (matrix.shape[0],):
        raise ValueError("fit_mask shape mismatch")
    representatives = _lloyd_representatives(matrix[selected], levels)
    base_reconstructed, assignments = _assign(matrix, representatives)
    errors = np.abs(matrix - base_reconstructed)
    if escape_mask is None:
        mask, _ = _top_fraction_escape_mask(errors, escape_fraction)
    else:
        mask = np.asarray(escape_mask, dtype=bool)
        if mask.shape != matrix.shape:
            raise ValueError("escape_mask shape mismatch")
    reconstructed = np.where(mask, matrix, base_reconstructed)
    return EncodedValues(
        reconstructed=reconstructed,
        representatives=representatives,
        assignments=assignments,
        escape_mask=mask,
        alphabet_size=levels + 1,
        escape_fraction=float(mask.mean()),
    )


def relative_frobenius_error(reference: np.ndarray, estimate: np.ndarray) -> float:
    reference64 = np.asarray(reference, dtype=np.float64)
    estimate64 = np.asarray(estimate, dtype=np.float64)
    denominator = np.linalg.norm(reference64)
    return float(np.linalg.norm(reference64 - estimate64) / denominator) if denominator else 0.0


def ordered_codebook_shuffle_error(
    values: np.ndarray,
    encoded: EncodedValues,
    feature_dim: int,
    seed: int,
    permutation: np.ndarray | None = None,
) -> dict:
    matrix = np.asarray(values, dtype=np.float64)
    if permutation is None:
        shuffled, permutation = shuffle_hop_blocks(matrix, feature_dim, seed)
    else:
        permutation = np.asarray(permutation, dtype=int)
        blocks = [matrix[:, index * feature_dim : (index + 1) * feature_dim] for index in permutation]
        shuffled = np.concatenate(blocks, axis=1)
    shuffled_base, _ = _assign(shuffled, encoded.representatives)
    shuffled_mask, _ = _top_fraction_escape_mask(np.abs(shuffled - shuffled_base), encoded.escape_fraction)
    shuffled_reconstructed = np.where(shuffled_mask, shuffled, shuffled_base)
    ordered_error = relative_frobenius_error(matrix, encoded.reconstructed)
    shuffled_error = relative_frobenius_error(shuffled, shuffled_reconstructed)
    return {
        "ordered_error": ordered_error,
        "shuffled_error": shuffled_error,
        "error_ratio": shuffled_error / ordered_error if ordered_error else float("inf"),
        "permutation": permutation.tolist(),
    }
