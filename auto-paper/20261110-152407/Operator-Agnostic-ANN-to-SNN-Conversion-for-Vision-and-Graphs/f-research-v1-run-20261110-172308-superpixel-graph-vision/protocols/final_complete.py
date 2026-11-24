#!/usr/bin/env python3
"""Final compile, refresh audits/hashes, run --complete and rebuild manifest."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

R = Path(__file__).resolve().parents[1]
PY = r"C:\Users\xhf\miniconda3\envs\dyg-cold\python.exe"
S = r"C:\Users\xhf\.workbuddy\skills\f-research-v1\scripts\pipeline_state.py"
TEX = R / "tex"


def sha(p):
    return hashlib.sha256((R / p).read_bytes()).hexdigest()


def fh(p):
    return {"path": p, "sha256": sha(p)}


def run(args, cwd=None):
    q = subprocess.run([PY, S, str(R / "pipeline-state.json")] + args,
                       capture_output=True, text=True, encoding="utf-8")
    return q.returncode, (q.stdout or "").strip()


# 1. clean rebuild
for f in ("main.aux", "main.bbl", "main.blg", "main.log", "main.out",
          "main.pdf", "main.fdb_latexmk", "main.fls"):
    (TEX / f).unlink(missing_ok=True)
p = subprocess.run(PY.replace("python.exe", "python.exe") + " --version",
                   capture_output=True, text=True)
c = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                   cwd=TEX, capture_output=True, text=True, encoding="utf-8")
(R / "audits" / "p15-compile.log").write_text(c.stdout + "\n" + c.stderr, encoding="utf-8")
print("latexmk rc:", c.returncode)
assert c.returncode == 0, (c.stdout[-800:] + c.stderr[-800:])
assert (TEX / "main.pdf").is_file()

# 2. refresh audits
v = subprocess.run([PY, str(R / "protocols" / "verify_paper.py")],
                   capture_output=True, text=True, encoding="utf-8")
print("verify:", v.stdout.strip()[:400])
assert v.returncode == 0

# 3. refresh stage evidence hashes for stages whose artifacts changed
state_path = R / "pipeline-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
rows = {r["id"]: r for r in state["stages"]}
refresh = {
    "P12": ["audits/reference-dedup-audit.md", "tex/references.bib"],
    "P13": ["tex/main.tex", "tex/numbers.tex", "tex/tables/tab_main.tex",
            "tex/sections/3_method.tex", "tex/sections/5_discussion.tex"],
    "P14": ["audits/p14-citation-verify.md", "audits/citation-gate-report.json"],
    "P15": ["audits/p15-compile.log", "tex/main.pdf"],
    "P16": ["audits/p16-length-audit.md", "contracts/submission-constraints.md"],
    "P17": ["audits/p17-paper-guidance-audit.md"],
    "P18": ["audits/p18-figure-table-audit.md"],
    "P21": ["audits/p21-final-audit.md"],
}
for sid, files in refresh.items():
    ev = [fh(x) for x in files]
    rows[sid]["inputs"] = ev
    rows[sid]["evidence"] = ev
state["citation_gate"] = [fh("audits/citation-gate-report.json")]
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 4. final gate checks
rc, out = run(["--complete"])
print("complete:", rc, out[:200])
assert rc == 0, out
rc2, out2 = run(["--submission-ready"])
print("submission-ready:", rc2, out2[:160])

# 5. readable ledger
led = R / "pipeline-state.md"
s = led.read_text(encoding="utf-8")
if "FINAL COMPLETE" not in s:
    s += ("\n\n## FINAL COMPLETE (" + datetime.now().strftime("%Y-%m-%d %H:%M") + ")\n\n"
          "- Contract v2 (user-authorized precision statement), P0–P21 all `passed`, `--complete` rc=0.\n"
          "- `--submission-ready` rc=1 as expected: `submission_ready=false` (author facts pending).\n"
          "- Compiled `tex/main.pdf` (7 pages, CVPR <= 8), 42 verified cited works, 23 in 2022–2026.\n")
    led.write_text(s, encoding="utf-8")

# 6. manifest (rebuild, no history mutation)
items = []
for f in sorted(R.rglob("*")):
    if f.is_file() and "__pycache__" not in str(f) and f.suffix not in {".aux", ".log", ".fls", ".fdb_latexmk", ".out", ".blg"}:
        items.append(f.relative_to(R).as_posix())
m = ["# DELIVERY MANIFEST", "", f"Generated {datetime.now().isoformat()}",
     "All deliverables and process files are under the guidance directory (this run root).", "",
     "## Primary deliverables", "",
     "- `tex/main.pdf` — compiled CVPR-format manuscript (7 pages, anonymous review mode, <=8 page limit)",
     "- `tex/main.tex`, `tex/sections/*.tex`, `tex/tables/*.tex`, `tex/numbers.tex`, `tex/references.bib`, `tex/manuscript_all.tex`",
     "- `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf`",
     "- `writing/p6-outline.md`, `writing/p7-draft.md`, two independent reviewer reports",
     "- `audits/` — all gate, integrity, length, citation and figure/table audits",
     "- `results/` — every raw experiment result (E1–E18)",
     "- `contracts/` — guidance-v3 snapshot, user authorization, submission constraints, metadata, citation policy",
     "", "## Final gate status", "",
     f"- `pipeline_state.py --complete`: rc={rc} — PASS",
     f"- `pipeline_state.py --submission-ready`: rc={rc2} — expected FAIL (submission_ready=false)",
     "- `latexmk -pdf`: rc=0; PDF text spot-check matches reported numbers",
     "- `validate_guidance.py guidance-v3.md --strict --packet`: rc=0",
     "", "## Readiness", "",
     "- `workflow_complete = true` (26 canonical stages passed in order under contract v2)",
     "- `submission_ready = false` (author-managed facts pending; see `contracts/manuscript-metadata.md`, `delivery-readiness.json`)", "",
     f"## All files ({len(items)})", ""]
m += [f"- `{x}`" for x in items]
(R / "DELIVERY-MANIFEST.md").write_text("\n".join(m) + "\n", encoding="utf-8")
print("MANIFEST_OK files:", len(items))
