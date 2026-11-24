"""Wait for novix task 17682 to reach a terminal state, then pull its workspace.

Polls a read-only status endpoint every 60 s (waiting on an external process, not retrying
a failed command). Never fabricates results: if the task fails or the workspace is absent,
that is recorded verbatim in wait-status.json.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = "17682"
DEADLINE = time.time() + 2700
POLL = 60
TERMINAL_OK = {"completed", "success", "succeeded", "finished", "done"}
log = []


def run(args, timeout=180):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return subprocess.CompletedProcess(args, -1, "", f"{type(exc).__name__}: {exc}")


def last_json(text):
    for line in reversed(text.strip().splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


status = "unknown"
timed_out = False
while time.time() < DEADLINE:
    r = run(["novix", "--json", "task", "result", TASK])
    d = last_json(r.stdout) or {}
    parsed = d.get("status")
    # rc=4 / unparsable output is a TRANSPORT error, not a task terminal state.
    # Treating it as failure previously caused a premature exit while the task was still running.
    if parsed is None or r.returncode != 0:
        entry = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"),
                 "status": "transport_error_retry", "steps": d.get("steps"), "rc": r.returncode}
        log.append(entry)
        print("POLL", json.dumps(entry), flush=True)
        time.sleep(POLL)
        continue
    status = str(parsed)
    entry = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "status": status,
             "steps": d.get("steps"), "rc": r.returncode}
    log.append(entry)
    print("POLL", json.dumps(entry), flush=True)
    if status.lower() in TERMINAL_OK or status.lower() in {"failed", "error", "cancelled", "canceled"}:
        break
    time.sleep(POLL)
else:
    timed_out = True

# Always capture the final result text.
res = run(["novix", "task", "result", TASK])
(HERE / "task-result-final.txt").write_text(
    (res.stdout or "") + "\n--- stderr ---\n" + (res.stderr or ""), encoding="utf-8")

pulled_ok = False
pull_log = []
if timed_out:
    pull_log.append({"skipped": "task still running at deadline; leave task id in automation-state.json for the next round"})
else:
    for attempt in range(1, 5):
        p = run(["novix", "debug", "pull", f"task:{TASK}", str(HERE / "pulled")], timeout=300)
        pull_log.append({"attempt": attempt, "rc": p.returncode,
                         "stdout": (p.stdout or "")[-800:], "stderr": (p.stderr or "")[-800:]})
        print("PULL", attempt, "rc=", p.returncode, flush=True)
        if p.returncode == 0 and any((HERE / "pulled").rglob("*")):
            pulled_ok = True
            break
        if status.lower() in {"failed", "error", "cancelled", "canceled"}:
            break
        time.sleep(POLL)

(HERE / "pull-final.log").write_text(json.dumps(pull_log, indent=2, ensure_ascii=False), encoding="utf-8")
files = [{"size": q.stat().st_size, "path": str(q.relative_to(HERE))}
         for q in (HERE / "pulled").rglob("*") if q.is_file()]
summary = {"task_id": TASK, "final_status": status, "timed_out": timed_out,
           "pulled_ok": pulled_ok, "poll_log": log, "pulled_files": files,
           "note": "No result is inferred here. Acceptance verdict must be computed from the pulled result.json."}
(HERE / "wait-status.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
print("DONE", json.dumps({"status": status, "pulled_ok": pulled_ok, "n_files": len(files)}), flush=True)
