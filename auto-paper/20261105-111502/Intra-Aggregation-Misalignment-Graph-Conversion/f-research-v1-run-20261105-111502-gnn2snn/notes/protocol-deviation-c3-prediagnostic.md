# Recorded protocol deviation — C3 pre-flight diagnostic

Date: 2026-11-05, before `run_campaign.py --stage c3` executed.

## What happened

`experiments/diagnose_c3.py` was written to check whether the pre-registered predictor form
$T\sim c\kappa$ is identifiable **before** spending the full C3 budget. Its graph list was
`["cora", "citeseer", "pubmed", "chameleon"]`. **chameleon is a held-out graph**, so the diagnostic
printed its per-seed gap curves and $T_{\min}$ values to `runs/c3_prediagnostic.log`. Its own
docstring claimed it "never touches held-out results"; that claim was wrong for this one graph.

This is recorded as a deviation, not hidden and not repaired by relabelling the graph.

## What was and was not affected

- `c` in `stage_c3` is fitted with `median(T_min/kappa)` over **FITTED = cora, citeseer, pubmed
  only**. The diagnostic did not change that list, the fit rule, $\epsilon$, the T grid, the seeds,
  the held-out graph list, or any pass/fail condition.
- The diagnostic output was **not** used to choose or tune a predictor. The pre-registered form
  $T^\star = \min\{T\in\text{grid}: T\ge\lceil c\kappa\rceil\}$ remains in force for the first C3
  execution.
- The frozen scalar written to `results/c3_fit.json` comes solely from the fitted graphs.
- The diagnostic therefore cannot change the held-out verdict, but it **does** mean the author
  (and the agent) have seen chameleon's gap distribution before the formal held-out evaluation.
  A reviewer reading the reproducibility record is entitled to know this.

## Honest consequence

The first C3 run is **not** a clean blinded held-out evaluation for chameleon. Two mitigations are
applied and reported:

1. The chameleon cells are still evaluated against the frozen `c` and the frozen pass conditions;
   the deviation is disclosed here and in `notes/S5_c3.md`.
2. If a correction loop later repairs the predictor, the repaired form must be justified from
   **fitted-graph evidence and theory only**, and the whole held-out set (including two graphs
   never shown to the diagnostic, squirrel and ogbn-arxiv) is re-evaluated in one pass. Any
   improvement is reported together with this disclosure.

No number from the diagnostic is used as a result in the manuscript. The diagnostic itself is
retained at `results/c3_prediagnostic.json` and `runs/c3_prediagnostic.log`.

## Lesson recorded

Pre-flight scripts must take their graph list from the same frozen `FITTED` constant as the main
campaign, with an assertion that excluded held-out names are never loaded. This is now a standing
rule for every later experiment repair in this run.
