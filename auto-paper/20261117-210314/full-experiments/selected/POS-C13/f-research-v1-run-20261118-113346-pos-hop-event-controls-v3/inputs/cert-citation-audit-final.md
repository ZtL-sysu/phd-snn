# Independent Citation Audit — Final

review_execution: independent-agent

## Verdict

**PASS**

All six fixes from the initial independent audit are resolved. The final set contains 40 real, correctly attributed, context-supported, deduplicated references. The final ledger is **40 KEEP, 0 FIX, 0 REPLACE, 0 REMOVE**.

## Summary Counts

| Axis | Result |
|---|---:|
| Total keys | 40 |
| Real works | 40 |
| KEEP | 40 |
| FIX | 0 |
| REPLACE | 0 |
| REMOVE | 0 |
| Supported contexts | 40 |
| Recent references, 2022–2026 | 30/40 |
| Missing/uncited/duplicate keys | 0 |
| Duplicate titles/DOIs/arXiv IDs | 0 |

The final `writing/references-final.bib` SHA-256 is `be176ede7327203c59bbb3ceaf0482853863064406964a0d744a73fdc4f0e6bb`, matching `results/reference-audit.json`.

## Six Initial Fixes

1. **Gowal authors — resolved.** `gowal2018ibp` now lists Robert Stanforth and Relja Arandjelovic in the official author sequence.
2. **Mirman source — resolved.** `results/reference-source-probes.json` now uses PMLR `mirman18b`.
3. **Platonov metadata — resolved.** `platonov2023heterophily` now identifies ICLR 2023 and arXiv `2302.11640`.
4. **asgcn context — resolved.** The manuscript says “Asynchronous event-based processing,” matching the event-based visual-processing paper.
5. **Cherukuri context — resolved.** The manuscript now says “generic low-rank neural compression.”
6. **Fast-SNN context — resolved.** `hu2023fast` is now cited under “quantized conversion,” matching ANN-to-SNN conversion.

## New-Reference Recheck

All nine additions are now KEEP: `gowal2018ibp`, `wong2018provable`, `mirman2018diffai`, `katz2017reluplex`, `jacob2018quantization`, `nagel2021white`, `yang2016planetoid`, `pei2020geomgnn`, and `platonov2023heterophily`.

The Nagel author correction remains verified: Markus Nagel, Marios Fournarakis, Rana Ali Amjad, Yelysei Bondarenko, Mart van Baalen, and Tijmen Blankevoort.

## Per-Key Ledger

| Key | Verdict | Final finding |
|---|---|---|
| `asgcn` | **KEEP** | Real AAAI event-based processing paper; corrected context supported. |
| `bu2023optimal` | **KEEP** | Real ICLR conversion paper; context supported. |
| `chaurasia2026sgspose` | **KEEP** | Real geometric spiking-GNN paper; context supported. |
| `cherukuri2025lowrank` | **KEEP** | Real generic low-rank compression paper; corrected context supported. |
| `dampfhoffer2023snnlearning` | **KEEP** | Real SNN-learning survey; context supported. |
| `delay-dsgn` | **KEEP** | Real delayed dynamic spiking-GNN paper; context supported. |
| `ding2021vqgnn` | **KEEP** | Real VQ-GNN paper; context supported. |
| `dy-sign` | **KEEP** | Real dynamic spiking-GNN paper; context supported. |
| `gholami2022quantization` | **KEEP** | Real quantization survey; context supported. |
| `gowal2018ibp` | **KEEP** | Real IBP paper; corrected author list verified. |
| `hao2023offset` | **KEEP** | Real offset-spike conversion paper; context supported. |
| `hu2023fast` | **KEEP** | Real quantized ANN-to-SNN conversion paper; corrected context supported. |
| `huang2025ecmt` | **KEEP** | Real Transformer-conversion paper; both uses supported. |
| `jacob2018quantization` | **KEEP** | Real CVPR quantization paper; context supported. |
| `katz2017reluplex` | **KEEP** | Real CAV verification paper; context supported. |
| `li2023graph1bit` | **KEEP** | Real graph/spiking representation paper; context supported. |
| `li2023seenn` | **KEEP** | Real temporal early-exit conversion paper; context supported. |
| `li2024erroraware` | **KEEP** | Real error-aware conversion paper; both uses supported. |
| `lv2024group` | **KEEP** | Real group-neuron conversion paper; context supported. |
| `mirman2018diffai` | **KEEP** | Real ICML verification paper; corrected PMLR `mirman18b` probe verified. |
| `msg` | **KEEP** | Real manifold spiking-GNN paper; context supported. |
| `nagel2021white` | **KEEP** | Real quantization white paper; corrected author list verified. |
| `nunes2022snnsurvey` | **KEEP** | Real SNN survey; context supported. |
| `one-spike` | **KEEP** | Real conversion/output-code paper; repeated key use is not duplication. |
| `pei2020geomgnn` | **KEEP** | Real Geom-GCN paper; dataset context supported. |
| `platonov2023heterophily` | **KEEP** | Real ICLR 2023 paper; arXiv `2302.11640` verified. |
| `signnn` | **KEEP** | Real dynamic spiking-GNN paper; context supported. |
| `spikenet` | **KEEP** | Real dynamic graph-representation paper; context supported. |
| `spikinggcn` | **KEEP** | Real spiking graph-convolution paper; context supported. |
| `sun2024spikegraphormer` | **KEEP** | Real final journal record; context supported. |
| `tailor2021degreequant` | **KEEP** | Real Degree-Quant paper; context supported. |
| `wan2023adaqp` | **KEEP** | Real distributed message-quantization paper; context supported. |
| `wang2022qgtc` | **KEEP** | Real quantized GNN execution paper; context supported. |
| `wang2022taxonomicsnn` | **KEEP** | Real SNN taxonomy survey; context supported. |
| `wong2018provable` | **KEEP** | Real ICML verification paper; context supported. |
| `yang2016planetoid` | **KEEP** | Real Planetoid/Cora dataset paper; context supported. |
| `you2024spikezip` | **KEEP** | Real Transformer-conversion paper; context supported. |
| `zhang2025sgnnbench` | **KEEP** | Real SGNNBench record; context supported. |
| `zhao2025ttfs` | **KEEP** | Real TTFS Transformer-conversion paper; context supported. |
| `zhu2023a2q` | **KEEP** | Real ICLR aggregation-aware quantization paper; both uses supported. |

## Final Decision

**PASS.** The final manuscript and bibliography require no further citation correction.
