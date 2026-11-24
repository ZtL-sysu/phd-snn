# Clean fact packet

- Scope: Chameleon/Squirrel, `[X,AX,A^2X,A^3X]`, split/probe seeds 600-604, five node-permutation and five non-identity hop-shuffle seeds.
- Method: eight Lloyd centroids plus one escape symbol; four-bit symbols; 32-bit float32 escapes; `8×32` bits/channel codebooks.
- Hybrid error: 3.952% Chameleon, 4.879% Squirrel.
- Conservative storage: 7.490× and 7.602×.
- Permutation maximum error: `2.22e-16` for raw and hybrid.
- Codec-consistent mismatched-shuffle mean ratios: 3.725× and 3.626×; minimum 3.310×; no identity permutations.
- Retrained hybrid versus raw paired balanced-accuracy differences: −0.083±1.197 pp Chameleon; +0.768±1.017 pp Squirrel.
- Fixed raw-probe ordered versus shuffled hybrid: +9.57 pp Chameleon; +9.08 pp Squirrel.
- Accepted task probes train only on train indices, select epochs on validation and evaluate on test.
- Full-data probe-fitting run is preserved negative evidence and excluded.
- Safe claim: hybrid hop-message coding with conservative storage and order controls.
- Forbidden claim: general graph-transformer→SNN, temporal, energy, hardware or causal positional-reasoning claim.
