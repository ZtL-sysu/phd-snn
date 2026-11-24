#!/usr/bin/env python3
"""Hardened watcher for novix task 21247 (no repeat of the 20049 failure).

20049 post-mortem / countermeasures implemented here:
  1. queued / NO_ALLOCATION for ~3 h unnoticed  -> queue-stall alarm after 15 min
  2. backend died on 429 + unrecognized_model   -> immediate pattern alarm on error_info
  3. main API rc=4/503 misleading               -> out-of-band debug is authoritative
  4. "finish" with zero pullable artifacts     -> terminal needs parsed status +
       finalReply + project/result.json + SHA; failed runs still get a rescue pull
  5. agent steps frozen silently               -> steps-stall alarm after 20 min
  6. deep run-root path -> WinError 206        -> pull to C:/tmp/tp21247 first
  7. result.json written outside pullable ws   -> verify + sync, alert if missing
  8. repeated blind resubmission               -> never resubmits; writes an alert
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

R = Path(__file__).resolve().parent
TASK = "21247"
SHORT = Path("C:/tmp/tp21247")
DEST = R / "novix_delivery"
LOG = R / "novix_watch.md"
JSONL = R / "novix_watch.jsonl"
ALERT = R / "NOVIX_ALERT.md"
INTERVAL = 180
MAX = 120                 # ~6 h
QUEUE_STALL_SEC = 15 * 60
STEPS_STALL_SEC = 20 * 60
FAIL_PATTERNS = ("429", "usage limit", "unrecognized_model", "request rejected",
                 "api error", "sdk error", "out of memory", "cuda out of memory")


def sh(cmd, timeout=900):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


def parse(s):
    try:
        return json.loads(s)
    except Exception:
        i, j = s.find("{"), s.rfind("}")
        if 0 <= i < j:
            try:
                return json.loads(s[i:j + 1])
            except Exception:
                return None
        return None


def note(msg):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def long(p: Path) -> str:
    return "\\\\?\\" + str(p.resolve())


def sync(src: Path, dst: Path) -> int:
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in src.rglob("*"):
        rel = f.relative_to(src)
        t = Path(long(dst / rel))
        if f.is_dir():
            t.mkdir(parents=True, exist_ok=True)
        else:
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(long(f), t)
            n += 1
    return n


def alert(kind, detail):
    body = (f"# NOVIX ALERT · {kind}\n\n"
            f"- time: {datetime.now().isoformat()}\n"
            f"- task: `{TASK}`\n"
            f"- detail: {detail}\n\n"
            "Action required before any resubmission: inspect `novix_watch.jsonl`, "
            "`novix --json debug task 21247` and the workspace listing. "
            "This watcher never resubmits automatically.\n")
    ALERT.write_text(body, encoding="utf-8")
    note(f"ALERT {kind}: {detail}")


def rescue_pull(tag):
    """Even on failure, pull whatever exists so partial evidence is not lost."""
    if SHORT.exists():
        shutil.rmtree(SHORT, ignore_errors=True)
    SHORT.mkdir(parents=True, exist_ok=True)
    rc, out, err = sh(f'novix debug pull task:{TASK} "{SHORT}"', 900)
    note(f"rescue pull ({tag}) rc={rc} out={out[:160]} err={err[:160]}")
    found = list(SHORT.rglob("result.json"))
    note(f"rescue result.json candidates: {[str(x) for x in found][:5]}")
    if SHORT.exists():
        try:
            n = sync(SHORT, DEST)
            note(f"rescue synced {n} files to {DEST}")
        except Exception as exc:
            note(f"rescue sync failed: {type(exc).__name__}: {exc}")
    return found


def terminal_and_verified(status, reply, found):
    return (status.lower() in ("finish", "finished", "complete", "completed", "success")
            and reply and bool(found))


def main():
    note(f"=== hardened watch {TASK} start; interval={INTERVAL}s max={MAX} ===")
    note("20049 countermeasures: queue-stall 15min / steps-stall 20min / "
         "429+unrecognized_model immediate alarm / out-of-band authoritative / "
         "terminal = parsed status + finalReply + pullable result.json + SHA")
    first_queue_t = None
    last_state = None
    last_steps = None
    last_steps_change = time.time()
    for i in range(1, MAX + 1):
        rc, out, err = sh(f"novix --json task result {TASK}", 120)
        d = parse(out) or {}
        rc2, out2, err2 = sh(f"novix --json debug task {TASK}", 120)
        dd = parse(out2) or {}
        b = dd.get("backend") or {}
        pl = dd.get("placement") or {}
        pool = dd.get("pool_status") or {}
        info = (b.get("error_info") or "")
        status = str(d.get("status") or "")
        steps = d.get("steps")
        reply = bool(d.get("finalReply"))
        state = pl.get("state")
        rec = dict(ts=datetime.now().isoformat(), probe=i, rc_main=rc, rc_debug=rc2,
                   status=status, steps=steps, finalReply=reply,
                   backend=b.get("status"), error_code=b.get("error_code"),
                   error_info=info[:500], placement=state, node=pl.get("node"),
                   dispatch_phase=pl.get("dispatch_phase"), pool=pool,
                   artifact_sync=dd.get("artifact_sync"), diagnosis=dd.get("diagnosis"))
        with JSONL.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        note(f"probe {i}: rc={rc}/{rc2} status={status} steps={steps} reply={reply} "
             f"backend={b.get('status')} err={b.get('error_code')} "
             f"placement={state} node={pl.get('node')} "
             f"pool={pool.get('eligible_nodes')}/paused={pool.get('dispatch_paused')}")

        # --- 20049 #2: platform-side failure patterns ---
        low = info.lower()
        hit = [p for p in FAIL_PATTERNS if p in low]
        if hit or (str(b.get("status") or "").lower() in ("error", "failed")):
            note(f"IMMEDIATE PLATFORM FAILURE: patterns={hit} backend={b.get('status')}")
            found = rescue_pull("platform-failure")
            alert("PLATFORM_FAILURE", f"patterns={hit}; backend={b.get('status')}; "
                  f"error_info={info[:400]}; rescue_result_json={len(found)}")
            return 3

        # --- 20049 #1: queue stall ---
        now = time.time()
        if state in ("queued", "reserved"):
            if first_queue_t is None:
                first_queue_t = now
            if now - first_queue_t > QUEUE_STALL_SEC:
                alert("QUEUE_STALL", f"placement stayed '{state}' for >15 min "
                      f"(node={pl.get('node')}, pool={pool})")
                return 2
        elif state in ("submitted", "running", "released"):
            first_queue_t = None
        last_state = state

        # --- 20049 #5: frozen steps ---
        if isinstance(steps, int):
            if steps != last_steps:
                last_steps = steps
                last_steps_change = now
            elif now - last_steps_change > STEPS_STALL_SEC:
                alert("STEPS_STALL", f"steps frozen at {steps} for >20 min; "
                      f"backend={b.get('status')} placement={state}")
                return 2

        # --- 20049 #4: strict terminal verdict ---
        terminal = status.lower() in ("finish", "finished", "complete", "completed",
                                     "success", "failed", "error", "cancelled", "canceled")
        if terminal and reply:
            found = rescue_pull("terminal")
            verified = False
            for p in found:
                try:
                    obj = json.loads(p.read_text(encoding="utf-8"))
                except Exception as exc:
                    note(f"unreadable {p}: {exc}")
                    continue
                sha = hashlib.sha256(p.read_bytes()).hexdigest()
                (DEST / "result.sha256").write_text(sha + "\n", encoding="utf-8")
                n = sync(SHORT, DEST)
                note(f"ACCEPTED {p} sha256={sha} synced={n} "
                     f"summary_keys={len(obj.get('summary', {}))}")
                verified = True
            if verified and status.lower() not in ("failed", "error", "cancelled", "canceled"):
                note("WATCH_DONE_VERIFIED")
                return 0
            alert("TERMINAL_UNVERIFIED", f"status={status} reply={reply} "
                  f"pullable_result_json={len(found)}")
            return 2

        if i < MAX:
            time.sleep(INTERVAL)
    alert("WATCH_TIMEOUT", "6 h elapsed without a verified terminal state")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
