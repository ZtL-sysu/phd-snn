# Research Guidance File

## Title / Topic

- Working title: Ten Mechanisms for Evidence-Backed GNN→SNN Conversion
- Target field: graph representation learning, ANN-to-SNN conversion, neuromorphic graph computing
- Target venue: Q2+ journal / strong specialized venue; this run's requested deliverable is a Chinese Markdown experiment-and-review report, not a submission manuscript
- Technique/method: ten frozen-conversion mechanisms selected by the 2026-11-17 smoke portfolio
- Selected application scenario: local real graph, coordinate, temporal-video and biological-edge assets with frozen ANN/GCN teachers

## Core Idea

Run the ten accepted mechanisms in canonical order, each against simple, matched and strongest feasible baselines: DYN-C01, EQ-C02, PERM-C03, SIGN-C04, LR-C05, EDGE-C06, CERT-C11, POS-C13, DLY-C14, READ-C18. The goal is to determine which mechanisms retain their smoke signal under full local evaluation, which fail, and what claim each result supports.

### Mechanism-Level Rationale

- Domain bottleneck: low-step GNN→SNN conversion loses temporal, geometric, signed, compressed, certified, positional and readout information in different operator locations.
- Why the mechanisms fit: each targets a concrete information/cost loss and has an exact or measurable control.
- Required adaptation: convert frozen graph representations/messages/edges/readouts; do not train a replacement spiking GNN as the proposed method.
- Why this is more than method X on dataset Y: each claim is tied to an operator-level mechanism, matched ablation and explicit falsifier.

## Paper Story

- Central scientific question: which graph-specific conversion mechanisms survive baseline-first full evaluation, and what evidence boundary do they support?
- Intended reader: GNN/SNN conversion and neuromorphic graph researchers deciding which mechanisms merit a standalone paper.
- Domain/theory problem → design requirement → candidate choice: graph information is lost at state, group action, ordering, sign, rank, edge weight, error propagation, positional encoding, delay and output levels → preserve or certify that information → ten bounded mechanisms.
- Expected contribution type: empirical mechanism audit plus resource/correctness trade-offs.
- planned_claim: each module has its own planned claim in the traceability table; no result is assumed.
- observed_finding: pending until P5/P5A.
- Main claim: the final report will state only the subset supported by full evidence, including failures.
- Boundary of the claim: local assets/checkpoints and the exact protocols below; no universal energy or hardware claim.

## Paper Outline

1. Introduction: motivation, conversion losses, portfolio question.
2. Related Work: frozen conversion, direct spiking GNNs, graph/transformer/equivariant prior art.
3. Method: ten operator-level mechanisms and their exact/matched controls.
4. Experiments and Results: sequential full experiment matrix with baselines, seeds, uncertainty and resource accounting.
5. Discussion: supported claims, failure modes, novelty boundaries and next-paper routes.
6. Conclusion: ranked evidence-backed recommendations.

## Experiment Plan

### Datasets and Assets

| Asset | Access/local role | Frozen split/protocol |
|---|---|---|
| DAVIS-2017 motion clips | local 728×8×32×32 clips + labels | deterministic 70/15/15 clip-index split, 5 seeds |
| MaleCNS soma coordinates/types | local 3,982 smoke subset; full typed rows used where available | deterministic stratified 60/20/20, 5 seeds |
| Chameleon/Squirrel/Corа/Citeseer/PubMed/OGBN-Arxiv | local graph loaders and frozen checkpoints | public fixed validation masks; checkpoints seeds 0–2 where available |
| FlyWire `syn_count` | local 385,946 finite edge weights | all finite weights; deterministic hash split for downstream aggregate checks |

### Baselines

- Simple baseline: raw/absolute representation, float32/full output, universal uniform quantization or random projection.
- Matched internal baseline: same data, dimensions, event/storage budget and seeds with the mechanism disabled or shuffled.
- Strongest feasible domain baseline: frozen GCN conversion and graph quantization controls from the local `core.convert`; literature baselines One-Spike/ASGCN/A²Q/AdaQP/SpikeZIP are context or adaptation attempts where code permits.
- Oracle/upper-bound: unquantized float teacher or exact original operator.

### Proposed Method Variants and Required Experiments

