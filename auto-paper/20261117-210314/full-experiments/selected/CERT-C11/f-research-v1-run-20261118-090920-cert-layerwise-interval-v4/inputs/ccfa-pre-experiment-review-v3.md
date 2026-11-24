# CCFA Pre-Experiment Review v3

review_execution: independent-agent

## Verdict

**BLOCK**

**Score: 5.8/10**  
**Confidence: high** for the mathematical and contract checks; scientific novelty remains medium-confidence because no new literature search was performed.

Guidance-v3 resolves the prior operator-chain ambiguity and gives a sound proposed interval bound. It does not yet resolve baseline validity or gate consistency. As written, CERT-D uses an Euclidean expression that is not a valid upper bound for independent coordinate intervals, and the binding 25% tightening gate is mathematically impossible for the global-uniform cells if `B_global` is a correctly defined output-column comparator.

## Evidence Reviewed

Only the specified frozen artifacts were used:

- `inputs/guidance-v3.md`
- `contract-extraction.yaml`
- `claim-evidence-matrix.md`
- `strong-result-feasibility-lock.md`
- `corrections/p1b-v2-review-resolution.md`
- `inputs/ccfa-pre-experiment-review-v2.md`
- `inputs/ccfa-pre-experiment-integrity-v2.md`

No experiment was run and no frozen input was modified.

## Prior-Issue Resolution

| Prior issue | v3 status | Gate judgment |
|---|---|---|
| Contradictory operator order | Resolved | The sole chain is now explicit and algebraically consistent |
| Error-derived or ambiguous `Delta` | Mostly resolved | Half-step radius is correct in exact arithmetic; float32 representation and constant-channel cases still need explicit treatment |
| Incorrect/loose Euclidean comparator | Not resolved | The new formula is dimensionally ambiguous and not generally valid for a coordinatewise box |
| Weak global comparator | Partly resolved | It is correctly labeled a loose reference, but the strong gate remains dependent on it |
| Undefined RMS/tightening/tolerance | Mostly resolved | Main formulas are fixed; matrix-axis and zero-comparator-denominator details remain |
| Coverage overclaim | Resolved | Deterministic theorem/implementation containment is clearly separated from statistical coverage |
| Broad GNN-to-SNN overclaim | Resolved | Scope is restricted to the exact frozen two-layer chain |

## Detailed Assessment

### Operator chain

**Resolved and sound.** For

`M=XW0`, `M_hat=Q(M)`, `H=relu(A M+b0)`, `H_hat=relu(A M_hat+b0)`,
`Z=A H W1+b_out`, and `Z_hat=A H_hat W1+b_out`,

the biases cancel and ReLU non-expansiveness gives

`abs(H-H_hat) <= abs(A) abs(M-M_hat) <= abs(A) Delta`.

The second aggregation and frozen weight then give

`abs(Z-Z_hat) <= abs(A) abs(A) Delta abs(W1) = B_prop`.

This derivation is valid for the exact chain stated in guidance-v3.

### Delta derivation

Mostly resolved. For a finite-range round-to-nearest quantizer with step `s`, `Delta=s/2` is correct in exact arithmetic, and forbidding observed-error-derived radii removes the prior tautology risk.

Remaining required definitions:

- For a constant channel, `s=0` is undefined; explicitly set `Q(m)=m`, reconstruction equals the constant, and `Delta=0`.
- If `M`, `Q`, or dequantization are evaluated in float32, the stored `M_hat` can differ from the ideal dequantized value by representation error. Either compute the quantizer/dequantizer in float64 with a defined cast, or enlarge `Delta` by a proven float32 representation-error term.
- Clarify whether “clipped” is only an endpoint safeguard. Since `min(M)` and `max(M)` define the range, any source value outside that range indicates an implementation error and should fail, as the gate states.

### Proposed formula

Resolved and sound. `B_prop=abs(A) abs(A) Delta abs(W1)` is the correct independent-coordinate absolute interval envelope for the frozen chain. “Exact before interval-dependence tightening” is acceptable only in the sense of componentwise interval propagation, not as the exact attainable error for the realized quantizer.

### Euclidean formula

