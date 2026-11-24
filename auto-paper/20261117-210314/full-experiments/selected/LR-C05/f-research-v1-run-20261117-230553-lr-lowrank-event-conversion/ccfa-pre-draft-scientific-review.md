# CCFA pre-draft scientific review

Review execution: `independent-agent`.

## Verdict

**Weak reject / major revision before drafting. Readiness 4/10.** The current evidence supports local message reconstruction and teacher-agreement effects, but not the planned equal-budget operator-aligned residual-event conversion claim.

## Supported

- Rank128 plus 1% sensitivity-selected exact sparse residual coefficients reduces message error by 19.29/30.60/25.91% on Cora/Chameleon/Squirrel under the nominal run model.
- Rate-coded teacher-agreement gains are positive on average; Squirrel T2 is unstable across three seeds.
- Local scope and no-energy boundary are appropriately explicit.

## Fatal repairs before P6

1. LR-A must use contracted hidden/logit MSE, not message error.
2. Serialized cost must include factors, indices, scales, residual values and encode/decode; rerun exact matched-bit controls.
3. Add random projection rank-k plus residual, top-absolute-residual ablation and full-float reference.
4. Adapt A²Q and One-Spike baselines; use AdaQP for positioning. Unless real asynchronous events are implemented, rename “residual events” to “sparse residual coefficients”.
5. Benchmark full SVD/selection/indexing/conversion latency and memory with warmed repeats; report all seeds, sample SD and descriptive n=3 intervals.

## Scorecard

| Dimension | Score | Confidence | Repair |
|---|---:|---:|---|
| Novelty | 2/5 | 3/5 | adapt prior-art baselines or narrow novelty |
| Soundness | 2/5 | 4/5 | fix LR-A metric and storage formula |
| Evidence | 2/5 | 4/5 | add contracted baselines and full-float reference |
| Significance | 3/5 | 4/5 | keep local frozen-GCN scope |
| Clarity | 3/5 | 4/5 | distinguish message/logit error and coefficient/event terminology |
| Reproducibility | 3/5 | 4/5 | complete warmed cost benchmark |
| Ethics/limitations | 4/5 | 4/5 | preserve boundary |

P6 writing is blocked until repairs pass and a new strong-result lock is issued.
