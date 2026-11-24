# CCFA Baseline Numeric Audit

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 8.7/10**  
**Confidence: high**

The frozen baseline artifacts are numerically consistent and satisfy every baseline-first condition. The audit supports proceeding to the remaining seed cells; it does not certify the unrun 24 rows.

## Evidence Audited

- `inputs/guidance-v6.md`
- `contract-extraction.yaml`
- `strong-result-feasibility-lock.md`
- `corrections/p3-v5-baseline-stop-loss.md`
- `results/cert-baseline.json`
- `results/cert-baseline.csv`
- `audits/p3-baseline-gate.md`

No experiment was run and no input was modified. Numeric checks were recomputed directly from the frozen JSON and CSV.

## Unit Audit

| Field | Unit/type | Check |
|---|---|---|
| `actual_rms`, `max_abs_error`, `max_bound_excess` | logit units | Finite and dimensionally consistent |
| `*_width_over_rms`, `tightening` | dimensionless | Finite; tightening represented as fraction, not percent |
| `clipping_count`, `zero_step_channels` | nonnegative integer counts | Valid |
| `containment`, `minkowski_valid`, `global_equality`, `nonfinite` | Boolean status | Valid |
| `radius_sha256` | provenance identifier | 12 unique hashes for 12 rows |

All reported ratios use the same actual-RMS denominator within a cell. No percent/fraction unit mismatch was found: the 25% gate corresponds to `tightening >= 0.25`.

## Row And Serialization Audit

- Expected baseline shape: `3 datasets x 1 seed x 2 levels x 2 quantizers = 12`.
- JSON rows: 12; CSV rows: 12.
- Cartesian keys are complete and unique.
- JSON/CSV numeric maximum absolute difference: `0`.
- JSON/CSV nonnumeric mismatches: `0`.
- Every row has phase `baseline`; no row is silently omitted.

## Coverage And Containment

- Deterministic containment: `12/12`.
- `max_bound_excess` is negative in every row; maximum value is `-0.096039772553308`, so no observed error exceeds its proposed bound.
- Non-finite rows: `0`.
- Clipping events: `0`.
- This is theorem/implementation containment only, not statistical coverage.

## Comparator Ordering

- `B_abs <= B_mink` status: `12/12`.
- Proposed width/RMS never exceeds Minkowski width/RMS in any row.
- Proposed width/RMS never exceeds the global outputwise comparator; equality holds for global-uniform rows and strict improvement holds for rowwise rows.
- The collapsed scalar reference is looser in all rows, as expected, and is excluded from the strong gate.

## Equality Control

- Global-uniform rows: `6/6`.
- Equality flags pass in all six rows.
- Maximum absolute proposed/global width-RMS gap: `7.105427357601e-15`, within the frozen tolerance.
- Reported global tightening spans `-4.44e-16` to `0`; the exact median is `-1.11e-16`, which is floating-point zero within tolerance.

## Tightening Audit

- Rowwise rows: `6/6`.
- Recomputed `1 - proposed_width_over_rms/global_width_over_rms` matches every reported value exactly at parsed precision.
- Range: `0.783821147712092` to `0.813609043452745`.
- Median: `0.80972455633038`.
- Gate result: all six are far above `0.25`.

## Descriptive Width Audit

| Quantizer | Proposed min | Proposed median | Proposed max | Minkowski max | Global max |
|---|---:|---:|---:|---:|---:|
| Global | 9.9888 | 17.1087 | 28.2985 | 31.0451 | 28.2985 |
| Rowwise | 15.8356 | 29.2856 | 36.9134 | 40.6544 | 170.7539 |

Absolute width/RMS remains descriptive. The observed range confirms why the v6 contract correctly removed absolute-width thresholds.

## Other Checks

- Actual RMS range: `0.0293451` to `0.9580673`.
- Maximum absolute error range: `0.2788362` to `8.0280742`.
- Zero-step rows are preserved: Chameleon rowwise has 233 zero-step channels per level; Squirrel rowwise has 165 per level.
- No zero-denominator substitution is present because every actual RMS is positive.

## Numeric Conclusion

The supplied baseline PASS is supported. The files are synchronized, units are coherent, all hard baseline checks pass, and the rowwise tightening margin is large. The phrase “strongest feasible comparator” in `audits/p3-baseline-gate.md` should be read only as the strongest comparator selected in this design; the numeric audit proves validity, not global optimality.
