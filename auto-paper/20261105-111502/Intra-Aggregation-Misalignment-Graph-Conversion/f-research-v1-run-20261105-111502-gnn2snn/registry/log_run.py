#!/usr/bin/env python3
"""Single writer for `registry/results.csv` (brief §9, discipline #2 and #6).

Every experiment in this project must funnel its numbers through `record()` so that
(a) the paper's tables can be generated from one CSV instead of hand-copied numbers,
(b) each row carries the git commit it was produced under, and
(c) a `runs/<run_id>/` directory exists with the config and the log.

Deliberately dependency-free (stdlib + subprocess for git) so it cannot break the
experiments it is supposed to be recording.
"""
from __future__ import annotations

import csv
import datetime as _dt
import json
import os
import platform
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "registry" / "results.csv"
RUNS = ROOT / "runs"

FIELDS = ["run_id", "date", "wp", "dataset", "method", "t_steps", "hidden", "seed",
          "ann_ref", "acc", "gap_pp", "spikes_per_node", "sop_est", "train_seconds",
          "retrain_count", "git_commit", "notes"]


def git_commit() -> str:
    """Short HEAD hash, or 'dirty:<hash>' when the worktree has uncommitted changes.

    A run whose commit cannot be reconstructed is worthless for review, so we mark
    dirtiness explicitly rather than pretending the hash identifies the code.
    """
    try:
        h = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, timeout=10).stdout.strip()
        if not h:
            return "no-git"
        # The registry and the run directories are *outputs* of the code, so committing them
        # would be circular: without excluding them every row would be stamped "dirty" the
        # moment it is written. Only changes to code, protocol or data definitions count.
        d = subprocess.run(["git", "status", "--porcelain", "--",
                            ":!registry/results.csv", ":!runs", ":!figures_report",
                            ":!notes"], cwd=ROOT, capture_output=True, text=True,
                           timeout=20).stdout.strip()
        return f"dirty:{h}" if d else h
    except Exception:
        return "no-git"


def new_run(wp: str, tag: str, config: dict | None = None) -> Path:
    """Create runs/<wp>-<tag>-<stamp>/ with config.yaml, log.txt, metrics.json."""
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    rid = f"{wp.lower()}-{tag}-{stamp}"
    d = RUNS / rid
    d.mkdir(parents=True, exist_ok=True)
    cfg = {
        "run_id": rid,
        "git_commit": git_commit(),
        "created": _dt.datetime.now().isoformat(timespec="seconds"),
        "host": socket.gethostname(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
    }
    cfg.update(config or {})
    (d / "config.yaml").write_text(
        "\n".join(f"{k}: {json.dumps(v, default=str)}" for k, v in cfg.items()) + "\n",
        encoding="utf-8")
    (d / "log.txt").write_text("", encoding="utf-8")
    (d / "metrics.json").write_text("{}", encoding="utf-8")
    return d


def record(rows, run_dir: Path | None = None, wp: str = "", notes: str = "") -> None:
    """Append rows (list of dicts keyed by FIELDS) to results.csv.

    Missing keys are filled with "" so a partially-populated row is visibly partial
    rather than silently wrong. Rows are written immediately (append mode) so a crash
    halfway through a sweep keeps the cells that already finished.
    """
    CSV.parent.mkdir(parents=True, exist_ok=True)
    new_file = not CSV.exists()
    rid = run_dir.name if run_dir else ""
    commit = git_commit()
    today = _dt.date.today().isoformat()
    with open(CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        for r in rows:
            r = dict(r)
            r.setdefault("run_id", rid)
            r.setdefault("date", today)
            r.setdefault("wp", wp)
            r.setdefault("git_commit", commit)
            if notes:
                r["notes"] = (str(r.get("notes", "")) + " " + notes).strip()
            w.writerow({k: r.get(k, "") for k in FIELDS})
    if run_dir is not None:
        with open(run_dir / "metrics.json", "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, default=str)
        with open(run_dir / "log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n# recorded {len(rows)} rows at {_dt.datetime.now().isoformat()}\n")
    print(f"[registry] appended {len(rows)} rows -> {CSV.relative_to(ROOT)}", flush=True)


def load():
    """Read results.csv back as a list of dicts (numbers coerced)."""
    if not CSV.exists():
        return []
    out = []
    with open(CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in ("t_steps", "hidden", "seed", "retrain_count"):
                if r.get(k) not in ("", None):
                    try:
                        r[k] = int(r[k])
                    except ValueError:
                        pass
            for k in ("ann_ref", "acc", "gap_pp", "spikes_per_node", "sop_est",
                      "train_seconds"):
                if r.get(k) not in ("", None):
                    try:
                        r[k] = float(r[k])
                    except ValueError:
                        pass
            out.append(r)
    return out


if __name__ == "__main__":
    rows = load()
    print(f"{len(rows)} rows in {CSV}")
    from collections import Counter
    print("by wp:", dict(Counter(r["wp"] for r in rows)))
    print("by method:", dict(Counter(r["method"] for r in rows)))
