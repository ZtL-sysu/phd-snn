# P15 clean build gate

**PASS.** A clean directory containing only the accepted TeX, BibTeX and referenced PNG figures compiled with `latexmk` return code 0.

- Clean PDF: 11 pages.
- Normalized extracted text exactly matches the accepted PDF.
- All fonts are embedded.
- PDF text has no `??` or `[?]`.
- Binary PDF hashes may differ because PDF creation timestamps differ; text, page count and font checks are identical.

Machine record: `results/p15-clean-build.json`.
