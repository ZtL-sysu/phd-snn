# Claim–evidence matrix

All rows are planned evidence at P1A.

| ID | Claim | Mechanism | Falsifier | Simple baseline | Strong/matched baseline | Evidence |
|---|---|---|---|---|---|---|
| LR-A | rank-128 compression is ≥8× on ≥2/3 graphs with lower logit error | SVD-aligned retained subspace | rank curve non-monotone or no equal-budget gain | full float | random+residual, uniform quantization | rank curves over 3 graphs×3 seeds |
| LR-B | downstream-scored residual events improve end-to-end conversion | prioritize residuals by hidden/logit sensitivity | no agreement gain over SVD-only | SVD-only | random residual and uniform residual | T=2/4 accuracy/agreement |
| LR-C | proposed allocation reduces residual bits/events at matched fidelity | sparse exact residual escapes | no bit/accuracy Pareto gain | uniform residual | equal total bits | bit/event Pareto |
| LR-D | method is computationally practical | low-rank transport plus bounded residual work | >20% regression without fidelity gain | SVD-only | optimized equal-budget coder | latency/peak-memory curves |

## Bounded execution contract

- Code: new run-local CUDA/CPU modules; prior LR screen is immutable input.
- Prototype: deterministic unit tests plus one seed; full: 3 graphs×3 seeds×ranks 16–128.
- Budget: ≤30 min/batch, ≤12GB VRAM, ≤12 configurations/seed, no remote compute.
- Search: frozen rank/budget grid; all trials logged.
- Stop/return: any target miss closes the row as negative and blocks success wording; code/split errors reopen earliest affected stage.
