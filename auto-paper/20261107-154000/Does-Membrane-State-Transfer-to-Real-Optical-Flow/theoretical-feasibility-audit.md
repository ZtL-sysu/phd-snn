# Theoretical / algorithm feasibility audit (round 001)

Causal mechanism: a stateless GNN applies `tanh(A x)` independently per frame; its readout average
is time-permutation-invariant for the label, so a direction label needs a comparison between frames.
LIF keeps `v_t = decay * v_{t-1} + syn(spikes_{t-1}) + drive_t`, so its state carries a decaying
trace of earlier frames and can serve as a sufficient statistic for short-horizon direction.
Measured locally on SYNTHETIC data: Kenyon feature std rises from 8.1e-05 (stateless) to 5.0e-03
(LIF plus homeostasis), and accuracy from 0.458 to 0.740.

Assumptions: (i) the real-flow sequence can be reduced to 8-frame clips at a sampling rate where
motion is still visible after 32x32 downsampling and ommatidium Voronoi sampling; (ii) the direction
or speed-change label can be derived from the clip without leaking static appearance;
(iii) synaptic current crosses the firing threshold without diverging, which requires homeostasis;
(iv) the readout retains enough signal-to-noise after propagation. Assumption (i) and (ii) are NEW
for this round and are the main falsification points, which is why the query fixes the derivation
protocol and requires a real-domain ceiling before any method claim.

Falsifying ablations: stateless (no state), A=0 (no propagation), the same-protocol SYNTHETIC domain
(if the gain is specific to regular synthetic motion), one-factor removal of each added mechanism,
sign shuffle, and degree-preserving null. If any of these erase the predicted pattern, the mechanism
story fails and the transferability verdict is reported as a negative result.

Tier failure mode: if the real-domain ceiling is below 0.70, or the gain appears only on synthetic
motion, the honest outcome is a diagnostic transferability note rather than a strong method paper;
that outcome still has value and must not be rewritten into a positive finding.
