import numpy as np
import pytest

from research.lr_core import (
    low_rank_reconstruct,
    random_residual_indices,
    rate_convert_hidden,
    residual_reconstruct,
    select_residual_indices,
    storage_bits,
    uniform_residual_reconstruct,
)


def test_low_rank_reconstruct_returns_exact_rank_shape():
    matrix = np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]])
    result = low_rank_reconstruct(matrix, rank=2)
    assert result["reconstructed"].shape == matrix.shape
    assert result["rank"] == 2
    assert result["relative_error"] < 1.0


def test_residual_selection_uses_downstream_sensitivity():
    residual = np.array([[5.0, -1.0], [0.1, 4.0]])
    weight = np.array([[1.0, 0.0], [0.0, 10.0]])
    indices = select_residual_indices(residual, weight, count=1)
    assert indices.tolist() == [[1, 1]]
    reconstructed = residual_reconstruct(residual, indices)
    assert reconstructed[1, 1] == 4.0
    assert reconstructed[0, 0] == 0.0


def test_rate_convert_hidden_preserves_shape():
    hidden = np.array([[0.0, 0.7], [1.2, 0.1]])
    decoded = rate_convert_hidden(hidden, t_steps=4)
    assert decoded.shape == hidden.shape
    assert np.all(decoded >= 0)


def test_invalid_residual_count_rejected():
    with pytest.raises(ValueError):
        select_residual_indices(np.ones((2, 2)), np.ones((2, 2)), count=0)


def test_storage_bits_counts_coordinates_values_and_indices():
    assert storage_bits((4, 8), rank=2, residual_count=3) == 2 * 12 * 32 + 3 * (32 + 7)


def test_random_residual_is_deterministic():
    residual = np.arange(12, dtype=float).reshape(3, 4)
    first = residual_reconstruct(residual, random_residual_indices(residual.shape, count=3, seed=4))
    second = residual_reconstruct(residual, random_residual_indices(residual.shape, count=3, seed=4))
    assert np.array_equal(first, second)


def test_uniform_residual_reconstructs_bounded_values():
    residual = np.array([[-1.0, -0.2, 0.3, 1.0]])
    quantized = uniform_residual_reconstruct(residual, bits=2)
    assert quantized.shape == residual.shape
    assert np.max(np.abs(quantized)) <= 1.0 + 1e-12


def test_uniform_residual_supports_one_bit_without_nan():
    quantized = uniform_residual_reconstruct(np.array([[-1.0, 0.0, 1.0]]), bits=1)
    assert np.isfinite(quantized).all()
    assert np.all(np.abs(quantized) <= 1.0 + 1e-12)
