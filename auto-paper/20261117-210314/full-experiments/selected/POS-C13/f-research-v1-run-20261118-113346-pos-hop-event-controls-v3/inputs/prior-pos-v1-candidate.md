# POS-C13-v1 — permutation-equivariant hop-position event encoding

Hypothesis: quantized hop-wise positional messages can preserve graph transformer positional information and node-permutation equivariance after event coding.

Smoke: Chameleon normalized adjacency and features, three-hop concatenated messages, 8-level uniform quantization. Gate: permutation error ≤1e-10, quantization relative error ≤20%, and ≥4× bit-storage reduction.

Novelty boundary: SpikeGraphormer is direct spiking graph-transformer training; this candidate targets conversion of positional/structural encodings.
