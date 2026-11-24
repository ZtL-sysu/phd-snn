# Idea red-team review (`ccf-idea-reviewer`, standard strict mode)

**Verdict first:** `revise` → `accept-to-develop` after two binding repairs. Current readiness
**6/10** for a ≥9-calibrated CCF-A manuscript; development potential **8/10**. Confidence:
**medium-high** on novelty, **high** on the mechanism diagnosis, **medium** on the held-out
capability (no experiment has run). This is an **idea-stage readiness score**, not a paper score and
not an acceptance probability; the paper score is measured only by `ccf-paper-reviewer` in full mode.

**Target venue and assumptions:** CCF-A main ML track (ICML/NeurIPS family), double blind,
8-page main text as a working assumption from ICML 2026 (2027 CFPs unpublished).

**Search basis:** `searched` in the public literature — 12 arXiv full-search queries plus PMLR,
ICML, ECVA/ECCV, ACM, NeurIPS, OpenReview, GitHub, OGB, PyG, SNAP (`prior-art-opportunity-map.md`,
`notes/G0_literature_map.md`). `user-provided` for the two unpublished companion manuscripts;
their overlap is an author-managed risk, not a literature finding.

**Stage and development potential:** mechanism fixed, evidence plan not yet executed. Potential is
high because the missing ingredient is a specific, cheap, pre-registerable capability experiment,
not a new architecture or a large compute budget.

## Normalized idea

Problem: low-T graph ANN→SNN conversion error is attributed by the only mechanistic account to
cross-layer stochastic misalignment. Gap: no graph-specific identity, bound or timestep rule.
Root challenge: neighbourhood aggregation scrambles per-neighbour phases deterministically.
Insight: the error is an exact algebraic function of `Â` and `ρ_n`, so it can be bounded and inverted.
Method: exact identity + G1(d) bound + `β*` correction + membrane decoder + `T*` allocation.
Expected evidence: S1 branch A/B, zero L≤4 counterexamples, held-out `T*` savings, T≤4 Pareto.
Limitation: two-layer transductive scope, proxy efficiency metrics, protocol differences.

## Closest prior art table

| work | same method family? | same task/dataset? | same central claim? | subtraction result |
|---|---|---|---|---|
| TPP, ICML'25 | partly (conversion) | no (images/CNN) | no (cross-layer stochastic) | survives: different error source, different bound, different fix |
| FTBC, ECCV'24 | partly (bias calibration) | no (images/CNN) | no (expected error per timestep) | survives: exact identity, `ρ_n`, graph operator |
| SGNNBench 2025 | no (benchmark) | yes (graphs) | no (no conversion entry) | survives: supplies baselines, not the claim |
| SpikingGCN / SpikeGCL / SpikeGraphormer / MSG | no (direct training) | yes | no | survives: external anchors only |
| 2026 conversion-error preprints (2608.13952, 2601.21778) | partly (error analysis) | no | no (non-graph) | survives: no aggregation operator |
| **Companion B (unpublished)** | **yes** | **yes** | **partly** (identity, `β*`, decoder, Pareto) | **does NOT survive as a priority claim**; only the new probes, G1(d) and `T*` remain |

**Novelty delta:** after subtracting the nearest prior work, what remains is a controlled physical
separation of two misalignment mechanisms, a bound whose multiplier is the neighbourhood row sum
rather than a weight norm, and a bound-derived timestep allocation validated on held-out graphs.
No "first conversion framework" claim remains available.

## Serious blockers

| id | severity | concern | repair | owner |
|---|---|---|---|---|
| F1 | **fatal if unaddressed** | "verifies a setting the paper already uses" — the exact deduction that kept companion B at 8 | make held-out `T*` allocation a binding `expected_strong` claim with pre-registered failure condition | f-research-v1 |
| F2 | **fatal if unaddressed** | same-group three-paper overlap / salami slicing | anonymous companion citation, division-of-evidence statement, no reused priority claim (author decided 2026-11-05) | author + writing |
| F3 | major | no released TPP code → a weak transplant would be a straw man | re-implement from equations (8)–(13), unit-test at T=8 against frozen numbers, log the diff | f-research-v1 |
| F4 | moderate | direct-training baselines use incompatible protocols | protocol column + 5-day stop-loss + labelled SGNNBench context rows | f-research-v1 |

## Per-expert reviewer notes (independent before synthesis)

