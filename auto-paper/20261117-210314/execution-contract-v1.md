# Execution contract v1 — GNN→SNN idea and smoke campaign

Date: 2026-11-17 (Asia/Shanghai).

## Goal and completion

Find ten distinct, mechanistically coherent GNN→SNN research candidates that pass a current primary-source novelty screen and a predeclared local smoke gate. A candidate is accepted only when its actual saved outputs meet its own gate; code execution, finite loss, parity with an ANN at a large T, or a single favorable seed is not a strong smoke result. Novelty means no identified duplicate within the recorded search scope, not proof that no unpublished or unindexed work exists.

## Authorized operations

- Read historical code, evidence, data, and checkpoints without changing frozen assets.
- Search public literature with public keywords, verify primary sources, and record access dates and overlap boundaries.
- Create a new run-local research workspace under `auto-paper/20261117-210314/`; write tests before reusable experiment code and run local Python only with the specified Conda interpreter.
- Run bounded local CPU/CUDA prototype, calibration, and validation experiments. No remote compute, paid APIs, credentials, external submission, or manuscript writing is authorized.
- Reject or replace candidates after novelty, mechanism, data, numerical-correctness, or smoke failure. Do not change a threshold after seeing the result to manufacture a pass; any revised candidate is a new version with a new gate.
- Use independently executed read-only literature and asset audits. The primary agent verifies consequential results and owns final scientific acceptance.

## Environment and resources

- Windows 11, 12 logical CPUs, approximately 32 GiB RAM, NVIDIA RTX 3060 with 12 GiB VRAM, approximately 486 GiB free disk at probe time.
- Conda interpreter: project-specified `dyg-cold` environment; Python 3.13.13, PyTorch 2.11.0+cu128, PyG 2.8.0.post1, CUDA available.
- Preserve GPU access for ordinary desktop use. Run one GPU training driver at a time; parallel workers are read-only or CPU-only.
- Initial discovery screen: up to 512 development graphs per dataset, up to 512 tuning graphs, and 512 disjoint internal validation graphs, all from official training or validation splits with saved IDs. Any broader experiment has its own frozen budget. No test-set reads for candidate generation or selection.
- Initial screen per candidate: at most 20 minutes GPU/CPU experiment time and 12 GiB VRAM; main method plus required controls, at least two datasets when the claim crosses visual graph datasets. Resource exhaustion is a failed/inconclusive screen, not a pass.

## Evidence and protocol

- Historical tests are exposed and may be used only as descriptive anchors. All new selection uses saved train/dev/internal-validation IDs; final official validation remains held out until the final candidate protocol is frozen.
- Reuse only verified terminal strong teachers, their original calibration, and source-equivalent conversion modules. Check hashes/provenance and reproduce reference outputs before new comparisons.
- Every candidate has a versioned mechanism card, closest-work search record, controls, data IDs, metrics, direction, minimum/strong/failure criteria, and stop rule before its smoke run.
- Strong screens require an actual benefit over the strongest feasible matched baseline/control, not merely fidelity to an already easy teacher. Report absolute values, paired per-example differences, uncertainty diagnostics, event/work accounting, and negative results. Smoke acceptance does not establish publication-level novelty, multi-seed robustness, energy savings, or final Q2+ evidence.
- The ten accepted candidates must be genuinely different in bottleneck, mechanism, or evidence question; variants of one threshold/grid/loss are not ten ideas.

## Output

- One portfolio root containing immutable contracts, asset/hardware/literature maps, candidate registry, tests/code, raw outputs, rejection log, and a final ten-candidate evidence index.
- One `auto-paper/20261117-210314/<paper-title>/` guidance package per accepted candidate, with the ordered CCFA/G0–G8 ledger and strict validation required by `f-guidance-builder-v1`. Rejected candidates remain outside accepted guidance folders.
- Update `auto-paper/generated-research-directions.md` only for completed accepted guidance builds. Update collaboration records with verified status and remaining uncertainty.

## Boundaries and preferences

- User language: Chinese summaries; method/paper titles may be English.
- Do not modify historical frozen results, retrain strong teachers, delete archives, change global settings, commit/push, or expose local data/weights/credentials.
- Distinguish direct ANN/GNN→SNN conversion from training a new spiking GNN; distinguish operation counts from measured hardware energy.
- Respect project AGENTS instructions and preserve all unrelated existing work.
