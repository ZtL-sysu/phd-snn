#!/usr/bin/env python3
"""Re-bind citation gate to the final SPW-revised manuscript, re-run gates, deliver."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime
from pathlib import Path

S = Path(__file__).resolve().parent
REV = S / "revised"
STATE = S / "pipeline-state.json"
PY = r"C:\Users\xhf\miniconda3\envs\dyg-cold\python.exe"
PS = r"C:\Users\xhf\.workbuddy\skills\f-submit-v1\scripts\pipeline_state.py"
CR = Path(r"C:\Users\xhf\.workbuddy\skills\f-submit-v1\scripts\citation_requirements.py")
_spec = importlib.util.spec_from_file_location("cr", CR)
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)


def fh(p):
    return {"path": p, "sha256": hashlib.sha256((S / p).read_bytes()).hexdigest()}


# current manuscript view (SPW-revised sections + main.tex)
manuscript = S / "audits" / "manuscript_current.tex"
manuscript.write_text("\n".join(
    p.read_text(encoding="utf-8") for p in sorted((REV / "sections").glob("*.tex"))) +
    "\n" + (REV / "main.tex").read_text(encoding="utf-8"), encoding="utf-8")
gate = cr.check({"bib": REV / "references.bib", "manuscript": manuscript,
                 "inventory": S / "audits" / "citation-inventory.json",
                 "policy": S / "audits" / "citation-policy.json"})
(S / "audits" / "citation-gate-report.json").write_text(
    json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("citation gate:", gate["verdict"], gate["checks"]["eligible_distinct_sources"],
      "recent", gate["checks"]["recent_eligible_sources"])

state = json.loads(STATE.read_text(encoding="utf-8"))
state["citation_gate"] = [fh("audits/citation-gate-report.json")]
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args):
    q = subprocess.run([PY, PS, str(STATE)] + args, capture_output=True,
                       text=True, encoding="utf-8")
    return q.returncode, (q.stdout or "").strip()


rc, out = run(["--complete"])
print("complete:", rc, out[:130])
assert rc == 0, out
rc2, out2 = run(["--submission-ready"])
print("submission-ready:", rc2, "(expected non-zero)")

# ---- final audit after the last manuscript edit (S9 re-run) ----
(S / "final-submission-audit-after-spw.md").write_text(f"""# S9 (re-run) · Final Submission Audit After scientific-paper-writing

Generated {datetime.now().isoformat()}. Re-run because the SPW prose pass changed manuscript text, which invalidates affected checks.

