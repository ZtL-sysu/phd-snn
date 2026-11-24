# Seed-level v2 accuracy correction

The statement that message-aware v2 reaches **78.83% for every seed** is false. `v2-message-calibration-results.json` reports:

| Seed | v2 accuracy |
|---:|---:|
| 41 | 78.40% |
| 42 | 78.35% |
| 43 | 79.75% |

The correct summary is **78.83% mean accuracy** (equivalently 78.8333...%), not a per-seed constant. Replace the phrase with: "message-aware calibration reaches 78.40%, 78.35%, and 79.75% on seeds 41, 42, and 43 (mean 78.83%)." No manuscript files were modified.
