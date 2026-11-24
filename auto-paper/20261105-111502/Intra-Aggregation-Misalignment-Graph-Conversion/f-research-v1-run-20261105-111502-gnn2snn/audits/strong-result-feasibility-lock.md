# P1A — strong-result feasibility lock

Executed **before any environment setup or proposed-method training**. Source:
`contracts/ccfa-startup-packet/claim-evidence-matrix.md`,
`.../strong-result-feasibility-contract.md`, `.../feasibility-contract.json` (4 claims, 7
hash-bound artifacts). `feasibility-contract.json` was validated by
`validate_guidance.py --strict --packet` (exit 0).

| requirement | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| mechanism stated | pass | pass | pass | pass |
| falsifying ablation | 2×2 + four-way control | L≤4 counterexample grid | shuffled-`ρ_n` + matched uniform-T + oracle | bias removal, decoder swap, 512-wide row |
| prerequisite assumptions | pass | pass | pass | pass |
| simple baseline | IF no-bias | naive `‖W‖∞·θ/T` | uniform-T max | IF no-bias |
| strongest feasible domain baseline | re-implemented TPP | companion `G^0.95` law (external calibration) | full T-grid oracle | ≥3 SGNNBench arms |
| matched internal control | IF+`β*` vs TPP+`β*` | same net without `β*` | same-budget uniform-T | same-width direct training |
| metric + direction | accuracy, higher | violations, lower | timesteps, lower | accuracy/cost pair, higher/lower |
| `minimum` | branch A/B, ≥1.5 pp TPP gap | zero L≤3 violations | ≥2/3 held-out reach ε | ≥2 arms, no dominated cell |
| `expected_strong` | branch B on 3/3, orthogonality | zero L≤4, 3×–8× conservatism | ≥3/3 within one step, ≥25% saving | ≥3 arms, never dominated |
| `failure` | branch C/D, reversal | unattributed violation, >20× | gap >2.3 pp, <2/3 hit, <0% saving | dominated point, <2 arms |
| code / adaptation route | `probes.py`, `tpp_neuron.py` from eq. (8)–(13) | `bound.py` + appendix proof | `latency_alloc.py`, one ANN per (graph,seed) | `hosts.py`, `pareto.py`, `tables.py` |
| prototype / sanity milestone | T=8 Cora TPP 0.7756 ±0.5 pp | identity residual ≤1e-5 on 30 cells | ≥6/9 fitted cells within one T step | H3 runs end-to-end on Cora |
| compute / memory / runtime | 24 h / 8 GB | 18 h / 8 GB | 30 h / 10 GB | 36 h / 12 GB |
| seeds / search trials | 7 / 120 | 7 / 60 | 7 / 90 | 7 / 200 |
| reproducibility artifacts | `runs/<id>/`, `results.csv`, hashes, device | same | frozen constants before held-out | same |
| stop-and-return condition | stop on branch C/D, report GP | return to theory design | return to C2, correction loop | 5-day stop-loss, versioned narrowing |
| reviewer question per experiment | yes | yes | yes | yes |
| reviewer question per ablation | yes | yes | yes | yes |
| reviewer question per robustness/efficiency | yes | yes | yes | yes |

**Calibration check (no arbitrary headline gain).** C3's ≥25% saving is one step of a five-value T
grid on average; the frozen task-book numbers show graph-dependent minimum T at T=4 (1.17 / 0.18 /
1.02 pp), so a uniform budget is measurably wasteful before any new experiment. C2's 3×–8×
conservatism is bracketed by the companion's measured 3.2–6.7× latency-bound looseness. C1's
1.5 pp TPP margin is bracketed by the frozen 2.65 / 4.23 / 2.57 pp T=8 margins. None of these
targets was chosen for presentation value.

**Compute-bounded:** total ≈108 h wall clock, ≤12 GB VRAM, 470 search trials, 7 seeds, no remote
compute. The C3 design removes the companion's earlier 49-training-per-dataset overrun by training
one ANN per (graph, seed).

**No-fabrication check:** `observed_finding` is unresolved; no numeric result exists in this run
at P1A; all feasibility numbers are budgets, not outcomes.

**Gate verdict: all four claims PASS.** No `block`. P2 may open. P1A does **not** relax P5:
the approved `expected_strong` must still be met with real logged evidence before writing.
