# CCFA Pre-Experiment Integrity Review v4

review_execution: independent-agent

## Integrity Verdict

**BLOCK PENDING INDEX/FORMULA CORRECTION**

**Score: 6.0/10**  
**Confidence: high**

The v4 evidence policy, reconstruction precision, comparator fairness, control design, and numerical rules are internally disciplined. The remaining integrity defect is a dimensional inconsistency between the matrix envelope and its expanded scalar formulas.

## Claim-Evidence Alignment

| Claim | Frozen evidence | Integrity status | Required action |
|---|---|---|---|
| Deterministic containment | Exact chain and 36-cell audit | Sound | Implement the matrix-correct formula |
| Independent-box interval envelope | `abs(A)abs(A)Delta abs(W1)` | Sound | Correct the expanded node/channel expression |
| Valid Minkowski comparator | Intended `c_i ||delta||_2 ||W1[:,k]||_2` | Correct in substance, wrong as written | Remove mixed indexing |
| Fair global comparator | `B_global_col` | Sound and output-column matched | Retain unchanged |
| Global-uniform equality | 18 constant-radius cells | Sound and expected by construction | Retain as control |
| Per-channel tightening | 18 heterogeneous-radius cells | Logically possible and falsifiable | Retain gate after formula correction |
| Numerical reproducibility | Float64 and exact policies | Sound | Retain unchanged |

## Mathematical Checks

### Matrix computation

Let `p` index nodes and `h` index hidden channels. With `C=abs(A)abs(A)`, `c_i=sum_p C[i,p]`, and `Delta=1_N delta^T`, the exact componentwise interval envelope is

`B_abs[i,k] = sum_p sum_h C[i,p] delta_h abs(W1[h,k]) = c_i sum_h delta_h abs(W1[h,k])`.

This follows from `B_abs=C Delta abs(W1)` and is consistent with all declared tensor shapes.

### Invalid expanded formula

The frozen expression `sum_j C[i,j] delta_j abs(W1[j,k])` uses `j` as both a node index and hidden-channel index. It omits the node sum `c_i` and improperly pairs graph-node rows of `C` with weight rows in `W1`. It cannot be used as the implementation definition.

### Valid Minkowski comparator

For independent coordinate radii `delta_h`, grouping errors by source node and applying Minkowski followed by Cauchy-Schwarz gives

`B_mink[i,k] = c_i ||delta||_2 ||W1[:,k]||_2`.

It is a valid upper bound and satisfies `B_abs[i,k] <= B_mink[i,k]`. The frozen formula `||W1[:,k]||_2 sum_j C[i,j] delta_j` is not this quantity and is not valid under the stated dimensions.

### Global comparator and control

`B_global_col[i,k]=c_i max_h(delta_h)||W1[:,k]||_1` is valid and fair at the output-column level. If all `delta_h` are equal, it equals `B_abs` exactly. The planned equality control is therefore sound, while restricting the tightening gate to per-channel cells is required and correctly implemented.

## Numeric-Policy Checks

- **All-float64 reconstruction:** resolved. Float32 snapshots are cast before computation and no later float32 reconstruction is used.
- **Radius derivation:** resolved. `delta_h=s_h/2` is computed from quantizer parameters before quantization errors are inspected.
- **Constant channels:** resolved. `s_h=0`, identity quantization, and `delta_h=0` are explicit.
- **Tolerance:** resolved. The exact predicate includes absolute and relative terms.
- **Median axis:** resolved. All `N x C` bound entries are used.
- **Zero handling:** resolved. Zero ratios require zero numerator and zero RMS; otherwise the cell fails.
- **Clipping:** resolved. Endpoint safeguard is distinguished from prohibited out-of-range input.
- **NaN/Inf:** resolved. Non-finite rows fail and remain recorded.
- **Interpretation:** resolved. Containment is theorem/implementation validation, not statistical coverage.

## Overclaim Risk Register

| Risk | Severity after v4 | Safe treatment |
|---|---|---|
| General interval theorem | Low | Keep “tailored componentwise interval envelope” |
| Statistical coverage | Low | Keep deterministic-audit wording |
| Global-uniform tightening | Resolved | Report equality, not improvement |
| Per-channel tightening | Medium | Claim only after all 18 cells pass |
| Broad GNN-to-SNN/robustness/energy scope | Low | Preserve explicit exclusions |
| Formula-to-code mismatch | High until corrected | Use separate node/channel indices and audit shapes |

## Integrity Conclusion

The v4 contract resolves every prior numerical and gate-policy issue. It does not yet pass final integrity review because the written scalar formulas for `B_abs` and `B_mink` are dimensionally inconsistent with the valid matrix definitions. Correct those two expressions and synchronize the extraction contract. After that correction, no remaining integrity issue blocks the pre-registered experiment.
