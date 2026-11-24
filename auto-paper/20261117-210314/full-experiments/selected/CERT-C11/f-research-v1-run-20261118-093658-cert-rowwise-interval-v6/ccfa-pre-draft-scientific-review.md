# CCFA Pre-Draft Scientific Review

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 6.8/10**  
**Confidence: medium-high**

The v6 evidence is scientifically coherent for a narrow application-specific certificate, and the rowwise-relative-tightening result is strong within the matched ablation. The paper is not yet ready to draft because novelty positioning is not evidenced in the reviewed package, the comparator establishes radius-granularity utility rather than broad superiority, and the GNN-to-SNN framing risks implying task, spike, energy, or robustness results that were not measured.

## Evidence Reviewed

- `pre-draft-evidence-dossier.md`
- `inputs/guidance-v6.md`
- `results/cert-baseline.json`
- `results/cert-methods.json`
- `results/cert-summary.json`
- `strong-result-lock.md`
- `experiment-traceability.md`
- `ccfa-baseline-evidence-review.md`

No experiment was run and no evidence was modified.

## Scientific Assessment

### Novelty

**5.5/10** The operator-aware graph context, rowwise radius matrix, and matched global-radius ablation form a useful application-level contribution. The underlying ingredients—absolute-value interval propagation, ReLU non-expansiveness, and norm comparisons—are standard. The defensible novelty is the rowwise quantizer/certificate design for the exact frozen two-layer GNN message path, not a new general certificate theorem.

The reviewed package contains no literature matrix or prior-art comparison. Before drafting, the paper must position the work against interval bound propagation, graph-message quantization, frozen ANN-to-SNN conversion, and certified/robust SNN literature. Without that audit, Q2+/TNNLS novelty is uncertain.

### Soundness

**8.5/10** The chain and derivation are sound:

`M=XW0`, `M_hat=Q_rowwise(M)`, `H=relu(A M_hat+b0)`, `Z=A H W1+b_out`.

ReLu non-expansiveness yields `|H-H_hat|<=|A||E|`, and the second aggregation gives

`B_abs=|A||A|Delta|W1|`.

The Minkowski comparator is valid, `B_abs<=B_mink` is analytic, and `B_global_col` is a fair matched global-radius collapse. Deterministic containment is correctly labeled theorem/implementation validation rather than statistical coverage.

### Baseline Fairness

**7/10** The global comparator is fair for the narrow question “what is gained by rowwise radii versus a single global radius?” It is not a broad state-of-the-art baseline. The 74.26–82.12% tightening is a real rowwise-radius ablation result, but it should not be described as superiority over certified norm bounds generally. `B_mink` is a validity comparator; its ordering is expected analytically.

### Claim Scope

**8/10** The dossier correctly limits the claim to deterministic final-logit envelopes for frozen two-layer GCN snapshots, 3 graphs, 3 seeds, 4/8 levels, and global/rowwise uniform quantization. It explicitly excludes learned quantizers, temporal spikes, energy, hardware, robustness, and multilayer claims. The absolute width/RMS target is correctly demoted to descriptive reporting.

## Result Strength

- Full matrix: 36/36 deterministic containment.
- Minkowski ordering: 36/36.
- Global-uniform equality: 18/18 within tolerance.
- Rowwise tightening: 18/18, 74.26–82.12%, median 79.65%.
- Failure diagnostics: no clipping, non-finite rows, or omitted failures.

This is strong evidence for the stated rowwise mechanism. It is not evidence for end-to-end SNN accuracy, spike efficiency, energy, or robustness.

## Reviewer-Facing Risks

1. **Novelty challenge:** reviewers may classify the method as straightforward interval propagation specialized to a rowwise quantizer.
2. **Baseline challenge:** the main comparator is a deliberately matched global-radius ablation, not an external certified baseline.
3. **Scope challenge:** “GNN-to-SNN” may overstate a final-logit finite-precision certificate with no spike dynamics or task metrics.
4. **Tautology challenge:** containment is construction/theorem validation; the empirical contribution is relative bound width.
5. **Width challenge:** descriptive width/RMS is large (rowwise median approximately 30.68, maximum 36.91), so it must remain out of headline claims.
6. **Quantizer challenge:** reviewers may ask why rowwise uniform radii are preferable to per-channel, learned, or nonuniform schemes.
7. **Generality challenge:** three graphs and three seeds support a scoped study, not a universal graph-conversion result.

## Required Scientific Actions

1. Add a verified related-work/novelty audit before drafting.
2. State the contribution as a rowwise-radius certificate and matched ablation for the exact frozen chain.
3. Keep all task, spike, energy, robustness, and temporal claims out of the title, abstract, and conclusion.
4. Report `B_abs`, `B_mink`, `B_global_col`, and width/RMS with explicit “validity comparator” and “global-radius ablation” labels.
5. Explain why rowwise radii are the tested granularity and list per-channel/learned quantizers as future comparisons.
6. Report the high descriptive width honestly and explain why no absolute-width claim is made.

**Recommendation:** revise the scientific positioning and claim language before drafting; the underlying evidence is sufficient for a narrow, carefully scoped paper.
