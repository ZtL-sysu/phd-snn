# P4 full-batch execution progress

- **Current phase:** Delivery
- **Status:** All stages complete; entrypoint and independent raw-artifact validation passed
- **Seeds:** 1, 2, 3, 4, 5
- **Durable checkpoint:** `/home/novix/workspace/project/result.json`
- **2026-11-07:** Restart-safe `experiment.py` skeleton and initial `result.json` written before environment probing.

## Active long-running processes

None.

## Key results

- Stage A complete: graph 130,391 nodes / 782,761 nnz; spectral radius 102.712294 -> 0.949999966.
- SYNTHETIC direction ceiling mean 0.998333; stateless/lif_homeostasis/lif_combo all 0.500000; degree-null LIF mean 0.703333; A=0 mean 0.891667 (5 seeds).
- SYNTHETIC flash ceiling 1.000000; stateless/lif_homeostasis/lif_combo all 0.500000; degree-null LIF mean 0.611667; A=0 mean 0.515000 (5 seeds).
- DAVIS acquired: 832,766,765-byte ZIP (SHA-256 `e3d0b5...aa492`), extracted 12,610 members; 728 dynamic clips (left 378/right 350), 727 annotation-derived and 1 frame-difference fallback.
- REAL ceiling mean 0.521461 < 0.70: protocol failure gate is active; no real-domain method or migration claim is permitted. Main means: stateless/homeostasis/combo 0.520548; degree-null 0.521461; A=0 0.536986.
- Paired bootstrap/FDR complete: homeostasis and combo deltas are exactly 0 in both domains; all BH-FDR rejections are false. Null-minus-biological delta: SYNTHETIC +0.203333 (95% CI [0.151667, 0.278333]); REAL +0.000913 (CI [-0.008219, 0.010046]).
- Migration verdict: `failure_real_ceiling_below_0.70_no_method_claim`; not evidence for transfer or synthetic specificity.
- Validation: 121 raw/evidence artifacts checked, 0 errors; `entrypoint.sh` exit 0; 4 invariant tests passed.
