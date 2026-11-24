---
contract_status: EXPERIMENT_STAGE_CONTRACT
round: 001
primary_idea: C1
generated_at: 2026-11-07T15:38:39+08:00
builder: f-guidance-builder-v1 (CCFA-startup -> G0...G8 -> validation -> handoff)
consumer: f-research-v1 (P0...P21)
remote_execution: OPTED_IN by user (novix exp-4090)
---

# Guidance — Does Membrane State Transfer to Real Optical Flow?

## Title / Topic

Working title: *Does Membrane State Transfer? A Connectome-Constrained Spiking GNN on Real Optical Flow*.
Field: neuromorphic / bio-inspired computer vision, graph neural networks, connectome-constrained models.
Target venue: CVPR 2027 main conference; submission 2026-11-16 AOE is an external hard date (recorded as risk).
Round-001 primary idea C1, selected by independent `ccf-idea-reviewer standard` ranking (Overall 6.1, GO as a relative
advancement recommendation, zero hard fatal gates hit). Scores are used for ranking only; no hard threshold is applied.

## Core Idea

Base model `eudald-seeslab/train-your-fly`: fixed FlyWire v783 whole-brain graph, measured ommatidium
(Voronoi) sampling, three stateless message-passing steps `x <- tanh(A x)`, Kenyon linear readout.
Local measurement (`mining/results/round7.json`): on a SYNTHETIC moving-dot direction task,
`stateless = A = 0 = 0.458`, `LIF + homeostasis = 0.740`, delta **+0.2817**, 95% CI [0.2033, 0.3617],
frame-stacked ceiling 0.988, five seeds. Flash detection delta -0.0167 (CI crosses zero).
Eight rounds found degree-preserving nulls never lose to the real wiring, so no topology-advantage claim is allowed.
The open question is whether that gain is an artifact of regular synthetic motion or transfers to real optical flow.
The experiment changes the **evidence domain**, not the mechanism, which makes attribution clean: the same
graph, eye frontend, dynamics and readout are run on SYNTHETIC and REAL sequences under one protocol,
and the domain gap itself is the measured quantity.

## Paper Story

Bottleneck: connectome-constrained visual GNNs with spiking state have only been validated on synthetic
dot stimuli; a reviewer can reasonably ask whether the reported gain is a property of regular synthetic motion.
Prior work (arXiv:2604.04033, arXiv:2610.10023, arXiv:2609.01330, Lappalainen et al. Nature 2024) does not
answer transferability to real optical flow. New insight: a same-protocol synthetic-versus-real comparison
turns a single-dataset gain into a **transferability verdict** that is valuable to the vision community
whether positive or negative. If the gain survives, it supports membrane-state dynamics as a real
temporal-integration mechanism; if it vanishes, it bounds the claim to synthetic regular motion and
prevents a misleading generalization. Evidence to convince: five seeds, bootstrap CI, BH correction,
ceiling checks, stateless / A=0 / degree-preserving-null controls, and a one-factor mechanism ablation,
with all raw logs and the exact script retained.

## Paper Outline

1. Introduction: temporal labels are invisible to stateless connectome GNNs; the transferability gap for spiking membrane state on real optical flow.
2. Related Work: connectome-constrained vision, spiking graph networks, null-model and negative-result methodology, temporal vision benchmarks.
3. Method: fixed graph and real eye frontend; stateless baseline; LIF membrane state with homeostasis; real-flow-to-ommatidium sampling and label derivation protocol; the one-factor mechanism ablation.
4. Experiments and Results: data and ceiling checks, same-protocol synthetic-versus-real comparison, five-seed main table, mechanism decomposition, null-model and A=0 controls, robustness and efficiency diagnostics.
5. Discussion: what transfer or non-transfer implies, the null-model boundary (no topology advantage), scale-stability constraints, limits of the eye frontend on real footage, honest venue-level scope.
6. Conclusion: the transferability verdict and the open questions it settles or raises.

## Experiment Plan

