#!/usr/bin/env python3
"""G0 foundation gate: reproduce the frozen Cora/PubMed T=8 numbers in THIS run.

This is not a claim of a new result. It proves that the copied core kernel, the copied
Planetoid files and this Conda environment form the same numerical pipeline as the frozen
task-book numbers, before any new experiment is allowed to start.

Acceptance: |reproduced - frozen| <= 0.10 pp for ANN and for converted T=8 on both graphs.
Every row is written to registry/results.csv and to runs/<id>/ with content-addressed hashes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
sys.path.insert(0, str(ROOT / "protocols"))

import core  # noqa: E402

FROZEN = {
    "cora": {"ann": 0.8060, "conv8": 0.8026},
    "pubmed": {"ann": 0.7757, "conv8": 0.7740},
}
TOL_PP = 0.10
SEEDS = list(range(7))
T = 8
HIDDEN = 16
DEVICE = "cpu"
EXTERNAL_COMMIT = "d12511207b1f0f1ee49650ec560de5236942c419"

FIELDS = [
    "run_id", "date", "stage", "probe", "dataset", "host", "method_family", "method",
    "is_transplant", "neuron", "bias_correction", "t_steps", "hidden", "seed", "ann_ref",
    "acc", "std", "gap_pp", "spikes_per_node", "sop_est", "train_seconds",
    "retrain_count", "perm_seed", "git_commit", "notes", "device",
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def asset_hashes(dataset: str) -> dict:
    out = {
        "experiments/core.py": sha(ROOT / "experiments/core.py"),
        "protocols/graph_data.py": sha(ROOT / "protocols/graph_data.py"),
        "experiments/wp0_reproduce.py": sha(ROOT / "experiments/wp0_reproduce.py"),
    }
    for path in sorted((ROOT / "results" / ".data").glob("ind." + dataset + ".*")):
        out["results/.data/" + path.name] = sha(path)
    return out


def main() -> int:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = "wp0-repro-" + stamp
    run_dir = ROOT / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    def log(msg: str) -> None:
        print(msg, flush=True)
        lines.append(msg)

    log("G0 reproduction gate | " + datetime.now().isoformat(timespec="seconds"))
    log("device=" + DEVICE + " seeds=" + str(SEEDS) + " T=" + str(T) + " hidden=" + str(HIDDEN))
    log("python=" + platform.python_version() + " numpy=" + np.__version__)
    import scipy
    import torch
    log("scipy=" + scipy.__version__ + " torch=" + torch.__version__)

    summary: dict = {}
    rows: list[dict] = []
    trace_basis: dict = {}

    for dataset, ref in FROZEN.items():
        hashes = asset_hashes(dataset)
        trace_basis[dataset] = hashes
        trace_id = "content:" + hashlib.sha256(
            json.dumps(hashes, sort_keys=True).encode("utf-8")
        ).hexdigest()[:16]
        log("dataset=" + dataset + " trace_id=" + trace_id)

        data = core.load(dataset)
        anns, convs, spikes, seconds = [], [], [], []
        for seed in SEEDS:
            t0 = time.perf_counter()
            model = core.train_ann(
                data, hidden=HIDDEN, n_layers=2, seed=seed, device=DEVICE
            )
            result = core.convert(data, model, T=T)
            elapsed = time.perf_counter() - t0
            anns.append(float(model["acc_test"]))
            convs.append(float(result["acc"]))
            spikes.append(float(result["spikes"]))
            seconds.append(elapsed)
            log(
                "  seed %d: ANN %.4f  T8 %.4f  spikes %.0f  %.1fs"
                % (seed, model["acc_test"], result["acc"], result["spikes"], elapsed)
            )
            rows.append({
                "run_id": run_id + "-" + dataset + "-s" + str(seed),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "stage": "S0/G0", "probe": "none", "dataset": dataset, "host": "H1_mean",
                "method_family": "conversion", "method": "repro_check:conversion_ftbc",
                "is_transplant": 0, "neuron": "IF", "bias_correction": "beta_star",
                "t_steps": T, "hidden": HIDDEN, "seed": seed,
                "ann_ref": round(anns[-1], 6), "acc": round(convs[-1], 6), "std": "",
                "gap_pp": round((convs[-1] - anns[-1]) * 100, 4),
                "spikes_per_node": round(spikes[-1] / data["N"], 6),
                "sop_est": T * data["E"] * HIDDEN,
                "train_seconds": round(elapsed, 3), "retrain_count": 1,
                "perm_seed": "", "git_commit": trace_id,
                "notes": "G0 reproduction of frozen T=8 value " + str(ref["conv8"]),
                "device": DEVICE,
            })

        a, c = float(np.mean(anns)), float(np.mean(convs))
        d_ann, d_conv = (a - ref["ann"]) * 100, (c - ref["conv8"]) * 100
        ok = abs(d_ann) <= TOL_PP and abs(d_conv) <= TOL_PP
        summary[dataset] = {
            "ann_mean": a, "ann_frozen": ref["ann"], "d_ann_pp": d_ann,
            "conv8_mean": c, "conv8_frozen": ref["conv8"], "d_conv_pp": d_conv,
            "conv8_std": float(np.std(convs)), "ann_std": float(np.std(anns)),
            "spikes_mean": float(np.mean(spikes)),
            "train_seconds_mean": float(np.mean(seconds)),
            "pass": ok, "trace_id": trace_id,
        }
        log(
            "[%s] ANN %.4f vs %.4f (d %+.3f pp) | T8 %.4f vs %.4f (d %+.3f pp) -> %s"
            % (dataset, a, ref["ann"], d_ann, c, ref["conv8"], d_conv,
               "PASS" if ok else "FAIL")
        )

    all_ok = all(v["pass"] for v in summary.values())
    log("G0 reproducibility gate: " + ("PASS" if all_ok else "FAIL"))

    config = {
        "run_id": run_id,
        "stage": "S0/G0",
        "command": "conda run -n base python experiments/wp0_reproduce.py",
        "conda_env": "base",
        "device": DEVICE,
        "seeds": SEEDS,
        "T": T,
        "hidden": HIDDEN,
        "n_layers": 2,
        "tolerance_pp": TOL_PP,
        "external_asset_commit": EXTERNAL_COMMIT,
        "traceability": "content-addressed (see audits/traceability-policy.md)",
        "code_and_data_sha256": trace_basis,
        "python": platform.python_version(),
        "numpy": np.__version__,
    }
    (run_dir / "config.yaml").write_text(
        "\n".join(
            [
                "# content-addressed run configuration",
                *[
                    (k + ": " + json.dumps(v, ensure_ascii=False))
                    if not isinstance(v, dict)
                    else (k + ":")
                    for k, v in config.items()
                ],
            ]
        )
        + "\n"
        + "\n".join(
            "  " + k + ": " + v
            for group in trace_basis.values()
            for k, v in group.items()
        )
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "log.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (run_dir / "metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (ROOT / "results" / "wp0_repro.json").write_text(
        json.dumps({"summary": summary, "all_pass": all_ok, "run_id": run_id}, indent=2) + "\n",
        encoding="utf-8",
    )

    csv_path = ROOT / "registry" / "results.csv"
    with csv_path.open("a", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writerows(rows)
    log("wrote " + str(len(rows)) + " rows to registry/results.csv")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
