# Frozen experiment protocol (v1, 2026-11-05)

**This file is frozen at P2. Any change requires a versioned correction with a reopened stage and
its whole downstream suffix.** It is the single source for every number in `registry/results.csv`.

## 1. Data and splits

Planetoid public splits only: Cora 140/500/1000, CiteSeer 120/500/1000,
PubMed 60/500/1000. No random splits in the main tables. Held-out graphs for claim C3:
ogbn-arxiv (official temporal split) and chameleon (declared Geom-GCN version with duplicate-node
treatment); squirrel is a stress cell. Heterophily versions must be named in every row.

Raw files live in `results/.data/`, copied from the companion run and hash-bound in
`audits/reaccepted-assets.md`. Any new download must be hashed into `config.yaml` before use.

## 2. Seeds and statistics

Seeds exactly 0–6 (7 seeds), never extended. Report mean and standard deviation, paired bootstrap
95% intervals, and the gap to the source ANN in percentage points. Measured noise floor:
**0.4 pp at T≥8** (to be re-measured here as a device-swap check). Any "improvement" must exceed
**2 × noise floor = 0.8 pp**; otherwise it is reported as a tie. No seed selection, no deletion of
negative results.

## 3. Hyperparameter budget parity

Conversion and direct-training arms use the same `lr × hidden × dropout` grid, the same early
stopping rule (validation only, patience as implemented in `core.train_ann`), and the same maximum
epochs. The full trial ledger is recorded. A test set is never used for selection.

## 4. Timestep grid

`T ∈ {2, 4, 8, 16, 32}` for every method. T=2 is an exploratory cell: bad values are reported,
never deleted. Conversion uses one ANN training for the whole grid; direct training retrains per T.

## 5. Device rule (contract C13)

The device is a **frozen field** per paired arm. `core.train_ann(..., device="cpu")` is the G0
reference because the companion measured a +0.69 pp PubMed ANN shift on CUDA (sparse-reduction
order changes the early-stopping epoch). GPU is used for compute-heavy arms only after a
verified-identical number check on a shared cell; any deviation is logged in the `device` column
and in `config.yaml`. Mixed-device rows are never silently pooled.

## 6. Metrics recorded for every run

`accuracy`, `ann_ref`, `gap_pp`, `spikes_per_node`, `sop_est = T × E × hidden`,
`train_seconds`, `retrain_count` (direct = |T|, conversion = 1), `std` over seeds, plus
`probe`, `host`, `method_family`, `is_transplant`, `neuron`, `bias_correction`, `perm_seed`,
`device`, `git_commit` (content-addressed trace id) and `notes`.

Spike counts and SynOps are **proxies**. No measured neuromorphic energy claim is permitted.

## 7. Traceability

Every run writes `runs/<run_id>/{config.yaml,log.txt,metrics.json}`. `config.yaml` contains the
full command line, all hyperparameters, seed, device, Conda env, library versions, the sha256 of
every code file and input data file, and the external asset commit where applicable. A run whose
hashes cannot be recomputed from files inside this run root is void. See
`audits/traceability-policy.md`.

`registry/results.csv` is the **only** source for tables and figures. Every in-text number in the
manuscript carries `% run: <run_id>` immediately after it. Unresolved tokens are forbidden before
compilation.

## 8. Pre-registration

`registry/registry.md` holds each claim's hypothesis, expected values and failure criterion,
written and frozen **before** the corresponding experiment. Results, including failures, are
back-filled after the run. Pre-registration constants for C3 (ε = 1.5 pp, held-out graph list,
T grid, fitting constants) are frozen before any held-out measurement and may not be re-fitted.

## 9. Stop rules

- G0: Cora and PubMed T=8 reproduced within 0.1 pp, else no downstream experiment.
- S1/GP: the S1 probe branch decides the paper's direction; branch C or D stops the campaign.
- A direct-training arm that cannot run within 5 working days uses the task book's labelled
  stop-loss with SGNNBench public numbers.
- Any Gate failure enters the f-research-v1 autonomous correction loop; the target is never
  silently lowered and a material scope change is reported to the author.

## 10. Hard prohibitions

No hand-typed table numbers, no cherry-picked seeds, no deleted negative results, no silent
claim rewording, no "SOTA", no energy claim, no "better than ICML'25", no invented author or
venue facts, no submission action.
