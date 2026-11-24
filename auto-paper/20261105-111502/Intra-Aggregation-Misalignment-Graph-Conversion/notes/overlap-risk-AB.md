# Outstanding author decision — relation to companion Papers A and B

**Status: BLOCKING for CCFA-startup / C8. No inference made, no priority claim written.**

The public-literature novelty check (G0) passed: no published work duplicates a graph ANN→SNN
conversion with an exact error identity. But the same workspace already contains two **complete,
unpublished** manuscripts from the same project, both built on the same machine and the same
theoretical assets. This is not a public-literature duplication; it is a **same-group overlap /
salami-slicing risk**, which a CCF-A reviewer and an overlap declaration will treat as a scientific
and ethical question. It must be settled by the author before the Core Idea of `guidance.md` is fixed.

## What already exists

Run root: `auto-paper/20261028-171500/Spiking-GNN-Conversion/f-research-v1-run-20261028-174053-gnn-snn-conv/`
(git `d125112`, 2026-11-05). Deliverables and skill-generated scores:

| paper | title | target | score | pages |
|---|---|---|---|---|
| A | *What Reproduces in Spiking Graph Neural Networks? An Audit of Every Method That Publishes Code* | NeurIPS 2026 E&D | **9** (8 on a main track) | 9 |
| B | *When Does Graph-to-Spiking Conversion Work? Spectral Gain, Activation Mass, and an Order-Invariant Readout* | CCF-A main track (unconfirmed) | **8** | 22 |

B already owns, with 7-seed evidence and 19 scripted tables:
the exact per-layer identity `B̂_l − B_l = (1−α)Â(E_{l−1}M_l)` (residual ~2e-6), the parameter-free
bias `β*=θ/(2T)`, the order-invariant membrane readout (0.000 pp spread vs 1.6 pp for count
decoding), the L=2 closed form (0.08 pp mean discrepancy over 105 cells), the depth amplification
law `G^0.95` at r=0.990, a width law, a four-arm Pareto (2–23× fewer SOPs at matched accuracy),
a threshold law verified over 7 seeds × 4 graphs (WP15), and explicit negative results
(prediction failure, ensemble failure, adaptive-threshold failure, L=3 closed-form failure).
A owns the seven-cell reproduction grid and the Split I / Split II finding.

## Overlap matrix against the new task book

| task-book element | already in A/B? | genuine increment available |
|---|---|---|
| "first conversion framework for graphs" + exact identity | **Yes, B's headline** | none — cannot be reused as a new first |
| `β*=θ/(2T)`, membrane decoding, latency theorem | **Yes, B** | none |
| Table 1 with T grid {2,4,8,16,32}, 8 method rows | partial (B has 19 tables, different row set) | the TPP-transplant row and the 3 aggregation hosts are new |
| S1-a inter-layer permutation probe (ICML'25 Fig.1 replication on graphs) | **No** (B tested order-invariance of its own decoder, not whether cross-layer shuffling *helps*) | **yes** — the decisive mechanism-separation experiment |
| S1-b intra-aggregation phase randomisation | **No** as a controlled 2×2 | **yes** |
| S1-c TPP transplant + 2×2 four-way control | frozen numbers exist in the task book §2, but not an independent controlled arm in B | **yes** |
| Theorem G1 (a)–(d), especially (d) with `ρ_n` and an L-layer closed form / `T_L` | **No** — B has an empirical `G^0.95` law and a recursion, not a `ρ_n`-weighted L-layer bound with a bias term | **yes, and it is the strongest new theory** |
| Three aggregation hosts H1/H2/H3 as a plug-in narrative | H1/H2 numbers exist; H3 unrun; not framed as plug-in | **yes, cheap** |
| ≥3 direct-training reproductions + Pareto | B has a four-arm Pareto of **its own** arms; A has three **audited** third-party pipelines | **partly** — codebase-level anchors can be cited as companions |

## Score arithmetic inherited from the previous terminal review

B's `ccf-paper-reviewer` full review (`ccfa-skill-review-B-wp15-final.md`) is explicit:
WP15 raised Quality 4→5 and Evidence 4→5 but **Significance stayed 4 and the score stayed 8**,
because the new result *verified a configuration the paper already used* rather than adding a
capability. Its named +1 route, M-B1, is *"an identity-derived method that achieves something
previously unavailable — e.g. a per-layer latency allocation from G that reaches a target accuracy
with provably fewer steps, validated on held-out graphs."*

Therefore: re-running the task book as written (mechanism separation + a theorem + more tables) is
likely to land at **8 again**. To reach the user's binding target of **≥ 9**, the new manuscript
needs a positive, usable capability. The task book's own Theorem G1(d) requirement — an L-layer
closed form and the explicit `T_L` dependence — is exactly the raw material for M-B1. This is a
design recommendation, recorded here for the author's decision, not a silent scope change.

## Three options for the author

| option | positioning | effect on claims | main risk |
|---|---|---|---|
| **1. Independent third paper with an explicit division of evidence (recommended)** | new paper centred on the ICML'25 contrast: S1 three probes, TPP four-way control, Theorem G1(d), and a G1(d)-derived per-layer latency allocation validated on held-out graphs; A and B cited as anonymous companions | no "first" claim; contribution = *mechanism separation + a bound that changes what a practitioner can compute*; each paper's main claim independent of the others | three same-topic manuscripts from one group → reviewers may still suspect slicing; the division-of-evidence statement must be airtight |
| **2. New paper replaces B** | B archived; the new manuscript becomes the conversion mainline, inheriting the "first conversion framework" claim and its evidence | simplest novelty story; can reuse B's numbers as reaccepted immutable evidence after full re-verification (hashes, commits, G0 reproduction) | loses an existing completed 8-score deliverable; the "first" claim still needs a genuine new capability to reach 9 |
| **3. Merge A + B + task book into one flagship** | one paper with audit anchor + theory + ICML'25 contrast | strongest single evidence package | far beyond 8 pages; three contribution centres dilute the argument; highest rewrite cost |

## Recommended default if the author does not choose

Option 1, with the G1(d)-derived latency allocation as the binding `expected_strong` capability.
The guidance would then declare: *the companion audit and companion conversion analysis are cited
as anonymous prior work; this paper's claims do not depend on their results; its own contribution is
the mechanism separation and a bound-derived deployment rule.* No "first" claim, no assumption that
A or B is published, and no overlapping submission is asserted.

**This file is a note, not a decision. CCFA-startup remains `running` until the author answers.**
