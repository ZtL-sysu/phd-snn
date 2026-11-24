#!/usr/bin/env python3
"""Watch novix task 21247; on terminal state, pull to a SHORT path and sync.

Windows path-length guard: the run root is very deep, so pull first to
C:/tmp/tp21247 and only then copy into the run root with \\?\ long-path prefix.
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
INTERVAL = 600
MAX = 36  # ~6 h


def sh(cmd, timeout=900):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


def note(s):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(s + "\n")
    print(s, flush=True)


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


def long(p: Path) -> str:
    return "\\\\?\\" + str(p.resolve())


def sync(src: Path, dst: Path):
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


def main():
    note(f"=== watch {TASK} start {datetime.now().isoformat()} ===")
    note("Rule: terminal requires parsed status + finalReply + pullable project/result.json + SHA.")
    for i in range(1, MAX + 1):
        rc, out, err = sh(f"novix --json task result {TASK}", 120)
        d = parse(out) or {}
        status = str(d.get("status") or "")
        steps = d.get("steps")
        reply = bool(d.get("finalReply"))
        rc2, out2, _ = sh(f"novix --json debug task {TASK}", 120)
        dd = parse(out2) or {}
        b = dd.get("backend") or {}
        pl = dd.get("placement") or {}
        note(f"[{datetime.now():%H:%M:%S}] probe {i}: rc={rc}/{rc2} status={status} "
             f"steps={steps} reply={reply} backend={b.get('status')} "
             f"placement={pl.get('state')} node={pl.get('node')}")
        terminal = status.lower() in ("finish", "finished", "complete", "completed",
                                     "success", "failed", "error", "cancelled", "canceled")
        if terminal and reply:
            if SHORT.exists():
                shutil.rmtree(SHORT, ignore_errors=True)
            SHORT.mkdir(parents=True, exist_ok=True)
            prc, pout, perr = sh(f'novix debug pull task:{TASK} "{SHORT}"', 900)
            note(f"pull rc={prc} out={pout[:200]} err={perr[:200]}")
            got = list(SHORT.rglob("result.json"))
            note(f"result.json candidates: {[str(x) for x in got][:5]}")
            for p in got:
                try:
                    obj = json.loads(p.read_text(encoding="utf-8"))
                except Exception as e:
                    note(f"unreadable {p}: {e}")
                    continue
                sha = hashlib.sha256(p.read_bytes()).hexdigest()
                (DEST / "result.sha256").write_text(sha + "\n", encoding="utf-8")
                n = sync(SHORT, DEST)
                note(f"ACCEPTED {p} sha256={sha} synced_files={n} "
                     f"summary_keys={len(obj.get('summary', {}))}")
                note("WATCH_DONE_VERIFIED")
                return 0
            note("terminal but no pullable result.json; keep watching for artifact sync")
        if i < MAX:
            time.sleep(INTERVAL)
    note("WATCH_TIMEOUT: not verified; do NOT resubmit blindly, inspect manually.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
