# Strong-result lock

The corrected POS-C13 v3 method meets every binding gate:

- Hybrid representation error is 3.952% on Chameleon and 4.879% on Squirrel.
- Conservative serialization reduces storage by 7.49× and 7.60×.
- Raw and hybrid permutation errors are `2.22e-16` across all permutation seeds.
- Codec-consistent mismatched-shuffle mean ratios are 3.72× and 3.63×; every seed is non-identity and above 3.31×.
- Five-seed retrained hybrid balanced-accuracy loss versus raw is 0.083 pp on Chameleon and a 0.768 pp gain on Squirrel.
- Fixed raw probes favor ordered over shuffled hybrid representations by 9.57 pp and 9.08 pp.

The first task run with full-data probe fitting is preserved as negative evidence and excluded. The accepted task rows train only on split train indices.
