# CCFA Baseline Evidence Review

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 8.3/10**  
**Confidence: high** for the baseline evidence; **medium-high** for extrapolation to the remaining 24 cells.

The P3 baseline stop-loss is handled fairly. The v6 claim explicitly abandons absolute width, preserves the negative evidence, and tests only deterministic validity plus relative rowwise tightening against a matched global-radius comparator. The baseline results support launching the full 36-cell campaign.

## Evidence Reviewed

The same frozen contract, stop-loss record, JSON/CSV baseline rows, and P3 gate summary were used. No experiment was run and no input was edited.

## Stop-Loss Assessment

The v5 failure was an unsupported absolute-width target under the corrected two-aggregation chain. Guidance-v6 does not conceal or relax that target:

- width/RMS is descriptive and has no hard gate;
- the failed v5 target remains negative evidence;
- deterministic containment and comparator validity remain hard gates;
- utility is restricted to rowwise-versus-global relative tightening;
- global-uniform quantization is an equality control.

This is an explicit claim correction, not silent threshold weakening.

## Baseline Evidence

- Coverage audit: 12/12 deterministic containment.
- Comparator audit: 12/12 `B_abs<=B_mink`.
- Global control: 6/6 equality within numerical tolerance.
- Rowwise utility: 6/6 cells tighten by 78.38–81.36%, median 80.97%.
- Failure audit: no clipping, non-finite values, or zero-denominator substitutions.
- Serialization: JSON and CSV agree exactly at parsed precision.

The baseline covers one-third of the final matrix and includes every dataset, level, and quantizer at seed 0.

## Baseline Fairness

`B_abs` and `B_global_col` share the same operator chain, radius provenance, output columns, precision, and comparator construction. Replacing heterogeneous row radii by their maximum isolates the intended rowwise-granularity effect. The Minkowski comparator is valid but its ordering is analytic and should not be counted as an empirical improvement.

The comparison supports only a rowwise radius ablation claim. It does not establish superiority over all certified norm bounds or state-of-the-art methods.

## Full 36-Cell Credibility

The full target remains credible to attempt:

- every baseline condition passes;
- rowwise tightening exceeds the gate by more than 53 percentage points at the worst observed cell;
- global equality behaves exactly as derived;
- the result repeats across both quantization levels and all three datasets at seed 0.

It is not yet confirmed. The remaining 24 rows vary checkpoint seeds and may change row-radius heterogeneity, hidden weights, RMS scale, and per-cell tightening. The appropriate status is **credible pre-registered target**, not expected result or completed evidence.

## Required Full-Run Discipline

1 Run the remaining seeds without changing thresholds or formulas.
2 Preserve every failed or negative row.
3 Keep width/RMS descriptive even if values are high or unstable.
4 Report the 18 rowwise cells individually, with minimum and median tightening.
5 Treat global equality as a structural control, not a performance win.
6 Describe `B_mink` as a valid comparator check, not necessarily the strongest possible bound.
7 Do not promote deterministic containment to statistical coverage.

## Remaining Risks

- **Medium:** seed 1/2 may reduce rowwise radius heterogeneity and lower tightening.
- **Medium:** the contribution remains application-specific and narrow.
- **Low:** baseline units, formulas, comparator ordering, and controls show no integrity defect.

**Recommendation:** proceed with the full 36-cell experiment under the unchanged v6 gate.
