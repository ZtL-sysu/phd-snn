# P1B — CCFA pre-experiment integrity audit (`claim-audit` mode)

Executor: `ccf-integrity-auditor` discipline applied locally to frozen planned claims.
`review_execution: same-agent-role-pass`. Inputs: `contracts/guidance.snapshot.md`,
`contracts/ccfa-startup-packet/`, `registry/registry.md`, `protocols/protocol.md`,
`audits/reaccepted-assets.md`.

## Evidence-status classification (mandatory at P1B)

| claim id | statement | status | why |
|---|---|---|---|
| C1 | intra-aggregation deterministic misalignment is distinct from cross-layer stochastic misalignment | **PLANNED** | no S1 probe has run |
| C2 | `ρ_n`-weighted L-layer bound holds with a mandatory bias term | **PLANNED** | no proof or counterexample grid executed here |
| C3 | inverted bound predicts `T*` with ≥25% saving on held-out graphs | **PLANNED** | the binding expected result, explicitly not a finding |
| C4 | conversion is not dominated at T≤4 and plugs into three hosts | **PLANNED** | no arm measured in this run |
| G0 | environment reproduces frozen Cora/PubMed T=8 within 0.1 pp | **PLANNED until the gate script finishes** | the reproduction is a check, not a scientific claim |

**No planned claim is promoted to reported evidence.** Every numeric value in the guidance and the
feasibility contract is either a frozen calibration target, a budget, or a threshold — never a
result of this run. The frozen task-book §2 numbers (0.8026 / 0.7740 etc.) are labelled
`calibration evidence`, and the companion's `G^0.95` law is labelled `external calibration`.

## Claim-support alignment

| check | outcome |
|---|---|
| each main claim has a named mechanism | pass (4/4) |
| each main claim has a falsifying ablation | pass (4/4) |
| each main claim has simple / strong / matched comparators | pass (4/4) |
| each main claim has minimum / strong / failure conditions | pass (4/4) |
| metric direction stated | pass (higher / lower / lower / higher) |
| dataset and split bound to each claim | pass |
| resource budget finite and local | pass (108 h, ≤12 GB, 470 trials) |
| stop-and-return condition | pass (4/4) |
| `planned_claim` ≠ `observed_finding` | pass, `observed_finding` = unresolved |
| no unsupported priority / SOTA / energy claim | pass; C8 addendum forbids them |
| FTBC inheritance declared | pass, required in Related Work |
| anonymous companion division of evidence | pass as a design requirement, to be written at P7 |
| no invented author or venue facts | pass; 7 items pending in `delivery-readiness.snapshot.json` |

## Numeric and source integrity (prospective)

- All external numbers were checked against primary sources; seven conflicts with the task book
  are recorded in the parent `notes/G0_source_conflicts.md` rather than silently corrected.
- The 37.23 / T=4 claim is not usable as a general statement; only labelled cells may be quoted.
- `SSEL` and `DRSGCN` are unverifiable names and are excluded from all tables.
- Device is frozen per paired arm; the companion's +0.69 pp CUDA drift is a known hazard.
- `registry/results.csv` is the single source; every manuscript number will carry `% run:`.
- No hand-typed table numbers, no seed shopping, no deletion of negative results.

## Conditions carried to P3A / P5A

At P3A the auditor must re-run in `numeric-audit` mode on **real** baseline numbers; at P5A in
`full` mode on the complete claim/result/table/figure mapping. Those runs must not reuse this
planned-evidence verdict.

**P1B integrity gate verdict: PASS (planned-evidence classification correct; no fabricated
result, no unsupported claim, no unresolved claim-support gap).**
