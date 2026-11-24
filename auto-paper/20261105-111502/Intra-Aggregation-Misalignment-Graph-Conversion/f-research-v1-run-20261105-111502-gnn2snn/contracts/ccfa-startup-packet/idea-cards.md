# Idea cards (`ccf-idea-optimizer`, standard mode)

**Target venue and assumptions:** CCF-A main ML track, ICML/NeurIPS family. Working assumption:
8-page main text + unlimited references/appendix, double blind, official LaTeX style (ICML 2026
rules; 2027 CFPs unpublished). Field: spiking neural networks / graph learning. Idea stage:
mechanism and evidence plan fixed, experiments not yet run.

**Mode and development stance:** standard, `accept-to-develop` with two binding repairs (a genuine
new capability, and a same-group overlap declaration). Novelty is treated as grounded only for the
public literature (`notes/G0_literature_map.md`); companion-manuscript overlap is an author-owned
risk, not a literature claim.

**Raw idea diagnosis:** "do the GNN→SNN conversion paper again, but frame it against ICML'25" is
not a contribution. Subtracted: the exact identity, `β*=θ/(2T)`, the membrane decoder, the Pareto,
the audit grid — all already owned by companions A/B. What remains after subtraction is (i) a
controlled physical separation of two *different* misalignment phenomena, (ii) a `ρ_n`-weighted
L-layer bound with a mandatory bias term that the image-domain bound lacks, and (iii) a bound-derived
deployment rule. Those three are the paper.

## Optimized idea card (C1, selected)

| field | content |
|---|---|
| Problem | ANN→SNN conversion on graphs loses accuracy at low T, and the field's only mechanistic account (ICML'25) locates the cause in cross-layer temporal misalignment and fixes it with stochastic neurons. Graph conversion has a different, deterministic error source that no image-domain bound describes. |
| Gap | No published work gives a graph conversion error identity with the neighbourhood aggregation operator inside it; no bound contains the adjacency row sum `ρ_n`; no conversion method allocates timesteps from a bound. |
| Root challenge | A unit's input is a sum over neighbours that fire at different times; the layer therefore integrates a locally time-scrambled, per-node quantized rate. Its expectation has a systematic bias that stochasticity cannot remove. |
| Insight | Write the per-layer error exactly as `B̂_l − B_l = (1−α)Â(E_{l−1}M_l)`. The aggregation operator `Â` is inside the identity, so the bound must contain `ρ_n` and a `β*` system term — features absent from `‖W‖∞·θ/T`. The same identity gives `T_L`, which can be **inverted** into a per-layer timestep budget. |
| Method | (1) S1 three probes; (2) Theorem G1 (a)–(d); (3) bias + membrane decoder + three aggregation hosts; (4) `T*` allocation from G1(d) with held-out validation. |
| Expected evidence | branch A or B on S1; TPP transplant > 1.5 pp behind at T=4; zero L≤4 counterexamples; ≥3 held-out graphs where bound-predicted `T*` reaches target accuracy with fewer steps than a uniform-T baseline; never-dominated T≤4 Pareto. |
| Limitation | two-layer transductive backbone, spike/SynOps proxies rather than measured energy, protocol differences in external baselines, no claim of beating ICML'25. |
| Innovation type | theory + empirical finding + method (a deployment rule), **not** a new architecture. |
| Contribution type declared | mechanism separation + bound-derived capability. Priority claim intentionally not reused. |

## Candidate concretizations (diversity pass)

