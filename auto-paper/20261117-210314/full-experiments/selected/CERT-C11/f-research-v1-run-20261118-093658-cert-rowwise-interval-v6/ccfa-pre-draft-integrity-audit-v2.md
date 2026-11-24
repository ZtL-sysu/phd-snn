# CCFA Pre-Draft Integrity Audit v2

review_execution: independent-agent

## Integrity Verdict

**PROCEED**

**Score: 9.2/10**  
**Confidence: high**

The P5A repairs resolve the prior numeric and traceability findings. The package is internally consistent against raw `results/cert-methods.json`, and no integrity issue blocks drafting.

## Repair Verification

### Standard median

`results/cert-summary.json`, `pre-draft-evidence-dossier.md`, and `strong-result-lock.md` now use the standard even-sample median:

`rowwise_width_rms_median = 30.679169413662216`.

Recomputation from the 18 rowwise values in raw methods gives the same value. The maximum remains `36.91338940552895`.

### Figure 3 source data

`figures/source-data/figure3-rowwise-tightening.csv` contains 36 rows and matches raw `cert-methods.json` field-for-field for all plotted metrics and radius hashes:

- row count: 36/36;
- numeric field mismatches: 0;
- radius hash mismatches: 0.

The repaired Figure 3 plan is therefore traceable and does not reconstruct evidence from prose.

### Provenance

`provenance-manifest.json` contains 24 entries covering model snapshots, dataset snapshots, run code, and raw outputs.

- checked entries: 24/24;
- missing paths: 0;
- SHA-256 mismatches: 0;
- byte-count mismatches: 0.

`experiment-traceability.md` links the manifest, Figure 3 source, and corrected summary statistic.

## Numeric Consistency

- Raw methods rows: 36 unique matrix keys.
- Containment: 36/36.
- Minkowski validity: 36/36.
- Global equality: 18/18 within tolerance.
- Rowwise tightening: 18/18; minimum `0.7426478701715937`, median `0.7964717049395805`, maximum `0.821233146666029`.
- Clipping count: 0.
- Non-finite rows: 0.
- Formula and comparator ordering: unchanged and valid.

## Claim Mapping

| Claim | Status |
|---|---|
| Deterministic final-logit containment | supported by 36 raw rows |
| `B_abs<=B_mink` | supported and analytic |
| Global-uniform equality | supported by 18 rows |
| Rowwise tightening versus matched global-radius ablation | supported by 18 rows |
| Descriptive standard median 30.68 | corrected and supported |
| No absolute-width or statistical-coverage claim | wording and lock are consistent |

## Overclaim Boundary

The package now consistently says:

> deterministic final-logit certificate plus matched global-radius ablation.

It does not claim statistical coverage, broad SNN superiority, robustness, energy, temporal spikes, or state-of-the-art compression. This is the correct integrity boundary.

**Recommendation:** proceed. Preserve the raw rows, source-data CSV, provenance manifest, and scoped wording unchanged during drafting.
