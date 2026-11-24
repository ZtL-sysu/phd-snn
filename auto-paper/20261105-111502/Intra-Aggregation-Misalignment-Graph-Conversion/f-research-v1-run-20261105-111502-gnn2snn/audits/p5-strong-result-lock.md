# P5 — strong-result lock (before writing)

The binding `expected_strong` is C3, the bound-derived latency allocation. Frozen quantities and
pass conditions are in `contracts/pre-registration-c3.md` (v1 + v3 + v4 corrections, all frozen
before execution).

| metric | observed | target |
|---|---|---|
| fitted constant c | -0.2198 | frozen before held-out |
| kappa / T_min correlation on fitted rows | 0.3876742024168812 | positive |
| held-out graphs passing | 1 / 2 | >= 3 |
| timestep saving | 50.0% | >= 25% |
| uniform-T budget | T = 8 | — |
| mean predicted T* | 4.0 | — |
| shuffled-kappa control strictly worse | True | True |
| **expected_strong verdict** | **False** | True |
| minimum verdict | True | True |

Per-graph held-out results: {"chameleon": {"status": "complete", "n": 2, "kappa_mean": 83.67778542856253, "out_of_calibration": false, "screening_predicted_reachable": true, "screening_actual_reachable": true, "screening_correct": true, "T_pred_mean": 4.0, "T_grid_min_mean": 2.0, "hit_rate": 1.0, "gap_at_pred_pp": 2.741228070175439, "max_gap_at_pred_pp": 3.28947368421052, "underprovisioned": 1}, "squirrel": {"status": "complete", "n": 7, "kappa_mean": 114.3536838536611, "out_of_calibration": false, "screening_predicted_reachable": true, "screening_actual_reachable": true, "screening_correct": true, "T_pred_mean": 4.0, "T_grid_min_mean": 2.2857142857142856, "hit_rate": 1.0, "gap_at_pred_pp": 0.17839989021545186, "max_gap_at_pred_pp": 1.4409221902017322, "underprovisioned": 0}, "ogbn-arxiv": {"status": "unreachable-with-evidence", "n": 0, "kappa_mean": 333.5921761240428, "out_of_calibration": true, "screening_predicted_reachable": false, "screening_actual_reachable": false, "screening_correct": true}}

All failed, partial and negative cells remain in `results/` and `registry/results.csv`. No target
was lowered, no number was invented, and no held-out result was used to re-fit c.
