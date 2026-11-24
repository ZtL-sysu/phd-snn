import sys
import unittest
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))


class RowwiseBoundTests(unittest.TestCase):
    def test_rowwise_quantizer_has_node_specific_radius(self):
        from cert_core import rowwise_quantize

        values = np.array([[0.0, 1.0], [10.0, 12.0], [-2.0, -2.0]], dtype=np.float64)
        quantized, steps, radius, clipping_count = rowwise_quantize(values, levels=3)

        self.assertEqual(radius.shape, values.shape)
        np.testing.assert_allclose(radius[0], np.array([0.25, 0.25]))
        np.testing.assert_allclose(radius[1], np.array([0.5, 0.5]))
        np.testing.assert_array_equal(quantized[2], values[2])
        self.assertEqual(clipping_count, 0)

    def test_matrix_bound_contains_synthetic_chain_and_tightens(self):
        from cert_core import certificate_bounds_matrix, rowwise_quantize

        adjacency = np.array([[0.5, 0.5], [0.25, 0.75]], dtype=np.float64)
        features = np.array([[0.1, 0.2], [-0.2, 0.4]], dtype=np.float64)
        weight0 = np.array([[1.0, -0.5], [0.25, 0.75]], dtype=np.float64)
        bias0 = np.array([0.1, -0.1], dtype=np.float64)
        weight1 = np.array([[0.5, -0.2], [0.1, 0.3]], dtype=np.float64)
        bias1 = np.array([0.0, 0.1], dtype=np.float64)
        message = features @ weight0
        quantized, _, radius, _ = rowwise_quantize(message, levels=3)
        hidden = np.maximum(adjacency @ message + bias0, 0.0)
        hidden_quantized = np.maximum(adjacency @ quantized + bias0, 0.0)
        logits = adjacency @ hidden @ weight1 + bias1
        logits_quantized = adjacency @ hidden_quantized @ weight1 + bias1
        proposed, minkowski, global_column, _ = certificate_bounds_matrix(adjacency, weight1, radius)
        actual = np.abs(logits - logits_quantized)

        self.assertTrue(np.all(actual <= proposed + 1e-10 + 1e-12 * np.abs(proposed)))
        self.assertTrue(np.all(proposed <= minkowski + 1e-10 + 1e-12 * np.abs(minkowski)))
        self.assertLess(np.median(proposed), np.median(global_column))


if __name__ == "__main__":
    unittest.main()
