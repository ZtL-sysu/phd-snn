# phd-snn — PhD Spiking Graph Neural Network (GNN→SNN) Research Workspace

> **中文简介**：本仓库是博士阶段 **GNN→SNN 转换与脉冲图神经网络（Spiking GNN）** 研究的**顶层总控与全流程实验档案库**。仓库同步保存了跨 Agent 协作记忆（`AGENTS.md`、`collaboration/`）、多轮研究方向生成与可行性论证记录、完整的 `20261117-210314` **10-Idea 系统空白检索与 RTX 3060 全量机制实验**（含独立 CCFA 评分报告，以及 `LR-C05`、`CERT-C11`、`POS-C13` 三篇完成 P0–P21 的深度研究手稿与实验证据）、`Intra-Aggregation Misalignment` 与 `Operator-Agnostic Superpixel Vision-Graph Conversion` 等历史专题实验与稿件、以及 `claude-fable5.2` 外部方案导入与严格负证据验证记录。**原始数据集、模型权重（`.pt`/`.npz`）、含本地平台路径/凭证读取逻辑的 `legacy/`、第三方源码及已在子仓库单独发布的归档目录保留在本地，不上传至 GitHub。**

Parent PhD research hub and curated experiment archive for **Graph-to-Spiking Neural Network (GNN→SNN) conversion**, mechanism screening, theoretical error certificates, and negative-control studies.

---

## 1. Research Repository Ecosystem

Because this PhD track spans multiple distinct manuscripts and experimental branches, curated deliverables are organized across focused sibling repositories linked from this parent workspace:

