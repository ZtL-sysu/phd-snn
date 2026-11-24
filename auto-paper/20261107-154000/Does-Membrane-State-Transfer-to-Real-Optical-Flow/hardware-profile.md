# Hardware profile (round 001)

Local, measured with `f-guidance-builder-v1/scripts/hardware_probe.py`: Windows 11, 12 logical cores,
34.25 GB RAM, RTX 3060 12.88 GB, CUDA 12.8, torch 2.11+cu128, conda `dyg-cold`
(`C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe`), TeX Live 2026, PyG 2.8.0, spikingjelly.
Local `light_smoke.py` self-test: 7 variants / 19.2 s / 4.0 GB peak / graph load 2.7 s.

Remote, measured on novix task 17682's `progress.md`: RTX 4090 46,068 MiB, driver 580.126.09,
CUDA 13.0, torch 2.11.0+cu130, `torch.cuda.is_available()=True`, one device. The clean sandbox
initially lacked scipy and scikit-learn; the agent installed them via pip. This is recorded so the
round-001 query lists dependencies explicitly. No wall-clock or turn budget is imposed on the
remote task; `runtime_hours` in the feasibility contract is a planning estimate only.
