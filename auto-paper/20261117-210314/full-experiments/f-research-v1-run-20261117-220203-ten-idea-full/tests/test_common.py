import numpy as np
import pytest

from research.common import (
    classification_metrics,
    initial_plus_residual,
    hybrid_lloyd_escape_quantize,
    low_rank_svd,
    per_channel_quantize,
    per_channel_quantile_quantize,
    per_channel_lloyd_quantize,
    random_projection,
    rotation_matrix,
    stratified_splits,
    TorchLinearProbe,
    top2_readout,
    uniform_quantize,
)


def test_stratified_splits_are_disjoint_and_complete():
    labels = np.repeat([0, 1, 2], 20)
    splits = stratified_splits(labels, seed=7)
    combined = np.concatenate(list(splits.values()))
    assert len(combined) == len(labels)
    assert len(np.unique(combined)) == len(labels)
    assert set(combined) == set(range(len(labels)))


def test_uniform_quantize_step_bound():
    values = np.array([0.0, 0.2, 0.9, 1.0])
    quantized, step = uniform_quantize(values, 4)
    assert np.max(np.abs(values - quantized)) <= step / 2 + 1e-12


def test_per_channel_quantize_shape_and_finite():
    values = np.array([[0.0, -2.0], [1.0, 2.0], [2.0, 4.0]])
    quantized, steps = per_channel_quantize(values, 4)
    assert quantized.shape == values.shape
    assert steps.shape == (2,)
    assert np.isfinite(quantized).all()


def test_low_rank_and_random_projection_are_finite():
    rng = np.random.default_rng(2)
    matrix = rng.normal(size=(20, 8))
    svd = low_rank_svd(matrix, 3)
    random = random_projection(matrix, 3, seed=2)
    assert 0 <= svd["relative_error"] < 1
    assert np.isfinite(random["relative_error"]) and random["relative_error"] >= 0


def test_top2_readout_preserves_argmax():
    logits = np.array([[1.0, 3.0, 2.0], [4.0, 0.0, 1.0]])
    result = top2_readout(logits)
    assert result["predictions"].tolist() == [1, 0]
    assert result["indices"].shape == (2, 2)


def test_rotation_matrix_is_orthogonal():
    matrix = rotation_matrix("z", 0.7)
    assert np.allclose(matrix @ matrix.T, np.eye(3))


def test_classification_metrics_handles_perfect_prediction():
    metrics = classification_metrics([0, 1, 2], [0, 1, 2])
    assert metrics["accuracy"] == 1.0
    assert metrics["balanced_accuracy"] == 1.0


def test_invalid_quantization_level_rejected():
    with pytest.raises(ValueError):
        uniform_quantize(np.ones(3), 1)


def test_torch_linear_probe_fits_separable_data_on_available_device():
    features = np.array([[-2.0], [-1.5], [1.5], [2.0]], dtype=np.float32)
    labels = np.array([0, 0, 1, 1])
    probe = TorchLinearProbe(seed=3, epochs=80, device="cpu")
    fit = probe.fit(features, labels, (features, labels))
    assert fit["device"] == "cpu"
    assert probe.predict(features).tolist() == labels.tolist()


def test_initial_plus_residual_reconstructs_frames():
    frames = np.arange(24, dtype=float).reshape(2, 3, 4)
    encoded = initial_plus_residual(frames)
    assert encoded.shape == frames.reshape(2, -1).shape
    initial = encoded[:, :4].reshape(2, 1, 4)
    residual = encoded[:, 4:].reshape(2, 2, 4)
    reconstructed = np.concatenate([initial, initial + np.cumsum(residual, axis=1)], axis=1)
    assert np.allclose(reconstructed, frames)


def test_per_channel_quantile_quantize_has_channel_representatives():
    values = np.array([[0.0, -2.0], [0.1, 0.0], [0.2, 2.0], [1.0, 4.0]])
    quantized, representatives = per_channel_quantile_quantize(values, 4)
    assert quantized.shape == values.shape
    assert representatives.shape == (4, 2)
    assert np.isfinite(quantized).all()


def test_per_channel_lloyd_quantize_beats_uniform_on_nonuniform_channel():
    rng = np.random.default_rng(12)
    values = np.concatenate([rng.normal(0, 0.05, 500), rng.normal(5, 0.2, 20), rng.normal(-3, 0.1, 20)])[:, None]
    uniform, _ = per_channel_quantize(values, 8)
    lloyd, representatives = per_channel_lloyd_quantize(values, 8)
    assert representatives.shape == (8, 1)
    assert np.linalg.norm(values - lloyd) < np.linalg.norm(values - uniform)


def test_hybrid_lloyd_escape_reduces_error_with_bounded_bits():
    rng = np.random.default_rng(18)
    values = np.concatenate([rng.normal(size=(500, 2)), rng.normal(0, 8, size=(10, 2))])
    lloyd, _ = per_channel_lloyd_quantize(values, 8)
    hybrid, mask, bits = hybrid_lloyd_escape_quantize(values, 8, escape_fraction=0.02)
    assert np.linalg.norm(values - hybrid) < np.linalg.norm(values - lloyd)
    assert 3.0 <= bits < 8.0
    assert np.array_equal(hybrid[mask], values[mask])
