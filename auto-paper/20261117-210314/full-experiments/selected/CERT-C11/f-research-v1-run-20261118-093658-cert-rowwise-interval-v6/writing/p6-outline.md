# Six-section manuscript outline

## Title

Rowwise Layerwise Interval Certificates for Quantized Messages in Frozen Two-Layer GNN-to-SNN Conversion

## Central question and answer

- Question: for the exact chain `M=XW0 → Q_rowwise(M) → A·relu(·+b0) → A·H·W1`, can a deterministic rowwise interval bound contain final-logit errors while materially tightening a matched global-radius ablation?
- Answer: yes within the tested matrix. All 36 cells are contained, the proposed bound is analytically no looser than the valid Minkowski comparator, global-uniform cells provide an equality control, and all 18 rowwise cells tighten by 74.26%–82.12%.

## 1 Introduction

Purpose: motivate operator-aware finite-precision certificates for frozen graph-message conversion and state the narrow contribution.

1. Finite-precision graph messages alter final logits through two graph aggregations and frozen weights.
2. Generic scalar bounds ignore rowwise quantizer radius and output-column structure.
3. The paper certifies one exact frozen two-layer final-logit chain and evaluates relative tightening against a matched global-radius ablation.
4. State scope: deterministic containment, not statistical coverage or broad SNN/robustness superiority.

## 2 Related Work

Purpose: locate the work among conversion error, graph-message quantization, and certificate/norm bounds.

1. Frozen ANN-to-SNN conversion and error correction.
2. Quantized graph communication and message compression.
3. Certified/robust SNN and interval/norm bound methods.
4. Differentiation: rowwise interval radius propagated through two adjacency operators and final weights; matched radius-granularity ablation.

## 3 Method

Purpose: define the exact chain, radius policy and all comparators.

1. Frozen two-layer GCN tensors and exact computation.
2. Rowwise uniform quantizer with float64 half-step radius `Delta`.
3. ReLU non-expansiveness and the derivation `B_abs=|A||A|Delta|W1|`.
4. Valid Minkowski comparator `B_mink`, matched global-radius ablation `B_global_col`, and scalar context.
5. Numerical policy: ties, constant rows, clipping, tolerance, zero rules, RMS and tightening.

## 4 Experiments and Results

Purpose: answer the research question without inventorying every cell in prose.

1. Experimental scope: 3 graphs, 3 seeds, 2 levels, global/rowwise quantizers.
2. Deterministic containment: 36/36; comparator validity: 36/36.
3. Global-uniform equality control: 18/18.
4. Rowwise tightening: min 74.26%, median 79.65%, max 82.12%.
5. Negative/descriptive evidence: width/RMS median 30.68, max 36.91; no absolute-width claim.
6. Failure audit: no clipping, non-finite rows, omitted cells or error-derived radii.

## 5 Discussion

Purpose: separate analytic validity, empirical relative utility and limitations.

1. The containment result validates implementation of the theorem, not statistical coverage.
2. `B_abs<=B_mink` is analytic ordering, not an empirical improvement.
3. The empirical effect is rowwise tightening over the matched global-radius ablation.
4. Limitations: two-layer frozen GCN, uniform quantizers, three graphs/seeds, high absolute width/RMS, no temporal/energy/robustness/multilayer claims.

## 6 Conclusion

Purpose: restate the scoped finding and future requirements.

1. Rowwise deterministic radii yield valid final-logit envelopes in all tested cells.
2. Rowwise radius granularity substantially tightens the matched global-radius ablation.
3. Absolute worst-case width remains loose; future work requires stronger distributional or multilayer certificates.

## Evidence map

| Section | Evidence |
|---|---|
| Method | `contract-extraction.yaml`, `research/cert_core.py` |
| Scope/matrix | `experiment-traceability.md`, `provenance-manifest.json` |
| Main result | `results/cert-methods.json`, `results/cert-summary.json` |
| Equality/tightening | `figures/source-data/figure3-rowwise-tightening.csv` |
| Negative width | `strong-result-lock.md`, raw rows |
| Limitations | `pre-draft-evidence-dossier.md`, CCFA v2 reviews |
