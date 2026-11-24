# P1 — guidance validation report

Guidance: `contracts/guidance.snapshot.md` (copy of the parent `guidance.md`).
Validator: `f-guidance-builder-v1/scripts/validate_guidance.py --strict --packet <packet>`.
Result: **`Guidance structure is valid.`** (exit 0).

| required element | present | evidence in guidance |
|---|---|---|
| Title / Topic, target field, tier, venues | yes | working title, CCF-A main track, ICML 2027 assumption recorded as unverified |
| Core Idea with mechanism-level rationale | yes | `Â` and `ρ_n` inside the identity; bound inversion into `T*` |
| Paper Story with central question, planned claim, boundary | yes | explicit separation of `planned_claim` from `observed_finding` |
| Paper Outline, exactly six canonical numbered sections | yes | `1 Introduction` … `6 Conclusion`, no prohibited top-level sections |
| Experiment Plan: datasets, direct URLs, baselines, variants, metrics, ablations | yes | six direct-public datasets, four baseline classes, seven ablations |
| Expected Results: minimum / strong / failure signal | yes | C3 is the binding `expected_strong` |
| Figure/Table Decision Rules | yes | framework figure first, evidence-driven, no quota |
| Traceability Checklist with `Must appear in paper?` | yes | 8 rows |
| Citation Scope with must-cite and recency | yes | ≥36 distinct, strict 2023–2026 majority, duplicate risks listed |
| Constraints and Preferences | yes | English, ICML-style, protected scope, prohibitions |
| Runtime / Hardware Budget | yes | RTX 3060 12 GB, ~108 h, 470 trials, scale repair |

## Startup packet loaded

`contracts/ccfa-startup-packet/` contains all seven artifacts plus `feasibility-contract.json`
with four claims (C1–C4) and hash bindings to all seven artifacts.
`startup-decision.md` = **`proceed`**, which is the only value that permits P1A.

## Contract extraction (saved for P6/P17 audits)

| field | value |
|---|---|
| `topic` | intra-aggregation deterministic misalignment in graph ANN→SNN conversion |
| `target_venue` | CCF-A main ML track; ICML 2027 working target (CFP unpublished) |
| `main_claim` | mechanism separation + `ρ_n`-weighted L-layer bound + bound-derived `T*` capability |
| `method` | exact identity, closed-form bias, membrane decoder, G1(d), latency allocation |
| `datasets` | Cora, CiteSeer, PubMed (fitted); ogbn-arxiv, chameleon (held-out); squirrel (stress) |
| `baselines` | IF no-bias, TPP transplant, ≥3 SGNNBench direct-training arms, uniform-T, grid oracle |
| `primary_metric` | node-classification accuracy and ANN gap in pp |
| `secondary_metrics` | bootstrap CI, bound violations, conservatism, `T*` hit rate, spikes/SynOps/retrain count |
| `expected_minimum` | branch A/B, ≥2/3 held-out graphs reach ε, ≥2 direct-training arms, no dominated T≤4 cell |
| `expected_strong` | ≥3/3 held-out graphs, ≥25% timestep saving, zero L≤4 counterexamples, ≥3 direct arms |
| `strong_result_entry_gate` | P5 cannot pass without C3 |
| `must_run_experiments` | G0 repro, S1 2×2 + four-way control, Table 1, three hosts, G1(d), C3, Pareto |
| `must_have_ablations` | bias removal, decoder swap, shuffled-`ρ_n`, matched uniform-T, L=3 schedule, adaptive threshold |
| `figure_table_decision_rules` | framework figure first; data plots and Tables 1–3 chosen after evidence stabilizes |
| `experiment_traceability` | `runs/<id>/{config.yaml,log.txt,metrics.json}`, content-addressed hashes, `% run:` comments |
| `citation_requirements` | `min_unique=36`, `as_of=2026`, `window=2023..2026`, strict majority |
| `citation_dedup_requirements` | DOI / arXiv id / normalized title / preprint-vs-published scan at P12 and P14 |
| `local_artifact_policy` | everything under this run root, inside the guidance directory |
| `page_length_policy` | 8-page main text, ICML-2026-derived working assumption, re-verify at P16/P20 |
| `single_final_pdf_template_policy` | one final PDF; official double-blind style when the venue is confirmed |
| `central_question` | what generates graph conversion error, and can a bound predict T before a sweep |
| `intended_reader` | low-latency event-driven graph-model practitioners |
| `domain_design_bridge` | aggregation scrambles neighbour phases → error identity must contain `Â` → invertible bound |
| `planned_claim` | C3 held-out `T*` capability |
| `observed_finding` | **unresolved until P5A** |
| `writing_preferences_and_source` | English, formal register, f-research-v1 scientific-writing-contract |
| `protected_scope_and_source` | parent execution contract v1 + C8 addendum |
| `venue_length_requirements_and_source` | ICML 2026 CFP (8 pages); 2027 rules unverified |
| `open_assumptions` | S1 branch, L=4 bound validity, `T*` transfer, baseline reproducibility, 2027 CFP |

**P1 gate verdict: PASS.** Story, outline, expected results, datasets, baselines, metrics,
experiment schedule and the startup decision are explicit; no blocking gap remains.
