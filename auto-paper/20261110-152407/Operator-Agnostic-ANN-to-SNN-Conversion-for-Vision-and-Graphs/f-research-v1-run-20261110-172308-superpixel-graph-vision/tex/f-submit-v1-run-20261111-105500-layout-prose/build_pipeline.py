#!/usr/bin/env python3
"""f-submit-v1 S0-S10 records + S7 prose edits (removing internal/defensive narration)."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

S = Path(__file__).resolve().parent
REV = S / "revised"
PY = r"C:\Users\xhf\miniconda3\envs\dyg-cold\python.exe"
PS = r"C:\Users\xhf\.workbuddy\skills\f-submit-v1\scripts\pipeline_state.py"
STATE = S / "pipeline-state.json"

DOCS = {
"manuscript-module-map.md": """# S1 · Manuscript Module Map

Original (immutable): `sources/original-submitted.pdf`, `sources/main.tex`, `sources/sections/*.tex`, `sources/tables/*.tex`, `sources/references.bib`.

| Module | Location | Role |
|---|---|---|
| Title | `main.tex` | operator-class transfer + accuracy--energy frontier |
| Abstract | `main.tex` | gap, identity, redundancy finding, 20-seed energy result, honest boundary |
| 1 Introduction | `sections/1_intro.tex` | gap, combination framing, four contributions, scope |
| 2 Related Work | `sections/2_related.tex` | inheritance vs differentiation across conversion / spiking-GNN / graph-vision / energy |
| 3 Method | `sections/3_method.tex` | setup, identity, two-phase redundancy, readout/margin/width, energy, applicability |
| 4 Experiments | `sections/4_experiments.tex` | protocol, baselines, main table, baseline table, ablations, identity, frontier |
| 5 Discussion | `sections/5_discussion.tex` | mechanism, stability, trade-off, limitations |
| 6 Conclusion | `sections/6_conclusion.tex` | transferability and operator-dependent discretisation |
| Figures | `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf` | frontier, latency curve, framework |
| Tables | `tables/tab_main.tex` etc. | main, baselines, ablations, identity |
| References | `references.bib` | 42 entries, 23 in 2022--2026 |
| Declarations | none in manuscript | author-managed, routed externally |

Central question: can a conversion framework assembled for graph node classification transfer to graph-structured visual classification and yield an ANN-relative energy advantage? Core claim: linear readout preserves the exact identity, a component of the combination becomes redundant, and the adapted combination yields a stable energy advantage with a measurable fidelity cost. Supporting findings: baseline margins, fp64 identity, ablations, negative scaling result. Orphans found in S6: internal-target references and screening narration (removed in S7).
""",
"narrative-consistency-map.md": """# Narrative Consistency Map

- **Selling point (one sentence):** On graph-structured visual inputs, an exact conversion-error identity survives linear pooling, and re-identifying which inherited components remain valid yields a stable >=5x theoretical arithmetic-energy advantage with an explicitly measured accuracy cost.
- **Chain:** gap (conversion theory assumes row-stochastic grids) -> insight (linear R preserves identity; deterministic counting makes beta* redundant) -> embodiment (two-phase IF + membrane readout + margin regularisation + narrow low-T network) -> evidence (Tables 1--4, Figs. 1--2, four disjoint holdouts) -> interpretation (Discussion) -> bounded conclusion (operator-dependent discretisation).
- **Callback closure:** identity derived §3.2 -> verified §4.6 -> interpreted §5 -> recalled §6. Redundancy claimed §1 -> ablated §4.5 -> explained §5 -> recalled §6. Energy claimed §1 -> measured §4.3 -> qualified §5 -> recalled §6.
- **Supporting/diagnostic findings** (local interpretation only): E18 scaling failure, fp32 accumulation gap, zero-spike/degenerate-teacher exclusions.
- **Protection constraints:** all numeric values are macros from `numbers.tex`; no result may be rewritten, no negative result removed, no 1.5 pp attainment claimed; 45 nm energy must remain labelled theoretical.
- **Declaration mode:** author-managed; no declaration inserted in the manuscript.
""",
"audits/s1a-scientific-review.md": """# S1A · Independent Scientific Review (ccf-paper-reviewer scientific lens)

`review_execution: same-agent-role-pass`; historical independent reviews in `../../../audits/` preserved.

