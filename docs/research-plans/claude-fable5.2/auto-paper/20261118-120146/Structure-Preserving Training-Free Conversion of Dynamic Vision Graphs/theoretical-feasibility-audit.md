# Theoretical feasibility audit

## Mechanism

Let node feature matrix `X` be encoded by a signed graded-pulse code `Q(X)` with maximum per-coordinate error bounded by `epsilon` on a calibration subset. A ViG-style Grapher computes distances from pairings such as `x_i - x_j`, selects the k nearest nodes, and applies channelwise max over signed neighbor messages. Both operators are discrete around ties:

- If `d_(k+1) - d_(k) <= 4 epsilon`, a feature perturbation can change the selected neighbor set.
- If two candidates for the signed max differ by at most `2 epsilon`, their winner can swap.
- A small feature error can therefore become a topology or winner error, while max itself is 1-Lipschitz conditional on the winner set.

The proposed method does not assume continuous error alone determines degradation. It calibrates coding thresholds/offsets to minimize structure disagreement on training data and evaluates structure restoration by oracle interventions.

## Learnability and implementation conditions

- The teacher is trained normally in FP32; conversion does not update teacher weights.
- Calibration updates only per-layer coding parameters using train/calibration examples.
- The Grapher operator is reimplemented from the paper-level description rather than copied from unlicensed code.
- Oracle interventions are diagnostic: teacher neighbor indices and winners are supplied only during analysis.

## Supporting evidence

- ViG primary record confirms dynamic kNN graph construction and Grapher/FFN design.
- DCGS primary record confirms differential coding and threshold iteration as a current training-free conversion route for CNN/ViT.
- The imported, separately audited materials document that existing graph-conversion attempts either fix the graph, retrain the source with special activations, or replace max pooling; they do not establish a prior solution to dynamic-kNN plus signed-max training-free conversion.
- The elementary distance/winner margin bounds are derived directly and do not depend on an unverified external claim.

## Falsifying ablation

1. Replace `Q(X)` with teacher `X` at each layer: structure disagreement must vanish. If not, the implementation is wrong or the claimed mechanism is not isolated.
2. Compare activation-MSE calibration with structure calibration at equal parameters/events: if activation-MSE matches or wins, the structure-specific mechanism is unsupported.
3. Restore teacher neighbors only, winners only, and both: if both-oracle fails to recover accuracy, structure disagreement does not explain accuracy loss.

## Failure mode for top-tier suitability

If conversion already yields near-perfect neighbor and winner agreement at T<=4 and small accuracy loss, no method story exists; the honest output is a negative diagnostic that likely eliminates the primary direction. If gains only appear with a deployable teacher oracle, the method is invalid. If the entire result depends on Fashion-MNIST toy structure, the paper must not claim general visual-graph conversion.

Gate verdict: `pass`. The mechanism is specific, assumptions are explicit, supporting primary records exist, and three falsifying ablations are defined.
