"""Shared deterministic utilities for the ten-module experiment campaign."""

from __future__ import annotations

import numpy as np
import torch
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split


def stratified_splits(labels: np.ndarray, seed: int, test_size: float = 0.2, validation_size: float = 0.2) -> dict[str, np.ndarray]:
    labels = np.asarray(labels)
    indices = np.arange(len(labels))
    train_val, test = train_test_split(indices, test_size=test_size, random_state=seed, stratify=labels)
    relative_validation = validation_size / (1.0 - test_size)
    train, validation = train_test_split(train_val, test_size=relative_validation, random_state=seed, stratify=labels[train_val])
    return {"train": train, "validation": validation, "test": test}


def classification_metrics(y_true: np.ndarray, prediction: np.ndarray) -> dict:
    y_true = np.asarray(y_true)
    prediction = np.asarray(prediction)
    return {
        "accuracy": float(accuracy_score(y_true, prediction)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, prediction)),
    }


def uniform_quantize(values: np.ndarray, levels: int) -> tuple[np.ndarray, float]:
    values = np.asarray(values, dtype=np.float64)
    if levels < 2:
        raise ValueError("levels must be >=2")
    minimum, maximum = float(values.min()), float(values.max())
    step = (maximum - minimum) / (levels - 1)
    if step == 0:
        return values.copy(), 0.0
    return np.round((values - minimum) / step) * step + minimum, step


def per_channel_quantize(values: np.ndarray, levels: int) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=np.float64)
    minimum = values.min(axis=0)
    maximum = values.max(axis=0)
    step = np.maximum((maximum - minimum) / (levels - 1), np.finfo(np.float64).eps)
    return np.round((values - minimum) / step) * step + minimum, step


def per_channel_quantile_quantize(values: np.ndarray, levels: int) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or levels < 2:
        raise ValueError("values must be [N,D] and levels >=2")
    quantized = np.empty_like(values)
    representatives = np.empty((levels, values.shape[1]), dtype=np.float64)
    for channel in range(values.shape[1]):
        column = values[:, channel]
        edges = np.quantile(column, np.linspace(0.0, 1.0, levels + 1))
        bins = np.clip(np.searchsorted(edges[1:-1], column, side="right"), 0, levels - 1)
        channel_reps = np.array([np.mean(column[bins == index]) if np.any(bins == index) else edges[index] for index in range(levels)])
        representatives[:, channel] = channel_reps
        quantized[:, channel] = channel_reps[bins]
    return quantized, representatives


def per_channel_lloyd_quantize(values: np.ndarray, levels: int, *, iterations: int = 20) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or levels < 2 or iterations < 1:
        raise ValueError("values must be [N,D], levels >=2 and iterations >=1")
    quantized = np.empty_like(values)
    representatives = np.empty((levels, values.shape[1]), dtype=np.float64)
    for channel in range(values.shape[1]):
        column = values[:, channel]
        reps = np.quantile(column, np.linspace(0.0, 1.0, levels))
        for _ in range(iterations):
            assignment = np.argmin(np.abs(column[:, None] - reps[None, :]), axis=1)
            updated = reps.copy()
            for level in range(levels):
                members = column[assignment == level]
                if members.size:
                    updated[level] = members.mean()
            if np.allclose(updated, reps, rtol=0, atol=1e-12):
                reps = updated
                break
            reps = updated
        assignment = np.argmin(np.abs(column[:, None] - reps[None, :]), axis=1)
        quantized[:, channel] = reps[assignment]
        representatives[:, channel] = reps
    return quantized, representatives


def hybrid_lloyd_escape_quantize(values: np.ndarray, levels: int, *, escape_fraction: float, iterations: int = 20) -> tuple[np.ndarray, np.ndarray, float]:
    values = np.asarray(values, dtype=np.float64)
    if not 0 <= escape_fraction < 1:
        raise ValueError("escape_fraction must be in [0,1)")
    quantized, representatives = per_channel_lloyd_quantize(values, levels, iterations=iterations)
    error = np.abs(values - quantized)
    count = int(round(escape_fraction * error.size))
    escape = np.zeros(error.shape, dtype=bool)
    if count:
        flat = np.argpartition(error.ravel(), -count)[-count:]
        escape.ravel()[flat] = True
    hybrid = np.where(escape, values, quantized)
    base_bits = float(np.log2(levels))
    average_bits = (1.0 - escape_fraction) * base_bits + escape_fraction * 32.0
    return hybrid, escape, average_bits


def initial_plus_residual(frames: np.ndarray) -> np.ndarray:
    frames = np.asarray(frames, dtype=np.float64)
    if frames.ndim < 2 or frames.shape[1] < 2:
        raise ValueError("frames must be [N,T,...] with T>=2")
    flattened = frames.reshape(frames.shape[0], frames.shape[1], -1)
    initial = flattened[:, 0]
    residual = np.diff(flattened, axis=1).reshape(frames.shape[0], -1)
    return np.concatenate([initial, residual], axis=1)


def log_quantize_positive(values: np.ndarray, levels: int) -> tuple[np.ndarray, float]:
    values = np.asarray(values, dtype=np.float64)
    if np.any(values < 0):
        raise ValueError("log quantization requires nonnegative values")
    transformed = np.log1p(values)
    quantized, step = uniform_quantize(transformed, levels)
    return np.expm1(quantized), step


def quantile_quantize(values: np.ndarray, levels: int) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=np.float64)
    edges = np.quantile(values, np.linspace(0.0, 1.0, levels + 1))
    bins = np.clip(np.searchsorted(edges[1:-1], values, side="right"), 0, levels - 1)
    representatives = np.array([np.mean(values[bins == index]) if np.any(bins == index) else edges[index] for index in range(levels)])
    return representatives[bins], representatives


