# Frozen v2 experiment commands

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m pytest tests -q
python -m research.run_lr_v2 --phase baseline --output results/baseline.json
python -m research.run_lr_v2 --phase method --output results/method.json
python -m research.run_lr_v2 --phase timing --output results/timing.json
python -m research.summarize_lr_v2
```

Grids are fixed. Every method records hidden/logit MSE, task metrics and exact payload/padded bits. Timing uses three warmups and seven measured repeats at rank128/1%.
