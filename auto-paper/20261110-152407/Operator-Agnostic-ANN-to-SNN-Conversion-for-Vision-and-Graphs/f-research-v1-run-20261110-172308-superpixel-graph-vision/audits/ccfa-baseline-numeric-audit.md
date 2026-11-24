# P3A · Baseline Numeric Audit

Mode: `ccf-integrity-auditor` numeric-audit semantics; `review_execution: same-agent-role-pass`.

Checked against `results/local_full/result.json`, `results/local_full_v2/result.json`, `results/paired_analysis.json`, `results/e17/confirmation.json`, `results/e18/confirmation.json`:

- Units: all accuracies in percent; conversion loss in percentage points; energy ratios dimensionless (45 nm theoretical arithmetic energy, NOT hardware joules).
- Metric direction: conversion loss lower is better; energy ratio higher is better; teacher accuracy higher is better.
- Splits: official SuperPixel MNIST/CIFAR10 splits; holdout groups seeds 0-4, 5-9, 10-14, 15-19 are mutually disjoint; each test evaluated once.
- Seeds: 5 frozen seeds per group; CUDA sparse reduction nondeterminism handled by reporting mean, std and 95% CI, never a single best seed.
- Zero-spike and degenerate-teacher guards active (`zero_spike_degenerate`, teacher >= 20%).
- Baseline landscape supports the mechanism: all single-point conversion baselines stay near chance while our method leads by 43.67pp (MNIST, T=4) and 19.85pp (CIFAR10, T=4).
- No numeric inconsistency found. P3A pass.