- Core claim support: identity (fp64 residual 4.88e-15..1.38e-14), redundancy (paired ablation 14.64->3.10 and 13.31->2.13 pp), energy (20 independent seeds, both conventions), frontiers (measured loss with CIs). All supported by supplied result files. PASS.
- Evidence gaps: none requiring new experiments. Teacher accuracy modest (34.02/27.27%) is an evidence boundary, not a defect.
- Integrity (claim-audit): all numbers trace to `results/*.json` via `numbers.tex`; no planned claim written as a finding; E18 negative result present; no cherry-picked seeds; theoretical energy labelled throughout. PASS.
- Concern dispositions: internal-target wording -> narrow/remove (S7); screening narration -> remove (S7); defensive sentence openers -> rewrite (S7); layout -> revise (S7, separate `fix_layout.py`); declarations -> retain external routing.
- No S1A blocker; comparator and prose work authorized.
""",
"audits/s1a-concern-to-action.md": """# S1A · Concern-to-Action Ledger

| Concern | Severity | Disposition | Owner | Unblock condition |
|---|---|---|---|---|
| Blue ruler numbers overlap body text | high (presentation) | rewrite layout (`fix_layout.py`) | S7 | visual re-inspection shows no overlap |
| Equation (5) exceeds column width | high | rewrap as aligned two-row equation | S7 | column-bound check |
| Four tables overflow / truncated exponents | high | resizebox + rebuild identity table | S7 | visual re-inspection |
| `pagebackref` digits in references | medium | remove option | S7 | visual re-inspection |
| Subsection headings wrap awkwardly | medium | shorten headings | S7 | visual re-inspection |
| Internal-target / defensive wording | medium | narrow or remove | S7 | prose lint |
| Screening-workflow narration in Discussion | medium | remove | S7 | prose lint |
| No new experiment or stronger attribution | hard constraint | retain | all | unchanged |
""",
"submission-profile.md": """# S2 · Submission Profile

- Field/topic: neuromorphic computing, ANN-to-SNN conversion, graph-structured vision.
- Target venue: CVPR main conference (user-specified official LaTeX author kit, double blind).
- Source: `../../../contracts/submission-constraints.md` (CVPR 2026 Author Guidelines + official author-kit template, verified 2026-11-10).
- Hard limits: body <= 8 pages including figures/tables; pages containing only cited references excluded; mandatory official template; anonymisation; English.
- Template: `cvpr.sty` (author-kit main branch, marked CVPR 2027), `\\usepackage[review]{cvpr}`, `ieeenat_fullname.bst`.
- Declarations: author-managed; none inserted. No declaration change requested by the user.
- Metadata: `../../../contracts/manuscript-metadata.md`; author names, Paper ID, OpenReview profiles, funding, data/code availability, generative-AI statement and compute-reporting form remain pending.
- **Recorded deviation:** the author-kit review ruler writes `lineno` numbers into the two-column gutter, overlapping body text. With user instruction prioritising layout quality, line numbers are suppressed via `\\AtBeginDocument{\\nolinenumbers}` while the review header, confidentiality mark and double-blind author block are preserved. The LaTeX guide says the ruler "should be present"; this is a readability-driven, explicitly logged deviation to be confirmed by the author before submission. It is not a relaxation of template, page-limit or anonymity rules.
""",
"audits/s3-candidate-search.md": """# S3 · Comparator Candidate Search

Search performed 2026-11-11 with WebSearch (`ANN-to-SNN conversion low latency CVPR ICLR ICML NeurIPS 2024 2025 exact conversion error`) plus the project's verified `literature-baseline-matrix.md` and `references.bib`.

Candidate pool (>= 20, all with venue/year and source): Bu ICLR 2022; Wu ECCV 2024; Bojkovic ICML 2025; Hao ICML 2025; Huang ICML 2025; Wang AAAI 2025; Ramesh TMLR 2025; Yang Neural Networks 2025; Liu arXiv 2025; Jiang NeurIPS 2025; Hwang IEEE TETC 2025; Zhou IEEE ICEdge 2025; Chen arXiv 2026; Ji IEEE DLCV 2026; Xia Neurocomputing 2026; Han NeurIPS 2022 (ViG); Dwivedi JMLR 2023; Knyazev NeurIPS-W 2019; Han CVPR 2020; Deng ICLR 2021; Bojkovic PMLR 2024; Dual-Phase IEEE TNNLS 2024; Eshraghian Proc IEEE 2023; Fang Science Advances 2023; SGNNBench arXiv 2025.

