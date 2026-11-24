# Execution contract v1 — CERT-C11 guidance-v5

## Goal

Complete all `f-research-v1` stages for the dimensionally corrected bound `B_abs[i,k]=c_i sum_h delta_h |W1[h,k]|`, where `c=(|A||A|)1`, over the exact chain `M=XW0 → Q(M) → A·relu(·+b0) → A·H·W1`.

## Authorized scope

- Local RTX3060/CPU and Conda `dyg-cold`; 3 graphs × 3 seeds × 2 levels × 2 quantizers.
- All quantization, dequantization, reconstruction and bound arithmetic in float64.
- Preserve all prior attempts and reviews.
- No commit, push, submission, remote compute, or credential writes.

## Quality

Binding gate: 36/36 deterministic containment; median width/RMS ≤10 and max ≤15; `B_abs<=B_mink+tol`; 18 global-uniform equality controls; every per-channel cell ≥25% tighter than `B_global_col`; no clipping, error-derived radius, NaN or Inf.

## Outputs

All artifacts remain under this run root; final paper uses six sections and one PDF.
