# Correction: top-two advanced indexing

- Trigger: READ baseline crashed in `top2_readout` because NumPy advanced indexing did not broadcast `(N,)` rows with `(N,2)` columns.
- Earliest affected stage: P2 shared utility.
- Repair: index with `rows[:, None]`; unit test already specifies the correct top-two shape/order.
- Result impact: no completed scientific result was accepted from the crashed READ run. Earlier unaffected module outputs are retained and will be hash-checked for reuse.
- Falsifier: `test_top2_readout_preserves_argmax` plus a three-class shape check must pass.
