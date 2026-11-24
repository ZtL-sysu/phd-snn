# P1B v2 review resolution

Guidance-v3 resolves both fatal v2 issues:

- Serialization now uses one four-bit symbol for eight centroids plus escape, 32-bit float payloads for escaped values, and `8×32` bits of codebook cost per channel amortized over `N` values. Average cost is exactly `4 + 32 f_escape + 256/N`.
- Shuffled-hop error is defined as quantizing globally hop-shuffled columns with unchanged ordered-channel codebooks and comparing with the shuffled raw target. It does not shuffle target and reconstruction together.
- Fixed raw probes reuse identical weights, intercepts, splits and evaluation nodes across ordered/shuffled rows.
- Codebook and escape fitting scope is explicit for representation versus task protocols.
