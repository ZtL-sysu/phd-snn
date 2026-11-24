# HOM-C17-v1 — homophily-conditioned timestep-gain law

Hypothesis: low-T conversion benefits from added steps much more on homophilous graphs than on heterophilous graphs because averaged same-label messages tolerate temporal residual noise differently.

Screening history: LAW-C07's six-dataset scalar correlation failed, and NM-C16's strict mixed-sign criterion failed. This candidate is a different grouped mechanism, not a relabeling of those passes.

Confirmation frozen before execution: held-out seeds 4–6. High-homophily group = Cora/Citeseer/PubMed; low-homophily group = Chameleon/Squirrel; OGBN-Arxiv is excluded from group means. Gate: `(mean T4−T2 high) − (mean T4−T2 low) ≥5 pp` in at least two of three held-out seeds.

Novelty boundary: no verified homophily-conditioned frozen GNN→SNN conversion law was found; this smoke supports an empirical mechanism only.
