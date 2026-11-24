# S1A · Concern-to-Action Ledger

| Concern | Severity | Disposition | Owner | Unblock condition |
|---|---|---|---|---|
| Blue ruler numbers overlap body text | high (presentation) | rewrite layout (`fix_layout.py`) | S7 | visual re-inspection shows no overlap |
| Equation (5) exceeds column width | high | rewrap as aligned two-row equation | S7 | column-bound check |
| Four tables overflow / truncated exponents | high | resizebox + rebuild identity table | S7 | visual re-inspection |
| `pagebackref` digits in references | medium | remove option | S7 | visual re-inspection |
| Subsection headings wrap awkwardly | medium | shorten headings | S7 | visual re-inspection |
| Internal-target / defensive wording | medium | narrow or remove | S7 | prose lint |
| Screening-workflow narration in Discussion | medium | remove | S7 | prose lint |
| No new experiment or stronger attribution | hard constraint | retain | all | unchanged |
