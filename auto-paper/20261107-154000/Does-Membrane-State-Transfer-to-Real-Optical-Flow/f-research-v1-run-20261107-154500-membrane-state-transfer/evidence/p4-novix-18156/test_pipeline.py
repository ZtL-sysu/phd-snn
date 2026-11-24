#!/usr/bin/env python3
"""Fast invariant tests for persisted P4 artifacts (no experiment rerun)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT = Path("/home/novix/workspace/project")
sys.path.insert(0, str(PROJECT / "src"))

from p4_pipeline.graph import GRAPH_ARRAYS, GRAPH_META, load_graph_arrays  # noqa: E402
from p4_pipeline.stimuli import build_voronoi_mapper  # noqa: E402


class GraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.arrays = load_graph_arrays(GRAPH_ARRAYS)
        cls.meta = json.loads(GRAPH_META.read_text())

    def test_orientation_and_spectral_normalization(self) -> None:
        self.assertEqual(self.meta["schema"]["orientation"], "A[post,pre]")
        self.assertFalse(self.meta["row_normalized"])
        self.assertAlmostEqual(self.meta["normalized_spectral_radius_40_iter"], 0.95, places=5)

    def test_graph_arrays_consistent(self) -> None:
        edge_count = len(self.arrays["src"])
        self.assertEqual(edge_count, self.meta["nnz"])
        self.assertEqual(edge_count, len(self.arrays["dst"]))
        self.assertEqual(edge_count, len(self.arrays["weight"]))
        self.assertTrue(np.all(self.arrays["weight"] > 0))
        self.assertEqual(len(np.unique(self.arrays["node_ids"])), len(self.arrays["node_ids"]))

    def test_kc_and_eye_indices_valid(self) -> None:
        n = len(self.arrays["node_ids"])
        self.assertTrue(np.all((self.arrays["input_indices"] >= 0) & (self.arrays["input_indices"] < n)))
        self.assertTrue(np.all((self.arrays["output_indices"] >= 0) & (self.arrays["output_indices"] < n)))
        self.assertEqual(len(self.arrays["output_indices"]), 2559)


class StimulusTests(unittest.TestCase):
    def test_voronoi_mapping_and_contrast(self) -> None:
        mapper, meta = build_voronoi_mapper()
        self.assertEqual(len(mapper.pixel_to_eye_position), 1024)
        self.assertEqual(meta["coordinate_columns"], ["x_axis", "y_axis"])
        frames = np.zeros((2, 8, 32, 32), dtype=np.float32)
        frames[0, :, 10:15, 10:15] = 0.5
        drive = mapper.transform(frames)
        self.assertEqual(drive.shape[:2], (2, 8))
        self.assertAlmostEqual(float(drive[0].max()), 1.0)
        self.assertEqual(float(drive[1].max()), 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
