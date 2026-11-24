# P10 — concern-to-action revision log

| concern | proposition | action | target | factual check |
|---|---|---|---|---|
| falsified inversion still asserted | Intro contribution 3, Discussion close, Conclusion | REWRITE | `tex/main.tex` | all numbers preserved via macros; no citation or equation changed |
| `expected_strong` unmet | Section 4.3 | KEEP + NARROW | `tex/main.tex` | negative result retained with mechanism |
| dense Section 4.3 | transition | KEEP | `tex/main.tex` | no new claim |

Revision script: `contracts/revision_p10.py`. Post-revision claim scan: 0 occurrences of
"no timestep sweep is needed" and 0 of "inverting the bound lets". Recompile: 0 errors,
0 undefined citations, 0 undefined references.
