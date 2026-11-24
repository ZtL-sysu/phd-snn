# CCFA Pre-Experiment Integrity Review v3

review_execution: independent-agent

## Integrity Verdict

**BLOCK PENDING CONTRACT CORRECTION**

**Score: 5.8/10**  
**Confidence: high**

Guidance-v3 fixes the prior chain ambiguity and removes observed-error-derived containment. The remaining integrity defects are algebraic and reproducibility-related: one comparator is not a valid upper bound, and the binding gate is inconsistent with the global-uniform quantizer definition.

## Claim-Evidence Alignment

| Claim | Frozen contract | Integrity status | Required action |
|---|---|---|---|
| Exact deterministic containment | Exact chain, half-step `Delta`, 36-cell audit | Sound in exact arithmetic | Cover float32 reconstruction and constant-channel cases |
| Valid proposed envelope | `abs(A)abs(A)Delta abs(W1)` | Sound for independent coordinate intervals | Keep “layerwise interval envelope” wording |
| Fair Euclidean comparison | Stated rowwise formula | Invalid/ambiguous as written | Replace with a proven coordinate-box upper bound |
| Tightness versus global scalar | Per-cell `>=25%` | Contradicted by global-uniform constant radius | Revise gate or restrict claim to per-channel cells |
| Quantizer scope | Global/per-channel uniform | Narrow and acceptable | Define zero-step channels and cast precision |
| Interpretation boundary | Deterministic audit, no statistical coverage | Sound | Preserve in abstract, results, and conclusion |

## Mathematical-Definition Checks

### Operator chain

The exact chain

`M=XW0`, `M_hat=Q(M)`, `H=relu(A M+b0)`, `Z=A H W1+b_out`

is consistent with

`B_prop=abs(A)abs(A)Delta abs(W1)`.

Biases cancel, ReLU is non-expansive, and both adjacency applications are present exactly once in the bound. The prior fatal chain ambiguity is resolved.

### Delta derivation

With deterministic round-to-nearest and finite endpoints, `Delta=s/2` bounds the ideal quantization error. The integrity condition is `Delta >= abs(M-M_hat)` for the actual values used by the model.

If dequantization or casting to float32 changes `M_hat`, the nominal half-step may not cover the stored-value error. The implementation must either use a proven representation-error inflation or perform the quantizer arithmetic at a precision where the radius bound is exact. Constant channels also require a zero-step reconstruction rule.

### Proposed bound

For independent coordinate intervals, `|E|<=Delta` implies

`|A E|<=|A|Delta`

before ReLU and

`|A(H-H_hat)W1|<=|A||A|Delta|W1|`.

The proposed formula is mathematically sound for the frozen chain. “Exact worst-case” should mean exact for the componentwise interval relaxation; correlated realized rounding errors may admit a tighter bound.

### Euclidean comparator

The v3 formula uses `Delta[j]` despite `Delta in R^(N x H)`. More importantly,

`sqrt(sum_j(C[i,j] ||Delta[j,:]||_2)^2) ||W1[:,k]||_2`

is not an upper bound for independent rowwise boxes. Error rows can align with `W1[:,k]`, yielding coherent addition across `j`.

A safe rowwise comparator is

`||W1[:,k]||_2 sum_j C[i,j] ||Delta[j,:]||_2`,

where `C=abs(A)abs(A)`. This is valid by Minkowski and Cauchy-Schwarz and satisfies `B_prop<=B_euc`.

### Global comparator

The sum axis in `sum(abs(W1))` is unspecified.

For the natural output-column definition

`B_global[i,k]=rowsum(C)[i] max(Delta) ||W1[:,k]||_1`,

global-uniform quantization has constant `Delta`, so `B_prop=B_global`. Its tightening is exactly `0`, contradicting the `>=25%` binding gate in every global-uniform cell.

If the full matrix L1 sum is intended, the comparator no longer has the advertised per-output meaning and is too loose to support the gate.

## Numeric-Policy Checks

- **Cell matrix:** `3 x 3 x 2 x 2 = 36`; consistent.
- **Precision:** float32 model/message and float64 bound arithmetic are reasonable, but quantizer/dequantizer/cast precision is not fully frozen.
- **Tolerance:** `atol=1e-10`, `rtol=1e-12` are concrete; the exact containment predicate should be written explicitly.
- **Width/RMS:** actual RMS is defined over `N x C`; the median axis for each bound matrix is not explicit.
- **Tightening:** the per-cell ratio is clear, but it cannot meet 25% for constant-radius global-uniform cells against the intended global bound.
- **Zero handling:** actual-RMS zero is defined. Zero global or Euclidean width/RMS is not defined.
- **Quantizer endpoints:** upward ties and exact endpoints are defined. Constant-channel `s=0` remains undefined.
- **Clipping:** source values outside the declared range fail; clarify that the finite-grid clip is only a numerical endpoint safeguard.

## Overclaim Risks

| Risk | Severity | Safe treatment |
|---|---|---|
| “Tighter than global scalar” across all cells | Fatal | Restrict to per-channel cells or revise the comparator/gate |
| Euclidean result as fairness evidence | Fatal until formula is fixed | Use a proven upper bound and state that ordering is analytic |
| 100% containment as empirical coverage | High | Call it deterministic theorem/implementation containment |
| Exact worst-case for realized quantizer | Medium | Say exact for the independent interval relaxation |
| General GNN-to-SNN certificate | High | Restrict to the stated frozen two-layer chain |
| Robustness, temporal, energy, or hardware claims | High | Exclude from the paper claim |

## Integrity Conclusion

The v3 package successfully resolves the prior operator-chain and containment-interpretation defects. It does not pass the pre-experiment integrity gate because `B_euc` is not valid as written and the strong global-tightening condition is algebraically incompatible with global-uniform quantization. Correct those contracts before launching the 36-cell experiment. No integrity concern requires discarding the core `B_prop` method; the block is limited to comparator validity and binding-gate consistency.