| Repository | Visibility | Scope & Relationship to `phd-snn` |
|---|---|---|
| [`ZtL-sysu/phd-snn`](https://github.com/ZtL-sysu/phd-snn) *(this repo)* | Public | **Parent PhD workspace**: cross-agent collaboration memory (`AGENTS.md`, `collaboration/`), guidance contracts, 10-idea systematic gap sweep & RTX 3060 experiments, `LR-C05` / `CERT-C11` / `POS-C13` full P0–P21 packages, historical campaigns (`20261104`–`20261110`), and Fable 5.2 negative-evidence audits. |
| [`ZtL-sysu/gnn2snn-v2`](https://github.com/ZtL-sysu/gnn2snn-v2) | Public | **Flagship journal-track release**: pre-submission LaTeX + compiled PDFs of **Paper A** (*What Reproduces in Spiking Graph Neural Networks?*) and **Paper B** (*When Does Graph-to-Spiking Conversion Work?*), registered JSON results, f-submit S0–S10 audits, protocols, Fable 5.2 provenance snapshot, and follow-up `gtmc-grid` calibration branch. |
| [`ZtL-sysu/gnn2snn`](https://github.com/ZtL-sysu/gnn2snn) | Public | **Visual superpixel-graph conversion archive**: `MNIST` / `CIFAR10` fixed GCN & GatedGCN conversion fidelity archive, worktree branches (`main`, `paper/20261115-*`, `research/2026-11-14-*`), and historical `docs/resource-reorg-20261117` branch. |
| [`ZtL-sysu/phd-dongtaitu`](https://github.com/ZtL-sysu/phd-dongtaitu) | Public | **Doctoral proposal implementation (EDSGN)**: offline Event-Driven Spiking Dynamic Graph Networks for nonstationary temporal graph forecasting (`edsgn` package, preregistered protocols, P3 68-job baseline campaign evidence). |
| [`ZtL-sysu/fly-connectome-control-ladder`](https://github.com/ZtL-sysu/fly-connectome-control-ladder) | Public | **Connectome-constrained vision archive**: sanitized collaboration log, null-ladder experiments, and 23 independent review reports corresponding to local `fly-connectome-cvpr2027/`. |
| [`ZtL-sysu/gnn2snn-dynamic-graph`](https://github.com/ZtL-sysu/gnn2snn-dynamic-graph) | Public | Lightweight GNN→SNN conversion for dynamic graphs (Neurocomputing target). |

---

## 2. Portfolio of Research Campaigns & Honest Verdicts

Every campaign follows a strict **preregistered-gate, baseline-first, negative-evidence-preserved** protocol (no post-hoc threshold lowering; failed or below-threshold manuscripts remain documented as negative or diagnostic evidence).

| Campaign Directory | Topic / Manuscripts | Status & Honest Verdict |
|---|---|---|
| `auto-paper/20261028-171500/` | **Spiking-GNN Conversion (Paper A & Paper B)** + Cross-Subject EEG Probabilistic SNN guidance | **Flagship qualifying manuscripts.** Original conference run (`f-research-v1-run-20261028-174053-gnn-snn-conv`, local read-only nested git): Paper A (NeurIPS E&D, skill review **9/10**) and Paper B (CCF-A main ML, skill review **8/10**). Full journal-track upgrade (`f-research-v1-run-20261118-181848-journal-upgrade`, f-research P0–P21 + f-submit S0–S10 PASS) is published cleanly in [`ZtL-sysu/gnn2snn-v2`](https://github.com/ZtL-sysu/gnn2snn-v2). Neither paper has been submitted yet. |
| `auto-paper/20261104-060416/` | `predictive-laws-gnn2snn` — Predictive Laws of Graph-to-Spiking Conversion | Guidance contract, CCFA startup packet, novelty/theory/story audits. |
| `auto-paper/20261105-111502/` | *Intra-Aggregation Misalignment and Bound-Derived Latency Allocation for Graph ANN-to-SNN Conversion* | Complete `f-research-v1` run with LaTeX draft, PDF, CSV metrics, and experiment code (`deliverables/paper.tex`, `tex/main.tex`). |
| `auto-paper/20261105-204552/` | Round-1 CVPR 2027 screening across 6 GNN × SNN × Fly-Connectome × Vision ideas | **0 / 6 GO** (`ROUND-1-SUMMARY.md`). All 6 independent CCFA reviews and local smoke tests preserved as negative screening evidence. |
| `auto-paper/20261107-141018/` | `Spiking-Mechanisms-for-Temporal-Vision-in-a-Fly-Connectome-GNN` | Provisional experiment contract & verification log (related vision archive in `ZtL-sysu/fly-connectome-control-ladder`). |
| `auto-paper/20261107-154000/` | `Does-Membrane-State-Transfer-to-Real-Optical-Flow` | Multi-round optical-flow membrane-state transfer evidence & acceptance verdicts (`acceptance-verdict-*.md`). |
| `auto-paper/20261110-152407/` | *Converting Graph Neural Networks for Graph-Structured Vision: Exact Error Identity, Membrane Readout, and an Accuracy–Energy Frontier on Superpixel Graphs* | Operator-agnostic grid / frozen-graph vision / graph message-passing study (`G0–G8` passed with narrowing; companion visual archive in [`ZtL-sysu/gnn2snn`](https://github.com/ZtL-sysu/gnn2snn)). |
| `auto-paper/20261117-210314/` | **Systematic GNN→SNN Gap Sweep (19 candidates → 10 full RTX 3060 experiments) + 3 Deep-Dive P0–P21 Manuscripts (`LR-C05`, `CERT-C11`, `POS-C13`)** | **9/10 passed mechanism strong gates** (`SIGN-C04` failed heterophily +2pp target). Independent CCFA scoring ranked `LR-C05` (5.7), `CERT-C11` (5.2), `POS-C13` (5.0) highest; all three completed P0–P21 end-to-end (details in Section 3 below), retained as diagnostic/secondary manuscripts that do not replace Paper A/B. |
| `docs/research-plans/claude-fable5.2/` | External Fable 5.2 plan import (13 Notion pages / 115 literature entries) + *Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs* (`20261118-120146`) | **Honest negative evidence.** Dynamic Vision Graph V2 rejected (independent review **3/10**; strong baseline ties & structural metric inconsistency). Follow-up NTU delta, residual-debt streaming GNN, fair-energy, and E(3) QM9 O(3) pilots also failed hard gates and are preserved transparently. |

---

## 3. Highlight: `auto-paper/20261117-210314/` — 10-Idea Matrix & Three P0–P21 Manuscripts

### 3.1 Ten-Mechanism Full RTX 3060 Experiment Matrix

Full report: [`auto-paper/20261117-210314/full-experiments/f-research-v1-run-20261117-220203-ten-idea-full/deliverables/ten-idea-full-experiment-and-ccfa-review.md`](auto-paper/20261117-210314/full-experiments/f-research-v1-run-20261117-220203-ten-idea-full/deliverables/ten-idea-full-experiment-and-ccfa-review.md)

Out of 19 candidates evaluated (`candidates/`, `rejections/`, `rejection-summary.md`), 10 passed frozen smoke tests (`smoke/tests` 32/32 PASS) and ran full matrices on local NVIDIA RTX 3060 12GB (`P0–P5A` PASS, 13/13 tests, 34 JSON artifacts):

| ID | Mechanism | Key Observed Result | Mechanism Gate | Independent CCFA Score |
|---|---|---|---|---|
| `LR-C05` | Operator-aligned low-rank graph message events | Rank-128 compression 7.32×–11.64×; SVD logit error 3.79×–6.20× below random | PASS | **5.7** |
| `CERT-C11` | Rowwise / layerwise graph-aggregation error certificates | 100% coverage; width/RMS 3.06–6.72, 79.7%–85.1% tighter than global bound | PASS | **5.2** |
| `POS-C13` | Permutation-equivariant hybrid hop-position event coding | 8-level Lloyd + 0.5% escapes; 2.46%/3.06% error, 10.17× storage cut, +2.13/+2.20pp acc | PASS | **5.0** |
| `EDGE-C06` | Non-uniform low-bit log-alphabet edge-weight events | 6-bit log error 2.82%, 5.33× storage reduction vs. 83.2% uniform error | PASS | 4.5 |
| `EQ-C02` | Radial-magnitude event + coordinate-frame rotation equivariance | Rotation error $2.91\times 10^{-11}$; balanced acc 25.99% vs. raw 24.35% | PASS | 4.2 |
| `DYN-C01` | Causal frame + membrane-state residual updates | Exact raw accuracy across 5 seeds; 20.52% fewer state-update events | PASS | 3.4 |
| `PERM-C03` | Graph event-pooling permutation certificate | Max error $1.11\times 10^{-16}$ across 3 graphs × 5 permutations vs. 0.50–0.95 naive | PASS | 3.1 |
| `READ-C18` | Top-two margin-pair graph readout | 100% prediction preservation across 6 graphs × 3 seeds; 63.33% median slot reduction | PASS | 2.7 |
| `DLY-C14` | Delay-aligned causal edge residuals | Exact reconstruction at matched delay (4.33% wrong-delay error); 20.52% event cut | PASS | 2.3 |
| `SIGN-C04` | Excitatory/inhibitory dual-polarity signed messages | Exact reconstruction, but only +0.46/+0.48pp on Chameleon/Squirrel (target +2pp) | **FAIL** | 1.9 |

### 3.2 Selected Deep-Dive P0–P21 Manuscripts (`auto-paper/20261117-210314/full-experiments/selected/`)

1. **`LR-C05`** — *Magnitude-Weighted Output-Jacobian Residual Coding of $M_0=\hat{A}X$ for Matched-Budget GNN-to-SNN Logit Fidelity*
   - Deliverable: `.../LR-C05/f-research-v1-run-20261118-004321-lr-logit-fidelity-v3/deliverables/LR-C05-final-v1/` (clean-extraction `paper.tex` + `paper.pdf`, figures, source CSVs, `ccfa-full-paper-review.md` [calibrated 5/10], `ccfa-full-integrity-audit.md`).
2. **`CERT-C11`** — *Rowwise Layerwise Interval Certificates for Quantized Messages in Frozen Two-Layer GNN-to-SNN Conversion*
   - Deliverable: `.../CERT-C11/f-research-v1-run-20261118-093658-cert-rowwise-interval-v6/deliverables/CERT-C11-final-v1/` (iterated v2 → v6 with full audits, corrections, tests, `paper.tex` + `paper.pdf`).
3. **`POS-C13`** — *Permutation-Equivariant Hybrid Hop-Message Coding for Frozen Graph Positional Representations*
   - Deliverable: `.../POS-C13/f-research-v1-run-20261118-113346-pos-hop-event-controls-v3/deliverables/POS-C13-final-v2/` (clean-build `paper.tex` + `paper.pdf`; `POS-C13-final-v1` is retained explicitly as a negative recovery record).

---

## 4. Repository Structure

```text
phd-snn/
├── README.md                                  # This master overview & repository index
├── AGENTS.md                                  # Multi-agent workspace rules & resume entry protocol
├── .gitignore                                 # Excludes datasets, weights, nested git repos, legacy/
├── collaboration/
│   ├── STATE.md                               # Project state, key decisions, verified facts, blockers
│   ├── TASKS.md                               # Cross-agent task ledger
│   └── agents/                                # 9 chronological handoff logs (Codex & Claude sessions)
│       ├── codex-reorg-20261117.md
│       ├── codex-idea-smoke-20261117.md
│       ├── codex-full-experiments-20261117.md
│       ├── codex-score5-full-pipeline-20261117.md
│       ├── codex-ccfa-integrity-auditor-20261118.md
│       ├── codex-ccfa-full-review-20261118.md
│       ├── codex-claude-fable5.2-import-20261118.md
│       ├── codex-fable5-research-20261118.md
│       └── claude-journal-upgrade-20261118.md
├── docs/
│   ├── agent-prompts/                         # Core briefs & teacher-probe prompts
│   └── research-plans/claude-fable5.2/        # Fable 5.2 Notion export, metadata & dynamic-ViG negative runs
├── paper/
│   └── cvpr2027/ccfa-review-run-20261115/     # Citation fetching utility
└── auto-paper/
    ├── generated-research-directions.md       # Master direction index maintained by f-guidance-builder-v1
    ├── 20261028-171500/                       # Spiking-GNN-Conversion guidance v1–v3, results & EEG guidance
    ├── 20261104-060416/                       # Predictive laws contract & startup packet
    ├── 20261105-111502/                       # Intra-Aggregation Misalignment full run & TeX/PDF draft
    ├── 20261105-204552/                       # Round-1 CVPR 2027 6-idea screening (0/6 GO, negative evidence)
    ├── 20261107-141018/                       # Fly-connectome temporal vision provisional contract
    ├── 20261107-154000/                       # Optical-flow membrane-state transfer verdicts & evidence
    ├── 20261110-152407/                       # Operator-agnostic vision & graph conversion study
    └── 20261117-210314/                       # 19-candidate sweep, 10-idea RTX 3060 matrix, LR-C05 / CERT-C11 / POS-C13
```

---

## 5. Multi-Agent Collaboration & Reproducibility Notes

### Resume Protocol (`AGENTS.md`)

1. Read `AGENTS.md` → `collaboration/STATE.md` → `collaboration/TASKS.md` → relevant `collaboration/agents/*.md` before modifying experiments or drafts.
2. Verify numbers directly against frozen JSON/CSV evidence files; never rely on stale status text.
3. Preserve all negative results and failed gates; never silently overwrite prior runs or lower preregistered thresholds.

### Local Execution Environment & Cloning

- **Cloning on Windows:** Some nested experiment paths under `docs/research-plans/claude-fable5.2/auto-paper/` exceed Windows' legacy 260-character path limit; clone with long paths enabled:
  ```bash
  git clone -c core.longpaths=true https://github.com/ZtL-sysu/phd-snn.git
  ```
- **Python / Conda:** Conda environment `dyg-cold` (Python 3.11+, PyTorch 2.x with CUDA 12.8 on local NVIDIA RTX 3060 12GB, or Apple Silicon MPS where applicable), PyTorch Geometric (`torch_geometric`), `numpy`, `scipy`, `matplotlib`, `pytest`.
- **LaTeX:** TeX Live (`latexmk -pdf -interaction=nonstopmode`) for compiling clean-extraction manuscripts under `auto-paper/`.
- **Datasets (local-only, auto-downloaded or externally obtained):** Planetoid (`Cora`, `CiteSeer`, `PubMed`), Geom-GCN (`Chameleon`, `Squirrel`), `ogbn-arxiv`, PyG superpixel `MNIST` / `CIFAR10`, `DAVIS-2017`, `MaleCNS` / `FlyWire` connectome graphs, and `QM9`.

---

## 6. Intentionally Excluded Local-Only Directories & Artifacts

To keep the public GitHub repository clean, secure, and lightweight (no datasets, no checkpoints, no credentials, no broken nested gitlinks), the following local directories and file patterns are excluded via `.gitignore`:

- **Datasets & Model Weights (~17 GB+ locally):** `data/`, `datasets/`, `pyg_bench/`, `ogbn_arxiv/`, `full_teacher_runs/`, `checkpoints/`, `weights/`, and binary formats (`*.pt`, `*.pth`, `*.ckpt`, `*.npz`, `*.npy`, `*.zip`, `*.tar`, `*.gz`, `*.bin`, `*.pkl`, `*.model`, `*.tif`/`*.tiff`). Local SHA-256 inventory manifests reside in local `archive-gnn2snn/gnn2snn-prep-archive/manifests/`.
- **Dedicated Sibling Repositories (avoiding duplication & nested `.git` gitlinks):**
  - `auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261118-181848-journal-upgrade/` → curated, path-scrubbed publication at [`ZtL-sysu/gnn2snn-v2`](https://github.com/ZtL-sysu/gnn2snn-v2).
  - `archive-gnn2snn/` (local worktrees of `gnn2snn` + `ANN-to-SNN-DCGS` reference) → upstream at [`ZtL-sysu/gnn2snn`](https://github.com/ZtL-sysu/gnn2snn).
  - `fly-connectome-cvpr2027/` → sanitized public release at [`ZtL-sysu/fly-connectome-control-ladder`](https://github.com/ZtL-sysu/fly-connectome-control-ladder).
  - `docs/research-plans/claude-fable5.2/github-gnn2gsnn/` → upstream [`Casey-sketch-cyber/gnn2gsnn`](https://github.com/Casey-sketch-cyber/gnn2gsnn) (pinned at `14f616f`; non-git snapshot also archived in `gnn2snn-v2/fable-material/`).
- **Read-Only Prior Nested Repository:** `auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv/` (local read-only git repo containing the original conference drafts of Paper A & B; untouched to preserve its read-only protection and avoid committing a broken submodule link).
- **Platform Evidence, Third-Party Clones & Ephemeral Caches:** `legacy/` (3.1 GB; historical Novix platform scripts/logs that may contain platform token loaders or local paths — never uploaded), `third_party/` (upstream `SpikeGraphormer` clone), `pull003/`, `tmp/`, `output/`, `.researchclaw_cache/`, `.workbuddy/`, `novix/pulled/`, raw `*.log` streams, and LaTeX build intermediates.
