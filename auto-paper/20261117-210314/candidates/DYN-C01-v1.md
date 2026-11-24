# DYN-C01-v1 — causal residual events for temporal graph rollouts

Hypothesis: for a temporal graph state sequence, encode changes rather than absolute states; a causal residual prefix has no future leakage and reduces nonzero event work while preserving reconstruction.

Smoke: 728 real DAVIS-2017 processed 8-frame motion clips, split-independent mechanism property. Gate: exact reconstruction ≤1e-12, future-change prefix error ≤1e-12, and nonzero residual reduction ≥20%.

Result: PASS — reconstruction and future-prefix errors 0.0; residual/nonzero ratio 0.7948, reduction 20.52%.

Novelty boundary: ASGCN occupies event-graph conversion and temporal SNNs are direct-trained; this candidate is specifically causal residual conversion for graph rollouts. Need a real temporal-GNN benchmark before a paper claim.
