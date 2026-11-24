# Reaccepted external assets (contract C9)

All assets below came from the companion run root
`C:/code/phd-snn/auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv/`
at git commit **`d12511207b1f0f1ee49650ec560de5236942c419`** (2026-11-05). They were copied
byte-for-byte into **this** run root. No runtime code path refers back to the companion directory.
Reacceptance requires that data, splits, code, config, seeds, environment and gate criteria still
match; that check is recorded per gate below.

## Code assets (sha256)

| local path | sha256 | source | why reaccepted |
|---|---|---|---|
| `experiments/core.py` | `e2f0b0a29b09ff60878c8975b8971fef7cbbca659368f0e054400e71bc7e86e4` | companion `experiments/core.py` | L-layer ANN + conversion kernel; its own header records a 0.000–0.003 pp reproduction of the shipped Cora/PubMed numbers on CPU with 7 seeds |
| `protocols/graph_data.py` | `78b73c666b8967ca3bcac4d4ec512c57cc41bbf1a057ae5e7cf3c77ad64f12b3` | companion `protocols/graph_data.py` | sparse graph-data hub; loads the same Planetoid public splits |
| `registry/log_run.py` | `71cfb2e1b80e6b973cdb8df325910b200d3465eec5501c30f4f544948c3ed6e0` | companion `registry/log_run.py` | kept for reference; **this run writes its own rows** with content-addressed traceability |
| `protocols/protocol.companion-snapshot.md` | see file | companion `experiments/protocol.md` | read-only record of the earlier frozen protocol; not the active protocol |

## Data assets

24 `ind.{cora,citeseer,pubmed}.{x,tx,allx,y,ty,ally,graph,test.index}` files copied into
`results/.data/`. Examples (sha256):

| file | sha256 |
|---|---|
| `ind.cora.allx` | `9419ba2f26f5c35243db64aba110e0f35a04851609e0dc5433450676ca6b8543` |
| `ind.cora.ally` | `2b998f5cc7fedc86e7f97ca2498f47a1ffc1462c29e2d578b23bf3f62b6e7d71` |
| `ind.cora.graph` | `58f13302f39dde8852dad6fe6d15b89b077b6d7f837626bce671ef80344b383d` |
| `ind.cora.test.index` | `297ce89af2b51a6a194181c7dbe1796c6a1cf9cd9349a88383b1b1e227867875` |
| `ind.cora.tx` | `b9afbaa4a400df991f6f02ef677e1e44da55ffc04801fd02f9e673987829226a` |

The full hash list is written into every `runs/<id>/config.yaml` at execution time. The
CiteSeer graph file is the **complete** 61987-byte version (the companion project previously
encountered a truncated 58953-byte download); completeness is checked on load.

## Applicability re-check

| item | companion | this run | match |
|---|---|---|---|
| split | Planetoid public 140/500/1000 etc. | same (frozen in `protocols/protocol.md`) | yes |
| seeds | 0–6 | 0–6, never extended | yes |
| T grid | {2,4,6,8,16,32} in the companion brief | **{2,4,8,16,32}** per the new task book | **changed, recorded** |
| device | CPU frozen | CPU frozen for paired arms; GPU only where verified identical | yes, with logged extension |
| backend | numpy/scipy/torch CPU | numpy 2.4.4 / scipy 1.18.0 / torch 2.11.0+cu128 on Windows | minor version change; G0 reproduction <0.1 pp is the acceptance test |
| code | files above | byte-identical copies | yes |

Because the T grid and the numeric library versions differ, **no companion result is transferred
as a result of this run**. Companion measurements appear only as `calibration_evidence` in the
feasibility contract and as explicitly labelled external anchors. Every main-table number is
regenerated here from `results.csv`.

## Verification performed at P0

`python -c "import core; core.load('cora')"` returned `N=2708, F=1433, E=5278`, matching the
expected Planetoid shape. NumPy emits a `VisibleDeprecationWarning` from pickle loading under
2.4.4; it does not change the data and is recorded rather than suppressed silently.
