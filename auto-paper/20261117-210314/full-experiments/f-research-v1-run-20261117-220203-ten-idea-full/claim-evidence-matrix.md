# Claim–evidence matrix

All entries are planned evidence at P1A, not observed findings.

| ID | Main claim | Mechanism | Falsifying ablation | Simple baseline | Strong/matched baseline | Primary evidence |
|---|---|---|---|---|---|---|
| DYN-C01 | causal residual coding preserves task accuracy while reducing repeated events | state differences with lossless prefix | shuffled/future residual | absolute frames | delay-0 residual | DAVIS 5-seed paired accuracy/event table |
| EQ-C02 | radial events preserve rotation equivariance with bounded coordinate error | magnitude quantization + direction | component quantization and shuffled direction | raw coordinates | component-uniform | typed-coordinate classification and rotation sweep |
| PERM-C03 | deterministic graph event pooling is permutation certified | commutative scatter/reduction | naive row order | naive pooling | exact scatter | 3 graphs×5 permutations |
| SIGN-C04 | signed message banks preserve inhibitory graph evidence | positive/negative exact split | sign shuffle | positive-only | absolute-value | heterophilic message classification |
| LR-C05 | SVD-aligned rank-128 events beat random rank-128 | operator-aligned subspace | random projection | rank-8/16/32 | random equal rank | logit MSE/compression curves |
| EDGE-C06 | nonuniform edge alphabets improve weighted-message fidelity | log/quantile quantization | shuffled weights | uniform alphabet | float32 | FlyWire error/aggregate curves |
| CERT-C11 | affine graph-aggregation envelope is valid and tighter | componentwise propagation | global norm bound | no certificate | Frobenius/global | coverage and tightness sweep |
| POS-C13 | hop-position events preserve positional information | multihop concatenation + quantization | shuffled hops | raw hops | per-channel/uniform | classification and permutation error |
| DLY-C14 | delay-aligned residuals preserve causal accuracy and reduce events | propagation-delay schedule | wrong delay/future leak | absolute frames | delay-0 residual | DAVIS 5-seed paired schedule table |
| READ-C18 | top-two pair readout preserves decisions at lower output cost | leader/runner-up signed margin | top1 and shuffled pair | full output | top1 | 6 graphs×3 seeds margin table |

## Resource and stop contract

- Code path: new `research/` modules import only read-only local data/checkpoints and the prior verified `core.convert`.
- Prototype milestone: deterministic unit tests plus one seed before the multi-seed matrix.
- Budget: ≤20 minutes/12 GiB per module, 5 seeds temporal/coordinate, graph seeds 0–2, zero remote compute.
- Search budget: fixed grids exactly as guidance; no post-result grid expansion.
- Stop/return: minimum miss closes the module as negative; strong miss narrows the claim and blocks strong wording; leakage/nonfinite/mismatched splits invalidates the run and returns to P2/P3 repair.
