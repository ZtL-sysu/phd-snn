# G6 — Baseline and ablation feasibility

## Comparison classes

| Role | Method | Implementation path | Feasibility |
|---|---|---|---|
| Simple baseline | Unsigned rate coding of ReLU-like activations / unsigned uniform quantization | Implement in the new clean prototype | Local, low cost |
| Strong conversion baseline | Signed multi-threshold differential coding from the published DCGS algorithm | Independent reimplementation from primary-paper algorithm; do not copy unlicensed repository | Local, moderate cost |
| Domain baseline | Locally reproduced small ViG-style dynamic-kNN/max Grapher on Fashion-MNIST or MNIST patches | Implement from ViG paper-level operator description; public MIT-licensed data route | Local, moderate cost |
| Matched internal baseline | Signed uniform quantization at the same nominal levels/event budget | Same teacher and calibration subset | Local, low cost |
| Structure ablation | Activation-MSE calibration without topology/winner terms | Same parameter count and search budget | Local, low cost |
| Causal ablation | Teacher-neighbor-only, teacher-winner-only, both-oracle, random-neighbor control | Diagnostic-only Grapher variants | Local, low cost |
| Prior-art adaptation | Rate/signed conversion applied to a fixed-graph GatedGCN using local MIT-sourced superpixel data and exposed teacher metadata | Reuse existing local resources; results labeled historically exposed | Local, diagnostic only |

## Fairness controls

- Same teacher weights, split identities, calibration subset, T values, nominal coding levels, and event-count accounting.
- Hyperparameters selected on train/validation only; historical exposed test sets cannot select methods.
- All seeds and failed runs retained.
- Strong recent conversion is represented by an independently reimplemented DCGS-family baseline, not by a literature number alone.
- Domain-specific structure is represented by the dynamic-kNN/max teacher, not by the existing fixed-graph GatedGCN checkpoints.

## Gate verdict

`pass`. Simple, strong, domain, matched, and causal-ablation paths are all locally implementable. The GatedGCN checkpoints are useful diagnostics but cannot carry the binding main claim because their test sets are historically exposed and their graph is fixed.
