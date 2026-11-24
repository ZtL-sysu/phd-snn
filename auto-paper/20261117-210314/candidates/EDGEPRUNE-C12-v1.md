# EDGEPRUNE-C12-v1 — operator-aware edge-event pruning

Hypothesis: retaining the strongest normalized edge events preserves graph conversion logits at fixed node events while reducing graph traversal slots.

Smoke: Chameleon and Squirrel normalized adjacency, keep top 60% nonzero edge weights, frozen GCN weights. Gate: retain ≤60% edges, downstream message relative error ≤15% on both datasets, and deterministic edge mask.

Novelty boundary: generic graph sparsification is mature; the contribution is conversion-time edge-event pruning with a frozen-teacher fidelity certificate.
