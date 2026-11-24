# Claim-evidence matrix

| Claim component | Required evidence | Comparator | Falsifier | Status |
|---|---|---|---|---|
| Deterministic validity of the output-column envelope | 36-cell actual-error containment audit with float64 bounds | Euclidean and global scalar bounds | Any actual error above the bound | pending |
| Operator-aware tightness | width/RMS and tightening for `abs(A) @ Delta @ abs(W2)` | global scalar L1 bound | median width/RMS >10, any cell >15, or minimum tightening <25% | pending |
| Quantizer generality within scope | global-uniform and per-channel-uniform rounding half-steps | same bound families | a valid quantizer produces an invalid envelope | pending |
| Scope stability | three graphs and three frozen checkpoint seeds | per-cell dispersion | result exists only for one graph or seed | pending |
| Interpretation boundary | derivation plus limitation audit | prior v1 rows | claim expanded to multilayer/nonlinear/temporal/energy without evidence | locked |
