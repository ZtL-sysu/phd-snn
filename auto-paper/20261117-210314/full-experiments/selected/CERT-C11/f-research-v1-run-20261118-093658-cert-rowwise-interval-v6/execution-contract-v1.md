# Execution contract v1 — CERT-C11 guidance-v6

## Goal

Complete all `f-research-v1` stages for rowwise layerwise interval certificates over `M=XW0 → Q_rowwise(M) → A·relu(·+b0) → A·H·W1`.

## Authorized scope

- Local RTX3060/CPU and Conda `dyg-cold`; 3 graphs × 3 seeds × 2 levels × global/rowwise quantizers.
- All quantization, dequantization, reconstruction and bound arithmetic in float64.
- Binding strong result is deterministic containment, valid Minkowski comparison, global-uniform equality control, and ≥25% tightening in every rowwise cell. Width/RMS is descriptive only.
- Preserve all v1-v5 attempts and baseline failures.
- No commit, push, submission, remote compute, or credential writes.

## Outputs

All artifacts remain under this run root; final paper uses six sections and one PDF.
