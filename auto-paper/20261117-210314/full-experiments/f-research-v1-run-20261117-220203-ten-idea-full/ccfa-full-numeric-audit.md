# Full numeric and claim audit

Mode: `ccf-integrity-auditor` full numeric/claim audit before independent review.

- `methods-manifest.json` hashes all ten final result files.
- `results/final-summary.json` values were recomputed from raw JSON; metric directions and denominators are explicit.
- DYN/DLY distinguish decoded task accuracy from direct representation-probe sensitivity. The direct probe is not used to claim failure of the lossless code.
- EQ/PERM certificate errors use float64 and meet frozen tolerance.
- POS bits are `0.995*3 + 0.005*32 = 3.145`, giving 10.17× reduction versus float32.
- SIGN is marked `strong-fail`; no success wording is permitted.
- No energy, universal dynamic-graph, or full E(3)-GNN claim is supported.

Severity: no unresolved numeric mismatch. Claim scope is narrowed exactly to the evidence.

No-invention status: **pass**.
