# Dataset access log

Verified 2026-11-05. Access decision: **direct-public** for every dataset used. No approval,
payment, NDA, IRB, institutional membership or "available on request" path is involved.

| Dataset | Direct access URL | Terms / licence | Size | Task and labels | Split | Friction | Decision |
|---|---|---|---|---|---|---|---|
| Cora | https://github.com/kimiyoung/planetoid/raw/master/data (`ind.cora.*`) | PyG docs give no explicit licence; source paper arXiv:1603.08861 | 2708 nodes, 10556 edges, 1433 features | 7-class node classification, accuracy | public 140/500/1000 | none | direct-public |
| CiteSeer | https://github.com/kimiyoung/planetoid/raw/master/data (`ind.citeseer.*`) | PyG docs give no explicit licence | 3327 nodes, 9104 edges, 3703 features | 6-class node classification, accuracy | public 120/500/1000 | none | direct-public |
| PubMed | https://github.com/kimiyoung/planetoid/raw/master/data (`ind.pubmed.*`) | PyG docs give no explicit licence | 19717 nodes, 88648 edges, 500 features | 3-class node classification, accuracy | public 60/500/1000 | none | direct-public |
| ogbn-arxiv | https://ogb.stanford.edu/docs/nodeprop/ (OGB loader); https://snap.stanford.edu/ogb/data/misc/ogbn_arxiv/titleabs.tsv.gz | **ODC-BY** (OGB official) | 169343 nodes, 1166243 edges, 128 features | 40-class node classification, accuracy | official temporal split (≤2017 / 2018 / ≥2019) | none | direct-public |
| chameleon | https://snap.stanford.edu/data/wikipedia.zip ; https://snap.stanford.edu/data/wikipedia-article-networks.html | SNAP page gives no explicit licence; Geom-GCN version GPL-3.0 | 2277 nodes, 31421 edges | 5-class node classification, accuracy | declared version, duplicates handled | none | direct-public |
| squirrel | https://snap.stanford.edu/data/wikipedia.zip | SNAP page gives no explicit licence | 5201 nodes, 198493 edges | 5-class node classification, accuracy | declared version, duplicates handled | none | direct-public |

Supplementary public split source (used only if a geom-gcn split is ever needed, and then labelled):
https://raw.githubusercontent.com/graphdml-uiuc-jlu/geom-gcn/master/splits/ .

## Rejected or restricted datasets

- Any variant requiring email approval, account vetting, institutional membership, payment or a
  private bucket was excluded before scenario selection; none was needed for this plan.
- SGNNBench's ogbn-proteins, Tmall and Patent settings are **not** selected: the benchmark itself
  reports out-of-memory or multi-day runs on 2×RTX 3090Ti, well beyond a single 12 GB card. They
  may appear only as labelled literature context, never as a measured arm.
- SpikeNet's large dynamic-graph settings are excluded from the main protocol for the same reason.

## Mandatory caveats

- Heterophily graphs: Platonov et al. (arXiv:2302.11640) show chameleon and squirrel contain many
  duplicate nodes. The manuscript must name the exact version and the de-duplication treatment;
  SGNNBench's filtered variants (Chameleon 890/8854, Squirrel 2223/46998) are a different protocol
  and cannot be silently pooled.
- Planetoid licence is not stated in PyG documentation; this is recorded as **unknown**, not
  asserted as permissive.
- A companion project previously encountered a truncated `ind.citeseer.graph` download (58953 B
  without a pickle STOP marker) where a complete 61987 B copy existed locally. All downloaded files
  are therefore checked for completeness and their byte sizes/hashes recorded in `runs/`.

Source pages accessed 2026-11-05: PyG Planetoid docs, PyG `planetoid.py` source, OGB nodeprop docs,
SNAP Wikipedia article networks, arXiv:2302.11640, HuggingFace NEExT data card.
