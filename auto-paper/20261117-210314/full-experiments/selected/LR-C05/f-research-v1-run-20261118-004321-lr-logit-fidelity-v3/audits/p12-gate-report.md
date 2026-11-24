# P12 gate report

## Decision

**PASS.** The corrected bibliography and manuscript placement meet the required 36-reference gate.

## Reference gate

| Requirement | Result |
|---|---|
| At least 36 unique verified references | 41 |
| Majority from 2022-2026 | 30 |
| Every bibliography key cited | 41/41 |
| Every citation key present in bibliography | 41/41 |
| Citation occurrences reviewed | 44 |
| Context-appropriate uses | 44/44 |
| Duplicate DOI groups | 0 |
| Duplicate arXiv groups | 0 |
| Duplicate normalized titles | 0 |
| Duplicate preprint/published versions | 0 |

## Verification

- Programmatic discovery and metadata verification used arXiv API, Crossref, OpenAlex, and official proceedings/publisher records.
- Independent first-pass citation audit identified 13 metadata/version issues.
- All 13 issues were corrected: author names, publication venues, years, page ranges, title, and accepted author lists.
- Independent re-audit returned `PASS` with 41 `KEEP`, 0 `FIX`, 0 `REPLACE`, 0 `REMOVE`.
- A final metadata-only recheck confirmed the `Low-Power Computer Vision` container/publisher and conference issue-field cleanup.
- `bibtex` parsed all 41 entries with exit code 0 and zero warnings.

## Scope corrections

- ASGCN is positioned as asynchronous event-based visual processing, not graph-message conversion.
- The unverified DCGS reference was removed.
- Published versions were preferred where verified; arXiv identifiers were retained only as secondary identifiers where appropriate.

## Artifacts

- `references.bib`
- `reference-coverage.csv`
- `reference-dedup-audit.md`
- `CITATION_AUDIT.md`
- `CITATION_AUDIT.json`
- `CITATION_AUDIT_INDEPENDENT_FINAL.md`
- `CITATION_AUDIT_INDEPENDENT_FINAL.json`
- `writing/p12/paper-with-verified-references.md`
