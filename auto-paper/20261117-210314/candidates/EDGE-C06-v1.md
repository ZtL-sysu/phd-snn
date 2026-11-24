# EDGE-C06-v1 — quantized biological edge-weight event messages

Hypothesis: irregular graph edge weights can be represented by a small event alphabet without losing weighted-message fidelity, enabling event-driven graph conversion rather than float32 edge transport.

Smoke: 385,946 finite FlyWire biological `syn_count` edge weights, 64 uniform levels (6 bits). Gate: relative quantization error ≤25% and storage reduction ≥4× versus float32.

Result: PASS — error 18.92%; 5.33× bit-storage reduction; total synapse mass 2,266,503.

Novelty boundary: One-Spike/ASGCN cover sparse event graphs but not this biological weighted-message quantization claim; hardware latency/energy remains unmeasured.
