# Frozen experiment commands

All commands use the project `dyg-cold` Conda Python and run inside the run root. `campaign.py` refuses to run without CUDA and records `NVIDIA GeForce RTX 3060`.

## Baseline phase

```powershell
python -m research.campaign --phase baseline --start 1 --end 3
python -m research.campaign --phase baseline --start 4 --end 6
python -m research.campaign --phase baseline --start 7 --end 10
```

## Proposed-method/full matrix phase

```powershell
python -m research.campaign --phase methods --start 1 --end 3
python -m research.campaign --phase methods --start 4 --end 6
python -m research.campaign --phase methods --start 7 --end 10
```

Each module writes `results/<phase>-<ID>.json`. DYN/EQ use five deterministic stratified seeds; graph modules use frozen checkpoint seeds 0–2 where available. No test split is used for selection; `stratified_splits` freezes train/validation/test IDs by seed before fitting.
