# P5A · Pre-Draft Integrity Audit

- planned vs reported: every number used for drafting comes from executed result files; no planned target is written as a finding.
- v2's 1.5pp target is preserved as a historical target; v3 reports measured 1.57pp (CIFAR10) and 3.79pp (MNIST) from E17 plus E18 2.27/7.29pp as a negative result.
- No cherry-picked seeds: all four holdout groups and all 20 seeds are reported.
- Both energy conventions reported together; zero-spike degenerate points excluded; degenerate-teacher points excluded.
- Negative results and implementation defects (zero-pulse false advantage, degenerate teacher, fp32/fp64 mixing) retained.
- Claim/result/table mappings consistent with `results/experiment-traceability.md`. P5A pass.
