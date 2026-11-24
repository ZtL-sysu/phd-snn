# CCFA startup — coordination report (`ccf-pipeline-orchestrator`)

Mode: standard planning. Date: 2026-11-05.

**Project goal:** produce a new, independent third manuscript on graph ANN→SNN conversion, aligned
against ICML'25 (TPP), whose calibrated `ccf-paper-reviewer` full-mode stance is **≥ 9**. The paper
separates intra-aggregation deterministic misalignment from ICML'25's cross-layer stochastic
misalignment, proves a `ρ_n`-weighted L-layer error bound (Theorem G1(d)), and turns that bound into
a **per-layer latency allocation** capability validated on held-out graphs.

**Current stage:** `CCFA-startup` (running). Author decisions are resolved in
`contracts/execution-contract-v1-addendum-C8.md`: independent third paper; A/B are anonymous
companions; the "first conversion framework" priority claim is not reused; the G1(d)-derived
latency allocation is authorized and binding.

**Known artifacts:** task-book snapshot, execution contract v1 + C8 addendum, hardware profile,
G0 literature map, G0 source-conflict ledger, overlap-risk note, two initialized JSON ledgers
(guidance 12 stages, research P0–P21), and the G0 search material.

**Missing artifacts:** the seven startup-packet files, `feasibility-contract.json`, and then the
guidance-side audits and `guidance.md`. `ccfa.yaml` is absent; project-state tracking is unavailable
and is not inferred — this report and `guidance-pipeline-state.md` carry the state instead.

**Gate decision:** `CCFA-startup` passes only when all seven packet artifacts exist, the red-team
review finds no unaddressed fatal risk, the strong-result contract has a mechanism-supported and
compute-bounded path for every binding claim, and `startup-decision.md` is `proceed`. Only then may
G0 be recorded passed. G0 material already collected is re-verified against this packet, not
grandfathered.

**Next owner skill:** `ccf-idea-optimizer` → `ccf-literature-searcher` → `ccf-idea-reviewer` →
`ccf-experiment-designer` (canonical order, no reordering). After the packet, `f-research-v1`
takes over at P0.

**Handoff packet:**
| item | path |
|---|---|
| task book (immutable) | `contracts/agent_prompt_v2_ICML25.snapshot.md` |
| execution contract | `contracts/execution-contract-v1.md` + `...-addendum-C8.md` |
| verified literature | `notes/G0_literature_map.md` |
| source conflicts | `notes/G0_source_conflicts.md` |
| overlap decision | `notes/overlap-risk-AB.md` |
| hardware | `hardware-profile.md` |

**Stage gates and artifact owners:**
| stage | owner | gate | artifact |
|---|---|---|---|
| CCFA-startup | orchestrator + 4 CCFA skills | 7 artifacts + `proceed` | this packet |
| G0 | literature-searcher | current baselines + code/checkpoint status verified | `notes/G0_literature_map.md`, `literature-baseline-matrix.md` |
| G1 | literature-searcher | ≥1 directly public dataset, no approval flow | `dataset-access-log.md` |
| G2 | experiment-designer | task, labels, split, metric, protocol | `claim-evidence-matrix.md` |
| G3 | idea-optimizer | mechanism-level fit + falsifier | `theoretical-feasibility-audit.md` |
| G4 | literature-searcher + idea-reviewer | no duplicate public work; companion overlap declared | `novelty-feasibility-report.md`, `notes/overlap-risk-AB.md` |
| G5 | orchestrator | local envelope holds | `hardware-profile.md` |
| G6 | experiment-designer | simple / strong / matched baselines + ≥2 ablations | `literature-baseline-matrix.md` |
| G7 | experiment-designer | calibrated `expected_strong`, prototype, budget, stop-return | `strong-result-feasibility-contract.md`, `feasibility-contract.json` |
| G8 | idea-reviewer | skeptical-reviewer story | `story-strength-audit.md` |
| validation | guidance-builder | `validate_guidance.py --strict --packet` clean | validator stdout |
| handoff | guidance-builder | index row appended | `auto-paper/generated-research-directions.md` |

**ccfa.yaml update:** not applicable (file absent). Do not fabricate one.

**Risks / blockers:**
1. **R1 (score risk, highest).** Companion B scored 8 because it verified an existing setting rather
   than adding a capability. Mitigation: the latency-allocation capability is a binding
   `expected_strong` target with a pre-registered failure condition, not an optional add-on.
2. **R2 (overlap risk).** Same-group three-paper slicing. Mitigation: anonymous companion citation,
   explicit division-of-evidence statement, and no reused priority claim.
3. **R3 (baseline risk).** TPP official code is unreleased; SpikeNet/SiGNN use dynamic link
   prediction rather than Planetoid node classification. Mitigation: re-implement TPP from
   equations (8)–(13) with a recorded unit test; select ≥3 direct-training arms from verified
   SGNNBench implementations and label protocol differences; apply the task book's 5-day stop-loss.
4. **R4 (venue risk).** ICML/NeurIPS 2027 CFPs unpublished. Mitigation: 8-page main text recorded
   as an ICML-2026-derived working assumption; `submission_ready` stays false.
5. **R5 (numeric risk).** CUDA changes sparse-reduction order and early stopping (observed +0.69 pp
   in the companion project). Mitigation: device is a frozen protocol field; G0 reproduction
   < 0.1 pp decides it; GPU used only where verified identical.
6. **R6 (dependency risk).** AutoResearchClaw package absent. Mitigation: local-executor
   substitutions with identical substantive gates, recorded as substitutions, never as ARC calls.
