# CCFA Pre-Experiment Integrity Review v5

review_execution: independent-agent

## Integrity Verdict

**REVISE FOR ONE DIMENSION METADATA FIX**

**Score: 9.0/10**  
**Confidence: high**

The v5 formulas and derivation are internally correct, and all prior comparator and strong-gate fixes remain valid. The sole remaining inconsistency is the `M:MxH` dimension entry in `contract-extraction.yaml`; it must be `M:NxH`.

## Formula Integrity

### Proposed bound

With `G=abs(A)abs(A)`, `c=G1_N`, and `Delta=1_N delta^T`,

`B_abs=G Delta abs(W1)`

reduces exactly to

`B_abs[i,k]=c_i sum_h delta_h abs(W1[h,k])`.

Node and hidden-channel indices are now separate, and the formula has output shape `N x C_out`.

### Minkowski comparator

For independent coordinate radii,

`B_mink[i,k]=c_i ||delta||_2 ||W1[:,k]||_2`

is a valid upper bound. The ordering `B_abs<=B_mink` follows from Cauchy-Schwarz and is suitable for CERT-D.

### Global comparator

`B_global_col[i,k]=c_i max_h(delta_h)||W1[:,k]||_1`

is valid, outputwise, and matched to `B_abs`. For constant radii it equals `B_abs`; for heterogeneous radii it can be tighter-gated by per-cell percentage improvement.

## Gate Integrity

- **Containment:** remains a deterministic theorem/implementation audit.
- **Equality control:** 18 global-uniform cells correctly require equality and zero tightening.
- **Tightening:** correctly restricted to 18 per-channel cells.
- **Norm control:** `B_abs<=B_mink+tol` is mathematically guaranteed up to the stated tolerance.
- **Precision:** all-float64 reconstruction removes unmodelled float32 error.
- **Numerical policy:** tolerance, median axis, zero ratios, clipping, and NaN/Inf rules remain exact and reproducible.
- **Claim scope:** remains limited to the frozen two-layer chain and does not imply statistical robustness or general SNN conversion.

## Dimension Metadata

Required tensor dimensions are:

`A:NxN`, `M:NxH`, `delta:H`, `W1:HxC_out`, `c:N`, and bounds `NxC_out`.

The frozen extraction entry `M:MxH` is inconsistent with `M=XW0` and the rest of the contract. Correcting it to `M:NxH` is mandatory before implementation freeze. Renaming the matrix currently called `C` is recommended to avoid collision with the class-count symbol.

## Integrity Conclusion

The v4 fatal formula defect is resolved. The v5 derivation, Minkowski comparator, global comparator, equality control, and per-channel gate are sound. Verdict remains **revise** only because the frozen dimension metadata still contains one incorrect shape. After `M:NxH` is recorded, the formula-only integrity gate is clear to proceed.
