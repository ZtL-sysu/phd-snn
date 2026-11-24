# CCFA Pre-Experiment Review

review_execution: independent-agent

## Verdict

**BLOCK**

**Score: 5.8/10**  
**Confidence: high** for design and accounting checks; novelty confidence remains medium.

POS-C13 v2 repairs the prior multi-seed and missing-control gaps: it now requires five split/probe seeds, five node-permutation seeds, five hop-shuffle seeds, a fixed raw probe, paired task comparisons, and complete negative-control reporting. The experiment should not launch yet because the hybrid bit ledger is underdefined and the shuffled-hop strong gate can become a construction artifact.

## Evidence Reviewed

- `inputs/guidance-v2.md`
- `contract-extraction.yaml`
- `claim-evidence-matrix.md`
- `strong-result-feasibility-lock.md`
- `inputs/prior-pos-v1-methods.json`
- `inputs/prior-independent-review.md`

No experiment was run and no input was modified.

## Prior-Gap Resolution

| Prior gap | v2 status | Judgment |
|---|---|---|
| Single split/probe seed | Five seeds with mean, sample SD and all rows | Resolved |
| Missing permutation audit | Two graphs x five node-permutation seeds | Resolved structurally |
| Missing shuffled-hop control | Two graphs x five hop-shuffle seeds | Present, but definition is not yet safe |
| Fixed-probe transfer absent | Raw-trained probe evaluated on raw/encoded/ordered/shuffled | Resolved structurally |
| Hybrid not best accuracy variant | Gate claims retention versus raw, not accuracy superiority | Appropriately narrowed |
| Broad conversion claim | Restricted to ordered hop-message coding | Resolved |

## Hybrid Gates

Prior seed-0 evidence is encouraging:

- relative Frobenius error: 2.46% on Chameleon and 3.06% on Squirrel;
- reported storage reduction: 10.17x on both graphs;
- hybrid balanced accuracy is 2.13 and 2.20 percentage points above raw;
- Lloyd-only and uniform variants are not uniformly worse, so the method must not claim general accuracy superiority.

The `≤5%` fidelity gate is reasonable. The `≤2 pp` mean loss gate is falsifiable but should use paired raw-minus-hybrid differences for identical splits and probe seeds. Five seeds may reveal substantial variance, but the fixed gate is preferable to post-hoc threshold changes.

## Fixed-Probe Design

The fixed-raw-probe transfer is the appropriate way to test whether an encoded representation remains usable without representation-specific retraining. The contract must freeze:

1 one probe fit per graph/split seed on raw features only;
2 identical normalization and feature ordering across representations;
3 identical probe weights, intercept, split and evaluation nodes;
4 no tuning based on encoded/shuffled results;
5 separate retrained-probe results, clearly labeled as different evidence.

The current guidance addresses most of these points. It should explicitly state that the fixed probe and split are reused unchanged across raw, uniform, Lloyd, hybrid, ordered and shuffled rows.

## Bit Accounting — Blocking

The prior `average_bits=3.145` and `10.17x` reduction are not reproducible from the stated “8-level Lloyd codebook plus 0.5% exact escapes.” Eight fixed-length Lloyd symbols already require three bits/value. An additional escape symbol for eight retained centroids requires a ninth symbol and therefore four bits/value if fixed length, plus the exact escape payload. A simple conservative ledger is:

- 4-bit symbol for eight centroids plus escape;
- 32-bit float32 payload for 0.5% escapes;
- expected `4 + 0.005*32 = 4.16` bits/value before codebook overhead;
- reduction about `32/4.16 = 7.69x`, still above the 4x gate but well below 10.17x.

Alternatively, seven centroids plus one escape code can use three-bit symbols and add `0.005*32=0.16` bits/value, but that is a seven-level codebook plus escapes—not the stated eight-level method. The reported `3.145` appears to add only 29 bits per escape and omits the escape marker, indices, codebook, and decoder metadata. The exact serialization scheme and amortized codebook cost must be frozen before claiming storage.

## Shuffled-Hop Gate — Blocking

The POS-E ratio `shuffled error ≥1.25 x ordered error` is meaningful only if both errors are defined against matched references. If shuffled output is compared to ordered raw `H`, the ratio mostly measures the deliberate permutation and is nearly guaranteed. If the same shuffle is applied to both target and reconstruction, the ratio instead tests coding distortion under reordered blocks.

The contract must define:

- whether the shuffle permutes hop blocks independently per node or uses one global hop permutation;
- whether raw and encoded representations use the same shuffle;
- the target matrix for ordered and shuffled Frobenius error;
- whether shuffle seeds are paired across methods;
- how fixed-probe ordered/shuffled accuracy complements rather than duplicates POS-E.

The fixed raw probe is the stronger task-level order control. POS-E should remain a representation-order diagnostic unless its target is defined non-tautologically.

## Novelty Scope

Lloyd quantization, exact escapes, multi-hop features, and permutation equivariance are established ingredients. The defensible novelty is their combined hop-message coding and order-control protocol for frozen graph positional messages. Do not claim a new general quantizer, graph transformer, SNN training method, temporal conversion, energy or hardware result.

## Fatal Risks

- **Fatal:** bit accounting is incomplete and the 10.17x figure is not derivable from the stated format.
- **Fatal:** shuffled-hop error can be tautological without a matched-reference definition.
- **Major:** matrix notation combines split and permutation seed axes ambiguously.
- **Major:** escape selection and codebook fitting data scope are unspecified.
- **Major:** novelty remains constrained by standard quantization and positional-message prior art.

**Recommendation:** block until the serialization ledger and shuffled-hop reference are frozen. The multi-seed accuracy and permutation plan is otherwise suitable for corrected execution.
