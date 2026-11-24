# P2 gate report

## Decision

**PASS.** The corrected certificate core was developed test-first and the local setup is reproducible.

## Checks

- RED: six named unit tests failed before implementation because `cert_core` was absent; preserved in `p2-tdd-red.log`.
- GREEN: `research/cert_core.py` implements the exact v5 quantizer, reduced bounds and synthetic chain.
- Tests cover constant-channel identity, upward tie rounding, hand-computed bounds, global-uniform equality, per-channel tightening and float64 containment.
- Final local test run passes 6/6 with return code 0 in `p2-tests.log`.
- `config.arc.yaml`, `protocols/arc-stage-map.md` and `protocols/experiment-protocol.md` freeze runtime and evidence policy.
- No remote execution, labels, actual-error tuning or credential material is used.
