# Handoff to f-research-v1

Recorded 2026-11-05 after `validate_guidance.py --strict --packet` returned
"Guidance structure is valid." and the ordered 12-stage ledger passed.

The guidance file is `guidance.md` in this run root; the CCFA startup packet is
`ccfa-startup-packet/` with `startup-decision.md = proceed`. The f-research-v1 run root is
`f-research-v1-run-20261105-111502-gnn2snn/` inside this directory, with its own P0-P21 ledger.

Binding decisions carried forward: independent third paper (A/B are anonymous companions, no
reused priority claim); C3 bound-derived latency allocation is the binding `expected_strong`;
six numbered main sections; no TODO tokens; >=36 citations with a strict 2023-2026 majority;
score >=9 measured only by `ccf-paper-reviewer` in full mode; no submission action.

The external index `auto-paper/generated-research-directions.md` received one new row for
`20261105-111502`. Local preparation only: `submission_ready` stays false with seven pending
author/production items in `contracts/delivery-readiness.json`.
