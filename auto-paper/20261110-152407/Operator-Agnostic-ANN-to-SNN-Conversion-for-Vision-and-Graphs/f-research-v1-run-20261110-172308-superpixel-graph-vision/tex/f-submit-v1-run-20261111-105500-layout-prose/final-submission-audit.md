# S9 · Final Submission Audit

- Exact limits: body <= 8 pages; compiled PDF 7 pages including figures/tables; references on later pages excluded. PASS.
- Template: official author-kit `cvpr.sty`, `review` mode, double-blind anonymous author block with Paper ID placeholder. PASS (logged ruler deviation in `submission-profile.md`).
- Claim support: identity, redundancy, energy and frontier claims each trace to a table/figure and a result file. PASS.
- Structure and paragraph flow: six canonical sections, distinct Discussion role, no orphan or late-added claim. PASS.
- Protected content: all numbers from `numbers.tex`; E18 negative result, E12/E11 holdouts, fp32 gap retained. PASS.
- Declarations: none in manuscript; author-managed items listed in `../../../contracts/manuscript-metadata.md`. PASS.
- Figure/table/citation integrity: `latexmk -pdf` rc=0; 42 cited works, 23 in 2022--2026, no undefined citations, no duplicate keys/titles. PASS.
- Metadata: canonical title matches `main.tex`, PDF and metadata record; author data pending. PASS for local preparation.
- Source--PDF--package consistency: revised sources in `revised/`, compiled PDF rebuilt from them, `sources/` holds the untouched original snapshot. PASS.
- Pending (non-scientific, author-managed): real author names/order, Paper ID, OpenReview profiles, funding, data/code availability, generative-AI statement, compute-reporting form, ruler deviation confirmation, submission authorization. `submission_ready = false`.

**Continuation note:** a further contribution-led wording pass is applied afterwards with `scientific-paper-writing`; any manuscript text change after this audit invalidates the affected check, so the audit is re-run against the final PDF in `final-submission-audit-after-spw.md`.
