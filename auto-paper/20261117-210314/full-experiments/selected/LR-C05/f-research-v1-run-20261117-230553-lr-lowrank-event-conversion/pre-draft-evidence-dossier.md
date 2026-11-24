# Pre-draft evidence dossier

## Question

Can operator-aligned low-rank residual events reduce graph-message transport while preserving frozen GNN→SNN conversion better than equal-budget strong controls?

## Verified findings

- At rank128 and 1% sensitivity-scored residual events, message-error reductions over the strongest residual control are 19.29% Cora, 30.60% Chameleon and 25.91% Squirrel; dimension compression is 7.32×/8.99×/11.64×.
- T=2 teacher-agreement gains over the strongest equal-storage control are +1.33 pp (95% bootstrap [0.80, 2.00]), +3.70 pp [1.92, 5.76], and +3.37 pp [−1.98, 6.97].
- T=4 gains are +0.73 pp [0.40, 1.40], +7.54 pp [5.35, 9.19], and +6.95 pp [5.89, 7.69].
- Runtime p95 is 1.113× SVD-only and peak CUDA allocation is 8.125 MB; a small tail exceeds 1.2×.

## Boundaries

Local node-classification graphs, frozen two-layer GCN teachers, CPU-compatible graph aggregation and explicit bit/event accounting. No hardware energy or broad architecture claim.
