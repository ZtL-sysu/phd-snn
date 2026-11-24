# CCFA Pre-Experiment Review

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 5.5/10**  
**Confidence: medium**

This is a plausible, narrowly scoped certificate study with a valid mathematical core, but it is not ready for manuscript-level claims. The central operator-aware containment idea is useful, yet the frozen guidance alternates between two different operator orders, the baseline suite is too weak to support a strong tightness claim, and the deterministic containment result must remain an implementation/theorem audit rather than empirical evidence.

## Evidence Reviewed

Only the frozen files in this run root were used:

- `inputs/guidance-v2.md`
- `contract-extraction.yaml`
- `claim-evidence-matrix.md`
- `strong-result-feasibility-lock.md`
- `concern-to-action-ledger.md`
- `inputs/prior-independent-review.md`
- `inputs/prior-cert-v1-baseline.json`
- `inputs/prior-cert-v1-methods.json`

No experiment was run and no input was altered.

## Assessment

### Scientific novelty

**5/10** The graph-specific framing, output-column reporting, normalized-adjacency propagation, and matched global/per-channel quantizer study create a useful application-level contribution. The underlying interval propagation through absolute weights and the ReLU 1-Lipschitz argument are standard certified-ML tools. The defensible novelty is therefore a tailored certificate and empirical tightness study for frozen GNN message quantization, not a new general certificate theorem.

The claim must not be presented as a general ANN-to-SNN conversion certificate, robustness certificate, or temporal/energy result. The current scope supports a narrow methods contribution for a frozen two-layer GCN.

### Baseline fairness

**4/10** The global scalar L1 bound is valid but intentionally merges coordinates and is a weak comparator. Large tightening against it is expected and does not by itself establish scientific value. The Euclidean comparator is also under-defined: as written it uses `rowsum(abs(A)) * ||Delta_row||_2 * ||W2[:,k]||_2`, which is generally looser than a standard rowwise Euclidean bound such as

`(sum_j (|A_ij| ||Delta_j||_2)^2)^(1/2) * ||W2[:,k]||_2`.

If `Delta` is constant across nodes, this reduces to `||A_i||_2 ||Delta||_2 ||W2[:,k]||_2`, not `rowsum(|A_i|)`. The proposed bound is likely no larger than the stated Euclidean formula by a simple norm inequality, so CERT-D may be a construction check rather than an informative comparison.

### Operator chain and containment soundness

**6/10 conditionally.** The inequality is sound for one explicit chain. If `E = M - M_hat`, ReLU is componentwise non-expansive, and the downstream computation is `A @ relu(M) @ W2`, then

`|A @ relu(M) - A @ relu(M_hat)| <= |A| @ |E|`,

and componentwise `|E| <= Delta` gives

`B_prop = |A| @ Delta @ |W2|`.

However, the guidance also describes the certificate as covering “one post-aggregation affine message followed by ReLU and one frozen downstream linear map.” For that chain, the adjacency is already inside `M`, and propagating another `A` is wrong. The notation must freeze one exact chain, for example `Z = A relu(M) W2` or `Z = relu(A M) W2`, and define where quantization occurs. Until this is fixed, the main theorem is ambiguous rather than fully sound.

### Deterministic containment interpretation

**8/10 if the definitions are fixed.** Using the known quantizer interval as `Delta`, without labels or measured errors, makes containment a deterministic theorem/implementation audit. It is valid to require 100% containment, but the result must never be described as independent statistical coverage. If `Delta` is estimated from actual errors, logits, test data, or a per-cell fitted maximum, the result becomes tautological and the main claim fails.

### Strong gate realism

**6/10** The prior six v1 rows have width/RMS from 3.06 to 6.72 and tightening from 79.7% to 85.1%, so the thresholds are plausible for the current setup. They are not evidence for the corrected 36-cell operator chain, especially after adding three seeds and two quantizer types. Treat the gate as a feasibility lock, not as a scientifically meaningful threshold. A failure should narrow the claim rather than trigger threshold relaxation.

## Key Strengths

- Clear separation of deterministic validity from empirical tightness.
- Explicit 36-cell matrix: 3 graphs x 3 seeds x 2 levels x 2 quantizers.
- Float64 certificate arithmetic is appropriate for auditable bounds.
- The prior-v1 limitation is acknowledged and old rows are marked background-only.
- Failure preservation and no-label inference constraints are appropriate.

## Main Weaknesses

- The operator order is inconsistent between the formula and the prose scope.
- The global comparator is deliberately loose; the Euclidean comparator is not clearly the standard tight Euclidean bound.
- Width/RMS, tolerance, clipping/saturation, tie-breaking, and zero-denominator policies are not numerically fixed.
- “Tightening” is defined ambiguously as a ratio of medians in the guidance, while prior values appear to be per-cell ratios of width/RMS.
- The evidence supports a narrow affine certificate, not a broad GNN-to-SNN or SNN robustness contribution.
- Three seeds and three graphs are adequate for a screening matrix but weak for a Q2+ generality claim without dispersion and failure analysis.

## Required Actions Before Proceeding

1 Freeze the exact tensor shapes and operator order. State whether quantization is before or after adjacency aggregation, and derive the bound for that chain only.
2 Define `M`, `M_hat`, `E`, `Delta`, `A`, `W1`, `W2`, and each matrix dimension. State whether `Delta` is a half-step, an interval radius, or a clipping-aware bound.
3 Replace or supplement the weak baselines with a correctly defined rowwise Euclidean/Lipschitz bound and a stronger interval or layerwise norm baseline. Keep the global scalar as a reference, not the main fairness test.
4 Freeze the metric policy: exact width/RMS formula, per-cell tightening formula, denominator-zero handling, numerical tolerance, and float32/float64 rounding rules.
5 Report all 36 cells, including failures, with seed/graph/level/quantizer dispersion and the worst cell. Do not use actual errors to construct `Delta` or tune the bound.
6 Narrow the novelty statement to an operator-aware deterministic envelope for the specified frozen two-layer GCN chain. Keep temporal SNN, energy, robustness, and multi-layer claims out of scope.

## Fatal Risks

- **Fatal if unresolved:** contradictory operator order invalidates the stated certificate.
- **Fatal if unresolved:** any use of measured errors to form `Delta` turns containment into a construction identity.
- **Major:** claiming strong tightness against only a global scalar bound overstates the baseline contribution.
- **Major:** undefined width/RMS or tightening policy can make the strong gate non-reproducible.
- **Major:** broad GNN-to-SNN, robustness, or temporal/energy language would exceed the evidence.

**Recommendation:** proceed only after the required revisions and a corrected, non-tautological implementation audit. The current package is suitable for experiment correction, not manuscript drafting.