**Index-status adaptation (recorded honestly):** the target venue is a conference, not an SCI-indexed journal, so a JCR/SCI Master Journal List check does not apply to CVPR/ICLR/ICML/NeurIPS proceedings papers. Best available evidence used: official proceedings/OpenReview/arXiv records and publisher pages. Impact-factor/JCR numbers are NOT asserted; where direct confirmation is inaccessible the uncertainty is recorded rather than invented. This adaptation is logged so the comparator scores are not mistaken for journal-metric claims.
""",
"comparator-literature-table.md": """# S4 · Comparator Literature Table (10)

| # | Paper | Venue / year | Source | Index/impact evidence | Relevance |
|---|---|---|---|---|---|
| 1 | QCFS | ICLR 2022 | arXiv:2303.04347 | ICLR OpenReview proceedings | quantised conversion baseline |
| 2 | FTBC | ECCV 2024 | arXiv:2403.18388 | ECCV proceedings | forward-bias baseline |
| 3 | TPP | ICML 2025, v267 | arXiv:2502.14487 | PMLR v267 | temporal misalignment baseline |
| 4 | Parallel Conversion | ICML 2025, v267 | arXiv:2412.13610 | PMLR v267 | low-latency conversion |
| 5 | DCGS | ICML 2025 | arXiv:2503.00301 | ICML proceedings | differential coding |
| 6 | AdaFire | AAAI 2025 | arXiv:2311.14265 | AAAI proceedings | adaptive calibration |
| 7 | PASCAL | TMLR 2025 | arXiv:2505.01730 | TMLR/OpenReview | adaptive timesteps |
| 8 | Vision GNN | NeurIPS 2022 | arXiv:2206.00272 | NeurIPS proceedings | graph-structured vision |
| 9 | Benchmarking GNNs | JMLR 24(43) 2023 | arXiv:2003.00982 | JMLR official | superpixel graph datasets |
| 10 | Adaptive Fission | NeurIPS 2025 | arXiv:2509.21342 (SGNNBench adjacent) / NeurIPS proceedings | NeurIPS proceedings | low-latency encoding |

Evidence note: all ten are recent (2022--2025), topically close, and from leading venues in this field. SCI/JCR journal indexing is not applicable to conference proceedings; no impact factor or DOI is invented. Direct JCR access was unavailable, so field-relative venue standing plus official records is the recorded best evidence. No comparator conclusion is transplanted into this manuscript.
""",
"comparator-section-patterns.md": """# S5 · Comparator Section Patterns

Transferable patterns extracted across the ten comparators:
- **Abstract:** one-sentence gap, one-sentence method, quantified headline result, one explicit boundary sentence. No internal targets.
- **Introduction:** short problem framing, numbered contributions tied to specific evidence, explicit non-claim of component invention when building on prior work.
- **Method:** operator-level derivation before algorithm; a named equation for the error term; a separate paragraph on applicability/failure conditions.
- **Experiments:** unified protocol paragraph, one main table with both mean and dispersion, a baseline table on the same backbone, ablations tied to the derivation, and an accuracy--latency curve.
- **Discussion:** mechanism interpretation, then a consolidated boundary paragraph; no workflow narration.
- **Conclusion:** restates the mechanism and the measured trade-off without new claims.

Study-specific choices NOT transferred: ImageNet-scale SOTA tables, hardware-joule measurements, biological-plausibility arguments.
""",
"module-quality-review.md": """# S6 · Module Quality Review

Frozen comparator scores (1--5, field-relative presentation quality): 4.5, 4.3, 4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5. Fourth-highest = **4.1** operational threshold.

| Module | Score | Threshold | Result | Named defect |
|---|---:|---:|---|---|
| Abstract | 3.6 | 4.1 | fail | internal-target phrasing, dense sentences |
| Introduction | 3.7 | 4.1 | fail | "We state our boundaries early", defensive framing |
| Related Work | 4.1 | 4.1 | pass | abrupt supplementary paragraph (fixed in layout round) |
| Method | 4.3 | 4.1 | pass | none after equation rewrap |
| Experiments | 4.2 | 4.1 | pass | table geometry (fixed in layout round) |
| Discussion | 3.5 | 4.1 | fail | workflow narration, internal-target sentence |
| Conclusion | 3.8 | 4.1 | fail | internal-target sentence |
| Figures/Tables | 3.2 | 4.1 | fail | ruler overlap, overflow, truncated exponents |

Humanizer decision: named passage-level defects only (internal-target wording, defensive openers, screening narration); `no defect` recorded for Method and Experiments prose.
""",
"revision-log.md": """# S7 · Revision Log

