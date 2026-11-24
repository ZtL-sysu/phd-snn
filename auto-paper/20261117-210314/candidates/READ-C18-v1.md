# READ-C18-v1 — top-two margin-pair graph readout events

Hypothesis: graph-level conversion need not emit events for every class; transmitting the leading class and its strongest competitor as a signed margin pair preserves the converted argmax while reducing output event slots.

Smoke: six local graph datasets, frozen checkpoints, T=2 converted logits, validation masks. Gate: predictions preserved exactly on every graph and median output-slot reduction ≥50% versus all-class readout.

Novelty boundary: One-Spike and generic conversion use full output mappings; the narrow contribution is a certified graph-readout event compression. It does not reduce hidden message work.
