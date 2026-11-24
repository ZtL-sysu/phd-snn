# Correction: typed-coordinate sampling

- Trigger: P3 baseline execution crashed in `typed_coordinates()` because pandas `groupby.apply(...).join(frame)` created overlapping columns.
- Earliest affected stage: P2 reusable code/setup.
- Prior attempt: first baseline batch completed DYN, then EQ failed before producing an EQ result.
- Repair: use `groupby("type").sample(n=1000, random_state=17)` directly; no result or threshold changed.
- Falsifier: unit/import checks plus EQ baseline must load, split and fit without overlap.
- Cost: negligible CPU fix; rerun P2 checks and then baseline batches.
- Budget impact: none; failed partial batch is preserved in the console/audit record and DYN result is not silently overwritten.
