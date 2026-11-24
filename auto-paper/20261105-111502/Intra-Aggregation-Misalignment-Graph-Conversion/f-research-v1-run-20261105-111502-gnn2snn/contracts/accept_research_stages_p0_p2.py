"""Record f-research-v1 stages P0..P2 as passed, in canonical order (P3 stays pending)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "pipeline-state.json"
VALIDATOR = Path("C:/Users/xhf/.workbuddy/skills/f-research-v1/scripts/pipeline_state.py")

TO_PASS = ["P0", "P1", "P1A", "P1B", "P2"]

CONTRACT_FILES = [
    "contracts/execution-contract-v1.md",
    "contracts/guidance.snapshot.md",
    "contracts/parent-execution-contract-v1.md",
    "contracts/parent-execution-contract-v1-addendum-C8.md",
    "contracts/agent_prompt_v2_ICML25.snapshot.md",
]

INPUTS = {
    "P0": ["contracts/guidance.snapshot.md", "contracts/execution-contract-v1.md"],
    "P1": ["contracts/guidance.snapshot.md", "contracts/ccfa-startup-packet/startup-decision.md"],
    "P1A": ["contracts/ccfa-startup-packet/claim-evidence-matrix.md",
            "contracts/ccfa-startup-packet/feasibility-contract.json"],
    "P1B": ["contracts/ccfa-startup-packet/idea-red-team-review.md",
            "audits/strong-result-feasibility-lock.md"],
    "P2": ["protocols/protocol.md", "registry/registry.md", "audits/reaccepted-assets.md"],
}

EVIDENCE = {
    "P0": ["pipeline-state.md", "audits/path-manifest.md", "contracts/execution-contract-v1.md"],
    "P1": ["audits/guidance-validation.md", "contracts/guidance.snapshot.md"],
    "P1A": ["audits/strong-result-feasibility-lock.md",
            "contracts/ccfa-startup-packet/strong-result-feasibility-contract.md"],
    "P1B": ["audits/ccfa-pre-experiment-review.md",
            "audits/ccfa-pre-experiment-integrity.md", "audits/concern-to-action-ledger.md"],
    "P2": ["protocols/protocol.md", "audits/p2-environment-check.md",
           "notes/S0_foundation.md", "results/wp0_repro.json", "registry/results.csv"],
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bind(rel: str) -> dict:
    path = ROOT / rel
    if not path.is_file() or not path.stat().st_size:
        raise SystemExit("missing or empty artifact: " + rel)
    return {"path": rel, "sha256": sha(path)}


def run(*flags: str) -> str:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(STATE), *flags],
        capture_output=True, text=True, check=False,
    )
    return "rc=" + str(result.returncode) + " " + (result.stdout + result.stderr).strip()


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    state["contract"] = [bind(rel) for rel in CONTRACT_FILES]
    state["readiness"] = [bind("contracts/delivery-readiness.snapshot.json")]
    state["history"] = []
    rows = {row["id"]: row for row in state["stages"]}
    order = [row["id"] for row in state["stages"]]
    if order[: len(TO_PASS)] != TO_PASS:
        raise SystemExit("unexpected stage order: " + str(order[:6]))
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    transcript = ["# f-research-v1 ledger validation transcript (P0-P2)", ""]
    for stage in TO_PASS:
        before = run("--before", stage)
        transcript.append("`--before " + stage + "`: " + before)
        if "rc=0" not in before:
            raise SystemExit("predecessor check failed at " + stage + "\n" + before)
        row = rows[stage]
        row["status"] = "passed"
        row["contract_version"] = "v1"
        row["inputs"] = [bind(rel) for rel in INPUTS[stage]]
        row["evidence"] = [bind(rel) for rel in EVIDENCE[stage]]
        row["gate_verdict"] = "pass"
        row["gate_report"] = "Recorded in " + EVIDENCE[stage][0]
        state["history"].append({"action": "pass", "stage": stage})
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        after = run()
        transcript.append("after `" + stage + "`: " + after)
        if "rc=0" not in after:
            raise SystemExit("post-stage validation failed at " + stage + "\n" + after)

    p3 = run("--before", "P3")
    transcript.append("`--before P3`: " + p3)
    transcript.append("")
    (ROOT / "audits" / "ledger-transcript-p0-p2.md").write_text(
        "\n".join(transcript) + "\n", encoding="utf-8"
    )
    print("\n".join(transcript[-3:]))


if __name__ == "__main__":
    main()
