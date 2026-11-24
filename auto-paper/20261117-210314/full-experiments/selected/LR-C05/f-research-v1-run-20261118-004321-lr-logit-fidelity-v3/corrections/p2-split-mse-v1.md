# Correction: split-specific MSE

- Trigger: first confirmation output had identical validation/test MSE because errors were computed on all nodes.
- Repair: compute message/hidden/logit MSE only on the selected split mask; preserve the invalid output as superseded.
- Gate unchanged. Rerun test confirmation before P3.
