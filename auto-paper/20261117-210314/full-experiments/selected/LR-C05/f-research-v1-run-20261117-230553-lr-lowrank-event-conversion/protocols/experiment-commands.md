# Frozen LR experiment commands

Run from the run root with project Conda Python.

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m pytest tests -q
python -m research.run_lr_experiments --phase baseline
python -m research.run_lr_experiments --phase method
python -m research.summarize_lr_results
```

The experiment driver refuses to run without CUDA and writes raw JSON under `results/`. It reads Cora/Chameleon/Squirrel local data and frozen checkpoints read-only. Baseline outputs precede proposed-method outputs; every graph/checkpoint/rank/budget row is retained.
