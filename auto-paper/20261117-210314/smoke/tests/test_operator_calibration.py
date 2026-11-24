import numpy as np
import pytest

from smoke.operator_calibration import evaluate_factor, fit_operator_factor, teacher_logits


def tiny_setup():
    data = {
        "adj": np.eye(3, dtype=np.float32),
        "y": np.array([0, 1, 2]),
        "train_mask": np.array([True, True, False]),
        "val_mask": np.array([False, False, True]),
    }
    model = {
        "Ms": [np.eye(3, dtype=np.float32), np.eye(3, dtype=np.float32)],
        "bs_layers": [np.zeros(3, dtype=np.float32)],
        "b_out": np.zeros(3, dtype=np.float32),
        "Hs": [np.eye(3, dtype=np.float32)],
        "n_layers": 2,
    }
    return data, model


def fake_convert(data, model, *, T, thetas, return_logits):
    factor = thetas[0]
    logits = np.eye(3, dtype=np.float32) * (2.0 if factor >= 2.0 else 1.0)
    return {"logits": logits, "spikes_per_node": factor}


def test_teacher_logits_uses_frozen_graph_readout():
    data, model = tiny_setup()
    got = teacher_logits(data, model)
    assert got.shape == (3, 3)
    assert np.allclose(got, np.eye(3))


def test_fit_selects_factor_with_highest_training_agreement():
    data, model = tiny_setup()
    target = np.array([[2.0, 0.0], [0.0, 2.0], [1.0, 0.0]], dtype=np.float32)
    selected = fit_operator_factor(
        data=data, model=model, target_logits=target, train_mask=data["train_mask"],
        factors=(0.5, 1.0, 2.0), t_steps=2, convert=fake_convert,
    )
    assert selected["factor"] == 2.0
    assert selected["train_agreement"] == 1.0
    assert len(selected["candidates"]) == 3


def test_evaluate_reports_accuracy_agreement_mse_and_work():
    data, model = tiny_setup()
    target = np.eye(3, dtype=np.float32)
    got = evaluate_factor(data=data, model=model, target_logits=target,
                          mask=np.array([False, False, True]), factor=1.0,
                          t_steps=2, convert=fake_convert)
    assert got["accuracy"] == 1.0
    assert got["teacher_agreement"] == 1.0
    assert got["logit_mse"] == 0.0
    assert got["spikes_per_node"] == 1.0


def test_fit_rejects_invalid_factor():
    data, model = tiny_setup()
    with pytest.raises(ValueError, match="positive"):
        fit_operator_factor(data=data, model=model, target_logits=np.eye(3),
                            train_mask=data["train_mask"], factors=(0.0,),
                            t_steps=2, convert=fake_convert)
