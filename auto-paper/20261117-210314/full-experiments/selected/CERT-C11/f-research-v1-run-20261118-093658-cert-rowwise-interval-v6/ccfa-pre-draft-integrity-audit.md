# CCFA Pre-Draft Integrity Audit

review_execution: independent-agent

## Integrity Verdict

**REVISE**

**Score: 8.1/10**  
**Confidence: high**

The full 36-row evidence is structurally complete and the binding strong gate is satisfied. One summary statistic is not computed under the standard median convention, and the planned radius-heterogeneity figure lacks a directly traceable distribution field in the reviewed artifacts. These are pre-draft corrections, not evidence failures.

## Numeric Consistency

### Matrix and serialization

- `cert-methods.json`: 36 rows.
- Unique matrix keys: 36 = 3 datasets x 3 seeds x 2 levels x 2 quantizers.
- `cert-baseline.json`: 12 rows; all 12 match their corresponding `cert-methods.json` seed-0 rows.
- `cert-summary.json`: row count and gate counts agree with recomputation.
- No row omissions or duplicate keys were found.

### Recomputed statistics

| Quantity | Recomputed from `cert-methods.json` | Stored summary | Status |
|---|---:|---:|---|
| Containment | 36 | 36 | pass |
| Minkowski validity | 36 | 36 | pass |
| Global equality flags | 18 | 18 | pass |
| Rowwise tightening min | 0.7426478701715937 | 0.7426478701715937 | pass |
| Rowwise tightening median | 0.7964717049395805 | 0.7964717049395805 | pass |
| Rowwise tightening max | 0.821233146666029 | 0.821233146666029 | pass |
| Rowwise width/RMS median | **30.679169413662216** | **30.712356567965056** | **mismatch** |
| Rowwise width/RMS max | 36.91338940552895 | 36.91338940552895 | pass |
| Clipping | 0 | 0 | pass |
| Non-finite rows | 0 | 0 | pass |

The width/RMS median mismatch is caused by using the upper middle order statistic (`30.712356567965056`) instead of the standard even-sample median, which averages the 9th and 10th sorted values (`30.64598225935937` and `30.712356567965056`). The dossier and `strong-result-lock.md` repeat the nonstandard `30.71` value. This does not affect the strong gate because width is descriptive, but it must be corrected or explicitly labeled as `median_high`.

### Additional numeric checks

- `B_abs <= B_mink`: 36/36; ordering failures: 0.
- Global equality maximum width gap: `3.20e-14`, within tolerance.
- Recomputed rowwise tightening differs from reported tightening by 0 at parsed precision.
- Maximum `max_bound_excess`: `-0.0689522`; all rows have negative excess.
- Actual RMS range: `0.0190024` to `0.9580673`.
- Clipping count: 0; non-finite count: 0.
- All 36 radius hashes are unique and retained.

## Claim-to-Result Mapping

| Claim | Mapping | Status |
|---|---|---|
| 36/36 containment | `cert-methods.json` flags and diagnostics | supported |
| 36/36 Minkowski validity | `minkowski_valid` and width ordering | supported |
| 18/18 global equality | global rows and equality flags | supported |
| Rowwise tightening 74.26–82.12%, median 79.65% | rowwise `tightening` | supported |
| Width/RMS median 30.71 | summary field | **incorrect under standard median** |
| Width/RMS maximum 36.91 | rowwise max | supported |
| No clipping/non-finite/omissions | diagnostics and row count | supported |

## Formula Audit

- `B_abs=|A||A|Delta|W1|` matches the rowwise `Delta∈R^(N×H)` contract.
- `B_mink=(|A||A| rownorm(Delta,2)) ||W1[:,k]||2` is valid and ordering is analytic.
- `B_global_col=rowsum(|A||A|) max(Delta) ||W1[:,k]||1` is a matched outputwise global-radius comparator.
- Float64 reconstruction, tolerance, zero rules, clipping, and deterministic-audit interpretation remain consistent across guidance, contract, and results.

## Planned Figures And Tables

- **Figure 1:** operator chain is supported by guidance and the dossier.
- **Figure 2:** rowwise/global width-RMS and tightening are supported by row-level results.
- **Figure 3:** global-equality component is supported; rowwise radius heterogeneity needs a traceable distribution or summary source beyond radius hashes and zero-step counts.
- **Table 1:** formulas and numerical policy are supported.
- **Table 2:** 36-row summary and worst-case diagnostics are supported, after correcting the width median label/value.

## Overclaim Boundaries

Correctly enforced:

- deterministic containment is not statistical coverage;
- width/RMS is descriptive;
- global comparator is a matched ablation;
- scope excludes temporal, energy, hardware, robustness, and multilayer claims.

Remaining risk:

- the phrase “accepted contribution” can sound stronger than the literature evidence;
- “final-logit certificate” must remain visible wherever “GNN-to-SNN” appears;
- Figure 3 must not imply radius-heterogeneity evidence that is not traceable.

## Required Integrity Actions

1 Correct `rowwise_width_rms_median` to `30.679169413662216`, or explicitly define and label an upper-median convention everywhere.
2 Synchronize the corrected statistic in `pre-draft-evidence-dossier.md` and `strong-result-lock.md`.
3 Provide a traceable radius-heterogeneity source for Figure 3 or remove/relabel that panel.
4 Add code/data/model/output hashes to the traceability record before manuscript freezing.
5 Keep the 36 rows and all diagnostics in the final table; do not summarize away failures or negative width evidence.

**Recommendation:** revise the summary statistic and figure traceability before drafting. The result package otherwise passes the integrity gate.
