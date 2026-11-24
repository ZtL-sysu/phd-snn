#!/usr/bin/env python3
"""Write the top-level project/result.json, README.md and logs/run.log from CSVs.

Runs with cwd = the novix workspace root (the directory CONTAINING project/).
Also syncs project/ into the pullable session workspace if the two differ.
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
PROJ = ROOT / "project"
TP = PROJ / "teacher_probe"
(PROJ / "logs").mkdir(parents=True, exist_ok=True)


def rows(name):
    p = TP / "results" / name
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stats(vals):
    import numpy as np
    a = [float(v) for v in vals if v not in ("", None)]
    if not a:
        return None
    return dict(n=len(a), mean=round(float(np.mean(a)), 3),
                std=round(float(np.std(a)), 3),
                ci95=round(float(1.96 * np.std(a) / max(len(a) ** 0.5, 1)), 3))


result = dict(
    task="teacher_probe A/B/C/D",
    generated=datetime.now().isoformat(),
    cwd=str(ROOT),
    config_hash=(json.loads((TP / "config.json").read_text()).get("config_hash")
                 if (TP / "config.json").exists() else None),
    per_seed={},
    summary={},
    artifacts=[],
    errors=[],
)
for name in ("teacher_probe.csv", "strong_teacher_conversion.csv",
             "energy.csv", "fidelity_width.csv", "table1_reaudit.csv"):
    r = rows(name)
    result["per_seed"][name] = r
    if name == "teacher_probe.csv":
        for ds in ("MNIST", "CIFAR10"):
            for exp in ("T0", "T1", "T2", "T3", "T4", "T5"):
                v = [x["teacher_at_working_point"] for x in r
                     if x["dataset"] == ds and x["exp_id"] == exp]
                if v:
                    result["summary"][f"{ds}_{exp}_teacher"] = stats(v)
    elif name == "strong_teacher_conversion.csv":
        for ds in ("MNIST", "CIFAR10"):
            for T in (2, 4, 8, 16):
                for b in ("zero", "star"):
                    v = [x["loss_pp"] for x in r
                         if x["dataset"] == ds and x["T"] == str(T) and x["beta"] == b]
                    if v:
                        result["summary"][f"{ds}_T{T}_{b}_loss"] = stats(v)
for f in sorted(PROJ.rglob("*")):
    if f.is_file():
        result["artifacts"].append(str(f.relative_to(PROJ)))
runlog = TP / "RUNLOG.md"
if runlog.exists():
    for ln in runlog.read_text(encoding="utf-8").splitlines():
        if "FAILED" in ln or "ERROR" in ln or "BLOCKED" in ln:
            result["errors"].append(ln)

out = PROJ / "result.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(PROJ / "README.md").write_text(
    "# teacher_probe 全量实验交付\n\n"
    "复现：`bash teacher_probe/run_all.sh`（固定 seeds 0-4）。\n"
    "顶层 `result.json` 由 `teacher_probe/summarize.py` 从 `teacher_probe/results/*.csv` 生成，"
    "含逐 seed 记录、mean±std/95% CI、config_hash、异常与交付清单。\n"
    "关键结论见 `teacher_probe/FINDINGS.md`；复现偏差说明见 `teacher_probe/REPRO_BLOCKER.md`。\n",
    encoding="utf-8")
(PROJ / "logs" / "run.log").write_text(
    runlog.read_text(encoding="utf-8") if runlog.exists() else "no RUNLOG.md\n",
    encoding="utf-8")

# ---- path sync: novixlet cwd may be /home/novix/workspace, while pull reads
#      /mnt/novix-k8s-workspace-root/session_<id>/workspace ----
sws = sorted(glob.glob("/mnt/novix-k8s-workspace-root/session_*/workspace"))
if sws:
    sw = Path(sws[-1])
    if sw.resolve() != ROOT.resolve():
        dst = sw / "project"
        dst.mkdir(parents=True, exist_ok=True)
        for src in PROJ.rglob("*"):
            rel = src.relative_to(PROJ)
            if src.is_dir():
                (dst / rel).mkdir(parents=True, exist_ok=True)
            else:
                (dst / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst / rel)
        print("SYNCED to", dst)

sha = hashlib.sha256(out.read_bytes()).hexdigest()
print("RESULT_JSON", out, "sha256", sha, "artifacts", len(result["artifacts"]))
