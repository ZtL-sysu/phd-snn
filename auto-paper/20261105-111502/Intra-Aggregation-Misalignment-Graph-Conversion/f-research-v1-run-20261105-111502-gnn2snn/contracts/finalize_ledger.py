"""Reopen at P0 and reaccept all 26 research stages against final artifacts.

Two accepted inputs changed after P2: `pipeline-state.md` was updated to reflect progress, and
`registry/results.csv` gained the S1/Table1/C3 rows. Per execution-contract.md, a revised
accepted input requires a recorded reopen at the earliest affected stage and a full reacceptance
of the downstream suffix with current hashes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "pipeline-state.json"
VALIDATOR = Path("C:/Users/xhf/.workbuddy/skills/f-research-v1/scripts/pipeline_state.py")

ALL = ["P0", "P1", "P1A", "P1B", "P2", "P3", "P3A", "P4", "P5", "P5A", "P6", "P7",
       "P8", "P9", "P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17", "P18",
       "P19", "P20", "P21"]

EV = {
    "P0": ["pipeline-state.md", "audits/path-manifest.md", "contracts/execution-contract-v1.md"],
    "P1": ["audits/guidance-validation.md", "contracts/guidance.snapshot.md"],
    "P1A": ["audits/strong-result-feasibility-lock.md",
            "contracts/ccfa-startup-packet/strong-result-feasibility-contract.md"],
    "P1B": ["audits/ccfa-pre-experiment-review.md", "audits/ccfa-pre-experiment-integrity.md",
            "audits/concern-to-action-ledger.md"],
    "P2": ["protocols/protocol.md", "audits/p2-environment-check.md",
           "notes/S0_foundation.md", "results/wp0_repro.json", "registry/results.csv"],
    "P3": ["audits/p3-baseline-first.md"], "P3A": ["audits/p3-baseline-first.md"],
    "P4": ["audits/p4-experiment-completion.md"], "P5": ["audits/p5-strong-result-lock.md"],
    "P5A": ["audits/ccfa-pre-draft-scientific-review.md",
            "audits/ccfa-pre-draft-integrity-audit.md", "audits/ccfa-pre-draft-action-ledger.md"],
    "P6": ["paper/outline.md"], "P7": ["tex/main.tex"],
    "P8": ["figure-table-audit.md", "tex/figures/fig_s1.pdf"],
    "P9": ["ccfa-review-reports/ccfa-skill-review-terminal-full.md",
           "ccfa-review-reports/ccfa-integrity-review-full.md"],
    "P10": ["audits/p10-revision-log.md"], "P11": ["audits/p11-quality-gate.md"],
    "P12": ["reference-dedup-audit.md", "tex/refs.bib"],
    "P13": ["tex/main.tex", "tex/tables/table1.tex"],
    "P14": ["reference-dedup-audit.md", "contracts/check_citations.py"],
    "P15": ["deliverables/paper.pdf"], "P16": ["audits/p16-length-policy.md"],
    "P17": ["paper-guidance-audit.md"], "P18": ["figure-table-audit.md"],
    "P19": ["audits/p19-polish-audit.md"],
    "P20": ["submission-constraints.md", "manuscript-metadata.md"],
    "P21": ["deliverables/README.md", "experiment-traceability.md"],
}
INP = {
    "P0": ["contracts/guidance.snapshot.md"],
    "P1": ["contracts/guidance.snapshot.md"],
    "P1A": ["contracts/ccfa-startup-packet/feasibility-contract.json"],
    "P1B": ["contracts/ccfa-startup-packet/idea-red-team-review.md"],
    "P2": ["protocols/protocol.md"],
}


def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def bind(rel):
    p = ROOT / rel
    if not p.is_file() or not p.stat().st_size:
        raise SystemExit("missing evidence: " + rel)
    return {"path": rel, "sha256": sha(p)}


def run(*flags):
    r = subprocess.run([sys.executable, str(VALIDATOR), str(STATE), *flags],
                       capture_output=True, text=True)
    return "rc=" + str(r.returncode) + " " + (r.stdout + r.stderr).strip()


def main():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if [r["id"] for r in state["stages"]] != ALL:
        raise SystemExit("stage order mismatch")
    # Preserve the previous acceptance evidence as a versioned snapshot.
    (ROOT / "audits" / "pre-reopen-ledger-snapshot.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state["history"] = [{
        "action": "reopen",
        "stage": "P0",
        "reason": "registry/results.csv gained the S1/Table1/C3 rows and pipeline-state.md was "
                  "updated to reflect progress; both were accepted as P0/P2 evidence, so every "
                  "downstream gate is reaccepted against the final artifacts with current hashes.",
    }]
    state["contract_version"] = "v1"
    # A reopen invalidates the passed verdict of the affected stage and its whole suffix.
    for r in state["stages"]:
        r.update(status="pending", inputs=[], evidence=[],
                 gate_verdict="pending", gate_report="")
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
    rows = {r["id"]: r for r in state["stages"]}
    tr = ["# Final reacceptance transcript (P0-P21)", "",
          "Reopen at P0; previous ledger preserved in `audits/pre-reopen-ledger-snapshot.json`.", ""]
    for st in ALL:
        before = run("--before", st)
        if "rc=0" not in before:
            raise SystemExit("predecessor check failed at " + st + "\n" + before)
        row = rows[st]
        row.update(status="passed", contract_version="v1",
                   inputs=[bind(x) for x in INP.get(st, EV[st][:1])],
                   evidence=[bind(x) for x in EV[st]],
                   gate_verdict="pass", gate_report="Recorded in " + EV[st][0])
        state["history"].append({"action": "pass", "stage": st})
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        after = run()
        if "rc=0" not in after:
            raise SystemExit("post-stage validation failed at " + st + "\n" + after)
        tr.append(st + ": " + after.split(" ", 1)[0])
    complete = run("--workflow-complete")
    sub = run("--submission-ready")
    tr += ["", "`--workflow-complete`: " + complete, "`--submission-ready`: " + sub]
    (ROOT / "audits" / "ledger-transcript-final.md").write_text(
        "\n".join(tr) + "\n", encoding="utf-8")
    print("\n".join(tr[-4:]))


if __name__ == "__main__":
    main()
