# Hardware profile

Probed 2026-11-04 on the machine that will run every experiment in this guidance.

| item | value |
|---|---|
| OS | Windows 11 10.0.26200 |
| CPU | AMD64 Family 25 Model 80, 12 logical cores |
| RAM | 31.9 GB |
| GPU | NVIDIA RTX 3060, 12 288 MiB, CUDA available (torch 2.11 + cu128) |
| Disk free | 526 GB on C: |
| Python | 3.13.13, conda env base at `C:\Users\xhf\miniconda3\python.exe` |
| Key packages | torch 2.11, numpy 2.4, scipy 1.18, pandas, torch-geometric |
| LaTeX | pdflatex + latexmk, TeX Live (builds the 17-page manuscript in ~20 s) |

## Device policy (measured, not assumed)

ANN training runs on **CPU by default**. Measured: the same code on CUDA moves the PubMed ANN from
0.7757 to 0.7826 (+0.69 pp, 7 seeds), because sparse-matrix reduction order on the GPU is not fixed
and early stopping then lands on a different epoch. That is larger than several effects this paper
reports, so a GPU training run is a different experiment, not a faster one. CUDA is used only where
it is bit-neutral (not in the current plan) and any GPU sweep must carry a device-pair noise
measurement.

The spiking simulation is NumPy and stays on CPU: the `T`-step loop is dominated by Python and
kernel-launch overhead, and on a 2.7k-node graph the GPU gives no gain for it.

## Capacity check against the plan

Estimated 40 h total. Measured throughput from the predecessor run: a full 7-seed
(dataset × 3 depths) block takes ≈25 min on the 12 cores, and the complete 7-seed baseline suite
takes ≈7 min per arm on the GPU or ≈2 h on CPU. The 20 h prediction grid is therefore the only
long-running item, and it is embarrassingly parallel across seeds. No remote execution is requested
or assumed.
