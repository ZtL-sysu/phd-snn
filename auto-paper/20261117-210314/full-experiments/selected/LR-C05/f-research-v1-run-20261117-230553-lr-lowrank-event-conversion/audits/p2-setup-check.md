# P2 setup and protocol check

- Python 3.13.13, PyTorch 2.11.0+cu128, CUDA RTX 3060, PyG 2.8.0.post1, SciPy/sklearn/pandas available.
- Run-local `config.arc.yaml` contains no credential; `researchclaw validate --config config.arc.yaml` passes.
- `researchclaw doctor --config config.arc.yaml` passes with an available DeepSeek executor model; the credential is supplied only through `DEEPSEEK_API_KEY` at invocation and is never written to artifacts.
- ARC stage mapping is verified from `pipeline/stages.py`, `pipeline/contracts.py`, `pipeline/executor.py` and `_paper_writing.py`.
- New LR primitives and the full driver compile; 7/7 tests pass. Baseline and method commands are frozen.

Verdict: **pass**.
