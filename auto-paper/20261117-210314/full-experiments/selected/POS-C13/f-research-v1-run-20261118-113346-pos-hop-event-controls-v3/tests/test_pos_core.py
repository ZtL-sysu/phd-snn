import sys
import unittest
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))


class PosCoreTests(unittest.TestCase):
    def test_hop_features_are_node_permutation_equivariant(self):
        from pos_core import hop_features

        adjacency = np.array([[0.5, 0.5], [0.25, 0.75]], dtype=np.float64)
        features = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
        permutation = np.array([1, 0])
        original = hop_features(adjacency, features, hops=3)
        permuted = hop_features(adjacency[np.ix_(permutation, permutation)], features[permutation], hops=3)
        np.testing.assert_allclose(permuted, original[permutation], rtol=0, atol=1e-12)

    def test_shuffle_hop_blocks_preserves_values_but_changes_order(self):
        from pos_core import shuffle_hop_blocks

        values = np.arange(24, dtype=np.float64).reshape(2, 12)
        shuffled, permutation = shuffle_hop_blocks(values, feature_dim=3, seed=7)
        self.assertEqual(sorted(permutation.tolist()), [0, 1, 2, 3])
        self.assertFalse(np.array_equal(shuffled, values))
        self.assertEqual(sorted(shuffled.ravel().tolist()), sorted(values.ravel().tolist()))

    def test_serialized_bits_include_symbol_payload_and_codebook(self):
        from pos_core import serialized_bit_ledger

        ledger = serialized_bit_ledger(nodes=1000, channels=10, escape_fraction=0.005)
        self.assertAlmostEqual(ledger["average_bits_per_value"], 4.0 + 0.005 * 32 + 256 / 1000)
        self.assertAlmostEqual(ledger["storage_reduction"], 32 / ledger["average_bits_per_value"])

    def test_hybrid_encoder_marks_exact_escapes(self):
        from pos_core import hybrid_lloyd_escape_encode

        rng = np.random.default_rng(4)
        values = rng.normal(size=(100, 4))
        encoded = hybrid_lloyd_escape_encode(values, levels=8, escape_fraction=0.05)
        self.assertGreaterEqual(int(encoded.escape_mask.sum()), 5 * 4)
        np.testing.assert_array_equal(encoded.reconstructed[encoded.escape_mask], values[encoded.escape_mask])
        self.assertEqual(encoded.alphabet_size, 9)

    def test_ordered_codebook_mismatch_control_increases_error(self):
        from pos_core import hybrid_lloyd_escape_encode, ordered_codebook_shuffle_error

        rng = np.random.default_rng(9)
        values = rng.normal(size=(200, 8)) * np.linspace(1.0, 8.0, 8) + np.linspace(-5.0, 5.0, 8)
        encoded = hybrid_lloyd_escape_encode(values, levels=8, escape_fraction=0.0)
        result = ordered_codebook_shuffle_error(values, encoded, feature_dim=2, seed=2)
        self.assertGreater(result["shuffled_error"], result["ordered_error"])

    def test_escape_selection_is_row_permutation_invariant_with_ties(self):
        from pos_core import hybrid_lloyd_escape_encode

        values = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]] * 5, dtype=np.float64)
        permutation = np.random.default_rng(11).permutation(values.shape[0])
        original = hybrid_lloyd_escape_encode(values, levels=3, escape_fraction=0.1)
        permuted = hybrid_lloyd_escape_encode(values[permutation], levels=3, escape_fraction=0.1)
        restored = np.empty_like(permuted.reconstructed)
        restored[permutation] = permuted.reconstructed
        np.testing.assert_allclose(restored, original.reconstructed, rtol=0, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
