# Theoretical feasibility audit

## The causal / algorithmic mechanism

A graph layer computes a sum over neighbours. Under rate-coded conversion, neighbour `j` delivers
its contribution at a time determined by its own quantized activation, so the receiving unit sees
a **locally time-scrambled, per-node quantized rate** rather than the ANN's simultaneous sum.
Writing the accumulated pre-activation error `E_{l-1}` through the normalized aggregation `Â`
gives the exact identity

`B_hat_l − B_l = (1 − α) Â (E_{l−1} M_l)`

for every layer. Three consequences are mechanical, not empirical:

1. `Â` is inside the error, so its row sum `ρ_n` and the neighbourhood geometry multiply the
   per-hop error. A bound of the image-domain form `‖W‖∞·θ/T` cannot express this.
2. The error has a **deterministic systematic component** from the quantization floor, cancelled
   by a closed-form forward bias `β* = θ/(2T)` weighted by `ρ_n`. Without it, the system term
   accumulates linearly in `ρ_n`. This is why changing the neuron's firing-time randomness (TPP)
   cannot fix it.
3. Because the identity is exact, the L-layer recursion can be unrolled into a closed form with an
   explicit `T_L` dependence. That closed form is **invertible**: given a target error and the
   trained weights, it predicts a minimum timestep `T*` and a per-layer allocation.

This is a mechanism-level reason to expect the method to work on graphs specifically: no other
setting puts a linear multi-agent aggregation operator between two spiking layers.

## Required assumptions

- Bounded, clipped activations with a fixed absolute threshold scale; ReLU homogeneity.
- A fixed normalized aggregation matrix `Â` with known row sums; static graph, no test-time
  adaptation of edges.
- Shared ANN/SNN weights, rate coding, and an IF or TPP neuron model whose expected rate matches.
- The margin/activation-mass proxy used by the `T*` inversion is computable from the trained ANN
  alone, without running a spiking simulation.
- Early stopping on validation only; device fixed per paired arm so sparse-reduction order does not
  change the model being converted.

## Supporting literature and prior measurements

- ICML 2025 (arXiv:2502.14487) Theorem 1 (a)–(d): expectation identities for probabilistic
  spiking and the layerwise `‖W‖∞·θ/T` bound. Verified against the arXiv HTML full text.
- FTBC (ECCV 2024, arXiv:2403.18388): forward-only temporal bias zeroes the **expected** error per
  timestep in CNNs. Our bias mechanism is inherited; the graph-specific `ρ_n` value and
  `ρ`-invariance are this project's contribution, and the attribution must be explicit.
- Companion project measurements, reaccepted as external calibration evidence (commit `d125112`,
  hashes to be bound at P1A): per-layer identity numerical residual ≤ 2e-6;
  `‖E_L‖/‖E_1‖ ∝ G^0.948` with r = 0.990 over 9 cells; L=2 closed form agreeing with simulation
  to 0.08 pp over 105 cells; L=3 closed form failing by 3.53 pp because reset makes intermediate
  **counts** depend on arrival order even though the output membrane does not; a four-layer loss of
  21 pp at T=8; an earlier latency bound conservative by 3.2–6.7×.
- Task-book §2 frozen numbers: T=4 gaps 1.17 / 1.02 / 0.18 pp and graph-dependent minimum T,
  which is the calibration for expecting a uniform-T budget to be wasteful.

These are **calibration evidence**, not results of this run. The new theorem, its counterexample
search and the `T*` inversion must be produced and verified here.

## Falsifying ablations

| ablation | what it kills |
|---|---|
| 2×2 crossed probe (inter-layer permutation × intra-aggregation phase randomisation) | the claim that the two misalignments are distinct |
| Four-way neuron control (IF / IF+`β*` / TPP / TPP+`β*`) | the claim that stochasticity cannot remove the systematic term |
| `β*` removal and spectral-norm-constrained training | the claim that the bias term is mandatory and cannot be normalised away |
| L ∈ {2,3,4} counterexample grid | the L-layer bound |
| Shuffled-`ρ_n` control | the claim that the geometric term, not a generic constant, drives `T*` |
| Matched uniform-T budget control | the claim that allocation, not spending, causes the saving |
| Held-out graphs with constants frozen before measurement | the claim that `T*` is predictive rather than fitted |

## Critical failure modes

1. **Loose but true bound.** A conservatism ratio above 20× makes the inversion useless even with
   zero violations. Pre-registered failure at C2; the honest fallback is an empirical
   characterisation with a stated depth boundary.
2. **L=3 reset path-dependence.** The companion showed the L=2 closed form fails at L=3 because
   intermediate spike counts depend on arrival order. The L-layer bound must be stated for the
   **membrane readout** (which is order-invariant) rather than for intermediate counts, or it will
   be false. This is the single most likely theoretical failure and is checked first.
3. **Under-provisioned `T*` on an unseen graph.** A prediction that misses by more than 2× the
   noise floor falsifies the capability. No held-out result may be used to re-fit a constant.
4. **Gauge/normalisation trap.** ReLU homogeneity allows weight renormalisation at zero ANN cost,
   but the IF threshold is an absolute scale; renormalising weights alone silences neurons. Any
   bound that ignores this will produce vacuous counterexamples.
5. **Device-induced drift.** CUDA can change early stopping by 0.69 pp; a bound fitted on one
   device and tested on another would appear violated. Device is frozen.

## Verdict

The mechanism has a concrete algebraic form, named assumptions, supporting measurements and five
independent falsifiers. A theory-only story was explicitly rejected because it would repeat the
companion's "no new capability" problem; the theorem is therefore tied to the `T*` capability.
G3 passes; the proof itself is P4 work with the prototype residual check at ≤ 1e-5.
