# f-submit-v1 Pipeline State

Run root under `paper_dir`; original submission preserved read-only in `sources/`.

| Stage | Status | Evidence |
|---|---|---|
| `S0` | passed | sources/original-submitted.pdf, sources/main.tex |
| `S1` | passed | manuscript-module-map.md, narrative-consistency-map.md |
| `S1A` | passed | audits/s1a-scientific-review.md, audits/s1a-concern-to-action.md |
| `S2` | passed | submission-profile.md |
| `S3` | passed | audits/s3-candidate-search.md |
| `S4` | passed | comparator-literature-table.md |
| `S5` | passed | comparator-section-patterns.md |
| `S6` | passed | module-quality-review.md |
| `S7` | passed | revision-log.md, fix_layout.py |
| `S8` | passed | audits/s8-rescore.md |
| `S9` | passed | final-submission-audit.md |
| `S10` | passed | upload-map.md |

## Gate log

- `--before S1`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S1A`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S2`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S3`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S4`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S5`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S6`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S7`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S8`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S9`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--before S10`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 
- `--complete`: rc=0 — PASS: ordered local workflow evidence and readiness-record checks; 

`submission_ready = false` (author-managed facts pending). No upload performed.


## scientific-paper-writing pass

A second, contribution-led prose pass was applied after S0–S10 (`revise_spw.py`), followed by a full recompile, 7-page visual re-inspection, citation-gate re-binding and an S9 re-run (`final-submission-audit-after-spw.md`). `--complete` rc=0 again. No numeric value, citation, negative result or evidence boundary changed.