| reviewer | lens | rejection-grade concern | or reason none | confidence |
|---|---|---|---|---|
| E1 | field expert (spiking GNN) | conversion arm absent from SGNNBench; will demand a codebase anchor | — | high |
| E2 | method expert (conversion theory) | FTBC already zeroes expected error; must prove the claim is exact and graph-specific, not a rediscovery | — | high |
| E3 | experiment expert | held-out `T*` needs frozen constants and a matched uniform-T budget control, else it is post-hoc fitting | — | high |
| E4 | AC / venue expert | Significance is the decisive axis for a 9; a theorem plus tables is not enough | — | high |
| E5 | skeptical prior-art expert | same group has two manuscripts on the same identity; overlap declaration must be airtight | — | high |
| E6 | theory expert (added) | an L-layer bound with `ρ_n` may be loose; conservatism must be quantified, and failure depth named | — | medium |
| E7 | integrity (added) | the task book's speed-card misstates ICML'25's T=4 numbers; any quoted number must be primary-source checked | — | high |

Agreement: all seven accept that the intersection of graph conversion and exact error analysis is
empty in the searched literature. Disagreement: E3/E4 would hold the score at 6 until a held-out
capability exists; E1/E2 consider the mechanism separation already worth developing. Synthesis does
not average away F1 — the final stance follows E3/E4.

## Rubric scores (1–5)

| dimension | score | confidence | evidence basis | deduction / repair condition |
|---|---|---|---|---|
| Problem importance | 4 | high | low-latency SNN conversion is an active 2024–2026 area | to 5: show a deployment setting where `T*` changes a decision |
| Novelty | 4 | medium-high | zero arXiv hits at the intersection; companion overlap real | to 5: independent replication of the mechanism separation |
| Mechanism clarity | 5 | high | identity written explicitly with `Â` inside | — |
| Theoretical soundness | 4 | medium | G1(d) not yet proved or counterexample-searched | to 5: L≤4 zero counterexamples + conservatism table |
| Feasibility | 5 | high | small graphs, 7 seeds, RTX 3060 12 GB verified, T grid is cheap | — |
| Baseline strength | 4 | high | ≥3 verifiable SGNNBench arms + four-way internal control | to 5: all three arms under the identical protocol |
| Evidence plan | 4 | high | pre-registration, 2× noise floor, held-out graphs, negative controls | to 5: frozen constants committed before measurement |
| Reproducibility | 5 | high | conda/WSL pinned, registry with commit hashes, scripted tables | — |
| Significance | **3** | high | **F1: no capability yet; companion B's exact deduction** | **to 5: held-out `T*` result that changes what a practitioner can compute** |
| Ethics / overlap | **3** | high | **F2: three same-group manuscripts** | to 5: division-of-evidence statement accepted by a reviewer |

Scores ≤3 carry an explicit deduction and repair condition as required by `ccf-common`.

**Weighted final score:** 6/10 current readiness; 8/10 development potential after F1–F4 repairs.
Score-change conditions (conservative, no probability claim):
- F1 repaired with a held-out `T*` capability: **+1 to +2** overall paper-stance potential.
- F2 repaired with a clean division of evidence: **0 to +0.5**, but removes a fatal desk-reject risk.
- F3/F4 repaired: **+0 to +0.5** on Evidence/Soundness.

**Strict reviewer comments:** "The identity is not new to this group. If the new paper only reframes
it against ICML'25, it is a second venue for the same result. Give me something I can compute with
your bound that I could not compute with the previous paper." — this is the decisive comment the
guidance must answer.

**Fixability table:** F1 = requires-new-result (designed, not yet run); F2 = evidence/writing-fixable
(author decision already taken); F3 = design-fixable; F4 = writing+design-fixable.

**Upgrade / pivot actions:** (1) bind `T*` allocation as `expected_strong`; (2) write the division
of evidence into Related Work at P7; (3) TPP re-implementation with unit test at P4; (4) protocol
column in Table 2. If `T*` fails, pivot within the same family to a bound-derived model-selection
rule (see `idea-cards.md` rescue routes).

**Evidence that would change my score:** a pre-registered held-out result showing bound-predicted
`T*` reaches target accuracy with strictly fewer steps than a matched uniform-T budget, with the
fitting constants frozen before measurement.

**Recommendation:** `accept-to-develop` conditional on F1 and F2 being written into the guidance
contract before G0. Both are now recorded in `execution-contract-v1-addendum-C8.md` and in the
strong-result feasibility contract, so the condition is satisfied at the idea stage.

**Optional next-module decision:** `ccf-experiment-designer` in `design` mode.

**Checklist status:** 10/10 mandatory items completed.

**Output self-check:** verdict first; venue and assumptions named; search basis labelled; closest-work
table precedes scores; five required expert roles plus two relevant additions are independent;
every ≤3 score has a deduction and repair condition; confidence separate from score; recommendation
is one of the allowed values; no acceptance probability; fixability and score-change conditions are
concrete; no forced disagreement.
