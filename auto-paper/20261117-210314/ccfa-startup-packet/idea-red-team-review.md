# Independent red-team review of the portfolio

Verdict: **proceed to individual guidance design with mandatory scope repairs**. The ten mechanisms pass smoke but are not equally paper-ready.

## Fatal risks by family

| Family | Fatal if unresolved | Repair |
|---|---|---|
| DYN/DLY | no actual dynamic-edge GNN teacher or task | add a public temporal-edge benchmark; keep DAVIS as mechanism evidence only |
| EQ | only rotation on coordinates; no downstream equivariant GNN | add an E(3)/SE(3) teacher and symmetry-error/accuracy controls |
| PERM/POS | property certificate may be seen as software testing | tie certificate to attention/positional conversion errors and strong transformer baselines |
| SIGN | negative-spike conversion exists | demonstrate heterophily-specific downstream gain against signed/unsigned controls |
| LR/EDGE | compression error may not preserve teacher decisions | report teacher agreement at equal event/memory budget and strong quantization baselines |
| CERT | conservative envelope may be scientifically trivial | prove tightness/measurement calibration and show useful abstention/precision tradeoff |
| READ | argmax preservation is tautological | measure hidden work, calibration, class-pair retrieval and failure under near-tied margins |

## Portfolio-level concerns

- Several accepted screens are exactness/compression proofs rather than accuracy wins. Calling them “strong results” without the qualifier would be misleading.
- DYN and DLY share DAVIS evidence; full papers must use distinct temporal graph tasks/claims or merge them.
- One local checkpoint family and fixed splits limit generality. Full experiments need independent teachers/seeds and direct-conversion baselines.
- Novelty confidence is medium-high within recorded scope; a fresh pre-submission search is mandatory.

Recommendation: select at most 2–3 candidates for full `f-guidance-builder-v1` packages initially; do not launch ten full papers simultaneously.
