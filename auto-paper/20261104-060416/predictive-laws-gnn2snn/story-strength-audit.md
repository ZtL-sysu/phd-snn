# Story strength audit

## The skeptical reviewer's first question

*"I have seen conversion papers before. What do I now know that I did not?"*

The answer the paper must give in one sentence: **you can now tell, from a trained GNN's weights and
without running the conversion, how faithful that conversion will be and how many timesteps it needs
— and the two design choices you were making blind (depth, width) are decided by that number.**

This is a claim no conversion paper currently makes, in any domain. That is why it can carry the tier.

## The strongest paper that could make this look incremental

The 2025 ICML temporal-misalignment paper. A reviewer sympathetic to it will say: "they already
showed that the temporal structure of the spike train matters and that fixing it improves conversion;
this paper renames the same thing."

**The experiment that distinguishes them is already run.** Their effect requires a stochastic, leaky
neuron: reordering changes *which* spikes fire. With our deterministic IF neuron and a sum readout,
four different orderings leave the membrane accuracy unchanged to four decimals (0.000 pp spread),
while the count decoder — the one their framing implicitly assumes — moves by up to 1.6 pp. Two
objects, not two names. This must be Table 10 and must be discussed before Related Work makes the
comparison, so the reader is not left to guess.

Second-strongest: the FTBC line. Mitigation is a paragraph that lists what is inherited (the bias
mechanism) and what is not (the graph value `β* = θ/(2T)` when row sums ≠ 1, the ρ-weighting, the
ρ-invariance of relative error).

## What threshold makes this strong rather than runnable

Three numbers, all pre-registered in the feasibility contract:

1. Held-out prediction MAE ≤ 1.0 pp, required-`T` exact on ≥ 70 % of cells. Below this, the title is
   not defensible.
2. Not Pareto-dominated at `T ≤ 4` by any of three external arms on at least two of three graphs.
3. Membrane order spread ≤ 0.01 pp with count spread ≥ 0.3 pp in the same cells (already 0.000 vs
   0.4–1.6).

## If only part of it lands

- Prediction fails, Pareto holds → paper is "an exact error analysis of graph conversion, with an
  external benchmark". Still publishable; the title must lose "predictive". B tier.
- Pareto fails, prediction holds → paper is "a predictive theory, validated on our conversions, whose
  external comparison is a formulation-level approximation". Weaker, and the limitations section has
  to lead with it.
- Both fail → the four surviving results (identity, depth law, order invariance, sparsity exchange
  rate) form a diagnostic paper. That is the honest floor and it is what the second, third and fourth
  claims were chosen to protect.

## The one thing that would make the paper untrustworthy rather than weak

Deleting the external arm that beats us (the SpikingGCN architecture wins Cora 0.8169 and CiteSeer
0.7073 against our 0.8046 and 0.6907). It stays, with both readings: it is a different architecture
with more capacity per step, *and* a practitioner will read it as "the published architecture is
better there". Framing does not make the second reading false. The paper says both.

## Story strength verdict

**Adequate for CCF-A conditional on the two red-team conditions.** Not adequate as currently written
(the 17-page draft has no prediction test and no external table), which is exactly what this guidance
adds. No claim in the story requires a result we have not already measured, except the two that are
implemented work.
