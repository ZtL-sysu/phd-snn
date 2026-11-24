"""Parallel HTTP Range downloader for a single large public Zenodo file.

Only used to fetch openly licensed connectome data faster. No credentials.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import math
import os
import time
from pathlib import Path

import requests

URL = ("https://zenodo.org/api/records/21549559/files/"
       "connections_biological.csv.gz/content")
SIZE = 178853187


def fetch(i: int, start: int, end: int, out: Path, url: str, retries: int = 3):
    part = out.with_suffix(f".part{i}")
    if part.exists() and part.stat().st_size == end - start + 1:
        return i, part.stat().st_size, "cached"
    for attempt in range(retries):
        try:
            r = requests.get(url, headers={"Range": f"bytes={start}-{end}"}, timeout=(15, 180))
            if r.status_code == 206 and len(r.content) == end - start + 1:
                part.write_bytes(r.content)
                return i, len(r.content), "ok"
            if r.status_code == 200 and len(r.content) == SIZE:
                # server ignored Range; fall back to single-stream (handled by caller)
                return i, 0, "no-range"
        except Exception as exc:
            if attempt == retries - 1:
                return i, 0, f"error:{type(exc).__name__}"
    return i, 0, "failed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "data" / "zenodo" / "connections_biological.csv.gz"))
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--size", type=int, default=SIZE)
    ap.add_argument("--url", default=URL)
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n = args.workers
    chunk = math.ceil(args.size / n)
    jobs = []
    for i in range(n):
        s = i * chunk
        e = min(s + chunk - 1, args.size - 1)
        if s <= e:
            jobs.append((i, s, e))
    t0 = time.time()
    results = []
    with cf.ThreadPoolExecutor(max_workers=n) as ex:
        futs = {ex.submit(fetch, i, s, e, out, args.url): i for i, s, e in jobs}
        for f in cf.as_completed(futs):
            results.append(f.result())
            print("part", f.result()[0], f.result()[2], flush=True)
    if any(r[2] != "ok" and r[2] != "cached" for r in results):
        print("PARALLEL_DOWNLOAD_FAILED", results, flush=True)
        return 1
    with out.open("wb") as w:
        for i, _, _ in sorted(results):
            w.write(out.with_suffix(f".part{i}").read_bytes())
    for i, _, _ in results:
        out.with_suffix(f".part{i}").unlink(missing_ok=True)
    print(f"DONE bytes={out.stat().st_size} seconds={round(time.time()-t0,1)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
