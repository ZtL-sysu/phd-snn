# CCFA Pre-Experiment Review v6

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 7.5/10**  
**Confidence: high** for the mathematical, comparator, and gate review; medium for broader scientific impact.

The rowwise interval formulation resolves the v5 baseline stop-loss by changing the scientific claim explicitly rather than weakening thresholds silently. The proposed bound and Minkowski comparator are valid, the global-uniform equality control is correct, and restricting the 25% gate to rowwise cells is logically coherent. Width/RMS is properly demoted to descriptive evidence.

## Evidence Reviewed

- `inputs/guidance-v6.md`
- `contract-extraction.yaml`
- `claim-evidence-matrix.md`
- `strong-result-feasibility-lock.md`
- `corrections/p3-v5-baseline-stop-loss.md`
- `inputs/v5-rowwise-baseline-diagnostic.json`
- `inputs/ccfa-pre-experiment-review-v5-final.md`
- `inputs/ccfa-pre-experiment-integrity-v5-final.md`

No experiment was run and no input was modified.

## Formula Assessment

Let `C=abs(A)abs(A)` and let `Delta in R^(N x H)` contain deterministic rowwise radii.

### Proposed bound

For `E=M-M_hat`, `abs(E)<=Delta`, ReLU non-expansiveness gives

`abs(H-H_hat)<=abs(A)abs(E)`.

After the second aggregation and frozen weight,

`abs(Z-Z_hat)<=abs(A)abs(A)Delta abs(W1)=B_abs`.

This is dimensionally consistent and is the exact componentwise independent-box interval envelope for the stated chain.

### Minkowski comparator

Let `r_p=||Delta[p,:]||_2`. Then

`B_mink[i,k]=(C r)[i] ||W1[:,k]||_2`

is valid because source-node contributions can be bounded by Minkowski and each hidden-channel row by Cauchy-Schwarz. It also satisfies `B_abs<=B_mink`. This is a valid norm comparator, although its ordering is analytic and should not be presented as an empirical victory.

### Global comparator

`B_global_col[i,k]=rowsum(C)[i] max(Delta) ||W1[:,k]||_1`

is valid, output-column matched, and compares rowwise radii against the natural global-radius collapse of the same interval model. For global-uniform quantization, `Delta` is constant and `B_abs=B_global_col`, so equality is a structural control.

## Baseline Stop-Loss

The v5 diagnostic shows why absolute width/RMS cannot remain a strong claim: global-uniform values reach 28.3 and rowwise values reach 36.9. Guidance-v6 handles this honestly:

- preserves the failed absolute-width target as negative evidence;
- removes all absolute width thresholds;
- reports width/RMS only descriptively;
- makes deterministic containment and comparator validity hard gates;
- evaluates utility only through rowwise-versus-global relative tightening.

This resolves the stop-loss at the claim-policy level without overstating absolute certificate quality.

## Baseline Fairness

The comparison is fair for the stated question because `B_abs` and `B_global_col` share the same chain, `C`, `W1`, output coordinates, precision, and underlying radius matrix. The only intervention is replacing heterogeneous row radii with their maximum. It therefore isolates the value of rowwise radius granularity.

It is not a broad comparison against all norm or interval certificates. Safe claims are:

- deterministic containment for the frozen two-layer chain;
- no looser than the valid Minkowski comparator;
- expected equality under global-uniform radii;
- at least 25% tightening over the global-radius ablation in every rowwise cell;
- descriptive absolute width/RMS.

## Diagnostic Support

The preserved seed-0 diagnostic reports 12/12 containment and valid Minkowski comparisons. Rowwise tightening is 78.4–81.4%, comfortably above the 25% gate, while global-uniform cells show expected near-zero numerical differences. This supports feasibility only; it is not substitute evidence for the frozen 18 rowwise cells.

## Required Claim Guardrails

1 Describe the 25% threshold as a pre-registered rowwise-radius utility gate, not a universal property.
2 Do not call `B_abs<=B_mink` or global-uniform equality empirical improvements; they are analytic/structural checks.
3 Do not promote width/RMS to a headline result or compare it to failed v5 targets as though equivalent.
4 State that tightening is versus the global-radius ablation, not state-of-the-art certified bounds.
5 Preserve the v5 stop-loss and all failed absolute-width evidence.
6 Keep the scope restricted to the exact frozen two-layer chain and deterministic theorem/implementation containment.

## Remaining Risks

- **Medium:** the rowwise method and comparator are still application-specific interval propagation, so novelty is limited.
- **Medium:** the seed-0 tightening is favorable but cannot establish all-cell success.
- **Low:** the formulas and gate are sound and no unfair baseline substitution remains.

**Recommendation:** proceed to the frozen experiment with the stated claim guardrails.
