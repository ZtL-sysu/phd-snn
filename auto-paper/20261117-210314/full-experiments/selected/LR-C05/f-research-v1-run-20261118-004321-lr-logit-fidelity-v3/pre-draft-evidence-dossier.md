# Pre-draft evidence dossier

## Main finding

On the reported official test split, output-Jacobian-selected sparse residual coefficients at rank128 and a 2% residual budget reduced the ratio of three-seed mean split-specific logit MSE by 26.23%, 33.99% and 25.83% relative to the strongest evaluated matched-budget control. All compared rank128/2% methods used identical total padded serialized bits within each dataset. The maximum three-seed-mean degradation across T2/T4 accuracy and teacher agreement was 1.86 pp; the largest seed-level degradation was 2.85 pp. Across nine dataset-seed pairs, paired p95 runtime ratios versus SVD-only ranged from 1.020× to 1.124×, with peak allocation 218.23 MB.

## Evidence boundary

The focal setting and logit-fidelity reframing were fixed after validation exposure and before the test run. The subsequent test run is held-out confirmation, not a preregistered or independent replication. Three local static graphs and three frozen two-layer GCN checkpoints bound the evidence. Sparse residual coefficients are not temporal SNN events. No energy or broad architecture claim.
