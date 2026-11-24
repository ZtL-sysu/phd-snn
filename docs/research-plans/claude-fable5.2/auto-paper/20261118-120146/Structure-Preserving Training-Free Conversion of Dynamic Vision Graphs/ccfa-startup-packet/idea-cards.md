# Mechanism-level idea cards

## Card A — stability-calibrated conversion for dynamic vision graphs

- Bottleneck: quantized/multi-threshold activations perturb feature distances and signed max-aggregation winners; dynamic kNN converts continuous errors into discrete topology changes.
- Mechanism: preserve the teacher's discrete operators at conversion time by (i) calibration that minimizes post-quantization neighbor/max disagreement on training data, (ii) a margin-aware neighbor selector that reserves teacher neighbors when distance gaps are below the calibrated error bound, and (iii) signed exact-integer winner selection for max aggregation before graded spike decoding.
- Assumptions: a public teacher backbone and dataset are available; neighbor flips and max-winner flips are measurable; a nontrivial fraction of graph layers have narrow k/k+1 margins; teacher discrete decisions remain the right target.
- Falsification: restoring teacher neighbors and winners produces less than half of the accuracy loss, or accuracy loss is negligible at the strongest baseline, or the method does not improve structure agreement at matched event/cost budget.
- Contribution type: method plus diagnostic structure-preservation analysis.
- Feasibility risks: official ViG weights may be tied to ImageNet-scale data; DCGS code has no graph operators and no license; signed max may require custom autograd-free implementation.

## Card B — layerwise error-carry delta inference for visual graphs

- Bottleneck: frame-to-frame feature changes spread over L hops; truncating small changes saves computation but can alter kNN and max winners.
- Mechanism: propagate residual delta with per-layer thresholds and carry-forward residual memory; allocate budget by predicted topological sensitivity rather than activation magnitude.
- Assumptions: consecutive frames are sufficiently correlated; dynamic graphs expose measurable sparsity; exact incremental graph methods are not already the strongest practical baseline.
- Falsification: dense per-frame inference has little delta sparsity, exact incremental methods match the method at equal error, or topological-sensitive allocation does not beat magnitude-only allocation.
- Contribution type: method plus sparsity/accuracy trade-off.
- Feasibility risks: video/skeleton data access, GPU sparse kernel overhead, and strong exact-increment baselines may erase practical gains.

## Card C — failure census of conversion across visual graph families

- Bottleneck: existing conversion methods are evaluated on CNN/Transformer and fixed graphs; failure modes on dynamic/max/sum and static/streaming graphs are unknown.
- Mechanism: controlled interventions isolate topology and winner changes as causes of accuracy loss.
- Assumptions: several teachers can be converted faithfully enough to measure a failure; intervention runs are computationally tractable.
- Falsification: no teacher shows material degradation or structure flip; interventions do not recover loss.
- Contribution type: diagnostic benchmark/report.
- Feasibility risks: may become an incremental audit rather than a top-tier method paper; negative result could eliminate A and B.

## Card D — fair energy accounting for spiking versus quantized graph networks

- Bottleneck: common SNN energy estimates omit memory and graph construction, and compare against 32-bit rather than strong low-bit baselines.
- Mechanism: paired spiking/quantized graph twins with equal accuracy targets and a full operation, memory, and dynamic-build cost ledger.
- Assumptions: defensible architecture mapping and cost parameters are available; strong quantized baselines can be reproduced.
- Falsification: no crossing point exists, or the conclusion is entirely determined by assumed hardware constants.
- Contribution type: analysis/benchmark.
- Feasibility risks: hardware-model dependence may prevent a decisive top-tier claim without silicon measurement.
