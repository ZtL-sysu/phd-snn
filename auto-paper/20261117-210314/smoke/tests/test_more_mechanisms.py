import numpy as np
import pytest

from smoke.more_mechanisms import (
    affine_error_envelope,
    delayed_residual_events,
    hop_position_messages,
    prune_lowest_edges,
    quantize_uniform,
)


def test_affine_error_envelope_contains_actual_error():
    adjacency = np.array([[0.5, 0.5], [0.0, 1.0]])
    weight = np.array([[1.0, -1.0], [2.0, 0.5], [-0.25, 0.75]])
    bound = affine_error_envelope(adjacency, weight, 0.1)
    error = np.abs(np.array([[0.13, -0.09], [0.19, 0.12]]))
    assert np.all(error <= bound)


def test_uniform_quantization_has_finite_step_and_shape():
    values = np.array([[0.0, -1.0], [1.0, 1.0], [0.5, 0.0]])
    quantized, step = quantize_uniform(values, levels=4)
    assert quantized.shape == values.shape
    assert step > 0
    assert np.max(np.abs(quantized - values)) <= step / 2 + 1e-12


def test_hop_position_messages_are_permutation_equivariant():
    adjacency = np.array([[0.5, 0.5], [0.25, 0.75]])
    features = np.array([[1.0], [2.0]])
    permutation = np.array([1, 0])
    direct = hop_position_messages(adjacency, features, hops=2)
    permuted = hop_position_messages(adjacency[np.ix_(permutation, permutation)], features[permutation], hops=2)
    assert np.allclose(permuted, direct[permutation])


def test_prune_lowest_edges_keeps_requested_fraction():
    adjacency = np.array([[0.0, 1.0, 4.0], [2.0, 0.0, 3.0], [0.5, 0.5, 0.0]])
    pruned, removed = prune_lowest_edges(adjacency, keep_fraction=0.5)
    assert removed == 3
    assert np.count_nonzero(pruned) == 3


def test_delayed_residual_events_reconstruct_and_are_causal():
    frames = np.array([0.0, 1.0, 1.0, 2.0])
    events = delayed_residual_events(frames, delay=1)
    assert np.allclose(np.cumsum(events) + frames[0], frames[1:])
    changed = frames.copy()
    changed[-1] += 10
    assert np.allclose(delayed_residual_events(changed)[:-1], events[:-1])


def test_invalid_parameters_raise():
    with pytest.raises(ValueError):
        affine_error_envelope(np.ones((2, 3)), np.ones((3, 2)), 0.1)
    with pytest.raises(ValueError):
        prune_lowest_edges(np.ones((2, 2)), keep_fraction=0)
