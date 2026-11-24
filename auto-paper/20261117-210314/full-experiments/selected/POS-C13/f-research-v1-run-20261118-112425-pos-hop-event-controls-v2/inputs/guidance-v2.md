# Research Guidance File

## Title / Topic

- Working title: Permutation-Equivariant Hybrid Hop-Event Coding for Frozen Graph Positional Messages
- Target field: graph positional representation compression and frozen GNN-to-SNN conversion
- Target venue: Q2+ journal / IEEE TNNLS-style graph-neuromorphic scope
- Technique/method: exact multi-hop positional features, node-permutation audit, shuffled-hop control, and 8-level Lloyd codebooks with 0.5% exact escapes
- Selected application scenario: Chameleon and Squirrel static graph node classification with frozen local graph snapshots

## Core Idea

Multi-hop positional messages preserve structural information but are expensive to transport. The contribution is a narrow conversion-level representation study: concatenate raw features with one-, two- and three-hop normalized messages, quantize hop channels using an 8-level Lloyd codebook plus 0.5% exact escapes, and certify node-permutation equivariance. A shuffled-hop ablation tests whether ordered hop blocks carry information beyond the same values in an arbitrary order.

### Mechanism-Level Rationale

- Domain bottleneck: multi-hop positional features are large and uniform/per-channel quantization alone loses tails or channel structure.
- Mechanism: a hybrid Lloyd codebook represents the mass of each channel distribution while exact escapes preserve rare hop values; hop blocks remain ordered and transform equivariantly under node permutations.
- Required controls: exact inverse-permutation audit, shuffled-hop representation/control, raw/uniform/per-channel baselines, five split/probe seeds and fixed-raw-probe transfer evaluation.
- Novelty boundary: conversion-level hop-message coding with explicit equivariance/order controls, not a new graph transformer, direct SNN training, broad transformer conversion, temporal dynamics, energy or hardware claim.

## Paper Story

- Central scientific question: can hybrid hop-event coding retain ordered multi-hop positional information at substantial storage reduction while remaining node-permutation equivariant and degrading under shuffled-hop controls?
- Intended reader: graph representation compression, graph transformers and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → choice: expensive hop messages → codebook plus rare-value escapes and exact permutation audit → compressed ordered positional representation.
- Expected contribution type: representation coding method plus equivariance/order-control study.
- planned_claim: hybrid coding has ≤5% relative representation error, ≥4× storage reduction, exact permutation equivariance, and shuffled-hop error at least 25% higher than ordered-hop error on both graphs.
- observed_finding: pending corrected multi-seed/control run.
- Main claim: ordered multi-hop message fidelity, storage efficiency and equivariance within the fixed two-graph protocol.
- Boundary: Chameleon/Squirrel, three hops, 8-level Lloyd plus 0.5% escapes, five split/probe seeds, no broad transformer-conversion or deployment claim.

## Paper Outline

1. Introduction: why ordered multi-hop positional messages need compression and conversion controls.
2. Related Work: graph positional encodings, graph transformers, quantized communication, ANN-to-SNN conversion and spiking graph models.
3. Method: hop features, hybrid codebook/escape encoding, bit ledger, permutation equivariance and shuffled-hop control.
4. Experiments and Results: representation error, storage, five-seed probe results, permutation and shuffled-hop ablations.
5. Discussion: what is established, prior-art overlap, negative results and limitations.
6. Conclusion: scoped hop-event coding result and requirements for real graph-transformer→SNN conversion.

## Experiment Plan

### Datasets and protocol

Chameleon and Squirrel from existing local snapshots. Construct `H=[X, A X, A^2 X, A^3 X]` with row-normalized `A`. Use split/probe seeds 600-604 and five fixed node/hop-shuffle permutation seeds.

### Methods and controls

- Raw float32 features.
- Global 8-level uniform quantization.
- Per-channel 8-level Lloyd quantization.
- Hybrid per-channel 8-level Lloyd plus 0.5% exact escapes.
- Ordered-hop versus within-node shuffled-hop controls.
- Node-permutation equivariance: permute nodes/graph, recompute features and encoding, inverse-permute, compare with original.
- Fixed-raw-probe transfer: fit the probe on raw features and evaluate raw/encoded/ordered/shuffled representations without retraining; separately report retrained-probe results.

### Required experiments

| ID | Matrix | Primary metric | Binding expected-strong |
|---|---|---|---|
| POS-A | 2 graphs × 5 split seeds × raw/uniform/Lloyd/hybrid | balanced accuracy | hybrid mean loss versus raw ≤2 pp on both graphs |
| POS-B | 2 graphs × hybrid | representation relative Frobenius error | ≤5% on both graphs |
| POS-C | 2 graphs × hybrid | bit-storage reduction | ≥4× on both graphs |
| POS-D | 2 graphs × 5 permutation seeds | inverse-permutation max error | ≤1e-10 for raw and hybrid |
| POS-E | 2 graphs × 5 hop-shuffle seeds | ordered/shuffled representation error | shuffled error ≥1.25× ordered error on both graphs |
| POS-F | 2 graphs × 5 seeds × fixed raw probe | ordered/shuffled accuracy | report full distribution; ordered mean ≥ shuffled mean, but no stronger accuracy gate |

### Metrics and statistics

Relative Frobenius error, average coded bits/value, storage reduction, balanced accuracy, fixed-probe accuracy, permutation maximum error, ordered/shuffled error ratio. Report every row, five-seed mean±sample SD, and all failed/negative controls. No formal confidence claim beyond descriptive seed dispersion.

### Runtime / hardware budget

RTX3060 12GB or CPU fallback; Conda `dyg-cold`; target under 25 minutes and under 4 GB peak memory. No remote compute.

## Expected Results

- Minimum: complete raw/uniform/Lloyd/hybrid matrix with permutation and shuffled-hop controls.
- Strong: POS-A through POS-E pass; POS-F remains descriptive.
- Failure: hybrid error >5%, storage <4×, any permutation violation, or shuffled-hop error <1.25× ordered blocks the strong claim.
- Writing gate: raw rows, exact bit ledger, permutation/shuffle seeds and five-seed probe outputs must be frozen first.

## Figure/Table Decision Rules

Figure 1 shows hop construction and hybrid escape coding. Figure 2 compares error/storage/accuracy across methods. Figure 3 shows permutation and shuffled-hop controls. Table 1 defines the bit ledger. Table 2 reports all method/seed/control results.

## Traceability Checklist

Every number maps to raw JSON/CSV, code, dataset/model hashes, permutation seeds, split seeds and bit-accounting output. Preserve prior single-split results and the independent review that motivated the corrected controls.

## Citation Scope

At least 30 unique verified references, majority 2022–2026. Cover positional encodings, graph transformers, quantized graph communication, ANN-to-SNN conversion, spiking graph models and permutation equivariance. Separate direct methods from literature-only context.

## Constraints and Preferences

English paper, Chinese logs; complete TeX/PDF/source package; one final PDF; no commit, push, submission, remote compute or credential writes; all artifacts under the POS-C13 v2 run root.
