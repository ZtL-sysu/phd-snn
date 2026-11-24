# Research Guidance File

## Title / Topic

- Working title: Operator-Aligned Low-Rank Residual Event Coding for GNN-to-SNN Conversion
- Target field: graph representation learning, ANN-to-SNN conversion, neuromorphic graph systems
- Target venue: Q2+ journal, with IEEE TNNLS / TNNLS-style systems-method scope as the working assumption
- Technique/method: low-rank graph-message transport plus sparse exact residual events inside frozen GNN→SNN conversion
- Selected application scenario: frozen two-layer graph GCN teachers on homophilous and heterophilous node-classification graphs

## Core Idea

Transport the dominant operator-aligned subspace of raw aggregated graph messages `A X`, then spend a bounded event budget only on the largest downstream-relevant residual components. The proposed method must be compared at matched average bit/event budgets against strong low-rank, quantization and residual controls, and evaluated through an actual frozen-conversion task rather than message MSE alone.

### Mechanism-Level Rationale

- Domain bottleneck: raw graph messages are high-dimensional and repeated across graph conversion ticks; generic compression loses downstream-relevant directions.
- Why the technique fits: SVD aligns the retained subspace with message energy and the downstream first-layer map can be used to prioritize residuals.
- Required adaptation: frozen GNN teacher, no spiking retraining; first aggregate `A X`, decompose, transmit low-rank coordinates plus sparse residual events, reconstruct hidden preactivation, then run matched rate/event conversion.
- Why this is more than applying low rank to a graph: the paper claims an operator-aligned residual-event allocation and a full conversion cost/fidelity trade-off under equal budgets.

## Paper Story

- Central scientific question: can operator-aligned low-rank residual events reduce graph-message traffic while preserving frozen GNN→SNN task accuracy better than strong equal-budget compression baselines?
- Intended reader: neuromorphic graph, GNN compression and ANN→SNN conversion researchers.
- Domain/theory problem → design requirement → candidate choice: repeated high-dimensional `A X` messages dominate transport; retain an operator-aligned subspace and allocate exact residuals by downstream sensitivity; compare end-to-end.
- Expected contribution type: conversion method plus resource/fidelity trade-off and operator-alignment analysis.
- planned_claim: the proposed low-rank+residual event coder improves accuracy-agreement at matched budget over SVD-only, random-projection+residual and uniform quantization.
- observed_finding: pending until P5.
- Main claim: a frozen-conversion method with explicit message bits/events, task fidelity and runtime/memory evidence.
- Boundary of the claim: local public node-classification graphs and frozen two-layer GCN teachers; no universal hardware-energy claim.
- Skeptical-reviewer hook: prior graph quantization/low-rank work exists, so the decisive result must be equal-budget end-to-end conversion, not a better reconstruction plot.
- Strongest competing paper and distinction: A²Q/AdaQP cover graph quantization/communication; One-Spike/ASGCN cover graph conversion. The proposed delta is operator-aligned residual-event allocation inside a frozen conversion pipeline with direct equal-budget controls.

## Paper Outline

1. Introduction: traffic bottleneck in graph conversion; why generic low rank is insufficient.
2. Related Work: One-Spike/ASGCN, A²Q/AdaQP, low-rank graph compression, rate/event conversion.
3. Method: operator-aligned decomposition, downstream residual scoring, sparse exact residual events, conversion and cost model.
4. Experiments and Results: three graphs×three seeds, T=2/4, equal-bit baselines, ablations, robustness, latency/memory.
5. Discussion: where operator alignment helps, failure modes, hardware scope and limitations.
6. Conclusion: evidence-backed trade-off and next-step requirements.

## Experiment Plan

### Datasets and splits

- Cora, Chameleon, Squirrel local public graphs and frozen two-layer hidden-16 GCN checkpoints.
- Checkpoint seeds 0, 1, 2 for each graph; fixed public validation masks for evaluation.
- Training-only message statistics and residual budgets; no test-mask selection. Preserve exact graph/checkpoint/data hashes.

### Baselines

