#!/usr/bin/env python3
"""Local 3060 full 5-seed campaign, CORRECTED combination (beta removed), mirroring local_full's specification.

Reason: novix 20049 has been queued / NO_ALLOCATION for >3h with steps=0.
This is a PARALLEL INSURANCE run, not a replacement: 20049 stays in flight
and its artifacts will still be pulled if it ever terminates.

All numbers here are produced by real local runs. Same config as the remote
spec so results are directly comparable.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_experiments as RE  # noqa: E402

R = HERE.parent
OUT = R / "results" / "local_full_v2"
OUT.mkdir(parents=True, exist_ok=True)
CFG = dict(datasets=["MNIST", "CIFAR10"], seeds=[0, 1, 2, 3, 4],
           n_train=5000, n_val=1000, n_test=2000, epochs=1000,
           hidden=128, lr=0.01, device="cuda", pool="sum",
           ours_beta="zero")

(OUT / "config.json").write_text(json.dumps(
    dict(CFG, note="local 3060 CORRECTED combination (redundant beta removed); paired with local_full; novix 20049 still in flight",
         energy_model="45nm theoretical arithmetic energy, NOT hardware measurement"),
    indent=2), encoding="utf-8")

LOG = OUT / "run.log"


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    result = dict(meta=dict(note="real local runs, no fabricated values",
                            started=datetime.now().isoformat()), runs=[])
    t0 = time.time()
    for ds in CFG["datasets"]:
        for seed in CFG["seeds"]:
            ts = time.time()
            try:
                rec = RE.run_one(ds, seed, CFG["n_train"], CFG["n_val"], CFG["n_test"],
                                 CFG["epochs"], device=CFG["device"],
                                 hidden=CFG["hidden"], lr=CFG["lr"], pool=CFG["pool"],
                                 ours_beta=CFG["ours_beta"])
                rec["dataset"], rec["seed"] = ds, seed
                rec["wall_sec"] = round(time.time() - ts, 2)
                result["runs"].append(rec)
                log(f"{ds} seed {seed} ANN {rec['ann']['test_acc']*100:.2f}% "
                    f"ours_T8 {rec['methods']['ours_T8']['acc']*100:.2f}% "
                    f"wall {rec['wall_sec']}s")
            except Exception as exc:
                log(f"{ds} seed {seed} FAILED {type(exc).__name__}: {exc}")
                result["runs"].append(dict(dataset=ds, seed=seed,
                                           error=f"{type(exc).__name__}: {exc}"))
            (OUT / "result.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2, default=float),
                encoding="utf-8")

    ok = [r for r in result["runs"] if "ann" in r]
    summary = {}
    for ds in CFG["datasets"]:
        rs = [r for r in ok if r["dataset"] == ds]
        if not rs:
            summary[ds] = dict(error="no successful runs")
            continue
        keys = [k for k in rs[0]["methods"]]
        summary[ds] = dict(
            n_seeds=len(rs),
            ann_mean=float(np.mean([r["ann"]["test_acc"] for r in rs])),
            ann_std=float(np.std([r["ann"]["test_acc"] for r in rs])),
            methods={k: dict(mean=float(np.mean([r["methods"][k]["acc"] for r in rs])),
                             std=float(np.std([r["methods"][k]["acc"] for r in rs])))
                     for k in keys},
            energy={f"T{T}": float(np.mean([
                r["energy"][f"ours_T{T}"]["energy_ratio_ann_over_snn"]
                for r in rs if f"ours_T{T}" in r["energy"]]))
                for T in (1, 2, 4, 8, 16)},
        )
    result["summary"] = summary
    result["meta"]["finished"] = datetime.now().isoformat()
    result["meta"]["total_sec"] = round(time.time() - t0, 2)
    (OUT / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    log("DONE " + json.dumps({k: {"ann": round(v.get("ann_mean", -1) * 100, 2),
                                  "n": v.get("n_seeds")}
                              for k, v in summary.items()}))


if __name__ == "__main__":
    main()
