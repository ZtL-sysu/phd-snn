# Hardware Profile

## Local Experiment Machine

- Role: experiments, training, evaluation, preprocessing, writing, TeX compilation, and artifact preparation by default.
- OS: Windows 11.
- CPU: 12 logical CPUs.
- RAM: not exposed by the privacy-safe probe; record actual process observations during runs.
- GPU: NVIDIA GeForce RTX 3060.
- GPU memory: 12 GB.
- Disk free: 517,243,854,848 bytes at probe time.
- CUDA: available; PyTorch 2.11.0+cu128.
- Apple MPS available: false.
- Conda/Python: Python 3.13.13.
- Selected Conda environment: `C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`.
- Key probes: `f-guidance-builder-v1/scripts/hardware_probe.py`, direct PyTorch CUDA probe, local dataset/teacher metadata inspection.

## Optional Remote Compute

- Enabled only when explicitly authorized after local feasibility fails.
- Role: none authorized.
- Endpoint reference: none; no credentials recorded.
- Artifact synchronization plan: not applicable.

## Experiment Budget

- Maximum runtime per run: 4 hours.
- Maximum total runtime: 24 hours for the first contract.
- Maximum number of runs: guided by 12 search trials and all required seeds/ablations.
- Maximum dataset size: 60,000 training images or locally available graph datasets for diagnostics.
- Maximum model size: small ViG-style Grapher, expected below 8 GB GPU memory.

## Feasibility Notes

- Expected bottleneck: Grapher kNN implementation and fair event-count accounting.
- Scaling strategy: begin with a 64-sample smoke prototype; use Fashion-MNIST/MNIST patch graphs before larger images.
- Risks: dynamic operator implementation, unlicensed upstream code, historically exposed local test sets.
- Assumptions: local RTX 3060 remains available and no remote execution is used.
