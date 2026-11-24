# Six-section manuscript outline

## Title

Permutation-Equivariant Hybrid Hop-Event Coding for Frozen Graph Positional Messages

## Central question and answer

- Question: can eight-centroid Lloyd codebooks with exact escapes compress ordered multi-hop graph messages while retaining fidelity, storage efficiency, permutation equivariance and hop-order sensitivity?
- Answer: yes within the fixed Chameleon/Squirrel protocol. Hybrid error is 3.95%/4.88%, storage is 7.49×/7.60×, permutation error is machine precision, and codec-consistent shuffled-hop mismatch is 3.72×/3.63×. Five-seed task loss is bounded and fixed raw probes favor ordered over shuffled features.

## 1 Introduction

Purpose: motivate ordered multi-hop positional messages and the need for conversion-level coding controls.

1. Multi-hop features are large and structurally ordered.
2. Quantization must account for symbols, escape payloads and codebooks.
3. The paper combines hybrid coding with permutation and shuffled-hop controls.
4. Scope is frozen positional-message conversion, not general transformer-to-SNN conversion.

## 2 Related Work

Purpose: position the work among positional encodings, graph transformers, graph-message quantization and ANN-to-SNN conversion.

1. Positional encodings and multi-hop graph features.
2. Graph transformer and spiking graph model context.
3. Quantized graph communication and codebook/escape methods.
4. Novelty delta: combined conversion-level serialization and order-control protocol.

## 3 Method

Purpose: define representation, codebook, serialization and controls.

1. `H=[X,AX,A^2X,A^3X]`.
2. Eight Lloyd centroids plus one escape symbol.
3. Exact bits: `4 + 32 f_escape + 256/N`.
4. Node-permutation recomputation and inverse comparison.
5. Codec-consistent ordered-codebook mismatched-shuffle control.
6. Retrained and fixed raw probes with train-only fitting.

## 4 Experiments and Results

Purpose: answer fidelity/storage/equivariance/order/task questions with complete tables.

1. Two-graph method matrix and conservative storage.
2. Hybrid error and exact bit ledger.
3. Permutation audit and non-identity shuffle controls.
4. Five-seed retrained balanced accuracy with paired mean±sample SD.
5. Fixed raw-probe ordered/shuffled distribution.
6. Negative leakage run and corrected accepted evidence.

## 5 Discussion

Purpose: separate established components, application-specific contribution and limitations.

1. Hybrid coding retains fidelity and storage within scope.
2. Order controls show canonical hop alignment matters to fixed probes and codebooks.
3. Task superiority is not claimed; hybrid losses are bounded and mixed.
4. Limitations: two graphs, no real graph-transformer→SNN, temporal/energy/hardware, or broad generality.

## 6 Conclusion

Purpose: restate scoped evidence and next requirements.

1. Conservative hybrid serialization passes all binding gates.
2. Permutation and shuffled-hop controls support the ordered-message interpretation.
3. Real graph-transformer conversion remains future work.

## Evidence map

| Section | Evidence |
|---|---|
| Method | `research/pos_core.py`, `contract-extraction.yaml` |
| Representation | `results/pos-representation.json`, summary |
| Task | `results/pos-task-rows.json`, `pos-dispersion-summary.json` |
| Provenance | `results/task-provenance.json` |
| Negative evidence | `corrections/pos-task-leaky-probe-v1.json` |
| Review limits | `ccfa-pre-draft-*` reports |
