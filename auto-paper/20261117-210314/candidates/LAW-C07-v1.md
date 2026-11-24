# LAW-C07-v1 — topology-conditioned conversion failure law

Hypothesis: frozen GNN→SNN low-T fidelity loss is predicted by graph topology (homophily, degree entropy, normalized spectral radius) rather than only activation scale. This is an empirical mechanism/benchmark contribution, not a claim that one scalar threshold is novel.

Smoke: six local graph datasets (Cora, Citeseer, PubMed, Chameleon, Squirrel, OGBN-Arxiv) with fixed public masks and frozen 2-layer hidden-16 checkpoints. Compare teacher accuracy and T=2/4 conversion accuracy on validation only.

Gate frozen before execution: at least two topology statistics have |Spearman ρ|≥0.60 with conversion gap across ≥5 datasets, with the same sign at T=2 and T=4; otherwise reject.

Novelty boundary: SGNNBench lacks a conversion arm and the agent literature screen found no verified topology-conditioned conversion law. A positive smoke still needs a broader graph suite and direct conversion baselines.
