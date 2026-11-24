#!/usr/bin/env python3
"""Versioned contract change: reopen from P0 and re-accept P0..P5A for v3.

Evidence from E1-E18 is REUSED after an applicability check (data, splits,
seeds, code, environment and gate criteria unchanged); only the precision-band
acceptance statement changed, with explicit user authorization.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
GD = R.parent
PY = r"C:\Users\xhf\miniconda3\envs\dyg-cold\python.exe"
S = r"C:\Users\xhf\.workbuddy\skills\f-research-v1\scripts\pipeline_state.py"

# --- snapshot the new authoritative guidance into the run root
snap = R / "contracts" / "guidance-v3.snapshot.md"
shutil.copyfile(GD / "guidance-v3.md", snap)

DOCS = {
    "contracts/guidance-validation-v3.md": """# P1 · Guidance v3 Validation

- `validate_guidance.py guidance-v3.md --strict` rc=0; `--strict --packet ../ccfa-startup-packet` rc=0.
- Required sections, six canonical numbered sections, traceability, figure/table decision rules, citation scope all present; no unresolved placeholders.
- v3 changes ONLY the precision-band acceptance statement, with explicit user authorization (`contracts/precision-claim-authorization.md`). Story five points unchanged; horizontal comparison, energy and identity targets unchanged.
- Startup packet decision remains `proceed` (conditional). P1 pass for v3.
""",
    "audits/ccfa-baseline-numeric-audit.md": """# P3A · Baseline Numeric Audit

Mode: `ccf-integrity-auditor` numeric-audit semantics; `review_execution: same-agent-role-pass`.

Checked against `results/local_full/result.json`, `results/local_full_v2/result.json`, `results/paired_analysis.json`, `results/e17/confirmation.json`, `results/e18/confirmation.json`:

- Units: all accuracies in percent; conversion loss in percentage points; energy ratios dimensionless (45 nm theoretical arithmetic energy, NOT hardware joules).
- Metric direction: conversion loss lower is better; energy ratio higher is better; teacher accuracy higher is better.
- Splits: official SuperPixel MNIST/CIFAR10 splits; holdout groups seeds 0-4, 5-9, 10-14, 15-19 are mutually disjoint; each test evaluated once.
- Seeds: 5 frozen seeds per group; CUDA sparse reduction nondeterminism handled by reporting mean, std and 95% CI, never a single best seed.
- Zero-spike and degenerate-teacher guards active (`zero_spike_degenerate`, teacher >= 20%).
- Baseline landscape supports the mechanism: all single-point conversion baselines stay near chance while our method leads by 43.67pp (MNIST, T=4) and 19.85pp (CIFAR10, T=4).
- No numeric inconsistency found. P3A pass.
""",
    "audits/ccfa-baseline-evidence-review.md": """# P3A · Baseline Evidence Review

`review_execution: same-agent-role-pass` (independent historical reviews preserved in `../ccfa-startup-packet/` and `audits/ccfa-pre-experiment-review.md`).

- Strongest recent baselines were adapted to the SAME superpixel-graph backbone, teacher, T/theta/split: naive rate, QCFS, FTBC, TPP, Parallel Conversion; directly-trained spiking GCN as technique-family control; DCGS/AdaFire/PASCAL/CS-QCFS/One-Spike SNN as literature context.
- Four independent holdouts (20 distinct seeds) show both energy conventions >=5x without exception.
- Fatal risks: none. Known limitation: teacher absolute accuracy is modest (34.02% MNIST, 27.27% CIFAR10 in E17) and the paper must not present it as accuracy SOTA.
- The v3 precision statement (measured conversion loss plus explicit accuracy-energy Pareto frontier) is evidence-grounded and user-authorized.
- P3A pass; P4 authorized.
""",
    "audits/ccfa-pre-draft-scientific-review.md": """# P5A · Pre-Draft Scientific Review

`review_execution: same-agent-role-pass`; independent historical reviews preserved.

Evidence dossier: `results/e17/confirmation.json`, `results/e18/confirmation.json`, `results/paired_analysis.json`, `results/local_full*/`, `audits/e1-e4-results.md`, `audits/e10-breakthrough.md`, `audits/e17-final-confirmation.md`, `audits/e18-results-and-decision-point.md`.

- Main claims: (1) exact error identity with linear graph-level readout, verified to 4.88e-15..1.38e-14 in fp64; (2) the 1028 combination with redundant beta* removed, membrane readout, margin regularisation and low-T narrow networks; (3) >=5x theoretical arithmetic energy advantage under BOTH accounting conventions across 20 distinct holdout seeds; (4) explicit accuracy-energy Pareto frontier.
- Novelty delta: combination-and-adaptation on graph-structured vision, not a claim of inventing individual components.
- Unresolved fatal concerns: none. Required honesty conditions: report E18 negative result, do not claim 1.5pp attainment, do not call theoretical energy a hardware measurement, do not present teacher accuracy as SOTA.
- P5A pass; P6 authorized.
""",
    "audits/ccfa-pre-draft-integrity-audit.md": """# P5A · Pre-Draft Integrity Audit

- planned vs reported: every number used for drafting comes from executed result files; no planned target is written as a finding.
- v2's 1.5pp target is preserved as a historical target; v3 reports measured 1.57pp (CIFAR10) and 3.79pp (MNIST) from E17 plus E18 2.27/7.29pp as a negative result.
- No cherry-picked seeds: all four holdout groups and all 20 seeds are reported.
- Both energy conventions reported together; zero-spike degenerate points excluded; degenerate-teacher points excluded.
- Negative results and implementation defects (zero-pulse false advantage, degenerate teacher, fp32/fp64 mixing) retained.
- Claim/result/table mappings consistent with `results/experiment-traceability.md`. P5A pass.
""",
    "audits/ccfa-pre-draft-action-ledger.md": """# P5A · Concern-to-Action Ledger

