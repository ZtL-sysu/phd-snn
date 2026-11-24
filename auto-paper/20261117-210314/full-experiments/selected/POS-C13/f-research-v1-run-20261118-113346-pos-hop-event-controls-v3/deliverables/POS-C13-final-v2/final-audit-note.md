# Final audit note

## Delivery status

The POS-C13 `f-research-v1` pipeline is complete through P21. The canonical run-root ledger passes `pipeline_state.py --complete`, and finalized state ledgers are included here.

## Verified artifacts

- `paper.tex` is the accepted generic source after P19 scope/format repairs.
- `paper.pdf` is the single accepted 8-page final PDF.
- `references.bib` contains 32 verified entries matching all 32 cited keys.
- Three figures and two tables have traceable source data and complete captions.
- `source-archive.zip` compiles after clean extraction; normalized text matches the accepted PDF.
- Accepted and clean-build PDFs have embedded fonts and no unresolved placeholders.

## Accepted result

- Hybrid representation error: 3.952% Chameleon, 4.879% Squirrel.
- Conservative storage reduction: 7.49× and 7.60×.
- Permutation maximum error: `2.22e-16`.
- Codec-consistent mismatched-shuffle ratios: mean 3.72×/3.63×, minimum 3.31×.
- Five-seed paired hybrid-minus-raw balanced accuracy: −0.083±1.197 pp and +0.768±1.017 pp.

## Preserved limitations

- Exact journal/author/form metadata is unresolved.
- Fixed-probe shuffle gaps are descriptive order-sensitivity evidence, not causal positional reasoning.
- The work does not claim general graph-transformer-to-SNN, temporal spike, energy, hardware or robustness performance.
- The first full-label probe run and incomplete `POS-C13-final-v1` recovery package remain negative bookkeeping and are excluded from accepted evidence.

## Bookkeeping

`manifest.json` is the final inventory and excludes only itself to avoid a circular self-hash. The earlier incomplete recovery package remains preserved outside the delivery target.
