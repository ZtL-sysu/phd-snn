# EQ-C02-v1 — group-equivariant radial event coding for coordinate GNNs

Hypothesis: encode coordinate message magnitude as quantized events and retain the group direction, so rotation/translation-free coordinate transforms commute with conversion.

Smoke: 3,982 real MaleCNS soma coordinates, 8 radial levels, 90° rotation. Gate: equivariance max error ≤1e-10 and quantization relative error ≤10%.

Result: PASS — equivariance error 0.0; quantization relative error 7.08%.

Novelty boundary: MSG/GC-LIF/SGSPose are direct/hybrid spiking equivariance; no verified frozen E(3) GNN→SNN conversion was found. Translation handling and molecular benchmarks remain required.
