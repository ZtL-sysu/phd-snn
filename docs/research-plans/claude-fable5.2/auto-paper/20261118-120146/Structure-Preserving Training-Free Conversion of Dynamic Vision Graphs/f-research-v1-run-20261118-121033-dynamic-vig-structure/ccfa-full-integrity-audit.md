# CCFA full integrity audit — v2 accepted evidence

- Scope: `v2-message-calibration-results.json`, `v2-ablation-results.json`, teacher checkpoints, frozen Fashion-MNIST test.
- All three teacher seeds (41/42/43) are reported; no seed is omitted or renamed.
- Teacher mean accuracy = 0.8360; v1 mean = 0.5023; v2 mean = 0.7883.
- Mean teacher gap: v1 = 33.37 pp; v2 = 4.77 pp; gap closure = 85.35%.
- Per-seed closure: 86.12%, 80.62%, 89.32%; all exceed the 50% strong threshold.
- Message MSE: v1 mean = 0.007922; v2 mean = 0.001411; reduction = 82.19%.
- Event count is exactly 6,272,000 in v1, v2, and both ablations; the matched-event condition holds.
- Ablation means: scale-only 0.5023, offset-only 0.3885, message-full 0.7883. Message-full is best for every seed.
- The source code computed message MSE on detached teacher features inside the v2 main run; one temporary ablation script retained a benign autograd conversion warning but wrote identical scalar values. No claim depends on gradients.
- Calibration data: first 5,000 Fashion-MNIST train examples; test used only after calibration parameters were frozen.
- Limit: implementation-level derivation of the spatial message uses the trained model's `message` linear layer and max readout; no claim is made about all ViG architectures or hardware energy.
- Verdict: numeric/claim consistency pass for the v2 strong-result lock.
