# Strong-result feasibility contract — idea-screen portfolio

This contract binds the smoke claims, not future paper headline gains.

| ID | Claim | Assumptions | Falsifier | Evidence | Stop condition |
|---|---|---|---|---|---|
| DYN-C01 | causal residuals preserve prefixes and reduce repeated events | fixed-length real sequences; lossless residual decoding | future leakage or <20% event reduction | `../smoke/results/mechanism-smoke.json` | fail → no temporal claim |
| EQ-C02 | radial events commute with rotations with bounded error | Euclidean coordinates; shared radial scale | equivariance error > tolerance or error >10% | same | fail → redesign encoder |
| PERM-C03 | message pooling commutes with node permutations | deterministic scatter/reduction | order-dependent output | same | fail → remove certificate claim |
| SIGN-C04 | signed split exactly preserves inhibitory messages | signed preactivations available | reconstruction error or <20% negative mass | same | fail → restrict to nonnegative graphs |
| LR-C05 | rank-128 messages compress ≥8× with <50% residual error | stable local message matrix | compression/error gate fails | same | fail → increase rank or reject |
| EDGE-C06 | 6-bit edge alphabet gives ≥4× storage at <25% error | bounded edge-weight range | error/storage gate fails | same | fail → no weighted-message claim |
| CERT-C11 | affine envelope covers all measured errors with width ≤10× RMS | componentwise error bound | any uncovered error or loose width | `../smoke/results/more-mechanisms.json` | fail → no certificate |
| POS-C13 | hop events retain positional information and equivariance | normalized fixed graph operator | permutation/quantization/storage gate fails | same | fail → no positional claim |
| DLY-C14 | delay-aligned residuals are causal and sparse | known propagation delay | leakage or <10% event reduction | same | fail → remove delay claim |
| READ-C18 | top-two pair preserves argmax and reduces output slots | logits available; classes ≥2 | any prediction change or median reduction <50% | `../smoke/results/READ-C18-v1.json` | fail → no readout compression |

All full-paper targets must be recalibrated against direct reruns; no arbitrary accuracy/energy gain is authorized.
