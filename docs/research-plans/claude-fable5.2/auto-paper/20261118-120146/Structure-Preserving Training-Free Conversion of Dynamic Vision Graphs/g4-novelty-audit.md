# G4 — Novelty and non-duplication

## Searches performed on 2026-11-18

- `all:"spiking" AND all:"dynamic graph" AND all:"conversion"`: no arXiv records.
- `all:"kNN" AND all:"spiking" AND all:"graph"`: no arXiv records.
- `all:"ANN-to-SNN" AND all:"graph"`: One-Spike SNN, spiking variational graph autoencoder, and tactile location-spiking work.
- `all:"max pooling" AND all:"ANN-to-SNN"`: a 2022 max-pooling approximation paper.
- `ti:"training-free" AND ti:"spiking"`: 2025 spiking Transformer conversion and AutoST.

## Closest work and differentiation

| Work | Same elements | Difference from proposed work |
|---|---|---|
| One-Spike SNN (2024/2025) | Training-free graph conversion; phase coding | Fixed text GCN with linear aggregation; no per-layer kNN, signed max, or structure-preserving calibration |
| Tactile location-spiking / PMSM | Graph conversion and spiking neurons | Special source training or fixed graph; no dynamic vision graph topology |
| Spiking max-pooling approximation | Max operation in SNNs | CNN max pooling, nonnegative/ReLU context; no signed neighbor max in a dynamic graph |
| DCGS | Training-free low-step differential coding, strongest current method family | CNN/Transformer only; no graph operators; no structure objective |
| SpikingGCN / Spiking PointNet / MSG | Graph or visual graph plus spiking | Direct training or different task family; not training-free conversion of a pretrained dynamic graph teacher |
| SpikeZIP-TF and 2025 training-free Transformer conversion | Training-free conversion of non-linear operators | Attention/normalization, not discrete kNN topology or signed graph max |

## Verdict

No highly similar paper in the performed searches matches the same method family, task, dataset class, and core contribution. This is a bounded novelty observation, not a claim of absolute novelty; the final paper must repeat the searches across venue pages, Google Scholar, Semantic Scholar, and citation lists before submission.

Gate verdict: `pass` with a mandatory final paper-stage novelty recheck.
