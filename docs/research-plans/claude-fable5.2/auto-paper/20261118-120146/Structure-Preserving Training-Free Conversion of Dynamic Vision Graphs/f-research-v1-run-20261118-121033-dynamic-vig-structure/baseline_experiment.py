import json, sys, time
from pathlib import Path

import torch

run = Path(__file__).resolve().parent
sys.path.insert(0, str(run / "src"))
from structure_conversion import (
    grapher_forward,
    knn_indices,
    load_images,
    patch_nodes,
    signed_max_aggregate,
    signed_multilevel_encode,
)


def set_seed(seed):
    torch.manual_seed(seed)


def neighbor_jaccard(left, right):
    left_sets = [set(row.tolist()) for row in left]
    right_sets = [set(row.tolist()) for row in right]
    values = []
    for a, b in zip(left_sets, right_sets):
        union = a | b
        values.append(len(a & b) / len(union) if union else 1.0)
    return sum(values) / len(values)


def build_teacher(nodes, seed):
    set_seed(seed)
    features = torch.nn.functional.normalize(nodes, dim=-1)
    scale = 1.0 + 0.25 * torch.linspace(-1.0, 1.0, features.size(1)).view(1, -1, 1)
    noise = 0.05 * torch.randn_like(features)
    return features * scale + noise


def uniform_encode(values, levels):
    scale = float(levels - 1)
    quantized = torch.round(((values.clamp(-1, 1) + 1) / 2) * scale) / scale
    return 2 * quantized - 1


def evaluate_baselines(images, levels, sample_limit):
    nodes, positions = patch_nodes(images[:sample_limit])
    rows = []
    for seed in (41, 42, 43):
        teacher = build_teacher(nodes, seed)
        teacher_indices = []
        teacher_winners = []
        for sample in teacher:
            idx = knn_indices(sample, positions, k=9)
            _, winner = signed_max_aggregate(sample, idx)
            teacher_indices.append(idx)
            teacher_winners.append(winner)
        teacher_indices = torch.stack(teacher_indices)
        teacher_winners = torch.stack(teacher_winners)

        for method in ("unsigned_uniform", "signed_uniform", "signed_multilevel"):
            jaccards = []
            agreements = []
            events_total = 0
            for sample, t_idx, t_win in zip(teacher, teacher_indices, teacher_winners):
                if method == "unsigned_uniform":
                    encoded = uniform_encode(sample.abs(), levels)
                elif method == "signed_uniform":
                    encoded = uniform_encode(sample, levels)
                else:
                    encoded, events, _ = signed_multilevel_encode(sample, levels=levels)
                    events_total += events
                enc_idx, enc_win, _ = grapher_forward(sample, positions, encoded, k=9)
                jaccards.append(neighbor_jaccard(t_idx, enc_idx))
                agreements.append(float((t_win == enc_win).float().mean()))
            rows.append({
                "seed": seed,
                "method": method,
                "neighbor_jaccard": sum(jaccards) / len(jaccards),
                "winner_agreement": sum(agreements) / len(agreements),
                "events": events_total if events_total else None,
                "levels": levels,
                "samples": len(jaccards),
            })
    return rows


def main():
    images, labels = load_images(run / "data/fashion_mnist_train.parquet", limit=240)
    started = time.time()
    rows = evaluate_baselines(images, levels=16, sample_limit=240)
    report = {
        "stage": "P3",
        "role": "baseline-first exact structure metric on the unexposed calibration subset",
        "dataset": "Fashion-MNIST train subset",
        "seed_policy": "teacher seeds 41/42/43; no test exposure",
        "wall_seconds": time.time() - started,
        "rows": rows,
    }
    out = run / "baseline-structure-results.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row))


if __name__ == "__main__":
    main()
