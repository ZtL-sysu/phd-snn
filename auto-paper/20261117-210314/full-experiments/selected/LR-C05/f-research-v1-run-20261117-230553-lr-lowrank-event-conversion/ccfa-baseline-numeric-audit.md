# P3A baseline numeric audit

- Row counts, datasets, seeds, ranks and budgets match the frozen guidance.
- Accuracy/agreement are higher-is-better; message/hidden errors and storage bits are separately labeled.
- The equal-budget comparator is uniform residual. Random is a matched allocation control.
- CPU reference graph aggregation is explicitly separated from CUDA SVD/reconstruction.

Severity: no numeric inconsistency. No-invention status: **pass**.
