# Experiment traceability

Started before accepting baseline output; the process was launched and then this ledger was synchronized during execution. No output has yet been accepted.

| Guidance row | Planned run | Strong expected result | Status | Evidence |
|---|---|---|---|---|
| LR-A | baseline/method grids: 3 graphs×3 seeds×4 ranks×3 budgets | hidden/logit MSE ≥20% better on ≥2/3 and compression ≥8× | running | `results/baseline.json`, `results/method.json` |
| LR-B | T2/T4 from every reconstruction | ≥1 pp agreement on ≥2/3 | running | same |
| LR-C | exact payload/padded bits | same bits ±1%; Pareto gain | running | row-level cost fields |
| LR-D | timing phase, 3 warm + 7 measured | p95 ≤1.2× at matched fidelity | planned | `results/timing.json` |
| LR-E | A2Q-style and One-Spike-style adaptations | proposed beats both on ≥2/3 or novelty narrowed | running | baseline grid |
