# P3 baseline-first gate

- `results/baseline.json` contains 333 rows: 3 graphs×3 checkpoint seeds×4 ranks×3 residual budgets for SVD-only/random/uniform controls, plus rank-128 reference rows.
- Execution device: NVIDIA GeForce RTX 3060. All output JSON is finite.
- At rank128/fraction 0.01, uniform residual is the strongest common baseline: T2/T4 agreement is Cora 84.93/90.73%, Chameleon 64.24/74.85%, Squirrel 51.16/73.94% averaged over seeds.
- Random and uniform residual use identical explicit storage accounting; SVD-only uses less storage and is not treated as an equal-budget win target.

Verdict: **pass**. Proposed downstream residual allocation must be compared against uniform residual, not only random.
