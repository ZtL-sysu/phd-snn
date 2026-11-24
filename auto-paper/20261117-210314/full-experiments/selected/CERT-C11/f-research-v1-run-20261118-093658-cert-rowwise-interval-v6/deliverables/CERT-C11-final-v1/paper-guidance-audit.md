# Paper guidance audit

## Decision

**PASS.** The final source `writing/p12-citation-updated-manuscript.md` covers the accepted guidance-v6 contract after documented baseline stop-loss and P5A corrections.

## Coverage

| Guidance item | Final coverage | Status |
|---|---|---|
| Exact chain | `M=XW0 → Q_row → A relu → A H W1` in Abstract/Method | covered |
| Rowwise quantizer | step, ties, constant rows, float64 radius policy | covered |
| Proposed bound | exact `B_abs=|A||A|Delta|W1|` derivation | covered |
| Comparators | valid Minkowski, matched global-radius ablation, scalar context | covered |
| 36-cell matrix | 3 graphs × 3 seeds × 2 levels × 2 quantizers | covered |
| Strong gate | 36/36 containment, 36/36 Minkowski, 18/18 equality, 18/18 ≥25% tightening | met |
| Negative evidence | width/RMS standard median 30.68 and max 36.91 | covered |
| Failure diagnostics | no clipping/non-finite/omissions | covered |
| Six sections | Introduction through Conclusion | covered |
| Figures | exact chain, width/tightening, equality/tightening | covered |
| Tables | exact bound formulas and complete 36-row results | covered |
| Citations | 40 verified references, 30 from 2022–2026 | covered |
| Scope | deterministic final-logit certificate; no temporal/energy/robustness/multilayer claim | covered |

## Reconciled changes

- The v5 absolute width/RMS target failed baseline evidence and was explicitly narrowed before guidance-v6; the negative width result remains in the paper.
- Per-channel radii were replaced with rowwise radii after a deterministic diagnostic; this is the accepted v6 mechanism.
- Figure 3 was relabeled from unsupported radius heterogeneity to traceable tightening/width distribution.
- No promised experiment remains infeasible or omitted.
