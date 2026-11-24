# Prior-art opportunity map

The portfolio uses public primary-source searches recorded in `../literature-baseline-matrix.md`. The opportunity map separates already occupied families from narrow conversion gaps:

- Occupied: generic ANN→SNN conversion, GCN conversion (One-Spike), event-graph conversion (ASGCN), generic signed spikes, graph quantization, direct spiking dynamic/equivariant/transformer GNNs, generic transformer conversion and SNN early exit.
- Open/under-tested in the search scope: causal frozen temporal-graph residual conversion; E(3)-preserving frozen conversion; conversion-level permutation certificates; signed graph-message banks; operator-aligned low-rank/weighted edge messages; graph-aggregation error certificates; hop-positional conversion; delay-aligned residual schedules; top-two graph-readout events.
- Mandatory direct baselines: One-Spike and ASGCN adaptations; A²Q/AdaQP for message compression; SpikeZIP/ECMT for positional conversion; SEENN/AdaFire for confidence mechanisms.
- Dataset/benchmark opportunities: local heterophilic Chameleon/Squirrel, Planetoid, OGBN-Arxiv, DAVIS-2017, MaleCNS coordinates and FlyWire edge weights. Dynamic-edge and molecular/protein datasets remain public-data gaps for full papers.

This is not an absolute novelty proof. It is a source-bounded opportunity map for idea selection.
