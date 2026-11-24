# NM-C16-v1 — non-monotonic low-timestep graph-conversion law

Hypothesis: increasing conversion steps does not monotonically improve graph accuracy because per-layer residual errors can cancel or reverse at T=2 versus T=4. The contribution would be a graph-specific failure law plus a signed-prefix correction motivated by it.

Discovery evidence: seed-0 local checkpoint screen suggested large T4 gains on Cora/Citeseer/PubMed but a T4 loss on Chameleon. This idea is not counted from that exploratory row.

Confirmation smoke frozen before execution: seeds 1–3, six local datasets, validation masks only. Gate: at least two of three seeds show T4−T2 ≥1 pp on at least three datasets and T4−T2 ≤−0.5 pp on at least one dataset.

Novelty boundary: TPP owns temporal misalignment in CNN conversion; no verified graph-conversion non-monotonic law was found. A pass remains a smoke-level empirical pattern, not a universal theorem.
