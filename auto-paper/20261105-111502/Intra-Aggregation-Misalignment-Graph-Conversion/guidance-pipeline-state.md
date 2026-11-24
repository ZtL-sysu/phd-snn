# guidance-pipeline-state — canonical ordered ledger

Pipeline: `f-guidance-builder-v1`. Canonical order (from `assets/pipeline-definition.json`):
`CCFA-startup -> G0 -> G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 -> validation -> handoff`.

Valid states: `pending | running | passed | blocked | superseded`. **`skipped` is not valid.**
A stage may only start when its immediate predecessor is `passed`. A repair reopens the earliest
affected stage and its whole downstream suffix, preserving prior evidence in versioned files.

| stage | state | entered | evidence / gate report | notes |
|---|---|---|---|---|
| CCFA-startup | **passed** | 2026-11-05 11:20 | 7 packet artifacts + `feasibility-contract.json` + C8 addendum | author decisions resolved; F1/F2 closed at design stage |
| G0 | **passed** | 11:36 | `notes/G0_literature_map.md`, `prior-art-opportunity-map.md`, `literature-baseline-matrix.md` | 12 arXiv queries + primary pages |
| G1 | **passed** | 11:36 | `dataset-access-log.md` | six direct-public graphs |
| G2 | **passed** | 11:36 | `claim-evidence-matrix.md`, `guidance.md` | fixed splits, metric, seeds, noise floor |
| G3 | **passed** | 11:40 | `theoretical-feasibility-audit.md` | `Â` inside the identity, named falsifier |
| G4 | **passed** | 11:40 | `novelty-feasibility-report.md`, `notes/overlap-risk-AB.md` | no public duplicate; same-group boundary declared |
| G5 | **passed** | 11:40 | `hardware-profile.md` | RTX 3060 12 GB + WSL pass-through |
| G6 | **passed** | 11:40 | `literature-baseline-matrix.md` | ≥3 direct reruns, ≥7 ablations, labelled checkpoint limitation |
| G7 | **passed** | 11:40 | `strong-result-feasibility-contract.md`, `feasibility-contract.json` | four calibrated claims, C3 binding |
| G8 | **passed** | 11:40 | `story-strength-audit.md`, `idea-red-team-review.md` | decisive reviewer question has a named experiment |
| validation | **passed** | 11:42 | validator stdout: "Guidance structure is valid." | `--strict --packet` clean |
| handoff | **passed** | 11:45 | `notes/handoff-note.md`, index row | f-research-v1 may start at P0 |

Structural ledger: `pipeline-state.json` (12 stages, all `passed`), `--workflow-complete` **PASS**,
`--submission-ready` **fails by design** (7 pending author/production items). Full validator
transcript: `notes/validator-transcript.md`.

## History

- 2026-11-05 11:15 — run root created; two ledgers initialized (`pipeline-state.json` for guidance,
  `f-research-v1-run-20261105-111502-gnn2snn/pipeline-state.json` for research); immutable contract v1 written.
- 2026-11-05 11:20 — G0 source material collected by an independent literature-research agent:
  12 arXiv search queries plus primary-source checks (PMLR/ICML/ECCV/OpenReview/GitHub/OGB/SNAP/PyG).
  Recorded as **material**, not as a passed gate.
- 2026-11-05 11:20 — environment probe: RTX 3060 12 GB with CUDA on four Windows Conda envs and
  WSL2 GPU pass-through; `AutoResearchClaw` package verified absent; CCFA and writing skills verified present.

## Open blockers

1. **Author decision (C8)**: the positioning of this manuscript relative to the two completed
   companion manuscripts. It changes the Core Idea, the priority claim and the related-work framing.
   Requires `AskUserQuestion`; no inference permitted.
2. **Venue rules (C14)**: ICML 2027 / NeurIPS 2027 CFPs are not published. The 8-page main-text
   target is a recorded working assumption, not a verified constraint.
