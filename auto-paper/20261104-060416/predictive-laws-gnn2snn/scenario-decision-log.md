# Scenario decision log

Three scenarios were carried into the gates. Only one reached G8 as `proceed`. The user fixed the
technique (GNN→SNN conversion) so scenarios differ in *what the paper claims*, not in what it builds.

| # | scenario | G0 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | **Predictive laws**: fidelity is computable from trained weights | pass | pass | pass | pass | pass | pass | pass | pass | pass | **selected** |
| S2 | Benchmark: one protocol, three published methods, Pareto curves | pass | pass | pass | weak | **fail** | pass | pass | pass | fail | rejected as lead |
| S3 | Energy: sparse conversion beats trained spiking nets on SOPs | pass | pass | pass | weak | pass | pass | pass | **fail** | fail | rejected |

## S2 — why rejected as the lead

G4 fails: a cross-protocol benchmark is not a new contribution at an A venue unless it overturns a
belief, and our own measurements already show the published architecture beating us on two graphs, so
the benchmark would mostly report that the field is incomparable. G8 fails for the same reason — a
skeptical reviewer asks "what do I now know that I did not", and "these numbers are not comparable"
is not an answer. **Retained inside S1** as the external anchor, where it does real work: a law that
only predicts our own re-implementations is not a law.

## S3 — why rejected

G7 fails on measured evidence rather than on principle. Post-hoc pruning at 50 % of hidden units cuts
spikes by 23–36 % at ≤0.5 pp on the three graphs, and reaching a 40 % cut costs about a full point.
The pre-registered gate (40 % at ≤0.3 pp) fails on all three. A paper whose headline is an energy win
would be reporting a number we do not have. **Retained inside S1** as an exchange-rate measurement,
with the honest caveat that synaptic operations do fall with width even when spikes do not.

## S1 — why selected

It passes every gate, and it is the only scenario that satisfies the red team's two score-change
conditions: out-of-sample prediction (+2) and an external Pareto anchor (+2). Its weakness is
recorded rather than hidden: if prediction MAE exceeds 2 pp the title claim collapses to a
descriptive account, and the guidance states that failure signal in advance so the decision cannot be
made after seeing the numbers.

## Revisit history

S2 was revisited once, after the depth law was measured, on the hypothesis that "depth does not
survive conversion" could itself be the headline contribution. It was folded into S1 instead, because
a negative depth result *plus* the gain that predicts it is a law, whereas the negative result alone
is a warning. No gate was marked passed on stale evidence during either visit.
