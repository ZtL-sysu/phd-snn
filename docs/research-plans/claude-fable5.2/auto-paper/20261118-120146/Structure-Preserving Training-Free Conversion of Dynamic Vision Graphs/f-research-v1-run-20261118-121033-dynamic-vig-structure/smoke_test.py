import json, sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from structure_conversion import (
    grapher_forward,
    knn_indices,
    load_images,
    patch_nodes,
    signed_max_aggregate,
    signed_multilevel_encode,
)

run = Path(__file__).resolve().parent
images, labels = load_images(run / "data/fashion_mnist_train.parquet", limit=64)
nodes, positions = patch_nodes(images)
teacher_nodes = torch.nn.functional.normalize(nodes[0], dim=-1)
teacher_nodes = teacher_nodes * (1.0 + 0.25 * torch.linspace(-1.0, 1.0, teacher_nodes.size(0)).view(-1, 1))

indices = knn_indices(teacher_nodes, positions, k=9)
assert indices.shape == (49, 9)
teacher_messages, teacher_winners = signed_max_aggregate(teacher_nodes, indices)
assert torch.isfinite(teacher_messages).all() and teacher_winners.shape == (49, 16)

encoded, events, unit = signed_multilevel_encode(teacher_nodes, levels=16)
assert encoded.shape == teacher_nodes.shape
assert torch.isfinite(encoded).all() and events >= 0 and unit > 0
encoded_indices, encoded_winners, encoded_messages = grapher_forward(teacher_nodes, positions, encoded, k=9)
assert encoded_indices.shape == indices.shape

oracle_indices, oracle_winners, oracle_messages = grapher_forward(
    teacher_nodes,
    positions,
    teacher_nodes,
    k=9,
    teacher_indices=indices,
    teacher_winners=teacher_winners,
)
assert torch.equal(oracle_indices, indices)
assert torch.equal(oracle_winners, teacher_winners)
assert torch.allclose(oracle_messages, teacher_messages, atol=1e-6)

report = {
    "status": "pass",
    "samples": int(images.size(0)),
    "nodes_per_sample": int(nodes.size(1)),
    "neighbor_shape": list(indices.shape),
    "finite_teacher_messages": bool(torch.isfinite(teacher_messages).all()),
    "finite_encoded": bool(torch.isfinite(encoded).all()),
    "encoded_events_first_sample": events,
    "neighbor_jaccard_first_sample": float(
        len(set(map(tuple, indices.tolist())) & set(map(tuple, encoded_indices.tolist())))
        / len(set(map(tuple, indices.tolist())) | set(map(tuple, encoded_indices.tolist())))
    ),
    "winner_agreement_first_sample": float((encoded_winners == teacher_winners).float().mean()),
    "oracle_exact": True,
}
(run / "smoke-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))



