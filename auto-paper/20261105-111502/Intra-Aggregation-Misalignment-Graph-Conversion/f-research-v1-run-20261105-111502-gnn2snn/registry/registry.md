# Pre-registration registry

Rule: hypothesis, expected values and failure criterion are written **before** the experiment.
Results, including failures, are back-filled afterwards. Nothing here is a reported finding yet.

| id | linked claim | hypothesis | expected values (pre-registered) | failure criterion | result | status |
|---|---|---|---|---|---|---|
| R0 | G0 foundation | the copied core kernel in this Conda environment reproduces the frozen task-book numbers on CPU | Cora ANN 0.8060 / T=8 0.8026; PubMed ANN 0.7757 / T=8 0.7740; both within 0.10 pp | any |d| > 0.10 pp | **PASS**: Cora ANN 0.8060 (Δ +0.000 pp), T8 0.8026 (Δ −0.003 pp); PubMed ANN 0.7757 (Δ +0.001 pp), T8 0.7740 (Δ +0.000 pp). 14 rows in `results.csv`, `results/wp0_repro.json` | **closed (passed)** |
| R1 | C1 mechanism separation | cross-layer permutation is near-neutral on graphs while intra-aggregation phase randomisation is harmful; TPP transplant trails IF+`β*` | branch A or B; TPP ≥1.5 pp behind at T=4 on ≥2/3 graphs; 2×2 directions differ by >0.8 pp | branch C or D, or a seed-level reversal | pending | registered |
| R2 | C2 `ρ_n` bound | the L-layer bound holds with zero violations at L≤4 and a conservatism between 3× and 8× | residual ≤1e-5; zero violations; mean conservatism 3–8× | any unattributed violation or conservatism >20× | pending | registered |
| R3 | **C3 `T*` capability (binding)** | the inverted bound predicts each model's minimum T before a sweep, and a per-layer allocation reaches ε=1.5 pp with fewer steps on unseen graphs | ≥3/3 held-out graphs hit within one T-grid step; ≥25% timestep saving; matched-budget uniform control fails on ≥2/3 graphs | any held-out gap >2.3 pp at predicted T*, hit rate <2/3, savings <0%, or shuffled-`ρ_n` control matching | pending | registered |
| R4 | C4 Pareto and hosts | conversion is never dominated at T≤4 and plugs into three aggregation hosts | ≥3 reproduced direct-training arms; zero dominated cells; H1–H3 differ <1 pp at T=8 | a dominating direct-training point or <2 reproducible arms | pending | registered |

## Frozen before any held-out measurement (R3)

- `epsilon = 1.5 pp` (gap to source ANN).
- T grid `{2, 4, 8, 16, 32}`; seeds 0–6; noise floor 0.4 pp; 2× rule = 0.8 pp.
- Fitted graphs: Cora, CiteSeer, PubMed. Held-out graphs: ogbn-arxiv, chameleon.
  Squirrel is a stress cell excluded from all claims if its runtime budget is exceeded.
- Fitting constants are frozen and committed here before the first held-out run; no held-out
  result may re-fit them.
- Controls: uniform-T matched total budget, shuffled-`ρ_n`, full grid-search oracle, L=3 schedule.

## Back-fill log

- 2026-11-05 — all five registrations written. No experiment had been executed at this point.
