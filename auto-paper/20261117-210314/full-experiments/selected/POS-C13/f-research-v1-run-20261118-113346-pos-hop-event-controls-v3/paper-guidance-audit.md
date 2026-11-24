# Paper guidance audit

## Decision

**PASS.** The final source `writing/p10-revised-manuscript.md` covers the accepted guidance-v3 contract after documented bit-ledger, shuffle-control and leakage corrections.

## Coverage

| Guidance item | Final coverage | Status |
|---|---|---|
| Multi-hop representation | `[X,AX,A^2X,A^3X]` | covered |
| Hybrid format | 8 Lloyd centroids + escape, 4-bit symbol, 32-bit payload, 256-bit codebook | covered |
| Exact ledger | `4+32f_escape+256/N` | covered |
| Permutation audit | 5 seeds/graph, machine-precision results | covered |
| Shuffled-hop control | codec-consistent ordered-codebook mismatch | covered |
| Five-seed tasks | 40 retrained rows and paired dispersion | covered |
| Fixed raw probe | 90 ordered/shuffled rows | covered |
| Strong gates | error/storage/permutation/ratio/task loss | met |
| Negative evidence | leaky probe run and earlier mixed-code/identity shuffle | preserved/excluded |
| Six sections | Introduction–Conclusion | covered |
| Figures/tables | 3 figures, 2 tables | covered |
| Citations | 32 verified, 25 recent | covered |
| Scope | no broad transformer/SNN, temporal, energy or causal claim | covered |

No promised experiment or analysis is omitted.
