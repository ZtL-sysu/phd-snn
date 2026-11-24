# Figure captions

## Figure 1. Exact-cost output-Jacobian residual transport for frozen GNN-to-SNN conversion

The frozen graph message is transported through a rank-128 SVD basis. A squared output-Jacobian score selects sparse exact residual coefficients, and the basis and residual records are serialized under a matched total padded serialized-bit budget before rate-coded conversion at T=2 and T=4. The diagram distinguishes exact residual coefficients from temporal SNN events and reserves diagnostics for validation-grid sensitivity and held-out confirmation after validation exposure.

## Figure 2. Matched-budget logit fidelity on three static graphs

Three-seed mean split-specific logit MSE for the output-Jacobian selector and matched-budget controls at rank 128 and a 2% residual budget on the reported test split. Error bars show sample SD across checkpoint seeds (n=3); no formal confidence interval is claimed. Lower is better. All compared residual methods use identical total padded serialized bits within each dataset.

## Figure 3. Logit-fidelity sensitivity across residual budgets

Relative logit-MSE reduction versus the strongest corresponding matched-budget control for the evaluated 0.5%, 1%, and 2% residual budgets. All nine dataset-budget cells favor the output-Jacobian selector. These are validation-grid sensitivity results; the focal 2% setting subsequently received held-out confirmation after validation exposure.

## Figure 4. Bounded task trade-off and warmed runtime overhead

(a) Official-test logit-MSE reduction versus the maximum three-seed-mean task degradation for each graph. The dashed line marks the prerevised 3 percentage-point task-loss bound; the observed maxima are descriptive and do not establish task equivalence. (b) Paired p95 full-pipeline runtime ratios of the proposed method to SVD-only for nine dataset-seed pairs at rank128/1%, with three warmups and seven measured repeats. The measurement is wall-clock pipeline cost and excludes hardware energy.
