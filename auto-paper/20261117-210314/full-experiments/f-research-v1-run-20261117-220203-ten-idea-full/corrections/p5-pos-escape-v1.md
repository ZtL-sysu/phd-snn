# Correction: POS hybrid escape codebook

- Trigger: full POS Lloyd codebook retained 6.57–6.69% relative error, above the frozen 5% strong threshold.
- Repair: keep the 8-level Lloyd codebook and add exact float32 escape events for the largest 0.5% errors. Average cost is explicitly `(0.995*3 + 0.005*32) = 3.145` bits/element.
- Gate change: none. Error must remain ≤5%, storage reduction ≥4×, and task accuracy non-inferior to raw.
- Result: final `methods-POS-C13.json` reports 2.46%/3.06% error, 10.17× storage reduction and positive balanced-accuracy deltas.
