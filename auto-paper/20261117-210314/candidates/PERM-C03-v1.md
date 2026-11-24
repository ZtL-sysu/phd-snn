# PERM-C03-v1 — permutation-equivariant message-pool conversion

Hypothesis: graph readout/message pooling should commute exactly with node permutations after event quantization, providing a correctness certificate for graph conversion.

Smoke: 2,277-node/65,019-nonzero Chameleon graph with a fixed random permutation. Gate: max equivariance error ≤1e-10.

Result: PASS — max error 0.0.

Novelty boundary: generic graph equivariance is standard; contribution is a conversion-level certificate and a test that catches order-dependent spike scheduling. Full attention/edge-bias conversion remains untested.
