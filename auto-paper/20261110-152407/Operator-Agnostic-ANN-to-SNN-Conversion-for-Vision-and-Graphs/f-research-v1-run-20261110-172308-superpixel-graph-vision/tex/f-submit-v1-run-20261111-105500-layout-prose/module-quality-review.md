# S6 · Module Quality Review

Frozen comparator scores (1--5, field-relative presentation quality): 4.5, 4.3, 4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5. Fourth-highest = **4.1** operational threshold.

| Module | Score | Threshold | Result | Named defect |
|---|---:|---:|---|---|
| Abstract | 3.6 | 4.1 | fail | internal-target phrasing, dense sentences |
| Introduction | 3.7 | 4.1 | fail | "We state our boundaries early", defensive framing |
| Related Work | 4.1 | 4.1 | pass | abrupt supplementary paragraph (fixed in layout round) |
| Method | 4.3 | 4.1 | pass | none after equation rewrap |
| Experiments | 4.2 | 4.1 | pass | table geometry (fixed in layout round) |
| Discussion | 3.5 | 4.1 | fail | workflow narration, internal-target sentence |
| Conclusion | 3.8 | 4.1 | fail | internal-target sentence |
| Figures/Tables | 3.2 | 4.1 | fail | ruler overlap, overflow, truncated exponents |

Humanizer decision: named passage-level defects only (internal-target wording, defensive openers, screening narration); `no defect` recorded for Method and Experiments prose.
