import numpy as np
import pytest

from smoke.zero_message_prune import prune_zero_rows, zero_message_mask


def test_zero_message_mask_identifies_all_zero_rows():
    counts = np.array([[0, 0], [1, 0], [0, 0], [2, 3]])
    assert zero_message_mask(counts).tolist() == [True, False, True, False]


def test_pruning_zero_rows_preserves_nonzero_rows_and_zeros_messages():
    values = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    pruned = prune_zero_rows(values, np.array([True, False, True]))
    assert np.array_equal(pruned, np.array([[0.0, 0.0], [3.0, 4.0], [0.0, 0.0]]))


def test_prune_rejects_bad_shape():
    with pytest.raises(ValueError, match="shape"):
        prune_zero_rows(np.ones((2, 2)), np.ones(3, dtype=bool))
