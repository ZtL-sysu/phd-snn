# Red-team review (independent, adversarial)

Readiness score: **4/10 as an A-venue submission today**, 7/10 as a B-venue paper. Confidence:
medium-high (the evidence is in hand; what is uncertain is how a reviewer weighs prediction against
benchmarking).

## Fatal risks

**F1 — "This is a diagnostic framework with a small effect, dressed up as a theory."**
The paper's strongest quantitative claims are about *its own* conversions: the exponent 0.948 is fit
to nine cells produced by one codebase. A reviewer will ask for out-of-sample prediction. Without a
held-out test the law is a curve fit.
*Condition to clear:* leave-one-configuration-out and leave-one-dataset-out prediction with stated
MAE, plus a pre-registered threshold the law must beat.

**F2 — "You never compare to a published method."** Still true in the current draft. Any A-venue
reviewer will ask. The answer cannot be a paragraph of framing; it has to be a table with the three
external arms over the full latency grid.
*Condition to clear:* an accuracy–T and an accuracy–SOP Pareto table with ≥3 external arms and a
clear statement of which are codebase reproductions and which are formulation re-implementations.

**F3 — "Your headline is a negative result, and negative results do not get in unless they overturn
a belief people hold."** Depth and energy are negative here. The belief they overturn — "deeper
GNNs convert fine, just needs more T" — is held, but the paper must show it is held, not assert it.
*Condition to clear:* state the belief, cite where it is implicitly assumed, and show the
counterexample with `G` and the measured exponent.

**F4 — "The order-invariance result is trivial."** It is one line once you write the accumulator
down. A reviewer may say "of course, the sum has no t".
*Condition to clear:* the point is not that the identity is hard but that the field's *terminology*
conflates the two phenomena. The 2×2 must carry the weight, and the paper must show a case where
the count decoder genuinely moves (it does, up to 1.6 pp).

## Serious risks

**F5 — Fitted constants that do not transfer.** If `‖E_1‖ = c√H/(2T)` needs a different `c` per
dataset, the "prediction" is a per-dataset calibration. Must report `c` per dataset and show it is
stable, or fit a single global `c` and accept the error.

**F6 — The ensemble (WP5) may fail.** If multi-view averaging does not beat the ANN, the paper has
no positive headline beyond fidelity. That is survivable (the prediction is the headline) but it
removes the most exciting sentence the draft could have. Do not plan the story around it.

**F7 — Compute honesty.** The predictive model needs many (dataset, L, H, T) cells. We have a 3060
and 12 CPU cores. If the grid is cut to fit the budget, the prediction test loses power and F1
returns.

## Score-change conditions

- +2 if F1 clears with MAE ≤ 1 pp on held-out cells and the required-T prediction is exact on ≥70 %
  of cells.
- +2 if F2 clears with a Pareto table where conversion is not dominated at T ≤ 4.
- +1 if F3 is framed as overturning a stated belief.
- −2 if any external arm is described as a codebase reproduction when it is a re-implementation.
- −1 if the paper claims energy savings anywhere.

## What I would tell the authors

The physics is real: an exact recursion, two measured exponents, and one clean invariance. What is
missing is not more theory, it is *out-of-sample prediction* and *an external anchor*. Do those two
and this becomes an A-venue paper, because "we can tell you before you run it" is a claim no
conversion paper currently makes.
