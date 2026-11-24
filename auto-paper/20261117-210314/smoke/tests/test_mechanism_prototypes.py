import numpy as np
import pytest

from smoke.mechanism_prototypes import (
    causal_residual_frames,
    centroid_event_encode,
    centroid_quantile_event_encode,
    low_rank_message,
    permutation_equivariant_mean,
    radial_event_encode,
    signed_split,
)


def test_signed_split_reconstructs_signed_messages_exactly():
    x = np.array([[1.25, -0.5, 0.0], [-2.0, 3.0, -0.125]], dtype=np.float64)
    positive, negative = signed_split(x)
    assert np.array_equal(positive, np.maximum(x, 0))
    assert np.array_equal(negative, np.maximum(-x, 0))
    assert np.array_equal(positive - negative, x)


def test_permutation_equivariant_mean_commutes_with_node_permutation():
    features = np.array([[1.0, 2.0], [3.0, -1.0], [0.5, 4.0]])
    adjacency = np.array([[0.5, 0.5, 0.0], [0.0, 0.25, 0.75], [1.0, 0.0, 0.0]])
    permutation = np.array([2, 0, 1])
    direct = permutation_equivariant_mean(features, adjacency)
    permuted = permutation_equivariant_mean(features[permutation], adjacency[np.ix_(permutation, permutation)])
    assert np.allclose(permuted, direct[permutation], atol=1e-12)


def test_radial_event_encoding_is_rotation_equivariant():
    points = np.array([[1.0, 2.0, -0.5], [-2.0, 0.25, 3.0]], dtype=np.float64)
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    encoded = radial_event_encode(points, levels=8)
    rotated = radial_event_encode(points @ rotation.T, levels=8)
    assert np.allclose(rotated["reconstructed"], encoded["reconstructed"] @ rotation.T, atol=1e-12)
    assert np.allclose(rotated["norm_quantized"], encoded["norm_quantized"], atol=1e-12)


def test_centroid_event_encoding_is_translation_invariant():
    points = np.array([[1.0, 2.0], [-1.0, 0.5], [3.0, -2.0]])
    shift = np.array([12.0, -7.0])
    direct = centroid_event_encode(points, levels=8)
    translated = centroid_event_encode(points + shift, levels=8)
    assert np.allclose(translated["reconstructed"], direct["reconstructed"], atol=1e-12)
    assert np.allclose(translated["norm_quantized"], direct["norm_quantized"], atol=1e-12)


def test_centroid_quantile_event_encoding_is_translation_invariant():
    rng = np.random.default_rng(9)
    points = rng.normal(size=(32, 3)) * np.array([3.0, 1.0, 0.25])
    direct = centroid_quantile_event_encode(points, levels=8)
    translated = centroid_quantile_event_encode(points + np.array([100.0, -20.0, 4.0]), levels=8)
    assert np.allclose(translated["reconstructed"], direct["reconstructed"], atol=1e-10)
    assert np.array_equal(translated["bins"], direct["bins"])


def test_causal_residual_frames_reconstruct_prefix_without_future():
    frames = np.array([[[1.0, 2.0]], [[1.5, 1.0]], [[0.5, 3.0]], [[2.0, 0.0]]])
    residuals = causal_residual_frames(frames)
    reconstructed = np.cumsum(residuals, axis=0)
    assert np.allclose(reconstructed, frames[1:] - frames[0])
    future_changed = frames.copy()
    future_changed[-1] += 100
    changed_residuals = causal_residual_frames(future_changed)
    assert np.allclose(changed_residuals[:-1], residuals[:-1])


def test_low_rank_message_reports_error_and_rank_budget():
    rng = np.random.default_rng(3)
    matrix = rng.normal(size=(12, 7))
    result = low_rank_message(matrix, rank=2)
    assert result["rank"] == 2
    assert result["compressed_dimension"] == 2 * (12 + 7)
    assert result["relative_error"] < 1.0
    assert result["reconstructed"].shape == matrix.shape
    assert result["relative_error"] >= 0.0


def test_low_rank_message_rejects_invalid_rank():
    with pytest.raises(ValueError, match="rank"):
        low_rank_message(np.ones((3, 3)), rank=0)
