# Paper guidance audit

| Guidance requirement | Status | Evidence / paper location |
|---|---|---|
| Canonical six sections | covered | Sections 1-6 are present and ordered. |
| Datasets and fixed splits | covered | Cora/Chameleon/Squirrel, fixed masks, seeds 0/1/2, validation/test chronology. |
| Baselines | covered | Full-float, SVD-only, random projection validation diagnostic, top-absolute, random, uniform, A2Q-style and One-Spike-style controls are named; random projection is explicitly scoped to the validation grid. |
| LR-A main logit gate | covered | 26.23/33.99/25.83% reductions and 9/9 paired direction. |
| LR-B task trade-off | covered | 0.53/1.17/1.86 pp three-seed maxima and 2.85 pp seed-level maximum. |
| LR-C exact ledger | covered | Formula, 2% denominator, coefficient counts, absolute bit totals, and matched scope. |
| LR-D warmed cost | covered-with-scope | 1.020-1.124x p95 and 218.23 MB at rank128/1%; focal 2% timing remains explicitly outside the claim. |
| LR-E adapted prior art | covered | A2Q-style and One-Spike-style matched-budget adaptations and numeric comparisons. |
| Metrics | covered | Message, hidden, logit MSE; T=2/4 accuracy; teacher agreement; bits; coefficients; latency/memory. |
| Statistics | covered | n=3, sample SD, paired descriptive comparisons, no formal CI/equivalence claim. |
| Figures | covered | Figure 1 architecture and Figures 2-4 evidence/robustness panels inserted. |
| Tables | covered-after-repair | Tables 1-3 added from frozen source evidence. |
| Citation scope | covered | 41 verified unique references; 30 from 2022-2026; duplicate audit passed. |
| Language/output constraints | covered | English manuscript, one final PDF, complete TeX/BibTeX/figures, no commit/push. |
| Negative findings | covered | Task-superiority failure, mixed task deltas, message-MSE trade-off, and scope limits retained. |

## Judgment

The guidance coverage is complete after adding the random-projection validation diagnostic, message-MSE/coefficient-count evidence, and Tables 1-3. The focal claim remains deliberately narrow: logit-fidelity coding of M0=A_hat X under matched total padded serialized-bit cost. The rank128/1% timing result is not generalized to the focal 2% setting.