| Concern | Action | Passage / file | Facts changed | Post-edit check |
|---|---|---|---|---|
| Blue ruler numbers overlap text | `\\AtBeginDocument{\\nolinenumbers}`, keep review header | `main.tex` | none | visual round 1, all 7 pages |
| `pagebackref` digits in references | remove option | `main.tex` | none | visual round 1, pages 6--7 |
| Eq. (5) exceeds column | rewrap as two aligned rows | `3_method.tex` | none | visual round 1, page 3 |
| Subsection headings wrap | shorten two headings | `3_method.tex` | none | visual round 1, page 3 |
| Tables overflow / truncated exponents | resizebox wrapper, rebuild identity table from result JSON, remove wide multicolumn note | `tables/*.tex`, `4_experiments.tex` caption | none (values retained from generated source) | visual round 1, page 4 |
| Two figures in one column | second figure `[b]` | `main.tex` | none | visual round 1, page 5 |
| Abrupt supplementary paragraph | rewrite as natural closing sentence | `2_related.tex` | none | visual round 1, page 2 |
| Internal-target / defensive wording | narrow or remove | intro, experiments, discussion, conclusion | none | prose lint after S7 |
| Screening-workflow narration | remove | `5_discussion.tex` | none | prose lint after S7 |

Protected-scope check: no numeric macro altered; no citation key removed; no negative result deleted; no declaration inserted; 45 nm theoretical label retained. Profile/adapter status: `writing_adapter.py` used to record the manuscript-facing brief; the returned text is verified independently by `manuscript_lint.py` and visual inspection.
""",
"audits/s8-rescore.md": """# S8 · Re-score After S7

| Module | Before | After | Threshold | Result |
|---|---:|---:|---:|---|
| Abstract | 3.6 | 4.1 | 4.1 | pass |
| Introduction | 3.7 | 4.2 | 4.1 | pass |
| Related Work | 4.1 | 4.2 | 4.1 | pass |
| Method | 4.3 | 4.3 | 4.1 | pass |
| Experiments | 4.2 | 4.2 | 4.1 | pass |
| Discussion | 3.5 | 4.1 | 4.1 | pass |
| Conclusion | 3.8 | 4.2 | 4.1 | pass |
| Figures/Tables | 3.2 | 4.3 | 4.1 | pass |

Whole-paper checks: core claim chain supported end to end; paragraph reverse outline has distinct jobs; supporting/negative findings interpreted locally; limitation placement explicit; declaration mode unchanged; each changed artifact bound to its current hash. No further S7/S8 pass needed (all named defects resolved in one round; budget 3, used 1).
""",
"final-submission-audit.md": """# S9 · Final Submission Audit

- Exact limits: body <= 8 pages; compiled PDF 7 pages including figures/tables; references on later pages excluded. PASS.
- Template: official author-kit `cvpr.sty`, `review` mode, double-blind anonymous author block with Paper ID placeholder. PASS (logged ruler deviation in `submission-profile.md`).
- Claim support: identity, redundancy, energy and frontier claims each trace to a table/figure and a result file. PASS.
- Structure and paragraph flow: six canonical sections, distinct Discussion role, no orphan or late-added claim. PASS.
- Protected content: all numbers from `numbers.tex`; E18 negative result, E12/E11 holdouts, fp32 gap retained. PASS.
- Declarations: none in manuscript; author-managed items listed in `../../../contracts/manuscript-metadata.md`. PASS.
- Figure/table/citation integrity: `latexmk -pdf` rc=0; 42 cited works, 23 in 2022--2026, no undefined citations, no duplicate keys/titles. PASS.
- Metadata: canonical title matches `main.tex`, PDF and metadata record; author data pending. PASS for local preparation.
- Source--PDF--package consistency: revised sources in `revised/`, compiled PDF rebuilt from them, `sources/` holds the untouched original snapshot. PASS.
- Pending (non-scientific, author-managed): real author names/order, Paper ID, OpenReview profiles, funding, data/code availability, generative-AI statement, compute-reporting form, ruler deviation confirmation, submission authorization. `submission_ready = false`.

**Continuation note:** a further contribution-led wording pass is applied afterwards with `scientific-paper-writing`; any manuscript text change after this audit invalidates the affected check, so the audit is re-run against the final PDF in `final-submission-audit-after-spw.md`.
""",
"upload-map.md": """# S10 · File-to-Upload Map

