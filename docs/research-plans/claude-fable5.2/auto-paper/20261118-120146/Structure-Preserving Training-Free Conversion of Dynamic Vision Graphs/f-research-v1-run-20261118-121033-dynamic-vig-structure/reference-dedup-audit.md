# Reference deduplication and citation audit

Audit date: 2026-11-18.

| Key | Status | Source used | Note |
|---|---|---|---|
| cao2015spiking | verified | Crossref/IJCV metadata record | Foundational conversion paper |
| rueckauer2017conversion | verified | Frontiers metadata | Foundational conversion paper |
| li2021calibration | verified | arXiv API `2106.06984` | Title and authors corrected from earlier draft |
| huang2025dcgs | verified | arXiv API `2503.00301` | Current strong training-free conversion baseline |
| onespike2025 | verified | Crossref DOI `10.1109/TETC.2024.3386893` | Author placeholders removed; journal metadata added |
| pmsm2025 | verified | arXiv API `2508.14520` | Author placeholders removed; version/title corrected |
| lan2023 | verified | Crossref DOI `10.1109/ICCV51070.2023.00845` | Exact ICCV title and authors added |
| spikinggcn2022 | verified | arXiv API `2205.02767` | IJCAI 2022 confirmation in comment |
| spikingpointnet2023 | verified | arXiv API `2310.06232` | NeurIPS confirmation in comment |
| vig2022 | verified | arXiv API `2206.00272` | NeurIPS 2022 confirmation in comment |
| deltacnn2022 | verified | arXiv API `2203.03996` | CVPR 2022 confirmation in comment |
| aegnn2022 | verified | arXiv API `2203.17149` | CVPR 2022 confirmation in comment |

## Duplicate check

No duplicate DOI, arXiv ID, or normalized title was found among the 12 references. `pmsm2025` uses the later almost-lossless title and arXiv version; the earlier lossless-title preprint is not separately cited.

## Context support

Each cited work appears in Related Work to support one of: conversion lineage, graph conversion limitations, dynamic vision graph architecture, or event-driven inference. No citation is used to support the paper's experimental numbers.

## Blocking issues fixed

- `author={Unknown}` placeholders in One-Spike and PMSM entries were removed.
- PMSM title and author list were corrected.
- Lan et al. title and author list were corrected from DOI metadata.
- Li et al. calibration title and authors were corrected from arXiv metadata.
