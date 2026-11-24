#!/usr/bin/env python3
"""Fast unit/integration tests for protocol-critical experiment components."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from scipy import sparse

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from fresearch.data import make_flash_control, make_synthetic_direction  # noqa: E402
from fresearch.encoders import (  # noqa: E402
    LIFSpec,
    encode_a0,
    encode_lif,
    encode_stateless,
    feature_diagnostics,
)
from fresearch.evaluation import (  # noqa: E402
    benjamini_hochberg,
    exact_paired_sign_flip_p,
    paired_bootstrap_ci,
    split_indices,
)
from fresearch.graph import choose_depth_and_readout, reachability_layers  # noqa: E402


class StimulusTests(unittest.TestCase):
    def test_synthetic_direction_protocol(self) -> None:
        frames, labels, meta = make_synthetic_direction(n=20, seed=123)
        self.assertEqual(frames.shape, (20, 8, 32, 32))
        self.assertEqual(frames.dtype, np.uint8)
        np.testing.assert_array_equal(np.bincount(labels), [10, 10])
        self.assertEqual(meta["speed_pixels_per_frame"], 2)
        # Every sample contains ink and is temporally nonconstant.
        self.assertTrue(np.all((frames == 0).reshape(20, -1).any(axis=1)))
        self.assertTrue(np.all(np.any(frames[:, 1:] != frames[:, :-1], axis=(1, 2, 3))))

    def test_flash_is_balanced_negative_control(self) -> None:
        frames, labels, meta = make_flash_control(n=20, seed=321)
        np.testing.assert_array_equal(np.bincount(labels), [10, 10])
        self.assertTrue(np.all(frames[labels == 0] == 255))
        positive_dark_frames = (frames[labels == 1] < 255).any(axis=(2, 3)).sum(axis=1)
        np.testing.assert_array_equal(positive_dark_frames, np.ones(10, dtype=int))
        self.assertIn("negative_control", meta["task"])


class GraphProtocolTests(unittest.TestCase):
    def test_a_post_pre_and_exact_length_reachability(self) -> None:
        # 0 -> 1 -> 2(KC), 2 -> 1 creates exact paths to KC at even hops.
        pre = np.array([0, 1, 2])
        post = np.array([1, 2, 1])
        a = sparse.coo_matrix((np.ones(3, dtype=np.float32), (post, pre)), shape=(4, 4)).tocsr()
        metrics, layers = reachability_layers(a, np.array([0]), np.array([2]), max_hop=5)
        self.assertEqual(metrics["exact_length_kc_counts"], {"1": 0, "2": 1, "3": 0, "4": 1, "5": 0})
        self.assertEqual(metrics["shortest_path_kc_counts"]["2"], 1)
        np.testing.assert_array_equal(layers[2], np.array([2]))

    def test_depth_correction_selects_first_k_at_or_above_five(self) -> None:
        layers = {
            1: np.array([1]), 2: np.array([2]), 3: np.array([3]),
            4: np.array([4]), 5: np.array([10, 11]), 6: np.array([10]),
            7: np.array([10]), 8: np.array([10]),
        }
        k, readout, definition, decision = choose_depth_and_readout(
            layers, np.array([10]), initial_k=3, correction_min_k=5, max_k=8,
        )
        self.assertEqual(k, 5)
        np.testing.assert_array_equal(readout, [10])
        self.assertFalse(decision["readout_fallback"])
        self.assertIn("K=5", definition)


class EncoderTests(unittest.TestCase):
    @staticmethod
    def tiny_graph() -> sparse.csr_matrix:
        # Feedforward chain 0->1->2 plus a weak self loop at node 2.
        pre = np.array([0, 1, 2])
        post = np.array([1, 2, 2])
        weights = np.array([0.5, 0.5, 0.05], dtype=np.float32)
        return sparse.coo_matrix((weights, (post, pre)), shape=(4, 4)).tocsr()

    @staticmethod
    def tiny_frames() -> np.ndarray:
        frames = np.full((4, 8, 32, 32), 255, dtype=np.uint8)
        frames[0:2, :, 0:4, 0:4] = 0
        frames[2:4, :, 16:20, 16:20] = 0
        return frames

    @staticmethod
    def mapping() -> np.ndarray:
        mapping = np.full(1024, -1, dtype=np.int64)
        mapping[:512] = 0
        mapping[512:] = 3
        return mapping

    def test_a0_and_stateless_shapes(self) -> None:
        frames = self.tiny_frames()
        a0, a0_diag = encode_a0(
            frames, self.mapping(), np.array([0, 3]), 4,
            device="cpu", batch_size=2,
        )
        self.assertEqual(a0.shape, (4, 2))
        self.assertTrue(np.isfinite(a0).all())
        stateless, diag = encode_stateless(
            frames, self.tiny_graph(), self.mapping(), np.array([2]),
            k_steps=2, device="cpu", batch_size=2,
        )
        self.assertEqual(stateless.shape, (4, 1))
        self.assertTrue(np.isfinite(stateless).all())
        self.assertEqual(diag["k_steps"], 2)

    def test_event_lif_index_add_path(self) -> None:
        features, diag = encode_lif(
            self.tiny_frames(), self.tiny_graph(), self.mapping(), np.array([2]),
            np.ones(4, dtype=np.float32),
            LIFSpec("test_lif", adaptive_threshold=False, refractory=False, signed_ei=False),
            k_steps=2, device="cpu", batch_size=2,
            max_events_per_chunk=64,
        )
        self.assertEqual(features.shape, (4, 1))
        self.assertTrue(np.isfinite(features).all())
        self.assertIn("torch.index_add_", diag["edge_accumulation"])
        self.assertGreaterEqual(diag["total_transmitted_edge_events"], 0)
        self.assertGreaterEqual(diag["spike_rate"], 0.0)
        self.assertLessEqual(diag["spike_rate"], 1.0)

    def test_feature_invariant_uses_across_sample_variation(self) -> None:
        constant = np.ones((5, 3), dtype=np.float32)
        diag = feature_diagnostics(constant)
        self.assertEqual(diag["feature_std"], 0.0)
        variable = constant.copy()
        variable[0, 0] = 2
        self.assertGreater(feature_diagnostics(variable)["feature_std"], 0.0)


class StatisticsTests(unittest.TestCase):
    def test_stratified_split_is_70_30_and_reproducible(self) -> None:
        y = np.repeat([0, 1], 200)
        train1, test1 = split_indices(y, 1)
        train2, test2 = split_indices(y, 1)
        np.testing.assert_array_equal(train1, train2)
        np.testing.assert_array_equal(test1, test2)
        self.assertEqual(len(train1), 280)
        self.assertEqual(len(test1), 120)
        np.testing.assert_array_equal(np.bincount(y[train1]), [140, 140])

    def test_exact_sign_flip_five_seed_minimum(self) -> None:
        result = exact_paired_sign_flip_p(np.ones(5))
        self.assertEqual(result["enumerated_sign_patterns"], 32)
        self.assertAlmostEqual(result["p_value_two_sided"], 0.0625)
        self.assertAlmostEqual(result["theoretical_min_two_sided_p_nonzero_no_ties"], 0.0625)

    def test_bootstrap_reproducible_and_bh_monotone(self) -> None:
        a = paired_bootstrap_ci(np.array([0.1, 0.2, 0.3, 0.4, 0.5]), n_resamples=2000, seed=7)
        b = paired_bootstrap_ci(np.array([0.1, 0.2, 0.3, 0.4, 0.5]), n_resamples=2000, seed=7)
        self.assertEqual(a[:2], b[:2])
        np.testing.assert_array_equal(a[2], b[2])
        q = benjamini_hochberg([0.01, 0.04, 0.03])
        self.assertTrue(all(0 <= x <= 1 for x in q))
        self.assertLessEqual(q[0], q[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
