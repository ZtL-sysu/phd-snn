# Independent Citation Audit — Final

review_execution: independent-agent

## Verdict

**REVISE**

All 40 cited keys identify real works, every key is cited and present in `writing/references-final.bib`, and the bibliography is deduplicated. The set is sufficiently recent: 30/40 entries are from 2022–2026. However, six targeted corrections remain: two bibliography metadata fixes, one source-probe correction, and three citation-context wording fixes. No reference requires replacement or removal.

## Summary Counts

| Axis | Result |
|---|---:|
| Total keys | 40 |
| Real works | 40 |
| KEEP | 34 |
| FIX | 6 |
| REPLACE | 0 |
| REMOVE | 0 |
| Contexts currently supported without edit | 37 |
| Contexts needing wording correction | 3 |
| Recent references, 2022–2026 | 30/40 |
| Missing/uncited/duplicate keys | 0 |
| Duplicate titles/DOIs/arXiv IDs | 0 |

## Evidence And Method

The audit used:

- `writing/p12-citation-updated-manuscript.md`
- `writing/references-final.bib`
- `results/reference-audit.json`
- `results/reference-source-probes.json`
- `reference-dedup-audit.md`
- `inputs/lr-citation-audit-final.md`
- `inputs/lr-citation-audit-final.json`
- independent checks of the nine new official sources and the corrected Nagel author list.

The final bibliography SHA-256 is `7d8cb4f60f51fb3bf31b761b8b182bb1c710090530b768d9d367cd8a7a3c64c3`, matching `results/reference-audit.json`.

## Nine New References

| Key | Independent finding | Status |
|---|---|---|
| `gowal2018ibp` | Real IBP paper. The final author list should include Robert Stanforth and Relja Arandjelovic; current BibTeX says “Chris Stanforth” and omits Arandjelovic. | **FIX** |
| `wong2018provable` | Real ICML 2018 paper; authors, title, year, pages, and context are correct. | **KEEP** |
| `mirman2018diffai` | Real ICML 2018 paper and supported context. The source probe points to `mirman18a`; the official paper is PMLR `mirman18b`. | **FIX** |
| `katz2017reluplex` | Real CAV 2017 paper; metadata and ReLU-verification context are correct. | **KEEP** |
| `jacob2018quantization` | Real CVPR 2018 quantization paper; metadata and generic quantization context are correct. | **KEEP** |
| `nagel2021white` | Real arXiv white paper. The corrected six-author list—Nagel, Fournarakis, Rana Ali Amjad, Bondarenko, van Baalen, Blankevoort—matches official arXiv metadata. | **KEEP** |
| `yang2016planetoid` | Real ICML 2016 Planetoid paper; Cora/Planetoid dataset context is supported. | **KEEP** |
| `pei2020geomgnn` | Real ICLR 2020 Geom-GCN paper; Chameleon/Squirrel dataset context is supported. | **KEEP** |
| `platonov2023heterophily` | Real ICLR 2023 paper, but the BibTeX venue says NeurIPS and the probe URL uses `2302.12244`. The canonical record is ICLR 2023 / arXiv `2302.11640`. | **FIX** |

