# P19 selective style audit

## Diagnosis

The manuscript was scanned for AI-writing patterns: promotional language, vague attribution, filler transitions, rule-of-three padding, synonym cycling, em-dash overuse, empty meta-commentary, and unsupported rhetorical claims. The scan found no concrete stylistic defect requiring a rewrite. The prose is intentionally formal and evidence-led; repeated terms such as `matched total padded serialized-bit budget`, `maximum observed degradation`, and `held-out confirmation after validation exposure` are technical invariants rather than filler.

## Lint candidates

| Candidate | Location | Decision | Reason |
|---|---|---|---|
| W001 possible production marker | Abstract | KEEP | `reported test`, `rank128/1%`, and measurement boundaries are scientific provenance terms. |
| W004 claim-strength check | Random-projection validation diagnostic | KEEP | The paragraph explicitly limits random projection to validation and denies causal interpretation. |
| W004 claim-strength check | Selector-control comparison | KEEP | The paragraph explicitly states that no Jacobian-only interaction ablation was performed. |
| W001 possible production marker | Timing protocol | KEEP | Warmup/repeat/synchronization details are required reproducibility facts. |
| W001 possible production marker | Figure 4 caption | KEEP | The caption distinguishes the 3 pp reference and rank128/1% timing condition. |
| W001 figure-label candidate | External visible-label audit | KEEP | The label is an audit record, not manuscript prose. |

## Decision

No sentence was paraphrased. No scientific fact, number, condition, citation, or limitation was changed. P19 passes as a selective no-op polish after diagnosis.
