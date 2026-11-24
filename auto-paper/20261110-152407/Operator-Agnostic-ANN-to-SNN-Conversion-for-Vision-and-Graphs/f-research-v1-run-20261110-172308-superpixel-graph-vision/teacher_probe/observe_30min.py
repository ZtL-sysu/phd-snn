#!/usr/bin/env python3
"""30-minute artifact watcher for 21247 (user chose 'observe 30 more minutes').

Uses the SESSION ID as target, because task:21247 now makes get_task fail with
IncompleteRead (~7.5 MB history). Watches the DATA PLANE (CSV/result.json),
not agent dialogue turns. Exits with a verdict file at 30 min or earlier if
artifacts appear. Never cancels or resubmits by itself.
"""
from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

R = Path(__file__).resolve().parent
SESSION = "87017bcfbba74e8124f6ac8e54316bfa"
TASK = "21247"
LOG = R / "observation.jsonl"
VERDICT = R / "OBSERVATION_RESULT.md"
INTERVAL = 300
MAX = 7   # t=0,5,10,15,20,25,30 -> 30 min


def sh(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


def listing(sub):
    rc, out, err = sh(f'novix debug ls {SESSION} {sub} -L 1', 90)
    return (rc, out, err)


def main():
    print(f"[{datetime.now():%H:%M:%S}] 30-min artifact watch start", flush=True)
    ls_timeouts = 0
    for i in range(1, MAX + 1):
        ts = datetime.now().isoformat()
        rc, out, err = listing("project/teacher_probe/results")
        csvs = sorted({ln.strip().split()[-1] for ln in out.splitlines()
                       if ".csv" in ln and not ln.startswith("==")})
        rc2, out2, _ = listing("project")
        has_result = "result.json" in out2
        rcm, outm, _ = sh(f"novix --json task result {TASK}", 90)
        try:
            m = json.loads(outm)
        except Exception:
            m = {}
        steps, status = m.get("steps"), m.get("status")
        if rc != 0:
            ls_timeouts += 1
        else:
            ls_timeouts = 0
        rec = dict(ts=ts, probe=i, minutes=(i - 1) * 5, status=status,
                   steps=steps, ls_rc=rc, ls_timeouts=ls_timeouts,
                   csvs=csvs, project_result_json=has_result)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(json.dumps(rec, ensure_ascii=False), flush=True)

        if csvs or has_result:
            VERDICT.write_text(
                "# OBSERVATION RESULT · ARTIFACTS APPEARED\n\n"
                f"- time: {ts}\n- task: `{TASK}`\n- csv: {csvs}\n"
                f"- project/result.json: {has_result}\n- steps: {steps}\n\n"
                "Data plane is producing artifacts. Continue normal watcher "
                "(`watch_novix_v3.py`); no cancellation or resubmission.\n",
                encoding="utf-8")
            print("VERDICT ARTIFACTS_APPEARED", flush=True)
            return 0

        if i == MAX:
            VERDICT.write_text(
                "# OBSERVATION RESULT · NO_ARTIFACTS_30MIN\n\n"
                f"- time: {ts}\n- task: `{TASK}`\n- steps: {steps}\n"
                f"- consecutive ls timeouts at end: {ls_timeouts}\n\n"
                "After 30 minutes the data plane still has NO result CSV and "
                "NO project/result.json. Per the user's chosen option, "
                "**switch to plan A**: cancel 21247 and resubmit the "
                "`novix_query_v3_execute_only.md` task (execute only; no audit, "
                "refactor, tests, benchmark or profiler). This watcher does not "
                "perform the cancellation itself.\n", encoding="utf-8")
            print("VERDICT NO_ARTIFACTS_30MIN", flush=True)
            return 2

        time.sleep(INTERVAL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
