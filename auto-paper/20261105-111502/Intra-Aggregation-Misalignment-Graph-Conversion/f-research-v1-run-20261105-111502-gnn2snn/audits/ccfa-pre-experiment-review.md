# P1B — CCFA pre-experiment adversarial review

Executor: `ccf-idea-reviewer` (standard mode) applied by the local agent to frozen planned inputs,
following the skill's `SKILL.md` and `ccf-common/references/review-output-standards.md`.
`review_execution: same-agent-role-pass` (the skill is installed but not invoked as a separate
agent process; this is recorded rather than presented as an independent-agent review).
Inputs: `contracts/ccfa-startup-packet/` (literature map, idea cards, claim-evidence matrix,
feasibility contract) and `contracts/guidance.snapshot.md`.

**Evidence status: every claim below is PLANNED evidence. No experiment has run in this run.**
No score here is a paper score; the ≥9 target is measured only by `ccf-paper-reviewer` at P9.

## Verdict

`accept-to-develop` with four conditions. No fatal novelty, soundness, feasibility or
claim-support risk remains unresolved after the repairs recorded below. Confidence: high on
feasibility, medium-high on novelty (bounded search), medium on the C3 outcome (untested).

## Closest prior art and novelty delta

| work | subtraction result |
|---|---|
| TPP, ICML 2025 (arXiv:2502.14487) | different error source, norm-only bound, stochastic fix → survives |
| FTBC, ECCV 2024 (arXiv:2403.18388) | expected-error CNN bias, not an exact graph identity → survives, attribution mandatory |
| SGNNBench (arXiv:2509.21342) | no conversion entry → supplies baselines only |
| 2026 conversion-error preprints | non-graph → survives |
| anonymous companion (same project) | **removes the priority claim**; only the mechanism separation, G1(d) and `T*` remain |

## Independent expert notes (before synthesis)

| role | lens | rejection-grade concern | score-change condition | confidence |
|---|---|---|---|---|
| E1 | field expert | SGNNBench has no conversion arm; a codebase anchor is mandatory | ≥3 arms reproduced under the frozen protocol | high |
| E2 | method expert | FTBC's expected-error zeroing makes `β*` look derivative | exact identity with `ρ_n`, explicit attribution | high |
| E3 | experiment expert | C3 constants must be frozen before held-out measurement, or it is post-hoc fitting | committed pre-registration + shuffled control | high |
| E4 | AC / venue expert | Significance is decisive for ≥9; a theorem plus tables is an 8 | positive held-out `T*` capability | high |
| E5 | prior-art skeptic | three same-group manuscripts | anonymous companion + division of evidence | high |
| E6 | integrity | task book misstates ICML'25 T=4 numbers | primary-source verification only | high |

Agreement: the four claims are testable and the mechanism is not duplicated in the searched
literature. Disagreement: E3/E4 would withhold development credit until C3 exists; E1/E2 consider
the plan ready. Synthesis follows the strongest unresolved concern (E3/E4), hence the four
conditions below rather than an unqualified pass.

## Rubric (1–5, planned-stage readiness)

| dimension | score | evidence basis | repair condition if ≤3 |
|---|---|---|---|
| Problem importance | 4 | active 2024–2026 low-latency conversion area | — |
| Novelty | 4 | zero arXiv hits at the intersection; bounded coverage | pre-submission sweep |
| Mechanism clarity | 5 | identity written explicitly with `Â` inside | — |
| Soundness (planned) | 4 | G1(d) not yet proved; counterexample grid designed | L≤4 result |
| Feasibility | 5 | verified hardware, finite budgets, scale repair | — |
| Baseline strength | 4 | ≥3 direct reruns planned; no checkpoints released | protocol-compatibility column |
| Evidence plan | 5 | pre-registration, noise floor, held-out isolation, negative controls | — |
| Reproducibility | 5 | content-addressed run hashes, scripted tables | — |
| Significance (planned) | 4 | C3 designated as a new capability, not yet observed | positive held-out result |
| Ethics / overlap | 4 | author decision taken; statement not yet written | division-of-evidence paragraph at P7 |

No score is 3 or below; every score has an evidence basis.

## Conditions (all closed at design stage before P2)

1. **C3 frozen pre-registration** — `registry/registry.md` freezes ε, the held-out graph list,
   the T grid and the no-refit rule before any held-out measurement.
2. **Division of evidence** — the manuscript must cite A/B as anonymous companions and declare
   that its claims do not depend on their results; no "first" claim is reused.
3. **TPP re-implementation** — equations (8)–(13) with a recorded unit test, because the official
   codebase is unreleased; no claim of using their code.
4. **Numeric discipline** — device frozen per paired arm, `% run:` comments, scripted tables,
   primary-source-checked external numbers.

## Concern-to-action ledger

| id | concern | severity | criterion | action | owner | stage |
|---|---|---|---|---|---|---|
| A1 | C3 could be post-hoc fitted | major | soundness | freeze constants before held-out | f-research-v1 | P2/P4 |
| A2 | same-group overlap | major | ethics | anonymous companion + no reused priority claim | writing | P7 |
| A3 | TPP straw man | moderate | soundness | re-implement + unit test + log diff | f-research-v1 | P4 |
| A4 | external protocol mismatch | moderate | evidence | compatibility column + 5-day stop-loss | f-research-v1 | P4 |
| A5 | bound fails at L=4 | moderate | soundness | pre-registered failure-depth condition | f-research-v1 | P4 |
| A6 | device-induced 0.69 pp drift | moderate | numeric | frozen device field + G0 <0.1 pp gate | f-research-v1 | P2 |

**P1B gate verdict: PASS.** No unresolved fatal concern; every deduction has a repair condition
and an owner. A future P3A/P5A failure reopens the earliest affected stage through the autonomous
correction loop — it is not deferred to P9.
