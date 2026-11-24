import numpy as np
import pytest

from research.lr_v2_core import (
    basis_random,
    basis_svd,
    dense_uniform_at_budget,
    one_spike_at_budget,
    select_residual_indices,
    sparse_cost_bits,
    sparse_reconstruct,
)


def test_basis_shapes_and_errors():
    matrix = np.random.default_rng(1).normal(size=(20, 9))
    svd = basis_svd(matrix, rank=3)
    random = basis_random(matrix, rank=3, seed=2)
    assert svd["reconstructed"].shape == matrix.shape
    assert random["reconstructed"].shape == matrix.shape
    assert svd["relative_error"] <= random["relative_error"] + 1e-12


def test_selection_modes_are_deterministic():
    residual = np.array([[5.0, -4.0], [0.2, 3.0]])
    weight = np.array([[1.0, 0.0], [0.0, 10.0]])
    downstream = select_residual_indices(residual, weight, count=1, mode="downstream")
    top = select_residual_indices(residual, weight, count=1, mode="top_abs")
    assert downstream.tolist() == [[0, 1]]
    assert top.tolist() == [[0, 0]]


def test_downstream_logit_mode_uses_output_path():
    residual = np.array([[2.0, 1.0], [1.0, 1.0]])
    first = np.array([[1.0, 0.0], [0.0, 1.0]])
    output = np.array([[10.0, 0.0], [0.0, 1.0]])
    indices = select_residual_indices(residual, first, count=1, mode="downstream_logit", output_weight=output)
    assert indices.tolist() == [[0, 0]]


def test_downstream_jacobian_mode_uses_exact_sensitivity():
    residual = np.array([[2.0, 1.0], [1.0, 1.0]])
    jacobian = np.array([[10.0, 1.0], [1.0, 1.0]])
    indices = select_residual_indices(
        residual,
        np.ones((2, 2)),
        count=1,
        mode="downstream_jacobian",
        jacobian_norm=jacobian,
    )
    assert indices.tolist() == [[0, 0]]


def test_sparse_cost_and_reconstruction():
    residual = np.arange(12, dtype=float).reshape(3, 4)
    indices = select_residual_indices(residual, np.ones((4, 2)), count=2, mode="top_abs")
    reconstructed = sparse_reconstruct(residual, indices)
    assert sparse_cost_bits(residual.shape, count=2) == 2 * 64
    assert np.count_nonzero(reconstructed) == 2


def test_dense_uniform_matches_target_with_padding():
    residual = np.random.default_rng(4).normal(size=(8, 5))
    result = dense_uniform_at_budget(residual, target_bits=1000)
    assert result["padded_bits"] == 1000
    assert result["payload_bits"] <= 1000
    assert result["reconstructed"].shape == residual.shape


def test_one_spike_uses_more_coefficients_at_same_budget():
    residual = np.random.default_rng(5).normal(size=(30, 7))
    result = one_spike_at_budget(residual, target_bits=1280)
    assert result["padded_bits"] == 1280
    assert result["coefficient_count"] > 0
    assert np.isfinite(result["reconstructed"]).all()


def test_invalid_modes_rejected():
    with pytest.raises(ValueError):
        select_residual_indices(np.ones((2, 2)), np.ones((2, 2)), count=1, mode="bad")
