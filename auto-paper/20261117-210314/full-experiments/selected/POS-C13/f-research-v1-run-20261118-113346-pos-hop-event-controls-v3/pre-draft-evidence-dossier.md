# Pre-draft evidence dossier

## Problem and novelty delta

Multi-hop positional messages are expensive to transport and require conversion controls that distinguish ordered hop information from arbitrary feature permutations. The supported contribution is a combined codebook/escape serialization and control protocol for frozen graph positional messages: eight Lloyd centroids plus one escape symbol, exact conservative bit accounting, node-permutation audit, and ordered-codebook mismatched-shuffle testing. Standard Lloyd quantization and permutation equivariance are ingredients; the contribution is their application-specific combination and evidence protocol.

## Main claims

1. Hybrid representation error is 3.952% on Chameleon and 4.879% on Squirrel.
2. Conservative storage reduction is 7.49× and 7.60× using `4 + 32 f_escape + 256/N` bits/value.
3. Raw and hybrid node-permutation errors are `2.22e-16`.
4. Codec-consistent ordered-codebook mismatched-shuffle mean ratios are 3.72× and 3.63×, with all individual ratios above 3.31× and no identity permutations.
5. Five-seed retrained hybrid balanced-accuracy loss versus raw is 0.083 pp on Chameleon and a 0.768 pp gain on Squirrel.
6. Fixed raw probes favor ordered over shuffled hybrid features by 9.57 pp and 9.08 pp.

## Baselines and methods

| Method | Role | Chameleon error | Squirrel error | Storage |
|---|---|---:|---:|---:|
| Raw float | task/representation reference | 0 | 0 | 1× |
| Uniform 8-level | simple quantizer | reported in raw rows | reported in raw rows | ~7.5× |
| Per-channel Lloyd | codebook-only baseline | reported in raw rows | reported in raw rows | ~7.6× |
| Hybrid Lloyd+escape | proposed | 3.95% | 4.88% | 7.49×/7.60× |

## Controls and statistics

- Five split/probe seeds (600-604) with paired raw/hybrid results and sample dispersion.
- Five node-permutation seeds per graph.
- Five non-identity hop-shuffle seeds per graph with identical ordered-codebook and escape-rate policies.
- Fixed raw probes reuse train-fitted weights, intercepts, splits and test nodes across ordered/shuffled rows.
- Full raw tables preserve every method, seed, escape threshold/fraction, bits and metric.

## Negative evidence

- The first task run trained probes on all labels and produced implausibly high accuracy. It is preserved in `corrections/pos-task-leaky-probe-v1.json` and excluded.
- The first shuffle control mixed hybrid ordered error with Lloyd-only shuffled error and included one identity permutation. Representation rows were regenerated with codec-consistent escapes and non-identity permutations.
- The prior single-split v1 run lacked the accepted permutation/shuffle evidence and is background only.

## Limitations

- Two graphs and five probe seeds support a controlled study, not broad graph-transformer generality.
- The method does not evaluate a real graph-transformer→SNN system, temporal spikes, energy or hardware.
- Fixed-probe shuffle gaps are descriptive evidence of order sensitivity, not a causal model of positional reasoning.
- The conservative bit ledger excludes deployment runtime metadata beyond the stated symbol/payload/codebook costs.

## Planned figures and tables

- Figure 1: hop construction and hybrid escape coding.
- Figure 2: method error/storage/retrained accuracy.
- Figure 3: permutation and ordered/shuffled controls.
- Table 1: exact bit ledger and method definitions.
- Table 2: complete five-seed task and control results.
