# S9 (re-run) · Final Submission Audit After scientific-paper-writing

Generated 2026-11-11T11:17:35.206285. Re-run because the SPW prose pass changed manuscript text, which invalidates affected checks.

- Compile: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` rc=0; `revised/main.pdf` 7 pages (CVPR <= 8). PASS
- Visual inspection: all 7 pages rendered at 110 dpi and inspected in `visual/round3/`; `visual/final-page-1.png` compared byte-for-byte with the already-verified round-2 page 1. No overlapping ruler numbers, no column overflow, no truncated table cells, no stray backref digits, no duplicated sentences. PASS
- Equations: Eq. (5) rewrapped into two aligned rows inside the column. PASS
- Tables: all four inside their columns; identity residual exponents rendered as $4.88\times10^{-15}$ -- $1.38\times10^{-14}$. PASS
- Figure placement: two figures in one column, captions legible, no overlap; recorded as an accepted two-column layout choice. PASS (with note)
- Citation gate re-bound to the current manuscript: verdict `pass`, 42 distinct cited sources, 23 in 2022--2026, 0 undefined citations, 0 duplicates. PASS
- `--complete`: rc=0. `--submission-ready`: rc=1 (expected; `submission_ready=false`). PASS
- Protected facts: every numeric value remains a macro in `revised/numbers.tex`; no citation key removed; E18 negative result, all four holdout groups, fp32 gap, 45 nm theoretical-energy label and teacher-accuracy boundary retained. PASS
- Declarations: none inserted; author-managed items still pending. PASS
- Logged deviation: review ruler line numbers suppressed for readability (see `submission-profile.md`); review header, confidentiality mark and anonymous author block preserved. Author should confirm before submission.

Remaining non-scientific pending items: author names/order, affiliations, Paper ID, OpenReview profiles, funding, data/code availability, generative-AI statement, compute-reporting form, ruler-deviation confirmation, submission authorization. `submission_ready=false`; no upload performed.
