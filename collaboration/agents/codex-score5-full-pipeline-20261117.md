# codex-score5-full-pipeline-20261117

## Scope

Complete the full `f-research-v1` P0-P21 pipelines for LR-C05, CERT-C11, and POS-C13 sequentially, with complete experiment artifacts, papers, PDFs, and source packages.

## LR-C05 completed run

- Run root: `C:\code\phd-snn\auto-paper\20261117-210314\full-experiments\selected\LR-C05\f-research-v1-run-20261118-004321-lr-logit-fidelity-v3`
- Contract: guidance-v3 logit-fidelity/resource trade-off after preserving v1/v2 failures.
- P0-P5A: passed; official-test confirmation supports 26.23%, 33.99%, and 25.83% logit-MSE reductions with bounded task loss.
- P6: passed with canonical six-section ARC Stage 16 outline and clean context audit.
- P7: passed with Codex ACP/ARC Stage 17 draft and reverse outline; one structural merge removed duplicate Results text.
- P8-P21: passed. Figure 1 uses the user-authorized deterministic self-drawn fallback after repeated GPT image-generation failures.
- Final delivery: `deliverables/LR-C05-final-v1/`, containing the accepted 11-page PDF, TeX, BibTeX, figures, source archive, experiment artifacts, final audits, state ledgers, and manifest.
- Final source archive clean-extraction `latexmk` returned 0; normalized PDF text matched the accepted PDF; 41/41 bibliography keys resolved; all fonts embedded.

## LR-C05 final evidence

- Data Figures 2-4 generated from frozen JSON with Python/matplotlib.
- SVG/PDF/PNG/TIFF exports and source CSVs exist.
- Visual QA passed after layout repairs.
- Figure captions, table plan, figure/table insertion audit, and a P8 manuscript copy with inserted data figures exist.
- Figure 1 prompt and deterministic fallback provenance are preserved in `figures/`; this substitution was explicitly authorized by the user after service failure.
- P20 final audit: `writing/p20-final-v2/p20-final-audit.json`.
- P21 verification: `audits/p21-delivery-verification.json`.
- Final package manifest SHA-256: `9ad7e0e893b514b9d3732d4de0b6ab6a273a89e4a012d0b2a9f50a1ccdf4e570`.

## Next run

- Score≥5 paper pipelines are complete. Preserve all three final packages and every failed/revised intermediate run.
- Future work starts from delivered packages and target-specific metadata, not by rerunning accepted P0-P21 workflows.

## CERT-C11 completed run

- Final run root: `C:\code\phd-snn\auto-paper\20261117-210314\full-experiments\selected\CERT-C11\f-research-v1-run-20261118-093658-cert-rowwise-interval-v6`.
- Accepted claim: deterministic final-logit interval containment plus 74.26%-82.12% rowwise tightening over a matched global-radius ablation.
- Negative result preserved: rowwise width/RMS standard median 30.68 and maximum 36.91; no absolute-width claim.
- Final package: `deliverables/CERT-C11-final-v1/`; manifest SHA-256 `3d2d545d4190adc6645366d8dd98edd0d7f2b05aaff1720395a08b34e1732128`.
- P21 clean source-archive compilation and normalized-text comparison passed; one final 10-page PDF included.

## POS-C13 completed run

- Final run root: `C:\code\phd-snn\auto-paper\20261117-210314\full-experiments\selected\POS-C13\f-research-v1-run-20261118-113346-pos-hop-event-controls-v3`.
- Accepted claim: permutation-equivariant hybrid hop-message coding with 3.952%/4.879% representation error, 7.49×/7.60× conservative storage reduction, and codec-consistent shuffled-hop controls.
- Negative evidence preserved: leaky full-label probe run, incomplete v1 delivery package, and earlier bit-ledger/shuffle-control defects.
- Final package: `deliverables/POS-C13-final-v2/`; manifest SHA-256 `e6f9de4ce714c1149f292c5ced3cc2082d8bb2694ff62a0a77a0242a81f36c10`.
- P21 clean source-archive compilation passed; normalized text matched; one final 8-page PDF included; 32/32 references resolved.

## Important boundaries

- Local Python: `C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`.
- Local GPU: RTX 3060 12GB.
- Do not commit, push, submit, or use remote compute.
- POS-C13 completed after CERT-C11; preserve the full sequential history.
- Preserve all failed attempts and negative results.
