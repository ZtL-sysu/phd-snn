# CCFA Baseline Evidence Review

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 9.1/10**  
**Confidence: high**

The repaired P3A baseline resolves the prior stop-loss. It now supports hybrid fidelity, conservative storage, permutation equivariance and a non-tautological ordered-codebook mismatch control. The full five-seed task/probe campaign remains credible and can proceed under the frozen v3 protocol.

## Verified Evidence

- Hybrid errors are 3.95% and 4.88%, below the 5% ceiling.
- Conservative storage is 7.49x and 7.60x, above the 4x floor.
- Raw and hybrid permutation errors are at machine precision.
- All five shuffle permutations per graph are non-identity.
- Mean mismatched-shuffle ratios are 3.72x and 3.63x; minimum is 3.31x.
- Ordered and shuffled computations use the same escape-fraction/threshold policy according to the P3 regression gate.
- Summary statistics match the raw JSON exactly.

## Prior Defect Resolution

1 Mixed hybrid/Lloyd codec comparison: resolved by codec-consistent ordered/shuffled reconstruction.
2 Identity permutation included as a shuffle: resolved; identity count is zero.
3 Inflated ratio means: resolved; means are now 3.72x/3.63x rather than 14.70x/9.72x.
4 Strong gate direction: valid; every corrected ratio is above 1.25x.

## Task/Probe Credibility

The representation baseline now provides a sound foundation for POS-A through POS-F:

- hybrid fidelity and storage gates pass with auditable margins;
- permutation equivariance is verified;
- shuffled-hop mismatch is non-tautological and consistent;
- fixed-probe task evaluation remains paired and descriptive as preregistered.

The Squirrel error is relatively close to 5%, so the task results should not be framed as guaranteed. The five-seed accuracy gate remains genuinely falsifiable.

## Remaining Non-Blocking Action

Log shuffle-side escape fraction and threshold in each control row, even though the P3 gate confirms the shared policy. This would make the codec consistency directly auditable without relying on the gate narrative.

**Recommendation:** proceed to the full task/probe campaign without changing the representation rows or gates.
