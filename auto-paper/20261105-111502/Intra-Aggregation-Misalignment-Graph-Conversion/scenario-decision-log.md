# Scenario decision log

Canonical evaluation: `CCFA-startup -> G0 -> G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 ->
validation -> handoff`. A rejected scenario keeps its failed gate and never advances; a replacement
restarts from CCFA-startup. All access dates 2026-11-05.

## Scenarios considered

| # | scenario | method/domain fit | first failing gate | verdict |
|---|---|---|---|---|
| S1 | **Intra-aggregation misalignment + bound-derived latency allocation on graph ANN→SNN conversion (selected)** | exact identity with `Â` inside, invertible `ρ_n` bound, low-T deployment rule | none | **proceed** |
| S2 | Unified graph-conversion benchmark (a table of T grids and methods) | weak: an evaluation table without a mechanism or capability | G8 (thin benchmark substitution; companion A already owns the audit) | rejected |
| S3 | A new stochastic neuron for graphs | contradicts the deterministic-mechanism claim; enters an accuracy race | G3/G8 (mechanism conflict, task book forbids SOTA spending) | rejected |
| S4 | Deeper/wider backbones to raise ANN accuracy | companion B already showed depth hurts conversion | G3/G8 (no mechanism-level fit; task book §0 iron rule 1) | rejected |
| S5 | Cross-subject EEG low-latency probabilistic SNN (pre-existing direction) | different application domain, no graph aggregation operator | G3 (out of the authorized method family) | not started |
| S6 | Theory-only paper with no held-out experiment | proof without a practitioner-usable capability | G8 (repeats companion B's Significance deduction) | rejected |

S5 is a pre-existing guidance direction from `auto-paper/20261028-171500/` and was not re-opened;
it is listed only to show it was considered and excluded from this run.

## Selected scenario S1 — gate record

| gate | status | evidence | pass reason |
|---|---|---|---|
| CCFA-startup | passed | 7 packet artifacts + `feasibility-contract.json` + C8 addendum | all owners named; F1/F2 closed at design stage; `startup-decision.md` = proceed |
| G0 | passed | `notes/G0_literature_map.md`, `prior-art-opportunity-map.md`, `literature-baseline-matrix.md` | current strong baselines with official URLs, code/checkpoint status, datasets, metrics, direct-vs-context roles |
| G1 | passed | `dataset-access-log.md` | six direct-public datasets, no approval flow |
| G2 | passed | `claim-evidence-matrix.md`, `guidance.md` Experiment Plan | node classification, fixed splits, accuracy, 7 seeds, bootstrap CI, frozen T grid |
| G3 | passed | `theoretical-feasibility-audit.md` | mechanism-level fit (`Â` inside the identity) with a named falsifier |
| G4 | passed with boundary | `novelty-feasibility-report.md`, `notes/overlap-risk-AB.md` | no public duplicate; same-group overlap author-managed |
| G5 | passed | `hardware-profile.md`, `strong-result-feasibility-contract.md` | RTX 3060 12 GB, WSL GPU pass-through, ~108 h, ≤12 GB, defined scale repair |
| G6 | passed with limitation | `literature-baseline-matrix.md` | four baseline classes, ≥3 direct reruns, ≥7 ablations; no released checkpoints recorded as a labelled limitation |
| G7 | passed | `strong-result-feasibility-contract.md`, `feasibility-contract.json` | four calibrated claims with prototypes, finite budgets and stop-return conditions |
| G8 | passed | `story-strength-audit.md`, `idea-red-team-review.md` | decisive reviewer question answered by a named held-out experiment |
| validation | passed | validator stdout: "Guidance structure is valid." | `--strict --packet` clean |
| handoff | passed | `auto-paper/generated-research-directions.md` row | `f-research-v1` may start at P0 |

## Revisits and repairs

- No scenario replacement occurred; S1 was evaluated once in canonical order.
- Two repairs happened **inside** CCFA-startup before any later gate was marked passed: the
  red-team's F1 (no new capability) was repaired by making C3 the binding `expected_strong`, and
  F2 (same-group overlap) was repaired by the author's 2026-11-05 decision. Both are recorded in
  `execution-contract-v1-addendum-C8.md`.
- The G0 sweep also produced seven source conflicts with the task book, recorded in
  `notes/G0_source_conflicts.md` rather than silently corrected in the claims.

## Source links

arXiv search pages and primary sources are listed in `notes/G0_literature_map.md` §6 and
`prior-art-opportunity-map.md`. Every link was accessed 2026-11-05.
