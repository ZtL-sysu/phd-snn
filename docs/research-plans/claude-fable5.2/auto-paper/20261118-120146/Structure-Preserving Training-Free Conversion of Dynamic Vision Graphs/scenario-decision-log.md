# Scenario decision log

| Scenario | CCFA | G0 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A. Structure-preserving training-free conversion of dynamic vision graphs | proceed with rescue | pass | pass via Fashion-MNIST/MNIST | pass | pass | pass | pass | pass | pass as pre-registration | pass conditional on strong evidence | Selected |
| B. Layerwise error-carry delta inference for visual graphs | rescue | pass | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | Held; activate only after A falsifier |
| C. Failure census across visual graph families | rescue | pass | diagnostic data only | exposed-test limitation recorded | not re-gated | not re-gated | pass diagnostic | diagnostic only | not re-gated | not re-gated | Protected as diagnostic/rescue |
| D. Fair SNN-vs-quantized-GNN energy comparison | not selected | pass | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | not re-gated | Rejected as primary: hardware constants dominate without silicon |

## Replacement rule

If A's G7 pilot fails, mark A superseded, create a versioned replacement guidance under the same run root, reopen the builder pipeline from CCFA-startup, and carry forward only evidence whose data, split, operator, baseline, and metric identities still match. Do not lower A's expected_strong to make it pass.
