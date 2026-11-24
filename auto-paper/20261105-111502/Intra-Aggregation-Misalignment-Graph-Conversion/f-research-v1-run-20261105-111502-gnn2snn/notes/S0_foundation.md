# S0 / G0 — foundation report

Date: 2026-11-05. This is the first stage report of the new run. **Next stage: S1 (P3/P4).**

## What was built

- Run root inside the guidance directory, with `protocols/`, `experiments/`, `registry/`,
  `results/.data/`, `runs/`, `audits/`, `notes/`, `figures/`, `tex/`, `writing/`,
  `deliverables/`, `contracts/`.
- Two ordered ledgers: the guidance 12-stage ledger (all passed, `--workflow-complete` PASS) and
  the f-research P0–P21 ledger (P0–P2 passed here).
- Frozen `protocols/protocol.md`: Planetoid public splits, seeds 0–6, T grid {2,4,8,16,32},
  paired bootstrap CI, noise floor 0.4 pp / 2× rule, device frozen per paired arm, content-
  addressed traceability, proxy-only efficiency metrics.
- `registry/results.csv` with the task-book §11.2 schema plus a `device` column;
  `registry/registry.md` with all five pre-registrations (R0–R4) written before any experiment.
- Reaccepted external assets: `core.py`, `graph_data.py`, `log_run.py` and 24 Planetoid files,
  copied byte-for-byte from companion commit `d12511207b1f0f1ee49650ec560de5236942c419`, with
  sha256 bindings in `audits/reaccepted-assets.md`. No runtime path points back to the companion.
- `audits/traceability-policy.md`: because the pipeline forbids unauthorized commits, every run
  uses a content-addressed trace id over code and data hashes instead of a git commit.

## G0 gate result — PASS

Command: `conda run -n base python experiments/wp0_reproduce.py` (device=cpu, 7 seeds, T=8,
hidden=16, 2 layers). Runtime 2m30s. Log: `runs/wp0_gate_stdout.log` and
`runs/wp0-repro-*/{config.yaml,log.txt,metrics.json}`. Raw: `results/wp0_repro.json`.

| dataset | ANN reproduced | ANN frozen | Δ pp | T=8 reproduced | T=8 frozen | Δ pp | verdict |
|---|---|---|---|---|---|---|---|
| Cora | 0.8060 | 0.8060 | +0.000 | 0.8026 | 0.8026 | −0.003 | PASS |
| PubMed | 0.7757 | 0.7757 | +0.001 | 0.7740 | 0.7740 | +0.000 | PASS |

All four deviations are far inside the 0.1 pp tolerance. This confirms that the copied kernel,
the copied Planetoid files, the frozen CPU device and Windows `base` (Python 3.13.13, numpy
2.4.4, scipy 1.18.0, torch 2.11.0+cu128) form the same numerical pipeline that produced the
frozen task-book numbers, despite the library version change.

14 rows were written to `registry/results.csv` (7 seeds × 2 datasets), each with a
`content:<sha256>` trace id, spike count, SynOps proxy, training seconds and device.

## Warnings observed (recorded, not suppressed)

- `VisibleDeprecationWarning` from pickle loading under NumPy 2.4.4 (`align=0`): does not change
  the data; G0's exact reproduction confirms it.
- PyTorch `UserWarning` about implicitly disabled sparse invariant checks in `train_ann`: the
  kernel's own design note; no numeric effect observed.

## Gate status

| gate | result |
|---|---|
| G0 (task book S0) reproduction < 0.1 pp | **PASS** |
| P0 run root and manifest | PASS |
| P1 guidance validation (`--strict --packet`) | PASS |
| P1A strong-result feasibility lock (4/4 claims) | PASS |
| P1B pre-experiment review + planned-evidence integrity audit | PASS |
| P2 protocols, environment, accelerator decision, setup check | PASS |

**Device decision:** CPU is frozen for all paired conversion arms. CUDA is available (RTX 3060
12 GB, and WSL2 pass-through) but the companion measured a +0.69 pp PubMed ANN shift when sparse
reduction moved to GPU, larger than every effect size in this paper. GPU will be used only for
compute-heavy arms after a verified-identical number check on a shared cell; otherwise the CPU
fallback is explicit. This honours "能上gpu的就上去，不行的拉到" without mixing devices in a table.

## Open items carried into S1

- Implement `probes.py` (inter-layer permutation, intra-aggregation phase randomisation) and
  `tpp_neuron.py` from ICML'25 equations (8)–(13); the official TPP codebase is unreleased.
- Unit-test the TPP neuron against the frozen T=8 Cora value 0.7756 ± 0.5 pp before the full grid.
- Run the S1 2×2 design and four-way control; **branch C or D stops the campaign and reports to
  the author** (task book GP, contract C2).
- Acquire ogbn-arxiv / heterophily caches at P4 with hashes recorded; the 292 MB companion cache
  is not copied yet because no claim needs it before C3.

No submission, upload or publication action was taken. `submission_ready` remains false.
