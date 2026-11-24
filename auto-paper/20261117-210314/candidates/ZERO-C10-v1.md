# ZERO-C10-v1 — exact zero-message node pruning during conversion

Hypothesis: if a node emits no hidden spikes across the causal conversion prefix, its outgoing message is exactly zero and can be omitted from graph scatter/linear work without changing logits. This is a structural sparsification proof, not a learned pruning heuristic.

Smoke: frozen Chameleon and Squirrel 2-layer GCN checkpoints, T=2, validation masks. Gate: at least 10% of nodes have all-zero hidden spike rows; pruned and unpruned logits agree to ≤1e-10; counted message slots fall by the same zero-node fraction.

Novelty boundary: sparse/event-driven graph conversion is adjacent to One-Spike/ASGCN, but exact zero-row certificate and graph-scatter cost accounting are distinct. Hardware energy is not claimed.
