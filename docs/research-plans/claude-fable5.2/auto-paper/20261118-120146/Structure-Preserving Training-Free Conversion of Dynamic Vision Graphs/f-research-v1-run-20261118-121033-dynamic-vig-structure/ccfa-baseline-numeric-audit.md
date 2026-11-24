# CCFA baseline numeric audit

- Source: `baseline-structure-results.json`.
- Dataset: Fashion-MNIST train subset, 240 samples; no official test exposure.
- Seeds: 41, 42, 43; all rows retained.
- Metric direction: higher is better; teacher reference is 1.0 for both Jaccard and winner agreement.
- Signed uniform baseline mean Jaccard = 0.6476, mean winner agreement = 0.2251.
- Corresponding teacher-relative losses = 35.24 pp Jaccard and 77.49 pp winner agreement, both above the pre-registered C1 thresholds of 5 pp and 2 pp.
- Unsigned uniform is weaker (Jaccard 0.3544; winner agreement 0.1524), as expected.
- Signed multilevel current implementation is weaker (Jaccard 0.4642; winner agreement 0.1102), identifying an implementation/calibration gap rather than a reason to lower the target.
- Units, split, seeds, metric direction, and source file are consistent. No task accuracy claim is made from these rows.

Gate: numeric audit pass for structure metrics only.
