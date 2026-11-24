"""I6 smoke: cost extrapolation from REAL measured I1 timings.

No new training. Uses smoke_i1.json (real 87k-node FlyWire subgraph, 40 steps,
single seed) to extrapolate whether the full benchmark grid fits the 11-day /
12 GB budget. All scaling factors are explicit and conservative.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
src = json.loads((OUT / "smoke_i1.json").read_text(encoding="utf-8"))

# measured
cell_seconds = max(c["seconds"] for c in src["conditions"])
cell_peak_mb = max(c["peak_gpu_MB"] for c in src["conditions"])
measured_steps = src["steps"]
measured_nnz = max(g["nnz"] for g in src["graph_info"].values())

# explicit scaling assumptions
FULL_GRAPH_NNZ = 2_700_000      # conservative: aggregated FlyWire v783 neuron-pair edges
FULL_TRAIN_STEPS = 5_000        # official paper-scale training
SEEDS = 5
GRID_FULL = 5 * 3 * 2 * 2      # 5 graphs x 3 dynamics x 2 task families x 2 budget axes
GRID_MINI = 2 * 2 * 1 * 1      # 2 graphs x 2 dynamics x 1 task x 1 budget
MINI_SEEDS = 3

nnz_scale = FULL_GRAPH_NNZ / measured_nnz
step_scale = FULL_TRAIN_STEPS / measured_steps
full_cell_seconds = cell_seconds * nnz_scale * step_scale
full_peak_mb = cell_peak_mb * (1 + 0.6 * (nnz_scale - 1))  # sparse A dominates, not dense x

full_runs = GRID_FULL * SEEDS
mini_runs = GRID_MINI * MINI_SEEDS
full_gpu_hours = full_runs * full_cell_seconds / 3600
mini_gpu_hours = mini_runs * full_cell_seconds / 3600

# wall-clock budget: 11 days, but writing / baseline reruns / debugging consume most of it
WALL_DAYS = 11
GPU_SHARE = 0.40
gpu_budget_hours = WALL_DAYS * 24 * GPU_SHARE
VRAM_BUDGET_MB = 10_000

result = {
    "source": "smoke_i1.json (real measured, not simulated)",
    "measured": {
        "per_cell_seconds": cell_seconds,
        "per_cell_peak_gpu_MB": cell_peak_mb,
        "steps": measured_steps,
        "nnz": measured_nnz,
        "nodes": src["graph_info"]["biological"]["nodes"],
    },
    "scaling": {
        "full_graph_nnz_assumed": FULL_GRAPH_NNZ,
        "nnz_scale": round(nnz_scale, 2),
        "steps_scale": step_scale,
        "full_cell_seconds_est": round(full_cell_seconds, 1),
        "full_cell_peak_gpu_MB_est": round(full_peak_mb, 1),
    },
    "grids": {
        "full": {"cells": GRID_FULL, "seeds": SEEDS, "runs": full_runs,
                 "gpu_hours": round(full_gpu_hours, 1)},
        "mini": {"cells": GRID_MINI, "seeds": MINI_SEEDS, "runs": mini_runs,
                 "gpu_hours": round(mini_gpu_hours, 1)},
    },
    "budget": {"wall_days": WALL_DAYS, "gpu_share": GPU_SHARE,
               "gpu_hours_available": round(gpu_budget_hours, 1),
               "vram_budget_MB": VRAM_BUDGET_MB},
    "checks": {
        "vram_ok": full_peak_mb < VRAM_BUDGET_MB,
        "full_grid_fits": full_gpu_hours <= gpu_budget_hours,
        "mini_grid_fits": mini_gpu_hours <= gpu_budget_hours,
    },
}
result["verdict"] = (
    "MINI_BENCHMARK_FEASIBLE" if result["checks"]["vram_ok"] and result["checks"]["mini_grid_fits"]
    else "INFEASIBLE"
)
result["note"] = (
    "GPU hours exclude baseline reruns, hyperparameter search, failed runs and writing. "
    "Full-grid point estimate alone does not make a CVPR主会 submission feasible in 11 days."
)
(OUT / "smoke_i6.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False), flush=True)
