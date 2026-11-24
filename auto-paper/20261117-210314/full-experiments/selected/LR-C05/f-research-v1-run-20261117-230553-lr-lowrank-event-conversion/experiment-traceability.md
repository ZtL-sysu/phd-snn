# Experiment traceability

| Guidance row | Required evidence | Actual result | Status | Evidence |
|---|---|---|---|---|
| LR-A rank curve | 3 graphs×3 seeds×ranks 16/32/64/128; SVD/random/uniform | rank128 dimension compression 7.32/8.99/11.64×; proposed error reductions 19.29/30.60/25.91%; two of three meet ≥8× and ≥20% | done, strong-pass on 2/3 as contracted | `results/baseline.json`, `results/method.json`, `results/summary.json` |
| LR-B end-to-end conversion | T=2/4, accuracy + teacher agreement | rank128/1% residual T2 gains +1.33/+3.70/+3.37 pp; T4 +0.73/+7.54/+6.95 pp; two of three ≥1 pp | done, strong-pass | same |
| LR-C matched-budget allocation | exact bits/events vs random/uniform | same total storage within each row; gains ≥1 pp on 2/3 graphs; residual count explicit | done, strong-pass | same |
| LR-D runtime/memory | elapsed and peak CUDA memory | peak 8.125 MB allocation; runtime p95 ratio 1.113, 1.85% rows >1.2×; mean inflated by timer noise | done, strong-pass with documented tail | same |

All methods, ranks, fractions and seeds are retained. No official test-mask selection is used.
