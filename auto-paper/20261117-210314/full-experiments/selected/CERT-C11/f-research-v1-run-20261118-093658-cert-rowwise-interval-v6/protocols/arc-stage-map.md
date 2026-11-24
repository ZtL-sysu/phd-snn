# ARC stage map

The final writing/export stages use the local AutoResearchClaw-compatible mapping recorded in prior runs:

| f-research stage | ARC stage |
|---|---|
| P6 | 16 `PAPER_OUTLINE` |
| P7 | 17 `PAPER_DRAFT` |
| P9 | 18 `PEER_REVIEW` |
| P10 | 19 `PAPER_REVISION` |
| P11 | 20 `QUALITY_GATE` |
| P13 | 22 `EXPORT_PUBLISH` |
| P14 | 23 `CITATION_VERIFY` |

P0-P5A are local evidence gates and do not require remote execution. Any adapter output must be checked against local raw results before acceptance.
