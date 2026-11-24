# Independent Citation Re-audit — Final

**Verdict: PASS (`all_entries_keep`)**

- Date: 2026-11-18 (Asia/Shanghai); generated 2026-11-17T23:55:41Z.
- Scope: corrected `references.bib`, all 41 entries, and all 44 citation occurrences in `writing/p12/paper-with-verified-references.md`.
- Result: **41 KEEP, 0 FIX, 0 REPLACE, 0 REMOVE**.
- Previous findings: all 13 FIX items are resolved against the canonical evidence used in the independent audit.
- Mapping: 41 unique bibliography keys, 41 unique cited keys, no uncited residual, no undefined citations, and the same 44 occurrence/key/line mapping as before correction.
- Duplicates: 20 unique DOI values, 13 unique arXiv identifiers, 41 unique normalized titles; no duplicate preprint/published pair or duplicate version remains.
- Context: all 44 occurrences remain context-appropriate; no wrong-context replacement or removal is required.
- Sources were not edited during this re-audit. The manuscript and all four probe files retain their prior hashes; `references.bib` has the newly audited corrected hash.

## Verification of the 13 Corrections

| Key | Bib | Verified resolution | Evidence |
|---|---:|---|---|
| `li2019deepgcn` | L37 | `Müller, Matthias` and `Thabet, Ali Kassem` now match the published author list. | [CVF](https://openaccess.thecvf.com/content_ICCV_2019/html/Li_DeepGCNs_Can_GCNs_Go_As_Deep_As_CNNs_ICCV_2019_paper.html) |
| `zhu2023a2q` | L112 | Now `@inproceedings`, ICLR 2023, with arXiv retained only as a secondary identifier. | [DBLP](https://dblp.org/rec/conf/iclr/ZhuLMH0LL023.html) |
| `hu2023fast` | L129 | TPAMI 45(12), 14546–14562, 2023, with the correct DOI. | [PubMed/DOI metadata](https://pubmed.ncbi.nlm.nih.gov/37721891/) |
| `cherukuri2025lowrank` | L148 | Venue corrected to International Conference on Machine Learning Technologies; pages 166–170 added. | [DOI/OpenAlex](https://doi.org/10.1109/ICMLT65785.2025.11193154) |
| `hao2023offset` | L168 | Now `@inproceedings`, ICLR 2023; no longer an arXiv-only journal record. | [DBLP](https://dblp.org/rec/conf/iclr/HaoDB0Y23.html) |
| `lv2024group` | L177 | ICASSP 2024 proceedings, pages 6475–6479, correct DOI. | [DOI/OpenAlex](https://doi.org/10.1109/ICASSP48485.2024.10448202) |
| `bu2023optimal` | L186 | Published ICLR record now uses the correct conference year 2022; arXiv is secondary. | [ICLR 2022 paper](https://yuzhaofei.github.io/papers/22-ICLR-Optimal%20ANN-SNN%20Conversion%20for%20High-accuracy%20and%20Ultra-low-latency%20Spiking%20Neural%20Networks.pdf) |
| `huang2025ecmt` | L216 | ACM Multimedia 2024, pages 10688–10697, correct DOI; no longer a 2025 arXiv-only record. | [DOI/OpenAlex](https://doi.org/10.1145/3664647.3680620) |
| `delay-dsgn` | L265 | Singular `Evolving Graph` and `Liang, Jianqing` now match PMLR. | [Official PMLR](https://proceedings.mlr.press/v267/wang25dm.html) |
| `sun2024spikegraphormer` | L296 | Information Sciences 755, article 123828, 2026, correct DOI and `O'Hare, Gregory M. P.` | [DOI/OpenAlex](https://doi.org/10.1016/j.ins.2026.123828) |
| `zhang2025sgnnbench` | L306 | Accepted NeurIPS 2026 title and all five accepted authors now match, including Huazhen Zhong and removal of preprint-only Li Kuang. | [Official NeurIPS listing](https://neurips.cc/virtual/2026/poster/139238), [author listing](https://chenliang.tech/publications) |
| `dampfhoffer2023snnlearning` | L343 | Final publication metadata now consistently uses 2024, 35(9), 11906–11921. | [IEEE](https://ieeexplore.ieee.org/document/10097504/) |
| `nunes2022snnsurvey` | L354 | Pages corrected to 60738–60764. | [Institutional metadata](https://sigarra.up.pt/ffup/en/pub_geral.pub_view?pi_pub_base_id=578876) |

The exact 13-key set above equals the FIX-key set in `CITATION_AUDIT_INDEPENDENT.json`; there are no unresolved prior findings.

## Full 41-Entry Ledger

All entries below are KEEP. `References` gives the current entry start line; `Uses` gives manuscript line numbers. Each listed use is SUPPORTS.

| Key | References | Uses | Final metadata/context status |
|---|---:|---:|---|
| `kipf2017gcn` | L1 | 17 | Verified GCN record; graph-convolution context. |
| `hamilton2018graphsage` | L10 | 17 | Verified GraphSAGE record; neighborhood-sampling context. |
| `velickovic2018gat` | L19 | 17 | Verified GAT record; graph-attention context. |
| `xu2019gin` | L28 | 17 | Verified GIN record; expressive-GNN context. |
| `li2019deepgcn` | L37 | 17 | Corrected authors verified; deep-GNN context. |
| `abu2019mixhop` | L46 | 17 | Verified MixHop record; higher-order-mixing context. |
| `chen2020gcnii` | L55 | 17 | Verified GCNII record; deep-GCN context. |
| `li2018deeper` | L64 | 17 | Verified AAAI record; GCN-depth analysis context. |
| `wu2021gnnsurvey` | L74 | 17 | Verified survey record; broad-GNN context. |
| `tailor2021degreequant` | L85 | 19 | Verified Degree-Quant record; GNN QAT context. |
| `ding2021vqgnn` | L94 | 19 | Verified VQ-GNN record; vector-quantized representation context. |
| `wang2022qgtc` | L103 | 19 | Verified PPoPP record; tensor-core execution context. |
| `zhu2023a2q` | L112 | 19, 87 | Corrected ICLR record; aggregation-aware/node-budget adaptation context. |
| `wan2023adaqp` | L121 | 19 | Verified MLSys record; distributed message-quantization context. |
| `hu2023fast` | L129 | 19 | Corrected TPAMI record; quantized-conversion context. |
| `gholami2022quantization` | L140 | 19 | Verified quantization-survey chapter; general-quantization context. |
| `cherukuri2025lowrank` | L148 | 19 | Corrected ICMLT record; low-rank compression context. |
| `one-spike` | L157 | 21, 21, 88 | Verified journal record; conversion/output-code/adapted-control contexts. Repeated key use is not duplication. |
| `hao2023offset` | L168 | 21 | Corrected ICLR record; offset-spike calibration context. |
| `lv2024group` | L177 | 21 | Corrected ICASSP record; group-neuron context. |
| `bu2023optimal` | L186 | 21 | Corrected ICLR 2022 record; high-accuracy/low-latency context. |
| `li2023seenn` | L195 | 21 | Verified NeurIPS record; temporal early-exit context. |
| `you2024spikezip` | L202 | 21 | Verified ICML/PMLR record; Transformer-conversion context. |
| `zhao2025ttfs` | L209 | 21 | Verified ICML/PMLR record; TTFS conversion context. |
| `huang2025ecmt` | L216 | 21 | Corrected ACM MM 2024 record; Transformer-conversion context. |
| `li2024erroraware` | L225 | 21 | Verified IJCV record; post-training calibration context. |
| `spikinggcn` | L236 | 23 | Verified IJCAI record; spiking graph-convolution context. |
| `spikenet` | L245 | 23 | Verified AAAI record; dynamic graph-representation context. |
| `dy-sign` | L254 | 23 | Verified AAAI record; dynamic spiking-GNN context. |
| `delay-dsgn` | L265 | 23 | Corrected title/author verified; delayed-evolution context. |
| `signnn` | L272 | 23 | Verified Pattern Recognition record; dynamic-graph context. |
| `msg` | L282 | 23 | Verified NeurIPS record; manifold-geometry context. |
| `negative-spike` | L289 | 23 | Verified IJCAI record; signed-conversion context. |
| `sun2024spikegraphormer` | L296 | 23 | Corrected Information Sciences record; spiking-attention context. |
| `zhang2025sgnnbench` | L306 | 23 | Corrected accepted NeurIPS 2026 record; large-scale evaluation context. |
| `li2023graph1bit` | L313 | 23 | Verified arXiv record; graph contrastive-learning context. |
| `chaurasia2026sgspose` | L322 | 23 | Verified IEEE Access record; geometric-application context. |
| `asgcn` | L332 | 23 | Verified AAAI record; asynchronous visual-processing context. |
| `dampfhoffer2023snnlearning` | L343 | 21 | Corrected final-journal metadata; conversion/direct-training survey context. |
| `nunes2022snnsurvey` | L354 | 21 | Corrected page range verified; broad-SNN survey context. |
| `wang2022taxonomicsnn` | L364 | 21 | Verified taxonomic survey; SNN learning/hardware context. |

## Mapping, Duplicates, and Immutability Checks

- Exact key-set equality: `bib_keys == cited_keys`, cardinality 41.
- Total occurrences: 44. Per-key line lists exactly match the previous ledger, including `zhu2023a2q` at lines 19 and 87 and `one-spike` at lines 21, 21, and 88.
- No new DOI/arXiv/title collision was introduced by replacing preprints with published records.
- Corrected bibliography SHA-256: `6af987364d10cb58731098c9b5ff55bf201026a29dc36c007e71633138aef2b3`.
- Unchanged manuscript SHA-256: `8a433c73f85c8ae69f7fec1dea3929e330e1e64238e8e389d36a3281f705a33b`.
- Unchanged probe hashes are recorded in `CITATION_AUDIT_INDEPENDENT_FINAL.json`.

**Final decision: PASS. All requested corrections are verified, all 41 entries are clean, all 44 uses are appropriate, and no duplicate versions remain.**

## Final Note — BibTeX Warning Cleanup

Rechecked 2026-11-17T23:59:53Z after metadata-only warning cleanup. All three changes are verified and the **PASS remains valid**:

- `gholami2022quantization` now correctly uses container `Low-Power Computer Vision` and publisher `Chapman and Hall/CRC`, matching DOI `10.1201/9781003162810-13`.
- `dy-sign` and `asgcn` retain their canonical titles, authors, years, proceedings volume, pages, and DOI. Their issue fields (`15` and `2`) were omitted solely for BibTeX-style warning cleanup; the remaining metadata uniquely and accurately identifies both AAAI records.
- The 41-entry key set, 44-use mapping, context verdicts, and duplicate/version results are unchanged. Updated `references.bib` SHA-256: `6486042a1f0e45745fe955e92658265c5a26dc299f754da4b936343736776508`.
