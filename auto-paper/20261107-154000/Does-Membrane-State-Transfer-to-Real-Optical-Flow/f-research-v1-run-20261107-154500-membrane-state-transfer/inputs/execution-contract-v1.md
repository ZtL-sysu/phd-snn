# execution-contract-v1.md (immutable run-local contract, round 001)

Generated 2026-11-07 for the round-001 guidance package. User instructions override skill defaults
where they conflict; host and system constraints remain supreme.

## User goal
Continuous research on a GNN-form fruit-fly connectome x SNN mechanisms x vision, target CVPR 2027,
using the user's own f-guidance-builder-v1 / f-research-v1 pipelines and the local CCFA skill chain.
Each round: 5 distinct idea candidates, one independent review pass used for ranking only (no hard
threshold), one primary idea selected, a compliant guidance contract generated, full experiments on
novix exp-4090, and the f-research-v1 protocol followed until the finished paper reaches
`ccf-paper-reviewer full` `**Overall:** X >= 8.0`.

## Authorized operations
Local read/write under `C:\code\phd-snn`; local GPU work in conda `dyg-cold`; novix exp-4090
submission and recovery; CCFA reviews; f-research writing, compilation and audit. Not authorized:
submission, OpenReview registration, commit/push, publishing, creating or modifying automations,
remote compute other than novix exp-4090.

## User directives (chronological)
- 14:10: mechanism changes are not limited to one substitution; multiple substitutions and added
  mechanisms are allowed, with independent ablations and parameter-matched controls.
- 14:34: no local wall-clock or step budget on the 4090 task; submit without `--max-turns`/`--timeout`,
  no blocking watch; results are recovered across rounds, local documents updated each round.
- 14:45: f-guidance-builder-v1 and f-research-v1 are the user's own pipelines; obey their SKILL.md,
  references, assets and scripts, including canonical stage order and validators.
- 15:09: all reviews must use locally installed CCFA skills; deadline restored to 2026-11-14 23:59:59 GMT+8.
- 15:28: exactly 5 distinct idea candidates per round; scores rank only, no hard threshold; pick the
  single most promising idea and run the full pipeline; the only completion criterion is the finished
  paper full review Overall >= 8.0; iterate via correction loop, backup pool, then fresh ideation.

## Interaction with skill budgets
`feasibility-contract.json` records estimated runtime and memory because the f-guidance feasibility
schema requires a finite planning budget for scientific planning. These are estimates for feasibility
only and are NEVER passed to `novix task create` as a timeout or turn cap.

## Inputs, scope, output root
Inputs: real FlyWire v783 edges/annotations/eye positions (Zenodo 21549559, CC BY 4.0),
DAVIS-2017 trainval-480p and optional MPI-Sintel real optical flow (direct links probed this session),
SYNTHETIC temporal sequences, eight rounds of local measurements, 21 verified first-hand references,
and the round-001 independent reviews. Output root: this guidance directory, which also contains the
f-research P0 run root. All process files and deliverables stay under `C:\code\phd-snn`.

## Quality requirements
No fabricated literature, data, results, scores or Overall. At least 5 seeds, bootstrap 95% CI,
BH correction, degree-preserving null, preregistered direction. The P12 citation gate (>=36 unique
verified works with strict recent majority) remains pending until real evidence exists.
`workflow_complete` and `submission_ready` are separate; the latter stays false.
