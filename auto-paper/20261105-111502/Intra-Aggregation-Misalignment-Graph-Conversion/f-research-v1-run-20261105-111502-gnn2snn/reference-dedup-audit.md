# P12 / P14 — reference deduplication audit

`tex/refs.bib` was built by a literature agent from arXiv abs pages, PMLR, ECCV/Springer,
Crossref and official proceedings. Duplicate-paper scan by DOI, arXiv id, normalised title and
preprint/published version: the two most likely collisions are TPP (arXiv:2502.14487 vs PMLR 267)
and FTBC (arXiv:2403.18388 vs ECCV LNCS), each retained once as a single entry. SpikeGCL
(arXiv:2305.19306 / ICLR 2024), QCFS (arXiv:2303.04347 / ICLR 2022) and SpikingGCN
(arXiv:2205.02767 / IJCAI 2022) are likewise single entries. Two anonymous companion entries
are distinct manuscripts, not duplicate versions.

Quantity/recency arithmetic is produced by `contracts/check_citations.py`, which counts distinct
keys actually cited in the manuscript and the frozen 2023-2026 window. No uncited padding entry
remains and no preprint/published pair is counted twice.
