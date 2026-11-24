import numpy as np
import pytest

from smoke.readout_pair import top2_pair_readout


def test_top2_pair_preserves_argmax_and_orders_pair():
    logits = np.array([[1.0, 3.0, 2.0], [4.0, 0.0, 1.0]])
    result = top2_pair_readout(logits)
    assert result["predictions"].tolist() == [1, 0]
    assert result["class_indices"].tolist() == [[1, 2], [0, 2]]
    assert np.allclose(result["margin"], [1.0, 3.0])


def test_top2_pair_reduces_output_slots():
    result = top2_pair_readout(np.zeros((4, 10)))
    assert result["output_slots_per_graph"] == 2
    assert result["full_slots_per_graph"] == 10


def test_top2_pair_rejects_invalid_logits():
    with pytest.raises(ValueError, match="finite"):
        top2_pair_readout(np.array([[np.nan, 1.0]]))
