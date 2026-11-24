# P4 — required experiment completion

| guidance requirement | artifact | cells | status |
|---|---|---|---|
| G0 reproduction | `results/wp0_repro.json` | 14 rows | done |
| S1 2x2 probe | `results/s1_probe.json` probe_2x2 | 36 | done |
| S1 faithful L=3 inter-layer replay | `results/s1_probe.json` l3_interlayer | 9 | done |
| S1 four-way neuron control | `results/s1_probe.json` four_way | 48 | done |
| Table 1 method x T grid | `results/table1.json` method_grid | 120 | done |
| Three plug-in hosts | `results/table1.json` hosts | 45 | done |
| C3 T-grid curves (6 graphs x 7 seeds x 5 T) | `results/c3_allocation.json` curves | 42 | done |
| Bound-derived fit (fitted graphs only) | `results/c3_fit.json` | 21 pairs | done |
| Held-out evaluation | `results/c3_allocation.json` heldout | 3 | done |
| Negative controls | `notes/`, Appendix D | see ledger | retained |

`infeasible-with-evidence` rows: 1.
Their partial rows are retained and no claim depends on them. Device repair for the largest
held-out graph is recorded in `contracts/pre-registration-c3.md` v4 with a one-seed CPU/CUDA
identity check in `runs/device_check.log`.

**Gate verdict: PASS** for execution completeness. Scientific acceptance is decided at P5.
