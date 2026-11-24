# P13 generic export gate

## Decision

**PASS.** The final generic academic TeX/PDF/BibTeX export is `writing/p13-final-v4/stage-22/`.

## Checks

- Final `latexmk` return code: 0.
- Exactly six numbered body sections; References is unnumbered.
- Three figures and two tables are present in the PDF text.
- Bibliography command count is one and the final BibTeX has 40 entries.
- PDF text contains no `??` or `[?]`; all fonts are embedded.
- TeX SHA-256: `510276602e23b11ff07267f47619a9ef337bc8349dcd8653af872324a7c0f20c`.
- PDF SHA-256: `113daa0e9aa0b4af589944750ab7ec622bdd05ac30b3f5143294509d8ad1d8ab`.
- BibTeX SHA-256: `be176ede7327203c59bbb3ceaf0482853863064406964a0d744a73fdc4f0e6bb`.

## Preserved failures

- `writing/arc-export-v1/`: missing ARC required configuration fields.
- `writing/arc-export-v2/`: malformed generic TeX and compile failure.
- `writing/p13-final/`: stale auxiliary-file failure.
- `writing/p13-final-v2/`: Table 1 parser/TeX failure.
- `writing/arc-export-v3/` and `writing/p13-final-v3/`: intermediate exporter/section-numbering attempts.