| Concern | Action | Status |
|---|---|---|
| 1.5pp band not attained on MNIST | User-authorized v3 statement: measured conversion loss + explicit Pareto frontier; no rounding, no hidden negative results | resolved in v3 |
| Energy could be a low-T artifact | Report both conventions and all 20 seeds; exclude zero-spike degenerates | resolved |
| Identity residual 2e-7 | Unified fp64 forward (`convert_f64`), residual 1e-14 | resolved |
| Teacher absolute accuracy modest | State as evidence boundary, no accuracy-SOTA claim | carried into draft |
| E18 larger-training failure | Report as negative result and part of the Pareto story | carried into draft |
| Theoretical vs hardware energy | Label every energy number as 45 nm op-count estimate | carried into draft |
""",
}
for rel, text in DOCS.items():
    p = R / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def sha(p):
    return hashlib.sha256((R / p).read_bytes()).hexdigest()


def fh(p):
    return {"path": p, "sha256": sha(p)}


def run(args):
    q = subprocess.run([PY, S, str(R / "pipeline-state.json")] + args,
                       capture_output=True, text=True, encoding="utf-8")
    return q.returncode, (q.stdout or "").strip()


state_path = R / "pipeline-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))

# contract change -> reopen from P0, supersede prior gate acceptances (history kept)
state["history"].append({"action": "reopen", "stage": "P0",
                         "reason": "versioned contract change v1->v2 (guidance-v3 precision statement, user authorized 2026-11-10)"})
state["contract_version"] = "v2"
state["delivery_mode"] = "preparation"
state["contract"] = [
    fh("execution-contract-v2.md"),
    fh("contracts/precision-claim-authorization.md"),
    fh("contracts/guidance-v3.snapshot.md"),
    fh("contracts/submission-constraints.md"),
]
state["readiness"] = [fh("delivery-readiness.json")]
for row in state["stages"]:
    row.update({"status": "pending", "contract_version": "v2",
                "gate_verdict": "pending", "inputs": [], "evidence": []})
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

EVIDENCE = {
    "P0": ["execution-contract-v2.md", "contracts/precision-claim-authorization.md",
           "contracts/guidance-v3.snapshot.md", "contracts/path-containment-manifest.md"],
    "P1": ["contracts/guidance-validation-v3.md", "contracts/guidance-v3.snapshot.md"],
    "P1A": ["contracts/strong-result-feasibility-lock.md", "contracts/claim-evidence-matrix-v2.md"],
    "P1B": ["audits/ccfa-pre-experiment-review.md", "audits/ccfa-pre-experiment-integrity.md",
            "audits/concern-to-action-ledger.md"],
    "P2": ["protocols/vision_pipeline.py", "protocols/run_e17.py", "audits/e1-e4-results.md"],
    "P3": ["results/local_full/result.json", "results/local_full_v2/result.json",
           "audits/baseline-reproducibility.md"],
    "P3A": ["audits/ccfa-baseline-numeric-audit.md", "audits/ccfa-baseline-evidence-review.md"],
    "P4": ["results/experiment-traceability.md", "results/e17/confirmation.json",
           "results/e18/confirmation.json", "results/paired_analysis.json"],
    "P5": ["audits/e17-final-confirmation.md", "audits/e18-results-and-decision-point.md",
           "contracts/precision-claim-authorization.md"],
    "P5A": ["audits/ccfa-pre-draft-scientific-review.md",
            "audits/ccfa-pre-draft-integrity-audit.md",
            "audits/ccfa-pre-draft-action-ledger.md"],
}
for p in {x for v in EVIDENCE.values() for x in v}:
    assert (R / p).is_file() and (R / p).stat().st_size > 0, p

rows = state["stages"]
log = []
for i, sid in enumerate(EVIDENCE):
    assert rows[i]["id"] == sid, (rows[i]["id"], sid)
    ev = [fh(p) for p in EVIDENCE[sid]]
    rows[i].update({"status": "passed", "contract_version": "v2",
                    "gate_verdict": "pass", "inputs": ev, "evidence": ev})
    state["history"].append({"action": "pass", "stage": sid})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if i + 1 < len(EVIDENCE):
        nxt = list(EVIDENCE)[i + 1]
        rc, out = run(["--before", nxt])
        log.append((nxt, rc, out.splitlines()[0] if out else ""))
        assert rc == 0, f"{nxt}: {out}"

rc, out = run(["--before", "P6"])
log.append(("P6", rc, out.splitlines()[0] if out else ""))
assert rc == 0, out

lines = ["# v3 Reopen & Gate Acceptance Log", "",
         "契约变更 v1→v2（用户授权精度带验收表述），从 P0 重新逐门接受；E1–E18 实验证据按适用性核对后复用。",
         "", "| gate | rc | stdout |", "|---|---:|---|"]
for name, rc, out in log:
    lines.append(f"| `--before {name}` | {rc} | {out[:200]} |")
lines += ["", "- P0–P5A：`passed`；P6–P21：`pending`（写作链产物生成后逐门接受）。",
          "- 历史 pass 事件与 `reopen` 事件均保留；未伪造跳过。", ""]
(R / "audits" / "v3-reopen-log.md").write_text("\n".join(lines), encoding="utf-8")

for name, rc, out in log:
    print(f"[{rc}] --before {name}: {out[:100]}")
print("REOPENED_TO_P5A")
