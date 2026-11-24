# Claim-evidence matrix

| Claim | Evidence | Comparator | Falsifier | Status |
|---|---|---|---|---|
| Exact deterministic containment | 36 corrected rows plus theorem audit | same actual errors | any `abs(Z-Z_hat) > B_prop+tol` | pending |
| Useful tightness | cellwise width/RMS and tightening | global scalar reference | median >10, max >15, or min tightening <25% | pending |
| Fair norm comparison | elementwise `B_prop <= B_euc+tol` | rowwise Euclidean bound | any violation | pending |
| Quantizer scope | global/per-channel uniform radius audit | same bounds | clipping, error-derived radius, NaN/Inf | pending |
| Scope stability | 3 graphs × 3 seeds × 2 levels × 2 quantizers | per-cell dispersion | isolated single-cell result | pending |
