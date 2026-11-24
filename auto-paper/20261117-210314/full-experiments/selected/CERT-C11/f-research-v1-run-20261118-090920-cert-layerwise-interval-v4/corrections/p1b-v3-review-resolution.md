# P1B v3 review resolution

Guidance-v4 resolves the v3 block:

- The gate comparator is `B_global_col[i,k]=c_i max(delta) ||W1[:,k]||_1`, not a collapsed full-matrix scalar.
- Global-uniform quantization has constant radii, so `B_abs == B_global_col` by construction. These 18 cells are equality controls and are excluded from the tightening gate.
- Tightening ≥25% is required only for the 18 per-channel cells where radius heterogeneity can create a real gap.
- The gate norm comparator is the valid Minkowski upper bound `||W1[:,k]||_2 sum_j C[i,j]delta_j`.
- All source values are cast to float64 before quantization and remain float64 through dequantization and reconstruction.
- Constant channels use step/radius zero with exact identity reconstruction.
- Median axes, zero-width policies, tolerance predicate and clipping behavior are exact.
