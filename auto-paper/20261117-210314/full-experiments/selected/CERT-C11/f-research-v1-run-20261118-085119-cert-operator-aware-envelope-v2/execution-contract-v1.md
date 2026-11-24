# Execution contract v1 — CERT-C11 guidance-v2

## Goal

Complete all `f-research-v1` P0-P21 stages for the corrected operator-aware affine error-envelope claim: frozen two-layer GCN messages quantized with global-uniform or per-channel-uniform rounding, propagated through normalized adjacency, ReLU, and the frozen downstream weight matrix, with output-column certificates compared against global scalar and Euclidean bounds.

## Authorized scope

- Local RTX3060/CPU and Conda environment `dyg-cold` only.
- Reuse prior CERT-C11 rows only as background/negative evidence; the v1 rows measured a narrower pre-aggregation affine map and do not support the corrected main claim.
- Recompute the corrected 36-cell matrix from frozen local graph/model snapshots with seeds 0/1/2, 4/8 levels, and two quantizers.
- Preserve all prior failures, reviewer limitations, and any failed corrected cells.
- No commit, push, submission, remote compute, or credential writes.

## Quality

The certificate must be derived for the stated operator chain, use deterministic quantizer half-steps rather than observed labels/logits, report every cell, distinguish theorem/implementation containment from statistical coverage, and pass the binding strong gate of 100% containment, median width/RMS ≤10, every cell width/RMS ≤15, and minimum tightening ≥25% versus the global scalar bound.

## Outputs

All evidence, code, audits, manuscript, figures, PDF, source archive, and final manifest live under this run root. Final paper uses exactly six numbered sections and one final PDF.
