# Final audit note

## Delivery status

The CERT-C11 `f-research-v1` pipeline is complete through P21. The canonical run-root ledger passes `pipeline_state.py --complete`, and the finalized state ledgers are included in this package.

## Verified artifacts

- `paper.tex` is the accepted generic academic source after the five P19 style repairs.
- `paper.pdf` is the single accepted 10-page final PDF.
- `references.bib` contains 40 verified entries and matches all 40 cited keys.
- Figures 1-3 match their accepted TeX-referenced PNG files.
- `source-archive.zip` compiles after clean extraction; normalized extracted PDF text exactly matches the accepted PDF.
- Both accepted and clean-build PDFs have embedded fonts and no `??`/`[?]` placeholders.

## Preserved limitations

- The exact journal, authors, affiliations, abstract/keyword/highlight limits, funding, data/code statement, declarations and submission portal fields remain unresolved.
- Deterministic containment is a theorem/implementation audit, not statistical coverage.
- The empirical contribution is rowwise tightening over a matched global-radius ablation.
- Absolute width/RMS remains large: standard median 30.68 and maximum 36.91. This negative evidence rejects an absolute-width claim.
- The work does not claim temporal SNN, energy, hardware, robustness, learned-quantizer or multilayer generality.

## Bookkeeping

`manifest.json` is the final package inventory and excludes only itself to avoid a circular self-hash. The immutable pre-acceptance inventory and full consistency output remain in the run root under `audits/`.
