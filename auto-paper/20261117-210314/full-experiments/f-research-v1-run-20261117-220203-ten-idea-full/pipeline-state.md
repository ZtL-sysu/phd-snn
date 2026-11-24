# Pipeline State

## Run Boundary

- Guidance file: `../guidance.md`
- Guidance directory: `C:\code\phd-snn\auto-paper\20261117-210314\full-experiments`
- Run root: `f-research-v1-run-20261117-220203-ten-idea-full`
- Artifact manifest: `artifact-manifest.json` (to be populated)
- Final deliverable policy: one Chinese Markdown report requested by the user; no numeric page target
- Path-containment status: passed

| Stage | Name | Status | Evidence / artifact path | Gate result | Notes |
|---|---|---|---|---|---|
| P0 | Load guidance and create run root | passed | `audits/p0-gate-report.md` | pass | input hashes verified |
| P1 | Validate guidance | passed | `audits/p1-guidance-validation.md` | pass | ten-row contract extracted |
| P1A | Strong-result feasibility lock | passed | `strong-result-feasibility-lock.md` | pass | planned targets only |
| P1B | CCFA pre-experiment review/integrity | passed | `ccfa-pre-experiment-*.md` | pass | fatal risks routed |
| P2 | Protocol/environment setup | passed | `audits/p2-setup-check.md` | pass | RTX3060; 13/13 tests |
| P3 | Baseline-first execution | passed | `audits/p3-baseline-gate.md` | pass | ten baseline files |
| P3A | Baseline stop-loss review | passed | `ccfa-baseline-*` | pass | continue with SIGN risk |
| P4 | Full ten-module experiments | passed | `audits/p4-experiment-gate.md` | pass | SIGN strong-fail retained |
| P5 | Strong-result lock | passed | `strong-result-lock.md` | pass | report wording narrowed |
| P5A | Independent CCFA science/integrity review | passed | `ccfa-independent-review.md` | pass | independent agent |

P0–P5A passed in canonical order. P6–P21 are `superseded` by the user-authorized Markdown deliverable recorded in `deliverable-scope.md`; no manuscript/PDF stage is falsely marked complete.
