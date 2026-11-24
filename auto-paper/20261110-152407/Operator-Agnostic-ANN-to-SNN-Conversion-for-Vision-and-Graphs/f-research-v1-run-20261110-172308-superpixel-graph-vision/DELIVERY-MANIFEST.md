# DELIVERY MANIFEST

## Current continuation status — 2026-11-12

The completion/gate statements below describe the historical 2026-11-11 delivery only. Research has reopened under contract v4. Current `pipeline-state.json` and `delivery-readiness.json` have `workflow_complete=false` and `submission_ready=false`; the historical manuscript is not a validated revised submission. Scientific corrections, complete-data strong-teacher experiments, matched baselines, seed replications and a new independent review remain in progress. The user's independent CCFA 8/10 target has not been achieved.

Current evidence: `takeover_20261112/full-data-reference-progress-v1.md`, `claim-evidence-update-20261112.md`, `independent-evidence-review-v2.md` and `active-runs.md`. The pre-edit manifest is preserved at `takeover_20261112/delivery-manifest-before-status-update.md`. Historical files and results below remain available for provenance, not current scientific acceptance.

Generated 2026-11-11T07:06:24.179793
All deliverables and process files are under the guidance directory (this run root).

## Primary deliverables

- `tex/main.pdf` — compiled CVPR-format manuscript (7 pages, anonymous review mode, <=8 page limit)
- `tex/main.tex`, `tex/sections/*.tex`, `tex/tables/*.tex`, `tex/numbers.tex`, `tex/references.bib`, `tex/manuscript_all.tex`
- `figures/pareto.pdf`, `figures/loss_T.pdf`, `figures/framework.pdf`
- `writing/p6-outline.md`, `writing/p7-draft.md`, two independent reviewer reports
- `audits/` — all gate, integrity, length, citation and figure/table audits
- `results/` — every raw experiment result (E1–E18)
- `contracts/` — guidance-v3 snapshot, user authorization, submission constraints, metadata, citation policy

## Final gate status

- `pipeline_state.py --complete`: rc=0 — PASS
- `pipeline_state.py --submission-ready`: rc=1 — expected FAIL (submission_ready=false)
- `latexmk -pdf`: rc=0; PDF text spot-check matches reported numbers
- `validate_guidance.py guidance-v3.md --strict --packet`: rc=0

## Readiness

- `workflow_complete = true` (26 canonical stages passed in order under contract v2)
- `submission_ready = false` (author-managed facts pending; see `contracts/manuscript-metadata.md`, `delivery-readiness.json`)

## All files (173)

