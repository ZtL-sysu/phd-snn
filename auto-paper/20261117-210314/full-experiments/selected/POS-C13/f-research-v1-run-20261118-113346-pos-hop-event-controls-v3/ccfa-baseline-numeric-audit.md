# CCFA Baseline Numeric Audit

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 9.3/10**  
**Confidence: high**

The codec-consistent shuffle repair resolves the prior mixed-codec and identity-permutation defects. All representation baseline gates now pass and the reported summary is numerically consistent with the raw rows.

## Row Audit

- Representation rows: 8 = 2 graphs x 4 methods.
- Permutation rows: 10 = 2 graphs x 5 seeds.
- Shuffle rows: 10 = 2 graphs x 5 non-identity seeds.
- Identity permutations: 0.
- Reported error ratios recompute exactly from `shuffled_error/ordered_error`.

## Bit Ledger

The hybrid rows exactly satisfy

`average_bits = 4 + 32 f_escape + 256/N`.

| Graph | Escape fraction | Bits/value | Recomputed | Storage reduction |
|---|---:|---:|---:|---:|
| Chameleon | 0.00500021 | 4.27243543 | 4.27243543 | 7.48987x |
| Squirrel | 0.00500001 | 4.20922147 | 4.20922147 | 7.60236x |

Both reductions exceed the 4x gate. The actual escape fractions include threshold ties as intended.

## Representation Error

- Chameleon hybrid: `0.0395166` (3.952%); pass against 5%.
- Squirrel hybrid: `0.0487877` (4.879%); pass against 5%.
- Uniform and Lloyd-only errors remain higher and are preserved.

## Permutation Audit

- Maximum raw error: `2.220446049250313e-16`.
- Maximum hybrid error: `2.220446049250313e-16`.
- All ten rows pass the `1e-10` gate.

## Codec-Consistent Shuffle Audit

The repaired shuffle rows use the ordered hybrid error as denominator and codec-consistent hybrid reconstruction as numerator. The P3 gate confirms that ordered and shuffled rows share the same escape-fraction/threshold policy. All five permutations per graph are non-identity.

| Graph | Mean ratio | Minimum | Maximum | Gate |
|---|---:|---:|---:|---|
| Chameleon | 3.72469 | 3.45440 | 3.87557 | pass |
| Squirrel | 3.62643 | 3.31026 | 4.08476 | pass |

Every individual ratio exceeds 1.25. The prior inflated mixed-codec ratios are no longer present.

## Summary Consistency

`pos-representation-summary.json` matches the raw rows:

- hybrid values match exactly;
- permutation maxima match exactly;
- shuffle mean/min/max match exact recomputation;
- `identity_shuffle_count=0`;
- `representation_gate_pass=true`.

One minor traceability improvement remains: shuffle rows do not repeat the escape fraction and threshold fields directly. The shared policy is confirmed by `audits/p3-representation-gate.md`, but those values should be logged per shuffle row in future raw exports.

## Numeric Conclusion

Bit accounting, representation error, storage, permutation equivariance and codec-consistent shuffle ratios all pass. The representation baseline is ready to support the full task/probe campaign.
