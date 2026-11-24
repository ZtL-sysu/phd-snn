# P5 strong-result lock report

- Required C1 structure-loss threshold: met on frozen test (Jaccard loss 93.8 pp and winner-agreement loss 37.0 pp for signed uniform; both far above minimums).
- Required C2: failed. Calibrated converted accuracy mean 50.23% versus teacher 83.60%; teacher gap 33.37 pp, far above the <=1 pp strong requirement.
- Required C3: failed in its intended interpretation. Both-oracle and neighbor-oracle recover to teacher, but method-level structure calibration does not recover half the oracle gain; the causal gap is continuous message fidelity, not discrete index choice alone.
- Decision: strong-result lock failed. No paper drafting is permitted.
- Correction: open cycle 1 and create a versioned replacement contract; do not lower the failed thresholds.
