# P5A pre-draft repair

The independent P5A review requested no experiment rerun. The following corrections are applied before drafting:

1. Recomputed `rowwise_width_rms_median` with the standard even-sample median: `30.679169413662216`. The prior upper-middle value is preserved in `corrections/cert-summary-pre-p5a.json`.
2. Replaced the untraceable radius-heterogeneity Figure 3 plan with a tightening/width distribution sourced directly from all 36 method rows in `figures/source-data/figure3-rowwise-tightening.csv`.
3. Narrowed novelty wording to a deterministic final-logit certificate and matched global-radius ablation; `B_mink` ordering is analytic, not an empirical win.
4. Added `provenance-manifest.json` with hashes for frozen models, dataset snapshots, run code and raw outputs.

Raw `cert-methods.json` rows and all experimental calculations remain unchanged.