Official checks included [Gowal et al.](https://arxiv.org/abs/1810.12715), [Wong and Kolter](https://proceedings.mlr.press/v80/wong18a.html), [Mirman et al.](https://proceedings.mlr.press/v80/mirman18b.html), [Reluplex](https://doi.org/10.1007/978-3-319-63387-9_5), [Jacob et al.](https://doi.org/10.1109/CVPR.2018.00286), [Nagel et al.](https://arxiv.org/abs/2106.08295), [Yang et al.](https://proceedings.mlr.press/v48/yanga16.html), [Geom-GCN](https://arxiv.org/abs/2002.05287), and [Platonov et al.](https://arxiv.org/abs/2302.11640).

## Context Corrections

1. `asgcn` is a real AAAI paper on asynchronous event-based visual processing, not asynchronous graph conversion. Change the manuscript phrase to “asynchronous event-based processing provides additional context.”
2. `cherukuri2025lowrank` supports generic low-rank neural-network compression, not specifically “low-rank graph communication.” Narrow that phrase accordingly.
3. `hu2023fast` supports quantized ANN-to-SNN conversion, not mixed-precision graph-message compression. Move it to conversion/quantization context or rewrite the list item.

## Per-Key Ledger

| Key | Verdict | Attribution/context finding | Required action |
|---|---|---|---|
| `asgcn` | **FIX** | Real AAAI event-based visual-processing paper; current “asynchronous graph conversion” context is unsupported. | Reword context. |
| `bu2023optimal` | **KEEP** | Verified ICLR conversion paper; context supported. | None. |
| `chaurasia2026sgspose` | **KEEP** | Verified geometric spiking-GNN application; context supported. | None. |
| `cherukuri2025lowrank` | **FIX** | Real generic low-rank compression paper; graph-communication wording overstates scope. | Narrow context. |
| `dampfhoffer2023snnlearning` | **KEEP** | Verified final journal metadata; survey context supported. | None. |
| `delay-dsgn` | **KEEP** | Verified delayed dynamic spiking-GNN paper; context supported. | None. |
| `ding2021vqgnn` | **KEEP** | Verified vector-quantized GNN paper; context supported. | None. |
| `dy-sign` | **KEEP** | Verified dynamic spiking-GNN paper; context supported. | None. |
| `gholami2022quantization` | **KEEP** | Verified quantization survey; generic quantization context supported. | None. |
| `gowal2018ibp` | **FIX** | Real paper; author metadata is incorrect/incomplete. | Correct authors. |
| `hao2023offset` | **KEEP** | Verified ICLR offset-spike conversion paper. | None. |
| `hu2023fast` | **FIX** | Real quantized ANN-to-SNN conversion paper; current message-compression context is mismatched. | Reword/move context. |
| `huang2025ecmt` | **KEEP** | Verified ACM MM Transformer-conversion paper; both uses supported. | None. |
| `jacob2018quantization` | **KEEP** | Verified CVPR quantization paper; context supported. | None. |
| `katz2017reluplex` | **KEEP** | Verified CAV verification paper; context supported. | None. |
| `li2023graph1bit` | **KEEP** | Verified graph/spiking representation paper; context supported. | None. |
| `li2023seenn` | **KEEP** | Verified temporal early-exit conversion paper. | None. |
| `li2024erroraware` | **KEEP** | Verified error-aware conversion/calibration paper; both uses supported. | None. |
| `lv2024group` | **KEEP** | Verified group-neuron conversion paper. | None. |
| `mirman2018diffai` | **FIX** | Real ICML verification paper and supported context; probe URL is wrong. | Change probe to PMLR `mirman18b`. |
| `msg` | **KEEP** | Verified manifold spiking-GNN paper; broad spiking-graph context supported. | None. |
| `nagel2021white` | **KEEP** | Corrected six-author list verified; generic quantization context supported. | Preserve correction. |
| `nunes2022snnsurvey` | **KEEP** | Verified SNN survey metadata and context. | None. |
| `one-spike` | **KEEP** | Verified conversion/output-code paper; key reuse is not duplication. | None. |
| `pei2020geomgnn` | **KEEP** | Verified Geom-GCN paper; Chameleon/Squirrel context supported. | None. |
| `platonov2023heterophily` | **FIX** | Real ICLR paper; BibTeX venue and source-probe arXiv ID are wrong. | Set ICLR 2023 and arXiv `2302.11640`. |
| `signnn` | **KEEP** | Verified dynamic spiking-GNN paper. | None. |
| `spikenet` | **KEEP** | Verified dynamic graph-representation paper. | None. |
| `spikinggcn` | **KEEP** | Verified spiking graph-convolution paper. | None. |
| `sun2024spikegraphormer` | **KEEP** | Verified final Information Sciences record; context supported. | None. |
| `tailor2021degreequant` | **KEEP** | Verified Degree-Quant paper; context supported. | None. |
| `wan2023adaqp` | **KEEP** | Verified distributed message-quantization paper. | None. |
| `wang2022qgtc` | **KEEP** | Verified quantized GNN execution paper. | None. |
| `wang2022taxonomicsnn` | **KEEP** | Verified SNN taxonomy survey. | None. |
| `wong2018provable` | **KEEP** | Verified ICML verification paper; context supported. | None. |
| `yang2016planetoid` | **KEEP** | Verified Planetoid/Cora dataset paper. | None. |
| `you2024spikezip` | **KEEP** | Verified Transformer-conversion paper. | None. |
| `zhang2025sgnnbench` | **KEEP** | Verified accepted SGNNBench record; large-scale evaluation context supported. | None. |
| `zhao2025ttfs` | **KEEP** | Verified TTFS Transformer-conversion paper. | None. |
| `zhu2023a2q` | **KEEP** | Verified ICLR aggregation-aware quantization paper; both uses supported. | None. |

## Final Decision

The citation collection is substantively sound and recent enough for the manuscript. Apply the six targeted fixes above; after those changes, the expected ledger is **40 KEEP, 0 FIX, 0 REPLACE, 0 REMOVE**.
