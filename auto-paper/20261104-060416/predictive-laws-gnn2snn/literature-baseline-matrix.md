# Literature–baseline matrix

Role vocabulary — `must-rerun` (we run it ourselves), `adaptation-attempt` (we re-implement the
published formulation and say so), `internal-matched` (same architecture, different training
paradigm), `oracle/upper-bound`, `literature-context` (numbers we quote but never compare directly).

| method | year / venue | official URL | task / metric | code | checkpoint | local rerun | role | why included |
|---|---|---|---|---|---|---|---|---|
| SpikingGCN | 2022 / IJCAI | github.com/ZulunZhu/SpikingGCN | node classification, accuracy | yes (Python 3.6, graphgallery 0.7.2) | none | **no** — dependency stack unavailable | `adaptation-attempt` | the canonical formulation; we re-implement SGC-2 propagation + 512-wide spiking layer |
| Direct BPTT spiking GCN | 2021–2024, multiple | n/a | node classification | our own | n/a | yes | `internal-matched` + `must-rerun` | the strongest same-architecture competitor; retrained per T |
| Rate-coded (Poisson) spiking GCN | 2022 / IJCAI (formulation) | as SpikingGCN | node classification | our own | n/a | yes | `adaptation-attempt` | isolates input coding from architecture |
| SiGNN | 2024 / arXiv 2404.07941 | github.com | dynamic-graph representation | yes | none | no — different task and splits | `literature-context` | nearest trained spiking GNN by name; not comparable on our task |
| SGNNBench | 2025 / arXiv 2509.21342 | repo + paper tables | unified evaluation | yes | none | no — different protocol | `literature-context` | the only unified protocol we could align to; used to argue the gap, never to claim a win |
| SpikeGraphormer | 2024 / arXiv 2403.15480 | github.com | graph transformer | yes | none | no — attention breaks the fixed-operator assumption | `literature-context` | explains why attention is out of scope rather than ignored |
| GCNII | 2020 / ICML | github.com/chennnnnyize/GCNII | node classification | yes | none | **yes** (implemented in `experiments/core.py`) | `oracle/upper-bound` | the depth backbone a reviewer expects us to try; we try it and report that it does not convert |
| DAGNN | 2020 / KDD | github.com/liandlt/DAGNN | node classification | yes | none | **yes** (implemented) | `oracle/upper-bound` | raises Cora's ANN to 0.845 and *lowers* converted accuracy; reported as a failed branch |
| GCN / SGC / APPNP | 2017–2019 | — | node classification | yes | — | yes | `simple_baseline` | the ANN reference and the propagation family |
| FTBC | 2024 / ECCV | arXiv 2407.…. | conversion bias | partial | none | formulation-level | `literature-context` | mechanism ancestor; must be cited explicitly |
| Temporal misalignment + TPP | 2025 / ICML | arXiv 2502.14487 | conversion, dense | partial | none | TPP implemented as an ablation arm | `internal-matched` | the paper we must not be confused with |

## What the matrix forces into the paper

1. The comparison table must label every row `codebase-reproduction` or `formulation-reimplementation`.
   We have **zero** of the former, and the caption must say so in those words.
2. The published architecture that beats us (0.8169 / 0.7073 / 0.7603 vs our 0.8046 / 0.6907 / 0.7771)
   stays in the table. Removing a measured unfavourable row is the one edit that would make the whole
   paper untrustworthy, so the guidance forbids it explicitly.
3. SGNNBench numbers appear only as context with a protocol note, never as a row we claim to beat.

## G6 verdict

Passed with a labelled limitation. At least one strong recent domain baseline (the SpikingGCN
architecture) is a direct adaptation attempt run locally at 7 seeds, and two more (direct BPTT,
rate-coded) are `must-rerun`. Literature-only baselines are separated in a different table with a
protocol note.
