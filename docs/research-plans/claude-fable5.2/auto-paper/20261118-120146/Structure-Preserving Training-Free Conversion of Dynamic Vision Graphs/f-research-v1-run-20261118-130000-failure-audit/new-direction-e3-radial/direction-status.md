# E(3) radial-event new direction: implementation-blocked

- Public CC0 QM9 data were downloaded and parsed successfully at the container level: `qm9.sdf` (252,425,350 bytes), `qm9.sdf.csv` (27,685,401 bytes), parquet metadata (133,885 rows).
- A first O(3) radial-event classification pilot completed and FAILED its pre-registered gate: radial8 beat component8 on only 2/5 seeds, mean gain was about 0.2pp (<2pp), and equivariance error was 1.27e-6 (>1e-6). Evidence: `new-direction-gate.json`.
- A second vector-regression pilot remained implementation-blocked because local SDF header parsing dropped almost all molecules. No scientific claim is made from it.
- Decision: do not start a paper from this direction. Preserve data, scripts, and negative/blocked evidence.
