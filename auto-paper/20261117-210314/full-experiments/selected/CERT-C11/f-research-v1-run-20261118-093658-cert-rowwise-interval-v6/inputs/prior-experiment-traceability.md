# Experiment traceability

The table maps every mandatory guidance row to final raw evidence. Commands are frozen in `protocols/experiment-commands.md`; split IDs and fit histories are embedded in result JSON. The final manifest hash-binds the accepted outputs. Earlier failed/superseded rounds are retained in `corrections/` and are not used as final results.

| ID | Required evidence | Final result | Strong gate | File |
|---|---|---|---|---|
| DYN-C01 | 5 DAVIS seeds, raw vs initial+residual, causal/future control | decoded accuracy identical; repeated-event reduction 20.52%; direct probe unstable | pass | `results/methods-DYN-C01.json` |
| EQ-C02 | 5 coordinate splits, raw/component/radial, rotations | rotation max 2.91e-11; radial error 3.78%; mean accuracy +1.64 pp raw and +1.50 pp component | pass | `results/methods-EQ-C02.json` |
| PERM-C03 | 3 graphs×5 permutations, deterministic/naive | deterministic max 1.11e-16; naive 0.50–0.95 | pass | `results/methods-PERM-C03.json` |
| SIGN-C04 | 3 graphs, signed/abs/positive | heterophilic gains +0.46/+0.48 pp only | **fail strong** | `results/methods-SIGN-C04.json` |
| LR-C05 | ranks 8–128, SVD/random | rank128 compression 7.32/8.99/11.64×; SVD logit error 3.79–6.20× lower | pass | `results/methods-LR-C05.json` |
| EDGE-C06 | 2–6 bits, uniform/log/quantile | 6-bit log error 2.82%, storage 5.33×, 83.2% lower error than uniform | pass | `results/methods-EDGE-C06.json` |
| CERT-C11 | 3 graphs×2 levels, proposed/global | 100% coverage; width/RMS 3.06–6.72; 79.7–85.1% tightening | pass | `results/methods-CERT-C11.json` |
| POS-C13 | 2 graphs, raw/uniform/per-channel/hybrid | hybrid error 2.46/3.06%, storage 10.17×, balanced accuracy +2.13/+2.20 pp | pass | `results/methods-POS-C13.json` |
| DLY-C14 | 5 DAVIS seeds, delay schedule and wrong-delay control | correct delay exact; wrong-delay error 4.04%; repeated-event reduction 20.52% | pass | `results/methods-DLY-C14.json` |
| READ-C18 | 6 graphs×3 seeds, full/top2/top1 and margins | top2 preservation 100%; median slot reduction 63.33% | pass | `results/methods-READ-C18.json` |

## Execution note

All final GPU probes use the RTX 3060. The immutable local `core.convert` reference is CPU-compatible for historical comparability; this is recorded rather than mislabeled as GPU energy measurement.
