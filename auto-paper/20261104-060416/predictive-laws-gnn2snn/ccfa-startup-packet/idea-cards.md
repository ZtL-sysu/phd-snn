# Idea cards — mechanism-level problem/method cards

Three cards were written before the literature map. Card B was the original plan; card A is the
one selected for guidance v4, because card B's decisive evidence (a cross-protocol benchmark)
depends on card A's machinery anyway and card B alone was judged incremental by the red team.

---

## Card A — selected

**Bottleneck.** Every ANN→SNN conversion paper reports accuracy only after running the spiking
simulation, and every design choice (depth, width, latency, sparsity) is therefore tuned by trial
and error. There is no way to say, for a *given trained network*, how faithful its conversion can
be or how many timesteps it will need, without converting it. Practitioners consequently pick
backbones for the ANN's accuracy, which — as we already measured — can make the converted network
worse.

**Mechanism (causal chain, not analogy).** The conversion error obeys an exact recursion
`B̂_l − B_l = (1−α)Â(E_{l−1}M_l)` with `E_0 = 0`. Taking norms gives
`‖E_L‖ ≲ ‖E_1‖·∏‖M_l‖₂`. The layer-1 error is a sum of independent per-unit quantisation errors,
so `‖E_1‖ ∝ √H_active/(2T)`. Therefore the whole conversion error is a *closed-form function of
three quantities that are read off the trained weights*: the cumulative spectral gain `G`, the
active width `H`, and the logit margin `Δ`. A decision survives when the error is small against the
margin, which turns fidelity into a computable probability rather than an experiment.

**Assumptions.** (i) No-leak IF with subtractive reset; (ii) constant-current input at layer 1;
(iii) per-unit quantisation errors approximately independent across units (falsifiable: it predicts
the √H law, which we already verified to 6 % over H = 16…128); (iii) the ReLU active set absorbs
sign flips, so the norm bound is conservative (measured: 0.95 exponent rather than 1.0).

**Falsification.** If, on held-out (dataset, depth, width, T) cells, the gap predicted from
`(G, H, Δ)` has MAE > 2 pp, or the required-T prediction is off by more than one grid step on more
than 30 % of cells, the mechanism is wrong and the paper falls back to a descriptive account.

**Contribution type.** Predictive theory + the method consequences it licenses (which backbones to
convert, how much latency, whether sparsity pays).

**Feasibility risks.** (a) `G` is a spectral norm of a trained matrix — cheap, exact, no risk.
(b) The margin model may need a per-node rather than global treatment; risk of a fitted constant
that does not transfer. Mitigated by leave-one-dataset-out fitting. (c) The prediction is about
*aggregate* accuracy, not per-node correctness; the per-node version is already in the shipped
margin-recovery theorem and is checked separately.

---

## Card B — rejected as the lead, retained as a section

**Bottleneck.** Conversion papers compare against each other across incompatible protocols, so no
one knows whether conversion or direct training is better at low latency.

**Mechanism.** Build one protocol, re-implement three published formulations, publish Pareto curves
in accuracy vs timesteps and accuracy vs synaptic operations.

**Why rejected as lead.** It is a benchmark, and benchmarks are incremental at an A venue unless
they overturn a belief. It survives inside card A as the external anchor that makes the predictive
claim credible (a law that only predicts our own re-implementations is not a law).

---

## Card C — rejected

**Bottleneck.** Conversion has no energy advantage.

**Mechanism.** Train the ANN under an activation-sparsity penalty, so the converted layer fires less.

**Why rejected.** We already ran the cheap version (post-hoc unit pruning) and the pre-registered
gate failed: `c < 0` units do not exist in sufficient number to matter, because spike count is set
by the *loud* units. A training-time penalty is the same trade-off with a different knob, and the
measured exchange rate (≈1 pp of accuracy for 40 % of spikes) makes an energy headline
unsupportable. Retained as a section: the exchange rate itself is a result, and the standard SOP
proxy does fall with width even when the spike count does not.
