# CCFA Full Integrity Audit

review_execution: independent-agent

## Integrity Verdict

**REVISE**

**Score: 8.2/10**  
**Confidence: high**

The numerical, control and negative-evidence integrity is strong. Revision is required for missing bibliography/provenance metadata and minor scope presentation.

## Numeric Consistency

- Representation rows: 8; permutation rows: 10; shuffle rows: 10.
- Task rows: 40; fixed-probe rows: 90.
- Hybrid representation errors: 3.952% / 4.879%.
- Storage reductions: 7.490x / 7.602x.
- Permutation maxima: `2.22e-16`.
- Shuffle means: 3.725x / 3.626x; minima 3.454x / 3.310x.
- Task paired loss/gain: -0.083 pp / +0.768 pp.
- Fixed ordered-minus-shuffled gaps: 9.566 pp / 9.081 pp.
- Table 2 means, sample SD and paired min/max match raw task rows exactly.
- Bit ledger recomputes exactly from `4 + 32 f_escape + 256/N`; storage recomputes exactly as `32/b_avg`.

## Probe Split Integrity

The preserved leaky run has near-99% task accuracy, while corrected train-only rows fall to plausible values. Corrected and leaky runs share identical representation error, escape, bit and storage fields, supporting a probe-only repair. `experiment-traceability.md` states train-only codebook/escape fitting and fixed probe reuse; row-level fit/split/probe hashes should be linked for final reproducibility.

## Formula And Claim Mapping

- `H=[X,AX,A^2X,A^3X]` and `B_avg` formulas are correct.
- Hybrid claim is fidelity/storage/retention, not accuracy superiority.
- Mismatched-shuffle ratio is labeled codebook-order sensitivity.
- Fixed-probe gaps are descriptive and not causal.
- Scope excludes temporal spikes, energy, hardware, dynamic graphs and full graph-transformer conversion.

## Figures And Tables

- Figure source data and assets exist for Figures 1–3.
- Table 1 contains the exact ledger and method roles.
- Table 2 contains paired five-seed dispersion and mixed outcomes.
- Figure 3 caption appropriately separates permutation and shuffle controls.

## Numbered Integrity Concerns

1. **Major:** 31 citation keys have no bibliography file in the run root.
2. **Medium:** task rows lack explicit fit-scope, split-index and probe-weight hashes.
3. **Low:** “event” terminology may be read as temporal spike evidence.
4. **Low:** runtime metadata and packet framing are excluded but should remain explicit in limitations.

**Recommendation:** revise for bibliography and provenance hardening. No numeric fabrication or control inconsistency remains.
