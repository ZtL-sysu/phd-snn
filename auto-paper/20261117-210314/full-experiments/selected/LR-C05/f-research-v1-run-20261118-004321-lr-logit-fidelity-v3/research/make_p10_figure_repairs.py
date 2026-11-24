from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


RUN_ROOT = Path(__file__).resolve().parents[1]
FIGURES = RUN_ROOT / "figures"
DATA_DIR = FIGURES / "source-data"
PLOT_DIR = FIGURES / "data"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["legend.frameon"] = False

COLORS = {
    "Cora": "#0F4D92",
    "Chameleon": "#42949E",
    "Squirrel": "#9A4D8E",
    "loss": "#B64342",
    "neutral": "#767676",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig: plt.Figure, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    task_rows = read_csv(RUN_ROOT / "results" / "p10-task-loss-three-seed-audit.csv")
    timing_rows = read_csv(RUN_ROOT / "results" / "p10-timing-summary.csv")
    datasets = ["cora", "chameleon", "squirrel"]
    labels = ["Cora", "Chameleon", "Squirrel"]

    task_losses = []
    reductions = [26.23240871, 33.98668714, 25.82841138]
    combined_rows: list[dict[str, object]] = []
    for dataset, label, reduction in zip(datasets, labels, reductions):
        loss = max(
            float(row["three_seed_mean_observed_degradation_pp"])
            for row in task_rows
            if row["dataset"] == dataset
        )
        task_losses.append(loss)
        combined_rows.append(
            {
                "dataset": dataset,
                "logit_mse_reduction_percent": reduction,
                "worst_three_seed_mean_task_loss_pp": loss,
                "split": "official_test",
                "task_comparator": "best matched-budget non-proposed control per dataset/metric, then maximum across four task metrics",
            }
        )

    ratios = [float(row["ratio_of_method_p95_to_svd_only_p95"]) for row in timing_rows]
    for row in timing_rows:
        combined_rows.append(
            {
                "dataset": row["dataset"],
                "seed": int(row["seed"]),
                "proposed_p95_sec": float(row["method_p95_sec"]),
                "svd_only_p95_sec": float(row["svd_only_p95_sec"]),
                "paired_p95_ratio": float(row["ratio_of_method_p95_to_svd_only_p95"]),
                "rank": 128,
                "budget": 0.01,
                "warmups": 3,
                "timed_repeats": 7,
            }
        )
    write_csv(DATA_DIR / "figure4-tradeoff-and-runtime.csv", combined_rows)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.45), gridspec_kw={"width_ratios": [1.12, 1.0]})
    ax = axes[0]
    scatter_handles = []
    for label, reduction, loss in zip(labels, reductions, task_losses):
        scatter_handles.append(
            ax.scatter(reduction, loss, s=45, color=COLORS[label], edgecolor="black", linewidth=0.5, label=label)
        )
    ax.axhline(3.0, color=COLORS["loss"], linestyle="--", linewidth=0.9)
    ax.text(
        0.98,
        0.92,
        "3 pp reference",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=6,
        color=COLORS["loss"],
    )
    ax.set_xlabel("Logit-MSE reduction (%)")
    ax.set_ylabel("Worst task loss (pp)")
    ax.set_xticks([25, 30, 35])
    ax.set_xlim(24, 36)
    ax.set_ylim(0, 3.35)
    ax.text(-0.12, 1.02, "a", transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")

    ax = axes[1]
    positions = np.arange(len(ratios))
    colors = [COLORS[label] for label in labels for _ in range(3)]
    ax.scatter(ratios, positions, c=colors, s=32, edgecolor="black", linewidth=0.4)
    ax.axvline(1.0, color=COLORS["neutral"], linestyle="--", linewidth=0.9)
    ax.set_yticks(positions)
    ax.set_yticklabels([f"{abbr}-{seed}" for abbr in ("C", "Ch", "S") for seed in (0, 1, 2)], fontsize=6)
    ax.set_xlabel("Paired p95 runtime ratio")
    ax.set_xticks([1.00, 1.05, 1.10, 1.15])
    ax.set_xticklabels(["1.00", "1.05", "1.10", "1.15"])
    ax.set_xlim(0.98, 1.15)
    ax.invert_yaxis()
    ax.text(-0.22, 1.02, "b", transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")
    fig.legend(
        handles=scatter_handles,
        labels=labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.99),
        ncol=3,
        columnspacing=1.5,
    )
    fig.subplots_adjust(left=0.14, right=0.98, bottom=0.18, top=0.82, wspace=0.58)
    save_figure(fig, PLOT_DIR / "figure4-tradeoff-and-runtime")

    artifacts = []
    for path in sorted(DATA_DIR.glob("*")) + sorted(PLOT_DIR.glob("*")):
        artifacts.append({"path": str(path.relative_to(RUN_ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size})
    (FIGURES / "data-figure-manifest.json").write_text(
        json.dumps({"schema_version": 2, "backend": "Python/matplotlib", "repair": "P10 task-loss comparator/aggregation correction", "artifacts": artifacts}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "passed", "task_losses": dict(zip(labels, task_losses)), "artifacts": len(artifacts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
