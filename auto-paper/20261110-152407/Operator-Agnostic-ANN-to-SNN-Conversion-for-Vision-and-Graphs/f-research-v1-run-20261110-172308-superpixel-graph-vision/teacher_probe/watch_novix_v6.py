#!/usr/bin/env python3
"""v4 watcher for 21524: session-id artifact channel + data-plane liveness.

v2 raised STEPS_STALL when `steps` froze at 201 for 20 min. That was a false
positive: steps are agent dialogue turns, and one long full-dataset training
command does not increment them. Independent checks showed steps 201->203 and
project/ mtimes advancing 05:07->06:05. v3 uses workspace activity as the
primary liveness signal and only alarms when BOTH signals are frozen.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

R = Path(__file__).resolve().parent
TASK = "21591"
SESSION = "24a9abd220b5201603f267e230e2fcec"
SHORT = Path("C:/tmp/tp21591")
DEST = R / "novix_delivery_21591"
LOG = R / "novix_watch_21591_v6.md"
JSONL = R / "novix_watch_21591_v6.jsonl"
ALERT = R / "NOVIX_ALERT_21591.md"
INTERVAL = 180
MAX = 240                     # ~12 h
QUEUE_STALL_SEC = 15 * 60
STEPS_STALL_SEC = 45 * 60     # relaxed; must coincide with frozen workspace
FAIL_PATTERNS = ("429", "usage limit", "unrecognized_model", "request rejected",
                 "api error", "sdk error", "out of memory", "cuda out of memory")
TS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def sh(cmd, timeout=240):
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
        t = Path(long(dst / f.relative_to(src)))
        if f.is_dir():
            t.mkdir(parents=True, exist_ok=True)
        else:
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(long(f), t)
            n += 1
    return n


def alert(kind, detail):
    ALERT.write_text(
        f"# NOVIX ALERT · {kind}\n\n- time: {datetime.now().isoformat()}\n"
        f"- task: `{TASK}`\n- detail: {detail}\n\n"
        "Inspect `novix_watch.jsonl`, `novix --json debug task 21247` and the "
        "workspace listing before any decision. This watcher never resubmits.\n",
        encoding="utf-8")
    note(f"ALERT {kind}: {detail}")


def workspace_stamp():
    """Newest mtime visible in project/ (data-plane liveness). None on timeout."""
    rc, out, _ = sh(f"novix debug ls {SESSION} project -L 1", 120)
    if rc != 0:
        return None
    stamps = TS.findall(out)
    return max(stamps) if stamps else None


def rescue_pull(tag):
    if SHORT.exists():
        shutil.rmtree(SHORT, ignore_errors=True)
    SHORT.mkdir(parents=True, exist_ok=True)
    rc, out, err = sh(f'novix debug pull {SESSION} "{SHORT}"', 900)
    note(f"rescue pull ({tag}) rc={rc} out={out[:160]} err={err[:160]}")
    found = list(SHORT.rglob("result.json"))
    note(f"rescue result.json candidates: {[str(x) for x in found][:5]}")
    try:
        n = sync(SHORT, DEST)
        note(f"rescue synced {n} files to {DEST}")
    except Exception as exc:
        note(f"rescue sync failed: {type(exc).__name__}: {exc}")
    return found


def main():
    note(f"=== v3 watch {TASK} start; interval={INTERVAL}s max={MAX} ===")
    note("v2 STEPS_STALL at 201 was a FALSE POSITIVE (steps 201->203, project "
         "mtimes advancing). v3: data-plane workspace stamp is primary; "
         "steps-stall needs 45min AND frozen workspace.")
    first_queue_t = None
    last_steps = None
    last_steps_change = time.time()
    last_stamp = None
    last_stamp_change = time.time()
    consecutive_bad_control = 0
    no_stamp_run = 0
    for i in range(1, MAX + 1):
        rc, out, err = sh(f"novix --json task result {TASK}", 120)
        d = parse(out) or {}
        rc2, out2, err2 = sh(f"novix --json debug task {TASK}", 120)
        dd = parse(out2) or {}
        b = dd.get("backend") or {}
        pl = dd.get("placement") or {}
        pool = dd.get("pool_status") or {}
        info = b.get("error_info") or ""
        status = str(d.get("status") or "")
        steps = d.get("steps")
        reply = bool(d.get("finalReply"))
        state = pl.get("state")
        stamp = workspace_stamp()
        rec = dict(ts=datetime.now().isoformat(), probe=i, watcher="v3",
                   rc_main=rc, rc_debug=rc2, status=status, steps=steps,
                   finalReply=reply, backend=b.get("status"),
                   error_code=b.get("error_code"), error_info=info[:500],
                   placement=state, node=pl.get("node"), pool=pool,
                   workspace_stamp=stamp, diagnosis=dd.get("diagnosis"),
                   artifact_sync=dd.get("artifact_sync"))
        with JSONL.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        note(f"probe {i}: rc={rc}/{rc2} status={status} steps={steps} "
             f"backend={b.get('status')} err={b.get('error_code')} "
             f"placement={state} stamp={stamp} "
             f"pool={pool.get('eligible_nodes')}")

        low = info.lower()
        hit = [p for p in FAIL_PATTERNS if p in low]
        if hit or str(b.get("status") or "").lower() in ("error", "failed"):
            found = rescue_pull("platform-failure")
            alert("PLATFORM_FAILURE", f"patterns={hit}; backend={b.get('status')}; "
                  f"error_info={info[:400]}; rescue_result_json={len(found)}")
            return 3

        # control-plane degradation: both channels unusable repeatedly
        if rc not in (0,) and rc2 not in (0,):
            consecutive_bad_control += 1
            if consecutive_bad_control >= 5:
                alert("CONTROL_PLANE_DEGRADED",
                      f"main+out-of-band failed {consecutive_bad_control} probes in a row")
                return 2
        else:
            consecutive_bad_control = 0

        now = time.time()
        if state in ("queued", "reserved"):
            if first_queue_t is None:
                first_queue_t = now
            if now - first_queue_t > QUEUE_STALL_SEC:
                alert("QUEUE_STALL", f"placement '{state}' >15 min, pool={pool}")
                return 2
        else:
            first_queue_t = None

        # data-plane liveness. A missing stamp means the control-plane ls
        # timed out, NOT that the workspace is frozen (track-ops is flaky).
        if stamp is not None:
            no_stamp_run = 0
            if stamp != last_stamp:
                last_stamp = stamp
                last_stamp_change = now
        else:
            no_stamp_run += 1
            if no_stamp_run >= 10:  # 30 min of failed workspace listing
                alert("WORKSPACE_LS_UNAVAILABLE",
                      f"10 consecutive probes could not list project/ "
                      f"(track-ops flaky); backend={b.get('status')} "
                      f"placement={state}; manual inspection needed")
                return 2

        # steps is a SOFT signal: alarm only if both are frozen
        if isinstance(steps, int):
            if steps != last_steps:
                last_steps = steps
                last_steps_change = now
        steps_frozen = now - last_steps_change > STEPS_STALL_SEC
        stamp_frozen = (last_stamp is not None) and (now - last_stamp_change > STEPS_STALL_SEC)
        if steps_frozen and stamp_frozen:
            alert("DUAL_STALL", f"steps frozen at {last_steps} >45min AND "
                  f"workspace stamp frozen at {last_stamp}; backend={b.get('status')} "
                  f"placement={state}")
            return 2

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
