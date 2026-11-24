#!/usr/bin/env python3
"""Watch novix task 20049 until a REAL terminal state, then pull and verify.

Terminal state requires ALL of:
  * parsed JSON status from the main channel (not just a transport success)
  * a finalReply / explicit terminal marker
  * a pullable project/result.json inside the run root
  * a recorded SHA-256 of the pulled result
Platform `status` alone is never authoritative (project history: 18885, 17682).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

R = Path(__file__).resolve().parents[1]
LOG = R / "novix" / "watch-log.md"
PULLED = R / "novix" / "pulled"
TASK = "20049"
INTERVAL_SEC = 600
MAX_PROBES = 36  # ~6 hours; low-frequency watch after a 3h NO_ALLOCATION stall


def sh(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as exc:
        return 1, "", f"{type(exc).__name__}: {exc}"


def parse_json(s):
    try:
        return json.loads(s)
    except Exception:
        start = s.find("{")
        end = s.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(s[start:end + 1])
            except Exception:
                return None
        return None


def note(line):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def probe(i):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rc1, out1, err1 = sh(f"novix --json task result {TASK}")
    j1 = parse_json(out1)
    rc2, out2, err2 = sh(f"novix --json debug task {TASK}")
    j2 = parse_json(out2)
    status = (j1 or {}).get("status")
    steps = (j1 or {}).get("steps")
    backend = ((j2 or {}).get("backend") or {}).get("status")
    placement = ((j2 or {}).get("placement") or {}).get("state")
    diagnosis = (j2 or {}).get("diagnosis")
    error = ((j2 or {}).get("backend") or {}).get("error_code")
    has_reply = bool((j1 or {}).get("finalReply") or (j1 or {}).get("final_reply"))
    note(f"[{ts}] probe {i}: rc={rc1}/{rc2} status={status} steps={steps} "
         f"backend={backend} placement={placement} diagnosis={diagnosis} "
         f"error={error!r} finalReply={has_reply}")
    if rc1 == 124 or rc1 == 4:
        note("  transport issue on main channel; out-of-band debug above is the fallback. "
             "No resubmission.")
    return dict(status=status, backend=backend, placement=placement,
                diagnosis=diagnosis, error=error, has_reply=has_reply,
                j1=j1, raw=out1)


def pull_and_verify():
    PULLED.mkdir(parents=True, exist_ok=True)
    rc, out, err = sh(f'novix debug pull task:{TASK} "{PULLED}"', timeout=600)
    note(f"pull rc={rc} out={out[:400]} err={err[:300]}")
    candidates = list(PULLED.rglob("result.json"))
    note(f"result.json candidates: {[str(p) for p in candidates][:10]}")
    for p in candidates:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            note(f"  unreadable {p}: {exc}")
            continue
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        runs = len(data.get("runs", [])) if isinstance(data, dict) else 0
        note(f"  ACCEPTED {p} runs={runs} sha256={sha}")
        summary = R / "results" / "novix-20049-summary.json"
        summary.parent.mkdir(parents=True, exist_ok=True)
        summary.write_text(json.dumps({
            "task_id": TASK, "result_path": str(p), "sha256": sha,
            "n_runs": runs, "summary": data.get("summary") if isinstance(data, dict) else None,
            "pulled_at": datetime.now().isoformat(),
        }, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
        return True
    note("  no valid project/result.json yet; terminal state NOT accepted.")
    return False


def main():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    note(f"=== watch {TASK} start {datetime.now().isoformat()} "
         f"interval={INTERVAL_SEC}s max_probes={MAX_PROBES} ===")
    note("Rule: only 'parsed status + finalReply + pullable project/result.json + SHA' "
         "counts as terminal. Queued/processing with NO_ALLOCATION is NOT a failure.")
    for i in range(1, MAX_PROBES + 1):
        st = probe(i)
        terminal = str(st["status"] or "").lower() in {
            "finish", "finished", "complete", "completed", "success",
            "failed", "error", "cancelled", "canceled"}
        if terminal and st["has_reply"]:
            ok = pull_and_verify()
            note(f"terminal status={st['status']} verified={ok}")
            if ok:
                note("WATCH_DONE_VERIFIED")
                return 0
            note("terminal reported but artifacts missing; keep watching for artifact_sync.")
        if i < MAX_PROBES:
            time.sleep(INTERVAL_SEC)
    note("WATCH_TIMEOUT: still not verified; do NOT resubmit, re-check manually.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
