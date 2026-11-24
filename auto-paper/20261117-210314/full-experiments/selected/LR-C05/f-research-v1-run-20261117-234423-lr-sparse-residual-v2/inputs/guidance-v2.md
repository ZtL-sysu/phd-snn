# Research Guidance File

## Title / Topic

- Working title: Operator-Aligned Low-Rank Sparse Residual Coefficients for Frozen GNN-to-SNN Conversion
- Target field: graph compression, ANN-to-SNN conversion, neuromorphic graph systems
- Target venue: Q2+ journal / IEEE TNNLS-style method-system scope
- Technique/method: SVD transport plus sensitivity-selected sparse exact residual coefficients and matched rate-coded conversion
- Selected application scenario: Cora, Chameleon and Squirrel with frozen two-layer GCN teachers

## Core Idea

Transport an operator-aligned rank-k approximation of `A X`, then encode only a bounded sparse set of exact residual coefficients chosen by downstream sensitivity. The claim is about serialized coefficient transport and frozen rate-coded conversion, not asynchronous temporal spikes. Exact serialized-bit matching, strong compression baselines and end-to-end latency are mandatory.

### Mechanism-Level Rationale

- Domain bottleneck: raw `A X` message transport is large; generic low-rank or uniform residual coding may preserve the wrong directions.
- Why the technique fits: SVD aligns message-energy directions; downstream weight sensitivity ranks residual coefficients by effect on the hidden preactivation.
- Required adaptation: sparse exact residual coefficients, explicit factors/scales/index/value bits, and a rate-coded hidden conversion with task metrics.
- Novelty boundary: A²Q/AdaQP constrain quantization; One-Spike/ASGCN constrain graph conversion. The possible delta is downstream-sensitivity residual allocation at exact matched serialized cost. No claim is made for temporal event coding or energy.

## Paper Story

- Central scientific question: at exact matched serialized cost, do downstream-sensitivity residual coefficients improve frozen GNN→SNN task fidelity over strong low-rank/quantization adaptations?
- Intended reader: graph compression and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → candidate choice: high-dimensional repeated messages → retain operator-aligned rank and allocate sparse residuals by hidden sensitivity → evaluate task, MSE and full cost.
- Expected contribution type: conversion/compression method with equal-cost baselines and operator-sensitivity analysis.
- planned_claim: equal-serialized-bit improvement in hidden/logit MSE and teacher agreement.
- observed_finding: pending.
- Main claim: local static-graph frozen-conversion evidence only.
- Boundary: three graphs, three checkpoint seeds, two-layer GCNs, rate-coded conversion, no hardware-energy claim.
- Skeptical-reviewer hook: the decisive experiment is exact-bit end-to-end comparison against A²Q-style mixed precision, One-Spike-style coefficient coding, random projection, top-absolute residual and uniform residual.

## Paper Outline

1. Introduction: graph-message transport and frozen-conversion fidelity.
2. Related Work: One-Spike/ASGCN, A²Q/AdaQP, low-rank graph compression and rate-coded conversion.
3. Method: SVD/random projection/CUR-style bases, sensitivity residual ranking, serialized cost model, rate-coded conversion.
4. Experiments and Results: equal-bit baselines, hidden/logit MSE, task accuracy/agreement, ablations, warmed runtime/memory.
5. Discussion: what operator sensitivity adds, uncertainty, prior-art scope and limitations.
6. Conclusion: bounded result and requirements for broader conversion claims.

## Experiment Plan

### Datasets and splits

- Cora, Chameleon, Squirrel; fixed public validation masks; checkpoint seeds 0,1,2.
- No test-mask selection. Preserve all configurations and descriptive n=3 intervals.

### Baselines

