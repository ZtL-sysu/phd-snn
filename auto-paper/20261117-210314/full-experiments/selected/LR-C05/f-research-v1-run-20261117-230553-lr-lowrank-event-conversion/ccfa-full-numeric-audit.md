# Full numeric and claim audit

- `results/summary.json` is recomputed from `baseline.json` and `method.json`.
- Rank128/1% results use seeds 0/1/2 and validation masks only.
- Gain intervals are paired seed bootstraps; Squirrel T2 includes zero.
- Compression is dimension compression `N F / [k(N+F)]`; residual storage accounting is separate.
- Runtime ratios include measurement noise; tail behavior is disclosed.

No numeric inconsistency found. Claim scope is valid. No-invention status: **pass**.
