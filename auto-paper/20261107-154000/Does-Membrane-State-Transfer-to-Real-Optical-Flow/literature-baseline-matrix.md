# Literature baseline matrix (round 001)

Master first-hand table: `fly-connectome-cvpr2027/literature/closest-work.md` (21 entries,
one UNVERIFIED NeuroGraphBench DOI NOT FOUND; do not cite until verified).

| Work | Role | Task / metric | Code | Note |
|---|---|---|---|---|
| arXiv:2610.10023 train-your-fly | `must-rerun` (base architecture) | static shape/number/color accuracy | public repo, cloned locally | our stateless baseline; official shapes 64.0% is literature context, not a full rerun |
| arXiv:2604.04033 topological sensitivity | `literature-context` + null protocol | MovingEdge, degree-preserving null | public | self-declared gaps: long horizon, multi-task, higher-order nulls |
| arXiv:2609.01330 connectome + spiking orientation maps | `literature-context` | neural response / orientation maps | not rerun | different output target |
| Lappalainen et al. Nature 2024 / flyvis | `literature-context` | neural response prediction | TuragaLab/flyvis | connectome-constrained, non-spiking |
| Dorkenwald / Schlegel Nature 2024 and MaleCNS / Cell 2026 | data provenance | connectome data | public | data sources only |
| DAVIS-2017 / MPI-Sintel dataset papers | `literature-context` | video / optical flow benchmarks | public datasets | new for round 001 |
| frame-stacked pixel or flow ridge | `oracle/upper-bound` | temporal direction accuracy | local | ceiling 0.988 on SYNTHETIC; real-domain ceiling not yet measured |
| stateless / A=0 / degree-preserving null | `internal-matched` | same split, same seeds | local `common.py` | decisive controls |

Honest gap: the published 64% figure is literature context, not a rerun of the full official training
pipeline in this run; the direct rerun is the local stateless baseline. A strong recent vision
baseline rerun remains a G6 improvement item, recorded rather than hidden.
