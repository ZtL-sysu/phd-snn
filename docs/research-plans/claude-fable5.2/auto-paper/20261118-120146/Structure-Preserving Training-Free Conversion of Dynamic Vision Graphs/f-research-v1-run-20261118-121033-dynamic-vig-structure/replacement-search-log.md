# Replacement search log — after independent 3/10 review

| Candidate | Decision | Evidence |
|---|---|---|
| V2 message-aware calibration | rejected | Strong-baseline audit showed feature-MSE and logit-MSE controls tie v2 exactly; frozen structure metrics were irreproducible; independent full review scored 3/10. |
| A. Layerwise thresholded delta inference | rejected at stage 1 | MIT-labeled NTU-60 CSV mirror is truncated with literal ellipses and unusable for training; the one analyzable sequence gives only 2.6%-20.5% inactive fractions, far below the 80% gate. Official ST-GCN weights require the separately licensed full NTU archive, which is not available in the run root. See `candidate-a-stage1-data-blocker.md` and `candidate-a-stage1-census.json`. |
| B. Failure census across visual graph families | rejected as top-tier main paper | Independent idea review: no new mechanism; prior records show applying methods to new models is not venue-valued without insight. |
| C. Fair SNN-vs-quantized-GNN energy | rejected as main paper | Independent idea review: needs real hardware and strong baselines (e.g., TopGQ); RTX3060 wall-clock cannot support neuromorphic energy claims. |
| Existing `fly-connectome-cvpr2027` ideas | rejected | Local strict review has 0/9 ideas above 8.0; best is 6.3 with a fatal venue-fit gate. See `C:\code\phd-snn\fly-connectome-cvpr2027\qualified-ideas.json`. |

## Current conclusion

The documented material set has no currently admissible top-conference-strength replacement that can be executed with the available direct data. The original reported V2 manuscript is preserved as a negative/internal-control result but must not be delivered as a top-tier paper. Do not lower the target; continue screening new evidence-backed directions or request only the material scope change necessary to access a real streaming graph dataset / target hardware.
