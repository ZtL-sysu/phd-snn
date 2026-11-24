# codex-ccfa-full-review-20261118

## Scope

- Independent CCFA `full` review of the frozen LR-C05 manuscript and specified evidence only.
- Read the frozen manuscript, evidence digest, ARC Reviewer A/B, confirmation summaries, validation summary, and timing summary.
- Did not edit the manuscript or run experiments.

## Output

- Report: `C:\code\phd-snn\auto-paper\20261117-210314\full-experiments\selected\LR-C05\f-research-v1-run-20261118-004321-lr-logit-fidelity-v3\ccfa-full-paper-review.md`
- Calibrated stance: weak reject / borderline negative.
- Overall score: 5/10; scholarly confidence: 4/5

## Key Findings

- The focal logit-MSE result is supported within the tested scope: 26.23%, 33.99%, and 25.83% reductions and nine positive dataset-seed comparisons.
- Raw confirmation data includes `top_abs`, `random`, and `uniform` selector rows omitted from the manuscript. This partially repairs ARC Reviewer A’s selector-isolation concern, but the controls are not defined in the frozen text.
- Matched total padded bits are visible per dataset, but the serialization schema, 2% denominator, rounding, and matching scope remain unauditable.
- Task-loss reporting is ambiguous: summary values align with teacher-agreement-only or best-task-control-per-metric interpretations, not a fully stated accuracy-plus-agreement formula tied to `top_abs`.
- Rank-128 transport scope for hidden-width-16 graph messages remains ambiguous and can be fatal if the wrong tensor/layer was compressed.
- Existing artifacts can repair raw-result presentation, comparator labeling, timing statistics, and some protocol documentation. Independent replication, formal task equivalence, focal 2% timing, downstream/energy utility, and missing mechanism ablations require new experiments.

## Checks

- Verified SHA256 values of the four raw evidence inputs cited in the digest.
- Recomputed matched-bit totals, paired fidelity directions, task-loss alternatives, and timing p95 ratios.
- Verified report section order, Markdown table column counts, and absence of placeholders.
- Verified manuscript SHA256 remained `e35047b6ed4e6ae0bdcc9470fb754d6fd398f8d6f2f8aaf2e20e574e9726b8cb`.
