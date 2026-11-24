# Claim–evidence matrix

Every claim below has one row and one artefact. A claim with no artefact is not a claim; an
artefact that supports no claim is deleted before submission.

| id | claim (as it will appear) | evidence artefact | success check | paper location | must appear |
|---|---|---|---|---|---|
| C1 | The conversion error satisfies `B̂_l − B_l = (1−α)Â(E_{l−1}M_l)` exactly, for any depth | `experiments/core.py:check_identity`, per-layer residual printed in `results/wp3_depth.json` | max abs residual ≤ 1e−5 at L∈{2,3,4} | §3.3 | yes |
| C2 | Fidelity is predictable out of sample from `(G, H, Δ, T)` | `experiments/wp7_predict.py` → `results/wp7_predict.json` (LOCO + LODO) | MAE ≤ 1.0 pp and required-T exact on ≥70 % of held-out cells | §4.4, Tab. 12 | yes |
| C3 | Depth is not survivable, and `G` predicts by how much | `results/wp3_depth.json` | amplification exponent in [0.5,1.5], r ≥ 0.9 | §4.7, Tab. 9 | yes |
| C4 | The membrane decoder is exactly order-invariant; the count decoder is not | `results/wp6a_misalignment.json` | membrane spread ≤ 0.1 pp over 4 perturbations, count spread > 0.3 pp | §4.8, Tab. 10 | yes |
| C5 | Under one protocol, conversion is not dominated at T ≤ 4 by three published formulations | `results/wp2_pareto.json` | no external arm has both higher accuracy and lower SOPs at T ≤ 4 | §4.2, Fig. 6, Tab. 12 | yes |
| C6 | Width, not depth, is the usable capacity lever (`‖E_1‖ ∝ √H`) | `results/wp3_depth.json:_P2` | `‖E_1‖/√H` varies < 10 % over H∈{16…128} | §4.9, Tab. 11 | yes |
| C7 | Sparsification buys SOPs, not spikes, at a measured exchange rate | `results/wp4_sparsity.json` | SOPs fall ≈ the pruned fraction; accuracy cost stated per graph | §4.6 | yes |
| A1 | The closed-form bias beats a grid search | `results/beta_star_s7.json` | wins ≥ 7 of 9 cells | §4.5, Tab. 3 | yes |
| A2 | The margin-recovery theorem is sound and conservative | `results/theory_s7.json`, `results/theory_tightness.json` | 0 counterexamples; tightness ratio reported | §4.10, Tab. 7 | yes |
| A3 | Two phenomena, not one: our error ≠ ICML'25 cross-layer shuffle | Tab. 10 + the 2×2 | as C4 | §2, §4.8 | yes |
| N1 | Conversion has no energy advantage at matched accuracy | `results/wp2_pareto.json` (spike column) | spikes higher than the trained arm at matched accuracy | §4.5 | yes |
| N2 | Depth cannot be rescued by reparametrisation | `results/wp3_depth.json` (gauge row) + `experiments/theory-depth.md` | gauge-normalised conversion accuracy collapses; ANN unchanged | §4.7 | yes |

## Unsupported-if-missing

If C2 fails, the paper loses its title claim and reverts to a descriptive account of one conversion
method with three measured laws. If C5 fails (conversion is dominated at T ≤ 4 by some external arm),
the low-latency positioning is withdrawn and the paper becomes a diagnostic framework only — still
publishable, not at the target tier.

## Deliberately absent claims

- No "we are the first to convert GNNs" — only "no published *analysis*".
- No state-of-the-art accuracy claim; the strongest external architecture already beats us on two
  graphs in our own measurements, and that row is reported.
- No energy saving; only an exchange rate.
- No depth support; the opposite.
