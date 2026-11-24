# G7 — Effectiveness and strong-result feasibility

## Baseline calibration

- No new observed result is claimed here. The binding thresholds in the feasibility contract are pre-registered from the discrete-decision mechanism and the imported literature evidence that max-pooling replacement severely damages point-cloud teachers.
- Local exposed-test metadata shows a large gap between plain (about 0.55 CIFAR10) and gated (0.684-0.692 CIFAR10) local teachers, demonstrating that architecture and operator choices can materially change accuracy. It does not establish the proposed method's gain and is not used as unseen-test evidence.
- The binding strong path requires the proposed conversion baseline itself to show >=5 pp neighbor-Jaccard loss or >=2 pp winner-agreement loss at T<=4. If that pilot condition fails, the method idea is falsified and the scenario returns to the rescue route.

## Prototype milestone

- Implement one Grapher block with exact teacher kNN/max and signed multi-threshold coding.
- Run 64 samples with finite-value, shape, and exact-oracle equivalence assertions.
- Measure structure disagreement before any method tuning.
- Only if the pilot passes does the run enter the full three-seed campaign.

## Compute budget

- Local RTX 3060 12 GB, 12 CPUs, ~481 GiB free disk.
- Fashion-MNIST/MNIST patch-grid teachers and conversions fit comfortably within 8 GB and 24 hours total for the declared seed/search budget.
- Existing 4.38 GB superpixel graph datasets and teacher metadata are available for diagnostics without download.

## Strong-result rule

- Do not lower `expected_strong` after a failed attempt.
- Improve implementation, calibration, architecture, or evidence within the same method family, or activate a versioned replacement contract from the material set.
- A gap that depends only on a historically exposed test cannot count as strong evidence.

Gate verdict: `pass` as a bounded pre-registration. The strong result is mechanism-supported and falsifiable, but it remains unobserved until f-research-v1 experiments.
