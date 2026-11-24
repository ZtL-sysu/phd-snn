# CCFA Pre-Experiment Review v4

review_execution: independent-agent

## Verdict

**BLOCK**

**Score: 6.0/10**  
**Confidence: high** for mathematical and contract checks; novelty remains medium-confidence because this review performs no external literature search.

Guidance-v4 resolves the prior gate-policy failures and gives the correct matrix-level envelope. However, the expanded `B_abs` and `B_mink` formulas use one index `j` simultaneously for graph nodes and hidden channels. Those scalar formulas are dimensionally inconsistent with `C in R^(N x N)`, `delta in R^H`, and `W1 in R^(H x C)`. The pre-experiment implementation contract must be corrected before the strong gate can be run.

## Evidence Reviewed

Only the specified frozen artifacts and copied reviews were used:

- `inputs/guidance-v4.md`
- `contract-extraction.yaml`
- `claim-evidence-matrix.md`
- `strong-result-feasibility-lock.md`
- `corrections/p1b-v3-review-resolution.md`
- `inputs/ccfa-pre-experiment-review-v2.md`
- `inputs/ccfa-pre-experiment-integrity-v2.md`
- `inputs/ccfa-pre-experiment-review-v3.md`
- `inputs/ccfa-pre-experiment-integrity-v3.md`

No experiment was run and no frozen input was modified.

## Prior-Issue Resolution

| v3 issue | v4 status | Judgment |
|---|---|---|
| Invalid Euclidean-style comparator | Partly resolved | The intended Minkowski bound is valid, but its expanded formula has inconsistent indices |
| Ambiguous global comparator | Resolved | `B_global_col` is output-column fair and dimensionally valid |
| Impossible global-uniform tightening gate | Resolved | Equality is correctly made a control and excluded from tightening |
| Float32 reconstruction error | Resolved | All source snapshots are cast to float64 before computation and remain float64 |
| Constant-channel zero step | Resolved | Identity reconstruction and zero radius are explicit |
| Median/zero/tolerance/clipping ambiguity | Resolved | Exact axes, predicates, and failure rules are specified |
| Coverage and scope overclaim | Resolved | Deterministic validation and narrow two-layer scope are explicit |

## Formula Audit

### Exact chain and matrix envelope

The chain `M=XW0`, `M_hat=Q(M)`, `H=relu(A M+b0)`, `Z=A H W1+b_out` and matrix bound `B_abs=abs(A)abs(A)Delta abs(W1)` are sound. With `C=abs(A)abs(A)` and `Delta=1_N delta^T`,

`B_abs[i,k] = sum_p sum_h C[i,p] delta_h abs(W1[h,k]) = c_i sum_h delta_h abs(W1[h,k])`.

### Blocking index inconsistency

Guidance-v4 instead writes `B_abs[i,k]=sum_j C[i,j] delta_j abs(W1[j,k])`. Here `C[i,j]` requires `j` to index graph nodes, while `delta_j` and `W1[j,k]` require `j` to index hidden channels. These spaces are different: `C` is `N x N`, whereas `W1` is `H x C`.

The same defect appears in `B_mink[i,k]=||W1[:,k]||_2 sum_j C[i,j] delta_j`. The valid Minkowski comparator for `Delta=1_N delta^T` is

`B_mink[i,k] = c_i ||delta||_2 ||W1[:,k]||_2`.

Then `B_abs[i,k] <= B_mink[i,k]` follows directly from Cauchy-Schwarz.

### Global comparator and controls

`B_global_col[i,k]=c_i max_h(delta_h) ||W1[:,k]||_1` is valid, output-column fair, and uses the same graph-operator and weight information while collapsing channel radii to one global radius.

For global-uniform quantization, `delta_h=delta` for all channels, so `B_abs=B_global_col`. Treating the 18 global-uniform cells as equality controls is mathematically correct. The 25% tightening gate applies only to the 18 per-channel cells, where improvement is possible.

## Strong Gate

The revised gate is logically coherent after the index correction. The 36/36 containment audit, equality controls, per-cell tightening, width/RMS thresholds, and Minkowski ordering are all valid and falsifiable. The current scalar formulas must not be implemented because they do not represent the stated matrix computation.

## Numerical Policy

The requested policies are otherwise resolved:

- **Float64 reconstruction:** source float32 snapshots are cast before `M=XW0`; quantization, dequantization, reconstruction, bounds, and metrics remain float64.
- **Constant channels:** step and radius are zero with exact identity reconstruction.
- **Tolerance:** `value <= bound + 1e-10 + 1e-12*abs(bound)` is exact.
- **Median:** taken over all `N x C` bound entries.
- **Zero rule:** ratio zero only for zero numerator and zero RMS; otherwise `+inf` and failure.
- **Clipping:** endpoint safeguard only; out-of-range beyond `1e-10` fails.
- **Non-finite values:** NaN/Inf fail the cell.
- **Interpretation:** deterministic theorem/implementation containment, not statistical coverage.

## Required Actions

1 Separate node and channel indices throughout the bound definitions, for example `p` for nodes and `h` for hidden channels.
2 Replace the expanded proposed formula with `c_i sum_h delta_h abs(W1[h,k])`.
3 Replace the Minkowski formula with `c_i ||delta||_2 ||W1[:,k]||_2`.
4 Synchronize `contract-extraction.yaml`, the claim matrix, implementation, and tests to those corrected formulas.
5 Retain `B_global_col`, the equality control, the per-channel-only tightening gate, and all current numerical policies.

## Fatal Risks

- **Fatal until corrected:** the expanded `B_abs` formula mixes node and channel indices.
- **Fatal until corrected:** the stated `B_mink` formula is not the valid Minkowski comparator for the defined `Delta`.
- **No remaining fatal issue:** operator order, global comparator fairness, equality control, tightening scope, float64 reconstruction, and numerical policy are resolved.

**Recommendation:** block only for the short formula/index correction. Once the scalar formulas match the matrix computation, the package is suitable to proceed to the corrected pre-registered experiment.
