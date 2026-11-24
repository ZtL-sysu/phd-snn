---
contract_status: PROVISIONAL_EXPERIMENT_CONTRACT
generated_at: 2026-11-07T14:10:18+08:00
builder: f-guidance-builder-v1 (CCFA-startup → G0–G8, honest gate ledger)
consumer: f-research-v1 (P0–P21; P6+ only after the acceptance verdict below passes)
remote_execution: OPTED_IN by user 2026-11-07 (novix exp-4090)
---

# Guidance — Spiking-State Mechanisms for Temporal Vision in a Fly-Connectome GNN

## 0. Contract status and authority

This is an **experiment-stage contract**, not a finished-paper contract. It is authoritative
for what to run, what counts as an acceptable result, and what happens next. The G8 story gate
and the P12 citation gate remain **pending** until remote evidence and the reference audit are
complete; they are recorded as pending, never as passed (see `guidance-pipeline-state.md`).
No experiment result, score, citation count, or review verdict is fabricated in this file.

**Scope correction (user, 2026-11-07 14:10):** the base skeleton stays, but mechanism changes
are **no longer limited to a single substitution**. Multiple simultaneous substitutions, added
mechanisms, new readout layers, new task families, and changed training are all allowed.
The one hard rule is **attributability**: every changed/added mechanism needs its own ablation
and a parameter-matched control; the main claim must decompose to specific mechanisms.

## Title / Topic

- Working title: *Spiking-State Mechanisms for Temporal Vision in a Connectome-Constrained Fly-Brain GNN*
- Field: neuromorphic / bio-inspired computer vision, graph neural networks, connectome-constrained models.
- Target venue: **CVPR 2027 main conference** (submission 2026-11-16 AOE is an external hard date;
  the user has waived internal deadlines but the external date is recorded as a risk).
  Rescue venue family: NeurIPS Datasets & Benchmarks / reproducibility-oriented venues.

## Core Idea

Base model = `eudald-seeslab/train-your-fly`: a **fixed FlyWire v783 whole-brain graph**,
photoreceptor (Voronoi) sampling of the image, **3 stateless message-passing steps**
`x ← tanh(A x)` (the README states "Neurons keep no state between steps"), a Kenyon-cell
linear readout, and only scalar synaptic gains learned.

**Claim under test:** on a task whose label exists only *across time* (motion direction),
stateless message passing cannot integrate frames, whereas membrane-state dynamics can.
The gain is a property of **spiking state × temporal integration**, not of the biological
wiring being specially advantageous. Multiple mechanisms may be combined, but each must be
ablated separately so the gain can be attributed.

Existing local evidence (real, `fly-connectome-cvpr2027/mining/results/round7.json`) is as follows.
stateless = A=0 = **0.458**, LIF+homeostasis = **0.740**, delta **+0.2817**,
95% CI **[0.2033, 0.3617]**, frame-stacked pixel ceiling **0.988**, 5 seeds.
Flash detection delta **−0.0167** (CI crosses 0) → the gain is specific to cross-frame motion.
Eight rounds of experiments consistently found **degree-preserving nulls never lose to the
real wiring** (static +0.151, E/I +0.099, temporal +0.147, 9/9 phase-diagram cells negative;
edge-count confound excluded: nnz difference 0.06%, weight ratio 1.0006). This reproduces
the direction of arXiv:2604.04033 and forbids any "biological topology is better" claim.

## Paper Story

- **Bottleneck:** connectome-constrained visual GNNs are evaluated on static images with
  stateless propagation; temporal structure is destroyed before the readout.
- **Why prior work is insufficient:** arXiv:2610.10023 trains the fly connectome as a stateless
  GNN on static classification; arXiv:2609.01330 simulates connectome + spiking neurons for
  orientation maps; arXiv:2604.04033 asks whether topology matters under degree-preserving
  nulls. None isolates *which spiking-state mechanism* makes a temporal visual label learnable,
  nor whether stacked mechanisms compose.
- **New insight:** membrane state is the factor that makes motion direction decodable at the
  Kenyon readout (feature std 8.1e-05 → 5.0e-03), while the same state adds nothing to
  instantaneous detection. Attribution requires a mechanism-decomposition ablation and an
  equal-parameter null.
- **Evidence that would convince:** a 5-seed, CI-backed, ceiling-checked comparison across
  stateless / single-mechanism LIF / combined-mechanism LIF / degree-preserving null / A=0,
  plus τ × speed and readout-layer ablations, with all raw logs and the exact script.

