# Final audit note

## Delivery status

The LR-C05 `f-research-v1` pipeline is complete through P21. The canonical run-root ledger passes `pipeline_state.py --complete`, and the finalized `pipeline-state.md` and `pipeline-state.json` are included in this package.

## Verified artifacts

- `paper.tex` is the accepted generic academic source.
- `paper.pdf` is the single accepted 11-page final PDF.
- `references.bib` contains 41 verified entries and matches all 41 cited keys.
- Figures 1-4 match their accepted TeX-referenced PNG files.
- `source-archive.zip` contains the accepted TeX, bibliography, and figure paths needed for compilation.
- Clean extraction and independent `latexmk` compilation returned `0`; normalized extracted PDF text exactly matches the accepted PDF.
- Both accepted and clean-build PDFs have 11 pages and zero embedded-font failures.
- PDF text contains no `??` or `[?]` placeholders.

## Preserved limitations

- The exact journal, authors, affiliations, abstract/keyword/highlight limits, funding, data/code statement, declarations, and submission portal fields remain unresolved because no journal package or form was supplied.
- Figure 1 remains a user-authorized deterministic self-drawn fallback after repeated GPT image-generation service failures; this is disclosed in the figure contract and P8/P18 audits.
- Task superiority was not established. The paper reports bounded descriptive task degradation and explicitly preserves the negative message-MSE trade-off.
- The warmed runtime comparison is for rank128/1%, not the focal rank128/2% condition.

## Bookkeeping

`manifest.json` is the final package inventory and excludes only itself to avoid a circular self-hash. The immutable pre-acceptance inventory and full consistency output remain in the run root under `audits/`.
