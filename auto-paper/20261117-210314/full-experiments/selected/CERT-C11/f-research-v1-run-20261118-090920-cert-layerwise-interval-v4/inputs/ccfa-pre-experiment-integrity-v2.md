# CCFA Pre-Experiment Integrity Review

review_execution: independent-agent

## Integrity Verdict

**REVISE BEFORE EVIDENCE FREEZE**

The claim-evidence structure is honest and appropriately narrow, but the mathematical and numerical contracts need tightening before the corrected rows can support the main claim. The principal integrity risk is not fabrication; it is overclaiming a deterministic construction guarantee as an empirical certificate result and comparing it with insufficiently strong baselines.

## Claim-Evidence Alignment

| Claim component | Frozen evidence | Integrity judgment | Required correction |
|---|---|---|---|
| Deterministic validity of `B_prop` | 36-cell containment plan; prior v1 rows are background only | Valid in principle if `Delta` is a known quantizer interval and the operator order is exact | State the exact chain and prohibit error-derived `Delta` |
| Operator-aware tightness | Width/RMS and tightening plan | Potentially valid, but baseline fairness is weak | Add a correct Euclidean/Lipschitz comparator and stronger interval baseline |
| Quantizer generality | Global and per-channel uniform quantizers | Narrow but auditable | Specify clipping, range, rounding ties, and per-channel dimensions |
| Scope stability | 3 graphs x 3 seeds x 2 levels x 2 quantizers | Adequate for a screening matrix, not broad generality | Report full cellwise dispersion and preserve all failures |
| Interpretation boundary | Prior review and limitation ledger | Correctly separates deterministic audit from statistical coverage | Keep this wording in the manuscript and abstract |

## Mathematical-Definition Checks

### 1 Operator-chain ambiguity

The document writes the bound as

`|A @ relu(M) - A @ relu(M_hat)| <= |A| @ |E|`

but also calls the certified object a “post-aggregation affine message followed by ReLU and one frozen downstream linear map.” These are different computations:

- `A @ relu(M) @ W2`: adjacency is propagated after ReLU.
- `relu(A @ M) @ W2`: adjacency is propagated before ReLU.
- `relu(M) @ W2` with `M = A @ X @ W1`: adjacency is already inside `M`; no second `A` belongs in the bound.

The proof is sound only after one chain is frozen. The report cannot treat all three as interchangeable.

### 2 ReLU and interval propagation

For componentwise ReLU, `|relu(x)-relu(y)| <= |x-y|` is valid. Therefore, if `E = M-M_hat` and `|E| <= Delta`, then `|A| @ Delta @ |W2|` is a valid worst-case bound for the chain `A @ relu(M) @ W2`. This does not depend on labels or empirical coverage.

The interval claim requires `Delta` to be a known deterministic quantizer radius. If the quantizer saturates, the radius must include saturation error. If range selection uses observed messages, the resulting bound may still be valid only conditional on that range and must not be described as an unconditional certificate.

### 3 Euclidean comparator definition

The frozen formula

`rowsum(abs(A))[i] * ||Delta_row||_2 * ||W2[:,k]||_2`

is not clearly the standard rowwise Euclidean bound. A tighter and more interpretable form is

`(sum_j (|A_ij| ||Delta_j||_2)^2)^(1/2) * ||W2[:,k]||_2`.

If `Delta_j` is identical for every node, this becomes `||A_i||_2 ||Delta||_2 ||W2[:,k]||_2`. Using `rowsum(|A_i|)` makes the comparator looser and may make CERT-D pass by construction. Define the intended comparator exactly before interpreting it as evidence.

## Numeric-Policy Checks

- **Cell count:** `3 x 3 x 2 x 2 = 36`; this is internally consistent.
- **Precision:** float64 for certificate arithmetic and float32 for model/message computation is reasonable, but the conversion boundary and tolerance are not specified.
- **Tolerance:** “beyond numerical tolerance” is not reproducible. Freeze an absolute and relative tolerance and state whether comparisons use elementwise or aggregate values.
- **Width/RMS:** define the numerator and denominator. If the denominator is RMS actual error, specify the zero-error case. Do not silently add epsilon.
- **Tightening:** prior values equal `1 - (proposed width/RMS)/(global width/RMS)` per cell. The guidance also says `1 - median(B_prop)/median(B_global)`, which is a different statistic. Choose one definition and state whether the 25% gate is per-cell minimum or a ratio of aggregate medians.
- **Non-finite values:** require rejection of NaN/Inf in all rows, with explicit failure status rather than omission.
- **Rounding:** specify quantizer tie-breaking, level endpoints, clipping/saturation, and whether `Delta` is a half-step or a full interval width.

## Baseline and Comparator Integrity

The global scalar bound is a valid sanity baseline but is too loose to establish fairness. The proposed formula uses coordinatewise information from both `Delta` and `W2`, whereas the scalar comparator collapses both. A strong paper should report:

1 the proposed absolute-value interval bound;
2 a correctly defined rowwise Euclidean or spectral-norm bound;
3 a stronger layerwise interval bound where applicable; and
4 the global scalar bound as a deliberately loose reference.

All bounds must use the same `A`, `Delta`, `W2`, normalization, quantizer, and precision policy. Actual error may be reported as a diagnostic, but it must not tune any bound or comparator.

## Overclaim Risk Register

| Risk | Severity | Why it matters | Safe wording |
|---|---|---|---|
| “100% coverage” as statistical evidence | High | Containment follows from the interval construction | “100% deterministic containment in the implementation audit” |
| “Substantially tighter certificate” from scalar comparison | High | The scalar bound is intentionally loose | “tighter than the global scalar reference; stronger comparator results are required” |
| General ANN-to-SNN conversion certificate | High | Only one frozen two-layer GCN chain is covered | “certificate for the specified frozen two-layer GCN message path” |
| Robustness or confidence claim | High | No perturbation distribution, labels, or confidence argument | “worst-case finite-precision message-error envelope” |
| Temporal, energy, or hardware claim | High | No SNN timing, event, energy, or hardware evidence | Remove from claims and conclusions |
| Generality across quantizers | Medium | Only two uniform schemes are planned | “within the tested uniform quantizer family” |
| Seed/graph generality | Medium | Three seeds and three graphs are limited | Report scope explicitly and show per-cell dispersion |

## Integrity Conclusion

The package has a defensible deterministic-bound idea and an appropriately cautious evidence policy. It is not yet claim-complete because the operator chain, comparator definitions, and numerical policies are not frozen precisely enough to prevent accidental overclaiming. Once those definitions are corrected and the corrected 36-cell rows are produced without error-derived tuning, the integrity posture can support a narrow certificate paper. Before that, the safe verdict is **revise**, not proceed or block.
