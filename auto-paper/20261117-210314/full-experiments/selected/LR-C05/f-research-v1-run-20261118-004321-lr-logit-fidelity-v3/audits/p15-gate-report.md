# P15 gate report

## Decision

**PASS.** The current exported TeX compiles cleanly to the required single final PDF.

## Compilation

| Check | Result |
|---|---|
| Compiler | `latexmk` 4.87 / pdfTeX |
| Return code | 0 |
| Output | `writing/arc-export-v1/stage-22/paper.pdf` |
| Pages | 10 |
| File size | 812,815 bytes |
| Undefined citations | 0 |
| Undefined references | 0 |
| LaTeX errors | 0 |
| Embedded fonts | pass |

## Source/output consistency

- `paper.tex` hash: `73b80a2dd38e726cd8fffb0059f47ec7aa613b0af0ec36423aa6adefaf77069e`
- `paper.pdf` hash: `f26ce0d6a1296bfe0659d9117aa540aa40410b86c5cf87509b851e5370072d98`
- `references.bib` hash: `348ce5f027b1def266c6fa38f61cb9d4f2d5c5b39bbd17c6ac4ffb8bdd0695ee`
- The PDF log records `Output written on paper.pdf (10 pages)`.
- PDF text contains all six canonical numbered sections and no unresolved markers.

The package remains a single final PDF; no alternate manuscript PDF is introduced.
