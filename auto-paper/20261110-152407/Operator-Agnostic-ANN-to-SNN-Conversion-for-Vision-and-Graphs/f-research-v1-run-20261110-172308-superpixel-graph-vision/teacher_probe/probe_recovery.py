#!/usr/bin/env python3
"""Detect when novix novixlet agent startup recovers from the tiktoken failure.

Submits a tiny probe every 15 min (max 6, ~1.5 h). Recovery = the probe reaches
steps>0 or a terminal success within 10 min. Writes PLATFORM_RECOVERED.md.
Never resubmits the heavy experiment itself.
"""
from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

R = Path(__file__).resolve().parent
LOG = R / "platform_probe.jsonl"
FLAG = R / "PLATFORM_RECOVERED.md"
QUERY = ("# 平台可用性探针（只做环境自检）\n\n"
         "把 python 版本、torch 版本、cuda 可用性写到工作区根 "
         "`project/result.json`，字段 `probe/python/torch/cuda`。"
         "所有值必须真实运行产生。不要审计、不要下载数据、不要写测试、不要跑 benchmark。"
         "最终回复报告 result.json 路径与 SHA-256。\n")
INTERVAL = 900
MAX = 6


def sh(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


def parse(s):
    try:
        return json.loads(s)
    except Exception:
        return None


def note(obj):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(json.dumps(obj, ensure_ascii=False), flush=True)


def main():
    qfile = Path("C:/tmp/novix_recovery_probe.md")
    qfile.parent.mkdir(parents=True, exist_ok=True)
    qfile.write_text(QUERY, encoding="utf-8")
    for i in range(1, MAX + 1):
        rc, out, err = sh(
            f'novix --json task create "$(cat {qfile.as_posix()})" '
            '--provider novixlet --resource-pool exp-4090 --gpu --gpu-count 1')
        d = parse(out) or {}
        tid = d.get("id")
        note(dict(ts=datetime.now().isoformat(), round=i, submit_rc=rc,
                  task_id=tid, err=err[:200]))
        if not tid:
            time.sleep(INTERVAL)
            continue
        recovered = False
        for k in range(5):  # 10 min observation, 2 min apart
            time.sleep(120)
            rc2, out2, _ = sh(f"novix --json task result {tid}", 90)
            m = parse(out2) or {}
            steps, status = m.get("steps"), str(m.get("status") or "")
            note(dict(ts=datetime.now().isoformat(), round=i, probe=k + 1,
                      task_id=tid, status=status, steps=steps))
            if (isinstance(steps, int) and steps > 0) or status in (
                    "finish", "finished", "complete", "completed", "success"):
                recovered = True
                break
            if status in ("error", "failed"):
                break
        if recovered:
            FLAG.write_text(
                f"# PLATFORM RECOVERED\n\n- time: {datetime.now().isoformat()}\n"
                f"- probe task: `{tid}`\n- observation: agent started successfully\n\n"
                "Next action: resubmit `novix_query_v3_execute_only.md` "
                "(execute-only experiment task). This script does not do it.\n",
                encoding="utf-8")
            note(dict(ts=datetime.now().isoformat(), event="PLATFORM_RECOVERED",
                      task_id=tid))
            return 0
        if i < MAX:
            time.sleep(INTERVAL)
    (R / "PLATFORM_PROBE_EXHAUSTED.md").write_text(
        f"# Platform probe exhausted\n\n- time: {datetime.now().isoformat()}\n"
        f"- rounds: {MAX}\n- conclusion: novixlet agent startup still failing "
        "(tiktoken o200k_base download / SSL EOF). Manual decision required.\n",
        encoding="utf-8")
    note(dict(ts=datetime.now().isoformat(), event="PROBE_EXHAUSTED"))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