- `audits/baseline-reproducibility.md`
- `audits/ccfa-baseline-evidence-review.md`
- `audits/ccfa-baseline-numeric-audit.md`
- `audits/ccfa-pre-draft-action-ledger.md`
- `audits/ccfa-pre-draft-integrity-audit.md`
- `audits/ccfa-pre-draft-scientific-review.md`
- `audits/ccfa-pre-experiment-integrity.md`
- `audits/ccfa-pre-experiment-review.md`
- `audits/citation-gate-report.json`
- `audits/citation-inventory.json`
- `audits/concern-to-action-ledger.md`
- `audits/e1-e4-results.md`
- `audits/e10-breakthrough.md`
- `audits/e11-confirmation.md`
- `audits/e12-results.md`
- `audits/e13-multiseed-and-identity-diagnosis.md`
- `audits/e15-margin-results.md`
- `audits/e16-results.md`
- `audits/e17-final-confirmation.md`
- `audits/e18-results-and-decision-point.md`
- `audits/e2-results-and-energy-boundary.md`
- `audits/e7-degenerate-teacher-trap.md`
- `audits/e8-results.md`
- `audits/e9-results.md`
- `audits/p10-revision-log.md`
- `audits/p11-quality-gate.md`
- `audits/p14-citation-verify.md`
- `audits/p16-length-audit.md`
- `audits/p17-paper-guidance-audit.md`
- `audits/p18-figure-table-audit.md`
- `audits/p19-polish-audit.md`
- `audits/p20-final-metadata.md`
- `audits/p21-final-audit.md`
- `audits/p8-figure-table-audit.md`
- `audits/p9-peer-review.md`
- `audits/paired-strong-result-audit.md`
- `audits/pipeline-state-update-log.md`
- `audits/reference-dedup-audit.md`
- `audits/strengthen-candidate-report.md`
- `audits/strong-result-gap-and-next.md`
- `audits/v3-reopen-log.md`
- `contracts/citation-policy.json`
- `contracts/claim-evidence-matrix-v2.md`
- `contracts/contract-change-v1-to-v2.md`
- `contracts/core-1028.snapshot.py`
- `contracts/guidance-v2.snapshot.md`
- `contracts/guidance-v3.snapshot.md`
- `contracts/guidance-validation-v3.md`
- `contracts/guidance-validation.md`
- `contracts/manuscript-metadata.md`
- `contracts/path-containment-manifest.md`
- `contracts/precision-claim-authorization.md`
- `contracts/strong-result-feasibility-lock.md`
- `contracts/strong-result-no-retreat.md`
- `contracts/submission-constraints.md`
- `data/pyg/raw/MNISTSuperpixels.zip`
- `data/pyg_bench/CIFAR10/processed/pre_filter.pt`
- `data/pyg_bench/CIFAR10/processed/pre_transform.pt`
- `data/pyg_bench/CIFAR10/processed/test_data.pt`
- `data/pyg_bench/CIFAR10/processed/train_data.pt`
- `data/pyg_bench/CIFAR10/processed/val_data.pt`
- `data/pyg_bench/CIFAR10/raw/CIFAR10_v2.pt`
- `data/pyg_bench/MNIST/processed/pre_filter.pt`
- `data/pyg_bench/MNIST/processed/pre_transform.pt`
- `data/pyg_bench/MNIST/processed/test_data.pt`
- `data/pyg_bench/MNIST/processed/train_data.pt`
- `data/pyg_bench/MNIST/processed/val_data.pt`
- `data/pyg_bench/MNIST/raw/MNIST_v2.pt`
- `delivery-readiness.json`
- `execution-contract-v1.md`
- `execution-contract-v2.md`
- `figures/framework.pdf`
- `figures/framework.png`
- `figures/loss_T.pdf`
- `figures/loss_T.png`
- `figures/pareto.pdf`
- `figures/pareto.png`
- `novix/in-flight-task.md`
- `novix/payload.b64`
- `novix/query-full.txt`
- `novix/query-header.md`
- `novix/query-improvement-arm.md`
- `novix/watch-log.md`
- `pipeline-state.json`
- `pipeline-state.md`
- `protocols/analyze_paired.py`
- `protocols/build_novix_query.py`
- `protocols/diag_identity.py`
- `protocols/final_complete.py`
- `protocols/finalize_pipeline.py`
- `protocols/gen_citation_gate.py`
- `protocols/gen_paper_artifacts.py`
- `protocols/reopen_and_gate_v3.py`
- `protocols/run_e1.py`
- `protocols/run_e10.py`
- `protocols/run_e11.py`
- `protocols/run_e12.py`
- `protocols/run_e13.py`
- `protocols/run_e15_margin.py`
- `protocols/run_e16.py`
- `protocols/run_e17.py`
- `protocols/run_e18.py`
- `protocols/run_e2.py`
- `protocols/run_e7.py`
- `protocols/run_e8.py`
- `protocols/run_e9.py`
- `protocols/run_experiments.py`
- `protocols/run_full_local.py`
- `protocols/run_full_local_v2.py`
- `protocols/scale_sweep.py`
- `protocols/strengthen_candidates.py`
- `protocols/update_state.py`
- `protocols/verify_paper.py`
- `protocols/vision_pipeline.py`
- `protocols/watch_20049.py`
- `results/e1/result.json`
- `results/e10/val_sweep.json`
- `results/e11/confirmation.json`
- `results/e12/confirmation.json`
- `results/e13/val_multiseed.json`
- `results/e15/val_sweep.json`
- `results/e16/val_sweep.json`
- `results/e17/confirmation.json`
- `results/e18/confirmation.json`
- `results/e2/val_sweep.json`
- `results/e7/refiltered.json`
- `results/e7/val_sweep.json`
- `results/e8/val_sweep.json`
- `results/e9/val_sweep.json`
- `results/experiment-traceability.md`
- `results/gpu_MNIST_seed0.json`
- `results/local_full/config.json`
- `results/local_full/README.md`
- `results/local_full/result.json`
- `results/local_full_v2/config.json`
- `results/local_full_v2/result.json`
- `results/paired_analysis.json`
- `results/scale_sweep.json`
- `results/smoke2_MNIST_seed0.json`
- `results/smoke3_MNIST_seed0.json`
- `results/smoke_MNIST_seed0.json`
- `results/strengthen_candidates.json`
- `tex/cvpr.sty`
- `tex/fig/teaser.tex`
- `tex/ieeenat_fullname.bst`
- `tex/main.bbl`
- `tex/main.brf`
- `tex/main.pdf`
- `tex/main.tex`
- `tex/manuscript_all.tex`
- `tex/numbers.tex`
- `tex/preamble.tex`
- `tex/rebuttal.tex`
- `tex/references.bib`
- `tex/sec/0_abstract.tex`
- `tex/sec/1_intro.tex`
- `tex/sec/2_formatting.tex`
- `tex/sec/3_finalcopy.tex`
- `tex/sec/X_suppl.tex`
- `tex/sections/1_intro.tex`
- `tex/sections/2_related.tex`
- `tex/sections/3_method.tex`
- `tex/sections/4_experiments.tex`
- `tex/sections/5_discussion.tex`
- `tex/sections/6_conclusion.tex`
- `tex/tables/tab_ablations.tex`
- `tex/tables/tab_baselines.tex`
- `tex/tables/tab_identity.tex`
- `tex/tables/tab_main.tex`
- `writing/p6-outline.md`
- `writing/p7-draft.md`
- `writing/p9-review-1.md`
- `writing/p9-review-2.md`
