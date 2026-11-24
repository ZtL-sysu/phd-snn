# Experiment completion lock

| Guidance experiment | Required evidence | Strong expected result | Actual result | Status | Blocking issue |
|---|---|---|---|---|---|
| DYN-C01 | 5-seed DAVIS, raw/residual/causal | decoded ≤1 pp loss and ≥15% reduction on ≥4/5 | exact decoded equality; 20.52% reduction | strong-pass | none |
| EQ-C02 | 5 coordinate splits/rotations | exact equivariance, ≤10% error, accuracy non-inferior, ≥1 pp control gain | 2.91e-11 error, 3.78% quantization, +1.50 pp vs component | strong-pass | none |
| PERM-C03 | 3 graphs×5 permutations | deterministic exact and naive fails | 1.11e-16 vs 0.50–0.95 | strong-pass | none |
| SIGN-C04 | 3 graphs, signed controls | ≥2 pp on heterophily | +0.46/+0.48 pp | **strong-fail** | success claim prohibited |
| LR-C05 | rank curves/SVD/random | ≥8× on 2/3 and ≥20% MSE reduction | 8.99/11.64× and 3.79–6.20× lower error | strong-pass | none |
| EDGE-C06 | equal-bit quantizers | ≥4×, ≤20%, ≥10% better | 5.33×, 2.82%, 83.2% better | strong-pass | none |
| CERT-C11 | coverage/tightness | 100%, width≤10, ≥25% tighter | 100%, 3.06–6.72, ≥79.7% | strong-pass | none |
| POS-C13 | hop codebooks | ≤5%, ≤2 pp loss, ≥4× | 2.46/3.06%, positive accuracy, 10.17× | strong-pass | none |
| DLY-C14 | 5-seed delay schedules | causal, ≤1 pp, ≥10% on ≥4/5 | exact decoded, 20.52% | strong-pass | none |
| READ-C18 | 6 graphs×3 seeds | top2 exact, ≥50% slots | 100%, 63.33% | strong-pass | none |

## Handoff decision

- All required experiments complete: **yes**.
- Strong expected results met for the portfolio's evidence-audit claim: **yes**; nine method strong-pass, one explicit strong-fail.
- Strongest feasible baseline/control complete: **yes**.
- Raw logs/configs/seeds/metrics/environment available: **yes**.
- Decision: **allow final Markdown report and independent CCFA review**, with SIGN's downstream-benefit claim removed.
