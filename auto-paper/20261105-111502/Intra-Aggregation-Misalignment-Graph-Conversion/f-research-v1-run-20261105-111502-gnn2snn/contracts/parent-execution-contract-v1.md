# execution-contract-v1 — immutable run-local contract

Version: v1. Established: 2026-11-05 11:15 +0800.
Status: **active**. Supersedes nothing; this is a new, independent paper run.
Run root: `C:/code/phd-snn/auto-paper/20261105-111502/Intra-Aggregation-Misalignment-Graph-Conversion/`

This file is immutable. Any change creates v2 and reopens the affected stage and its
entire downstream suffix under `references/execution-contract.md`.

## 1. User goal and exact authorization

> Instruction (2026-11-05): "我们现在做一篇新的论文，主题还是这个gnn2snn，这是最新的指导书
> `@agent_prompt_v2_ICML25.md`，允许你使用我的 `@skill:f-guidance-builder-v1` `@skill:f-research-v1`
> 进行文章的推进，指导书里与我的科研流水线冲突的地方以科研流水线为准，目标依然是
> `@skill:ccf-common` 的评分来到9分及以上。我们做实验的时候允许你用我的wsl，允许你用我的win下的conda，
> 能上gpu的就上去，不行的拉到。"

- **Scientific content contract**: `agent_prompt_v2_ICML25.md` (task book v3, ICML'25 TPP-aligned).
  Immutable snapshot: `contracts/agent_prompt_v2_ICML25.snapshot.md`.
- **Execution authority**: `f-guidance-builder-v1` (CCFA-startup → G0–G8 → validation → handoff)
  followed by `f-research-v1` (P0 → P21). `ccf-common` governs review/score language.
- **On any conflict, the research pipeline wins.** The adjudication table in §3 is binding.
- **Score target**: calibrated overall stance **≥ 9** from `ccf-paper-reviewer` in `full` mode.
  Per the user's standing correction (W9 of the companion project), no self-assigned scores count;
  only skill-generated reviews are recorded as scores. `ccf-common/references/review-output-standards.md`
  governs scorecards, confidence, evidence basis, repair conditions and the multi-reviewer panel.
- **Compute**: Windows Conda + WSL2, both authorized. CUDA must be used where it is numerically
  safe; CPU fallback is recorded where it is not. No remote/cloud compute, no credentials in files.
- **Not authorized**: submit, upload, publish, `git push`, or any external action. Local preparation only.

## 2. Scope, resources, envelope

| item | value |
|---|---|
| output root | the run root above; every deliverable/process file must live under it |
| guidance output root | run root (guidance.md + 7 audits + `ccfa-startup-packet/`) |
| f-research run root | `f-research-v1-run-20261105-111502-gnn2snn/` inside the run root |
| host | Windows, 12 logical cores, 953 GB disk (513 GB free) |
| GPU | NVIDIA GeForce RTX 3060, 12288 MiB, driver 591.74; WSL2 GPU pass-through confirmed (`nvidia-smi` visible in Ubuntu-22.04) |
| Win Conda | `C:/Users/xhf/miniconda3`; `base` py3.13.13 torch 2.11.0+cu128 CUDA True; `siigm` py3.11.15 torch 2.12.0+cu126 CUDA True; `jiewu-research` / `dyg-cold` py3.13.13 torch 2.11.0+cu128 CUDA True; `spikinggcn36` py3.6.15 torch 1.10.2+cpu (legacy third-party reproduction only) |
| WSL Conda | `~/miniconda3`, envs `spikg` (py3.8 torch 2.1 + dgl 1.1.3, third-party spiking-GNN code), `autoresearchclaw` (py3.11.6 torch 2.12.0 — **contains no ARC package**), `ros2_jazzy` |
| device rule | the frozen protocol must fix ONE device per experimental arm; see C13. GPU is used for compute-heavy arms that do not change the reproduced numbers; CPU fallback is explicit and logged |
| time | no schedule; stage gates only. Any single experiment > 24 GPU-hours requires prior report |

### Installed dependencies (recorded, not inferred)

- CCFA family: `ccf-common`, `ccf-pipeline-orchestrator`, `ccf-idea-optimizer`, `ccf-literature-searcher`,
  `ccf-idea-reviewer`, `ccf-experiment-designer`, `ccf-paper-reviewer`, `ccf-integrity-auditor`,
  `ccf-paper-writer`, `ccf-visual-composer`, `ccf-submission-checker`, `ccf-rebuttal-writer`, etc.
- Writing/figure/compile: `ml-paper-writing`, `paper-refine`, `paper-polish-workflow`, `humanizer`,
  `nature-figure`, `nature-citation`, `citation-audit`, `paper-compile`, `paper-illustration-image2`.
- **Absent**: `AutoResearchClaw` Python package (verified: `importlib.util.find_spec("autoresearchclaw") -> None`
  in the WSL env of that name and on Windows). Stages 16/17/18/19/20/22/23 therefore execute as
  **local-executor substitutions** with the same substantive gates, recorded as such. They must never
  be reported as ARC tool calls. `spark-task-delegator` is likewise absent; no canonical stage is
  parallelized (only read-heavy research runs alongside).

## 3. Conflict adjudication (binding; research pipeline wins)

| id | task book | pipeline | adjudication |
|---|---|---|---|
| C1 | S0→S8 stage chain with its own gates; "no skipping" | f-research-v1 P0→P21 is the structural authority; guidance-builder has its own 12-stage ledger | **Two ledgers, one authority.** `pipeline-state.json` in run root = guidance 12 stages; `f-research-v1-run-*/pipeline-state.json` = P0–P21. S0–S8 survive as the **scientific experiment contract** mapped into P3/P4/P5/P8. Gates G0–G7 are re-verified as scientific criteria inside P5 (strong-result lock) and P5A (pre-draft review), not as a competing state machine. |
| C2 | "任一 Gate 不过：停手，写进 notes，报人类，禁止自行调整目标" | P1B/P3A/P5A must enter the autonomous correction loop; they may not terminate automation merely because a review fails. User direction only for material scope expansion | **Pipeline wins.** On a failed gate: preserve the review and all negative runs, run the correction loop (repair evidence / narrow a claim with a versioned contract / pivot inside the same method family and tier), never lower `expected_strong`, never invent numbers. Stop and report only when no candidate passes with public data and the verified envelope, or when a new method family, tier, private data, hardware, credentials or budget is required. |
| C3 | eight-section skeleton (Abstract / 1 Intro / 2 Related / 3 Method / 4 Theory / 5 Exp / 6 Limitations / Appendix); 8 pages + appendix | six numbered main sections exactly: `1 Introduction`, `2 Related Work`, `3 Method`, `4 Experiments and Results`, `5 Discussion`, `6 Conclusion`; no appendix added to satisfy page count; no research content after Conclusion | **Pipeline wins.** Theorem G1 lives in a §3 or §4 subsection; limitations become positive evidence boundaries inside §5 Discussion; abstract is unnumbered. An appendix carrying proofs, the full protocol table, hyperparameter grids and per-seed numbers is permitted because the task book and the ICML-style venue explicitly require it, but it carries no new research conclusion and is not used to absorb main-text content. 8-page main text retained as the length target. |
| C4 | Fig.1 = S1 phenomenon figure; Fig.2 = mechanism illustration from an image model; Fig.3 = acc vs T; exactly 3 main figures | P8: Figure 1 **must** be the overall framework/architecture figure generated directly with GPT image generation (`image2`); no fixed artifact count; data plots via `nature-figure` | **Pipeline wins.** Figure 1 = framework figure. The S1 phenomenon plot, the Pareto curves and the bound-vs-measured plot follow as scripted figures; no quota is imposed. |
| C5 | §5.3: every in-text number carries `% run: <run_id>`; tables generated by script; `TODO(run_id)` cleared before compile | identical in substance, plus `results.csv` as the single source and 0 untraced numeric tokens | **Union**: `% run:` comments + scripted tables + `registry/results.csv` + integrity audit (0 untraced) + `grep -rn "TODO("` clean. `run_id` refers to **this** run. |
| C6 | no citation count requirement | ≥ 36 distinct, verified, relevant, actually cited works; strict recent majority in a frozen 3–5 year window | **Pipeline wins.** `min_unique=36`, `as_of=2026`, `recent_window_years=4` → inclusive 2023–2026 (rationale: spiking-GNN and low-latency conversion literature becomes substantive from 2023; recorded), `require_recent_majority=true`. Separate quantity/recency arithmetic at P12/P14. |
| C7 | §10 forbidden phrasings: no "SOTA", no energy claim, "first conversion framework for graphs", explicit FTBC inheritance | scope must be written as positive evidence boundaries; no defensive disclaimers, no process narration, no rhetorical addresses to venue/reviewer | **Both apply, rewritten form wins.** "We do not claim energy savings" becomes "we report spike counts and SynOps proxies"; "not SOTA" becomes "we establish the first reference baseline in this setting"; FTBC inheritance is a positive attribution in §2. The scientific facts behind the prohibitions remain fully binding (no energy claim without G5, no SOTA claim, no "first spiking GNN", no "better than ICML'25"). |
| C8 | "first conversion-based SNN framework for graphs" as the lead contribution | claim/evidence alignment; no unsupported priority claim; no duplicate or overlapping submission | **Blocked pending author decision.** The same project already holds two complete manuscripts, A (reproduction audit, NeurIPS 2026 E&D, score 9) and B (conversion theory, score 8), both built on the same identity, `β*=θ/(2T)` and membrane readout. See `notes/overlap-risk-AB.md`. Until the author chooses, the guidance's central claim is the **ICML'25 mechanism separation + Theorem G1(d)**, not a priority claim. |
| C9 | §2 "frozen numbers, do not rerun unless a counterexample appears" | P3 baseline-first; P4 every guidance experiment; every reported number traceable to `runs/<id>/` in **this** run; G0 requires Cora/PubMed T=8 reproduction < 0.1 pp | **Pipeline wins.** The task-book numbers are calibration evidence and the G0 reproduction target. Main-table numbers come from this run's `results.csv`. Companion-project results may be reaccepted as immutable external evidence only after data/split/code/config/seed/environment/gate re-check with hashes and commit recorded; they never masquerade as this run's rows. |
| C10 | §7.4 reproduce SpikeNet / SiGNN / SpikingGCN; appendix references "DRSGCN", "SSEL" | claims must be supported by verified artifacts; no invented baselines | G0 verification: **SSEL not found** in arXiv/Web; **DRSGCN not found** (SGNNBench records DRSGNN, AAAI 2024); SpikeNet and SiGNN are dynamic-graph link-prediction methods with a different protocol. The ≥3 direct-training arms are chosen from verifiable SGNNBench implementations, with protocol differences stated explicitly. Unverifiable method names never enter a table. |
| C11 | appendix speed-card: "T=4 generally collapses", "TPP+QCFS on ResNet-34/ImageNet only 37.23", "T=4 basically unusable" | truthfulness is a hard gate; numbers must be verified from the primary source | G0 primary-source check: 37.23 is the **unfavourable** ResNet-34/ImageNet T=4 TPP+QCFS cell; the paper's Figure 1 (VGG-16/ImageNet, ANN 70.00) gives T=4 QCFS 4.67 / permuted 55.54 / **TPP+QCFS 68.39**. The task book's generalisation is therefore not supportable. Recorded in `notes/G0_source_conflicts.md`. The manuscript may only place gaps side by side, never "better than TPP". |
| C12 | TPP neuron "implementation", citing official code if used | every implementation must record source + commit; no unreleased code assumed | TPP-SNN official repository states the full codebase is "coming soon" and exposes only a QCFS core link, with no checkpoints. The TPP neuron is therefore **re-implemented from the paper's equations (8)–(13)**, with the derivation and commit recorded in `notes/`. No claim of using official TPP code. |
| C13 | protocol frozen (Planetoid public split, seeds 0–6, T grid, 2× noise floor); silent on device | P2 probes accelerators; G0 demands < 0.1 pp reproduction | User authorizes GPU "where it works". **Device is a frozen protocol field.** A known numerical hazard from the companion project: switching the same sparse-reduction code to CUDA moved PubMed ANN by +0.69 pp because the early-stopping epoch changed. Therefore the device that reproduces G0 within 0.1 pp is frozen for all paired arms; GPU is used for compute-heavy arms whose numerics are verified identical, and any deviation is logged with its device in `results.csv`. "不行的拉到" = an explicit, recorded CPU fallback, never a silent mixed-device table. |
| C14 | NeurIPS 2026 / ICML 2026 window from the older brief; task book says ICML/NeurIPS | P20 records only current official constraints | G0 verification: NeurIPS 2026 and ICML 2026 windows have closed; **ICML 2027 and NeurIPS 2027 CFPs are not yet published**. Working assumption recorded, not a fact: ICML-style 8-page main text, unlimited references/appendix, double blind, official LaTeX style. `submission-constraints.md` must mark venue/window as **unverified** until a CFP exists. |

## 4. Protected scope and writing modes

- `edit_scope`: full six-section manuscript plus appendix proofs; evidence tables and all numbers are protected.
- `protected_sections`: any sentence carrying a `% run:` comment, every scripted table, all equations of
  Theorem G1 (a)–(d), the FTBC attribution statement, and the §10 legal/illegal phrasing list.
- `protected_artifacts`: `registry/results.csv`, all `runs/<id>/` logs and metrics, `results/*.json`,
  `paper/claims.md`, all skill-generated review reports, `notes/` negative-result records.
- `declaration_mode`: `author-managed` (no author names, affiliations, funding, competing interests,
  code-release route or LLM disclosure inferred).
- `allow_new_experiments`: true, within the method family, tier and the local resource envelope.
- `editing_round_budget`: 3; stop after two rounds without fewer concrete defects. Exhaustion never
  grants acceptance.
- Every in-text number must resolve to a `run_id`; negative results are retained, never deleted.

## 5. Quality requirements carried into every gate

1. Score ≥ 9 from `ccf-paper-reviewer` (`full` mode), with a scorecard, confidence, evidence basis,
   repair conditions and an independent multi-reviewer panel per `ccf-common`.
2. Six numbered main sections; 0 untraced numeric tokens; 0 duplicate references; citation gate PASS
   (≥36 distinct, strict 2023–2026 majority); `grep -rn "TODO("` empty.
3. All tables/figures scripted from `results.csv`; compiled PDF from a clean extraction matches the
   accepted build; `latexmk`/pdflatex with 0 errors and 0 undefined references.
4. `workflow_complete` and `submission_ready` reported separately; the latter stays false while
   author/portal facts are pending. No submission action.
5. Failed gates, negative results and instrumented exceptions are written to `notes/` before any
   downstream stage opens.

## 6. Input manifest (snapshots under run root)

| file | role |
|---|---|
| `contracts/agent_prompt_v2_ICML25.snapshot.md` | scientific content contract (immutable copy of the task book) |
| `contracts/execution-contract-v1.md` | this contract |
| `pipeline-state.json` | guidance-builder 12-stage ledger |
| `f-research-v1-run-20261105-111502-gnn2snn/pipeline-state.json` | f-research-v1 P0–P21 ledger |

Hashes are bound into each ledger at stage acceptance; a mutable ledger is never its own evidence.
