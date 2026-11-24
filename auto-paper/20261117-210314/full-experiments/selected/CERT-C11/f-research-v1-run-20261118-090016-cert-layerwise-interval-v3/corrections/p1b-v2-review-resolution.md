# P1B v2 review resolution

The v2 independent CCFA review returned `revise` because the operator chain alternated between incompatible pre/post-aggregation forms, the Euclidean comparator was not the standard rowwise bound, and numerical policies were incomplete.

Guidance-v3 resolves these defects before experimentation:

- The sole certified chain is `M=XW0`, `M_hat=Q(M)`, `H=relu(A M+b0)`, `H_hat=relu(A M_hat+b0)`, `Z=A H W1+b_out`.
- `Delta` is the deterministic half-step radius of the declared uniform/per-channel quantizer and is never estimated from actual errors.
- `B_prop=abs(A)abs(A)Delta abs(W1)` is the independent-coordinate absolute interval envelope.
- The Euclidean comparator is the correctly defined rowwise `l2` bound, while the global scalar formula remains a loose reference.
- RMS, median width, per-cell tightening, zero-denominator handling, float precision, clipping, tie-breaking, NaN/Inf, and `atol/rtol` are fixed.
- The claim is limited to the exact two-layer frozen-GCN path and deterministic theorem/implementation containment.

The previous v2 run is preserved as a failed/revised attempt and is not evidence for the v3 main claim.