Not resolved. Guidance-v3 uses

`sqrt(sum_j((abs(A)abs(A))[i,j] Delta[j])^2) * ||W1[:,k]||_2`.

First, `Delta` is an `N x H` matrix, so `Delta[j]` is not defined unless it means a scalar or a row norm. Second, replacing it with `||Delta[j,:]||_2` does not make the formula valid for independent coordinate intervals: different source rows can align their hidden-channel errors with `W1[:,k]`, so their scalar contributions add coherently.

A valid rowwise Euclidean/Minkowski comparator is

`B_euc[i,k] = ||W1[:,k]||_2 * sum_j(abs(A)abs(A))[i,j] * ||Delta[j,:]||_2`.

A second valid, sometimes looser global Frobenius comparator is

`B_eucF[i,k] = ||abs(A)abs(A)[i,:]||_2 * ||Delta||_F * ||W1[:,k]||_2`.

The proposed interval bound is elementwise no larger than the first valid comparator by Cauchy-Schwarz. CERT-D should use a proven upper bound, not merely an expression expected to be larger.

### Global formula and strong gate

Blocking inconsistency. The formula

`B_global[i,k] = rowsum(abs(A)abs(A))[i] * max(Delta) * sum(abs(W1))`

does not specify the sum axis.

- If `sum(abs(W1))` means the output-column L1 norm `sum_l abs(W1[l,k])`, then for global-uniform quantization `Delta` is constant and `B_prop=B_global` elementwise. The tightening is exactly zero, so the required `>=25%` fails in all 18 global-uniform cells.
- If it means the full-matrix L1 sum, `B_global[i,k]` is not an output-column comparator and is artificially over-loose; the 25% gate does not establish useful tightness.

Therefore the binding strong gate is impossible or non-informative under either natural interpretation. This is a fatal pre-experiment contract error.

### Numerical policy

Mostly resolved. Float32 model computation, float64 bound arithmetic, `atol=1e-10`, `rtol=1e-12`, upward ties, NaN/Inf failure, and actual-RMS zero handling are concrete.

Still required:

- State that `median(B)` is over all `N x C` elements, or define another exact axis.
- Define zero handling for `global_width_over_rms` and `euclidean_width_over_rms`, not only zero actual RMS.
- State the exact tolerance predicate, for example `error <= bound + atol + rtol*abs(bound)`.
- Preserve quantizer-step computation precision and dequantized-value cast behavior in the audit.

## Strong-Gate Realism

**Not realistic as written.** The width/RMS thresholds may be feasible, but the per-cell 25% global-tightening threshold cannot pass for constant-radius global-uniform quantization with a correct columnwise scalar comparator. This is not an empirical uncertainty; it is an algebraic impossibility. The gate must be revised before any experiment is launched.

## Required Actions

1 Replace the Euclidean comparator with a valid coordinate-box upper bound, preferably `||W1[:,k]||_2 sum_j C[i,j] ||Delta[j,:]||_2`, and prove its validity.
2 Define `sum(abs(W1))` by axis and matrix shape.
3 Remove the 25% global-tightening requirement from global-uniform cells, or change the claim/gate to a comparison where improvement is possible. Equality for constant `Delta` should be reported as an expected structural result.
4 Define constant-channel quantization and float32 reconstruction error explicitly.
5 Freeze median axes and all zero-denominator/tolerance predicates.
6 Keep the strong claim limited to the exact two-layer chain and deterministic containment.

## Fatal Risks

- **Fatal:** the strong gate is impossible for global-uniform cells under the intended output-column global comparator.
- **Fatal:** the stated Euclidean expression is not a guaranteed upper bound for the independent coordinate box.
- **Major:** `Delta[j]` is dimensionally ambiguous for `Delta in R^(N x H)`.
- **Major:** float32 dequantized reconstruction error is not included in the nominal half-step radius.
- **Major:** novelty and tightness claims must not imply a general interval theorem or robustness result.

**Recommendation:** block the corrected experiment until the comparator formulas and strong gate are revised. The exact chain and `B_prop` derivation are ready; the remaining defects are confined to comparison validity and binding-policy consistency.
