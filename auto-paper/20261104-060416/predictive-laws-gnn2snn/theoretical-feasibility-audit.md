# Theoretical feasibility audit

## Mechanism, stated as a causal chain

1. A converted layer receives, at step `t`, the term `(1−α)Â s_{l−1}(t) M_l` plus a constant. The
   *only* difference from the ANN is that `s_{l−1}(t)` is a binary sample whose time-average is a
   quantised rate, rather than the rate itself.
2. Summing over `t` is exact: the accumulator equals `Â(count_{l−1}M_l) + T·c_l`. So the conversion
   error is not a dynamics effect at all — it is the quantisation error of a rate, pushed through the
   same linear map the ANN uses.
3. That gives `B̂_l − B_l = (1−α)Â(E_{l−1}M_l)` with `E_0 = 0`, verified to `2×10⁻⁶` at L ∈ {2,3,4}.
4. Layer 1's error is the difference between a floor-quantised rate and its true value, per unit.
   Those errors are independent across units (different weights, different thresholds crossings), so
   `‖E_1‖` grows like `√H`, not like `H`. Measured: `‖E_1‖/√H = 1.724 … 1.614` over `H = 16…128`, a
   6.4 % spread.
5. Because the propagation is linear and `‖Â‖₂ ≤ 1`, the output error is `‖E_1‖` times a product of
   per-layer gains. Measured exponent 0.948 against `G` at `r = 0.990` over nine cells; the shortfall
   from 1.0 is the ReLU active-set mask clipping sign flips, which the norm bound cannot see.
6. A decision survives iff the perturbation is smaller than the margin. So accuracy is a monotone
   function of `√H·G/(T·Δ)`, and each factor is computable from the trained weights.

## Assumptions, and what each costs if false

| assumption | if false | test |
|---|---|---|
| No-leak IF, subtractive reset | the accumulator identity fails and the whole recursion changes | the identity residual itself; and the leak ablation in claim O |
| Layer-1 input is constant over `t` | `E_0 ≠ 0` and the first layer contributes error | architectural fact for rate-coded conversion; would need re-derivation for Poisson input coding |
| Quantisation errors independent across units | `‖E_1‖ ∝ H` instead of `√H`; the width conclusion inverts | the `√H` measurement, plus the shuffle ablation |
| Margins dominate the error (not the tails) | prediction of *aggregate* accuracy degrades at very low `T` where most nodes flip | report per-`T` residual; the predictor is only claimed where the flip rate is between 1 % and 50 % |

## Falsifying ablations (each one can kill a claim, by design)

- **Shuffle the per-unit quantisation errors** before propagating them. If the shuffled model predicts
  held-out gaps as well as the real one, then the specific structure `Â(E M)` carries no information
  and the mechanism is decorative. Success = shuffled MAE worse by ≥0.5 pp.
- **Gauge-normalise every layer** to unit spectral norm. If converted accuracy survives, the
  amplification claim is wrong. Measured: it does not survive (0.787 → 0.144 on Cora at T=8).
- **Leaky membrane readout.** If order still does not matter with decay ≠ 1, the invariance is a
  simulator artefact rather than a property of the sum readout.
- **Widen without bound.** If the fidelity gap does not eventually grow with `H`, the `√H` law is
  being masked by margin growth and the width recommendation must be conditioned.

## Failure mode that would make the project unsuitable for the tier

The predictor is fitted on our own codebase. If, across datasets, the constant `c` in
`‖E_1‖ ≈ c√H/(2T)` varies by more than ~20 %, then "prediction" means "prediction up to a per-dataset
calibration constant", which a reviewer will read as a fit. The audit therefore requires reporting `c`
per dataset *and* a pooled fit, and requires the leave-one-dataset-out test to be reported separately
from leave-one-config-out. If LODO fails while LOCO passes, the paper says exactly that and drops
"predictive" from the title.

## What would still be true even if prediction fails

The identity, the depth measurement (depth is unusable, G says by how much), the order-invariance
theorem, and the external Pareto. Those four survive independently, which is why the paper can lose
its title claim without losing its contribution.
