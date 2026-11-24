# Structure-number reconciliation

## Bottom line

The manuscript's `Jaccard 0.065 / winner agreement 0.488` and `p4-method-oracle-results.json`'s `neighbor_jaccard 0.758 / winner_agreement 0.630` are **not two measurements of the same quantity**. They must not be placed in one table without renaming or recomputation. The `0.065` is a correct rounded mean of `frozen-test-results.json` (0.065031), but the `0.488` is not: that file gives 0.481972 (0.482) for signed-uniform winner agreement.

Use two separately labelled quantities:

- **True Jaccard**, `mean_i |N_teacher(i) ∩ N_code(i)| / |N_teacher(i) ∪ N_code(i)|`: use the `frozen-test-results.json` protocol (0.065 / **0.482** for signed-uniform, 0.081 / 0.521 for signed-multilevel). Its current implementation must be fixed as described below.
- **Overlap@k**, `mean_i |N_teacher(i) ∩ N_code(i)| / k`: use the P4 protocol (0.758 / 0.630). Rename `neighbor_jaccard` to `neighbor_overlap_at_k` wherever this file is cited.

Never write `0.758` as Jaccard. Never compare `0.065` directly with `0.758`. Never write `0.488` as the mean winner agreement from `frozen-test-results.json`.

## Exact causes

1. **Different denominator / metric definition.** `frozen_test.py` computes set Jaccard with union denominator. `p4_method_oracle.py` computes
   `len(set(teacher_indices[i]) & set(indices[i])) / 9`, i.e. overlap@k. Our recomputation on the same learned embeddings and scale-9 uniform code gives true Jaccard 0.790 and overlap@k 0.867 on average across seeds 41/42/43, reproducing the P4 winner agreement exactly. The two metrics differ by construction.

2. **Different feature tensor.** `frozen_test.py` compares true-Jaccard structure of signed-uniform codes of the **normalized learned Grapher embedding** (`F.normalize(F.relu(model.embed(patches)))`), with self-masked top-k teacher neighbors. `baseline-structure-results.json` compares structure of codes built from **raw 4×4 pixel patches** using position-regularized `knn_indices`. Our audit recomputes the raw-patch variant at 0.542 true Jaccard / 0.607 overlap@k / 0.317 winner agreement, showing that source features alone change the values substantially.

3. **Different encoder.** The 0.065 / 0.482 pair is from `signed_uniform` coding at 16 levels on learned embeddings; the P4 0.758 / 0.630 pair is from a winner-agreement-selected uniform scale (9.0) on learned embeddings. Their winner agreements differ because their encoders differ. Repeating the P4 scale-9 path with the code path used in `frozen_test.py` gives mean winner agreement 0.630, confirming P4's number is internally consistent.

4. **A latent implementation bug in `frozen_test.py` makes the reported frozen numbers untrustworthy.** It builds `teacher_winners` from `model(images)`'s internal top-k graph, but builds the comparison codes with `matrix_winners(codes, matrix_knn_indices(codes))`. Our strict line-for-line re-execution gave 0.805 / 0.660 for signed-uniform, not the stored 0.062 / 0.478 per-seed values (0.065 / 0.482 mean). The exact historical numbers are not reproducible from the saved checkpoints and current source. In addition, `frozen_test.py` computes `agreement` by stacking already-misaligned winner tensors. The paper must either (a) re-run a corrected frozen test and use the new values, or (b) explicitly label these as historical, non-reproducible diagnostics and remove them from quantitative claims.

## Recommended numbers

- The **P4 oracle table** is reliable for internally consistent structure diagnostics when its metric is renamed to overlap@k: 0.758 overlap@k and 0.630 winner agreement.
- The **frozen-test 0.065 / 0.482** (and the manuscript's 0.488) should not be used as current evidence. Its source implementation is not reproducible and mixes teacher-graph and converted-graph winner conventions.
- For a corrected manuscript table, report both `true_jaccard` and `overlap_at_k`, with the feature source and encoder stated in the caption. `structure-number-audit.json` provides reproducible learned-embedding values from the saved checkpoints.

## Reproducibility note

The audit script initially failed with: (1) unpacking two loader return values into three; (2) flattening the wrong tensor axis when converting top-k indices to Python sets. These failures were corrected; no protected artifact was modified. Final audit: `structure-number-audit.json`.
