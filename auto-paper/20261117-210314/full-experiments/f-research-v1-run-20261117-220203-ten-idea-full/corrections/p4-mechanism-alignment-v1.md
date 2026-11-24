# Correction: align full representations with frozen mechanisms

- Trigger: first P4 matrix showed DYN/DLY omitted the initial state from an otherwise lossless residual code; EQ/PERM used float32 despite exact certificate gates; POS used only uniform per-channel quantization although the proposed mechanism allows an 8-level per-channel codebook.
- Earliest affected stage: P2 shared experiment code.
- Repair: use initial+residual features, float64 rotation/permutation checks, and per-channel quantile codebook as the proposed POS variant while retaining raw/uniform/per-channel-uniform controls.
- Threshold change: none. All minimum/strong/failure gates remain exactly frozen.
- Preserved evidence: first-round outputs remain in `results/`; affected modules will be rerun and the final result manifest distinguishes superseded rounds.
- Falsifier: unit reconstruction tests, float64 exactness, and unchanged gate evaluation must pass.
