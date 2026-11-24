# Correction loop state

- Triggered at P5 strong-result lock.
- Original contract: v1 structure-preserving training-free conversion of dynamic vision graphs.
- Classifier: mechanism/evidence.
- Earliest affected stage: P4 experiment design, because the accepted end-to-end protocol measured structure but did not isolate all numeric-path causes before writing.
- Status: open.
- Prior attempt: local ViG-style teacher, signed uniform/multilevel coding, calibration-scale search, structure metrics, and oracle interventions.
- Evidence: `p4-method-oracle-results.json`.
- Observed: teacher mean 83.60%; calibrated converted mean 50.23%; gap 33.37 pp. Neighbor Jaccard mean 0.7581 and winner agreement 0.6305. Oracle with encoded indices/winners and teacher features recovers mean 83.42%; neighbor-only and both-oracle recover to teacher exactly.
- Interpretation: discrete structure disagreement exists and teacher-feature restoration recovers accuracy, but preserving only neighbor indices and winner indices is insufficient. The remaining loss is in continuous feature reconstruction/message magnitude, so C2/C3 strong targets fail.
- Authorized next action: do not lower the failed target. Preserve this contract as superseded, create versioned guidance v2 from the documented material set with a genuinely different mechanism and fresh baseline calibration.
