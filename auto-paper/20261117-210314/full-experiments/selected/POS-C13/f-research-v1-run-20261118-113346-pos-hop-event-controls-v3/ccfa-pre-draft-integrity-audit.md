# CCFA Pre-Draft Integrity Audit

review_execution: independent-agent

## Integrity Verdict

**PROCEED**

**Score: 8.9/10**  
**Confidence: high**

The corrected evidence package is numerically consistent and the fixed-probe leakage repair is supported by the preserved negative run and corrected task rows. No integrity defect blocks drafting.

## Row And Summary Audit

- Corrected task rows: 40 = 2 graphs x 5 split seeds x 4 methods.
- Fixed-probe rows: 90 = 2 graphs x 5 split seeds x 4 ordered methods plus 5 shuffled controls.
- All numeric fields are finite.
- `pos-task-summary.json` exactly reproduces the corrected row means, losses and fixed-probe gaps.
- `p5-gate-verification.json` reports 40 task rows, 90 fixed rows and all six checks passed.

## Bit Ledger

Every corrected hybrid task row exactly satisfies

`average_bits_per_value = 4 + 32 escape_fraction + 256/N`.

The corresponding storage reduction is exactly `32/average_bits_per_value`. Maximum recomputation difference is zero. Training-only escape fractions vary slightly by split seed and are retained.

## Leakage Prevention

The first task run is preserved in `corrections/pos-task-leaky-probe-v1.json`. Its balanced accuracies are near 0.99, while corrected train-only results are 0.62/0.46-scale values. Corrected and leaky rows have identical representation error, bit ledger, storage and escape fields, while task metrics change sharply. This pattern is consistent with repairing probe fitting rather than altering representations.

`experiment-traceability.md` states that task codebooks and escape thresholds fit training indices only and that fixed raw probes reuse identical weights, intercepts, splits and test nodes. The row schema should ideally add fit-scope, split-hash and probe-hash fields, but the current evidence and gate tests support the repair.

## Numeric Claims

| Claim | Recomputed | Status |
|---|---:|---|
| Chameleon hybrid loss | 0.083373 pp | pass |
| Squirrel hybrid gain | 0.767575 pp | pass |
| Chameleon fixed ordered-minus-shuffled | 9.566173 pp | pass |
| Squirrel fixed ordered-minus-shuffled | 9.080824 pp | pass |
| Hybrid error max | 3.967%/4.860% | pass |
| Hybrid storage minimum | 7.476x/7.591x | pass |

## Controls

- Five paired split/probe seeds are complete.
- Five permutation seeds and five non-identity shuffle seeds are preserved.
- Representation shuffle rows use codec-consistent escape policy.
- Fixed raw probes separate ordered hybrid from shuffled hybrid without retraining.
- Retrained and fixed-probe metrics are reported separately.
- All negative and leaky rows remain preserved and excluded from accepted results.

## Planned Figure Integrity

The raw rows support all planned figures and tables. Figure 3 must not convert descriptive fixed-probe gaps into causal hop-order claims. Table 2 should include every seed and control row and the sample SD or paired differences.

## Remaining Hardening

1 Add `fit_scope`, split-index hash and fixed-probe weight hash to task/control rows or a linked manifest.
2 Preserve the exact leaky run hash and exclusion record.
3 Report sample SD and paired seed differences in the manuscript table.

**Recommendation:** proceed.
