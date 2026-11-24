"""Baseline-first LR-C05 experiment driver."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

from research.lr_core import (
    low_rank_reconstruct,
    random_residual_indices,
    rate_convert_hidden,
    residual_reconstruct,
    select_residual_indices,
    storage_bits,
    uniform_residual_reconstruct,
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
RESIDUAL_FRACTIONS = (0.005, 0.01, 0.02)


def load_case(dataset: str, seed: int) -> tuple[dict, dict, np.ndarray, np.ndarray, np.ndarray]:
    data = core.load(dataset, str(CORE_ROOT / "results/.data"))
    path = MODEL_ROOT / f"{dataset}__H1_mean__s{seed}.npz"
    with np.load(path, allow_pickle=False) as archive:
        model = {
            "Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()],
            "bs_layers": [archive["bs0"].copy()],
            "b_out": archive["b_out"].copy(),
        }
    messages = np.asarray(data["adj"] @ data["X"], dtype=np.float32)
    hidden = np.maximum(messages @ model["Ms"][0] + model["bs_layers"][0], 0.0)
    teacher_logits = np.asarray(data["adj"] @ hidden @ model["Ms"][1] + model["b_out"], dtype=np.float32)
    return data, model, messages, hidden, teacher_logits


def converted_outputs(data: dict, model: dict, reconstructed_messages: np.ndarray, t_steps: int) -> tuple[np.ndarray, np.ndarray]:
    hidden = np.maximum(reconstructed_messages @ model["Ms"][0] + model["bs_layers"][0], 0.0)
    decoded = rate_convert_hidden(hidden, t_steps=t_steps)
    logits = np.asarray(data["adj"] @ decoded @ model["Ms"][1] + model["b_out"], dtype=np.float32)
    return hidden, logits


def metrics(data: dict, logits: np.ndarray, teacher_logits: np.ndarray) -> dict:
    mask = data["val"]
    labels = data["y"][mask]
    prediction = np.argmax(logits[mask], axis=1)
    teacher_prediction = np.argmax(teacher_logits[mask], axis=1)
    return {
        "accuracy": float(np.mean(prediction == labels)),
        "teacher_agreement": float(np.mean(prediction == teacher_prediction)),
    }


def full_and_svd_payloads(dataset: str, seed: int, rank: int, case: tuple, rank_result: dict) -> dict:
    data, model, messages, hidden, teacher_logits = case
    full = rank_result
    reconstructed = full["reconstructed"]
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    hidden_hat, logits = converted_outputs(data, model, reconstructed, t_steps=2)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    peak_memory_mb = torch.cuda.max_memory_allocated() / 2**20 if torch.cuda.is_available() else 0.0
    return {
        "dataset": dataset,
        "seed": seed,
        "rank": rank,
        "shape": list(messages.shape),
        "message_relative_error": full["relative_error"],
        "hidden_relative_error": float(np.linalg.norm(hidden - hidden_hat) / max(np.linalg.norm(hidden), 1e-12)),
        "teacher": metrics(data, teacher_logits, teacher_logits),
        "converted": metrics(data, logits, teacher_logits),
        "storage_bits": storage_bits(messages.shape, rank=rank, residual_count=0),
        "elapsed_sec": elapsed,
        "peak_memory_mb": peak_memory_mb,
    }


def evaluate_residual_variant(
    *,
    dataset: str,
    seed: int,
    rank: int,
    residual_fraction: float,
    method: str,
    case: tuple,
    rank_result: dict,
) -> dict:
    data, model, messages, hidden, teacher_logits = case
    low_rank = rank_result["reconstructed"]
    residual = messages - low_rank
    count = max(1, int(round(residual_fraction * residual.size)))
    proposed_storage = storage_bits(messages.shape, rank=rank, residual_count=count)
    if method == "downstream_residual":
        indices = select_residual_indices(residual, model["Ms"][0], count=count)
        residual_hat = residual_reconstruct(residual, indices)
    elif method == "random_residual":
        indices = random_residual_indices(residual.shape, count=count, seed=10000 + seed * 101 + rank)
        residual_hat = residual_reconstruct(residual, indices)
    elif method == "uniform_residual":
        lowrank_bits = storage_bits(messages.shape, rank=rank, residual_count=0)
        available = max(residual.size, proposed_storage - lowrank_bits)
        bits = max(1, min(8, int(available // residual.size)))
        residual_hat = uniform_residual_reconstruct(residual, bits=bits)
    elif method == "svd_only":
        residual_hat = np.zeros_like(residual)
        count = 0
    else:
        raise ValueError(method)
    reconstructed = low_rank + residual_hat
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    hidden_hat, logits2 = converted_outputs(data, model, reconstructed, t_steps=2)
    _, logits4 = converted_outputs(data, model, reconstructed, t_steps=4)
    elapsed = time.perf_counter() - start
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    peak_memory_mb = torch.cuda.max_memory_allocated() / 2**20 if torch.cuda.is_available() else 0.0
    storage = storage_bits(messages.shape, rank=rank, residual_count=count)
    return {
        "dataset": dataset,
        "seed": seed,
        "rank": rank,
        "residual_fraction": residual_fraction,
        "method": method,
        "residual_count": count,
        "storage_bits": storage,
        "storage_per_element_bits": storage / residual.size,
        "message_relative_error": float(np.linalg.norm(messages - reconstructed) / max(np.linalg.norm(messages), 1e-12)),
        "hidden_relative_error": float(np.linalg.norm(hidden - hidden_hat) / max(np.linalg.norm(hidden), 1e-12)),
        "T2": metrics(data, logits2, teacher_logits),
        "T4": metrics(data, logits4, teacher_logits),
        "elapsed_sec": elapsed,
        "peak_memory_mb": peak_memory_mb,
    }


def run_phase(phase: str) -> dict:
    if not torch.cuda.is_available():
        raise RuntimeError("RTX3060 CUDA is required")
    rows = []
    methods = ("svd_only", "random_residual", "uniform_residual") if phase == "baseline" else ("downstream_residual",)
    for dataset in DATASETS:
        for seed in SEEDS:
            case = load_case(dataset, seed)
            for rank in RANKS:
                rank_result = low_rank_reconstruct(case[2], rank=rank)
                for fraction in RESIDUAL_FRACTIONS:
                    for method in methods:
                        rows.append(evaluate_residual_variant(
                            dataset=dataset,
                            seed=seed,
                            rank=rank,
                            residual_fraction=fraction,
                            method=method,
                            case=case,
                            rank_result=rank_result,
                        ))
            rank128 = low_rank_reconstruct(case[2], rank=128)
            rows.append(full_and_svd_payloads(dataset, seed, rank=128, case=case, rank_result=rank128))
    return {"phase": phase, "device": torch.cuda.get_device_name(0), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("baseline", "method"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_phase(args.phase)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"phase": args.phase, "rows": len(result["rows"]), "device": result["device"]}))


if __name__ == "__main__":
    main()
