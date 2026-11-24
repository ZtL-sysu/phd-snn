# Correction: low-rank message scope and GPU decomposition

- Trigger: P3 baseline LR used 16-dimensional hidden preactivations, making rank 128 overcomplete and the compression gate ill-posed.
- Earliest affected stage: P2 experiment implementation.
- Repair: use raw aggregated graph messages `A X` as in the accepted smoke contract, predict the first hidden preactivation, and run SVD/random projection on the RTX 3060 via PyTorch.
- Preserved evidence: LR's old result is invalid for the binding rank/compression claim; unaffected baseline modules remain reusable after hash checks.
- Falsifier: rank-128 compression must be computed as raw matrix elements divided by `rank*(N+F)`; no hidden 16-channel matrix may substitute.
