# CCFA Full-Paper Review

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 6.9/10**  
**Confidence: medium-high**

The manuscript is technically coherent, numerically disciplined, and unusually explicit about its limitations. It is not yet submission-ready because the citation apparatus is incomplete and the rate-coded SNN wording exceeds the measured final-logit scope. The scientific contribution is valid but narrow and should be positioned as an application-specific certificate plus a matched radius-granularity ablation.

## Evidence Reviewed

- `writing/p8-manuscript-with-figures.md`
- `figures/captions.md`
- `writing/p8-table-plan.md`
- `figure-table-insertion-audit.md`
- `results/cert-methods.json`
- `results/cert-summary.json`
- `strong-result-lock.md`
- `pre-draft-evidence-dossier.md`
- `provenance-manifest.json`

No manuscript or evidence file was edited and no experiment was run.

## Scientific Assessment

### Novelty

**5.8/10** The rowwise radius matrix, exact two-aggregation graph chain, and matched global-radius ablation form a clear application-specific contribution. The mathematical ingredients—interval propagation, ReLU non-expensiveness, and norm bounds—are standard. The paper should sell the contribution as a carefully scoped deterministic final-logit certificate and radius-granularity study, not a new general verification theorem.

The manuscript contains 37 unique citation keys but no References/Bibliography section. The novelty and related-work claims are therefore not yet auditable. The `katz2022reluplex` key also needs bibliographic verification; citation keys cannot substitute for verified references.

### Soundness

**8.5/10** The chain, quantizer radius, `B_abs`, `B_mink`, and `B_global` are mathematically consistent. The manuscript correctly distinguishes analytic ordering from empirical tightening and deterministic containment from statistical coverage.

### Baseline fairness

**7.5/10** `B_global` is a fair matched global-radius ablation for the stated question. It is not a state-of-the-art compression or certified-ML baseline. The paper says this explicitly, which is appropriate. The 74.26–82.12% tightening should remain scoped to the ablation and exact chain.

### Clarity and claim scope

The method and results sections are clear, and the negative absolute-width result is handled honestly. The abstract’s phrase “after conversion to a rate-coded spiking implementation” is broader than the evidence: the experiments certify final logits in a frozen conversion chain and do not measure temporal spikes or a rate-coded implementation.

## Reviewer Concerns

1. **Major — Missing bibliography.** The manuscript has 37 unique `\\cite` keys but no References/Bibliography section, DOI/URL audit, or evidence that each key resolves to a real source. Add a verified bibliography and check duplicate titles, authors, years, and venues.
2. **Major — Rate-coded scope.** Remove or qualify “rate-coded spiking implementation” unless an actual rate-coded SNN is evaluated. Safe wording is “finite-precision frozen GNN-to-SNN conversion chain” or “final-logit conversion path.”
3. **Medium — Novelty positioning.** Explicitly contrast the work with standard IBP and norm bounds; do not imply that the absolute-value propagation itself is new.
4. **Medium — Table 1 definition precision.** The `B_mink` role text says “row-radius 2-norm times output-column 2-norm” but omits the graph-weighted sum `sum_q G_iq ||Delta_q||_2`. Use the full formula or label it as shorthand.
5. **Medium — Comparator auditability.** Table 2 contains containment, width/RMS, and tightening, but not `B_abs<=B_mink` or equality-gap status. Add compact status columns or an appendix table so the headline comparator claims are directly auditable.
6. **Low — Signed zero formatting.** Several global tightening cells display `-0.00`. Normalize values within tolerance to `0.00` or explain that these are floating-point zeros.

## Required Actions

1. Add and verify the complete bibliography and citation metadata.
2. Remove or qualify the rate-coded SNN wording throughout the abstract/title framing.
3. Tighten novelty language around standard interval propagation and the rowwise application delta.
4. Correct or expand Table 1 formulas.
5. Make comparator/equality status auditable in Table 2 or a linked appendix.
6. Normalize signed zero values and retain all 36 rows.

**Recommendation:** revise before final paper approval. The core scientific evidence is sound; the remaining issues are presentation, citation completeness, and scope precision.