- Full float `A X` and ordinary frozen GCN conversion.
- SVD rank-k without residual events.
- Random projection rank-k with identical residual budget.
- Per-channel uniform quantization at the same average bit budget.
- Strongest feasible graph-compression control: SVD plus uniform residual quantization at matched total bits.
- Proposed: SVD rank-k plus top-|downstream sensitivity| sparse exact residual events.

### Proposed method variants and required experiments

| ID | Matrix | Required ablations | Primary metric | Minimum | Binding expected-strong |
|---|---|---|---|---|---|
| LR-A | ranks 16/32/64/128, 3 graphs×3 seeds | SVD-only, random+residual, uniform quantization | reconstructed hidden/logit MSE | finite and monotone rank curve | at rank128, compression ≥8× on ≥2/3 graphs and proposed logit error ≥20% below strongest equal-budget baseline |
| LR-B | end-to-end frozen conversion T=2/4 | no-residual, random residual, downstream-scored residual | validation accuracy, teacher agreement | no worse than SVD-only | proposed teacher agreement ≥1 pp over strongest equal-budget baseline on ≥2/3 graphs averaged over seeds at T=2 or T=4 |
| LR-C | event/bit accounting | same total bits, same rank, same reconstruction path | average bits/message, residual events, peak memory | explicit finite budget | ≥2× fewer residual-event bits than uniform residual at matched accuracy or ≥1 pp accuracy at matched bits |
| LR-D | runtime/robustness | batch sizes, graph-size strata, rank perturbation | latency, memory, error quantiles | finite, no leakage | no >20% runtime regression versus SVD-only at matched reconstruction, or a documented trade-off with improved fidelity |

### Metrics and statistics

- Message/hidden/logit relative MSE, validation accuracy, teacher agreement, average bits per message element, residual event count, peak allocated memory, wall latency.
- Three checkpoint seeds; report mean/sample SD and paired bootstrap 95% CIs. Tune ranks/budget on training/validation only.

### Runtime / hardware budget

- Local Conda `dyg-cold`, RTX 3060 12GB, 32GB RAM; CUDA for decompositions/probes, immutable `core.convert` may use CPU reference.
- ≤30 minutes per batch, ≤12GB VRAM, ≤12 configurations per seed; no remote compute.
- Frozen split IDs and complete trial ledger; no post-result grid expansion.

## Expected Results

- Minimum acceptable result: complete equal-budget curves and at least one graph where proposed residual allocation improves fidelity without exceeding SVD-only runtime by >20%.
- Strong result: LR-A/B/C binding rows above.
- Failure signal: no equal-budget advantage, gain only against random projection, reconstruction improvement without teacher agreement, or budget/runtime contradiction.
- Strong-result entry gate: every row complete and claim narrowed to observed evidence; a failed row blocks success wording.

## Figure/Table Decision Rules

- Figure 1: operator-aligned low-rank residual event pipeline, generated after method freeze.
- Result table: rank/budget/accuracy-agreement trade-off across graphs/seeds.
- Figure: Pareto accuracy vs average bits and residual events; error-vs-rank curves only if they clarify operator alignment.
- Ablation table: SVD-only/random/uniform/proposed at matched budgets.
- No energy claim from bit/event counts.

## Traceability Checklist

Every LR-A–LR-D row must map to raw JSON, protocol, code hash and a table/figure decision. Include failures and all seeds.

## Citation Scope

- Must-cite: One-Spike SNN, ASGCN, A²Q, AdaQP, Fast-SNN, DCGS, QCFS/FTBC and graph low-rank/quantization foundations.
- Search keywords: GNN ANN-to-SNN conversion, graph message compression, low-rank graph, residual event coding, neuromorphic graph.
- Recency: 2021–2026 with foundational conversion references.
- Duplicate risks: arXiv/published versions of One-Spike, DCGS and graph quantization papers; verify DOI/arXiv/title.

## Constraints and Preferences

- Final deliverables: complete f-research-v1 TeX/PDF paper package, source archive and evidence bundle.
- Chinese process logs; English manuscript.
- No commit/push/submission. All run artifacts under this guidance directory's run root.
- Page policy: proportionate to evidence; no numeric target unless a current venue limit is verified.
