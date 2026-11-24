# CCFA Pre-Draft Action Ledger

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 7.5/10**  
**Confidence: high**

The evidence supports a narrow rowwise certificate paper after a small set of scientific-positioning and integrity corrections. No action requires rerunning experiments or changing the frozen result rows.

## Priority P0 — Before Drafting

| Action | Reason | Completion evidence |
|---|---|---|
| Correct rowwise width/RMS median from 30.712356567965056 to 30.679169413662216, or label `median_high` explicitly | Standard even-sample median mismatch | Dossier, lock, summary, and manuscript numbers agree |
| Make Figure 3 radius heterogeneity traceable or remove/relabel the panel | Reviewed rows expose hashes/zero-step counts but not the plotted distribution | Figure source and caption map to a frozen field/artifact |
| Freeze claim wording around deterministic final-logit containment | Prevents statistical-coverage and end-to-end SNN overclaim | Abstract, title, and conclusion use scoped wording |

## Priority P1 — Scientific Positioning

| Action | Reason | Completion evidence |
|---|---|---|
| Verify related work and novelty against interval propagation, graph quantization, and ANN-to-SNN conversion | Current dossier has no literature audit | Verified references and explicit novelty delta |
| Call `B_global_col` a matched global-radius ablation | It is fair for radius granularity but not a SOTA baseline | Baseline wording in methods, tables, and discussion |
| Call `B_mink` a valid norm comparator | Its ordering is analytic, not an empirical win | Figure/table labels and result text |
| Explain rowwise choice versus per-channel/learned quantizers | Reviewers will ask why this granularity is appropriate | Limitations/future-work paragraph |
| Preserve high width/RMS as descriptive negative evidence | Avoids reviving the failed absolute-width claim | All results tables report the full range |

## Priority P2 — Reproducibility And Presentation

| Action | Reason | Completion evidence |
|---|---|---|
| Add code, data, model, and output hashes to traceability | Guidance requires frozen provenance beyond radius hashes | `experiment-traceability.md` links manifests and hashes |
| Report all 36 rows and worst cases | Prevents selective summary and preserves failures | Table 2 and raw artifact references |
| Separate theorem audit, comparator ordering, and empirical tightening | Prevents tautology/overclaim confusion | Results and discussion structure |
| Keep scope at frozen two-layer final-logit conversion | Avoids unsupported spike, energy, robustness, or multilayer claims | Abstract, title, conclusion, limitations |

## Acceptance Condition

After P0 and P1 actions, the package is suitable for manuscript drafting with the following fixed claims:

- 36/36 deterministic theorem/implementation containment;
- 36/36 valid `B_abs<=B_mink`;
- 18/18 global-uniform equality controls;
- 18/18 rowwise cells with at least 25% tightening versus `B_global_col`;
- width/RMS descriptive only.

No experiment rerun is required by this ledger. If Figure 3 cannot be sourced without new computation, replace it with a table or remove it rather than reconstructing data from prose.
