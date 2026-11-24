# P3A baseline numeric audit

Mode: `ccf-integrity-auditor` numeric-audit.

- Every baseline JSON parses with finite metrics and explicit units/directions.
- Accuracy/balanced accuracy are higher-is-better; errors/compression ratios are labeled separately.
- DYN and DLY raw baselines are identical because both phases use the same raw representation; this is expected and cannot be counted twice as independent evidence.
- LR compression uses raw `A X` matrix elements over `rank*(N+F)`, matching the frozen contract after correction.
- Edge error is norm-relative; bit reduction is `32/bits`; no energy claim is made.
- CERT coverage is empirical error containment; width/RMS and tightening are separate.

Severity: no numeric inconsistency in accepted baseline files. The earlier invalid LR file is superseded and not cited.

No-invention status: **pass**.
