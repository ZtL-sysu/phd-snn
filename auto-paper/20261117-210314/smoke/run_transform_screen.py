"""TRANS-C15-v1 real-coordinate smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from smoke.mechanism_prototypes import centroid_event_encode


WORKSPACE = Path(__file__).resolve().parents[3]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    frame = pd.read_feather(WORKSPACE / "fly-connectome-cvpr2027/data/malecns_annotations.feather")
    points = np.asarray([value for value in frame["somaLocation"].head(4096) if isinstance(value, (list, tuple, np.ndarray)) and len(value) == 3], dtype=np.float64)
    shift = np.array([1200.0, -700.0, 350.0])
    direct = centroid_event_encode(points, levels=8)
    translated = centroid_event_encode(points + shift, levels=8)
    translation_error = float(np.max(np.abs(translated["reconstructed"] - direct["reconstructed"])))
    relative_error = float(np.linalg.norm(direct["centered"] - direct["reconstructed"]) / max(np.linalg.norm(direct["centered"]), 1.0))
    result = {
        "coordinates": int(points.shape[0]),
        "translation": shift.tolist(),
        "translation_error": translation_error,
        "relative_quantization_error": relative_error,
        "gate_pass": translation_error <= 1e-10 and relative_error <= 0.10,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
