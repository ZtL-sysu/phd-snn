# CCFA Pre-Experiment Integrity Review v3

review_execution: independent-agent

## Integrity Verdict

**PROCEED**

**Score: 8.5/10**  
**Confidence: high**

The v3 formulas, control construction and experimental scope are internally consistent. No remaining integrity defect blocks execution.

## Formula Checks

- Representation: `H=[X,AX,A^2X,A^3X]` remains dimensionally valid.
- Alphabet: eight centroid IDs plus escape require nine fixed-length symbols, hence four bits/value.
- Escape payload: one float32 value adds 32 bits only when the escape symbol occurs.
- Codebook: eight float32 centroids per channel add 256 bits per channel.
- Amortization: `256/N` is correct when `N` is the number of values per channel.
- Total: `4+32f_escape+256/N` includes all stated serialization costs.

## Control Checks

- **Permutation:** recompute `H` under permuted graph/features, encode, inverse-permute and compare. This is a deterministic implementation audit.
- **Mismatched shuffle:** ordered codebooks are applied to globally hop-shuffled raw columns and reconstruction is compared with the same shuffled raw target. This avoids target/reconstruction co-shuffling and is not tautological.
- **Fixed probe:** identical probe weights, intercept, splits and evaluation nodes are reused. This supports paired transfer evidence.
- **Task fitting:** representation rows use all-node label-free codebooks; task rows fit codebooks/escape thresholds on training nodes only. The scopes are explicit and not interchangeable.

## Gate Integrity

| Gate | Status | Reason |
|---|---|---|
| Hybrid error ≤5% | Pass as a preregistered target | Prior single-seed values were 2.46%/3.06% |
| Storage ≥4x | Pass as a preregistered target | Conservative ledger predicts 7.49x/7.60x at 0.5% escapes |
| Permutation error ≤1e-10 | Sound | Deterministic numerical audit |
| Mismatch ratio ≥1.25 | Sound if aggregation is declared | Non-tautological codebook-order mismatch |
| Mean paired accuracy loss ≤2 pp | Sound | Five fixed paired split/probe seeds |
| Fixed-probe accuracy | Correctly descriptive | No stronger gate |

## Remaining Reproducibility Notes

1 Record the actual escape fraction and full formula inputs per row.
2 Record the global shuffle permutation seed and mapping.
3 Declare POS-E aggregation across five shuffle seeds.
4 Preserve all negative rows and do not tune codebooks/escape rates after task results.

**Recommendation:** proceed.
