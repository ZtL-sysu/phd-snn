import numpy as np

from smoke.conformal_selective import fit_risk_threshold, selective_result, uncertainty_scores


def test_uncertainty_scores_are_finite_and_shape_checked():
    scores = uncertainty_scores(np.zeros((3, 2)), np.array([[2.0, 0.0], [1.0, 0.0], [0.0, 1.0]]))
    assert scores.shape == (3,)
    assert np.isfinite(scores).all()


def test_fit_risk_threshold_selects_largest_safe_coverage():
    scores = np.array([0.1, 0.2, 0.8, 0.9])
    correct = np.array([True, True, False, True])
    result = fit_risk_threshold(scores, correct, target_risk=0.1)
    assert result["status"] == "calibrated"
    assert result["threshold"] == 0.2
    assert result["coverage"] == 0.5
    assert result["risk"] == 0.0


def test_selective_result_reports_coverage_and_error():
    logits = np.array([[2.0, 0.0], [0.0, 2.0], [1.0, 0.0]])
    labels = np.array([0, 1, 1])
    result = selective_result(logits, labels, np.array([0.1, 0.2, 0.9]), 0.2)
    assert result["coverage"] == 2 / 3
    assert result["selective_error"] == 0.0