def relative_error(reference: np.ndarray, estimate: np.ndarray) -> float:
    reference = np.asarray(reference, dtype=np.float64)
    estimate = np.asarray(estimate, dtype=np.float64)
    return float(np.linalg.norm(reference - estimate) / max(np.linalg.norm(reference), 1e-12))


def low_rank_svd(matrix: np.ndarray, rank: int) -> dict:
    matrix = np.asarray(matrix, dtype=np.float64)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tensor = torch.as_tensor(matrix, dtype=torch.float32, device=device)
    left, singular, right = torch.linalg.svd(tensor, full_matrices=False)
    reconstructed = ((left[:, :rank] * singular[:rank]) @ right[:rank]).cpu().numpy().astype(np.float64)
    return {"reconstructed": reconstructed, "relative_error": relative_error(matrix, reconstructed), "compressed_dimension": rank * sum(matrix.shape), "device": str(device)}


def random_projection(matrix: np.ndarray, rank: int, seed: int) -> dict:
    matrix = np.asarray(matrix, dtype=np.float64)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    projection = torch.randn((matrix.shape[1], rank), generator=generator, dtype=torch.float32) / np.sqrt(rank)
    tensor = torch.as_tensor(matrix, dtype=torch.float32, device=device)
    projection = projection.to(device)
    reconstructed = ((tensor @ projection) @ projection.T).cpu().numpy().astype(np.float64)
    return {"reconstructed": reconstructed, "relative_error": relative_error(matrix, reconstructed), "compressed_dimension": rank * sum(matrix.shape), "device": str(device)}


def top2_readout(logits: np.ndarray) -> dict:
    logits = np.asarray(logits)
    order = np.argsort(-logits, axis=1)
    top = order[:, :2]
    rows = np.arange(len(logits))
    values = logits[rows[:, None], top]
    return {"predictions": top[:, 0], "indices": top, "values": values, "margin": values[:, 0] - values[:, 1]}


def rotation_matrix(axis: str, radians: float) -> np.ndarray:
    cosine, sine = np.cos(radians), np.sin(radians)
    if axis == "z":
        return np.array([[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]])
    if axis == "x":
        return np.array([[1.0, 0.0, 0.0], [0.0, cosine, -sine], [0.0, sine, cosine]])
    if axis == "y":
        return np.array([[cosine, 0.0, sine], [0.0, 1.0, 0.0], [-sine, 0.0, cosine]])
    raise ValueError("unknown axis")


def paired_bootstrap_difference(first: np.ndarray, second: np.ndarray, seed: int, draws: int = 2000) -> dict:
    first = np.asarray(first, dtype=float)
    second = np.asarray(second, dtype=float)
    rng = np.random.default_rng(seed)
    values = np.empty(draws)
    for index in range(draws):
        take = rng.integers(0, len(first), len(first))
        values[index] = first[take].mean() - second[take].mean()
    return {"mean": float(values.mean()), "lower_95": float(np.quantile(values, 0.025)), "upper_95": float(np.quantile(values, 0.975))}


class TorchLinearProbe:
    """Deterministic GPU-capable linear probe used for downstream representation tests."""

    def __init__(self, *, seed: int = 0, epochs: int = 250, lr: float = 0.03, weight_decay: float = 1e-3, device: str = "cuda"):
        self.seed = seed
        self.epochs = epochs
        self.lr = lr
        self.weight_decay = weight_decay
        self.device = torch.device(device if device != "cuda" or torch.cuda.is_available() else "cpu")
        self.model = None
        self.mean = None
        self.std = None

    def fit(self, features: np.ndarray, labels: np.ndarray, validation: tuple[np.ndarray, np.ndarray]) -> dict:
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        features = np.asarray(features, dtype=np.float32)
        labels = np.asarray(labels, dtype=np.int64)
        self.mean = features.mean(axis=0, keepdims=True)
        self.std = features.std(axis=0, keepdims=True)
        self.std[self.std == 0] = 1.0
        x_train = torch.tensor((features - self.mean) / self.std, device=self.device)
        y_train = torch.tensor(labels, device=self.device)
        x_val, y_val = validation
        x_val = torch.tensor((np.asarray(x_val, dtype=np.float32) - self.mean) / self.std, device=self.device)
        y_val = torch.tensor(np.asarray(y_val, dtype=np.int64), device=self.device)
        classes = int(labels.max()) + 1
        self.model = torch.nn.Linear(features.shape[1], classes, device=self.device)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        best = -np.inf
        best_state = None
        history = []
        for epoch in range(self.epochs):
            self.model.train()
            optimizer.zero_grad(set_to_none=True)
            loss = torch.nn.functional.cross_entropy(self.model(x_train), y_train)
            loss.backward()
            optimizer.step()
            self.model.eval()
            with torch.no_grad():
                score = float((self.model(x_val).argmax(1) == y_val).float().mean().cpu())
            history.append(score)
            if score > best:
                best = score
                best_state = {key: value.detach().clone() for key, value in self.model.state_dict().items()}
        self.model.load_state_dict(best_state)
        return {"best_validation_accuracy": best, "epochs": self.epochs, "device": str(self.device), "history": history}

    def predict(self, features: np.ndarray) -> np.ndarray:
        features = np.asarray(features, dtype=np.float32)
        normalized = torch.tensor((features - self.mean) / self.std, device=self.device)
        self.model.eval()
        with torch.no_grad():
            return self.model(normalized).argmax(1).cpu().numpy()
