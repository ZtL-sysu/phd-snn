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
FIGURES.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)


def save_figure(fig, stem: str) -> None:
    for suffix in ("png", "pdf", "svg"):
        fig.savefig(DATA / f"{stem}.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_box(ax, x, y, width, height, text, color):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.5,
        edgecolor=color,
        facecolor=color + "18",
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=10)


def draw_arrow(ax, x0, y0, x1, y1, color="#334155"):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.4,
            color=color,
        )
    )


def figure1() -> None:
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.15, 4.65, "Actual frozen computation", fontsize=12, fontweight="bold")
    boxes = [
        (0.2, 3.55, 1.65, 0.75, r"$M=XW_0$", "#2563eb"),
        (2.25, 3.55, 1.85, 0.75, r"$\widehat M=Q_{row}(M)$", "#7c3aed"),
        (4.55, 3.55, 1.85, 0.75, r"$H=\mathrm{relu}(AM+b_0)$", "#0891b2"),
        (6.85, 3.55, 1.75, 0.75, r"$Z=AHW_1+b$", "#0f766e"),
        (9.05, 3.55, 1.55, 0.75, r"$|Z-\widehat Z|$", "#be123c"),
    ]
    for x, y, w, h, text, color in boxes:
        draw_box(ax, x, y, w, h, text, color)
    for i in range(len(boxes) - 1):
        draw_arrow(ax, boxes[i][0] + boxes[i][2], 3.925, boxes[i + 1][0], 3.925)

    ax.text(0.15, 2.65, "Deterministic radius and certificate", fontsize=12, fontweight="bold")
    bound_boxes = [
        (0.2, 1.45, 1.65, 0.75, r"$\Delta_{ih}=s_i/2$", "#7c3aed"),
        (2.25, 1.45, 1.85, 0.75, r"$|A|\Delta$", "#0891b2"),
        (4.55, 1.45, 1.85, 0.75, r"$|A||A|\Delta$", "#0f766e"),
        (6.85, 1.45, 1.75, 0.75, r"$B_{abs}=|A||A|\Delta|W_1|$", "#166534"),
        (9.05, 1.45, 1.55, 0.75, r"$|Z-\widehat Z|\leq B_{abs}$", "#166534"),
    ]
    for x, y, w, h, text, color in bound_boxes:
        draw_box(ax, x, y, w, h, text, color)
    for i in range(len(bound_boxes) - 1):
        draw_arrow(ax, bound_boxes[i][0] + bound_boxes[i][2], 1.825, bound_boxes[i + 1][0], 1.825)

    ax.text(
        5.5,
        0.55,
        "Radius is fixed from the rowwise quantizer before actual errors are inspected.",
        ha="center",
        fontsize=10,
        color="#475569",
    )
    save_figure(fig, "figure1-certificate-chain")


def load_rows() -> list[dict]:
    payload = json.loads((ROOT / "results/cert-methods.json").read_text(encoding="utf-8"))
    rows = payload["rows"]
    return sorted(rows, key=lambda row: (row["quantizer"], row["dataset"], row["seed"], row["levels"]))


def figure2(rows: list[dict]) -> None:
    x = np.arange(len(rows))
    colors = ["#2563eb" if row["quantizer"] == "global" else "#f97316" for row in rows]
    width = np.array([row["proposed_width_over_rms"] for row in rows])
    tightening = np.array([100 * row["tightening"] for row in rows])

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].scatter(x, width, c=colors, s=30, alpha=0.9)
    axes[0].axhline(np.median(width), color="#334155", linestyle="--", linewidth=1.2, label="overall median")
    axes[0].set_ylabel("Bound width / realized RMS")
    axes[0].set_yscale("log")
    axes[0].legend(frameon=False)
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].scatter(x, tightening, c=colors, s=30, alpha=0.9)
    axes[1].axhline(25, color="#be123c", linestyle="--", linewidth=1.2, label="25% strong gate")
    axes[1].axhline(0, color="#64748b", linewidth=0.8)
    axes[1].set_ylabel("Tightening vs global-radius (%)\n")
    axes[1].set_xlabel("Cells ordered by quantizer, graph, seed and level")
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", alpha=0.25)

    handles = [
        plt.Line2D([], [], marker="o", linestyle="", color="#2563eb", label="global uniform"),
        plt.Line2D([], [], marker="o", linestyle="", color="#f97316", label="rowwise uniform"),
    ]
    axes[0].legend(handles=handles, frameon=False, loc="lower left")
    save_figure(fig, "figure2-width-tightening")


def figure3(rows: list[dict]) -> None:
    global_rows = [row for row in rows if row["quantizer"] == "global"]
    rowwise_rows = [row for row in rows if row["quantizer"] == "rowwise"]
    equality_gap = np.array(
        [abs(row["proposed_width_over_rms"] - row["global_width_over_rms"]) for row in global_rows]
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    axes[0].hist(equality_gap, bins=10, color="#2563eb", alpha=0.8)
    axes[0].set_xlabel("Absolute width/RMS gap")
    axes[0].set_ylabel("Global-uniform cells")
    axes[0].set_title("Equality control")
    axes[0].grid(axis="y", alpha=0.25)

    datasets = ("cora", "chameleon", "squirrel")
    values = [
        [100 * row["tightening"] for row in rowwise_rows if row["dataset"] == dataset]
        for dataset in datasets
    ]
    axes[1].boxplot(values, tick_labels=datasets, patch_artist=True, widths=0.55)
    for patch, color in zip(axes[1].patches, ("#fb923c", "#f97316", "#ea580c")):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
    axes[1].axhline(25, color="#be123c", linestyle="--", linewidth=1.2)
    axes[1].set_ylabel("Rowwise tightening (%)\n")
    axes[1].set_title("Rowwise radius-granularity effect")
    axes[1].grid(axis="y", alpha=0.25)
    save_figure(fig, "figure3-equality-tightening")


def source_csv(rows: list[dict]) -> None:
    fields = [
        "dataset",
        "seed",
        "levels",
        "quantizer",
        "tightening",
        "proposed_width_over_rms",
        "minkowski_width_over_rms",
        "global_width_over_rms",
        "scalar_width_over_rms",
        "radius_sha256",
    ]
    path = FIGURES / "source-data/figure3-rowwise-tightening.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def main() -> None:
    rows = load_rows()
    figure1()
    figure2(rows)
    figure3(rows)
    source_csv(rows)
    print(json.dumps({"figures": 3, "rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
