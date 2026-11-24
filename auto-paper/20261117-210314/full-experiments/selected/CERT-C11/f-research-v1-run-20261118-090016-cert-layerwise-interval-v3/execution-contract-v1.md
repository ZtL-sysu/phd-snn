# Execution contract v1 — CERT-C11 guidance-v3

## Goal

Complete all `f-research-v1` P0-P21 stages for layerwise interval certificates over the exact frozen two-layer chain `M=XW0 → Q(M) → A·relu(·+b0) → A·H·W1+b_out`.

## Authorized scope

- Local RTX3060/CPU and Conda `dyg-cold` only.
- Run the corrected 36-cell matrix: three graphs, seeds 0/1/2, 4/8 levels, global/per-channel uniform quantizers.
- Use only deterministic quantizer radii; actual errors cannot construct or tune bounds.
- Preserve v1/v2 experiments and CCFA reviews as background/negative evidence.
- No commit, push, submission, remote compute, or credential writes.

## Quality

The run must freeze tensor dimensions, quantizer tie/clipping behavior, float precision, tolerances, RMS/width/tightening formulas, and comparator definitions. The binding strong gate is 36/36 deterministic containment, median width/RMS ≤10, maximum ≤15, per-cell tightening ≥25% versus the global scalar reference, and `B_prop <= B_euc + tol` everywhere.

## Outputs

All code, raw results, audits, figures, TeX/PDF, source archive, and manifests stay under this run root. Final paper has exactly six numbered sections and one PDF.
