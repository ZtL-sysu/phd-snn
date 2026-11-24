# Candidate A stage-1 data blocker

- A directly MIT-labeled NTU-60 CSV mirror was downloaded and inspected: `data/ntu60_points.csv` (51,018,604 bytes).
- The file stores NumPy-style arrays with literal `...` truncation. It is not a complete skeleton tensor; only one sampled sequence could be parsed into a [T,V,2] array, so it cannot support model-level sparse-delta calibration.
- The descriptive census on that single usable sequence produced inactive fractions of 0.026 at thresholds 0.5-5 pixels and 0.205 at 10 pixels, far below the pre-registered 0.80 gate.
- MMAction2 provides an official ST-GCN checkpoint but still requires the separately licensed NTU RGB+D raw skeleton archive, which is not in the run root.
- Decision: Candidate A's stage-1 gate is not passed. Keep the negative evidence; do not start a full paper on A.
