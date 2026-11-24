# CCFA P9 Merged Concern Ledger

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 7.4/10**  
**Confidence: high**

The merged scientific and integrity evidence is strong enough for revision rather than rejection or blocking. Data, formulas, figures, tables, and provenance are sound; citation completeness and scope wording must be corrected before final approval.

## Numbered Concerns

| # | Severity | Concern | Evidence | Required action |
|---:|---|---|---|---|
| 1 | Major | Missing bibliography and unverified citation metadata | 37 unique `\\cite` keys; no References/Bibliography or bibliography entries in `writing/p8-manuscript-with-figures.md` | Add verified references, DOI/URL/title/author/year audit, and resolve suspicious keys such as `katz2022reluplex` |
| 2 | Major | Rate-coded SNN wording exceeds evidence | Abstract mentions “rate-coded spiking implementation”; experiments certify final logits only and explicitly exclude temporal spikes | Replace with scoped frozen GNN-to-SNN conversion/final-logit wording |
| 3 | Medium | Novelty may read as standard IBP repackaged | Method uses standard interval propagation and ReLU non-expansiveness; no direct prior-art table | Make the rowwise-radius application delta and matched ablation the explicit novelty |
| 4 | Medium | Table 1 comparator definition is abbreviated | `B_mink` role omits `sum_q G_iq ||Delta_q||_2`; scalar role omits `c_i` | Print exact formulas or label shorthand clearly |
| 5 | Medium | Comparator/equality claims are not directly auditable in Table 2 | Table 2 has containment, width/RMS, tightening only | Add `B_abs<=B_mink` and equality-gap/status columns or an appendix table |
| 6 | Low | Signed zero formatting is confusing | Global tightening rows include `-0.00` | Normalize within tolerance to `0.00` or footnote floating-point zeros |
| 7 | Low | Hidden-width/architecture claim needs provenance | Manuscript says hidden-16; reviewed result rows expose no architecture shape | Link model architecture metadata/hash in traceability |

## Verified Strengths

- 36-row matrix is complete and unique.
- All raw numeric claims and Table 2 rounded values agree.
- Standard median is correctly reported as `30.679169413662216`.
- Figure 3 source data is traceable and complete.
- Provenance manifest passes 24/24 hash and byte checks.
- Scope limitations are mostly explicit and scientifically conservative.

## Acceptance Condition

Proceed after concerns 1–2 are fixed and concerns 3–7 are addressed or explicitly accepted as presentation limitations. No rerun is required unless the authors choose to add a measured rate-coded SNN experiment; absent that, remove the rate-coded claim.