| Item | Specification |
|---|---|
| Dataset | REAL FlyWire v783 edges, annotations and eye positions from Zenodo `10.5281/zenodo.21549559` (CC BY 4.0); REAL optical flow from DAVIS-2017 trainval-480p (official direct link, 832,766,765 bytes, HTTP 200/206, ZIP magic `PK` verified 2026-11-07) and optionally MPI-Sintel complete (5,627,783,629 bytes, HTTP 206, ZIP magic verified); SYNTHETIC moving-dot sequences from the local `light_smoke.py` generator. |
| Direct access URL | `https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip` and `http://files.is.tue.mpg.de/sintel/MPI-Sintel-complete.zip`; Zenodo record files for the connectome tables. All three were probed with HTTP HEAD and a 16-byte Range request in this session. |
| Baselines | stateless three-step tanh propagation, A=0 (no propagation), frame-stacked pixel/optical-flow ridge ceiling, degree-preserving rewiring null, sign-shuffled E/I control, and the SYNTHETIC domain under the identical protocol. |
| Proposed method variants | LIF with fan-in homeostasis, LIF plus combined mechanisms (adaptive threshold, refractory, real E/I signs), and one-factor removal ablations for each added mechanism. |
| Primary metric | Held-out classification accuracy on the temporal direction / speed-change label; headline is `delta = LIF - stateless` within each domain and the domain gap of that delta. |
| Secondary metrics | 95% bootstrap confidence intervals (2000 resamples), BH-FDR q values, spike rate, readout feature std, ceiling accuracy, peak GPU memory, wall time, and per-seed variance. |
| Failure signal | Real-domain ceiling below 0.70 (label or derivation broken), delta at or below zero with CI lower bound at or below zero, NaN, missing raw script, or fewer than five valid seeds. Any of these returns to task design before P2. |
| Statistical checks | Five fixed seeds, preregistered direction, bootstrap 95% CI, BH correction at q=0.05, two-seed apparent effects are not findings, tolerance never larger than the effect size, conclusions re-checked against raw numbers. |
| Runtime / Hardware Budget | Remote novix `exp-4090` (RTX 4090 46,068 MiB, CUDA 13.0, torch 2.11.0+cu130, measured on task 17682) for the P4 batch; local RTX 3060 12 GB / conda `dyg-cold` for verification, figures, writing and compilation. Estimates in `feasibility-contract.json` are planning figures only and are NEVER passed as a task timeout. |
| Stopping criteria | Ceiling below 0.70, NaN, unavailable main condition, or absent script and result.json; no tuning to significance, failed runs retained as evidence. |
| Reproducibility | `experiment.py`, `result.json`, config, seeds, command history, dependency list, raw logs and `git`-free artifact copies pulled into the run root. |

Every row of the traceability checklist below must be `done` with evidence before P5. The full P4 batch
includes all datasets, baselines, variants, ablations, metrics, statistical checks, robustness and
efficiency measurements under `f-research-v1` P4, not a lightweight smoke test.

## Expected Results

These are **preregistered, falsifiable transfer predictions calibrated on the local synthetic measurement
(+0.2817, CI [0.2033, 0.3617]), NOT observed results on real optical flow**. No real-domain number exists yet.

- `minimum`: real-domain `delta(LIF - stateless) >= +0.15` with 95% bootstrap CI lower bound > 0.
- `expected_strong`: real-domain `delta >= +0.25` with CI lower bound > 0, AND a decisive transferability
  verdict (survives or vanishes) backed by the same-protocol synthetic-versus-real comparison, AND at least
  one one-factor ablation identifying which mechanism carries the gain.
- `failure`: real-domain ceiling < 0.70, `delta <= 0`, CI lower bound <= 0, NaN, or missing raw evidence.
- Honesty constraint: `degree_null - LIF` is reported as measured regardless of sign. If the null is again
  higher, the claim is phrased as a gain from spiking-state dynamics, not from connectome-specific wiring.
