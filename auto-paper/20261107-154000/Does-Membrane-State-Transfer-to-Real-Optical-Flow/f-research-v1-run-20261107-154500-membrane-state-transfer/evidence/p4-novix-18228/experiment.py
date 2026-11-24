#!/usr/bin/env python3
"""CLI for the f-research-v1 P4 C1 correction-loop-v3 full experiment.

This entrypoint immediately delegates to a crash-safe runner.  ``result.json``
is atomically checkpointed before downloads, after each invariant, and after each
experiment group, including on design-invalid or runtime-error exits.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fresearch.runner import run_full  # noqa: E402
from fresearch.utils import hardware_report  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run P4 C1 correction-loop-v3 with four fail-fast invariants."
    )
    parser.add_argument("--run-full", action="store_true", help="Run the complete pipeline (default).")
    parser.add_argument(
        "--reuse-features", action="store_true",
        help="Reuse feature caches only when their data/graph/config signatures match exactly.",
    )
    parser.add_argument(
        "--skip-download", action="store_true",
        help="Do not imply offline mode: existing files are still byte/hash/format validated.",
    )
    parser.add_argument("--hardware-only", action="store_true", help="Print hardware metadata and exit.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.hardware_only:
        print(json.dumps(hardware_report(), indent=2, ensure_ascii=False))
        return 0
    result = run_full(
        PROJECT_DIR,
        reuse_features=args.reuse_features,
        skip_download=args.skip_download,
    )
    summary = {
        "status": result.get("status"),
        "design_valid": result.get("design_valid"),
        "phase": result.get("phase"),
        "verdict": result.get("verdict", {}).get("decision"),
        "result_path": str(PROJECT_DIR / "result.json"),
        "total_elapsed_s": result.get("total_elapsed_s"),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if result.get("status") == "completed":
        return 0
    if result.get("status") == "design_invalid":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
