# Execution contract v1 — CERT-C11 guidance-v4

## Goal

Complete all `f-research-v1` stages for the exact chain `M=XW0 → Q(M) → A·relu(·+b0) → A·H·W1+b_out`, using float64 dequantization and bounds, a valid Minkowski comparator, a global-radius outputwise comparator, and a global-uniform equality control.

## Authorized scope

- Local RTX3060/CPU and Conda `dyg-cold` only.
- Run 3 graphs × 3 seeds × 2 levels × 2 quantizers.
- Actual errors cannot construct or tune radii or bounds.
- Preserve all previous attempts and CCFA blocks.
- No commit, push, submission, remote compute, or credential writes.

## Quality

Binding gate: 36/36 deterministic containment; median width/RMS ≤10 and maximum ≤15; `B_abs <= B_mink+tol`; 18 global-uniform cells satisfy `B_abs == B_global_col+tol`; every per-channel cell has ≥25% tightening versus `B_global_col`; no clipping, error-derived radius, NaN or Inf.

## Outputs

All code, results, audits, paper, figures, PDF, source archive and manifests remain under this run root.
