# SIGN-C04-v1 — signed excitatory/inhibitory message split

Hypothesis: split signed graph messages into nonnegative positive/negative event banks so heterophilic inhibitory evidence is not erased by ReLU/rate coding.

Smoke: 5,201×16 Squirrel preactivation messages from a frozen local GCN checkpoint. Gate: exact reconstruction ≤1e-12 and negative-message fraction ≥20%.

Result: PASS — exact reconstruction 0.0; negative fraction 34.73%; 54,316 positive and 28,900 negative event slots.

Novelty boundary: negative-spike ANN→SNN conversion exists (IJCAI 2025); the defensible gap is signed graph-message conversion with heterophily-stratified validation, not signed spikes in general.
