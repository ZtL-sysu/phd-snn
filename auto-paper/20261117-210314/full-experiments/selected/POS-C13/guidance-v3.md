# Research Guidance File

## Title / Topic

- Working title: Permutation-Equivariant Hybrid Hop-Event Coding for Frozen Graph Positional Messages
- Target field: graph positional representation compression and frozen GNN-to-SNN conversion
- Target venue: Q2+ journal / IEEE TNNLS-style graph-neuromorphic scope
- Technique/method: exact multi-hop positional features, node-permutation audit, shuffled-hop codebook-mismatch control, and 8-centroid Lloyd alphabets with one escape symbol and 0.5% exact escapes
- Selected application scenario: Chameleon and Squirrel static graph node classification with frozen local graph snapshots

## Core Idea

Multi-hop positional messages preserve structural information but are expensive to transport. The contribution is a narrow conversion-level representation study: concatenate raw features with one-, two- and three-hop normalized messages, quantize hop channels using eight Lloyd centroids plus one escape symbol, and certify node-permutation equivariance. A shuffled-hop codebook-mismatch control tests whether channel-specific codebooks depend on the canonical hop order without making the error ratio tautological.

### Mechanism-Level Rationale

- Domain bottleneck: multi-hop positional features are large and uniform/per-channel quantization alone loses tails or channel structure.
- Mechanism: a hybrid Lloyd alphabet uses four-bit symbols for eight centroids plus one escape marker; escaped values carry a 32-bit float payload. Codebook centroids cost `8×32` bits per channel and are amortized over node count. Hop blocks remain ordered and transform equivariantly under node permutations.
- Required controls: exact inverse-permutation audit, shuffled-hop representation/control, raw/uniform/per-channel baselines, five split/probe seeds and fixed-raw-probe transfer evaluation.
- Novelty boundary: conversion-level hop-message coding with explicit equivariance/order controls, not a new graph transformer, direct SNN training, broad transformer conversion, temporal dynamics, energy or hardware claim.

## Paper Story

- Central scientific question: can hybrid hop-event coding retain ordered multi-hop positional information at substantial storage reduction while remaining node-permutation equivariant and degrading under shuffled-hop controls?
- Intended reader: graph representation compression, graph transformers and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → choice: expensive hop messages → codebook plus rare-value escapes and exact permutation audit → compressed ordered positional representation.
- Expected contribution type: representation coding method plus equivariance/order-control study.
- planned_claim: hybrid coding has ≤5% relative representation error, ≥4× storage reduction under an exact conservative ledger, exact permutation equivariance, and ordered-codebook mismatched-shuffle error at least 25% higher than ordered error on both graphs.
- observed_finding: pending corrected multi-seed/control run.
- Main claim: ordered multi-hop message fidelity, storage efficiency and equivariance within the fixed two-graph protocol.
- Boundary: Chameleon/Squirrel, three hops, eight Lloyd centroids plus escape, five split/probe seeds, no broad transformer-conversion or deployment claim.

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
- Hybrid per-channel eight-centroid Lloyd plus one escape symbol and 0.5% exact escapes.
- Serialization: every value uses one four-bit symbol (eight centroid IDs or escape); escaped values add one 32-bit float32 payload; each channel stores eight float32 centroids. Average bits/value are `4 + 32 f_escape + 256/N`, with no omitted mask/index cost.
- Escape/codebook scope: representation/storage rows fit codebooks and select the top 0.5% source-side errors on all nodes; task rows fit codebooks and escape thresholds on training nodes only and apply them unchanged to validation/test nodes.
- Shuffled-hop mismatch control: fit channel codebooks on canonical ordered `H`, apply one global hop-block permutation per shuffle seed to the raw columns, quantize the shuffled columns with the unchanged ordered codebooks, and compare with shuffled raw `S H`. The ratio is `E_shuffled/E_ordered`; it is not formed by shuffling target and reconstruction together.
- Node-permutation equivariance: permute nodes/graph, recompute features and encoding with deterministic tie handling, inverse-permute, and compare with the original.
- Fixed-raw-probe transfer: fit one probe per graph/split seed on raw training features and reuse the exact weights, intercept, split and evaluation nodes for raw, encoded, ordered and shuffled rows. Retrained-probe results are separate descriptive evidence.

### Required experiments

| ID | Matrix | Primary metric | Binding expected-strong |
|---|---|---|---|
| POS-A | 2 graphs × 5 split seeds × raw/uniform/Lloyd/hybrid | balanced accuracy | hybrid mean loss versus raw ≤2 pp on both graphs |
| POS-B | 2 graphs × hybrid | representation relative Frobenius error | ≤5% on both graphs |
| POS-C | 2 graphs × hybrid | bit-storage reduction | ≥4× on both graphs |
| POS-D | 2 graphs × 5 permutation seeds | inverse-permutation max error | ≤1e-10 for raw and hybrid |
| POS-E | 2 graphs × 5 hop-shuffle seeds | ordered-codebook mismatched-shuffle error | shuffled error ≥1.25× ordered error on both graphs |
| POS-F | 2 graphs × 5 split seeds × fixed raw probe | ordered/shuffled accuracy | report full distribution; ordered mean ≥ shuffled mean, but no stronger accuracy gate |

### Metrics and statistics

Relative Frobenius error, exact average bits/value from `4 + 32 f_escape + 256/N`, storage reduction, balanced accuracy, fixed-probe accuracy, permutation maximum error and ordered-codebook mismatched-shuffle error ratio. Report every row, actual escape fraction, codebook overhead, five-seed mean±sample SD and all failed/negative controls. No formal confidence claim beyond descriptive seed dispersion.

### Runtime / hardware budget

RTX3060 12GB or CPU fallback; Conda `dyg-cold`; target under 25 minutes and under 4 GB peak memory. No remote compute.

## Expected Results

- Minimum: complete raw/uniform/Lloyd/hybrid matrix with permutation and shuffled-hop controls.
- Strong: POS-A through POS-E pass; POS-F remains descriptive.
- Failure: hybrid error >5%, conservative storage <4×, any permutation violation, or mismatched-shuffle error <1.25× ordered blocks the strong claim.
- Writing gate: raw rows, exact bit ledger, permutation/shuffle seeds and five-seed probe outputs must be frozen first.

## Figure/Table Decision Rules

Figure 1 shows hop construction and hybrid escape coding. Figure 2 compares error/storage/accuracy across methods. Figure 3 shows permutation and shuffled-hop controls. Table 1 defines the bit ledger. Table 2 reports all method/seed/control results.

## Traceability Checklist

Every number maps to raw JSON/CSV, code, dataset/model hashes, permutation seeds, split seeds, escape masks and the exact symbol/payload/codebook ledger. Preserve prior single-split results and the independent review that motivated the corrected controls.

## Citation Scope

At least 30 unique verified references, majority 2022–2026. Cover positional encodings, graph transformers, quantized graph communication, ANN-to-SNN conversion, spiking graph models and permutation equivariance. Separate direct methods from literature-only context.

## Constraints and Preferences

English paper, Chinese logs; complete TeX/PDF/source package; one final PDF; no commit, push, submission, remote compute or credential writes; all artifacts under the POS-C13 v2 run root.
