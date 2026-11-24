# P3 baseline-first execution gate

All ten baseline/control files exist before proposed-method campaign. Main execution device is the local RTX 3060; immutable `core.convert` graph reference runs retain CPU compatibility and are explicitly separated from GPU probes/SVD.

| ID | Baseline evidence | Gate interpretation |
|---|---|---|
| DYN/DLY | raw DAVIS probe mean accuracy 56.16% | task is nontrivial; residual/delay methods must compare paired |
| EQ | raw 24.35%, component-uniform 24.49% | difficult 8-class coordinate task; radial encoder comparison remains decisive |
| PERM | naive max errors 0.50/0.90/0.95 | order-sensitive control gives a real falsifier |
| SIGN | balanced accuracy signed 56.25%, abs 55.56%, positive 55.78% | signed smoke advantage is modest; strong ≥2 pp is at risk but not contradicted |
| LR | rank128 compression 7.32×/8.99×/11.64×; SVD logit error 0.091/0.182/0.330 vs random 0.566/0.935/1.251 | strong path credible on 2/3 graphs |
| EDGE | log quantization strongly beats uniform at 3–6 bits | nonuniform claim is plausible; 6-bit log error 2.82% |
| CERT | coverage 100%; width/RMS 3.06–6.72; 79.7–85.1% tighter | strong certificate path credible |
| POS | per-channel balanced accuracy 61.23%/45.53% vs raw 58.52%/43.32% | strong path credible |
| READ | top2 preservation 100%; median slot reduction 63.33% | strong path already supported by baseline/control file |

No baseline crash remains. The LR and top-two implementation repairs are recorded in `corrections/`; invalid pre-repair LR output was overwritten by the corrected raw-message run.

Verdict: **pass**.
