# Novelty and feasibility report (round 001, primary idea C1)

Novelty delta: versus 2610.10023 we add a real-optical-flow domain and a transferability verdict,
not static accuracy; versus 2604.04033 we do not re-ask whether topology wins, we ask whether a gain
measured on synthetic motion survives real footage; versus 2609.01330 we train a visual readout on a
behavioural task, not simulate neural orientation maps. The contribution type is a rigorous
external-validity / diagnostic result, which is distinct from the rejected topology-advantage axis.

Documented risk from the independent review: strict-idea-review guardrail 4 boundary hit, because
novelty concentrates on applying a validated mechanism to a new dataset. Mitigation, written into the
guidance as go-conditions: (1) fix the real-flow-to-ommatidium sampling and direction/speed label
derivation protocol in the query and run the real-domain ceiling first; (2) report the same-protocol
synthetic-versus-real comparison with 5 seeds, bootstrap CI and BH; (3) retain stateless, A=0 and
degree-preserving null controls and never claim a wiring advantage; (4) deliver a venue-valued
transferability verdict, i.e. whether the gain is specific to synthetic regular motion.

Feasibility: all data directly public and probed this session, local plus 4090 compute available and
authorised, prototype self-test passed, 5-seed statistical protocol and kill criteria preregistered.
The nine historical independent reviews scored 4.3-6.3; C1 scored 6.1 with GO as a relative
advancement recommendation, zero hard fatal gates, and three fixable serious risks. No score was
raised to reach any threshold because no idea-stage threshold exists.
