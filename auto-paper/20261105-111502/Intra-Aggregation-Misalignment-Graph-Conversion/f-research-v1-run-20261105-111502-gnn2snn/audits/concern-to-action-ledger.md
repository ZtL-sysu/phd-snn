# Concern-to-action ledger (live)

Updated at each review gate. Status vocabulary: `open | in-progress | closed | blocked`.

| id | source | concern | severity | criterion | action | owner | stage | status |
|---|---|---|---|---|---|---|---|---|
| A1 | P1B E3 | C3 constants could be fitted post-hoc | major | soundness | freeze ε, held-out list, T grid and no-refit rule before measurement | f-research-v1 | P2 | closed in `registry/registry.md` |
| A2 | P1B E5 | three same-group manuscripts | major | ethics | anonymous companion citation + division-of-evidence paragraph + no reused "first" claim | writing | P7 | open (design decision taken 2026-11-05) |
| A3 | P1B E2 | TPP transplant as a straw man | moderate | soundness | re-implement from eq. (8)–(13), unit-test at T=8, log source diff | f-research-v1 | P4 | open |
| A4 | P1B E1 | external baseline protocol mismatch | moderate | evidence | compatibility column in Table 2 + 5-day stop-loss | f-research-v1 | P4 | open |
| A5 | P1B E6 | L=4 bound failure | moderate | soundness | pre-registered failure-depth condition; retain negative result | f-research-v1 | P4 | open |
| A6 | P1B | device-induced 0.69 pp drift | moderate | numeric | frozen device field + G0 <0.1 pp gate | f-research-v1 | P2 | **closed** — G0 PASS (Cora −0.003 pp, PubMed +0.000 pp on CPU); CPU frozen for paired arms, `protocols/protocol.md` §5 |
| A7 | G0 sweep | task book misstates ICML'25 T=4 numbers | moderate | integrity | primary-source-only quotation, recorded in parent `notes/G0_source_conflicts.md` | writing | P7 | closed (design) |
| A8 | G0 sweep | `SSEL` / `DRSGCN` unverifiable | minor | integrity | excluded from all tables | writing | P7 | closed (design) |
| A9 | red team F1 | no new capability → score stays 8 | **decisive** | significance | C3 bound-derived latency allocation as binding `expected_strong` | f-research-v1 | P4/P5 | open (the main risk) |
| A10 | red team F2 | same-group overlap | major | ethics | author decision + division of evidence | author + writing | P7 | closed at design stage |
| A11 | venue | 2027 CFPs unpublished | moderate | format | 8 pages recorded as a working assumption; re-verify when published | author | P20 | open |
| A12 | dependencies | AutoResearchClaw absent | moderate | process | local-executor substitutions with identical gates, recorded as substitutions | f-research-v1 | P6–P14 | closed (design) |
| A13 | data | heterophily duplicate nodes | moderate | validity | name version and de-duplication per arXiv:2302.11640 | f-research-v1 | P4 | open |
| A14 | budget | squirrel C3 cell may exceed runtime | moderate | evidence | one ANN per (graph,seed); `infeasible-with-evidence` with partial rows retained | f-research-v1 | P4 | closed (design) |

## Rules

- A concern requiring an experiment, correction, narrowed claim or guidance revision reopens the
  earliest affected stage and its downstream suffix; it is never deferred to P9 merely because
  drafting has begun.
- A closed design concern is not evidence. Only a logged run can close an evidence concern.
- Score-change conditions are recorded in the corresponding review reports; no acceptance
  probability is estimated.
