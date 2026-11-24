# P8 reacceptance after P10 visual repair

## Trigger

P10 reviews found two visual-data/notation defects:

- Figure 1 used `dm_i` rather than the implemented residual coordinate `dr_i` and omitted the residual-magnitude factor in the score label.
- Figure 4 used the legacy Cora task-loss summary value `0.47 pp` rather than the auditable maximum three-seed-mean value `0.53 pp`, and its caption omitted the 3 pp reference explanation.

This changed P8 visual dependencies and triggered a recorded reopen of P8.

## Reacceptance decision

**PASS.** Figure 1 and Figure 4 were regenerated from deterministic source specifications, visually inspected, and rebound to the revised manuscript at P10.

| Check | Result |
|---|---|
| Figure 1 structured source updated | pass |
| Figure 1 notation matches `s_i=r_i^2 ||dz/dr_i||^2` | pass |
| Figure 4 task points use audited three-seed-mean maxima | pass |
| Figure 4 3 pp reference explained in manuscript caption | pass |
| Vector/raster exports regenerated | pass |
| Hash manifests regenerated | pass |
| Figures 2-3 unchanged and still valid | pass |

The original P8 gate and partial history remain preserved. This report supersedes only the stale visual hashes, not the scientific evidence or fallback authorization.
