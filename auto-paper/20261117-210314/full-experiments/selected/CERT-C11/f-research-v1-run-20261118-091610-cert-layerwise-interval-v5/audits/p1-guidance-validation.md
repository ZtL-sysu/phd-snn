# P1 guidance validation

**PASS.** Guidance-v5 corrects the node/channel dimensions and uses `c=(|A||A|)1`, `B_abs[i,k]=c_i sum_h delta_h|W1[h,k]|`, `B_mink[i,k]=c_i||delta||2||W1[:,k]||2`, and `B_global_col[i,k]=c_i max(delta)||W1[:,k]||1`. All numerical and gate policies remain explicit.
