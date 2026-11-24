# P10 manuscript-lint disposition

The final lint report has zero integrity errors. Five candidate findings remain for human judgment and are dispositioned as follows.

| Rule/location | Candidate | Decision | Reason |
|---|---|---|---|
| W001, Abstract | “reported test” may look like a production marker | KEEP | It is the scientific split/provenance term required by the validation-exposure disclosure. |
| W004, Section 4.4 | Claim-strength check on selector-control comparison | KEEP | The paragraph explicitly says the comparison does not isolate a causal Jacobian contribution; wording is appropriately bounded. |
| W001, Section 4.5 | “method-dataset-seed p95” may look procedural | KEEP | It defines the experimental unit and p95 aggregation, not manuscript production. |
| W001, Figure 4 caption | Condition labels may look procedural | KEEP | The labels distinguish rank128/2% task/fidelity evidence from rank128/1% timing and are required for interpretation. |
| W001, visible-label audit | `Figure 4b: ...` may look procedural | KEEP | This is an external figure-label audit record, not manuscript text. |

No lint candidate was deleted automatically. No candidate contradicts the bound evidence or introduces a production/process narrative into the manuscript.
