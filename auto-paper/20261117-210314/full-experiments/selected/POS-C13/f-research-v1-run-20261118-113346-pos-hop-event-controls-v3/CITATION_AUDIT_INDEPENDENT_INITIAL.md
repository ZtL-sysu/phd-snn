# Independent Citation Audit — Final

review_execution: independent-agent

## Verdict

**REVISE**

All 32 cited keys identify real works and are used in supported contexts. The bibliography is deduplicated and sufficiently recent, but two positional references have incorrect BibTeX metadata and the recorded bibliography hash is stale.

## Summary Counts

| Axis | Result |
|---|---:|
| Total keys | 32 |
| Real works | 32 |
| KEEP | 30 |
| FIX | 2 |
| REPLACE | 0 |
| REMOVE | 0 |
| Contexts supported | 32 |
| Recent references, current metadata | 24/32 |
| Recent references after Dwivedi year fix | 25/32 |
| Missing/uncited/duplicate keys | 0 |
| Duplicate titles/DOIs/arXiv IDs | 0 |

The current `writing/references-final.bib` SHA-256 is `8fadbc63f2799f43b366a9473700b0993bb704eb564a260ba9c5f954e003dc43`, while `results/reference-audit.json` records `b92e29216a95b97c96c21cc728cd24ad9a5177e30143f770fbd61edfeafe83ec`. Regenerate the audit after metadata correction.

## New Positional References

| Key | Independent finding | Status |
|---|---|---|
| `vaswani2017attention` | Real NeurIPS 2017 Transformer paper; authors, title and attention context are correct. | **KEEP** |
| `dwivedi2021graph` | Real paper on learnable structural and positional representations, but it is ICLR 2022, not ICLR 2021. | **FIX** |
| `kreuzer2021rethinking` | Real NeurIPS 2021 spectral-attention paper. The first author is Devin Kreuzer, not Matthias Kreuzer; William L. Hamilton is the full author name. | **FIX** |

Official checks included [Attention Is All You Need](https://arxiv.org/abs/1706.03762), [Dwivedi et al., ICLR 2022](https://arxiv.org/abs/2110.07875), and [Kreuzer et al., NeurIPS 2021](https://dl.acm.org/doi/10.5555/3540261.3541915).

## Per-Key Ledger

| Key | Verdict | Finding |
|---|---|---|
| `asgcn` | **KEEP** | Real asynchronous event-based processing paper; context supported. |
| `bu2023optimal` | **KEEP** | Real ANN-to-SNN conversion paper; context supported. |
| `chaurasia2026sgspose` | **KEEP** | Real geometric spiking-GNN application; adjacent context supported. |
| `delay-dsgn` | **KEEP** | Real delayed dynamic spiking-GNN paper; context supported. |
| `ding2021vqgnn` | **KEEP** | Real vector-quantized GNN paper; compression context supported. |
| `dwivedi2021graph` | **FIX** | Change conference year to 2022 and update the source-probe metadata. |
| `dy-sign` | **KEEP** | Real dynamic spiking-GNN paper; context supported. |
| `gholami2022quantization` | **KEEP** | Real quantization survey; compression context supported. |
| `hao2023offset` | **KEEP** | Real offset-spike conversion paper; context supported. |
| `hu2023fast` | **KEEP** | Real quantized ANN-to-SNN conversion paper; context supported. |
| `huang2025ecmt` | **KEEP** | Real Transformer-conversion paper; context supported. |
| `jacob2018quantization` | **KEEP** | Real quantization paper; compression context supported. |
| `kreuzer2021rethinking` | **FIX** | Correct first author to Devin Kreuzer and author to William L. Hamilton. |
| `li2023graph1bit` | **KEEP** | Real compact graph/spiking representation paper; context supported. |
| `li2023seenn` | **KEEP** | Real temporal early-exit conversion paper; context supported. |
| `li2024erroraware` | **KEEP** | Real error-aware conversion paper; context supported. |
| `lv2024group` | **KEEP** | Real group-neuron conversion paper; context supported. |
| `nagel2021white` | **KEEP** | Real quantization white paper; attribution supported. |
| `one-spike` | **KEEP** | Real output-code conversion paper; context supported. |
| `pei2020geomgnn` | **KEEP** | Real Geom-GCN paper; Chameleon/Squirrel context supported. |
| `platonov2023heterophily` | **KEEP** | Real ICLR 2023 heterophily/dataset paper; context supported. |
| `signnn` | **KEEP** | Real dynamic spiking-GNN paper; context supported. |
| `spikenet` | **KEEP** | Real dynamic graph-representation paper; context supported. |
| `spikinggcn` | **KEEP** | Real spiking graph-convolution paper; context supported. |
| `sun2024spikegraphormer` | **KEEP** | Real graph-transformer/spiking-attention paper; context supported. |
| `tailor2021degreequant` | **KEEP** | Real Degree-Quant paper; compression context supported. |
| `vaswani2017attention` | **KEEP** | Real Transformer paper; general attention context supported. |
| `wan2023adaqp` | **KEEP** | Real distributed message-quantization paper; context supported. |
| `wang2022qgtc` | **KEEP** | Real quantized GNN execution paper; context supported. |
| `zhang2025sgnnbench` | **KEEP** | Real spiking-GNN benchmark paper; context supported. |
| `zhao2025ttfs` | **KEEP** | Real TTFS Transformer-conversion paper; context supported. |
| `zhu2023a2q` | **KEEP** | Real aggregation-aware quantization paper; context supported. |

## Deduplication And Recency

- 32 unique BibTeX keys and 32 normalized titles.
- No duplicate DOI or arXiv identifier.
- Twenty-nine keys inherit the verified CERT-C11 audit.
- The three new positional works are real and appropriately cited.
- Current recency is 75%; correcting the ICLR year raises it to 78.1%. The set is sufficiently recent.

## Required Fixes

1. Correct `dwivedi2021graph` to ICLR 2022.
2. Correct `kreuzer2021rethinking` authors to Devin Kreuzer and William L. Hamilton.
3. Update `results/reference-source-probes.json` to stop labeling those incorrect metadata records as fully consistent.
4. Regenerate `results/reference-audit.json` and its bibliography hash after the BibTeX edits.

After these changes, the expected ledger is **32 KEEP, 0 FIX, 0 REPLACE, 0 REMOVE**.
