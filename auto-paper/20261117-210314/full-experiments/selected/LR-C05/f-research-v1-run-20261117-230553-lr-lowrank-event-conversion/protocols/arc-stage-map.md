# Verified AutoResearchClaw stage map

Local checkout: AutoResearchClaw commit `84dad0a401404739cfcc47851cd1d282b671bb2f`.

| f-research stage | ARC stage ID/name | Verified implementation |
|---|---|---|
| P6 | 16 `PAPER_OUTLINE` | `pipeline/stages.py`, `_paper_writing.py` |
| P7 | 17 `PAPER_DRAFT` | `pipeline/stages.py`, `_paper_writing.py` |
| P9 | 18 `PEER_REVIEW` | `pipeline/stages.py`, `pipeline/executor.py` |
| P10 | 19 `PAPER_REVISION` | `pipeline/stages.py`, `pipeline/executor.py` |
| P11 | 20 `QUALITY_GATE` | `pipeline/stages.py`, `pipeline/executor.py` |
| P13 | 22 `EXPORT_PUBLISH` | `pipeline/stages.py`, `pipeline/executor.py` |
| P14 | 23 `CITATION_VERIFY` | `pipeline/stages.py`, `pipeline/executor.py` |

CLI supports `researchclaw run --config ... --output ... --from-stage PAPER_OUTLINE --to-stage ...`. The run-local config names `DEEPSEEK_API_KEY` by environment variable and contains no credential. Actual provider/model usage is recorded from executor responses before any stage is marked passed.
