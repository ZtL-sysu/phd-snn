# Dataset access log

All datasets are directly downloadable with no approval flow, no NDA and no application form. Access
verified 2026-11-04 by loading each from the local cache produced earlier by the same scripts.

| dataset | source / direct access URL | licence / terms | split used | N / E / classes | status |
|---|---|---|---|---|---|
| Cora | https://github.com/kimiyoung/planetoid (`data/ind.cora.*`) | public research data, no explicit licence file; widely redistributed | Planetoid public 140/500/1000 | 2708 / 5278 / 7 | downloaded, cached |
| CiteSeer | same repository (`ind.citeseer.*`) | as above | Planetoid public 120/500/1000 | 3327 / 4552 / 6 | downloaded, cached |
| PubMed | same repository (`ind.pubmed.*`, npz) | as above | Planetoid public 60/500/1000 | 19717 / 44324 / 3 | downloaded, cached |
| ogbn-arxiv | https://ogb.stanford.edu/docs/nodeprop/ (raw csv.gz) | OGB terms, research use | official time split 90941/29799/48603 | 169343 / 1166243 / 40 | downloaded, cached |
| chameleon | PyG `WikipediaNetwork` (https://pytorch-geometric.readthedocs.io) | research use | Geom-GCN split 0 (48/32/20) | 2277 / 31371 / 5 | downloaded, cached |
| squirrel | same | research use | Geom-GCN split 0 | 5201 / 198353 / 5 | downloaded, cached |

## Rejected

- **A flood-extent graph** from the predecessor guidance: no directly public, correctly licensed
  version at the required size; would need an institutional request. Rejected under G1 and replaced
  by ogbn-arxiv plus the two heterophilic graphs.
- **OGB-Products / Papers100M**: public, but the conversion simulation is NumPy and a single
  `T=32` sweep at 2.5 M nodes exceeds the 32 GB budget by an order of magnitude. Not rejected for
  access reasons; excluded on G5.

## Notes on reproducibility

Planetoid files are the original pickle/npz artefacts, not a re-packed mirror, so the public split is
the one every baseline paper uses. `graph_data.py` binarises duplicate edges before normalising
because CSR construction sums duplicates while the reference loader assigns 1.0; that difference alone
moved CiteSeer's ANN by 0.4 pp and is documented at the call site.
