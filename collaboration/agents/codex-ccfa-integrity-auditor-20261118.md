# codex-ccfa-integrity-auditor-20261118

## Scope

Independent `ccf-integrity-auditor` `full` audit of the frozen LR-C05 manuscript `auto-paper/20261117-210314/full-experiments/selected/LR-C05/f-research-v1-run-20261118-004321-lr-logit-fidelity-v3/writing/p8/paper-data-figures.md`.

## Evidence Checked

- `writing/p9-evidence-digest.json`
- `results/confirmation-summary.json`
- `results/confirmation-test-v2.json`
- `inputs/v2-summary.json`
- `inputs/v2-timing.json`
- `figures/source-data/*.csv`
- `figure-table-insertion-audit.md`
- figure captions/contracts/manifests and `writing/verified-reference-context-p7.md`

## Findings

- Headline test reductions, task-loss bounds, hidden-MSE sensitivity, budget-grid range, runtime range, and memory value are numerically supported.
- F8 A2Q/One-Spike reduction values match `figures/source-data/figure2-main-logit-mse.csv`, but the evidence digest points to `results/confirmation-test-v2.json`, which does not reproduce those aggregate percentages.
- Figure 1 exists and is visually coherent, but its recorded deterministic self-draw fallback conflicts with the mandatory direct-GPT Figure 1 P8 gate.
- Citation keys are draft placeholders only; no bibliography is present. `dcgs`, `one-spike`, and preprint-style entries need P12 metadata resolution.

## Deliverable

`ccfa-full-integrity-audit.md` in the LR-C05 run root. The manuscript was not edited and no literature search or evidence invention was performed.
