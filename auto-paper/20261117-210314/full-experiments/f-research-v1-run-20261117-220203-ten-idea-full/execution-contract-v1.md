# Execution contract v1 — ten-idea full experiment campaign

Date: 2026-11-17 Asia/Shanghai.

## User goal

Use `f-research-v1` to execute the ten accepted ideas in order with full local experiments and result records, then deliver one Markdown report containing each idea's story, actual results, and independent CCFA scoring.

## Authorized scope

- Read/hash existing local data, frozen checkpoints, prior smoke code and literature artifacts.
- Write only inside this run root; do not modify frozen historical evidence.
- Run local CPU/CUDA experiments in `dyg-cold`; no remote compute, credentials, submission, commit or push.
- Baselines first; tune only on training/validation; preserve failures and all trial counts.
- Use independent CCFA review for the final stories/results. User-requested Markdown overrides a paper PDF deliverable; experimental P0–P5A evidence rules remain binding.

## Inputs

- `../guidance.md` and the prior portfolio packet/evidence manifest.
- Local DAVIS clips, MaleCNS annotations, FlyWire edge weights, graph loaders/checkpoints.
- Installed Python 3.13.13, PyTorch 2.11.0+cu128, PyG 2.8.0.post1, NumPy/SciPy/sklearn/pandas.

## Quality and resource envelope

- Ten modules in canonical order; each has a frozen matrix/minimum/strong/failure gate.
- Five seeds for temporal/coordinate modules; graph seeds 0–2 where available; deterministic splits saved before execution.
- Max 20 minutes/12 GiB per module, one GPU driver, all evidence and logs in the run root.
- A failed strong target is not rewritten as success; it is recorded and its claim narrowed or marked unsupported.
