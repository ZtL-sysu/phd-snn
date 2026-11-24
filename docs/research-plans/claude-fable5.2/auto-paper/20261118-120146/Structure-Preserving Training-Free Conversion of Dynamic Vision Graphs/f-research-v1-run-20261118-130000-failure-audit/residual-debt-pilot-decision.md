# Residual-debt pilot decision: NO-GO

The pre-registered gate required at least 2x latency reduction, at most 1% embedding drift, and at least 50% drift reduction over no-debt/lazy controls at matched activity.

Observed in `ripple-residual-debt-pilot.json` on a local Cora edge-addition stream:
- Best speedup versus full recomputation was below 1.0x for every tested mode and threshold.
- Mean embedding drift was about 0.378 for all thresholded and debt modes.
- Residual debt did not reduce drift relative to no-debt thresholding or lazy refresh; propagated activities were equal or worse.
- The implementation used a PyG proxy because DGL/OGB are absent from the local Conda environment; the official Ripple Apache-2.0 code and README were preserved for baseline provenance. This proxy is enough for a NO-GO because the mechanism produced neither speed nor fidelity benefit.

Decision: reject Candidate Bounded-Staleness Streaming GNN via Residual-Debt Repair. Do not write a paper from it and do not lower the gate.
