# POS-C13 v3 experiment protocol

1. Build `H=[X,AX,A^2X,A^3X]` in float64 from frozen Chameleon/Squirrel snapshots.
2. Fit eight-centroid per-channel Lloyd codebooks and select exact escapes by the frozen representation or training-only task protocol.
3. Serialize each value with one four-bit symbol (eight centroid IDs or escape), add a 32-bit float32 payload for each escape, and charge `8×32` bits per channel for centroids. Report `4 + 32 f_escape + 256/N`.
4. Evaluate raw, uniform, per-channel Lloyd and hybrid methods over split/probe seeds 600-604.
5. For each graph and shuffle seed, fit ordered codebooks, globally permute hop blocks, quantize shuffled columns with the unchanged codebooks, and compare to shuffled raw. POS-E aggregation is the mean error ratio over five shuffle seeds per graph; report min/max and every row. The strong gate is graph-level mean ratio ≥1.25 on both graphs.
6. Reuse one fixed raw-trained probe and identical split/evaluation nodes for ordered and shuffled fixed-probe rows.
7. Run node-permutation audits with five permutation seeds and deterministic tie handling.
8. Preserve all raw rows, escape masks, bit ledgers and negative controls.
