# Pre-draft evidence dossier

## Problem and novelty delta

Finite-precision messages in frozen GNN-to-SNN conversion need a certificate that follows the actual graph operators and output weights. The supported contribution is a deterministic final-logit interval envelope for the exact chain `M=XW0 → Q_rowwise(M) → A·relu(·+b0) → A·H·W1`, evaluated against a matched global-radius ablation. It is not broad SNN superiority, a state-of-the-art compression baseline, or a robustness theorem.

## Main claims

1. `B_abs=|A||A|Delta|W1|` contains every measured final-logit absolute error in 36/36 graph/seed/level/quantizer cells.
2. `B_abs` is no looser than the valid Minkowski upper comparator in all cells.
3. Global-uniform quantization is an equality control: 18/18 cells match `B_global_col`.
4. Rowwise uniform radii tighten the global-radius outputwise comparator by 74.26%–82.12%, median 79.65%, in all 18 rowwise cells.
5. Absolute width/RMS is descriptive only: standard median 30.68, maximum 36.91 for rowwise; no absolute-width or statistical-coverage claim.

## Evidence and baseline table

| Evidence set | Matrix | Result |
|---|---|---|
| Baseline seed-0 | 3 graphs × 2 levels × 2 quantizers | 12/12 containment; rowwise tightening 78.38–81.36% |
| Corrected full matrix | 3 graphs × 3 seeds × 2 levels × 2 quantizers | 36/36 containment; 36/36 Minkowski valid |
| Global control | 18 cells | 18/18 equality within tolerance |
| Rowwise method | 18 cells | minimum tightening 74.26%; median 79.65%; maximum 82.12% |
| Failure diagnostics | all rows | zero clipping, zero non-finite rows, zero omissions |

## Mechanism and falsification

For `E=M-Q(M)`, componentwise ReLU non-expansiveness gives `|H-H_hat|<=|A||E|`, and the second aggregation gives `|Z-Z_hat|<=|A||A|Delta|W1|`. The claim is falsified by any uncovered error, invalid Minkowski ordering, failed global equality control, or rowwise tightening below 25%.

## Scope and limitations

- Frozen two-layer GCN snapshots on Cora, Chameleon and Squirrel; three seeds; 4/8 levels.
- Global/rowwise uniform rounding only; no learned quantizer, temporal spike, energy, hardware or multilayer claim.
- Containment is deterministic theorem/implementation validation. The RMS denominator is descriptive and can be small, so absolute width/RMS is not a quality claim.
- The global comparator is a matched radius-granularity ablation, not a broad state-of-the-art baseline.

## Planned figures and tables

- Figure 1: exact quantization and operator chain.
- Figure 2: rowwise versus global width/RMS and tightening.
- Figure 3: global-uniform equality control and traceable rowwise tightening/width distribution from `figures/source-data/figure3-rowwise-tightening.csv`.
- Table 1: formulas and numerical policy.
- Table 2: complete 36-cell summary and worst cases.
