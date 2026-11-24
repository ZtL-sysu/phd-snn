from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
DATA = FIGURES / "data"
SOURCE = FIGURES / "source-data"
for directory in (DATA, SOURCE):
    directory.mkdir(parents=True, exist_ok=True)


def save(fig, name: str) -> None:
    for suffix in ("png", "pdf", "svg"):
        fig.savefig(DATA / f"{name}.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, color):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", linewidth=1.5, edgecolor=color, facecolor=color + "18")
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=13, linewidth=1.3, color="#334155"))


def figure1():
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.1, 4.65, "Ordered multi-hop representation", fontsize=12, fontweight="bold")
    top = [
        (0.2, 3.5, 1.4, 0.8, "X", "#2563eb"),
        (2.0, 3.5, 1.5, 0.8, "A X", "#0891b2"),
        (3.9, 3.5, 1.7, 0.8, "A^2 X", "#0f766e"),
        (6.0, 3.5, 1.7, 0.8, "A^3 X", "#7c3aed"),
        (8.2, 3.5, 2.3, 0.8, "ordered H blocks", "#475569"),
    ]
    for item in top:
        box(ax, *item)
    for i in range(len(top) - 1):
        arrow(ax, top[i][0] + top[i][2], 3.9, top[i + 1][0], 3.9)
    ax.text(0.1, 2.65, "Hybrid serialization", fontsize=12, fontweight="bold")
    bottom = [
        (0.2, 1.4, 1.8, 0.8, "8 Lloyd centroids", "#2563eb"),
        (2.4, 1.4, 1.5, 0.8, "escape marker", "#be123c"),
        (4.3, 1.4, 1.8, 0.8, "4-bit symbol", "#7c3aed"),
        (6.5, 1.4, 1.8, 0.8, "32-bit payload", "#ea580c"),
        (8.7, 1.4, 1.8, 0.8, "256-bit codebook / N", "#166534"),
    ]
    for item in bottom:
        box(ax, *item)
    for i in range(len(bottom) - 1):
        arrow(ax, bottom[i][0] + bottom[i][2], 1.8, bottom[i + 1][0], 1.8)
    ax.text(5.5, 0.55, "b_avg = 4 + 32 f_escape + 256/N", ha="center", fontsize=11, color="#334155")
    save(fig, "figure1-hop-coding")


def load_rows():
    representation = json.loads((ROOT / "results/pos-representation.json").read_text(encoding="utf-8"))
    tasks = json.loads((ROOT / "results/pos-dispersion-summary.json").read_text(encoding="utf-8"))
    return representation, tasks


def figure2(representation, tasks):
    rep_rows = representation["rows"]
    methods = ["raw", "uniform", "lloyd", "hybrid"]
    datasets = ["chameleon", "squirrel"]
    x = np.arange(len(methods))
    width = 0.36
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.1))
    colors = ["#64748b", "#2563eb", "#7c3aed", "#f97316"]
    for idx, dataset in enumerate(datasets):
        errors = [next(row["relative_error"] for row in rep_rows if row["dataset"] == dataset and row["method"] == method) * 100 for method in methods]
        axes[0].bar(x + (idx - 0.5) * width, errors, width, label=dataset, color=colors[idx], alpha=0.85)
    axes[0].set_xticks(x, methods, rotation=20)
    axes[0].set_ylabel("Representation error (%)")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False)

    for idx, dataset in enumerate(datasets):
        storage = [next(row["storage_reduction"] for row in rep_rows if row["dataset"] == dataset and row["method"] == method) for method in methods]
        axes[1].bar(x + (idx - 0.5) * width, storage, width, color=colors[idx], alpha=0.85)
    axes[1].axhline(4, color="#be123c", linestyle="--", linewidth=1.1)
    axes[1].set_xticks(x, methods, rotation=20)
    axes[1].set_ylabel("Storage reduction (×)")
    axes[1].grid(axis="y", alpha=0.25)

    for idx, dataset in enumerate(datasets):
        means = [tasks["datasets"][dataset]["retrained_" + method]["mean"] * 100 for method in methods]
        sds = [tasks["datasets"][dataset]["retrained_" + method]["sample_sd"] * 100 for method in methods]
        axes[2].errorbar(x + (idx - 0.5) * width, means, yerr=sds, fmt="o", capsize=4, color=colors[idx], label=dataset)
    axes[2].set_xticks(x, methods, rotation=20)
    axes[2].set_ylabel("Retrained balanced accuracy (%)")
    axes[2].grid(axis="y", alpha=0.25)
    axes[2].legend(frameon=False)
    fig.tight_layout()
    save(fig, "figure2-method-tradeoff")


def figure3(representation, tasks):
    perm = representation["controls"]["permutation"]
    shuffle = representation["controls"]["shuffle"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].scatter([row["permutation_seed"] for row in perm], [row["raw_max_error"] for row in perm], label="raw", color="#2563eb")
    axes[0].scatter([row["permutation_seed"] for row in perm], [row["hybrid_max_error"] for row in perm], label="hybrid", color="#f97316")
    axes[0].axhline(1e-10, color="#be123c", linestyle="--", linewidth=1.1)
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Node-permutation seed")
    axes[0].set_ylabel("Inverse-permutation max error")
    axes[0].legend(frameon=False)
    axes[0].grid(axis="y", alpha=0.25)

    datasets = ["chameleon", "squirrel"]
    values = [[row["error_ratio"] for row in shuffle if row["dataset"] == dataset] for dataset in datasets]
    axes[1].boxplot(values, tick_labels=datasets, patch_artist=True, widths=0.55)
    axes[1].axhline(1.25, color="#be123c", linestyle="--", linewidth=1.1)
    axes[1].set_ylabel("Ordered-codebook shuffled/ordered error")
    axes[1].grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save(fig, "figure3-order-controls")


def source_tables(representation, tasks):
    with (SOURCE / "figure2-method-tradeoff.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["dataset", "method", "relative_error", "storage_reduction", "balanced_accuracy_mean", "balanced_accuracy_sd"])
        for row in representation["rows"]:
            task = tasks["datasets"][row["dataset"]]["retrained_" + row["method"]]
            writer.writerow([row["dataset"], row["method"], row["relative_error"], row["storage_reduction"], task["mean"], task["sample_sd"]])
    with (SOURCE / "figure3-order-controls.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["dataset", "control", "seed", "value"])
        for row in representation["controls"]["permutation"]:
            writer.writerow([row["dataset"], "raw_permutation_error", row["permutation_seed"], row["raw_max_error"]])
            writer.writerow([row["dataset"], "hybrid_permutation_error", row["permutation_seed"], row["hybrid_max_error"]])
        for row in representation["controls"]["shuffle"]:
            writer.writerow([row["dataset"], "shuffle_error_ratio", row["shuffle_seed"], row["error_ratio"]])


def main():
    representation, tasks = load_rows()
    figure1()
    figure2(representation, tasks)
    figure3(representation, tasks)
    source_tables(representation, tasks)
    print(json.dumps({"figures": 3, "source_tables": 2}, indent=2))


if __name__ == "__main__":
    main()
