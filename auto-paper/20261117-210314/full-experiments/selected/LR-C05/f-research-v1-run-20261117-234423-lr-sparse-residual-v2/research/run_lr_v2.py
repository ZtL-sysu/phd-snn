"""Guidance-v2 exact-cost LR experiments."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

from research.lr_v2_core import (
    basis_random,
    basis_svd,
    dense_uniform_at_budget,
    one_spike_at_budget,
    rate_convert_hidden,
    select_residual_indices,
    sparse_cost_bits,
    sparse_reconstruct,
)


RUN_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = next(parent for parent in Path(__file__).resolve().parents if parent.name == "phd-snn")
CORE_ROOT = WORKSPACE / "auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv"
MODEL_ROOT = WORKSPACE / "auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/f-research-v1-run-20261105-111502-gnn2snn/results/models"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


DATASETS = ("cora", "chameleon", "squirrel")
SEEDS = (0, 1, 2)
RANKS = (16, 32, 64, 128)
BUDGETS = (0.005, 0.01, 0.02)


def load_case(dataset: str, seed: int) -> dict:
    data = core.load(dataset, str(CORE_ROOT / "results/.data"))
    with np.load(MODEL_ROOT / f"{dataset}__H1_mean__s{seed}.npz", allow_pickle=False) as archive:
        model = {
            "Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()],
            "bs_layers": [archive["bs0"].copy()],
            "b_out": archive["b_out"].copy(),
        }
    messages = np.asarray(data["adj"] @ data["X"], dtype=np.float32)
    hidden = np.maximum(messages @ model["Ms"][0] + model["bs_layers"][0], 0.0)
    logits = np.asarray(data["adj"] @ hidden @ model["Ms"][1] + model["b_out"], dtype=np.float32)
    return {"data": data, "model": model, "messages": messages, "hidden": hidden, "logits": logits}


def mse(reference: np.ndarray, estimate: np.ndarray) -> float:
    return float(np.mean((np.asarray(reference) - np.asarray(estimate)) ** 2))


def evaluate_reconstruction(case: dict, reconstructed: np.ndarray, cost: dict) -> dict:
    data, model = case["data"], case["model"]
    hidden_hat = np.maximum(reconstructed @ model["Ms"][0] + model["bs_layers"][0], 0.0)
    logits_hat = np.asarray(data["adj"] @ hidden_hat @ model["Ms"][1] + model["b_out"], dtype=np.float32)
    mask = data["val"]
    labels = data["y"][mask]
    teacher_pred = np.argmax(case["logits"][mask], axis=1)
    output = {
        "message_mse": mse(case["messages"], reconstructed),
        "hidden_mse": mse(case["hidden"], hidden_hat),
        "logit_mse": mse(case["logits"], logits_hat),
        **cost,
    }
    for steps in (2, 4):
        decoded = rate_convert_hidden(hidden_hat, t_steps=steps)
        converted = np.asarray(data["adj"] @ decoded @ model["Ms"][1] + model["b_out"], dtype=np.float32)
        pred = np.argmax(converted[mask], axis=1)
        output[f"T{steps}"] = {
            "accuracy": float(np.mean(pred == labels)),
            "teacher_agreement": float(np.mean(pred == teacher_pred)),
            "logit_mse": mse(case["logits"][mask], converted[mask]),
        }
    return output


def make_variant(
    case: dict,
    basis_name: str,
    residual_mode: str,
    rank: int,
    budget: float,
    *,
    basis: dict | None = None,
    jacobian_norm: np.ndarray | None = None,
) -> dict:
    messages = case["messages"]
    data, model = case["data"], case["model"]
    if basis is None:
        basis = basis_svd(messages, rank) if basis_name == "svd" else basis_random(messages, rank, seed=7000 + rank)
    residual = messages - basis["reconstructed"]
    if jacobian_norm is None:
        hidden_mask = case["hidden"] > 0
        adjacency_column_norm = np.sqrt(np.asarray(data["adj"].power(2).sum(axis=0), dtype=np.float64).ravel())
        masked_weight = model["Ms"][0][None, :, :] * hidden_mask[:, None, :]
        jacobian_vectors = np.einsum("nfh,hc->nfc", masked_weight, model["Ms"][1], optimize=True)
        jacobian_norm = adjacency_column_norm[:, None] * np.linalg.norm(jacobian_vectors, axis=2)
    count = max(1, int(round(budget * residual.size)))
    residual_target_bits = sparse_cost_bits(residual.shape, count=count)
    if residual_mode in ("downstream", "downstream_logit", "downstream_jacobian", "top_abs", "random", "a2q_node_budget"):
        indices = select_residual_indices(
            residual,
            model["Ms"][0],
            count=count,
            mode=residual_mode,
            seed=8000 + rank,
            output_weight=model["Ms"][1],
            jacobian_norm=jacobian_norm,
        )
        reconstructed = basis["reconstructed"] + sparse_reconstruct(residual, indices)
        residual_payload = residual_target_bits
        residual_padded = residual_target_bits
        coefficient_count = count
    elif residual_mode == "uniform":
        dense = dense_uniform_at_budget(residual, target_bits=residual_target_bits)
        reconstructed = basis["reconstructed"] + dense["reconstructed"]
        residual_payload = dense["payload_bits"]
        residual_padded = dense["padded_bits"]
        coefficient_count = residual.size
    elif residual_mode == "one_spike":
        one = one_spike_at_budget(residual, target_bits=residual_target_bits)
        reconstructed = basis["reconstructed"] + one["reconstructed"]
        residual_payload = one["payload_bits"]
        residual_padded = one["padded_bits"]
        coefficient_count = one["coefficient_count"]
    elif residual_mode == "none":
        reconstructed = basis["reconstructed"]
        residual_payload = residual_padded = 0
        coefficient_count = 0
    else:
        raise ValueError(residual_mode)
    cost = {
        "basis_bits": basis["basis_bits"],
        "residual_target_bits": residual_target_bits,
        "residual_payload_bits": residual_payload,
        "residual_padded_bits": residual_padded,
        "total_padded_bits": basis["basis_bits"] + residual_padded,
        "coefficient_count": coefficient_count,
        "dimension_compression": messages.size / (rank * sum(messages.shape)),
    }
    return evaluate_reconstruction(case, reconstructed, cost)


def full_float(case: dict) -> dict:
    messages = case["messages"]
    cost = {
        "basis_bits": int(messages.size * 32),
        "residual_target_bits": 0,
        "residual_payload_bits": 0,
        "residual_padded_bits": 0,
        "total_padded_bits": int(messages.size * 32),
        "coefficient_count": messages.size,
        "dimension_compression": 1.0,
    }
    return evaluate_reconstruction(case, messages.copy(), cost)


def run_grid(phase: str) -> dict:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA RTX3060 required")
    methods = {
        "baseline": {
            "svd": ("top_abs", "random", "a2q_node_budget", "uniform", "one_spike", "none"),
            "random_projection": ("top_abs", "random", "a2q_node_budget", "none"),
        },
        "method": {
            "svd": ("downstream_jacobian",),
            "random_projection": ("downstream_jacobian",),
        },
    }[phase]
    rows = []
    for dataset in DATASETS:
        for seed in SEEDS:
            case = load_case(dataset, seed)
            hidden_mask = case["hidden"] > 0
            adjacency_column_norm = np.sqrt(np.asarray(case["data"]["adj"].power(2).sum(axis=0), dtype=np.float64).ravel())
            masked_weight = case["model"]["Ms"][0][None, :, :] * hidden_mask[:, None, :]
            jacobian_vectors = np.einsum("nfh,hc->nfc", masked_weight, case["model"]["Ms"][1], optimize=True)
            jacobian_norm = adjacency_column_norm[:, None] * np.linalg.norm(jacobian_vectors, axis=2)
            for rank in RANKS:
                basis_cache = {
                    "svd": basis_svd(case["messages"], rank),
                    "random_projection": basis_random(case["messages"], rank, seed=7000 + rank),
                }
                for budget in BUDGETS:
                    for basis_name, residual_modes in methods.items():
                        for residual_mode in residual_modes:
                            row = make_variant(
                                case,
                                basis_name,
                                residual_mode,
                                rank,
                                budget,
                                basis=basis_cache[basis_name],
                                jacobian_norm=jacobian_norm,
                            )
                            row.update({"dataset": dataset, "seed": seed, "rank": rank, "budget": budget, "basis": basis_name, "residual_mode": residual_mode})
                            rows.append(row)
            if phase == "baseline":
                row = full_float(case)
                row.update({"dataset": dataset, "seed": seed, "rank": 0, "budget": 0.0, "basis": "full_float", "residual_mode": "none"})
                rows.append(row)
    return {"phase": phase, "device": torch.cuda.get_device_name(0), "rows": rows}


def run_timing() -> dict:
    rows = []
    for dataset in DATASETS:
        for seed in SEEDS:
            case = load_case(dataset, seed)
            hidden_mask = case["hidden"] > 0
            adjacency_column_norm = np.sqrt(np.asarray(case["data"]["adj"].power(2).sum(axis=0), dtype=np.float64).ravel())
            masked_weight = case["model"]["Ms"][0][None, :, :] * hidden_mask[:, None, :]
            jacobian_vectors = np.einsum("nfh,hc->nfc", masked_weight, case["model"]["Ms"][1], optimize=True)
            jacobian_norm = adjacency_column_norm[:, None] * np.linalg.norm(jacobian_vectors, axis=2)
            for method in ("svd_only", "top_abs", "a2q_node_budget", "uniform", "one_spike", "downstream_jacobian"):
                timings = []
                for repeat in range(10):
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                        torch.cuda.reset_peak_memory_stats()
                    start = time.perf_counter()
                    row = make_variant(
                        case,
                        "svd",
                        method if method != "svd_only" else "none",
                        128,
                        0.01,
                        jacobian_norm=jacobian_norm,
                    )
                    if torch.cuda.is_available():
                        torch.cuda.synchronize()
                    elapsed = time.perf_counter() - start
                    peak = torch.cuda.max_memory_allocated() / 2**20 if torch.cuda.is_available() else 0.0
                    if repeat >= 3:
                        timings.append({"elapsed_sec": elapsed, "peak_memory_mb": peak, "T2": row["T2"], "T4": row["T4"]})
                rows.append({
                    "dataset": dataset,
                    "seed": seed,
                    "method": method,
                    "warmups": 3,
                    "timed_repeats": timings,
                    "median_elapsed_sec": float(np.median([x["elapsed_sec"] for x in timings])),
                    "p95_elapsed_sec": float(np.quantile([x["elapsed_sec"] for x in timings], 0.95)),
                    "peak_memory_mb": float(np.max([x["peak_memory_mb"] for x in timings])),
                })
    return {"device": torch.cuda.get_device_name(0), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("baseline", "method", "timing"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_timing() if args.phase == "timing" else run_grid(args.phase)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"phase": args.phase, "rows": len(result["rows"]), "device": result["device"]}))


if __name__ == "__main__":
    main()
