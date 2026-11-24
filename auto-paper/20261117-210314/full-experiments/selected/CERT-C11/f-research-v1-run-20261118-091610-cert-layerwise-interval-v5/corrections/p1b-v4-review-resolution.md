# P1B v4 review resolution

The v4 review correctly observed that `Delta` has hidden-channel dimension `H`, while `C=|A||A|` has node dimension `N×N`; a shared `j` index was invalid.

Guidance-v5 uses the dimensionally correct reduction:

- `c_i=sum_q |A_iq| sum_p |A_qp|`.
- `B_abs[i,k]=c_i sum_h delta_h |W1[h,k]|`.
- `B_mink[i,k]=c_i ||delta||_2 ||W1[:,k]||_2`.
- `B_global_col[i,k]=c_i max_h(delta_h) ||W1[:,k]||_1`.

All other v4 numerical and gate policies are retained.
