# Concern-to-Action Ledger

review_execution: independent-agent

## Verdict

**BLOCK**

**Score: 5.7/10**  
**Confidence: high**

## Numbered Concerns

| # | Severity | Concern | Evidence | Required action |
|---:|---|---|---|---|
| 1 | Fatal | Bit ledger cannot reproduce `3.145` bits/value or `10.17x` from 8 Lloyd levels plus escapes | Prior methods report 3.145 bits; contract omits tag/index, payload, and codebook accounting | Freeze serialization and symbolic/numerical bit ledger |
| 2 | Fatal | POS-E shuffled error can be a permutation artifact | No target/reference definition for ordered versus shuffled Frobenius error | Apply matched shuffles to target and reconstruction or redefine POS-E |
| 3 | Major | Matrix and paired-seed row counts are ambiguous | Contract compresses split/probe and permutation/shuffle axes | Publish exact rows per experiment and pairing keys |
| 4 | Major | Fixed-probe reuse is not explicit enough | Guidance mentions transfer but not immutable probe weights/normalization | Freeze probe, split and preprocessing across all representations |
| 5 | Major | Escape/codebook fitting scope is unspecified | 0.5% exact escape selection has no train/test/transductive rule | State label-free data scope and decoder behavior |
| 6 | Medium | Mean accuracy loss can hide failed seeds | POS-A gates only five-seed mean | Report every paired difference and SD; do not hide outliers |
| 7 | Medium | Novelty may be overstated | Lloyd, escapes, multi-hop features and equivariance are established | Frame contribution as combined hop-message coding/order-control study |

## Positive Controls To Retain

- Five split/probe seeds with sample SD and complete rows.
- Five node-permutation and five hop-shuffle seeds.
- Raw/uniform/Lloyd/hybrid baselines.
- Fixed raw probe separated from retrained probes.
- Exact inverse-permutation audit.
- Negative and failed controls preserved.

## Acceptance Condition

Proceed only after concerns 1–2 are fixed and concerns 3–5 are frozen in the experiment contract. No threshold relaxation is permitted after results are observed.
