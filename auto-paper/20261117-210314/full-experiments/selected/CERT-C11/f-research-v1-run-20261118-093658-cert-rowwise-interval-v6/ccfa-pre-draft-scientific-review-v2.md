# CCFA Pre-Draft Scientific Review v2

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 8.4/10**  
**Confidence: medium-high**

The P5A repair resolves the prior scientific-positioning blockers. The package now consistently frames the contribution as a **deterministic final-logit certificate plus matched global-radius ablation**, not broad SNN superiority, robustness, or a state-of-the-art compression baseline.

## Evidence Reviewed

- `corrections/p5a-pre-draft-repair.md`
- `results/cert-summary.json`
- `pre-draft-evidence-dossier.md`
- `strong-result-lock.md`
- `figures/source-data/figure3-rowwise-tightening.csv`
- `provenance-manifest.json`
- `experiment-traceability.md`
- raw `results/cert-methods.json`

No experiment was run and no evidence was modified.

## Scientific Assessment

### Novelty and positioning

The defensible contribution is narrow but coherent: rowwise quantizer radii are propagated through the exact frozen two-layer graph chain, and the resulting outputwise envelope is compared with a matched global-radius ablation. The dossier explicitly rejects broad SNN superiority, state-of-the-art compression, and robustness claims. This resolves the prior overclaim risk.

The contribution remains application-specific interval propagation; related-work positioning should continue to avoid presenting `B_abs` as a new general theorem.

### Soundness

The formula chain remains valid:

`B_abs=|A||A|Delta|W1|`.

The Minkowski ordering is analytic, global-uniform equality is structural, and the empirical contribution is the rowwise relative tightening under deterministic containment. The wording now reflects that distinction.

### Baseline fairness

`B_global_col` is correctly described as a matched global-radius ablation. The reported 74.26–82.12% rowwise tightening is meaningful for radius granularity, but should remain scoped to this comparator and exact chain.

### Evidence strength

- 36/36 deterministic final-logit containment.
- 36/36 valid Minkowski ordering.
- 18/18 global-uniform equality controls.
- 18/18 rowwise cells pass the 25% tightening gate.
- Standard rowwise width/RMS median is corrected to 30.679169413662216; width remains descriptive.

## Reviewer-Facing Guardrails

1. Keep “deterministic final-logit certificate” visible wherever “GNN-to-SNN conversion” appears.
2. Call the comparator a matched global-radius ablation, not an external state-of-the-art baseline.
3. Keep `B_mink` ordering labeled as an analytic validity check.
4. Keep width/RMS descriptive and report the high values honestly.
5. Preserve exclusions for temporal spikes, energy, hardware, learned quantizers, robustness, and multilayer claims.

**Recommendation:** proceed to drafting with the scoped wording and evidence boundaries unchanged.
