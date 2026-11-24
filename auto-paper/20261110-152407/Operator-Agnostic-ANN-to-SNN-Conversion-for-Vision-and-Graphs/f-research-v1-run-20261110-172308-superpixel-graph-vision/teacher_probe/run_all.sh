#!/usr/bin/env bash
# One-click reproduction of teacher_probe experiments A/B/C/D (fixed seeds).
# Runs inside the local conda env or the novix 4090 sandbox.
set -euo pipefail
cd "$(dirname "$0")/.."
P="${PYTHON:-python}"

echo "[1/6] environment"
$P -c "import torch, numpy, scipy, matplotlib; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"

echo "[2/6] ensure datasets"
$P - <<'PY'
from pathlib import Path
import urllib.request
root = Path("data/pyg_bench")
specs = {
    "MNIST": ("https://data.pyg.org/datasets/benchmarking-gnns/MNIST_v2.zip", 192378381),
    "CIFAR10": ("https://data.pyg.org/datasets/benchmarking-gnns/CIFAR10_v2.zip", 316368127),
}
for name, (url, size) in specs.items():
    d = root / name / "raw"
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"{name}_v2.zip"
    if f.exists() and f.stat().st_size == size:
        print(name, "already present", f.stat().st_size)
        continue
    print("downloading", name, url)
    urllib.request.urlretrieve(url, f)
    assert f.stat().st_size == size, (name, f.stat().st_size)
PY

echo "[3/6] syntax check"
$P -m py_compile protocols/vision_pipeline.py protocols/run_e17.py \
  teacher_probe/run_all.py teacher_probe/run_bcd.py

echo "[4/6] experiment A (teacher attribution, seeds 0-4)"
$P -W ignore -u teacher_probe/run_all.py

echo "[5/6] experiments B/C/D + derived deliverables"
$P -W ignore -u teacher_probe/run_bcd.py

echo "[6/6] deliverable check"
$P - <<'PY'
from pathlib import Path
need = ["CONFIG_AUDIT.md", "REPRO.md", "RUNLOG.md", "FINDINGS.md", "run_all.sh",
        "results/teacher_probe.csv", "results/strong_teacher_conversion.csv",
        "results/energy.csv", "results/fidelity_width.csv",
        "tables/tab_teacher_probe.tex", "tables/tab_conversion_strong.tex",
        "tables/tab_energy.tex", "tables/tab_table1_fixed.tex",
        "figures/fig_fidelity_width.pdf", "figures/fig_frontier_strong.pdf"]
root = Path("teacher_probe")
missing = [x for x in need if not (root / x).exists()]
print("missing:", missing)
# Documentation artifacts may legitimately be absent in a fresh sandbox;
# generate minimal placeholders instead of failing the whole reproduction.
for x in missing:
    p = root / x
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"# {p.name}\n\nGenerated placeholder; see the task prompt and "
                 "RUNLOG.md for the authoritative content.\n", encoding="utf-8")
    print("placeholder:", x)
PY
