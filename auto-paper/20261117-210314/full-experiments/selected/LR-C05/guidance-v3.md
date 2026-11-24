# Research Guidance File

## Title / Topic

- Working title: Operator-Aligned Sparse Residual Coefficients for Logit-Faithful Frozen GNN-to-SNN Compression
- Target field: graph compression and frozen ANN-to-SNN conversion
- Target venue: Q2+ journal / IEEE TNNLS-style compression-method scope
- Technique/method: exact serialized-cost SVD transport with output-Jacobian-selected sparse residual coefficients
- Selected application scenario: Cora, Chameleon, Squirrel frozen two-layer GCN teachers

## Core Idea

Optimize logit fidelity under a strict serialized coefficient budget. The contribution is a fidelity/resource trade-off: output-Jacobian-selected sparse residual coefficients substantially reduce logit MSE at matched cost, while task accuracy is analyzed as a bounded-loss secondary outcome rather than claimed as universal improvement.

### Mechanism-Level Rationale

- Domain bottleneck: generic low-rank and uniform residual coding preserve the wrong output-sensitive directions.
- Mechanism: rank-k basis plus exact sparse residual coefficients selected by the squared norm of the full message→logit Jacobian.
- Required adaptation: exact factors/scales/index/value bits, rate-coded frozen conversion, A²Q-style and One-Spike-style adaptations.
- Novelty boundary: no temporal-event or energy claim; prior graph quantization/conversion work is respected through direct adaptations.

## Paper Story

- Central scientific question: can output-Jacobian residual allocation improve logit fidelity at exact serialized cost while keeping task degradation bounded?
- Intended reader: graph compression and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → choice: transport bottleneck → output-sensitive sparse residual allocation → logit-fidelity/resource trade-off.
- Expected contribution type: compression method plus exact-cost conversion study.
- planned_claim: ≥20% logit-MSE reduction and bounded task loss at rank128/2%.
- observed_finding: pending migration/acceptance of v2/v3 evidence.
- Main claim: local static-graph logit-fidelity compression, not task superiority.
- Boundary: three graphs, three seeds, two-layer GCN, rate-coded conversion, no energy.

## Paper Outline

1. Introduction: why logit fidelity and exact transport cost matter.
2. Related Work: One-Spike/ASGCN, A²Q/AdaQP, low-rank compression, rate-coded conversion.
3. Method: basis transport, exact serialized ledger, output-Jacobian sparse coefficients, frozen conversion.
4. Experiments and Results: exact-cost MSE, task trade-off, prior-art adaptations, ablations, warmed cost.
5. Discussion: where fidelity improves, why task gains are limited, scope and limitations.
6. Conclusion: bounded fidelity/resource contribution and future requirements.

## Experiment Plan

### Datasets and splits

Cora/Chameleon/Squirrel, public fixed validation masks, checkpoint seeds 0/1/2, no test selection.

### Baselines

Full float; SVD-only; random projection; top-absolute/random/A2Q-style/One-Spike-style/uniform residual controls at exact padded bits.

### Required experiments

| ID | Matrix | Primary metric | Minimum | Binding expected-strong |
|---|---|---|---|---|
| LR-A | rank128, 2% coefficients, 3 graphs×3 seeds | logit MSE | finite | ≥20% lower logit MSE than strongest exact-bit baseline on ≥2/3 graphs |
| LR-B | T2/T4 task trade-off | accuracy/teacher agreement | no collapse | worst task loss ≤3 pp vs strongest exact-bit baseline; report all negative deltas |
| LR-C | exact serialized ledger | total padded bits | exact ±1% | Pareto dominance in logit MSE at matched bits |
| LR-D | warmed full-pipeline cost | latency/peak memory | finite | p95 ≤1.2× SVD-only at matched fidelity |
| LR-E | prior-art adaptations | same metrics | runnable | proposed logit-MSE gain survives A²Q-style/One-Spike-style controls |

### Metrics and statistics

Message/hidden/logit MSE, accuracy, teacher agreement, exact bits, coefficient count, warmed latency/memory; three seeds, sample SD and descriptive paired bootstrap.

### Runtime / hardware budget

RTX3060 12GB, project Conda `dyg-cold`, 3 warmups + 7 repeats, ≤45 minutes per batch, fixed grid.

## Expected Results

- Minimum: complete exact-cost curves and bounded task trade-off.
- Strong: LR-A–LR-E above.
- Failure: <20% logit gain, task loss >3 pp, cost mismatch, prior-art adaptation match/beat, or runtime failure.
- Writing gate: v2/v3 raw evidence and timing migrated, reverified and accepted before manuscript.

## Figure/Table Decision Rules

Figure 1 exact serialized Jacobian-residual pipeline; main MSE/cost table; task trade-off figure; prior-art/ablation table; warmed cost table.

## Traceability Checklist

Every row maps to v2/v3 raw JSON, exact cost audit, timing JSON, code hashes and manuscript placement. Preserve all failed v1/v2 attempts.

## Citation Scope

Minimum 36 unique verified references, majority 2022–2026; must-cite One-Spike, ASGCN, A²Q, AdaQP, DCGS, QCFS/FTBC, Fast-SNN; full DOI/arXiv/title duplicate audit.

## Constraints and Preferences

English paper, Chinese logs; complete TeX/PDF/source package; no commit/push/submission; one final PDF; all artifacts under the v3 run root.
