# Story strength audit

## Why a skeptical top-tier reviewer should care

The ANN→SNN conversion literature has an exact error theory for images and a growing benchmark
literature for spiking GNNs, but nothing in between: SGNNBench evaluates nine spiking-GNN methods
and contains no conversion entry. A reviewer who works on low-latency SNNs should care because
choosing the timestep budget T is currently an empirical sweep, and the only mechanistic account of
why low T fails (ICML 2025) concerns a random cross-layer rearrangement that a deterministic graph
aggregation does not have. This paper says the graph case has a **different** error source, writes
it exactly, and turns the resulting bound into a rule that predicts T from trained weights.

The claim is not "we are more accurate". It is "the error has a structure you can compute with,
and here is the experiment showing the computation transfers to graphs you did not fit on".

## Strongest incrementality threat

Two, in order of severity:

1. **The same project's anonymous companion manuscript.** It already owns the exact identity,
   `β*=θ/(2T)`, the order-invariant membrane readout, the Pareto and an empirical `G^0.95` depth
   law. Its `ccf-paper-reviewer` terminal review scored **8** and said explicitly that a later
   result raising Quality and Evidence to 5 did not move the score because it verified a
   configuration the paper already used rather than adding a capability. A third manuscript that
   only reframes the same identity against ICML 2025 is, in that reviewer's words, "a second venue
   for the same result".
2. **FTBC (ECCV 2024)** already calibrates a forward temporal bias. A reviewer may ask whether
   `β*` is a rediscovery. The distinction must be exact (not expectation-level), graph-specific
   (`ρ_n`-weighted), and explicitly attributed.

## The exact experiment that distinguishes this work

The pre-registered held-out `T*` allocation (claim C3): fit the bound's constants on three fitted
graphs, commit them, and then — without re-fitting — predict the minimum timestep for ogbn-arxiv
and chameleon and verify that a per-layer allocation reaches a 1.5 pp target with ≥25% fewer
timesteps than a matched uniform-T budget. Two controls make it decisive rather than post-hoc:
a uniform-T arm with the **same total timestep budget**, and a shuffled-`ρ_n` arm that keeps the
bound's constants but destroys the geometric signal. The companion paper cannot answer this
question because it has no L-layer closed form and no inversion.

The 2×2 probe (claim C1) is the second discriminator: it converts "your misalignment is just our
misalignment on graphs" from a definition dispute into a measurement with opposite signs.

## Result threshold for a strong paper, not a runnable demo

- S1 lands in branch A or B with the TPP transplant ≥1.5 pp behind at T=4.
- Zero L≤4 bound counterexamples (or an explicit failure-depth condition) with mean conservatism
  3×–8×.
- On ≥3/3 held-out graphs, predicted `T*` within one T-grid step and ≥25% timestep savings at
  matched accuracy, with the matched-budget control failing.
- ≥3 reproduced direct-training arms and no dominated T≤4 conversion point.
- Final `ccf-paper-reviewer` full-mode calibrated stance **≥ 9**, measured only by the skill.

A paper with only the first and fourth items is a competent 8-score conversion paper. The
second and third items are what change the Significance axis.

## If the result is only partially positive

- `T*` fails the held-out criterion → keep the exact bound, the mechanism separation and the
  negative controls; pivot within the same method family to a **bound-derived model-selection
  rule** (choose which pretrained GNN converts within ε at a given T) and publish the failed
  allocation with its mechanism. Honest, still publishable, lower tier.
- The bound fails at L=4 → state the failure-depth condition as a result; the companion showed a
  well-characterised negative result is acceptable when the mechanism is explained.
- Direct-training arms cannot reproduce → apply the task-book 5-day stop-loss with labelled
  SGNNBench numbers; narrow the Pareto claim rather than deleting the row.
- S1 lands in branch C or D → stop and report per GP; the mechanism story needs redesign, not a
  softer wording.

In every case negative results stay in `notes/` and `results.csv`, the four publicly stated
assertions are either supported or explicitly falsified, and no target is quietly lowered.

## Agreement with the strong-result feasibility contract

This audit promises no experiment absent from `ccfa-startup-packet/strong-result-feasibility-contract.md`.
The capability target, its baselines (uniform-T, grid oracle, matched budget), its seed budget
(7), its prototype milestone (6/9 fitted cells), its compute budget (30 h, 10 GB, 90 trials) and
its stop–return condition all appear there and in `feasibility-contract.json` claim C3. The
framework figure and the data plots are decided after evidence stabilizes, as the guidance's
figure/table decision rules require.