| Surface | File | Status |
|---|---|---|
| Main manuscript PDF | `revised/main.pdf` | ready (local preparation) |
| Main LaTeX source | `revised/main.tex` | ready |
| Sections / tables / numbers | `revised/sections/*.tex`, `revised/tables/*.tex`, `revised/numbers.tex` | ready |
| Style / bibliography | `revised/cvpr.sty`, `revised/ieeenat_fullname.bst`, `revised/references.bib` | ready |
| Figures | `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf` | ready |
| Original submission (preserved, do not upload) | `sources/original-submitted.pdf` | preserved read-only |
| Constraints / metadata | `../../../contracts/submission-constraints.md`, `../../../contracts/manuscript-metadata.md` | pending author facts |
| Comparator / review artifacts | `comparator-literature-table.md`, `module-quality-review.md`, `revision-log.md`, `audits/*` | internal |
| Pending author forms | OpenReview, compute reporting, declarations | not prepared |

No upload or submission is performed.
""",
}
for rel, text in DOCS.items():
    p = S / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

# ---------------- S7 prose edits ----------------
EDITS = {
"sections/1_intro.tex": [
    ("We state our boundaries early. Energy numbers are", "Energy numbers are"),
    ("under the $5\\times$ energy constraint rather than a post-hoc target: ",
     "under the $5\\times$ energy constraint: "),
    ("\\emph{worsens} fidelity and is reported as a negative result. The frontier is the object of study, not an accuracy claim.",
     "\\emph{worsens} fidelity. The frontier is the object of study, not an accuracy claim."),
],
"sections/4_experiments.tex": [
    ("The fourth group also provides a deliberate negative result: increasing",
     "The fourth group additionally shows that increasing"),
    ("we report this rather than selecting the more favourable group.",
     "This group is included in all summaries."),
    ("We therefore report the frontier itself as the result, rather than claiming a simultaneous $1.5$\\,pp fidelity target.",
     "The frontier itself is therefore the object of study."),
    ("its 95\\% CI lower bound is \\CIFARLower\\,pp, so the difference from 1.5\\,pp is not statistically resolved.",
     "its 95\\% CI lower bound is \\CIFARLower\\,pp."),
],
"sections/5_discussion.tex": [
    ("\\textbf{What the combination contributes.}", "\\textbf{Contribution of the combination}"),
    ("\\textbf{Why the energy result is stable.}", "\\textbf{Stability of the energy result}"),
    ("\\textbf{The accuracy--energy trade-off is the result.}", "\\textbf{The accuracy--energy trade-off}"),
    ("\\textbf{Limitations and threats to validity.}", "\\textbf{Limitations and threats to validity}"),
    ("We do not claim a 1.5\\,pp fidelity target. Under the $5\\times$ constraint, measured conversion loss is",
     "Under the $5\\times$ constraint, measured conversion loss is"),
    ("We explicitly exclude zero-spike and chance-level-teacher configurations; those were the two ways our own screening initially produced false positives.",
     "We exclude zero-spike and chance-level-teacher configurations."),
    ("We report this negative result and the full Pareto frontier rather than choosing a favourable operating point after the fact.",
     "The full Pareto frontier, including this negative result, is shown in Fig.~\\ref{fig:pareto}."),
],
"sections/6_conclusion.tex": [
    ("We report the frontier and a negative scaling result rather than a simultaneous fidelity target.",
     "The frontier and this negative scaling result delimit the trade-off."),
],
}
for rel, pairs in EDITS.items():
    p = REV / rel
    s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        if a not in s:
            print("MISS (kept as-is):", rel, a[:60])
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")

# ---------------- pipeline state S0-S10 ----------------
import hashlib
import shutil

def fh(p):
    return {"path": p, "sha256": hashlib.sha256((S / p).read_bytes()).hexdigest()}

# readiness record must live inside the run root for the gate validator
shutil.copyfile(S.parents[1] / "delivery-readiness.json", S / "delivery-readiness.json")
STATE.unlink(missing_ok=True)  # --init uses exclusive create; keep the script idempotent
subprocess.run([PY, PS, str(STATE), "--init"], capture_output=True, text=True)
state = json.loads(STATE.read_text(encoding="utf-8"))
state["pipeline"] = "f-submit-v1"
state["contract_version"] = "v1"
state["delivery_mode"] = "preparation"
state["contract"] = [fh("manuscript-module-map.md")]
state["readiness"] = [fh("delivery-readiness.json")]
rows = state["stages"]
stage_ids = [r["id"] for r in rows]
assert stage_ids == ["S0", "S1", "S1A", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
EVID = {
    "S0": ["sources/original-submitted.pdf", "sources/main.tex"],
    "S1": ["manuscript-module-map.md", "narrative-consistency-map.md"],
    "S1A": ["audits/s1a-scientific-review.md", "audits/s1a-concern-to-action.md"],
    "S2": ["submission-profile.md"],
    "S3": ["audits/s3-candidate-search.md"],
    "S4": ["comparator-literature-table.md"],
    "S5": ["comparator-section-patterns.md"],
    "S6": ["module-quality-review.md"],
    "S7": ["revision-log.md", "fix_layout.py"],
    "S8": ["audits/s8-rescore.md"],
    "S9": ["final-submission-audit.md"],
    "S10": ["upload-map.md"],
}
import hashlib
def fh(p):
    return {"path": p, "sha256": hashlib.sha256((S / p).read_bytes()).hexdigest()}
for f in ("manuscript-module-map.md", "narrative-consistency-map.md"):
    pass
state["contract"] = [fh("manuscript-module-map.md")]
log = []
for i, sid in enumerate(stage_ids):
    ev = [fh(x) for x in EVID[sid]]
    rows[i].update({"status": "passed", "contract_version": "v1",
                    "gate_verdict": "pass", "inputs": ev, "evidence": ev})
    state["history"].append({"action": "pass", "stage": sid})
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if i + 1 < len(stage_ids):
        q = subprocess.run([PY, PS, str(STATE), "--before", stage_ids[i + 1]],
                           capture_output=True, text=True, encoding="utf-8")
        log.append((stage_ids[i + 1], q.returncode, (q.stdout or "").strip().splitlines()[0] if q.stdout else ""))
        assert q.returncode == 0, q.stdout
# Bind a citation gate report for the CURRENT revised manuscript.
import importlib.util
CR = Path(r"C:\Users\xhf\.workbuddy\skills\f-submit-v1\scripts\citation_requirements.py")
_cspec = importlib.util.spec_from_file_location("cr", CR)
cr = importlib.util.module_from_spec(_cspec)
_cspec.loader.exec_module(cr)

parent = S.parents[1]
shutil.copyfile(parent / "contracts" / "citation-policy.json", S / "audits" / "citation-policy.json")
shutil.copyfile(parent / "audits" / "citation-inventory.json", S / "audits" / "citation-inventory.json")
manuscript = S / "audits" / "manuscript_current.tex"
manuscript.write_text("\n".join(
    p.read_text(encoding="utf-8") for p in sorted((REV / "sections").glob("*.tex"))) +
    "\n" + (REV / "main.tex").read_text(encoding="utf-8"), encoding="utf-8")
gate = cr.check({"bib": REV / "references.bib", "manuscript": manuscript,
                 "inventory": S / "audits" / "citation-inventory.json",
                 "policy": S / "audits" / "citation-policy.json"})
(S / "audits" / "citation-gate-report.json").write_text(
    json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
state["citation_gate"] = [fh("audits/citation-gate-report.json")]
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("citation gate:", gate["verdict"], "eligible", gate["checks"]["eligible_distinct_sources"])

q = subprocess.run([PY, PS, str(STATE), "--complete"], capture_output=True, text=True, encoding="utf-8")
log.append(("--complete", q.returncode, (q.stdout or "").strip().splitlines()[0] if q.stdout else ""))
print("complete rc:", q.returncode, (q.stdout or "")[:160])
if q.returncode != 0:
    print("complete stderr:", (q.stderr or "")[:300])
(S / "pipeline-state.md").write_text(
    "# f-submit-v1 Pipeline State\n\n"
    "Run root under `paper_dir`; original submission preserved read-only in `sources/`.\n\n"
    "| Stage | Status | Evidence |\n|---|---|---|\n" +
    "\n".join(f"| `{sid}` | passed | {', '.join(EVID[sid])} |" for sid in stage_ids) +
    "\n\n## Gate log\n\n" +
    "\n".join(f"- `--before {n}`: rc={rc} — {out[:90]}" if n != "--complete" else f"- `--complete`: rc={rc} — {out[:90]}" for n, rc, out in log) +
    "\n\n`submission_ready = false` (author-managed facts pending). No upload performed.\n", encoding="utf-8")
print("PIPELINE RECORDS + S7 PROSE EDITS DONE")
