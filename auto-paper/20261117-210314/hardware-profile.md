# Hardware profile

Probe date: 2026-11-17. Local execution only.

| Resource | Measured/probed value |
|---|---|
| OS | Windows 11 AMD64 |
| CPU | 12 logical processors |
| RAM | 33,446,280 KiB total; 16,905,768 KiB free at probe |
| GPU | NVIDIA GeForce RTX 3060, compute capability 8.6 |
| VRAM | 11.9995 GiB total |
| Python | 3.13.13, project `dyg-cold` Conda environment |
| ML runtime | PyTorch 2.11.0+cu128; PyG 2.8.0.post1; CUDA available |
| Other packages | NumPy, SciPy, scikit-learn, pandas, SpikingJelly, pytest available; OGB and snnTorch absent |
| Disk | 521,491,755,008 bytes free on workspace drive at probe |
| Probe | `hardware_probe.py` executed with the project interpreter; native CUDA/PyTorch/OS checks executed |

No active Python/Conda research process was observed at campaign startup. Desktop processes are not research jobs.

## Budget policy

Reuse frozen 101k-parameter visual GCN teachers and existing graph datasets. Run a single GPU driver, limit initial screening to 512 development/tuning/validation graphs per partition and 20 minutes per candidate, and use CPU workers for citation/small-graph screens. Record actual elapsed time and peak CUDA memory where available. No remote fallback is authorized.
