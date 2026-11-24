# P0 gate report

## Decision

**PASS.** CERT-C11 guidance-v2 is located in its selected guidance directory, the run root is nested inside that directory, and the initial path-containment ledger is present.

## Checks

- Guidance: `inputs/guidance-v2.md`, SHA-256 `e4980f3774b0fbe28d241f8967da7eab360170774448e354b4373a671db819d0`.
- Run root: `f-research-v1-run-20261118-085119-cert-operator-aware-envelope-v2`.
- Pipeline ledger initialized with canonical P0-P21 order and `contract_version: v1`.
- `path-containment-manifest.json` records that outputs remain under the run root; prior external source references are read-only and hash-tracked in `input-manifest.json`.
- Prior CERT-C11 v1 baseline/method rows and independent review are copied into `inputs/` as background evidence only.
- The corrected claim explicitly treats containment as a deterministic validity audit and does not relabel it as independent statistical coverage.
