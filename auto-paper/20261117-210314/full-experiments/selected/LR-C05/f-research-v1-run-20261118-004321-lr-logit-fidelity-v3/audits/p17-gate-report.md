# P17 gate report

## Decision

**PASS after evidence-preserving coverage repair.**

The audited final source is `writing/p17/paper-guidance-complete.md`.

## Coverage repairs

- Added the random-projection validation-grid diagnostic and its scope boundary.
- Added message-MSE results, including the negative message-MSE trade-off.
- Added selected-coefficient counts and complete serialized-cost totals.
- Added Table 1 for fidelity decomposition and observed task maxima.
- Added Table 2 for A2Q-style and One-Spike-style matched-budget adapted controls.
- Added Table 3 for the exact basis/residual/total/full-float bit ledger.

## Coverage result

- Six canonical sections: covered.
- Datasets, splits, seeds and validation/test chronology: covered.
- Full-float, SVD-only, random-projection diagnostic, top-absolute, random, uniform, A2Q-style and One-Spike-style baselines: covered.
- LR-A to LR-E evidence: covered; LR-D remains explicitly scoped to rank128/1% warmed timing.
- Message, hidden and logit MSE, accuracy, teacher agreement, exact bits, coefficient counts, latency and memory: covered.
- Four figures and three evidence tables: covered.
- 41 unique verified references and duplicate audit: covered.
- Negative findings and limitations: covered.
- English manuscript, one-PDF policy, TeX/BibTeX/figures and no-push constraints: covered.

The repair adds only evidence already present in frozen source artifacts. It does not add new experiments or strengthen the claim beyond logit-fidelity coding of `M0=A_hat X`.
