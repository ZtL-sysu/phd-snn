import numpy as np
import pytest

from smoke.adaptive_prefix import (
    choose_thresholds,
    make_internal_partitions,
    selective_prefix,
    uncertainty_scores,
)


def test_internal_partitions_are_disjoint_deterministic_and_saved():
    first = make_internal_partitions(np.arange(20), seed=7, dev=4, tune=5, validation=6)
    second = make_internal_partitions(np.arange(20), seed=7, dev=4, tune=5, validation=6)
    assert all(np.array_equal(first[key], second[key]) for key in first)
    all_ids = np.concatenate([first["dev"], first["tune"], first["validation"]])
    assert len(all_ids) == 15
    assert len(np.unique(all_ids)) == 15
    assert set(all_ids.tolist()).issubset(set(range(20)))


def test_uncertainty_scores_reflect_margin_and_prefix_disagreement():
    t1 = np.array([[4.0, 0.0], [1.0, 0.0], [2.0, 1.9]])
    t2 = np.array([[4.0, 0.0], [0.0, 1.0], [2.0, 1.9]])
    scores = uncertainty_scores(t1, t2)
    assert scores[1] > scores[0]
    assert scores[2] > scores[0]
    assert np.isfinite(scores).all()


def test_selective_prefix_uses_only_declared_risky_threshold():
    t2 = np.array([[4.0, 0.0], [1.0, 0.0], [2.0, 1.9]])
    t4 = np.array([[4.0, 0.0], [2.0, 1.0], [1.8, 2.0]])
    scores = np.array([0.1, 0.9, 0.2])
    logits, used = selective_prefix(t2, t4, scores, uncertainty_threshold=0.5)
    assert used.tolist() == [False, True, False]
    assert np.array_equal(logits[0], t2[0])
    assert np.array_equal(logits[1], t4[1])
    assert np.array_equal(logits[2], t2[2])


def test_threshold_selection_maximizes_saved_teacher_agreement_on_tune():
    t2 = np.array([[3.0, 0.0], [2.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.0, 2.0], [0.0, 3.0]])
    t1 = t2.copy()
    t4 = np.array([[3.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 2.0], [0.0, 3.0]])
    teacher = np.array([[3.0, 0.0], [2.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 2.0], [0.0, 3.0]])
    selected = choose_thresholds(t1, t2, t4, teacher, fractions=(0.0, 1 / 3, 1.0))
    assert 0.0 < selected["fraction"] < 1.0
    assert selected["validation_note"] == "thresholds are fit on tune only"


def test_selective_prefix_rejects_shape_mismatch():
    with pytest.raises(ValueError, match="shape"):
        selective_prefix(
            np.zeros((2, 3)), np.zeros((3, 3)), np.zeros(2), uncertainty_threshold=0.5
        )
