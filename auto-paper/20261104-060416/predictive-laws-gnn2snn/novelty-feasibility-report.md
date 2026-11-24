# Novelty and feasibility report

**Verdict: novel at the formulation level, with an explicit boundary.**

## What is not ours

- The mechanism of a constant forward bias cancelling the systematic rate-code deficit belongs to
  FTBC (ECCV 2024). We inherit it and say so in Related Work and again in the discussion.
- The term "temporal misalignment" belongs to the ICML 2025 conversion paper. We use it only to name
  the object we then show is *different* from theirs.
- ANN→SNN conversion for feed-forward networks is 5+ years old.

## What we claim, and against what

| claim | nearest prior work | why it is not there |
|---|---|---|
| Conversion error obeys an exact recursion at any depth on a graph | feed-forward bounds; graph conversion papers report accuracy only | no graph conversion paper writes the recursion; the 2025 and 2024 works are for dense layers where the input is not a neighbourhood average |
| Fidelity is *predictable* from trained weights before simulation | none found in either conversion or spiking-GNN literature | the closest work is bound-based and never evaluates a prediction on held-out configurations |
| Depth is not survivable, and the cumulative spectral gain says by how much | conversion papers report 2 layers; GCNII/DAGNN literature discusses depth for the ANN, not for its conversion | the exponent 0.948 at r = 0.990 is a measurement nobody has reported |
| The membrane decoder is exactly order-invariant while the count decoder is not | the 2025 paper attributes a benefit to reordering, on a stochastic neuron | with a sum readout the accumulator has no `t`; this is a proof plus a 2×2, and it separates the two objects |
| Sparsification buys synaptic operations but not spikes, at a measured exchange rate | energy claims in spiking-GNN papers are usually modelled, not measured | we report the exchange rate including the case where it fails the gate we set |

## Search evidence

arXiv `abs:"spiking" AND abs:"graph neural network"` returns 33 records, all inspected:
SpikingGCN, SiGNN, DGSNN, SpikeGraphormer, continuous spiking GNN, geometry-aware, Riemannian, Loihi
deployment, heterogeneous spiking GAT, hybrid variable-spiking, photonic spiking GNN, anomaly
detection, SGNNBench. Every one is trained, none analyses conversion. SGNNBench — the only unified
evaluation — has no conversion entry, which is positive evidence rather than an absence of search.

## Duplication risk and mitigation

Moderate on one axis: a reviewer may read "closed-form bias on a graph" as "FTBC with a graph in
front". The mitigation is structural, not rhetorical — the paper gives one paragraph listing exactly
what is inherited and what is not, and the ρ-invariance of the *relative* error is the technical
content that FTBC does not have.

Low on the predictive axis: we found no paper that predicts conversion accuracy from weights, in any
domain. This is the claim the title rests on, and it is the one the red team flagged as the only
route to the target tier.

## Feasibility

Every ingredient is already measured on this machine at 7 seeds: the recursion (residual 2e−6), the
amplification exponent (0.948, r = 0.990), the √H law (6 % stability), the order invariance (0.000 pp),
and the three external arms. What is missing is the *out-of-sample* prediction test and the Pareto
table, both of which are implemented work rather than speculative work.