| id | angle | mechanism | evidence type | venue fit | decision |
|---|---|---|---|---|---|
| C1 | mechanism separation + bound-derived latency allocation | exact identity → `ρ_n` bound → invert `T_L` | controlled probes + held-out prediction | strong | **selected** |
| C2 | pure reproduction/benchmark paper on graph conversion | survey + unified protocol | benchmark table | weak for main track | rejected — companion A already owns the audit, and a table alone scores 7–8 |
| C3 | a new stochastic neuron for graphs | probabilistic firing tuned to `ρ_n` | accuracy SOTA race | weak | rejected — contradicts the deterministic-mechanism claim and the "no SOTA" rule |
| C4 | deeper/wider backbone accuracy push | GCNII / DAGNN with conversion | leaderboard | weak | rejected — task book forbids accuracy SOTA spending before G5; companion B already showed depth hurts |
| C5 | theory-only paper with no new experiments | proof + counterexample search | proof | medium | rejected — the user's pipeline is empirical; a theorem without held-out validation repeats B's Significance problem |

Internal-consistency check: C3 and C4 contradict C1's deterministic and low-latency framing; C2/C5
lack a new capability. No theme drift remains in C1.

## Problem statement

Given a trained L-layer GNN and a target conversion error ε, decide (a) whether the dominant error
is the cross-layer stochastic phenomenon of ICML'25 or an intra-aggregation deterministic one, and
(b) the minimum timesteps `T*` per model/layer that achieve ε — without running the full T grid.

## Method blueprint

1. Derive `E_l` recursion under a general normalized aggregation `Â` with row sums `ρ_n`; prove
   `‖E_L‖ ≤ f(ρ_n, ‖D_W‖, θ, T, ‖E_l‖)` with the `β*` system term and an L-layer closed form.
2. Invert the closed form: from a target ε and measured `(ρ_n, G, margin distribution)` compute
   `T*`; allocate per-layer timesteps under a fixed total budget.
3. Falsify with (i) an adaptive-`ρ` control, (ii) a uniform-T matched-budget control, (iii) held-out
   graphs never used to fit constants, (iv) L∈{2,3,4} counterexample search.
4. Separate the two misalignments with the 2×2 probe design: cross-layer permutation on/off ×
   intra-aggregation phase randomization on/off.

## Reviewer-risk register

| risk | class | smallest repair |
|---|---|---|
| "just TPP on graphs" | requires-new-result | S1 2×2 + four-way TPP control, branch A/B |
| "verifies an existing setting, no capability" (companion B's M-B1) | requires-new-result | **binding held-out `T*` allocation experiment** |
| "same group's third paper on one identity" | evidence-fixable | anonymous companion + division of evidence + no reused "first" claim |
| "no released TPP code, so the transplant is a straw man" | design-fixable | re-implement from equations (8)–(13), unit-test against frozen T=8 numbers, publish the diff |
| "external baselines use different protocols" | writing-fixable | protocol column + task-book 5-day stop-loss + SGNNBench labelled context rows |
| "bound is loose / only 2 layers" | evidence-fixable | bound/measured conservatism table, L≤4 counterexample search, explicit failure depth |
| "energy claim" | venue-mismatch | spike/SynOps proxies only, positive evidence boundary in Discussion |

## Rescue routes and suggested pivots (within the same method family and tier)

- If S1 lands on branch C or D → stop and report (task book GP), then repair via the correction
  loop: narrow the mechanism to the surviving probe, never quietly rewrite `β*`.
- If `T*` allocation fails its held-out criterion → keep the exact bound and the negative result,
  and pivot the capability to a **bound-derived model-selection rule** (choose which pretrained GNN
  converts within ε at a given T), still a practitioner-usable capability but with a lower ceiling.
- If ≥3 direct-training arms cannot run → apply the task-book stop-loss with labelled SGNNBench
  numbers, retaining the internal four-arm Pareto.

**Closest-work / novelty unknowns:** public-literature sweep completed (`notes/G0_literature_map.md`);
unsearched: non-arXiv full-text proceedings, post-2026-11 work, and the companion manuscripts'
eventual public versions. Novelty confidence: medium-high, not absolute.

**Checklist status:** 11/11 mandatory items completed; missing inputs (venue CFP, TPP code,
checkpoints) named rather than guessed.

**Optional next-module decision:** `ccf-literature-searcher` (opportunity map) then
`ccf-idea-reviewer` (red team), then `ccf-experiment-designer` (claim-evidence contract).
