# CCFA Full Integrity Audit

review_execution: independent-agent

## Integrity Verdict

**REVISE**

**Score: 8.5/10**  
**Confidence: high**

The numerical and artifact integrity of the manuscript is strong. Revision is required for missing citation provenance, one scope phrase beyond the evidence, and table definition/auditability improvements.

## Numeric Consistency

- Raw `cert-methods.json`: 36 rows.
- Unique matrix keys: 36 = 3 graphs x 3 seeds x 2 levels x 2 quantizers.
- Containment: 36/36.
- Minkowski validity: 36/36.
- Global equality flags: 18/18.
- Rowwise tightening: 18/18, range `0.7426478701715937`–`0.821233146666029`, standard median `0.7964717049395805`.
- Rowwise width/RMS: standard median `30.679169413662216`, maximum `36.91338940552895`.
- Clipping count: 0; non-finite rows: 0.
- `cert-summary.json` agrees with raw methods for all binding statistics.
- Table 2 has 36 rows and every rounded width/tightening/containment entry matches raw methods.
- Provenance manifest: 24/24 entries exist and pass SHA-256 plus byte-count verification.

## Claim/Result Mapping

| Claim | Integrity status | Evidence |
|---|---|---|
| 36/36 deterministic final-logit containment | supported | raw rows and summary |
| `B_abs<=B_mink` | supported | raw flags and ordering |
| 18/18 global equality | supported | global rows and tolerance |
| Rowwise tightening 74.26–82.12%, median 79.65% | supported | raw rowwise values |
| Width/RMS standard median 30.68, max 36.91 | supported | summary and raw methods |
| No clipping/non-finite/omissions | supported | diagnostics and complete matrix |
| Bibliography/citation validity | **not auditable** | no references section in manuscript |

## Formula Checks

- `M=XW0`, `H=relu(AM+b0)`, `Z=AHW1+b_out` are dimensionally consistent.
- `B_abs=|A||A|Delta|W1|` follows from ReLU non-expansiveness and the two aggregation operations.
- `B_mink` is a valid analytic comparator, but Table 1’s shorthand omits the graph-weighted row-radius sum and should be expanded.
- `B_global` is correctly scoped as a matched global-radius ablation.
- Width/RMS and tightening definitions match the summary and Table 2.

## Figures And Tables

- Figure assets exist for Figures 1–3.
- Figure 3 source CSV is present and tied to the 36 raw rows.
- Captions correctly avoid statistical-coverage and absolute-width claims.
- Table 2 is complete for its declared columns and preserves all 36 rows.
- Comparator validity and equality gap are not columns in Table 2; this is an auditability gap, not a numeric contradiction.

## Scope And Overclaim Audit

Safe boundaries are mostly preserved:

- deterministic theorem/implementation containment is not statistical coverage;
- absolute width/RMS is descriptive;
- global comparator is a matched ablation;
- temporal, energy, hardware, learned-quantizer, robustness, and multilayer claims are excluded.

Unresolved boundary:

- “rate-coded spiking implementation” appears in the abstract despite no rate-coded SNN or temporal spike experiment.

## Required Integrity Actions

1 Add a verified bibliography and source metadata for all 37 citation keys.
2 Replace or qualify rate-coded SNN wording.
3 Expand Table 1’s `B_mink` and scalar-reference definitions.
4 Add comparator/equality status to Table 2 or a linked appendix.
5 Normalize `-0.00` values to numerical zero or explain the formatting.
6 Keep the provenance manifest and complete raw table attached to the final package.

**Recommendation:** revise. No numerical fabrication, row omission, formula inconsistency, or provenance failure was found.
