# Concern-to-action ledger

| Review round | Blocking concern | Resolution | Status |
|---|---|---|---|
| v2 | operator order ambiguous | frozen exact `M→Q→A·relu→A·W1` chain | resolved |
| v2 | weak/undefined comparator | valid Minkowski comparator and outputwise global-radius comparator | resolved |
| v3 | impossible tightening on global-uniform cells | equality control for global-uniform; tightening gate only per-channel | resolved |
| v3 | float32/zero-radius ambiguity | all computation in float64; constant channel identity with zero radius | resolved |
| v4 | node/channel index mixed | reduced formula `c_i sum_h delta_h|W1_hk|` with `c=(|A||A|)1` | resolved |
| v5 | contract extraction wrote `M:MxH` | corrected to `M:NxH`; old accepted file preserved | resolved |

No strong threshold was weakened. The final independent verdict is `proceed` with score 10/10 for contract readiness.
