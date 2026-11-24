# P3 reacceptance after mechanism alignment

The P2 repair changed proposed representations/precision, not frozen baseline identities, data, splits, seeds, metrics or gate thresholds. The ten baseline files remain hash-valid in `baseline-manifest.json`.

- DYN/DLY raw baseline remains valid; only the proposed residual representation changes.
- EQ raw/component baselines remain valid; only the rotation certificate precision changes.
- PERM naive baseline remains valid; deterministic pooling is recomputed in float64.
- POS raw/uniform baselines remain valid; a per-channel-uniform control is added alongside the proposed per-channel quantile codebook.
- SIGN/LR/EDGE/CERT/READ are unaffected.

Verdict: **pass**; unchanged baseline evidence is explicitly reused after applicability check.
