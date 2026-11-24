# P3 baseline gate

- 1,089 baseline rows completed on RTX3060 with full-float, SVD/random bases and top-absolute/random/A2Q-style/uniform/One-Spike-style controls.
- Exact total padded bits are recorded per row. At rank128/1% the SVD top-absolute and A2Q-style controls are strongest; uniform and One-Spike are weaker.
- Full-float references and hidden/logit MSE are present, resolving the v1 metric gap.

Verdict: **pass**. Proposed downstream sensitivity must beat the strongest of top-absolute and A2Q-style at equal bits.
