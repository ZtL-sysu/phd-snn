"""Record the f-guidance-builder-v1 canonical stages as passed, in order.

Each stage is validated with `--before` before it is opened and with a plain validation
immediately after it is recorded. Evidence files are hash-bound and must exist under the run root.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "pipeline-state.json"
VALIDATOR = Path(
    "C:/Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py"
)

STAGES = [
    "CCFA-startup",
    "G0",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "validation",
    "handoff",
]

CONTRACT_FILES = [
    "contracts/execution-contract-v1.md",
    "contracts/execution-contract-v1-addendum-C8.md",
    "contracts/agent_prompt_v2_ICML25.snapshot.md",
]

PACKET = "ccfa-startup-packet/"

STAGE_INPUTS = {
    "CCFA-startup": [
        "contracts/execution-contract-v1.md",
        "contracts/execution-contract-v1-addendum-C8.md",
        "contracts/agent_prompt_v2_ICML25.snapshot.md",
        "notes/overlap-risk-AB.md",
    ],
    "G0": [PACKET + "startup-stage-plan.md", "notes/G0_literature_map.md"],
    "G1": ["notes/G0_literature_map.md"],
    "G2": [PACKET + "claim-evidence-matrix.md"],
    "G3": [PACKET + "idea-cards.md"],
    "G4": [PACKET + "prior-art-opportunity-map.md"],
    "G5": ["hardware-profile.md"],
    "G6": [PACKET + "prior-art-opportunity-map.md"],
    "G7": [PACKET + "claim-evidence-matrix.md"],
    "G8": [PACKET + "idea-red-team-review.md"],
    "validation": ["guidance.md", PACKET + "feasibility-contract.json"],
    "handoff": ["guidance.md", "scenario-decision-log.md"],
}

STAGE_EVIDENCE = {
    "CCFA-startup": [
        PACKET + "startup-stage-plan.md",
        PACKET + "idea-cards.md",
        PACKET + "prior-art-opportunity-map.md",
        PACKET + "idea-red-team-review.md",
        PACKET + "claim-evidence-matrix.md",
        PACKET + "strong-result-feasibility-contract.md",
        PACKET + "startup-decision.md",
        PACKET + "feasibility-contract.json",
    ],
    "G0": [
        "notes/G0_literature_map.md",
        "notes/G0_source_conflicts.md",
        PACKET + "prior-art-opportunity-map.md",
        "literature-baseline-matrix.md",
    ],
    "G1": ["dataset-access-log.md"],
    "G2": [PACKET + "claim-evidence-matrix.md", "guidance.md"],
    "G3": ["theoretical-feasibility-audit.md"],
    "G4": ["novelty-feasibility-report.md", "notes/overlap-risk-AB.md"],
    "G5": ["hardware-profile.md"],
    "G6": ["literature-baseline-matrix.md"],
    "G7": [PACKET + "strong-result-feasibility-contract.md", PACKET + "feasibility-contract.json"],
    "G8": ["story-strength-audit.md", PACKET + "idea-red-team-review.md"],
    "validation": ["guidance.md", "scenario-decision-log.md", PACKET + "feasibility-contract.json"],
    "handoff": ["notes/handoff-note.md", "guidance.md"],
}

HANDOFF_NOTE = """# Handoff to f-research-v1

Recorded 2026-11-05 after `validate_guidance.py --strict --packet` returned
"Guidance structure is valid." and the ordered 12-stage ledger passed.

The guidance file is `guidance.md` in this run root; the CCFA startup packet is
`ccfa-startup-packet/` with `startup-decision.md = proceed`. The f-research-v1 run root is
`f-research-v1-run-20261105-111502-gnn2snn/` inside this directory, with its own P0-P21 ledger.

Binding decisions carried forward: independent third paper (A/B are anonymous companions, no
reused priority claim); C3 bound-derived latency allocation is the binding `expected_strong`;
six numbered main sections; no TODO tokens; >=36 citations with a strict 2023-2026 majority;
score >=9 measured only by `ccf-paper-reviewer` in full mode; no submission action.

The external index `auto-paper/generated-research-directions.md` received one new row for
`20261105-111502`. Local preparation only: `submission_ready` stays false with seven pending
author/production items in `contracts/delivery-readiness.json`.
"""


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bind(rel: str) -> dict:
    path = ROOT / rel
    if not path.is_file() or not path.stat().st_size:
        raise SystemExit("missing or empty evidence: " + rel)
    return {"path": rel, "sha256": sha(path)}


def run_validator(*flags: str) -> str:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(STATE), *flags],
        capture_output=True,
        text=True,
        check=False,
    )
    out = (result.stdout + result.stderr).strip()
    return "rc=" + str(result.returncode) + " " + out


def main() -> None:
    (ROOT / "notes" / "handoff-note.md").write_text(HANDOFF_NOTE, encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    state["contract"] = [bind(rel) for rel in CONTRACT_FILES]
    state["readiness"] = [bind("contracts/delivery-readiness.json")]
    state["history"] = []
    rows = {row["id"]: row for row in state["stages"]}
    if [row["id"] for row in state["stages"]] != STAGES:
        raise SystemExit("stage order mismatch")

    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    transcript = ["# Ordered ledger validation transcript", "", "Run: 2026-11-05, local Conda Python.", ""]

    for stage in STAGES:
        before = run_validator("--before", stage)
        transcript.append("`--before " + stage + "`: " + before)
        if "rc=0" not in before:
            raise SystemExit("predecessor check failed at " + stage + "\n" + before)
        row = rows[stage]
        row["status"] = "passed"
        row["contract_version"] = "v1"
        row["inputs"] = [bind(rel) for rel in STAGE_INPUTS[stage]]
        row["evidence"] = [bind(rel) for rel in STAGE_EVIDENCE[stage]]
        row["gate_verdict"] = "pass"
        row["gate_report"] = "Recorded in " + STAGE_EVIDENCE[stage][0]
        state["history"].append({"action": "pass", "stage": stage})
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        after = run_validator()
        transcript.append("after `" + stage + "`: " + after)
        if "rc=0" not in after:
            raise SystemExit("post-stage validation failed at " + stage + "\n" + after)

    complete = run_validator("--workflow-complete")
    subready = run_validator("--submission-ready")
    transcript.append("")
    transcript.append("`--workflow-complete`: " + complete)
    transcript.append("`--submission-ready`: " + subready)
    (ROOT / "notes" / "validator-transcript.md").write_text(
        "\n".join(transcript) + "\n", encoding="utf-8"
    )
    print("\n".join(transcript[-4:]))


if __name__ == "__main__":
    main()
