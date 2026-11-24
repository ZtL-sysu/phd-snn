# P21 gate report

## Decision

**PASS.** The CERT-C11 final package is internally consistent and reproducible from its source archive.

## Delivery checks

- Package: `deliverables/CERT-C11-final-v1/`.
- Required files include `paper.tex`, one `paper.pdf`, `references.bib`, three figures, source archive, experiment artifacts, pipeline ledgers, guidance/figure/reference/page audits, submission constraints and metadata.
- TeX, BibTeX and all three figures match exactly across accepted output, package, source archive and clean extraction.
- The accepted PDF package copy is byte-identical to `writing/p20-final-v1/stage-22/paper.pdf`, SHA-256 `f08e8e3d38dfa76e12fe493a4db295aea1e9b03b51327d526b887122d4e52f4e`.
- Clean extraction compiled with `latexmk` return code 0 and produced 10 pages.
- Normalized accepted/clean PDF text matches exactly; both PDFs have embedded fonts.
- All 40 cited keys resolve to 40 BibTeX entries; no PDF placeholders or uncited entries remain.
- The package contains exactly one PDF and every file is under the run root.

## Evidence

- `audits/p21-delivery-verification.json`.
- `audits/p21-package-manifest-preacceptance.json`, 29 pre-acceptance files.
- Source archive SHA-256: `fabbe8a1fff22e7d1865daab38bb06bc21e4cf601ffa7bfa9cc4071366563e89`.

## Post-acceptance refresh

After P21 is recorded and `pipeline_state.py --complete` passes, the package's `pipeline-state.md`/JSON will be refreshed and a final `manifest.json` plus `final-audit-note.md` will be generated. This refresh changes only mutable delivery bookkeeping.
