"""Create a tiny SYNTHETIC graph for code-path dry-runs only. Never a scientific result."""
from pathlib import Path
import numpy as np
import pandas as pd

d = Path(__file__).resolve().parent / "fake_data"
d.mkdir(exist_ok=True)
rng = np.random.default_rng(0)
N = 500
pre = rng.integers(0, N, 3000)
post = rng.integers(0, N, 3000)
pd.DataFrame({
    "pre_root_id": [f"n{i}" for i in pre],
    "post_root_id": [f"n{i}" for i in post],
    "syn_count": rng.integers(1, 20, 3000),
}).to_csv(d / "connections.csv", index=False)
types = ["R1-6"] * 40 + ["R7"] * 40 + ["R8"] * 40 + ["KCapbp-m"] * 60 + ["other"] * (N - 180)
pd.DataFrame({
    "root_id": [f"n{i}" for i in range(N)],
    "cell_type": types[:N],
    "side": ["right"] * N,
}).to_csv(d / "classification.csv", index=False)
xy = rng.random((400, 2))
pd.DataFrame({
    "root_id": [f"p{i}" for i in range(400)],
    "cell_type": ["R7"] * 200 + ["R8"] * 200,
    "x_axis": xy[:, 0],
    "y_axis": xy[:, 1],
}).to_csv(d / "right_visual_positions_all_neurons.csv", index=False)
print("fake data written to", d)
