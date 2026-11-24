# P21 gate report

## Decision

**PASS.** The complete `deliverables/POS-C13-final-v2/` package is consistent and reproducible from its source archive.

## Checks

- Accepted TeX/BibTeX/figures match exactly across package, source archive and clean extraction.
- Package PDF is byte-identical to the accepted p19 PDF and is the only PDF in the package.
- Clean extraction compiles with `latexmk` return code 0; normalized PDF text matches exactly.
- Both PDFs have eight pages and embedded fonts.
- All 32 cited keys resolve to 32 BibTeX entries; no placeholders or uncited entries remain.
- Required paper, figure, audit, metadata, provenance and experiment artifacts are present.
- The earlier `POS-C13-final-v1` recovery package is preserved as incomplete negative bookkeeping and is not the delivery target.

Evidence: `audits/p21-delivery-verification.json` and `audits/p21-package-manifest-preacceptance.json`.