- Full-float frozen conversion.
- SVD-only and random-projection rank-k.
- SVD/random basis plus top-absolute-residual coefficients.
- SVD/random basis plus random residual coefficients.
- Dense uniform residual at exact matched serialized bits.
- A²Q-style sensitivity-driven mixed-precision residual allocation at exact bits.
- One-Spike-style single-amplitude coefficient coding adaptation at exact bits; if official semantics cannot be reproduced, label adaptation and use a documented direct substitute.

### Proposed variants and required experiments

| ID | Matrix | Required controls | Primary metrics | Minimum | Binding expected-strong |
|---|---|---|---|---|---|
| LR-A | ranks 16/32/64/128, budgets 0.5/1/2%, 3 graphs×3 seeds | SVD/random/top-abs/A2Q-style/uniform | hidden MSE, logit MSE | finite rank curve | rank128 ≥8× dimension compression on ≥2/3 and ≥20% lower **hidden/logit MSE** than strongest exact-bit baseline on ≥2/3 |
| LR-B | T=2/4 frozen conversion | full float, equal-bit baselines | validation accuracy, teacher agreement | no catastrophic drop | ≥1 pp teacher-agreement gain over strongest exact-bit baseline on ≥2/3 graphs at T2 or T4 |
| LR-C | exact serialized cost | factors, scales, indices, values, encode/decode | total bits, coefficient count | exact same bits ±1% | ≥1 pp gain at matched bits or ≥2× fewer residual bits at matched agreement |
| LR-D | full-pipeline warmed runtime/memory | SVD-only and strongest baseline | encode/decode/selection/conversion latency, peak memory | finite | p95 full-pipeline ratio ≤1.2× at matched task fidelity; tail disclosed |
| LR-E | prior-art adaptations | A²Q-style and One-Spike-style | same task/cost metrics | adaptations runnable | proposed beats each adapted baseline on ≥2/3 graphs or novelty is explicitly narrowed |

### Metrics and statistics

- Hidden/logit MSE, message MSE, validation accuracy, teacher agreement, exact serialized bits, coefficient counts, full-pipeline wall latency and peak CUDA memory.
- Three seeds; mean, sample SD, paired seed deltas and descriptive bootstrap intervals (n=3).

### Runtime / hardware budget

- RTX3060 12GB, project Conda `dyg-cold`, local only.
- Warm-up 3 repeats; measure 7 repeats after SVD and for full encode/decode path separately.
- ≤45 minutes per batch and ≤12GB VRAM; fixed grids, no post-result expansion.

## Expected Results

- Minimum acceptable result: complete exact-bit curves and one task-fidelity advantage without cost inflation.
- Strong result: LR-A–LR-E binding targets.
- Failure signal: LR-A hidden/logit target miss, invalid cost matching, only message-MSE gain, prior-art adaptation match/beat, or runtime/memory contradiction.
- Strong-result entry gate: all repairs complete and all binding rows pass before writing.

## Figure/Table Decision Rules

- Figure 1: exact serialized sparse residual coefficient pipeline.
- Main table: exact-bit rank/budget/task/MSE results.
- Pareto figure: teacher agreement versus serialized bits.
- Ablation table: sensitivity vs top-absolute vs random vs A²Q-style allocation.
- Runtime/memory table: full encode/decode/selection/conversion.

## Traceability Checklist

Every LR-A–LR-E row must map to raw JSON, exact cost audit, code/config hashes and a manuscript table/figure decision. Include failed adaptations and uncertainty.

## Citation Scope

- Must-cite: One-Spike SNN, ASGCN, A²Q, AdaQP, DCGS, QCFS/FTBC, Fast-SNN and low-rank graph compression.
- Minimum 36 unique verified relevant references; majority from 2022–2026 inclusive.
- Duplicate audit by DOI/arXiv/normalized title/published version.

## Constraints and Preferences

- Deliver complete f-research-v1 TeX/PDF package and source archive.
- English manuscript; Chinese process logs.
- No commit/push/submission. All artifacts under the v2 run root.
- Proportionate length; one final PDF unless a verified venue limit applies.