- Article acceptance is separate from experiment acceptance: the finished manuscript must obtain
  `ccf-paper-reviewer full` `**Overall:** X >= 8.0` at P9 and complete P21 before it is recorded as qualified.
  Below 8.0 the correction loop continues (current plan repair, then backup ideas, then fresh ideation).

## Traceability Checklist

| Guidance requirement | Required artifact | Minimum success check | Strong success check | Must appear in paper? |
|---|---|---|---|---|
| Real-data ceiling and label derivation | `evidence/real_ceiling.json` | ceiling >= 0.70 with derivation script | ceiling >= 0.85 and split protocol inspectable | Yes |
| Same-protocol synthetic and real comparison | `evidence/main_table.csv` | five seeds in both domains | delta >= +0.25 with CI lower bound > 0 | Yes |
| One-factor mechanism ablation | `evidence/ablation.json` | each added mechanism removed once | carrier mechanism identified with CI lower bound > 0 | Yes |
| Degree-preserving null control | `evidence/null.json` | measured delta reported with sign | real wiring beats null only if CI lower bound > 0 | Yes |
| A=0 and stateless controls | `evidence/main_table.csv` | both recorded, no NaN | reproduced across all five seeds | Yes |
| Spike rate and feature std | `evidence/diagnostics.json` | non-empty per condition | variance change explained by the mechanism | Optional |
| Reproducibility metadata | `evidence/run_manifest.json` | task id, seeds, config, script present | pulled script re-runnable locally | No, audit artifact |

## Citation Scope

Keywords: Drosophila connectome, FlyWire / MaleCNS, connectome-constrained GNN, spiking neural network,
LIF membrane state, temporal vision, optical flow, DAVIS-2017 / MPI-Sintel, null models, negative results.
Must-cite clusters: arXiv:2604.04033 (topology null models), arXiv:2610.10023 (structure alone),
arXiv:2609.01330 (connectome plus spiking orientation maps), Lappalainen et al. Nature 2024
doi:10.1038/s41586-024-07939-3 (flyvis), Dorkenwald et al. Nature 2024 doi:10.1038/s41586-024-07558-y,
Schlegel et al. Nature 2024 doi:10.1038/s41586-024-07686-5, DAVIS-2017 and MPI-Sintel dataset papers,
and SNN efficiency / null-model methodology. Binding f-series rule: at least 36 distinct verified relevant
cited works with a strict majority in a frozen 3-5 year window; duplicate DOI / arXiv id / normalized title /
preprint-versus-published versions must be audited in `reference-dedup-audit.md`. Currently 21 first-hand
entries are verified in `fly-connectome-cvpr2027/literature/closest-work.md`; the remainder is a P12 gate,
explicitly pending and not assumed satisfied. One NeuroGraphBench DOI was NOT FOUND in an earlier round
and must not be cited until verified.

## Figure and Table Plan

Select visuals only after evidence stabilises; no fixed count and no per-subsection quota. Candidates include
(a) the same-protocol synthetic-versus-real framework schematic, (b) the five-seed main table with 95% CI,
(c) a one-factor mechanism decomposition table, (d) a domain-gap plot of `delta` with CI,
(e) a spike-rate versus feature-std diagnostic, (f) the null-model comparison. Each must answer a
scientific question and be cited near its first discussion. Figure 1 is the overall framework figure and
shows only verified components; data figures follow `nature-figure` conventions.

## Constraints and Preferences

English manuscript, Chinese for internal logs and user discussion. Artifact boundary: everything
(protocols, pulled results, TeX, PDF, audits, manifest) stays under this guidance directory; the
`f-research-v1` P0 run root lives inside it. No submission, OpenReview registration, commit/push or
publishing. No credentials in guidance, logs or manuscript. No workflow, tool or pipeline names in the
manuscript body. Six fixed top-level sections. Negative and null results are preserved and reported.
`workflow_complete` and `submission_ready` are reported separately; the latter stays false in this project.