## Paper Outline

1. Introduction: temporal labels are invisible to stateless connectome GNNs; question and contribution.
2. Related Work: connectome-constrained vision, spiking GNNs, null-model / negative-result studies, temporal vision benchmarks.
3. Method: fixed graph and eye frontend; stateless baseline; LIF membrane state; the mechanism set
   (homeostasis, adaptive threshold, refractory, E/I signs, learnable τ, readout placement);
   attribution protocol with one-factor-at-a-time and matched controls.
4. Experiments and Results: ceiling, main 5-seed comparison, decomposition ablation,
   null-model and A=0 controls, τ × speed phase diagram, readout-layer sweep, spike-rate/feature-std diagnostics.
5. Discussion: what the gain does and does not imply (no topology advantage), scale-stability
   constraints, synthetic-stimulus limits, venue-level honest scope.
6. Conclusion: mechanism-level finding and open questions.

## Experiment Plan

| Item | Specification |
|---|---|
| Graph | REAL FlyWire v783 edges, Zenodo `10.5281/zenodo.21549559`, `connections_biological.csv.gz` (CC BY 4.0); `A[post,pre]=log1p(syn_count)`, spectral-radius normalisation 0.95/λ. A gz **prefix** is acceptable only if labelled as a prefix subset. |
| Frontend | REAL measured ommatidium coordinates (`right_visual_positions_all_neurons.csv`), Voronoi nearest-neighbour sampling, per-image contrast normalisation. |
| Readout | REAL Kenyon cells from `neuron_annotations_flywire_v2.1.0.tsv.gz`; hop-1/hop-2 layers as ablation, PCA(32) when dim > 2000 (train-only fit). |
| Stimuli | **EXPLICITLY SYNTHETIC** T=8 sequences: `direction` (left/right motion), `flash`, `accel` (constant vs accelerating), speed 1/2/4. Real optical-flow sequences (Sintel / DAVIS-2017) are a later, separately labelled stage. |
| Baselines | stateless GNN (base), A=0, frame-stacked pixel ridge ceiling, degree-preserving rewiring null, sign-shuffled E/I control, sign-preserving-but-random high-order null (later stage). |
| Proposed variants | single-mechanism LIF+homeostasis; **combined** LIF (adaptive threshold + refractory + real E/I signs); learnable τ; readout-follows-spike-front. Every added mechanism gets its own removal ablation. |
| Primary metric | classification accuracy on a fixed 70/30 split; headline = `delta = variant − stateless`. |
| Secondary metrics | 95% bootstrap CI (2000 resamples), BH correction across variants, spike rate, readout feature std, ceiling, peak GPU memory, wall time. |
| Statistics | ≥5 seeds, direction preregistered, BH-FDR q=0.05; **2-seed apparent effects are not findings**; a conclusion's tolerance must not exceed its effect size; conclusions must be re-checked against raw numbers, not script flags. |
| Runtime / Hardware Budget | **novix exp-4090** (`--provider novixlet --resource-pool exp-4090 --gpu --gpu-count 1`) for the experiment batch; local RTX 3060 12 GB / conda `dyg-cold` for verification, figures, writing, compilation. Remote execution is explicitly opted in by the user. |
| Budget guard | **No local wall-clock or step budget on the 4090 task** (user directive 2026-11-07 14:34). Submit without `--max-turns` / `--timeout`, do not block on `watch`; the task runs to the platform's own terminal state, possibly across several automation rounds. Recovery is owned by a later round's Step 0 via `automation-state.json`. If the pool is unavailable, record the failure and do not resubmit the same experiment in a loop. |
| Stopping / stop-and-return | ceiling < 0.90, NaN, missing raw script, or unavailable main condition ⇒ invalid run, return to task design. No tuning-to-significance. Failed runs are retained as evidence. |
| Reproducibility | `query.txt`, `create-response.json`, task id, `watch.log`, `task-result.txt`, `pull.log`, pulled `experiment.py` and `result.json` all under `novix/` in this guidance directory. |

## Expected Results

This section is the machine- and human-readable rule deciding whether a returned novix result
is "acceptable" and therefore whether the local `f-research-v1` writing stages (P6 onward) may start.

