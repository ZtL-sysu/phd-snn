# Manuscript outline (three claims per section, with evidence dependencies)

Written before drafting, as required by the task book's writing order. All numbers are supplied by
`tex/numbers.tex`, generated from `results/*.json`; the outline contains no numeric claim.

## 1 Introduction
1. Graph SNN work is dominated by direct training and has no conversion error theory; the only mechanistic account of low-timestep conversion error concerns cross-layer stochastic rearrangement.
2. On graphs the error is generated inside one neighbourhood aggregation, is deterministic, and is amplified by the aggregation row sum; a controlled probe separates the two phenomena.
3. An exact identity yields a usable bound, and inverting the bound yields a timestep-allocation rule that a practitioner can compute from trained weights.
Dependencies: `s1_probe.json` (probe 2x2, four-way), `c3_allocation.json`, `c3_fit.json`, `tpp2025`, `sgnnbench2025`.

## 2 Related Work
1. Conversion error theory (QCFS, FTBC, TPP and 2024--2026 extensions) is expectation- or norm-based and image-specific.
2. Spiking GNNs are directly trained; SGNNBench has no conversion entry; published numbers use heterogeneous protocols.
3. The three-line contrast table, the FTBC attribution and the anonymous companion division of evidence fix the paper's position.
Dependencies: `refs.bib` (55 verified works), `notes/G0_literature_map.md`, `notes/G0_source_conflicts.md`.

## 3 Method
1. The aggregation operator sits inside the exact per-layer identity; Theorem G1 (a)--(d) follows.
2. The closed-form bias cancels the deterministic system term; the membrane readout is order-invariant and needs no randomness.
3. Inverting the bound gives kappa and the frozen scalar c, hence a predicted minimum timestep per model; three plug-in hosts and hardware implementability follow.
Dependencies: Appendix A proof, `contracts/pre-registration-c3.md`, `results/table1.json` hosts block.

## 4 Experiments and Results
1. Protocol, G0 reproduction and the full Table 1 grid, including the unfavourable T=2 cells.
2. Mechanism separation (2x2 probe, faithful L=3 replay, four-way neuron control) and the held-out T* allocation result.
3. Plug-in hosts, Pareto shape, and the retained negative controls.
Dependencies: `table1.json`, `s1_probe.json`, `c3_allocation.json`, `registry/results.csv`, `figures/*.pdf`.

## 5 Discussion
1. Evidence boundaries: two-layer transductive scope, proxy efficiency metrics, modest ANN backbone.
2. External comparability, protocol differences, and the relation to probabilistic neurons.
3. Threats to validity: calibration of c, margin proxy, frozen device, companion priority.
Dependencies: `audits/reaccepted-assets.md`, `runs/device_check.log`, `notes/G0_source_conflicts.md`.

## 6 Conclusion
1. Graph conversion error is an exact algebraic object with the aggregation operator inside it.
2. The four-part theorem turns the identity into a bound; inverting it removes the timestep sweep.
3. The correction is deterministic, needs no randomness, and plugs into standard aggregations.
Dependencies: all of the above; no new claim.

## Appendix
Proof of Theorem G1 with symbol table and failure depth; frozen protocol table; per-seed standard deviations; negative controls with mechanisms.
