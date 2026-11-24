# Hardware profile

Probed 2026-11-05 11:15–11:20 +0800 on the user's local workstation. All commands run locally;
no remote compute, no credentials recorded.

## Host

| item | measured |
|---|---|
| OS | Windows (Git Bash shell) + WSL2 Ubuntu 22.04, kernel 6.18.33.2-microsoft-standard-WSL2 |
| CPU | 12 logical cores |
| Disk | C: 953 GB total, 513 GB free |
| GPU | NVIDIA GeForce RTX 3060, 12288 MiB, driver 591.74 |
| WSL GPU | `nvidia-smi` inside Ubuntu-22.04 returns the same RTX 3060 (pass-through works) |
| RAM | not separately measured; 12 GB GPU VRAM is the binding memory limit for the planned models |

## Conda environments (Windows, `C:/Users/xhf/miniconda3`)

| env | Python | torch | CUDA available | intended role |
|---|---|---|---|---|
| `base` | 3.13.13 | 2.11.0+cu128 | **True**, RTX 3060 | **primary experimental env** |
| `siigm` | 3.11.15 | 2.12.0+cu126 | True | fallback / third-party compatibility |
| `jiewu-research` | 3.13.13 | 2.11.0+cu128 | True | fallback |
| `dyg-cold` | 3.13.13 | 2.11.0+cu128 | True | fallback |
| `dyg-writing` | — | import failed | — | not used |
| `spikinggcn36` | 3.6.15 | 1.10.2+cpu | False | pinned legacy reproduction of SpikingGCN (graphgallery 0.7.2) |

## WSL environments (`~/miniconda3`)

| env | role |
|---|---|
| `spikg` | py3.8 + torch 2.1 + dgl 1.1.3; runs SpikeGraphormer / SpikeGCL / SGNNBench code that lacks Windows cp313 wheels |
| `autoresearchclaw` | py3.11.6 + torch 2.12.0; **contains no `autoresearchclaw` package** (`find_spec -> None`) → AutoResearchClaw stages are local-executor substitutions |
| `ros2_jazzy` | unrelated |

## Installed skill dependencies

Present: the full CCFA family (`ccf-pipeline-orchestrator`, `ccf-idea-optimizer`,
`ccf-literature-searcher`, `ccf-idea-reviewer`, `ccf-experiment-designer`, `ccf-paper-reviewer`,
`ccf-integrity-auditor`, `ccf-paper-writer`, `ccf-visual-composer`, `ccf-submission-checker`, ...),
plus `ml-paper-writing`, `paper-refine`, `paper-polish-workflow`, `humanizer`, `nature-figure`,
`nature-citation`, `citation-audit`, `paper-compile`, `paper-illustration-image2`.

Absent: `AutoResearchClaw` Python package, `spark-task-delegator`. `nature-figure` and
`paper-compile` are available for P8/P15, so those stages do not need a fallback.

## Device policy (contract C13)

The frozen protocol fixes one device per paired arm. CUDA is used where it is numerically safe and
materially faster; a CPU fallback is recorded explicitly in `results.csv` (`device` column) and in
`runs/<id>/config.yaml`. Rationale: in the companion project the same sparse-reduction code changed
PubMed ANN by +0.69 pp when moved to CUDA, because the early-stopping epoch changed. G0
(< 0.1 pp reproduction of Cora/PubMed T=8) decides which device is frozen for the paired arms;
mixed-device rows are never silently pooled.

## Runtime budget

Small Planetoid graphs (Cora 2708 / CiteSeer 3327 / PubMed 19717 nodes, 2-layer hidden-16/64 GCN)
are CPU-cheap per run; the cost driver is the **number of cells**, not a single run: 7 seeds ×
5 T values × 8 Table-1 rows × 3 graphs, plus 3 probes, three aggregation hosts and ≥3 direct-training
arms. Estimated wall clock is dominated by third-party direct-training reproductions. No single
experiment may exceed 24 GPU-hours without a prior report to the author. Scale repair, if needed:
reduce the largest graphs first, keep all 7 seeds and the full T grid, never drop a Table-1 row.
