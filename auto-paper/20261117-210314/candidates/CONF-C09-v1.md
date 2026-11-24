# CONF-C09-v1 — conformal selective conversion

Hypothesis: converted-prefix uncertainty can support risk-controlled selective prediction. Unlike C09-v1's forced T2→T4 upgrades, this mechanism may abstain on uncertain graphs and provide an empirical risk bound at a chosen coverage.

Smoke: fixed-GCN full validation T1/T2/T4 archives for SuperPixel MNIST/CIFAR10. Use deterministic 512 dev/512 tune/512 internal-validation partitions; fit the uncertainty threshold on tune only. No test archives.

Gate frozen before execution: at least 30% validation coverage, selective error ≤5% on both datasets, and lower error than a random accept set at the same coverage in ≥95% of 2,000 random draws. Report calibration risk and coverage, not only accuracy.

Novelty boundary: SEENN/AdaFire occupy SNN confidence/early-exit conversion; SIGHT occupies spiking-graph uncertainty but is direct/hybrid. The narrow contribution is conformal risk control for frozen GNN→SNN conversion with graph-level held-out shifts.
