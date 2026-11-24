# Path-containment manifest (P0)

Run root: `C:/code/phd-snn/auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/f-research-v1-run-20261105-111502-gnn2snn/`
Guidance directory (parent of the paper-title folder) contains `guidance.md`; the run root is
**inside** that directory, satisfying the f-research-v1 artifact boundary.

| artifact class | path under run root | status |
|---|---|---|
| run-local execution contract | `contracts/execution-contract-v1.md` | present |
| guidance snapshot | `contracts/guidance.snapshot.md` | to be copied |
| CCFA packet snapshot | `contracts/ccfa-startup-packet/` | to be copied |
| ordered JSON ledger | `pipeline-state.json` | initialized, 26 stages pending |
| readable ledger | `pipeline-state.md` | present |
| frozen protocol | `protocols/protocol.md` | P2 |
| companion protocol snapshot | `protocols/protocol.companion-snapshot.md` | copied |
| experiment code | `experiments/` | core.py copied, new scripts to be added |
| data hub | `protocols/graph_data.py` | copied |
| result registry | `registry/results.csv`, `registry/registry.md` | P2 |
| raw results | `results/*.json`, `results/.data/` | Planetoid raw files copied |
| per-run evidence | `runs/<run_id>/{config.yaml,log.txt,metrics.json}` | starts at G0 reproduction |
| audits and notes | `audits/`, `notes/` | present |
| figures | `figures/` | empty, P8 |
| manuscript | `tex/`, `writing/` | empty, P6+ |
| delivery | `deliverables/` | empty, P21 |

## External sources (explicitly recorded, never a deliverable location)

| source | use | sync rule |
|---|---|---|
| companion run root `.../f-research-v1-run-20261028-174053-gnn-snn-conv/` (git `d12511207b1f0f1ee49650ec560de5236942c419`) | `core.py`, `graph_data.py`, `log_run.py`, Planetoid raw files, companion protocol | copied byte-for-byte into this run root; hashes in `audits/reaccepted-assets.md`; no runtime dependency on the external path |
| WSL `spikg` / `spikinggcn36` environments | third-party spiking-GNN code at P3/P4 | any log or metric used for a claim is synchronized into `runs/` before acceptance |
| public dataset URLs | ogbn-arxiv / heterophily graphs at P4 | downloaded directly into `results/.data/`, hashes recorded |

No AutoResearchClaw external artifacts directory is used. No deliverable is written to a temp,
desktop, downloads, `auto-paper/` root or global cache location.

**Containment verdict:** `pending` until P0's first gate check; re-verified at P21 with a full
directory scan.
