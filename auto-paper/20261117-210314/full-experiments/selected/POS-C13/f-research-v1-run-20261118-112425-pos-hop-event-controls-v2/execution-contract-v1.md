# Execution contract v1 — POS-C13 guidance-v2

## Goal

Complete all `f-research-v1` stages for permutation-equivariant hybrid hop-event coding with explicit ordered/shuffled-hop controls and five split/probe seeds.

## Authorized scope

- Local RTX3060/CPU and Conda `dyg-cold`; Chameleon/Squirrel only.
- Compare raw, uniform, per-channel Lloyd, and hybrid Lloyd+0.5% escapes on `[X,AX,A^2X,A^3X]`.
- Hard gates: hybrid error ≤5%, storage ≥4×, permutation max error ≤1e-10, shuffled-hop error ≥1.25× ordered on both graphs.
- Five probe seeds and five permutation/hop-shuffle seeds; report all rows and negative controls.
- Preserve prior single-split results and independent review limitations.
- No commit, push, submission, remote compute or credential writes.

## Outputs

All evidence and final deliverables remain under this run root.
