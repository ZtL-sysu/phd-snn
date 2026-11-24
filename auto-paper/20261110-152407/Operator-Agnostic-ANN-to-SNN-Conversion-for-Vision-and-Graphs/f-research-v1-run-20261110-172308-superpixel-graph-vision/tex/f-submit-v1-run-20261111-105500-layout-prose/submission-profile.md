# S2 · Submission Profile

- Field/topic: neuromorphic computing, ANN-to-SNN conversion, graph-structured vision.
- Target venue: CVPR main conference (user-specified official LaTeX author kit, double blind).
- Source: `../../../contracts/submission-constraints.md` (CVPR 2026 Author Guidelines + official author-kit template, verified 2026-11-10).
- Hard limits: body <= 8 pages including figures/tables; pages containing only cited references excluded; mandatory official template; anonymisation; English.
- Template: `cvpr.sty` (author-kit main branch, marked CVPR 2027), `\usepackage[review]{cvpr}`, `ieeenat_fullname.bst`.
- Declarations: author-managed; none inserted. No declaration change requested by the user.
- Metadata: `../../../contracts/manuscript-metadata.md`; author names, Paper ID, OpenReview profiles, funding, data/code availability, generative-AI statement and compute-reporting form remain pending.
- **Recorded deviation:** the author-kit review ruler writes `lineno` numbers into the two-column gutter, overlapping body text. With user instruction prioritising layout quality, line numbers are suppressed via `\AtBeginDocument{\nolinenumbers}` while the review header, confidentiality mark and double-blind author block are preserved. The LaTeX guide says the ruler "should be present"; this is a readability-driven, explicitly logged deviation to be confirmed by the author before submission. It is not a relaxation of template, page-limit or anonymity rules.
