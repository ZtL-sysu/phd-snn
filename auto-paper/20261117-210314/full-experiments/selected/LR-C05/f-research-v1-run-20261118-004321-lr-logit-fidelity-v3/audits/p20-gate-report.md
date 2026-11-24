# P20 gate report

## Decision

**PASS.** The accepted guidance-complete source was converted to the generic academic template, compiled cleanly, and retained the audited numerical evidence.

## Checks

- Canonical source: `writing/p17/paper-guidance-complete.md`, SHA-256 `e411d0692420f25fde23d1eb0978fdb8e5e3b0ef7fbbf429ab7edd3ee76ff1fe`.
- Final export: `writing/p20-final-v2/stage-22/paper.tex`, `paper.pdf`, and `references.bib`.
- Template: generic academic `article`; no unavailable journal-specific template or form was invented.
- The three evidence tables from P17 are present in the final TeX with their audited logit-MSE, message-MSE, hidden-MSE, task-loss, coefficient-count, adapted-control, and exact-bit values.
- The P12/P17 independent audited-value reconciliation adapter was used because ARC's local paper-verifier fixture did not contain the complete result tables. The adapter preserved the audited values instead of substituting fixture placeholders.
- Final `latexmk` returned `0`; the final PDF is 11 pages with no undefined citations and no embedded-font failures.
- Final TeX SHA-256: `c5729cfd8e0e99910a93eaedc9f90cfa3e92ab4996753e33a57d4eee9c3ddcbf`.
- Final PDF SHA-256: `1b492d599edb67314af1fa6369e95d06e2fecc9ffade67fe6cdd920cc9461d73`.
- Final bibliography SHA-256: `348ce5f027b1def266c6fa38f61cb9d4f2d5c5b39bbd17c6ac4ffb8bdd0695ee`.

## Metadata boundary

The exact journal, authors, affiliations, abstract/keyword/highlight limits, funding, data/code statement, declarations, and portal fields remain unresolved because no target journal package or submission form was supplied. These limitations are recorded in `submission-constraints.md` and `manuscript-metadata.md`; they are not treated as silently passing journal-specific requirements.

## Reacceptance note

`page-count-audit.md` preserves the P16 acceptance of the earlier 10-page export. The final 11-page P20 export is recorded separately in `page-count-audit-final.md`; the final package will use that current audit under the canonical delivery filename.
