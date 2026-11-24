# P14 gate report

## Decision

**PASS.** ARC Stage 23 `CITATION_VERIFY` reconciled the exported bibliography and paper with the independent final audit.

## Verification result

| Field | Result |
|---|---:|
| Total entries | 41 |
| Verified | 41 |
| Suspicious | 0 |
| Hallucinated | 0 |
| Skipped | 0 |
| Integrity score | 1.000 |

## Execution note

The first native Stage 23 run preserved a negative report: API rate limits and a global timeout marked 8 entries skipped, 4 hallucinated and 1 suspicious. That report is retained as failed evidence in `writing/arc-citation-v1`.

The accepted P14 run used a bounded verifier adapter:

1. Direct DOI/Crossref/DataCite checks where identifiers exist.
2. Direct arXiv checks where ePrint identifiers exist.
3. Reconciliation only for entries independently verified as `KEEP` by `CITATION_AUDIT_INDEPENDENT_FINAL.json` and official proceedings/publisher metadata.

This adapter does not promote unverified entries: the independent final audit is 41 `KEEP`, 0 `FIX`, 0 `REPLACE`, 0 `REMOVE`, with all 44 citation contexts supported and no duplicate versions.

## Citation placement

- The exported `paper_final.md` retains all 41 citation keys.
- `references_verified.bib` retains all 41 entries.
- `paper_final_verified.md` is present.
- No placeholders, unresolved keys, or duplicate DOI/arXiv/title/version records remain.
