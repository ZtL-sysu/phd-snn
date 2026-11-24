import sys
import unittest
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))


class CertCoreTests(unittest.TestCase):
    def test_constant_channel_is_identity_with_zero_radius(self):
        from cert_core import uniform_quantize

        values = np.full((4, 3), 2.5, dtype=np.float64)
        values[:, 1] = [-1.0, 0.0, 1.0, 2.0]
        quantized, step, radius, clipping_count = uniform_quantize(values, levels=4, per_channel=True)

        np.testing.assert_array_equal(quantized[:, 0], values[:, 0])
        self.assertEqual(step[0], 0.0)
        self.assertEqual(radius[0], 0.0)
        self.assertEqual(clipping_count, 0)

    def test_rounding_ties_break_upward_and_respect_half_step(self):
        from cert_core import uniform_quantize

        values = np.array([0.0, 0.25, 0.75, 1.0], dtype=np.float64)[:, None]
        quantized, step, radius, clipping_count = uniform_quantize(values, levels=3, per_channel=False)

        np.testing.assert_array_equal(quantized[:, 0], np.array([0.0, 0.5, 1.0, 1.0]))
        self.assertAlmostEqual(float(step), 0.5)
        self.assertAlmostEqual(float(np.max(radius)), 0.25)
        self.assertLessEqual(float(np.max(np.abs(values - quantized))), float(np.max(radius)) + 1e-12)
        self.assertEqual(clipping_count, 0)

    def test_bounds_match_hand_computed_reduced_formula(self):
        from cert_core import certificate_bounds

        adjacency = np.array([[0.5, 0.5], [0.25, 0.75]], dtype=np.float64)
        weight = np.array([[1.0, -2.0], [-3.0, 4.0]], dtype=np.float64)
        radius = np.array([0.1, 0.2], dtype=np.float64)
        proposed, minkowski, global_column, scalar = certificate_bounds(adjacency, weight, radius)

        coeff = np.abs(adjacency) @ np.abs(adjacency) @ np.ones(2)
        expected = coeff[:, None] * (np.abs(weight) * radius[:, None]).sum(axis=0)[None, :]
        np.testing.assert_allclose(proposed, expected, rtol=0, atol=1e-12)
        self.assertTrue(np.all(proposed <= minkowski + 1e-12))
        self.assertTrue(np.all(global_column <= scalar + 1e-12))

    def test_global_uniform_radius_makes_proposed_equal_global_column(self):
        from cert_core import certificate_bounds

        adjacency = np.array([[0.2, 0.8], [0.6, 0.4]], dtype=np.float64)
        weight = np.array([[1.0, -1.0], [2.0, 3.0]], dtype=np.float64)
        radius = np.full(2, 0.125, dtype=np.float64)
        proposed, _, global_column, _ = certificate_bounds(adjacency, weight, radius)

        np.testing.assert_allclose(proposed, global_column, rtol=0, atol=1e-12)

    def test_per_channel_radius_tightens_global_column(self):
        from cert_core import certificate_bounds

        adjacency = np.array([[0.2, 0.8], [0.6, 0.4]], dtype=np.float64)
        weight = np.array([[1.0, -1.0], [2.0, 3.0]], dtype=np.float64)
        radius = np.array([0.01, 0.2], dtype=np.float64)
        proposed, _, global_column, _ = certificate_bounds(adjacency, weight, radius)

        proposed_width = np.median(proposed)
        global_width = np.median(global_column)
        self.assertGreater(1.0 - proposed_width / global_width, 0.25)

    def test_float64_chain_contains_actual_error(self):
        from cert_core import evaluate_synthetic_chain

        result = evaluate_synthetic_chain()
        self.assertTrue(result["containment"])
        self.assertTrue(result["minkowski_valid"])
        self.assertTrue(np.isfinite(result["actual_rms"]))


if __name__ == "__main__":
    unittest.main()
