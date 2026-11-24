# Independent red-team record (round 001)

Five independent `ccf-idea-reviewer standard` reports live in
`fly-connectome-cvpr2027/ideas/round-001/reviews/C1.md` through `C5.md`, with `scores.json` and
`SOURCE-NOTES.md`. Overall values: C1 6.1, C3 6.0, C4 5.8, C2 5.6, C5 5.6. `review_execution:
independent-agent`. No score was raised to meet any threshold; this round has no idea-stage threshold.

Three consistent concerns carried into the guidance as go-conditions:
(1) C1's real-flow interface and label derivation must be fixed in the query, with the real-domain
ceiling measured first; (2) the remote clean environment must list dependencies and must write
`experiment.py` plus a staged `result.json` before any early termination (task 17682 failed this way);
(3) the guardrail-4 framing boundary needs a venue-valued transferability verdict rather than a
plain re-test. All three are recorded, not waived.
