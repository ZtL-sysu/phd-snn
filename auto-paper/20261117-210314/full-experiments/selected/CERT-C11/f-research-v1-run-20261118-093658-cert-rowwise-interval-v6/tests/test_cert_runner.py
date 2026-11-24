import sys
import unittest
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))


class CertRunnerTests(unittest.TestCase):
    def test_evaluate_snapshot_returns_complete_row(self):
        from cert_runner import evaluate_snapshot

        row = evaluate_snapshot(
            adjacency=np.array([[0.5, 0.5], [0.25, 0.75]], dtype=np.float64),
            features=np.array([[0.1, 0.2], [-0.2, 0.4]], dtype=np.float64),
            weight0=np.array([[1.0, -0.5], [0.25, 0.75]], dtype=np.float64),
            bias0=np.array([0.1, -0.1], dtype=np.float64),
            weight1=np.array([[0.5, -0.2], [0.1, 0.3]], dtype=np.float64),
            bias1=np.array([0.0, 0.1], dtype=np.float64),
            levels=4,
            quantizer="per_channel",
            dataset="synthetic",
            seed=0,
        )
        required = {
            "dataset",
            "seed",
            "levels",
            "quantizer",
            "containment",
            "minkowski_valid",
            "global_equality",
            "actual_rms",
            "proposed_width_over_rms",
            "global_width_over_rms",
            "tightening",
            "clipping_count",
        }
        self.assertTrue(required.issubset(row))
        self.assertTrue(row["containment"])


if __name__ == "__main__":
    unittest.main()