| Order | ID | Full experiment matrix | Required ablations/controls | Primary metric | Minimum | Binding expected-strong |
|---:|---|---|---|---|---|---|
| 1 | DYN-C01 | DAVIS 5 seeds; absolute repeated state vs causal residual vs shuffled residual; downstream direction accuracy, reconstruction, nonzero events | future-prefix perturbation; delay-0 residual | accuracy + event fraction | exact prefix; ≥10% event reduction | accuracy within 1 pp of raw and ≥15% event reduction on ≥4/5 seeds |
| 2 | EQ-C02 | typed MaleCNS coordinates; raw vs component-uniform vs radial events; 5 rotations and 5 split seeds | reflection and shuffled direction controls | balanced accuracy + equivariance error | error ≤1e-8 | accuracy within 2 pp raw, beats component-uniform by ≥1 pp, quantization error ≤10% |
| 3 | PERM-C03 | 3 graphs×5 permutations; deterministic scatter vs naive row-order pooling | shuffled permutation and noncommutative reduction counterexample | max permutation error | ≤1e-10 | exact on all cases and naive control fails at least once per graph family |
| 4 | SIGN-C04 | Chameleon/Squirrel/Cora, seeds 0–2; full signed vs abs-only vs positive-only message classifier | sign shuffle and equal-event magnitude control | balanced accuracy + reconstruction | exact signed reconstruction | signed beats both controls by ≥2 pp on both heterophilic datasets in mean |
| 5 | LR-C05 | message matrices on 3 graphs; ranks 8/16/32/64/128; SVD vs random projection | rank-matched random, truncated tail residual | teacher logit MSE + compression | finite | rank128 ≥8× compression and SVD MSE ≥20% lower than random on ≥2/3 graphs |
| 6 | EDGE-C06 | FlyWire weights; uniform/log/quantile alphabets 4/8/16/32/64 bits; downstream weighted aggregation | shuffled weights and float oracle | relative error + aggregate MSE | <50% error | ≥4× bit reduction, error ≤20%, and ≥10% better than uniform at same bits |
| 7 | CERT-C11 | 3 graphs×2 quant levels; proposed affine envelope vs global Frobenius bound | uncovered-error audit and empirical quantile | coverage/tightness | 100% coverage | width/RMS ≤10 and ≥25% tighter than global bound |
| 8 | POS-C13 | Chameleon/Squirrel; 1–3 hops, levels 4/8/16; raw vs uniform vs per-channel quantized hop events | permutation and shuffled-hop controls | downstream balanced accuracy + error | exact permutation | 8-level error ≤5%, accuracy within 2 pp raw, ≥4× storage reduction |
| 9 | DLY-C14 | DAVIS 5 seeds; delay 0/1/2 residual schedules vs absolute | wrong-delay and future-leakage controls | accuracy + prefix error | exact causal | delay1/2 accuracy within 1 pp best and event reduction ≥10% on ≥4/5 seeds |
| 10 | READ-C18 | 6 graphs×3 seeds; full vs top2 vs top1 readout | near-margin bins and class-shuffled pair | preservation, slots, calibration | top2 exact | top2 100% preservation and median slot reduction ≥50%; top1 documents failures |

### Metrics and Statistical Checks

- Accuracy/balanced accuracy, teacher agreement, logit/representation MSE, reconstruction error, equivariance/permutation error, event/slot/bit reduction, runtime and peak memory.
- Five seeds for DAVIS/MaleCNS; graph checkpoint seeds 0–2 where present. Report mean, sample SD and paired bootstrap 95% intervals where applicable.
- No test-set search. Frozen deterministic splits/IDs are saved before model/parameter selection.

### Runtime / Hardware Budget

- Local Conda `dyg-cold`, RTX 3060 12 GiB, 32 GiB RAM; CPU for small graph analysis.
- Maximum 20 minutes and 12 GiB per module; maximum 10 modules × 5 seeds, no remote compute.
- All commands/logs/results under this run root; historical inputs are hash-registered read-only sources.

## Expected Results

- Minimum acceptable result: each module either meets its minimum and yields an interpretable comparison, or fails with complete negative evidence and falsifier status.
- Strong result: the binding expected-strong column above.
- Failure signal: minimum miss, mechanism/control indistinguishability, leakage, nonfinite output, budget exhaustion, or only favorable seeds.
- Strong-result entry gate for final narrative: all required matrices complete; claim wording is narrowed to actual evidence; failed modules remain explicitly reported.

## Figure/Table Decision Rules

- Required first figure type: none mandated because the requested deliverable is Markdown; a compact mechanism map is optional.
- Required experiment tables: one sequential result table and one claim/CCFA score table.
- Evidence that may benefit from visual inspection: accuracy-event Pareto, compression-error curves, certificate coverage/tightness, margin-stratified readout.
- Exclude plots that obscure denominators, mix operation counts with energy, or compare unmatched budgets.

## Traceability Checklist

Every row in “Proposed Method Variants and Required Experiments” is mandatory and maps to `results/<ID>.json`, `protocols/<ID>.md`, and `experiment-traceability.md`. All ten must appear in the final Markdown report with actual values, pass/fail, failure analysis and supported claim scope.

## Citation Scope

- Must-cite: One-Spike SNN, ASGCN, Negative-spike conversion, A²Q, AdaQP, SEENN, SpikeGraphormer, SpikeZIP-TF, ECMT, SGNNBench.
- Search keywords: ANN-to-SNN graph conversion, event graph, equivariant spiking GNN, graph quantization, spiking graph transformer, graph readout compression.
- Target recency: 2022–2026 plus foundational conversion work.
- Known duplicate risk: arXiv/published versions of One-Spike, SpikeGraphormer, ECMT and transformer-conversion papers; verify title/DOI/arXiv before final review.

## Constraints and Preferences

- Final deliverable: one Chinese Markdown file describing all ten stories, actual experiment results and independent CCFA scoring.
- Preserve negative/null results; no fabricated gains, energy claims or silent reruns.
- No commit/push/submission. Use project Conda Python only.
- Local artifact policy: every new process/deliverable file under `f-research-v1-run-20261117-220203-ten-idea-full/`.
- Writing language: Chinese summary with English identifiers/numbers.