**Prerequisite validity (ALL must hold; otherwise the run is INVALID, not a negative result):**
- frame-stacked pixel ceiling ≥ **0.90** (task is learnable, not at a broken-label level);
- `stateless ≤ 0.60` and `A=0 ≤ 0.60` (base cannot solve the temporal label; local reference 0.458);
- all 5 seeds finished for the main conditions; no NaN; `experiment.py` and `result.json` pulled back;
- the pulled script's graph/eye/readout construction is inspectable and its data sources are the public URLs above.

**Minimum acceptable (enter correction/iteration, not writing):**
- `delta(lif_combo − stateless) ≥ +0.15` with 95% bootstrap CI lower bound > 0.

**`expected_strong` (the binding target for entering local paper writing):**
- `delta(lif_combo − stateless) ≥ +0.25` with CI lower bound > 0
  (calibrated against the local single-mechanism result +0.2817, CI [0.2033, 0.3617]);
- **and** `delta(lif_combo − lif_homeostasis) ≥ +0.05` with CI lower bound > 0
  (this is the new contribution axis after the scope correction: stacked mechanisms must add
  something beyond a single substitution, and each addition must be attributable by ablation);
- **and** at least one decomposition ablation shows which mechanism carries the gain.

**Honesty constraint on the null:** `degree_null_lif − lif_homeostasis` must be reported as measured.
If the null is again higher, the claim is phrased as "the gain comes from spiking-state dynamics,
not from connectome-specific wiring". Claiming topology advantage, or hiding the null, is a
fatal integrity failure regardless of the headline delta.

**Failure signal** — any one of the following triggers a stop
- ceiling < 0.90 ⇒ task design failure, return to scenario design;
- prerequisite validity fails ⇒ invalid run, resubmit a corrected design once, do not re-tune;
- minimum not met ⇒ `f-research-v1` autonomous correction loop (P1B/P3A/P5A), **no P6 writing**;
- strong target met ⇒ record an `acceptance-verdict.md` in this directory, then start local
  `f-research-v1` at the appropriate stage with a P0 run root **inside this guidance directory**.

**Verdict values:** `ACCEPT_STRONG` / `ACCEPT_MINIMUM_ITERATE` / `REJECT_INVALID` / `REJECT_NEGATIVE`.
Only `ACCEPT_STRONG` authorises the local writing chain. A `REJECT_NEGATIVE` is kept as evidence
and feeds the next idea round; it never gets rewritten into a positive result.

## Figure and Table Plan

Select visuals only after evidence stabilises; no fixed count and no per-subsection quota.
Candidates: (a) mechanism/attribution schematic; (b) main 5-seed accuracy with 95% CI;
(c) one-factor-at-a-time decomposition table; (d) τ × speed heatmap; (e) spike-rate vs feature-std
diagnostic; (f) null-model comparison. Each must answer a scientific question and be cited near
its first discussion. Figure 1 is the overall framework figure and must show only verified
components.

## Citation Scope

- Keywords: Drosophila connectome, FlyWire / MaleCNS, connectome-constrained GNN, spiking neural
  network, LIF / membrane state, temporal vision, motion direction, null models, negative results.
- Must-cite clusters: arXiv:2604.04033 (topology null models), arXiv:2610.10023 (structure alone),
  arXiv:2609.01330 (connectome + spiking orientation maps), Lappalainen et al. Nature 2024
  doi:10.1038/s41586-024-07939-3 (flyvis), Dorkenwald et al. Nature 2024 doi:10.1038/s41586-024-07558-y,
  Schlegel et al. Nature 2024 doi:10.1038/s41586-024-07686-5, MaleCNS / Cell 2026,
  train-your-fly / connectome / cogstim repositories, SNN efficiency and null-model methodology.
- **Binding f-series rule:** ≥36 distinct verified relevant cited works, strict majority in a
  frozen 3–5-year window; duplicate DOI / arXiv id / normalized title / preprint-vs-published
  versions must be audited in `reference-dedup-audit.md`. Currently **21 first-hand entries**
  are verified in `fly-connectome-cvpr2027/literature/closest-work.md`; the remainder is a
  **P12 gate**, explicitly pending, not assumed satisfied.
- Known duplicate/near-duplicate risks: the two FlyGM ids are different papers; one
  NeuroGraphBench DOI was NOT FOUND in this round and must not be cited until verified.

## Traceability Checklist

