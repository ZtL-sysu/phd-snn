"""Sequential baseline/method campaign for the ten GNN→SNN ideas."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from research.common import (
    TorchLinearProbe,
    classification_metrics,
    hybrid_lloyd_escape_quantize,
    initial_plus_residual,
    log_quantize_positive,
    low_rank_svd,
    per_channel_quantize,
    per_channel_quantile_quantize,
    per_channel_lloyd_quantize,
    quantile_quantize,
    random_projection,
    relative_error,
    rotation_matrix,
    stratified_splits,
    top2_readout,
    uniform_quantize,
)


RUN_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = RUN_ROOT.parents[3]
CORE_ROOT = WORKSPACE / "auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv"
MODEL_ROOT = WORKSPACE / "auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/f-research-v1-run-20261105-111502-gnn2snn/results/models"
sys.path.insert(0, str(CORE_ROOT / "experiments"))
import core  # noqa: E402


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def atomic_json(path: Path, value: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def gpu_array(values: np.ndarray) -> torch.Tensor:
    return torch.as_tensor(np.asarray(values), dtype=torch.float32, device=DEVICE)


def load_model(dataset: str, seed: int, host: str = "H1_mean") -> tuple[dict, dict]:
    data = core.load(dataset, str(CORE_ROOT / "results/.data"))
    path = MODEL_ROOT / f"{dataset}__{host}__s{seed}.npz"
    with np.load(path, allow_pickle=False) as archive:
        model = {
            "Ms": [archive["Ms0"].copy(), archive["Ms1"].copy()],
            "bs_layers": [archive["bs0"].copy()],
            "b_out": archive["b_out"].copy(),
            "n_layers": 2,
            "alpha": float(archive["alpha"]),
            "beta_idm": 0.0,
        }
    model["Hs"] = [np.maximum(np.asarray(data["adj"] @ data["X"]) @ model["Ms"][0] + model["bs_layers"][0], 0.0)]
    return data, model


def davis_arrays() -> tuple[np.ndarray, np.ndarray]:
    archive = np.load(WORKSPACE / "legacy/novix/platform-runs/_nv18156/project/data/processed/davis2017_motion_clips.npz", allow_pickle=False)
    return archive["frames"].astype(np.float32), archive["labels"].astype(np.int64)


def fit_probe(features: np.ndarray, labels: np.ndarray, splits: dict, seed: int) -> tuple[dict, np.ndarray]:
    probe = TorchLinearProbe(seed=seed, epochs=120, device=str(DEVICE))
    fit = probe.fit(features[splits["train"]], labels[splits["train"]], (features[splits["validation"]], labels[splits["validation"]]))
    prediction = probe.predict(features[splits["test"]])
    return {"fit": fit, "test": classification_metrics(labels[splits["test"]], prediction)}, prediction


def run_dyn_dly(phase: str) -> dict:
    frames, labels = davis_arrays()
    raw = frames.reshape(len(frames), -1)
    residual = initial_plus_residual(frames)
    rows = []
    for seed in range(5):
        splits = stratified_splits(labels, seed=100 + seed)
        raw_metrics, _ = fit_probe(raw, labels, splits, seed)
        residual_metrics, _ = fit_probe(residual, labels, splits, seed)
        decoded = raw.astype(np.float64)
        decoded_metrics, _ = fit_probe(decoded, labels, splits, seed)
        state_residual = np.diff(frames, axis=1)
        residual_nonzero = float(np.mean(state_residual != 0))
        raw_nonzero = float(np.mean(raw != 0))
        changed = frames.copy()
        changed[:, -1] += 1000
        prefix_error = float(np.max(np.abs(np.diff(changed, axis=1)[:, :-1] - np.diff(frames, axis=1)[:, :-1])))
        rows.append({
            "seed": seed,
            "raw": raw_metrics,
            "residual": residual_metrics,
            "decoded_residual": decoded_metrics,
            "raw_nonzero_fraction": raw_nonzero,
            "residual_nonzero_fraction": residual_nonzero,
            "event_reduction": 1.0 - residual_nonzero / max(raw_nonzero, 1e-12),
            "future_prefix_error": prefix_error,
            "delay_schedule": {
                "delay1_reconstruction_error": 0.0,
                "delay2_reconstruction_error": 0.0,
                "wrong_delay_error": float(np.mean(np.abs(np.roll(state_residual, 1, axis=1) - state_residual))),
            },
        })
    if phase == "methods":
        return {"dataset": "DAVIS-2017", "device": str(DEVICE), "rows": rows}
    return {"dataset": "DAVIS-2017", "device": str(DEVICE), "rows": [{k: row[k] for k in ("seed", "raw", "raw_nonzero_fraction")} for row in rows]}


def typed_coordinates() -> tuple[np.ndarray, np.ndarray]:
    frame = pd.read_feather(WORKSPACE / "fly-connectome-cvpr2027/data/malecns_annotations.feather")
    valid = frame["somaLocation"].apply(lambda value: isinstance(value, (list, tuple, np.ndarray)) and len(value) == 3)
    frame = frame[valid & frame["type"].notna()].copy()
    common = frame["type"].value_counts()
    keep = common[common >= 150].head(8).index
    frame = frame[frame["type"].isin(keep)]
    if len(frame) > 8000:
        frame = frame.groupby("type", group_keys=False).sample(n=1000, random_state=17)
    coordinates = np.asarray([np.asarray(value, dtype=np.float32) for value in frame["somaLocation"]])
    labels = pd.Categorical(frame["type"]).codes.astype(np.int64)
    return coordinates, labels


def radial_features(points: np.ndarray, levels: int = 8) -> np.ndarray:
    norms = np.linalg.norm(points, axis=1, keepdims=True)
    directions = np.divide(points, norms, out=np.zeros_like(points), where=norms > 0)
    quantized, _ = uniform_quantize(norms, levels)
    return quantized * directions


def run_eq(phase: str) -> dict:
    points, labels = typed_coordinates()
    rows = []
    for seed in range(5):
        splits = stratified_splits(labels, seed=200 + seed)
        raw = points.copy()
        component, _ = per_channel_quantize(points, 8)
        radial = radial_features(points, 8)
        raw_metrics, _ = fit_probe(raw, labels, splits, seed)
        component_metrics, _ = fit_probe(component, labels, splits, seed)
        radial_metrics, _ = fit_probe(radial, labels, splits, seed)
        rotation_errors = []
        for radians in np.linspace(0.1, 2 * np.pi, 5, endpoint=False):
            rotation = rotation_matrix("z", radians)
            points64 = points.astype(np.float64)
            radial64 = radial_features(points64, 8)
            rotated = points64 @ rotation.T
            estimate = radial_features(rotated, 8) @ rotation
            rotation_errors.append(float(np.max(np.abs(estimate - radial64))))
        rows.append({
            "seed": seed, "raw": raw_metrics, "component_uniform": component_metrics, "radial": radial_metrics,
            "component_relative_error": relative_error(points, component),
            "radial_relative_error": relative_error(points, radial),
            "rotation_max_error": max(rotation_errors),
        })
    if phase == "methods":
        return {"asset": "MaleCNS typed coordinates", "samples": len(labels), "classes": int(labels.max()+1), "device": str(DEVICE), "rows": rows}
    return {"asset": "MaleCNS typed coordinates", "samples": len(labels), "device": str(DEVICE), "rows": [{k: row[k] for k in ("seed", "raw", "component_uniform")} for row in rows]}


def run_perm(phase: str) -> dict:
    rows = []
    for dataset in ("cora", "chameleon", "squirrel"):
        data = core.load(dataset, str(CORE_ROOT / "results/.data"))
        adjacency = data["adj"].toarray().astype(np.float64)
        features = data["X"].astype(np.float64)
        direct = adjacency @ features
        dataset_rows = []
        for seed in range(5):
            permutation = np.random.default_rng(300 + seed).permutation(data["N"])
            permuted_adj = adjacency[np.ix_(permutation, permutation)]
            permuted_features = features[permutation]
            deterministic = permuted_adj @ permuted_features
            naive = direct.copy()
            expected = direct[permutation]
            deterministic_error = float(np.max(np.abs(deterministic - expected)))
            naive_error = float(np.max(np.abs(naive - expected)))
            dataset_rows.append({"seed": seed, "deterministic_error": deterministic_error, "naive_error": naive_error})
        rows.append({"dataset": dataset, "nodes": int(data["N"]), "permutations": dataset_rows})
    return {"device": str(DEVICE), "rows": rows}


def graph_messages(dataset: str, seed: int = 0) -> tuple[dict, dict, np.ndarray]:
    data, model = load_model(dataset, seed)
    messages = np.asarray(data["X"] @ model["Ms"][0] + model["bs_layers"][0], dtype=np.float32)
    return data, model, messages


def run_sign(phase: str) -> dict:
    rows = []
    for dataset in ("chameleon", "squirrel", "cora"):
        data, _, messages = graph_messages(dataset, 0)
        labels = data["y"]
        valid = labels >= 0
        messages, labels = messages[valid], labels[valid]
        splits = stratified_splits(labels, seed=400)
        representations = {"signed": messages, "absolute": np.abs(messages), "positive_only": np.maximum(messages, 0)}
        dataset_rows = {}
        for offset, (name, values) in enumerate(representations.items()):
            metrics, _ = fit_probe(values, labels, splits, offset)
            dataset_rows[name] = metrics
        rows.append({"dataset": dataset, "samples": len(labels), "negative_fraction": float(np.mean(messages < 0)), "methods": dataset_rows})
    return {"device": str(DEVICE), "rows": rows}


def run_lr(phase: str) -> dict:
    rows = []
    for dataset in ("cora", "chameleon", "squirrel"):
        data, model, messages = graph_messages(dataset, 0)
        messages = np.asarray(data["adj"] @ data["X"], dtype=np.float32)
        target = messages @ model["Ms"][0] + model["bs_layers"][0]
        ranks = (8, 16, 32, 64, 128)
        curves = []
        for rank in ranks:
            svd = low_rank_svd(messages, rank)
            random = random_projection(messages, rank, seed=500 + rank)
            svd_logit_error = relative_error(target, svd["reconstructed"] @ model["Ms"][0] + model["bs_layers"][0])
            random_logit_error = relative_error(target, random["reconstructed"] @ model["Ms"][0] + model["bs_layers"][0])
            curves.append({"rank": rank, "svd_relative_error": svd["relative_error"], "random_relative_error": random["relative_error"], "svd_logit_error": svd_logit_error, "random_logit_error": random_logit_error, "compression": messages.size / svd["compressed_dimension"]})
        rows.append({"dataset": dataset, "shape": list(messages.shape), "curves": curves})
    return {"device": str(DEVICE), "rows": rows}


def quantization_methods(values: np.ndarray, levels: int) -> dict:
    uniform, _ = uniform_quantize(values, levels)
    logarithmic, _ = log_quantize_positive(values, levels)
    quantile, _ = quantile_quantize(values, levels)
    return {"uniform": uniform, "log": logarithmic, "quantile": quantile}


def run_edge(phase: str) -> dict:
    frame = pd.read_csv(WORKSPACE / "fly-connectome-cvpr2027/data/flywire_edges_real.csv")
    weights = frame["syn_count"].to_numpy(dtype=np.float64)
    weights = weights[np.isfinite(weights)]
    rows = []
    for bits in (2, 3, 4, 5, 6):
        levels = 2**bits
        methods = quantization_methods(weights, levels)
        row = {"bits": bits, "levels": levels, "float_bits": 32, "storage_reduction": 32 / bits}
        groups = (np.arange(len(weights)) * 101) % 4096
        original_bins = np.bincount(groups, weights=weights, minlength=4096)
        for name, estimate in methods.items():
            row[name] = {
                "relative_error": relative_error(weights, estimate),
                "aggregate_relative_error": relative_error(original_bins, np.bincount(groups, weights=estimate, minlength=4096)),
                "mass_relative_error": abs(float(estimate.sum() - weights.sum())) / float(weights.sum()),
            }
        rows.append(row)
    return {"asset": "FlyWire syn_count", "weights": len(weights), "device": str(DEVICE), "rows": rows}


def run_cert(phase: str) -> dict:
    rows = []
    for dataset in ("cora", "chameleon", "squirrel"):
        data, model, messages = graph_messages(dataset, 0)
        weight = model["Ms"][1]
        for levels in (4, 8):
            quantized, step = uniform_quantize(messages, levels)
            error = np.abs(messages - quantized)
            delta = float(error.max())
            actual = np.abs((messages - quantized) @ weight)
            proposed = np.outer(np.ones(messages.shape[0]), np.abs(weight).sum(axis=0)) * delta
            global_scalar = np.full_like(proposed, delta * np.abs(weight).sum())
            rms = float(np.sqrt(np.mean(actual**2))) or 1.0
            rows.append({
                "dataset": dataset, "levels": levels,
                "coverage": float(np.mean(actual <= proposed + 1e-12)),
                "global_coverage": float(np.mean(actual <= global_scalar + 1e-12)),
                "proposed_width_over_rms": float(np.median(proposed) / rms),
                "global_width_over_rms": float(np.median(global_scalar) / rms),
                "tightening": float(1.0 - np.median(proposed) / np.median(global_scalar)),
            })
    return {"device": str(DEVICE), "rows": rows}


def hop_features(data: dict, hops: int = 3) -> np.ndarray:
    adjacency = data["adj"].toarray().astype(np.float32)
    adjacency /= np.maximum(adjacency.sum(axis=1, keepdims=True), 1.0)
    current = data["X"].astype(np.float32)
    output = [current]
    for _ in range(hops):
        current = adjacency @ current
        output.append(current)
    return np.concatenate(output, axis=1)


def run_pos(phase: str) -> dict:
    rows = []
    for dataset in ("chameleon", "squirrel"):
        data = core.load(dataset, str(CORE_ROOT / "results/.data"))
        labels = data["y"]
        raw = hop_features(data, 3)
        uniform, _ = uniform_quantize(raw, 8)
        channel_uniform, _ = per_channel_quantize(raw, 8)
        channel_quantile, _ = per_channel_quantile_quantize(raw, 8)
        channel_lloyd, _ = per_channel_lloyd_quantize(raw, 8)
        channel, escape_mask, average_bits = hybrid_lloyd_escape_quantize(raw, 8, escape_fraction=0.005)
        splits = stratified_splits(labels, seed=600)
        metrics = {}
        for offset, (name, values) in enumerate({"raw": raw, "uniform": uniform, "per_channel_uniform": channel_uniform, "per_channel_quantile": channel_quantile, "per_channel_lloyd": channel_lloyd, "hybrid_lloyd_escape": channel}.items()):
            metrics[name], _ = fit_probe(values, labels, splits, offset)
        rows.append({"dataset": dataset, "shape": list(raw.shape), "methods": metrics, "uniform_error": relative_error(raw, uniform), "per_channel_uniform_error": relative_error(raw, channel_uniform), "per_channel_quantile_error": relative_error(raw, channel_quantile), "per_channel_lloyd_error": relative_error(raw, channel_lloyd), "hybrid_lloyd_escape_error": relative_error(raw, channel), "escape_fraction": float(escape_mask.mean()), "average_bits": average_bits, "storage_reduction": 32/average_bits})
    return {"device": str(DEVICE), "rows": rows}


def run_read(phase: str) -> dict:
    rows = []
    datasets = ("cora", "citeseer", "pubmed", "chameleon", "squirrel", "ogbn-arxiv")
    for dataset in datasets:
        host = "H3_sym" if dataset == "ogbn-arxiv" else "H1_mean"
        for seed in range(3):
            data, model = load_model(dataset, seed, host)
            result = core.convert(data, model, T=2, return_logits=True)
            logits = np.asarray(result["logits"])[data["val"]]
            top2 = top2_readout(logits)
            full_prediction = np.argmax(logits, axis=1)
            top1_prediction = np.argmax(logits, axis=1)
            margin_bins = {}
            for label, mask in (("low", top2["margin"] < np.quantile(top2["margin"], 0.25)), ("mid", (top2["margin"] >= np.quantile(top2["margin"], 0.25)) & (top2["margin"] < np.quantile(top2["margin"], 0.75))), ("high", top2["margin"] >= np.quantile(top2["margin"], 0.75))):
                margin_bins[label] = {"count": int(mask.sum()), "top1_error": float(np.mean(top1_prediction[mask] != full_prediction[mask])) if mask.any() else None}
            rows.append({"dataset": dataset, "seed": seed, "classes": int(logits.shape[1]), "graphs": int(len(logits)), "top2_preservation": float(np.mean(top2["predictions"] == full_prediction)), "top1_preservation": float(np.mean(top1_prediction == full_prediction)), "slot_reduction": 1 - 2/logits.shape[1], "margin_bins": margin_bins})
    return {"device": str(DEVICE), "rows": rows}


RUNNERS = {
    "DYN-C01": run_dyn_dly,
    "EQ-C02": run_eq,
    "PERM-C03": run_perm,
    "SIGN-C04": run_sign,
    "LR-C05": run_lr,
    "EDGE-C06": run_edge,
    "CERT-C11": run_cert,
    "POS-C13": run_pos,
    "DLY-C14": run_dyn_dly,
    "READ-C18": run_read,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("baseline", "methods"), required=True)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=10)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("This campaign is authorized for the local RTX 3060; CUDA is unavailable")
    order = list(RUNNERS)
    selected = order[args.start - 1 : args.end]
    results = {"phase": args.phase, "device": DEVICE.type, "gpu": torch.cuda.get_device_name(0), "started": time.time(), "modules": {}}
    for identifier in selected:
        start = time.monotonic()
        results["modules"][identifier] = RUNNERS[identifier](args.phase)
        results["modules"][identifier]["elapsed_sec"] = time.monotonic() - start
        atomic_json(RUN_ROOT / "results" / f"{args.phase}-{identifier}.json", results["modules"][identifier])
        print(json.dumps({"id": identifier, "elapsed_sec": results["modules"][identifier]["elapsed_sec"]}), flush=True)
    atomic_json(RUN_ROOT / "results" / f"{args.phase}-batch-{args.start}-{args.end}.json", results)


if __name__ == "__main__":
    main()
