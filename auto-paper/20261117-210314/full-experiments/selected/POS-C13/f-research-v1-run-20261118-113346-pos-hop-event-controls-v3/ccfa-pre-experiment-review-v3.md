# CCFA Pre-Experiment Review v3

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 8.3/10**  
**Confidence: high** for the corrected design and accounting; novelty confidence remains medium.

The two fatal v2 issues are resolved. The hybrid serialization now has an exact conservative bit ledger, and the shuffled-hop control compares mismatched-codebook reconstruction with the matched shuffled raw target rather than shuffling target and reconstruction together. The v3 contract is suitable for pre-registered execution.

## Evidence Reviewed

- `corrections/p1b-v2-review-resolution.md`
- `inputs/guidance-v3.md`
- `contract-extraction.yaml`
- `strong-result-feasibility-lock.md`

No experiment was run and no input was modified.

## Bit Ledger

The alphabet contains eight float32 Lloyd centroids plus one escape symbol, so each value has a fixed four-bit symbol. An escaped value adds one float32 payload. Each channel stores eight float32 centroids, costing 256 bits. For `N` values in a channel:

`average_bits = 4 + 32 f_escape + 256/N`.

This accounts for the symbol, escape payload, and amortized codebook without a separate mask or index stream. At the nominal `f_escape=0.005`:

- Chameleon (`N=2277`): `4.27243` bits/value, about `7.49x` reduction from float32.
- Squirrel (`N=5201`): `4.20922` bits/value, about `7.60x` reduction.

The conservative reductions exceed the 4x gate and no longer rely on the unsupported 10.17x accounting.

## Mismatched-Shuffle Control

The corrected protocol is non-tautological:

1. Fit channel codebooks on canonical ordered `H`.
2. Apply one global hop-block permutation to raw columns.
3. Quantize the shuffled columns with unchanged ordered codebooks.
4. Compare reconstruction with shuffled raw `S H`.
5. Divide shuffled reconstruction error by ordered reconstruction error.

Target and reconstruction are not shuffled together. The ratio therefore measures sensitivity to channel/codebook mismatch caused by canonical hop order. It is not a guaranteed identity from an artificial target permutation.

## Other Corrections

- Five split/probe seeds and five permutation/shuffle seeds remain fixed.
- Fixed raw probes reuse identical weights, intercepts, splits and evaluation nodes.
- Retrained probes are separate descriptive evidence.
- Representation and task rows have explicit codebook/escape fitting scopes.
- Paired balanced-accuracy loss, sample SD and all failed controls are required.
- The strong gate remains unchanged in substance: fidelity, conservative storage, permutation audit, mismatched-shuffle ratio and paired task retention.

## Claim Boundary

POS-E supports **ordered-codebook mismatch sensitivity**. It does not alone prove that hop order carries task-relevant information. POS-F fixed-probe results provide descriptive task-level evidence, but remain nonbinding. Keep novelty limited to combined hop-message coding, exact escape accounting, permutation audit and mismatch control; do not claim a new general quantizer or end-to-end SNN conversion result.

## Remaining Non-Blocking Actions

1 State whether the POS-E 1.25x gate applies to every shuffle seed, the minimum across seeds, or a predeclared mean.
2 Keep paired seed keys explicit in the raw table.
3 Use “ordered-codebook mismatch” rather than broad “hop information” wording for POS-E.

**Recommendation:** proceed with the frozen v3 contract.
