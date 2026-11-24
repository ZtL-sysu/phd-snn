# Pipeline State — f-research-v1

Update after every stage. Never begin the next stage until the current one is `passed`.

## Run Boundary

- Guidance file: `C:/code/phd-snn/auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/guidance.md`
- Guidance directory: `C:/code/phd-snn/auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/`
- Run root under guidance directory: `.../f-research-v1-run-20261105-111502-gnn2snn/`
- Artifact manifest: `audits/path-manifest.md`
- Single final PDF page policy: 8-page main text + unlimited references/appendix, an ICML-2026-derived **working assumption** because 2027 CFPs are unpublished; no numeric default imposed by the workflow.
- Final template policy: ICML-style official double-blind LaTeX when the venue is confirmed; otherwise the contract-selected self-contained preamble, recorded as unresolved.
- Path-containment status: `passed` at P0 (re-checked at P21). All claim-bearing artifacts are inside the run root; external companion assets were copied byte-for-byte with hashes in `audits/reaccepted-assets.md`.

All process files and deliverables must be under the run root. External paths are listed only as
explicitly authorized execution sources or tool-cache sources after the accepted artifact has been
copied into the run root.

| Stage | Name | Status | Evidence / artifact path | Gate result | Notes |
|---|---|---|---|---|---|
| P0 | Load guidance file and create guidance-directory run root | passed | `audits/path-manifest.md`, `contracts/execution-contract-v1.md` | PASS | run root inside guidance directory |
| P1 | Validate guidance file | passed | `audits/guidance-validation.md` | PASS | `--strict --packet` clean; packet `proceed` |
| P1A | Strong-result feasibility lock | passed | `audits/strong-result-feasibility-lock.md` | PASS | 4/4 claims pass; C3 binding |
| P1B | CCFA pre-experiment review and integrity audit | passed | `audits/ccfa-pre-experiment-review.md`, `audits/ccfa-pre-experiment-integrity.md` | PASS | all claims correctly marked PLANNED |
| P2 | Local Conda experiment protocols and setup checks | passed | `protocols/protocol.md`, `audits/p2-environment-check.md`, `notes/S0_foundation.md` | PASS | G0 reproduction < 0.1 pp |
| P3 | Baseline-first execution gate | running |  |  | S1 probes next; see `notes/S1_design.md` |
| P3A | Baseline-evidence stop-loss review | pending |  |  |  |
| P4 | Full guidance experiment execution | pending |  |  |  |
| P5 | Strong-result lock and experiment evidence audit | pending |  |  |  |
| P5A | CCFA pre-draft scientific review and integrity audit | pending |  |  |  |
| P6 | Adapted scientific packet and AutoResearchClaw 16 PAPER_OUTLINE | pending |  |  |  |
| P7 | Clean-packet draft and paragraph reverse outline | pending |  |  |  |
| P8 | Evidence-selected figure/table generation and insertion | pending |  |  |  |
| P9 | AutoResearchClaw 18 PEER_REVIEW | pending |  |  |  |
| P10 | AutoResearchClaw 19 PAPER_REVISION | pending |  |  |  |
| P11 | AutoResearchClaw 20 QUALITY_GATE | pending |  |  |  |
| P12 | Reference build, verification, and duplicate-paper audit | pending |  |  |  |
| P13 | AutoResearchClaw 22 EXPORT_PUBLISH into run root | pending |  |  |  |
| P14 | AutoResearchClaw 23 CITATION_VERIFY | pending |  |  |  |
| P15 | TeX export verification and PDF compilation in run root | pending |  |  |  |
| P16 | Single final PDF and venue/author length policy | pending |  |  |  |
| P17 | Guidance-file paper audit | pending |  |  |  |
| P18 | Selected figure/table scientific-use audit | pending |  |  |  |
| P19 | Academic-profile selective polish via writing adapter | pending |  |  |  |
| P20 | Final PDF recompile and sanity checks | pending |  |  |  |
| P21 | Final delivery from guidance-directory run root | pending |  |  |  |

Allowed statuses: `pending`, `running`, `passed`, `blocked`, `superseded`. The canonical definition
is `assets/pipeline-definition.json`; validate the matching JSON ledger before advancing.

## Path-Containment Audit

| Artifact class | Expected location under run root | Current status | External source recorded? | Notes |
|---|---|---|---|---|
| Protocols and commands | `protocols/`, `experiments/` | pending | yes | `audits/reaccepted-assets.md` |
| Experiment logs and raw metrics | `results/`, `runs/` | pending | no | all new runs are local |
| Process audits and traceability | `audits/`, `notes/` | pending | no | — |
| Figures and source data | `figures/` | pending | no | — |
| Drafts and writing outputs | `writing/`, `tex/` | pending | no | ARC substitute is local |
| TeX build inputs and logs | `tex/` | pending | no | — |
| Final delivery bundle | `deliverables/` | pending | no | — |

## Page-Policy Audit

| Artifact | Template/style | Page count | Requirement | Status | Notes |
|---|---|---:|---|---|---|
| `paper.pdf` | ICML-style double blind (unverified for 2027) | — | 8-page main text as a working assumption | pending | recount after P16 |
