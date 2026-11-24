# S1 design note (before implementation)

Status: **design frozen, code not yet written.** P2 has passed; S1 is the next gate and the task
book calls it the single experiment that decides the paper's direction. Branch C or D stops the
campaign and reports to the author (task book GP; contract C2).

## Critical implementation finding from the reaccepted kernel

The copied `experiments/core.py` already exposes `l1_mode="tpp"` inside `convert()`:

```
p = np.clip(us[l], 0.0, th_l) / th_l
s = (rng.random(us[l].shape) < p).astype(np.int8)
```

This is a **single-stage membrane-proportional Bernoulli** neuron, not ICML'25's two-phase TPP
(accumulate past threshold, then fire with a probability that increases with time). The frozen
task-book TPP numbers (Cora 0.7756 / CiteSeer 0.6457 / PubMed 0.7427 at T=8) were most likely
produced by this simplified variant. Two consequences, both mandatory:

1. **Unit test first.** Run `convert(..., l1_mode="tpp", T=8)` on the 7-seed Cora ANNs and check
   the mean against 0.7756 ± 0.5 pp. If it matches, this is the calibrated transplant; record it
   as a *simplified* TPP and never claim to have run the official implementation.
2. **Faithful two-phase TPP as a robustness arm.** Implement from ICML'25 equations (8)–(13): an
   accumulation phase, then a firing phase whose Bernoulli probability increases with `t`. Run it
   as a second transplant arm at least on Cora, T∈{4,8}, and report both. This closes the
   "straw man" concern (concern A3) instead of relying on a simplification that a reviewer could
   call unfair.

The official TPP-SNN repository states the full codebase is "coming soon" and ships no
checkpoints, so neither arm can be presented as a reproduction of their code. Both are
re-implementations, with source equations and commit recorded.

## S1-a — inter-layer permutation (their Fig.1 on graphs)

`core.convert()` propagates `prev` within a single timestep, so a cross-layer *time* permutation
cannot be expressed by simply shuffling `us`. The probe therefore needs a replay simulator that:

1. records the first hidden layer's spike train as `(T, N, H)` for each of K=5 permutation seeds;
2. applies a random permutation along the T axis **per unit** (matching their "randomly rearrange
   the spike train after each layer");
3. replays the permuted train through the same aggregation and readout.

Expectation from the companion's order-invariance result: the output membrane accumulator
`acc_out = Σ_t (Â(s_t M) + b)` has no `t` inside it, so a pure time permutation should leave
accuracy unchanged (0.000 pp spread). That would land in **branch B** — exactly the useful
outcome, because it says the image-domain cross-layer phenomenon does not transfer to graphs.
The count decoder must be measured as a positive control so that "no effect" is not an artefact
of an insensitive metric.

## S1-b — intra-aggregation phase randomisation (our phenomenon)

A plain `adj @ spikes` sum is order-invariant by construction, so "shuffling the accumulation
order" alone would be a no-op and would prove nothing. The physically meaningful operation is to
give **each neighbour's contribution a random arrival phase inside the same aggregation window**:
expand the spike tensor along a phase axis, jitter each edge's contribution by a bounded random
delay, and integrate. That changes which spikes fall inside the T-step window and therefore the
per-node quantized rate, which is what the identity `B̂_l − B_l = (1−α)Â(E_{l−1}M_l)` predicts.
The probe must record the phase seed, the jitter support, and a no-jitter control.

**Pre-registered expectation:** this arm is worse, by more than 2× the 0.4 pp noise floor, at
T≥2. If it *improves* accuracy, branch D is triggered and the mechanism explanation must be
rewritten — stop and report.

## S1-c — four-way control

| # | neuron | bias | purpose |
|---|---|---|---|
| 1 | IF | none | floor |
| 2 | IF | `β*` | this paper's method |
| 3 | TPP (simplified + faithful arms) | none | their method |
| 4 | TPP | `β*` | orthogonality check; expectation ④ ≥ ③ |

T∈{2,4,8,16}, three graphs, 7 seeds, mean±std. Pre-registered expectation: ③ > ① but
significantly below ②; ④ ≥ ③. GP requires TPP ≥1.5 pp behind at T=4 and branch A or B.

## 2×2 crossed design

`{inter-layer permutation on/off} × {intra-aggregation phase randomisation on/off}` on Cora first,
T∈{1,2,4,8}, then the full grid. The task book requires the two directions to be **physically
separated**, not merely defined differently; this table is that separation. Each cell writes its
own `run_id`, `perm_seed`, `probe` and `device` into `results.csv`.

## Execution order and stop rules

1. Unit-test the simplified TPP against 0.7756 ± 0.5 pp (one cell, Cora, T=8, 7 seeds).
2. Implement the faithful two-phase TPP and the two replay simulators; verify on a 1-seed Cora
   smoke grid before the full run.
3. Run the Cora-first S1 grid, then the full three-graph 7-seed grid in the background.
4. Decide the branch from the data. **No branch may be chosen by expectation.**
5. Branch C/D → write `notes/S1_probe.md` with the evidence, stop, report to the author; do not
   open S3 or P4.

Runtime estimate: one ANN per (graph, seed) is reused across all probe cells, so 21 trainings
(~3 minutes) plus cheap NumPy replays. No GPU is needed; CPU is the frozen device for these
paired arms.

## Traceability

Every S1 row carries `run_id`, seed, `perm_seed`, `probe`, `host`, `method_family`,
`is_transplant`, `neuron`, `bias_correction`, `t_steps`, `git_commit` (content-addressed),
`device`, and a `notes` field naming the TPP variant. Raw JSON and stdout logs go into `results/`
and `runs/`; nothing is deleted, including branch C/D outcomes.
