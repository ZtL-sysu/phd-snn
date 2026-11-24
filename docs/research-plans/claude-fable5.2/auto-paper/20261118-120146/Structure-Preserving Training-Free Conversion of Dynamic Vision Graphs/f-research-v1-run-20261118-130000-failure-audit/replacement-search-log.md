# Replacement search log — final update

| Candidate | Decision | Evidence |
|---|---|---|
| V2 message-aware calibration | rejected | Independent full review 3/10; feature/logit MSE controls tie it; frozen structure numbers irreproducible. |
| A. Layerwise thresholded delta inference on NTU-60 | rejected | MIT HF CSV mirror truncated by ellipsis; only one sequence analyzable; inactive fraction 2.6%-20.5%, below 80% gate. |
| B. Failure census | rejected as top-tier main paper | No new mechanism. |
| C. Fair energy comparison | rejected as main paper | Requires real target hardware and strong quantized baselines. |
| Fly-connectome idea bank | rejected | 0/9 ideas above threshold; best 6.3 with fatal venue-fit gate. |
| Bounded-staleness streaming GNN with residual debt | rejected | PyG/Ripple-style pilot: no speedup (all <1x), ~37.8% drift, no drift reduction over controls. See `residual-debt-pilot-decision.md`. |

## Current conclusion

All documented or newly surfaced replacement candidates failed hard gates under the original top-conference target and local resource envelope. The original manuscript is preserved only as a rejected diagnostic artifact. The target remains active and unlowered; a materially new method family, complete streaming-graph data, or target hardware would be required to continue.
