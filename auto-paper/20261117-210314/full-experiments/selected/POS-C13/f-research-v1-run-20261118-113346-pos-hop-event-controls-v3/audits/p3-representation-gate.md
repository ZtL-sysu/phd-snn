# P3 baseline-first representation gate

## Decision

**PASS.** Raw/uniform/Lloyd/hybrid representations and all representation controls were evaluated before multi-seed probe experiments.

## Results

- Hybrid Chameleon: relative error 3.952%, conservative storage 7.490×.
- Hybrid Squirrel: relative error 4.879%, conservative storage 7.602×.
- Raw and hybrid permutation maximum errors are `2.22e-16`, below `1e-10`.
- Codec-consistent ordered-codebook mismatched-shuffle mean error ratios are 3.72× on Chameleon and 3.63× on Squirrel; every individual shuffle seed is above 3.31× and no identity permutation remains.
- Top-k escape tie instability and ordered/shuffled codec mismatch found in earlier runs were repaired; regression tests pass.

Raw outputs: `results/pos-representation.json`, `results/pos-representation.csv`, `results/pos-representation-summary.json`.
