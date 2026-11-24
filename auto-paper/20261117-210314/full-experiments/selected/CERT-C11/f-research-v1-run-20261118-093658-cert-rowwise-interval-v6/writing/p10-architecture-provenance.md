# Architecture provenance

`results/model-shapes.json` records tensor shapes for all nine frozen graph/checkpoint pairs. Every `W0` matrix has output dimension 16 and every `W1` matrix has input dimension 16, so the hidden-16 statement is directly traceable. Model snapshots are hash-listed in `provenance-manifest.json`.
