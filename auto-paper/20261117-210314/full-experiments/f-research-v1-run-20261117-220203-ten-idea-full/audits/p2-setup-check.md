# P2 setup and protocol check

- Conda Python 3.13.13; PyTorch 2.11.0+cu128; PyG 2.8.0.post1.
- CUDA probe: `NVIDIA GeForce RTX 3060`, selected as `cuda`; campaign code exits if CUDA is unavailable.
- Shared utilities compile; 9/9 unit tests pass.
- Ten runner IDs import successfully and map to the canonical order DYN, EQ, PERM, SIGN, LR, EDGE, CERT, POS, DLY, READ.
- Commands, split policy, seed policy and result paths are frozen in `protocols/experiment-commands.md`.
- Historical datasets/checkpoints are read-only; all new logs/results stay in the run root.
- Reacceptance after `corrections/p2-eq-sampling-v1.md`: typed-coordinate class sampling uses pandas `groupby.sample`; tests and runner import are rerun before P3.
- Reacceptance after `corrections/p2-top2-indexing-v1.md`: top-two advanced indexing is covered by the existing order/shape test; all runners are re-imported.
- Reacceptance after `corrections/p2-lr-message-scope-v1.md`: LR uses raw `A X` messages and CUDA SVD/random projection; compression denominator is auditable.
- Reacceptance after `corrections/p4-mechanism-alignment-v1.md`: lossless initial+residual, float64 certificates and per-channel quantile POS codebook are covered by 11/11 tests.
- Reacceptance after `corrections/p5-pos-escape-v1.md`: hybrid 8-level Lloyd plus 0.5% escape events is covered by 13/13 tests and explicit average-bit accounting.

Verdict: **pass**.
