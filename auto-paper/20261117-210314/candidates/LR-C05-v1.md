# LR-C05-v1 — operator-conditioned low-rank message events

Hypothesis: graph messages can be transmitted in an operator-aligned low-rank subspace at large compression, with a quantized residual event stream for the omitted component.

Smoke: 2,277×2,325 Chameleon graph messages, rank 128. Gate: relative reconstruction error ≤50% and compressed dimension/input dimension ≤1/8.

Result: PASS — relative error 45.57%; 589,056 compressed dimensions vs 5,294,025 input dimensions (8.99× reduction).

Novelty boundary: graph quantization and low-rank compression are established; the contribution must be conversion-time operator alignment and a downstream fidelity/cost test.
