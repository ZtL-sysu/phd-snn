# P4 task and control gate

## Decision

**PASS.** The corrected five-seed task/probe matrix meets every binding gate.

## Results

- Hybrid error max: 3.967% Chameleon, 4.860% Squirrel.
- Conservative storage minimum: 7.476× Chameleon, 7.591× Squirrel.
- Retrained hybrid balanced-accuracy loss versus raw: +0.083 pp loss on Chameleon and −0.768 pp on Squirrel (a gain).
- Fixed raw-probe ordered minus shuffled balanced accuracy: +9.57 pp Chameleon and +9.08 pp Squirrel.
- Forty retrained rows and ninety fixed-probe rows are complete.

The earlier full-data probe-fitting run is preserved as negative evidence and excluded from the accepted result. Corrected probes train only on split train indices, select epochs on validation, and evaluate once on test.
