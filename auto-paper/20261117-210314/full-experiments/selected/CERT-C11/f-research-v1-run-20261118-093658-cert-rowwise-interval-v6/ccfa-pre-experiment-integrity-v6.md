# CCFA Pre-Experiment Integrity Review v6

review_execution: independent-agent

## Integrity Verdict

**PROCEED WITH CLAIM GUARDRAILS**

**Score: 7.5/10**  
**Confidence: high**

The v6 rowwise formulation is mathematically valid and the baseline stop-loss is disclosed and handled through a narrower, pre-registered claim. No formula, comparator, or gate integrity defect blocks experimentation.

## Claim-Evidence Alignment

| Claim | Evidence contract | Integrity judgment |
|---|---|---|
| Deterministic containment | 36 cells with error-diagnostic exclusion | Sound theorem/implementation audit |
| Valid rowwise interval bound | `abs(A)abs(A)Delta abs(W1)` | Sound for independent coordinate radii |
| Minkowski validity | `B_abs<=B_mink` | Analytically valid; not an empirical win |
| Global-uniform equality | 18 constant-radius cells | Correct structural control |
| Rowwise tightening | 18 cells against `B_global_col` | Fair radius-granularity ablation |
| Absolute width utility | Width/RMS reported without threshold | Honest and appropriately limited |

## Mathematical Checks

### Rowwise Delta

`Delta in R^(N x H)` is computed from rowwise quantizer parameters before quantization errors are inspected. For a constant row, identity reconstruction and zero radius are specified. For ordinary rows, the half-step radius covers the float64 rounding error.

### Proposed bound

With `C=abs(A)abs(A)`, independent coordinate errors satisfy

`abs(Z-Z_hat)<=C Delta abs(W1)`.

The node and hidden-channel dimensions are correct, and the result has shape `N x C_out`.

### Minkowski comparator

For `r_p=||Delta[p,:]||_2`,

`B_mink[i,k]=(C r)[i] ||W1[:,k]||_2`

is a valid upper bound. It follows by summing source-node contributions with Minkowski and bounding each hidden row with Cauchy-Schwarz. Therefore `B_abs<=B_mink` is sound.

### Global comparator

`B_global_col[i,k]=rowsum(C)[i] max(Delta)||W1[:,k]||_1`

is a valid outputwise global-radius ablation. Constant global radii produce exact equality with `B_abs`; heterogeneous row radii can produce genuine relative tightening.

## Numeric And Evidence Policy

- **Precision:** all quantization, reconstruction, bounds, and metrics are float64.
- **Tolerance:** `value<=bound+1e-10+1e-12*abs(bound)` remains explicit.
- **Width/RMS:** median over all bound entries divided by actual RMS, descriptive only.
- **Tightening:** per-cell and limited to the 18 rowwise cells.
- **Zero/NaN/Inf/clipping:** failure rules remain explicit.
- **Radius provenance:** no actual errors, labels, or logits construct `Delta`.
- **Negative evidence:** v5 absolute-width failure is preserved and acknowledged.

## Overclaim Risks

| Risk | Severity | Required treatment |
|---|---|---|
| Presenting descriptive width as success | High | Keep it out of the headline claim |
| Calling analytic comparator ordering empirical | Medium | Label it a validity check |
| Generalizing 25% beyond tested rowwise cells | Medium | Scope it to the frozen matrix |
| Calling the global comparator state of the art | High | Call it a global-radius ablation |
| General GNN-to-SNN or robustness claim | High | Preserve the explicit exclusions |
| Ignoring the v5 stop-loss | High | Preserve and discuss the failed target |

## Integrity Conclusion

The baseline stop-loss is resolved without an unfair comparator or hidden threshold change. The rowwise method is evaluated against a matched global-radius ablation, absolute width is honestly descriptive, and the remaining strong claim is limited to deterministic validity plus pre-registered relative tightening. Provided the manuscript retains these boundaries, the integrity gate is clear to proceed.
