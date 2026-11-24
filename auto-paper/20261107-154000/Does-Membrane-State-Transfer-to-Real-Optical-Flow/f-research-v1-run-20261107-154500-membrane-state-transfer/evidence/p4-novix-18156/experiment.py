#!/usr/bin/env python3
"""Restart-safe command-line entrypoint for the f-research-v1 P4 batch.

Usage:
    python3 /home/novix/workspace/project/experiment.py --stage A
    python3 /home/novix/workspace/project/experiment.py --stage B
    python3 /home/novix/workspace/project/experiment.py --stage C

Every completed seed/condition is durably checkpointed in ``result.json``.
Re-running a stage resumes missing work unless ``--force`` is supplied.
"""
from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

PROJECT = Path("/home/novix/workspace/project")
SRC = PROJECT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from p4_pipeline.common import add_unavailable, append_command, checkpoint, load_result  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one restart-safe P4 full-batch stage")
    parser.add_argument("--stage", required=True, choices=("A", "B", "C"))
    parser.add_argument("--force", action="store_true", help="recompute completed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = f"python3 {Path(__file__).resolve()} --stage {args.stage}" + (" --force" if args.force else "")
    append_command(command)
    checkpoint(f"stage_{args.stage}_dispatch", {"last_command": command})
    try:
        if args.stage == "A":
            from p4_pipeline.runner import run_stage_a

            run_stage_a(force=args.force)
        elif args.stage == "B":
            from p4_pipeline.runner import run_stage_b

            run_stage_b(force=args.force)
        else:
            from p4_pipeline.stats import run_stage_c

            run_stage_c(force=args.force)
    except Exception as exc:
        reason = f"{type(exc).__name__}: {exc}"
        add_unavailable(f"stage_{args.stage}_execution", reason, args.stage)
        checkpoint(
            f"stage_{args.stage}_exception",
            {
                f"stage_{args.stage}": {
                    "last_exception": {
                        "reason": reason,
                        "traceback_tail": traceback.format_exc().splitlines()[-15:],
                    }
                }
            },
        )
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
