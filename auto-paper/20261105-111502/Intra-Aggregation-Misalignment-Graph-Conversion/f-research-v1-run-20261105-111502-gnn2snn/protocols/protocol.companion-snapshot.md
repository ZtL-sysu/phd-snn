# Frozen experimental protocol (WP0)

Status: **FROZEN at git `5c1f394`**. Every experiment in this project cites this file.
Changing anything below is a protocol change and must be recorded in §7 with a date and a reason.
Rows written before a change keep the protocol version they were run under (`protocol_ver` column
is not in the CSV, so the change log in §7 is the record).

---

## 1. Data and splits

| dataset | loader | split | notes |
|---|---|---|---|
| Cora | `graph_data.load_planetoid_sparse` | Planetoid public: 140 / 500 / 1000 | BoW features, L1 row-normalised |
| CiteSeer | same | Planetoid public: 120 / 500 / 1000 | BoW features, L1 row-normalised |
| PubMed | same | Planetoid public: 60 / 500 / 1000 | TF-IDF, L1 row-normalised |
| ogbn-arxiv | `graph_data.load_ogbn_arxiv` | OGB official time split 90941 / 29799 / 48603 | features already normalised |
| chameleon | `graph_data.load_wikipedia` | Geom-GCN split 0 (48/32/20) | heterophilic |
| squirrel | same | Geom-GCN split 0 | heterophilic |

**Random splits are forbidden as a main-table protocol.** If a random split is ever run it goes in the
appendix and is labelled as such. Reason: every competing number in the literature we compare against
is on the public split, and re-splitting makes the comparison uninterpretable.

Node features are L1-row-normalised only where the BoW recipe says so (`graph_data.ROW_NORMALIZE`).
Row-normalising an already-normalised matrix changes the graph's effective feature scale and moves
accuracy by whole points, so this is a protocol decision, not an implementation detail.

## 2. Seeds and statistics

- 7 seeds, indices 0–6. Report mean over seeds; std is over seeds.
- Paired comparisons use the **same seed** for both arms (same init, same dropout stream where the
  arm allows it). Differences are per-seed paired differences.
- Intervals: percentile bootstrap over the 7 paired differences, 10,000 draws, 95 %.
- Wilcoxon signed-rank is **not** used as a headline statistic: with n=7 the smallest attainable
  two-sided p is 2/2⁷ = 0.0156, i.e. the test floors out exactly where we would want to report.

## 3. Hyper-parameter budget parity

Both the conversion arm and every directly-trained arm use the same budget: one configuration, chosen
by validation accuracy, drawn from the same grid

```
lr        ∈ {0.01}          hidden ∈ {16, 32, 64, 128}
dropout   ∈ {0.5}           weight_decay = 5e-4
epochs    = 400             early stopping: patience 30 on validation accuracy
θ         = 1.0             (conversion only; swept separately as a sensitivity, never as a tuning knob)
```

No arm gets a larger search than another. If an arm is later given a wider search, all arms get it.

**Validation, never test.** Early stopping and any bias calibration use `train_mask` / `val_mask`.
`val_mask` is disjoint from `train_mask` and `test_mask` by construction in `graph_data._masks_from_idx`.

## 4. Noise floor and the 2× rule

`noise_floor` is measured, not assumed: the **same code, same protocol, different device** (CPU vs
CUDA), 7 seeds. Per-cell displacement ranges 0–17 pp, so a per-cell floor would let one chaotic cell
poison every comparison. The floor is therefore the **median within a latency class**:

| class | T | noise_floor |
|---|---|---|
| low | T ≤ 2 | 0.36 pp — **not adjudicated at all**, two of five cells change qualitatively |
| mid | T = 4 | 3.40 pp |
| high | T ≥ 8 | 0.40 pp |

A difference counts only if `|Δ| > 2 × noise_floor` **and** the 95 % bootstrap interval excludes 0.
Everything else is written as a **tie**, in the table and in the prose. Re-measured by
`protocols/stats_ci.py`; the numbers above are its output, not a guess.

The T=4 floor is large because 400 epochs with patience 30 is close to the point where a run either
converges or does not; that instability is a property of the baseline, and hiding it by quoting
T=8 only would be dishonest.

## 5. Latency grid

Primary grid `T ∈ {2, 4, 6, 8, 16, 32}`. Every method runs the whole grid. Entries in the paper
that use the older `{1,2,4,8,16}` grid are labelled `legacy grid` wherever they appear.

`T = 1` is reported separately and **never used for a superiority claim**: at T=1 both trained
baselines collapse to a single-class predictor on Cora (measured: 1 distinct predicted class,
modal share 1.000), so a "win" there compares two failures.

## 6. Metrics that must be recorded for every run

`accuracy, gap_pp (vs that dataset's ANN reference), spikes_per_node, sop_est, train_seconds,
retrain_count`

- `sop_est = T × edges × hidden` — a **proxy**, never called energy. Reported as "synaptic
  operations per inference".
- `spikes_per_node` is the measured total spike count divided by N, from the same spike train that
  produced the accuracy (not a model of it).
- `retrain_count` = number of training runs needed to cover the whole T grid. Conversion = 1;
  every directly-trained arm = one per T. This is the honest cost axis and it is not a proxy.

## 7. Change log

| date | change | reason |
|---|---|---|
| 2026-11-03 | protocol created and frozen | WP0 |

## 8. What counts as a claim

Only statements that are (a) produced by a script in `protocols/`, (b) present in
`registry/results.csv`, and (c) traceable to a `runs/<run_id>/` directory may appear in the paper.
A number that exists only in a `.tex` file is a bug.
