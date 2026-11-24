import io
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import torch
from PIL import Image


def load_images(path, limit=None):
    table = pq.read_table(path)
    if limit is not None:
        table = table.slice(0, limit)
    rows = table.to_pylist()
    images = []
    labels = []
    for row in rows:
        with Image.open(io.BytesIO(row["image"]["bytes"])) as image:
            array = np.asarray(image.convert("L"), dtype=np.float32) / 255.0
        images.append(torch.from_numpy(array))
        labels.append(int(row["label"]))
    return torch.stack(images), torch.tensor(labels, dtype=torch.long)


def patch_nodes(images, patch_size=4):
    batch, height, width = images.shape
    patches_y = height // patch_size
    patches_x = width // patch_size
    nodes = images.unfold(1, patch_size, patch_size).unfold(2, patch_size, patch_size)
    nodes = nodes.contiguous().view(batch, patches_y * patches_x, patch_size * patch_size)
    positions = torch.stack(
        torch.meshgrid(torch.arange(patches_y), torch.arange(patches_x), indexing="ij"), dim=-1
    ).reshape(-1, 2).float()
    return nodes, positions


def knn_indices(features, positions, k=9):
    features = features / (features.norm(dim=-1, keepdim=True).clamp_min(1e-6))
    distances = torch.cdist(features, features)
    distances = distances + 1e3 * (1.0 - torch.eye(features.size(0), device=features.device))
    distances = distances + 1e-3 * torch.cdist(positions, positions)
    return torch.topk(-distances, k=k, dim=-1).indices


def matrix_knn_indices(features, k=9):
    scores = torch.bmm(features, features.transpose(1, 2))
    rows = features.size(1)
    diagonal = torch.eye(rows, device=features.device, dtype=torch.bool).unsqueeze(0)
    return scores.masked_fill(diagonal, -1e4).topk(k, dim=-1).indices


def matrix_winners(features, indices):
    batch = features.size(0)
    row = torch.arange(batch, device=features.device).view(batch, 1, 1).expand(batch, features.size(1), indices.size(-1))
    neighbors = features[row, indices]
    return (neighbors - features.unsqueeze(2)).argmax(dim=2)


def signed_max_aggregate(features, indices):
    neighbors = features[indices]
    center = features.unsqueeze(1)
    messages = neighbors - center
    winners = messages.argmax(dim=1)
    aggregated = torch.gather(messages, 1, winners.unsqueeze(-1)).squeeze(1)
    return aggregated, winners


def signed_multilevel_encode(values, levels=16, threshold_scale=0.75):
    if values.numel() == 0:
        return values.clone(), 0, torch.ones((), device=values.device, dtype=values.dtype)
    unit = values.abs().max() / float(levels)
    unit = unit.clamp_min(1e-6)
    exponents = torch.arange(levels, device=values.device, dtype=values.dtype)
    step_sizes = unit / (2.0 ** exponents)
    thresholds = (step_sizes * threshold_scale).view(1, -1, *([1] * (values.dim() - 1)))
    crossing = (values.abs().unsqueeze(1) + 1e-7) >= thresholds
    previous = torch.cat([torch.zeros_like(crossing[:, :1]), crossing[:, :-1]], dim=1)
    active = crossing & ~previous
    codes = (step_sizes.view(1, -1, *([1] * (values.dim() - 1))) * active).sum(dim=1) * values.sign()
    event_count = int(active.sum().item())
    return codes, event_count, unit


def grapher_forward(features, positions, encoded_features, k=9, teacher_indices=None, teacher_winners=None):
    if teacher_indices is None:
        indices = knn_indices(encoded_features, positions, k=k)
    else:
        indices = teacher_indices
    aggregated, winners = signed_max_aggregate(encoded_features, indices)
    if teacher_winners is not None:
        neighbors = encoded_features[indices]
        center = encoded_features.unsqueeze(1)
        messages = neighbors - center
        aggregated = torch.gather(messages, 1, teacher_winners.unsqueeze(-1)).squeeze(1)
        winners = teacher_winners
    return indices, winners, aggregated


