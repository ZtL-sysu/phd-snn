# execution-contract-v1.md (immutable run-local contract)

Generated 2026-11-07 for the round-000 guidance package. The user's current instructions
override skill defaults where they conflict; host/system constraints remain supreme.

## User goal
Continuous research on a GNN-form fruit-fly connectome x SNN mechanisms x vision,
target CVPR 2027, using the user's own f-guidance-builder-v1 / f-research-v1 pipelines
and the CCFA skill chain. Five evaluated ideas per round; promising ones go to the
novix exp-4090 pool; an acceptable result starts the local f-research chain.

## Authorized operations
Local read/write under `C:\code\phd-snn`; GPU smoke locally in conda `dyg-cold`;
novix exp-4090 task submission and result recovery; CCFA reviews; f-research writing,
compilation and audit. NOT authorized: submission, OpenReview registration, commit/push,
publishing, creating or modifying automations, remote compute other than novix exp-4090.

## User directives that override skill defaults (recorded verbatim in intent)
- 2026-11-07 14:10: mechanism changes are NOT limited to a single substitution; multiple
  substitutions and added mechanisms are allowed. Attributability by independent ablation
  and parameter-matched controls is mandatory.
- 2026-11-07 14:34: **no local wall-clock/step budget on the 4090 task**. Do not pass
  `--max-turns` / `--timeout`, do not block on `watch`. Tasks may span several 6-hour rounds.
  Every round first checks in-flight tasks and updates local documents; only a completed
  task with an ACCEPT_STRONG verdict starts the local f-research chain.
- 2026-11-07 14:45: `f-guidance-builder-v1` and `f-research-v1` are the user's own
  research pipelines. The automation MUST obey their SKILL.md, references, assets and
  scripts, including canonical stage order, their own validators and their output layout.
  A paraphrased summary is not a substitute.

## Interaction between the two directives (important)
`feasibility-contract.json` records estimated `runtime_hours` / `memory_gb` because the
skill's feasibility schema requires a finite execution budget for scientific planning.
These are **estimates for feasibility only** and are NEVER passed to `novix task create`
as a timeout or turn cap. The 4090 task itself has no imposed budget.

## Inputs, scope, output root
Inputs: real FlyWire v783 edges/annotations/eye positions (Zenodo 21549559, CC BY 4.0),
explicitly SYNTHETIC temporal stimuli, eight rounds of local measurements and 21 verified
first-hand references. Output root: this guidance directory; the f-research P0 run root
must live inside it. All process files and deliverables stay under `C:\code\phd-snn`.

## Quality requirements
No fabricated literature, data, results, scores or Overall. At least 5 seeds, bootstrap
95% CI, BH correction, degree-preserving null, preregistered direction. G8 story gate and
P12 citation gate (>=36 unique verified works, strict recent majority) remain pending
until real evidence exists. `workflow_complete` and `submission_ready` are separate.

## Known pending / blocked gates
G8, validation, handoff are pending by design: this is an experiment-stage contract, not
a finished-paper contract. `pipeline_state.py --complete` is therefore expected to fail
until those gates pass with real evidence; that failure must be reported, not hidden.
