# CCFA Pre-Experiment Review v5

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 9.0/10** for the formula-only gate  
**Confidence: high**

The corrected bound formulas, comparator ordering, and gate logic are mathematically sound. One frozen dimension declaration remains wrong: `contract-extraction.yaml` states `M:MxH`, but the defined computation `M=XW0` with `X in R^(N x F)` and `W0 in R^(F x H)` gives `M in R^(N x H)`. This is a narrow metadata correction, not a failure of the derivation.

## Evidence Reviewed

- `inputs/guidance-v5.md`
- `contract-extraction.yaml`
- `strong-result-feasibility-lock.md`
- `corrections/p1b-v4-review-resolution.md`
- `inputs/ccfa-pre-experiment-review-v4.md`
- `inputs/ccfa-pre-experiment-integrity-v4.md`

No experiment was run and no frozen input was modified.

## Dimension Check

The operative dimensions are:

- `A in R^(N x N)`
- `M, M_hat, Delta in R^(N x H)`
- `delta in R^H`
- `W1 in R^(H x C_out)`
- `c=(abs(A)abs(A))1_N in R^N`
- `B_abs, B_mink, B_global_col in R^(N x C_out)`

All formulas use node indices for `c` and hidden-channel indices for `delta` and `W1`. The v4 node/channel collision is resolved. Only `M:MxH` in the extraction contract conflicts with this dimension system and should read `M:NxH`.

## Derivation Check

Let `G=abs(A)abs(A)` and `c=G1_N`. Because `Delta=1_N delta^T`,

`G Delta abs(W1)[i,k]`

`= sum_p sum_h G[i,p] delta_h abs(W1[h,k])`

`= c_i sum_h delta_h abs(W1[h,k])`.

Thus

`B_abs[i,k]=c_i sum_h delta_h abs(W1[h,k])`

matches the matrix computation exactly.

For each source node, the hidden-channel error is bounded in the coordinate box `[-delta_h,delta_h]`. Minkowski followed by Cauchy-Schwarz gives

`B_mink[i,k]=c_i ||delta||_2 ||W1[:,k]||_2`

and therefore `B_abs<=B_mink` elementwise.

The global-radius comparator

`B_global_col[i,k]=c_i max_h(delta_h) ||W1[:,k]||_1`

is valid and output-column matched.

## Comparator And Gate Check

- `B_abs<=B_mink` is analytically valid and suitable as the comparator sanity gate.
- `B_global_col` is fairer than the former collapsed full-matrix scalar.
- If `delta_h=delta` for all `h`, then `B_abs=B_global_col`; the 18 global-uniform equality controls are correct.
- Tightening `1-width_over_rms(B_abs)/width_over_rms(B_global_col)` is required only for the 18 per-channel cells, where it is logically possible.
- The 36-cell containment, width/RMS, clipping, tolerance, zero, and non-finite gates remain unchanged and coherent.

## Required Action

1 Change the extraction dimension `M:MxH` to `M:NxH`.
2 Optionally rename the node matrix `C=abs(A)abs(A)` to `G` or `C_A`, because `C` already denotes the output-class dimension. This is notation hygiene, not a mathematical blocker.

After the `M:NxH` correction, the formula-only gate supports **proceed** to the pre-registered experiment.
