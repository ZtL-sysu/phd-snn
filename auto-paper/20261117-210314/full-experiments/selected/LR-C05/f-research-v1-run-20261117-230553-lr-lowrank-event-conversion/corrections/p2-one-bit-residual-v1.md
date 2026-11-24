# Correction: one-bit residual quantizer

- Trigger: P3 baseline start produced division-by-zero warnings because the signed one-bit quantizer had zero levels.
- Repair: support one-bit sign quantization and zero residual matrices; add a failing-first finite-output test. No target or budget changed.
- Evidence: invalid run was stopped before acceptance and no result file was accepted; 8/8 tests pass after repair.
