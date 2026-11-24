# P21 gate report

## Decision

**PASS.** The LR-C05 final delivery package is internally consistent with the accepted P20 source and PDF, and the source archive compiles successfully after clean extraction.

## Delivery package

- Canonical package: `deliverables/LR-C05-final-v1/`.
- Required manuscript files: `paper.tex`, one `paper.pdf`, and `references.bib`.
- Required figure files: Figure 1 plus Figures 2-4 at the exact `includegraphics` paths used by the TeX source.
- Required audits: `paper-guidance-audit.md`, `figure-table-insertion-audit.md`, `reference-dedup-audit.md`, `page-count-audit.md`, `citation-audit.md`, `submission-constraints.md`, and `manuscript-metadata.md`.
- Traceability and evidence: `experiment-traceability.md` and eight frozen experiment artifacts covering confirmation rows, adapted controls, task loss, exact bits, timing, validation sensitivity, and the evidence manifest.
- Source archive: `source-archive.zip`, SHA-256 `b55904992e10f7d91f377b22d02b487856ff04fa0de1c720e3dbcf01b21d28e4`.

## Consistency and clean-build checks

- `paper.tex`, `references.bib`, and all four TeX-referenced PNG figures match exactly across the accepted P20 export, package copies, source-archive entries, and clean extraction.
- The accepted PDF package copy is byte-identical to `writing/p20-final-v2/stage-22/paper.pdf`, SHA-256 `1b492d599edb67314af1fa6369e95d06e2fecc9ffade67fe6cdd920cc9461d73`.
- The source archive was extracted to `writing/p21-clean-extraction-v1/`; clean `latexmk` returned `0` and produced an 11-page PDF.
- Accepted and clean-build PDF binary hashes differ only because the PDF creation timestamp differs. Normalized layout-preserving extracted text is exactly identical, with SHA-256 `104aa289354477fe848885f654202d6dce109850f576198e5ef76535a885107c`.
- Both PDFs have 11 pages and zero embedded-font failures.
- The bibliography contains 41 entries, the TeX cites 41 unique keys, and there are no uncited entries or missing bibliography keys.
- PDF text contains Conclusion and References and contains neither `??` nor `[?]`.
- Every package file is under the LR-C05 run root; the pre-acceptance manifest contains 25 files and verifies path containment.

## Evidence hashes

- `audits/p21-delivery-verification.json`: `b46d026c82d3e39a8bfaa801a4c1112d9e514bd7c47db8d4af265087d79ddd5e`.
- `audits/p21-package-manifest-preacceptance.json`: `6f3f635c57f0f6a22b623eab2212a7486be11aa7e1acde385ef7b8e7ff3b50fb`.
- `research/p21_verify_delivery.py`: `25a6a49413e1d5e05b3096c496a2f567da5b64bf9d380769c07ec5e1a488c1da`.
- Clean-build log: `6d7788f1e0fd5a8223e4cc5b2cc2fba95734c075250e1feccfde978fb5623758`.

## Post-acceptance state refresh

After the P21 ledger entry is accepted and `pipeline_state.py --complete` passes, the canonical `pipeline-state.md` will be copied into the package and a final package manifest plus final audit note will be generated. This refresh affects only the mutable status ledger and delivery bookkeeping, not the accepted TeX, PDF, bibliography, figures, source archive, experiment artifacts, or consistency results.
