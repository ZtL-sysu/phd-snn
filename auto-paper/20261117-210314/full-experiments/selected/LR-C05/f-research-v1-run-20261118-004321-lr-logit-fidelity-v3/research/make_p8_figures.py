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
    "Output-Jacobian": "#0F4D92",
    "Top-|m|": "#7884B4",
    "A2Q-style": "#B4C0E4",
    "One-Spike-style": "#E4CCD8",
    "Cora": "#0F4D92",
    "Chameleon": "#42949E",
    "Squirrel": "#9A4D8E",
    "gain": "#2E9E44",
    "loss": "#B64342",
    "neutral": "#767676",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_figure(fig: plt.Figure, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0])
    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    confirmation = json.loads((RUN_ROOT / "results" / "confirmation-test-v2.json").read_text(encoding="utf-8"))
    summary = json.loads((RUN_ROOT / "results" / "confirmation-summary.json").read_text(encoding="utf-8"))
    budget_summary = json.loads((RUN_ROOT / "inputs" / "v2-summary.json").read_text(encoding="utf-8"))
    timing = json.loads((RUN_ROOT / "inputs" / "v2-timing.json").read_text(encoding="utf-8"))

    mode_to_label = {
        "downstream_jacobian": "Output-Jacobian",
        "top_abs": "Top-|m|",
        "a2q_node_budget": "A2Q-style",
        "one_spike": "One-Spike-style",
    }
    datasets = ["cora", "chameleon", "squirrel"]
    dataset_labels = ["Cora", "Chameleon", "Squirrel"]
    methods = list(mode_to_label.values())
    rows = confirmation["rows"]

    main_rows: list[dict[str, object]] = []
    main_values: dict[str, list[float]] = {method: [] for method in methods}
    main_errors: dict[str, list[float]] = {method: [] for method in methods}
    for dataset in datasets:
        for mode, label in mode_to_label.items():
            values = np.array(
                [row["logit_mse"] for row in rows if row["dataset"] == dataset and row["residual_mode"] == mode],
                dtype=float,
            )
            mean = float(values.mean())
            std = float(values.std(ddof=1))
            main_values[label].append(mean)
            main_errors[label].append(std)
            main_rows.append(
                {
                    "dataset": dataset,
                    "method": label,
                    "n_seeds": len(values),
                    "mean_logit_mse": mean,
                    "sample_sd_logit_mse": std,
                    "rank": 128,
                    "budget": 0.02,
                    "split": "test",
                }
            )
    write_csv(DATA_DIR / "figure2-main-logit-mse.csv", main_rows)

    x = np.arange(len(datasets))
    width = 0.19
    fig, ax = plt.subplots(figsize=(7.2, 3.25))
    for index, method in enumerate(methods):
        offset = (index - 1.5) * width
        ax.bar(
            x + offset,
            np.array(main_values[method]) * 100,
            width=width,
            yerr=np.array(main_errors[method]) * 100,
            color=COLORS[method],
            edgecolor="black",
            linewidth=0.6,
            capsize=2,
            label=method,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(dataset_labels)
    ax.set_ylabel(r"Logit MSE ($\times 10^{-2}$)")
    ax.set_xlabel("Static graph")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.18), columnspacing=1.1)
    ax.text(0.99, 0.96, "lower is better", transform=ax.transAxes, ha="right", va="top", fontsize=6.5, color=COLORS["neutral"])
    fig.tight_layout()
    save_figure(fig, PLOT_DIR / "figure2-main-logit-mse")

    budget_rows: list[dict[str, object]] = []
    budget_values: dict[str, list[float]] = {label: [] for label in dataset_labels}
    budgets = [0.005, 0.01, 0.02]
    for dataset, label in zip(datasets, dataset_labels):
        for budget in budgets:
            reduction = float(budget_summary["datasets"][dataset][str(budget)]["logit_mse"]["relative_reduction"])
            budget_values[label].append(reduction * 100)
            budget_rows.append(
                {
                    "dataset": dataset,
                    "budget": budget,
                    "logit_mse_reduction_percent": reduction * 100,
                    "n_seeds": 3,
                    "evidence_scope": "validation-grid sensitivity",
                }
            )
    write_csv(DATA_DIR / "figure3-budget-sensitivity.csv", budget_rows)

    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    for label in dataset_labels:
        ax.plot(
            np.array(budgets) * 100,
            budget_values[label],
            marker="o",
            markersize=4,
            linewidth=1.6,
            color=COLORS[label],
            label=label,
        )
    ax.axhline(0, color=COLORS["neutral"], linewidth=0.8, linestyle="--")
    ax.set_xlabel("Sparse residual budget (%)")
    ax.set_ylabel("Logit-MSE reduction (%)")
    ax.set_xticks([0.5, 1.0, 2.0])
    ax.legend(ncol=3, loc="upper left")
    ax.text(0.99, 0.13, "validation grid", transform=ax.transAxes, ha="right", va="bottom", fontsize=6.5, color=COLORS["neutral"])
    fig.tight_layout()
    save_figure(fig, PLOT_DIR / "figure3-budget-sensitivity")

    tradeoff_rows: list[dict[str, object]] = []
    reductions = []
    task_losses = []
    for dataset, label in zip(datasets, dataset_labels):
        reduction = float(summary["datasets"][dataset]["logit_mse_reduction"]) * 100
        loss = float(summary["datasets"][dataset]["worst_task_loss_pp"])
        reductions.append(reduction)
        task_losses.append(loss)
        tradeoff_rows.append(
            {
                "dataset": dataset,
                "logit_mse_reduction_percent": reduction,
                "worst_three_seed_mean_task_loss_pp": loss,
                "split": "official_test",
            }
        )

    ratio_rows: list[dict[str, object]] = []
    ratios = []
    for dataset, label in zip(datasets, dataset_labels):
        for seed in (0, 1, 2):
            method_row = next(row for row in timing["rows"] if row["dataset"] == dataset and row["seed"] == seed and row["method"] == "downstream_jacobian")
            baseline_row = next(row for row in timing["rows"] if row["dataset"] == dataset and row["seed"] == seed and row["method"] == "svd_only")
            ratio = float(method_row["p95_elapsed_sec"]) / float(baseline_row["p95_elapsed_sec"])
            ratios.append(ratio)
            ratio_rows.append(
                {
                    "dataset": dataset,
                    "seed": seed,
                    "proposed_p95_sec": method_row["p95_elapsed_sec"],
                    "svd_only_p95_sec": baseline_row["p95_elapsed_sec"],
                    "paired_p95_ratio": ratio,
                    "rank": 128,
                    "budget": 0.01,
                    "warmups": 3,
                    "timed_repeats": 7,
                }
            )
    write_csv(DATA_DIR / "figure4-tradeoff-and-runtime.csv", tradeoff_rows + ratio_rows)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.45), gridspec_kw={"width_ratios": [1.12, 1.0]})
    ax = axes[0]
    scatter_handles = []
    for label, reduction, loss in zip(dataset_labels, reductions, task_losses):
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
    colors = [COLORS[label] for label in dataset_labels for _ in range(3)]
    ax.scatter(ratios, positions, c=colors, s=32, edgecolor="black", linewidth=0.4)
    ax.axvline(1.0, color=COLORS["neutral"], linestyle="--", linewidth=0.9)
    ax.set_yticks(positions)
    ax.set_yticklabels(
        [f"{abbr}-{seed}" for abbr in ("C", "Ch", "S") for seed in (0, 1, 2)],
        fontsize=6,
    )
    ax.set_xlabel("Paired p95 runtime ratio")
    ax.set_xticks([1.00, 1.05, 1.10, 1.15])
    ax.set_xticklabels(["1.00", "1.05", "1.10", "1.15"])
    ax.set_xlim(0.98, 1.15)
    ax.invert_yaxis()
    ax.text(-0.22, 1.02, "b", transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")
    fig.legend(
        handles=scatter_handles,
        labels=dataset_labels,
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
        json.dumps({"schema_version": 1, "backend": "Python/matplotlib", "artifacts": artifacts}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "passed", "artifacts": len(artifacts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
