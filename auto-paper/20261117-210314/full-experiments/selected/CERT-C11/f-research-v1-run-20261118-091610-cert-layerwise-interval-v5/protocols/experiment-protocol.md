# CERT-C11 corrected experiment protocol

1. Load frozen local graph/model snapshots for Cora, Chameleon and Squirrel, seeds 0/1/2.
2. Cast all source arrays to float64 before quantization.
3. For levels 4/8 and global/per-channel uniform quantizers, compute deterministic half-step radius before inspecting actual errors.
4. Reconstruct `M_hat`, `H_hat`, `Z_hat` along the exact v5 chain.
5. Compute `B_abs`, `B_mink`, `B_global_col`, `B_scalar`, actual error, RMS and tolerance diagnostics.
6. Emit every cell to JSON and CSV, including clipping, zero-step, non-finite and comparator failures.
7. Run tests before and after the matrix; no labels, splits, actual-error tuning or remote compute.
