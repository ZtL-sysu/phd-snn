# Manuscript evidence packet

## Accepted claim

Message-aware calibration substantially closes the low-step conversion gap for a dynamic Grapher at equal event count.

## Accepted numbers

- Teacher mean accuracy: 83.60% (seed SD 0.49 pp).
- v1 structure/scale calibration mean accuracy: 50.23% (SD 4.32 pp).
- v2 message-aware calibration mean accuracy: 78.83% (SD 0.79 pp).
- Teacher gap: 33.37 pp (v1) to 4.77 pp (v2); 85.35% mean closure; per-seed 86.12%, 80.62%, 89.32%.
- Message MSE: 0.007922 (v1) to 0.001411 (v2); 82.19% reduction.
- Events: 6,272,000 in every evaluated method/ablation.
- Ablation means: scale-only 50.23%, offset-only 38.85%, message-full 78.83%.
- Prior v1 oracle: teacher-feature restoration with converted discrete decisions reaches 83.42%; teacher features plus restored neighbor/winner indices exactly match teacher accuracy. This motivates the v2 message-fidelity claim.

## Scope conditions

- Small patch-grid dynamic Grapher on Fashion-MNIST.
- Three teacher seeds and 2,000 frozen test examples per seed.
- No hardware-energy measurement; cost is event count and wall-clock only.
- No universal claim across all ViG architectures.

## Required six sections

1 Introduction, 2 Related Work, 3 Method, 4 Experiments and Results, 5 Discussion, 6 Conclusion.

## Evidence sources

- `v2-message-calibration-results.json`
- `v2-ablation-results.json`
- `p4-method-oracle-results.json`
- `frozen-test-results.json`
- `baseline-structure-results.json`
- `teacher-training-results.json`

## Writing exclusions

No pipeline states, correction chronology, dataset-download mechanics, JSON/CSV-to-figure workflow, reviewer dialogue, or submission-admin text in the manuscript.
