# P2 — local environment, commands and accelerator decision

## Measured environment

| item | value |
|---|---|
| host | Windows, 12 logical cores, 513 GB free disk |
| GPU | RTX 3060 12 GB, driver 591.74; WSL2 GPU pass-through confirmed |
| primary env | `C:/Users/xhf/miniconda3` env `base` |
| Python | 3.13.13 |
| numpy / scipy / torch / PyG | 2.4.4 / 1.18.0 / 2.11.0+cu128 / 2.8.1 |
| CUDA available | True (verified by `torch.cuda.is_available()` and `get_device_name(0)`) |
| WSL env | `spikg` (py3.8, torch 2.1, dgl 1.1.3) for third-party spiking-GNN code |
| legacy env | `spikinggcn36` (py3.6, torch 1.10.2+cpu) for official SpikingGCN |

## Runnable commands (all local)

| purpose | command |
|---|---|
| G0 reproduction | `conda run -n base python experiments/wp0_reproduce.py` |
| S1 probes | `conda run -n base python experiments/s1_probe.py` |
| Table 1 / hosts | `conda run -n base python experiments/tables.py` |
| bound and `T*` | `conda run -n base python experiments/latency_alloc.py` |
| third-party arms | `MSYS_NO_PATHCONV=1 wsl -d Ubuntu-22.04 -- bash <script>.sh` inside `spikg` |
| legacy SpikingGCN | `conda run -n spikinggcn36 python ...` |

Long jobs are launched as background shell tasks with output redirected to `runs/*.log`; no
`head`/`timeout` truncation is used (a closed pipe would kill the job).

## Accelerator decision (contract C13)

**Frozen device for paired numeric arms: CPU.** Rationale: the companion project measured a
+0.69 pp PubMed ANN shift when the same sparse-reduction code ran on CUDA, because the reduction
order changed the early-stopping epoch. That shift exceeds the 0.8 pp decision threshold used
throughout this paper. The G0 reproduction here on CPU matched the frozen numbers to 0.003 pp,
which licenses the CPU choice.

GPU is authorized and will be used for:
- third-party direct-training arms whose own published code expects CUDA, provided the arm is not
  pooled with CPU conversion rows without a device column;
- ogbn-arxiv scale cells where a CPU run would exceed the budget, after a shared-cell identity
  check on a small graph;
- any arm where a re-run on both devices agrees within the 0.1 pp G0 tolerance.

"不行的拉到": where CUDA changes the number or a dependency lacks a Windows wheel, an explicit CPU
or WSL fallback is recorded in `config.yaml` and in the `device` column. No silent mixed-device
pooling.

## Setup checks performed

| check | result |
|---|---|
| `import core` and `core.load("cora")` | PASS, N=2708 F=1433 E=5278 |
| all 24 Planetoid raw files present with hashes | PASS |
| G0 reproduction < 0.1 pp on both graphs | PASS (see `notes/S0_foundation.md`) |
| `registry/results.csv` schema and 14 G0 rows | PASS |
| WSL `nvidia-smi` | PASS (same RTX 3060 visible) |
| AutoResearchClaw package | **absent** → local-executor substitution recorded |
| writing/figure/compile skills | present (ml-paper-writing, paper-refine, humanizer, nature-figure, paper-compile, citation-audit) |

## Artifact paths

`protocols/protocol.md`, `registry/registry.md`, `registry/results.csv`, `runs/<run_id>/`,
`results/`, `figures/`, `tex/`, `deliverables/`. All inside the run root; see
`audits/path-manifest.md`. No external sync is required for G0/S1; third-party outputs at P4 will
be copied into `runs/` before any claim uses them.

**P2 gate verdict: PASS.** Runnable protocols, local environment checks, commands, accelerator
decision and artifact paths all exist in the run root.
