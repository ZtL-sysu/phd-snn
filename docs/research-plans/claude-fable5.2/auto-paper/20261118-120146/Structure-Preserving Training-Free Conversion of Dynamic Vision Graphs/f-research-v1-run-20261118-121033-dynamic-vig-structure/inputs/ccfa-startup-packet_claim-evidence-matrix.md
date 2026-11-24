# Claim-evidence matrix

| Claim | Mechanism | Required evidence | Minimum | Expected strong | Failure / falsifier |
|---|---|---|---|---|---|
| C1: activation quantization causes measurable discrete structure disagreement in dynamic vision graphs | Distance perturbation and signed max winner perturbation convert small numeric errors into neighbor/winner flips | Calibration subset and held-out test; layerwise neighbor Jaccard and max-winner agreement; multiple seeds | Disagreement is finite and measurable on at least one teacher/layer | Conversion baseline causes >=5 pp neighbor-Jaccard drop or >=2 pp winner-agreement drop at T<=4 versus teacher | <1% disagreement and <1 pp accuracy gap at T=4 |
| C2: teacher-structure calibration improves conversion without extra inference-time transport | Calibration chooses thresholds/offsets by minimizing structure disagreement, not only activation MSE | Matched event/cost budget; calibration-only tuning; frozen test | No worse than matched baseline beyond seed noise | >=50% recovery of baseline structure-disagreement loss at matched events, with accuracy loss <=1 pp versus teacher | Calibration cannot recover any disagreement or requires extra test-time graph oracle |
| C3: preserving discrete structure explains accuracy recovery | Teacher-neighbor and teacher-winner interventions are causal probes | Intervention matrix: baseline, method, neighbor oracle, winner oracle, both-oracle | All interventions run and preserve split identity | Method recovers at least half the oracle recovery achieved by restoring teacher structure at matched budget | Oracle restoration gives <1 pp gain or method gains when structure is unchanged |

## Required runs

- R0: public-data and license verification.
- R1: small licensed dynamic-graph teacher implementation and reproduction on CIFAR-10.
- R2: baseline conversion matrix for T in {2,4,8}: direct rate coding, signed uniform quantization control, signed multi-threshold coding.
- R3: method variants: activation-MSE calibration, structure-only calibration, combined calibration.
- R4: ablations and interventions: teacher-neighbor oracle, teacher-winner oracle, both, random neighbor control.
- R5: three seeds, fixed split, calibration/train only, final test isolation, event count and latency ledger.

## Statistical rule

- Report all seeds, means, and sample SD. Use paired comparisons over identical examples and seeds for structure metrics. No held-out test value may guide tuning; any adaptive use is recorded as exposed and requires a fresh holdout.
