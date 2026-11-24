# Mechanism-level idea card (round 001 primary, C1)

Bottleneck: all existing evidence for the spiking-state gain comes from SYNTHETIC moving dots.
Mechanism: real optical flow frames -> measured ommatidium Voronoi sampling -> fixed FlyWire graph ->
LIF membrane state with homeostasis (or stateless control) -> Kenyon readout -> direction/speed-change label.
Assumptions: 8-frame clips retain visible motion after downsampling; labels are derivable without static leakage;
homeostasis keeps synaptic current bounded. Falsification: gain vanishes on real footage, or ceiling < 0.70.
Contribution type: external-validity / transferability verdict with mechanism decomposition.
Feasibility risks: real-flow-to-eye interface undefined (fixed in the query), remote clean environment
missing scipy/scikit-learn (fixed in the query), guardrail-4 framing risk (fixed by the verdict framing).
Decisive controls: stateless, A=0, degree-preserving null, frame-stacked ceiling, same-protocol SYNTHETIC domain,
one-factor removal ablations. Five seeds, bootstrap 95% CI, BH q=0.05.
The other four candidates C2-C5 stay in `candidate_pool` with their independent reviews.
