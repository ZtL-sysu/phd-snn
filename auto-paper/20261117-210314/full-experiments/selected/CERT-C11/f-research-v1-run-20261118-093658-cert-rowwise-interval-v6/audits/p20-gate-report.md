# P20 gate report

## Decision

**PASS.** The final generic academic source, PDF and bibliography agree with the P12/P19-audited manuscript and metadata boundary.

## Checks

- Final source: `writing/p19-final-manuscript.md`, SHA-256 `a840044a7e3e52b789986d9b888a97eae8d21f7dbafb7a0edb8783270c3d6785`.
- Final export: `writing/p20-final-v1/stage-22/`.
- `latexmk` returned 0; PDF is 10 pages with embedded fonts.
- 40 cited keys match 40 BibTeX entries; no missing keys or PDF placeholders.
- Three complete figure captions and two complete table captions remain; manual caption paragraphs are zero.
- Unresolved author/journal/form metadata is explicitly recorded in `submission-constraints.md` and `manuscript-metadata.md`.
- Audit JSON: `writing/p20-final-v1/p20-final-audit.json`.
