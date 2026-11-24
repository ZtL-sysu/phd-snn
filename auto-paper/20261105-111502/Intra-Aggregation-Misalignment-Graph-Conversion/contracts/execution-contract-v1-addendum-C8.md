# Addendum to execution-contract-v1 — resolution of C8 and the ≥9 capability decision

Date: 2026-11-05. Contract v1 is **unchanged**; this addendum resolves the one item v1 explicitly
left to the author. No stage had been recorded `passed` at the time, so no downstream suffix needs
reopening. v1 and this addendum are bound together as the active contract input.

## Author decisions (2026-11-05, via structured question)

1. **Relation to companion Papers A/B → "independent third paper" (option 1).**
   The new manuscript is centred on the ICML'25 mechanism separation. A and B are cited as
   anonymous companions. The three papers declare a division of evidence; no paper's main claim
   depends on another's results. **The "first conversion-based SNN framework for graphs" priority
   claim is NOT reused.** It belongs to companion B and is attributed to it.
2. **Theorem G1(d) → per-layer latency allocation is AUTHORIZED as a main contribution** (option 1).
   From the L-layer closed form and its `T_L` dependence, predict each model's minimum `T*` for a
   target error, and validate the saved timesteps on held-out graphs. This is the binding
   `expected_strong` capability of the new paper and the intended +1 route over the companion's
   score of 8. It is a **new capability**, not a re-verification of a setting already in use.

## Consequent binding constraints

- `Core Idea` of `guidance.md`: the central claim is
  *"graph conversion error is generated inside a single neighbourhood aggregation, is deterministic
  and amplified by the adjacency row sum `ρ_n`; ICML'25 probabilistic neurons address a different
  (cross-layer, stochastic) phenomenon; an exact per-layer identity yields both a `ρ_n`-weighted
  L-layer bound and a bound-derived per-layer latency allocation that reaches a target accuracy
  with fewer timesteps on held-out graphs."*
- `planned_claim` and `observed_finding` remain distinct until P5A. The capability target is a
  **prediction to be falsified**, not a promised result. Its failure condition must be pre-registered.
- Expected score movement is not guaranteed. The score target ≥ 9 is measured only by
  `ccf-paper-reviewer` (`full` mode) at P9 and again at terminal review; if it is not reached,
  the autonomous correction loop applies (contract C2), never a manual score inflation.
- Related work must contain: the ICML'25 three-row contrast table, the explicit FTBC inheritance
  statement, and the anonymous companion division-of-evidence statement.
- No overlapping-submission assertion is made anywhere; `submission_ready` stays false.

## Updated input manifest binding

| file | role |
|---|---|
| `contracts/execution-contract-v1.md` | base contract (immutable) |
| `contracts/execution-contract-v1-addendum-C8.md` | this resolution |
| `notes/overlap-risk-AB.md` | evidence behind the decision |
