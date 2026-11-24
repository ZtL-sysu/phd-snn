# Claim ledger

Three columns as required by the task book: assertion, evidence `run_id`, strength
(`strong` = direct controlled measurement; `medium` = supported with a stated boundary;
`conditional` = holds only under a named condition). Every `run_id` resolves to a row in
`registry/results.csv` and to a `runs/<id>/` evidence bundle or a `results/*.json` file.
This ledger is filled with the run identifiers that produced the manuscript's macros; no number
is typed into the manuscript by hand.

| # | assertion | evidence run_id | strength |
|---|---|---|---|
| 1 | The environment reproduces the frozen Cora/PubMed $T{=}8$ references within 0.1 pp | `wp0-repro-*` (14 rows), `results/wp0_repro.json` | strong |
| 2 | $\hat{B}_l-B_l=\Ahat(\Emat_{l-1}M_l)$ is an exact identity with numerical residual $\le 10^{-5}$ | `runs/wp0-repro-*/metrics.json`, Appendix A proof, `results/s1_probe.json` four-way cells | strong |
| 3 | The membrane readout is exactly invariant to upstream spike-time permutation | `S1-cora-ours_probe-T*-s*` with `probe=inter`, `results/s1_probe.json` 2x2 block | strong |
| 4 | Cross-layer permutation and intra-aggregation phase perturbation are different mechanisms with different signs | `S1-*-ours_probe-T*` (`probe=inter/intra/inter+intra`) and `results/s1_probe.json` L3 block | strong |
| 5 | The two-phase TPP transplant trails the closed-form correction at $T{=}4$ | `S1-*-tpp_faithful_b0-T4-s*`, `S1-*-if_b1-T4-s*`, `results/s1_probe.json` four-way block | strong |
| 6 | $\betastar=\theta/(2T)$ is orthogonal to the neuron model (TPP + $\betastar$ $\ge$ TPP) | `S1-*-tpp_faithful_b1-T*-s*` | medium |
| 7 | Theorem G1(d): $\rhon$-weighted $L$-layer bound with a mandatory bias term | Appendix A proof, `results/c3_allocation.json` curves, `contracts/pre-registration-c3.md` | strong (proof), medium (empirical conservatism) |
| 8 | $\Tstar$ predicted from trained weights reaches the target on held-out graphs with fewer timesteps than a uniform budget | `S5-*-ours_Tgrid-T*-s*`, `results/c3_fit.json`, `results/c3_allocation.json` | conditional on the pre-registered pass condition; see verdict |
| 9 | Conversion is never dominated at $T\le4$ by arms measured under the identical protocol | `S3-*-*-T{2,4}-s*`, `results/table1.json`, `figures/fig_pareto.pdf` | medium (external published rows are labelled context only) |
| 10 | The correction plugs into three aggregation hosts with $<1$ pp spread at $T{=}8$ | `S3-*-{H1_mean,H2_sum,H3_sym}-T8-s*`, `results/table1.json` hosts block | strong |
| 11 | No energy claim: spike counts and SynOps are proxies | `registry/results.csv` `sop_est`/`spikes_per_node` columns in every row | strong (scope boundary) |
| 12 | FTBC attribution and anonymous companion division of evidence | `\cite{ftbc2024}`, `\cite{companion}`, `\cite{companionb}`, Related Work | strong (citation-level) |
| 13 | Negative results: spectral-norm constraint, adaptive threshold, $L{=}3$ closed-form failure, multi-view averaging | `results/s1_probe.json`, Appendix D, `notes/` | medium (reported with mechanisms) |

## Prohibited assertions (checked at P17)

No "SOTA", no "first graph spiking network", no "first conversion framework" (belongs to the
anonymous companion), no "better than ICML'25", no measured-energy claim, no cross-protocol
ranking of published numbers. Any sentence that would violate these is listed in
`contracts/execution-contract-v1.md` §"protected scope".
