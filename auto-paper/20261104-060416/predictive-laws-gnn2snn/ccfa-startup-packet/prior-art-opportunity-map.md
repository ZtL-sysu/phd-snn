# Prior-art and opportunity map

Search date 2026-11-04. Two independent sweeps: arXiv API `abs:"spiking" AND abs:"graph neural
network"` (33 hits, all inspected by title+abstract) and targeted keyword searches for conversion
*theory* (feed-forward), for the two mechanism ancestors, and for the benchmark papers.

## Cluster 1 — trained spiking GNNs (the competing family). 12 works, all direct-training.

| work | venue/year | what it does | relevance to us |
|---|---|---|---|
| SpikingGCN, Zhu et al. | IJCAI 2022 | SGC-style propagation + spiking FC, rate decoding | the canonical formulation we re-implement as an external arm |
| SiGNN, Chen et al. | arXiv 2404.07941, 2024 | spike-induced dynamic-graph representation | direct-training, different task (dynamic) |
| DGSNN / Dynamic Spiking Framework, Yin et al. | AAAI 2024 | dynamic spiking graph nets | direct-training |
| SpikeGraphormer, Sun et al. | arXiv 2403.15480, 2024 | spiking graph attention/transformer | direct-training |
| Continuous Spiking GNN, Fan et al. | arXiv 2404.01897, 2024 | ODE-style continuous spiking propagation | direct-training |
| Geometry-Aware Spiking GNN, Zhang et al. | arXiv 2508.06793, 2025 | geometry-aware spiking propagation | direct-training |
| Spiking GNN on Riemannian Manifolds, Sun et al. | arXiv 2410.17941, 2024 | manifold-valued spiking GNN | direct-training |
| Transductive Spiking GNN for Loihi, Snyder et al. | arXiv 2404.17048, 2024 | hardware deployment | deployment, not conversion |
| Spiking Heterogeneous GAT | arXiv 2601.02401, 2025 | heterogeneous graphs | direct-training |
| Hybrid variable spiking GNN, Jain et al. | arXiv 2412.09379, 2024 | energy-efficient SciML | direct-training |
| SGNNBench, Zhang et al. | arXiv 2509.21342, 2025 | unified evaluation of trained spiking GNNs | **the external protocol we align to**; contains no conversion method |
| Neuromorphic graph anomaly detection | arXiv 2605.13863, 2026 | STDP + spiking GNN | application |

**Gap confirmed:** none of the 33 hits analyses conversion error, and SGNNBench — the largest
unified evaluation — has no conversion entry at all. The absence is a *positive* datum (a benchmark
that searched for methods did not find one), not merely "we did not find it".

## Cluster 2 — conversion theory for feed-forward networks (the mechanism ancestors)

| work | venue/year | what we inherit |
|---|---|---|
| FTBC: forward temporal bias correction, Wu, Bojković, Gu et al. | ECCV 2024 | the mechanism of a constant forward bias cancelling the systematic rate-code deficit |
| Temporal Misalignment…, Bojković, Wu, Gu | ICML 2025 | the term "temporal misalignment" for the *cross-layer* shuffle; TPP neuron |
| Optimal threshold / potential initialisation, Bu et al.; Deng & Gu | ICML 2021; IJCAI 2021 | the `1/(2T)` floor-deficit analysis for ReLU-IF |

**Boundary we must state explicitly:** the bias *mechanism* is FTBC's. Ours is the graph-specific
value `β* = θ/(2T)` when row sums are not one, the ρ-weighting, and the ρ-invariance of relative
error. A reviewer who knows FTBC must be able to see in one paragraph what is inherited.

## Cluster 3 — what is genuinely absent (the opportunity)

1. **No predictive theory of conversion fidelity for graphs.** The feed-forward analyses bound the
   error; none turns the bound into a *prediction of accuracy loss from trained weights*. A
   prediction is falsifiable in a way a bound is not, and it is what a practitioner needs to choose
   a backbone.
2. **No depth statement.** Conversion papers report one or two layers and do not say what happens at
   four. We have the recursion and a measured exponent (0.948, r = 0.990).
3. **No separation of ordering from quantisation.** The field uses "temporal misalignment" for a
   cross-layer shuffle whose effect requires a stochastic neuron; we show that with a sum readout
   the ordering is *exactly* invisible, so the two phenomena are different objects and only one of
   them exists here.
4. **No honest energy accounting at matched accuracy.** We have the exchange rate.

## Current strongest baselines and their code status

| baseline | code | checkpoint | rerun feasible locally |
|---|---|---|---|
| SpikingGCN (IJCAI'22) | public repo (Python 3.6, graphgallery 0.7.2) | none | **no** — dependency-pinned to an unavailable stack; we re-implement the *formulation* instead and say so |
| SiGNN (2024) | public repo | none | no — dynamic-graph task, different splits |
| direct BPTT spiking GCN | our own reference implementation | n/a | yes (already run, 7 seeds) |
| rate-coded (Poisson) formulation | our own | n/a | yes (already run, 7 seeds) |
| SGNNBench numbers | benchmark paper | none | literature context only, protocol differs |

The honest position: two of three external arms are *formulation-level re-implementations*, one
(SpikingGCN-architecture) is a re-implementation of a published architecture, and the benchmark
numbers are literature context. The guidance forbids claiming a codebase-level reproduction; it
requires saying which is which in the table caption.