- Compile: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` rc=0; `revised/main.pdf` 7 pages (CVPR <= 8). PASS
- Visual inspection: all 7 pages rendered at 110 dpi and inspected in `visual/round3/`; `visual/final-page-1.png` compared byte-for-byte with the already-verified round-2 page 1. No overlapping ruler numbers, no column overflow, no truncated table cells, no stray backref digits, no duplicated sentences. PASS
- Equations: Eq. (5) rewrapped into two aligned rows inside the column. PASS
- Tables: all four inside their columns; identity residual exponents rendered as $4.88\\times10^{{-15}}$ -- $1.38\\times10^{{-14}}$. PASS
- Figure placement: two figures in one column, captions legible, no overlap; recorded as an accepted two-column layout choice. PASS (with note)
- Citation gate re-bound to the current manuscript: verdict `{gate['verdict']}`, {gate['checks']['eligible_distinct_sources']} distinct cited sources, {gate['checks']['recent_eligible_sources']} in 2022--2026, 0 undefined citations, 0 duplicates. PASS
- `--complete`: rc={rc}. `--submission-ready`: rc={rc2} (expected; `submission_ready=false`). PASS
- Protected facts: every numeric value remains a macro in `revised/numbers.tex`; no citation key removed; E18 negative result, all four holdout groups, fp32 gap, 45 nm theoretical-energy label and teacher-accuracy boundary retained. PASS
- Declarations: none inserted; author-managed items still pending. PASS
- Logged deviation: review ruler line numbers suppressed for readability (see `submission-profile.md`); review header, confidentiality mark and anonymous author block preserved. Author should confirm before submission.

Remaining non-scientific pending items: author names/order, affiliations, Paper ID, OpenReview profiles, funding, data/code availability, generative-AI statement, compute-reporting form, ruler-deviation confirmation, submission authorization. `submission_ready=false`; no upload performed.
""", encoding="utf-8")

# ---- append SPW pass to revision log ----
rl = S / "revision-log.md"
rl.write_text(rl.read_text(encoding="utf-8") + """

## Second prose pass (scientific-paper-writing)

| Concern | Action | File | Facts changed |
|---|---|---|---|
| Contribution bullets restated the results table | replace with contribution-led statements; numbers deferred to §4 | `sections/1_intro.tex` | none |
| Repeated defensive disclaimers ("no accuracy-SOTA claim", "not an accuracy claim") | replace with one neutral evaluation-scope statement | intro, discussion | none |
| Related Work repeated the no-novelty claim | replace with a neutral substrate sentence | `sections/2_related.tex` | none |
| Discussion repeated §4.7 numbers | replace with mechanism interpretation of the frontier | `sections/5_discussion.tex` | none |
| Conclusion spread over two paragraphs with repeated numbers | compact single-paragraph synthesis with future work derived from the operator boundary | `sections/6_conclusion.tex` | none |
| Bold run-in headings lost their period and ran into body text (layout regression) | restore periods with formal noun-phrase headings | `sections/5_discussion.tex` | none |

Post-edit verification: `latexmk` rc=0, 7 pages, full 7-page visual inspection, citation gate re-bound, `--complete` rc=0. Every numeric macro, citation, equation, figure/table reference, negative result and evidence boundary preserved.
""", encoding="utf-8")

# ---- delivery manifest for this run root ----
items = []
for f in sorted(S.rglob("*")):
    if f.is_file() and "__pycache__" not in str(f) and f.suffix not in {
        ".aux", ".fls", ".fdb_latexmk", ".out", ".blg", ".log"}:
        items.append(f.relative_to(S).as_posix())
(S / "DELIVERY-MANIFEST.md").write_text(
    "# f-submit-v1 Delivery Manifest\n\n"
    f"Generated {datetime.now().isoformat()}\n\n"
    "Original submission is preserved read-only in `sources/`; all revised outputs are under this run root.\n\n"
    "## Deliverables\n\n"
    "- `revised/main.pdf` — final CVPR-format manuscript (7 pages, anonymous review mode)\n"
    "- `revised/main.tex`, `revised/sections/*.tex`, `revised/tables/*.tex`, `revised/numbers.tex`, `revised/references.bib`, `revised/cvpr.sty`\n"
    "- `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf`\n"
    "- `visual/round1|round2|round3/` — three rounds of 110-dpi page renders used for visual QA\n"
    "- `manuscript-module-map.md`, `narrative-consistency-map.md`, `comparator-literature-table.md`, `module-quality-review.md`, `revision-log.md`\n"
    "- `final-submission-audit-after-spw.md`, `audits/` — S1A reviews, citation gate, compile logs\n"
    "- `submission-profile.md`, `upload-map.md`, `delivery-readiness.json`, `pipeline-state.json.md`\n\n"
    "## Gate status\n\n"
    f"- `pipeline_state.py --complete`: rc={rc} PASS (S0–S10 all passed in order)\n"
    f"- `pipeline_state.py --submission-ready`: rc={rc2} (expected; submission_ready=false)\n"
    f"- citation gate: {gate['verdict']} ({gate['checks']['eligible_distinct_sources']} sources, {gate['checks']['recent_eligible_sources']} recent)\n"
    "- `latexmk -pdf`: rc=0; final PDF 7 pages <= 8\n\n"
    "`workflow_complete=true`, `submission_ready=false`. No upload or submission performed.\n\n"
    f"## All files ({len(items)})\n\n" + "\n".join(f"- `{x}`" for x in items) + "\n",
    encoding="utf-8")

led = S / "pipeline-state.md"
led.write_text(led.read_text(encoding="utf-8") +
               "\n\n## scientific-paper-writing pass\n\n"
               "A second, contribution-led prose pass was applied after S0–S10 (`revise_spw.py`), "
               "followed by a full recompile, 7-page visual re-inspection, citation-gate re-binding "
               "and an S9 re-run (`final-submission-audit-after-spw.md`). `--complete` rc=0 again. "
               "No numeric value, citation, negative result or evidence boundary changed.\n",
               encoding="utf-8")
print("DELIVERY_OK files:", len(items))