| Guidance requirement | Required artifact | Minimum success check | Strong success check | Must appear in paper? |
|---|---|---|---|---|
| Task learnability / ceiling | `novix/pulled/result.json` | ceiling >= 0.90 recorded with raw script | ceiling >= 0.95 and split protocol inspectable | Yes |
| Main 5-seed comparison | `novix/pulled/result.json` | five seeds for stateless and lif_combo | delta >= +0.25 with 95% CI lower bound > 0 | Yes |
| Mechanism decomposition ablation | `novix/pulled/experiment.py` | one-factor removal logged | carrier mechanism identified with CI lower bound > 0 | Yes |
| Degree-preserving null control | `novix/pulled/result.json` | measured delta reported with its sign | real wiring beats the null with CI lower bound > 0 | Yes |
| A=0 and stateless controls | `novix/pulled/result.json` | both <= 0.60 and no NaN | reproduced across all five seeds | Yes |
| Spike rate and readout feature std | `novix/pulled/result.json` | non-empty diagnostics per condition | variance change explained by the mechanism | Optional |
| Reproducibility metadata | `novix/query.txt`, `novix/create-response.json`, `novix/pull.log` | task id and command recorded | pulled script re-runnable locally | No (audit artifact) |

Rows are checked before P2 setup and re-checked at P4/P5; anything `infeasible-with-evidence`
enters the authorised correction loop instead of being silently dropped.

## 9. Constraints and Preferences

- Language: English manuscript; Chinese for internal logs/discussion with the user.
- Artifact boundary: everything (protocols, pulled results, TeX, PDF, audits, manifest) stays
  under this guidance directory; f-research P0 run root lives inside it.
- No submission, no OpenReview registration, no commit/push, no publishing. No timed-task creation
  from inside the workflow. No remote compute other than the explicitly authorised novix exp-4090.
- Credentials never enter guidance, logs, manuscript, or conversation; only field names and paths.
- No workflow/tool/pipeline names, stage ledgers, or internal review dialogue in the manuscript body.
- Manuscript top-level sections exactly the six listed in §4; no appendices added for length.
- Negative and null results are preserved and reported honestly.
- External hard date risk: CVPR 2027 submission 2026-11-16 AOE; user waived internal deadlines,
  but the date cannot be waived and is recorded here.

## Appendix — compact contract extraction

```yaml
topic: spiking-state mechanisms for temporal vision in a connectome-constrained fly-brain GNN
target_venue: CVPR 2027 main (rescue: NeurIPS D&B)
main_claim: membrane state, not biological wiring specificity, makes temporal motion direction decodable; stacked mechanisms must add attributable gain
method: fixed FlyWire graph + real eye frontend + Kenyon readout; stateless vs LIF vs combined-mechanism LIF; one-factor ablations
datasets: Zenodo 21549559 FlyWire v783 edges/annotations/eye positions; SYNTHETIC temporal stimuli; later Sintel/DAVIS-2017
baselines: stateless, A=0, frame-stacked pixel ridge ceiling, degree-preserving null, sign-shuffled E/I
primary_metric: accuracy on fixed 70/30 split; delta vs stateless
secondary_metrics: bootstrap 95% CI, BH q, spike rate, feature std, ceiling, peak VRAM, wall time
expected_minimum: delta(lif_combo - stateless) >= +0.15 with CI lower bound > 0
expected_strong: delta >= +0.25 AND combo - single >= +0.05, both CI lower bound > 0, plus decomposition ablation
strong_result_entry_gate: ACCEPT_STRONG verdict + P5/P5A passed
must_run_experiments: main 5-seed comparison, decomposition, null, A=0, ceiling, tau x speed, readout sweep
must_have_ablations: one-factor-at-a-time for each added mechanism; matched-parameter controls
figure_table_decision_rules: evidence-driven, no fixed count
experiment_traceability: guidance requirement -> artifact -> minimum/strong check table before running
citation_requirements: >=36 unique verified, strict recent majority
citation_dedup_requirements: DOI/arXiv/title/version duplicate audit
local_artifact_policy: run root inside this guidance directory
page_length_policy: current venue limits; otherwise proportionate, no default threshold
single_final_pdf_template_policy: exactly one final compiled PDF
central_question: which spiking-state mechanism makes a temporal visual label learnable, and does stacking compose
intended_reader: CV / neuromorphic / connectome modelling researcher
planned_claim: stated in section 2
observed_finding: unresolved_until_evidence
open_assumptions: 4090 result pending; G8 story gate and P12 citation gate pending
```
