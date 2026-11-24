# f-submit-v1 Delivery Manifest

Generated 2026-11-11T11:17:35.214383

Original submission is preserved read-only in `sources/`; all revised outputs are under this run root.

## Deliverables

- `revised/main.pdf` — final CVPR-format manuscript (7 pages, anonymous review mode)
- `revised/main.tex`, `revised/sections/*.tex`, `revised/tables/*.tex`, `revised/numbers.tex`, `revised/references.bib`, `revised/cvpr.sty`
- `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf`
- `visual/round1|round2|round3/` — three rounds of 110-dpi page renders used for visual QA
- `manuscript-module-map.md`, `narrative-consistency-map.md`, `comparator-literature-table.md`, `module-quality-review.md`, `revision-log.md`
- `final-submission-audit-after-spw.md`, `audits/` — S1A reviews, citation gate, compile logs
- `submission-profile.md`, `upload-map.md`, `delivery-readiness.json`, `pipeline-state.json.md`

## Gate status

- `pipeline_state.py --complete`: rc=0 PASS (S0–S10 all passed in order)
- `pipeline_state.py --submission-ready`: rc=1 (expected; submission_ready=false)
- citation gate: pass (42 sources, 23 recent)
- `latexmk -pdf`: rc=0; final PDF 7 pages <= 8

`workflow_complete=true`, `submission_ready=false`. No upload or submission performed.

## All files (86)

- `audits/citation-gate-report.json`
- `audits/citation-inventory.json`
- `audits/citation-policy.json`
- `audits/manuscript_current.tex`
- `audits/s1a-concern-to-action.md`
- `audits/s1a-scientific-review.md`
- `audits/s3-candidate-search.md`
- `audits/s8-rescore.md`
- `build_pipeline.py`
- `comparator-literature-table.md`
- `comparator-section-patterns.md`
- `delivery-readiness.json`
- `figures/framework.pdf`
- `figures/loss_T.pdf`
- `figures/pareto.pdf`
- `final-submission-audit-after-spw.md`
- `final-submission-audit.md`
- `finalize_after_spw.py`
- `fix_layout.py`
- `manuscript-module-map.md`
- `module-quality-review.md`
- `narrative-consistency-map.md`
- `pipeline-state.json`
- `pipeline-state.md`
- `revise_spw.py`
- `revised/cvpr.sty`
- `revised/ieeenat_fullname.bst`
- `revised/main.bbl`
- `revised/main.pdf`
- `revised/main.tex`
- `revised/numbers.tex`
- `revised/preamble.tex`
- `revised/references.bib`
- `revised/sections/1_intro.tex`
- `revised/sections/2_related.tex`
- `revised/sections/3_method.tex`
- `revised/sections/4_experiments.tex`
- `revised/sections/5_discussion.tex`
- `revised/sections/6_conclusion.tex`
- `revised/tables/tab_ablations.tex`
- `revised/tables/tab_baselines.tex`
- `revised/tables/tab_identity.tex`
- `revised/tables/tab_main.tex`
- `revision-log.md`
- `sources/cvpr.sty`
- `sources/ieeenat_fullname.bst`
- `sources/main.tex`
- `sources/manuscript_all.tex`
- `sources/numbers.tex`
- `sources/original-submitted.pdf`
- `sources/preamble.tex`
- `sources/references.bib`
- `sources/sections/1_intro.tex`
- `sources/sections/2_related.tex`
- `sources/sections/3_method.tex`
- `sources/sections/4_experiments.tex`
- `sources/sections/5_discussion.tex`
- `sources/sections/6_conclusion.tex`
- `sources/tables/tab_ablations.tex`
- `sources/tables/tab_baselines.tex`
- `sources/tables/tab_identity.tex`
- `sources/tables/tab_main.tex`
- `submission-profile.md`
- `upload-map.md`
- `visual/final-page-1.png`
- `visual/round1/page-1.png`
- `visual/round1/page-2.png`
- `visual/round1/page-3.png`
- `visual/round1/page-4.png`
- `visual/round1/page-5.png`
- `visual/round1/page-6.png`
- `visual/round1/page-7.png`
- `visual/round2/page-1.png`
- `visual/round2/page-2.png`
- `visual/round2/page-3.png`
- `visual/round2/page-4.png`
- `visual/round2/page-5.png`
- `visual/round2/page-6.png`
- `visual/round2/page-7.png`
- `visual/round3/page-1.png`
- `visual/round3/page-2.png`
- `visual/round3/page-3.png`
- `visual/round3/page-4.png`
- `visual/round3/page-5.png`
- `visual/round3/page-6.png`
- `visual/round3/page-7.png`
