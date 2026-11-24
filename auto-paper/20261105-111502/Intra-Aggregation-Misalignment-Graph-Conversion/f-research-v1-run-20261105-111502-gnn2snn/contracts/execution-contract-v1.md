# execution-contract-v1 — f-research-v1 run-local contract

Version: v1. Established 2026-11-05. Immutable; a change creates v2 and reopens from P0.

This is the **research-stage** contract. The parent guidance-stage contract lives at
`../../contracts/execution-contract-v1.md` plus its `...-addendum-C8.md`; both are binding here and
are copied as snapshots into this run root. On any conflict, the f-research-v1 pipeline wins over
the task book (adjudication C1–C14 in the parent contract).

## Goal and authorization

Produce an evidence-backed English first draft for an independent third paper on graph
ANN→SNN conversion, with a `ccf-paper-reviewer` full-mode calibrated stance **≥ 9**. Authorized:
local Windows Conda (`base` primary, `siigm`/`jiewu-research`/`dyg-cold` fallback,
`spikinggcn36` legacy), WSL2 (`spikg` for third-party code), CUDA where numerically safe, CPU
fallback recorded. Not authorized: remote compute, submission, upload, publication, `git push`,
or any external action.

## Input manifest

| file | role |
|---|---|
| `contracts/guidance.snapshot.md` | authoritative guidance (copy of parent `guidance.md`) |
| `contracts/ccfa-startup-packet/` | startup decision `proceed`, claim-evidence matrix, feasibility contract |
| `contracts/agent_prompt_v2_ICML25.snapshot.md` | scientific content contract (task book) |
| `contracts/execution-contract-v1.md` (parent) + C8 addendum | conflict adjudication, author decisions |

## Binding scientific contract

- Four claims C1–C4 in `ccfa-startup-packet/feasibility-contract.json`. **C3 (bound-derived
  latency allocation) is the designated `expected_strong` capability**; P5 cannot pass without it.
- `planned_claim` is distinct from `observed_finding` until P5A.
- Six numbered main sections exactly: `1 Introduction`, `2 Related Work`, `3 Method`,
  `4 Experiments and Results`, `5 Discussion`, `6 Conclusion`.
- No priority claim reused; A/B are anonymous companions with a division-of-evidence statement.
- No SOTA claim, no energy claim, no "better than ICML'25"; FTBC attribution is explicit.
- Every in-text number carries `% run: <run_id>`; every table is scripted from `results.csv`;
  no hand-typed numbers; unresolved tokens are forbidden before compilation.
- ≥36 distinct verified actually-cited works, strict 2023–2026 majority, duplicate-paper audit.

## Writing controls

- `edit_scope`: full six-section manuscript plus appendix proofs; numbers and evidence tables protected.
- `protected_sections`: every `% run:` sentence, every scripted table, Theorem G1 (a)–(d), the FTBC
  attribution, the companion division-of-evidence paragraph, and the task book §10 phrasing rules.
- `protected_artifacts`: `results/`, `runs/`, `registry/results.csv`, `paper/claims.md`, all
  skill-generated reviews, all `notes/` negative-result records.
- `declaration_mode`: `author-managed`. `allow_new_experiments`: true within the method family,
  tier and local envelope. `editing_round_budget`: 3; stop after two rounds without fewer defects.
- Hash protected originals and compare exact ranges before/after edits.

## Dependency substitutions (recorded, not disguised)

`AutoResearchClaw` Python package is absent on Windows and in the WSL env named
`autoresearchclaw` (verified `find_spec -> None`). Stages 16, 17, 18, 19, 20, 22, 23 run as
**local-executor substitutions** with identical substantive gates and are never reported as ARC
tool calls. `spark-task-delegator` is absent; canonical stages are not parallelized. Available
installed skills are used for their owning responsibilities: `ml-paper-writing`, `paper-refine`,
`paper-polish-workflow`, `humanizer`, `nature-figure`, `nature-citation`, `citation-audit`,
`paper-compile`, `ccf-paper-reviewer`, `ccf-integrity-auditor`.

## Environment ledger

Windows `C:/Users/xhf/miniconda3` env `base`: Python 3.13.13, numpy 2.4.4, scipy 1.18.0,
torch 2.11.0+cu128, torch_geometric 2.8.1, CUDA True (RTX 3060 12 GB, driver 591.74).
WSL2 Ubuntu 22.04 GPU pass-through confirmed; `spikg` = py3.8 + torch 2.1 + dgl 1.1.3.
Device is frozen per paired arm (see `protocols/protocol.md` and parent contract C13).

## Traceability policy

The parent pipeline forbids commits without explicit author instruction, while the experiment
discipline requires every run to be traceable. This run therefore uses **content-addressed
traceability** instead of a git commit: each `runs/<id>/config.yaml` records the sha256 of the
exact code files, the sha256 of every input data file, the external asset commit
`d12511207b1f0f1ee49650ec560de5236942c419` where an asset came from the companion run, the
Conda environment, the device, the seeds and the full command line. A run whose hashes cannot be
recomputed from files inside this run root is void. If the author later authorizes a local git
repository, a commit field is added without invalidating the hash chain.

## Output and readiness

`workflow_complete` and `submission_ready` are reported separately. Seven author/production items
remain pending in `../../contracts/delivery-readiness.json`; `submission_ready` stays false.
Final deliverables: TeX source, compiled PDF, figures, bibliography, `results/`, `runs/`, the
ordered ledger, traceability matrix, figure/table audit, reference-dedup audit, citation audit,
final reviews, and the pending checklist — all under this run root.
