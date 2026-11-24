# CCFA pre-draft scientific review

Review execution: `independent-agent`.

## Verdict

**Conditional pass; readiness 7/10; confidence 4/5.** The core logit-MSE claim is supported for three graphs, three seeds and frozen two-layer GCNs. P6 writing may proceed, but wording/numeric repairs are mandatory before freezing the abstract, conclusion or result lock.

## Verified findings

- Ratio-of-three-seed-mean split-specific logit-MSE reductions versus the strongest matched-budget control are 26.23%, 33.99% and 25.83%; all nine dataset-seed comparisons improve.
- Rank128/2% methods use identical total padded serialized bits within each dataset, though payload lengths and coefficient counts differ.
- Worst three-seed-mean task loss is 1.86 pp; worst seed-level loss is 2.85 pp, within the 3 pp bound.
- Paired p95 runtime ratios range 1.020–1.124×; peak allocation is 218.23 MB.

## Mandatory wording

- Main claim: “On the reported official test split, output-Jacobian-selected sparse residual coefficients at rank 128 and a 2% residual budget reduced the ratio of three-seed mean split-specific logit MSE by 26.23%, 33.99%, and 25.83% relative to the strongest evaluated matched-budget control.”
- Cost: “All compared rank-128/2% methods used identical total padded serialized bits within each dataset.”
- Task: “The maximum three-seed-mean degradation across T2/T4 accuracy and teacher agreement was 1.86 pp; the largest seed-level degradation was 2.85 pp.”
- Disclosure: “The focal setting and logit-fidelity reframing were fixed after validation exposure and before the confirmation run. The subsequent test run is held-out confirmation, not a preregistered or independent replication.”
- Timing: “Across nine dataset-seed pairs, paired p95 runtime ratios versus SVD-only ranged from 1.020× to 1.124×.”
- Literature: call A²Q/One-Spike implementations our matched-budget adaptations; no SOTA/novelty claim before 36-reference audit.

## Scorecard

| Dimension | Score | Confidence |
|---|---:|---:|
| Novelty | 3/5 | 3/5 |
| Soundness | 4/5 | 4/5 |
| Evidence | 4/5 | 4/5 |
| Significance | 3/5 | 4/5 |
| Clarity | 3/5 | 4/5 |
| Reproducibility | 4/5 | 4/5 |
| Ethics/limitations | 4/5 | 4/5 |
